from __future__ import annotations

import hashlib
import re
import subprocess
import tempfile
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / "themes" / "srwf-registration"
CSS = THEME / "src" / "srwf-registration.css"
PHP = THEME / "src" / "srwf-registration-theme.php"
MAP = THEME / "IMPLEMENTATION_MAP.md"
REFERENCE = THEME / "reference" / "materialize_reference.sh"
NARROW_SCOPE = ".gform-theme--framework.srwf-registration-theme_wrapper"
ENFORCED_SCOPE = "head:has(#gravity_forms_theme_framework-css) + body .gform-theme--framework.gform-theme.srwf-registration-theme_wrapper"
ACTIVATION_CLASS = ".srwf-registration-theme_wrapper"
HOSTILE_ORBITAL_SELECTOR = '#gform_wrapper_1[data-form-index="0"].gform-theme'
REFERENCE_SHA256 = "436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000"

REVIEWED_GF_API = {
    "--gf-font-family-base",
    "--gf-color-primary",
    "--gf-color-primary-rgb",
    "--gf-color-danger",
    "--gf-color-danger-rgb",
    "--gf-color-success",
    "--gf-color-success-rgb",
    "--gf-ctrl-bg-color",
    "--gf-ctrl-color",
    "--gf-ctrl-border-color",
    "--gf-ctrl-border-color-focus",
    "--gf-ctrl-border-color-error",
    "--gf-ctrl-radius",
    "--gf-ctrl-size",
    "--gf-ctrl-font-size",
    "--gf-ctrl-font-weight",
    "--gf-ctrl-choice-size",
    "--gf-ctrl-radio-check-size",
    "--gf-ctrl-label-color-primary",
    "--gf-ctrl-label-font-size-primary",
    "--gf-ctrl-label-font-weight-primary",
    "--gf-ctrl-desc-color",
    "--gf-ctrl-desc-color-error",
    "--gf-ctrl-btn-bg-color-primary",
    "--gf-ctrl-btn-bg-color-hover-primary",
    "--gf-ctrl-btn-bg-color-focus-primary",
    "--gf-ctrl-btn-color-primary",
    "--gf-ctrl-btn-radius",
    "--gf-ctrl-btn-size",
    "--gf-ctrl-btn-font-size",
    "--gf-ctrl-btn-font-weight",
    "--gf-ctrl-file-zone-radius",
    "--gf-field-section-border-color",
    "--gf-form-validation-heading-color",
}


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def css_blocks(css: str) -> list[tuple[str, str]]:
    clean = strip_comments(css)
    return [
        (match.group(1).strip(), match.group(2))
        for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean, flags=re.S)
    ]


def gf_token_declarations(body: str) -> list[tuple[str, str]]:
    return re.findall(
        r"(?m)^\s*(--gf-[a-z0-9-]+)\s*:\s*([^;]+);",
        body,
    )


def gf_token_blocks(css: str) -> list[tuple[str, str]]:
    return [
        (selectors, body)
        for selectors, body in css_blocks(css)
        if gf_token_declarations(body)
    ]


def split_selector_list(selector_list: str) -> list[str]:
    parts: list[str] = []
    start = 0
    paren_depth = 0
    bracket_depth = 0
    quote: str | None = None
    escaped = False

    for index, char in enumerate(selector_list):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote is not None:
            if char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth -= 1
        elif char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
        elif char == "," and paren_depth == 0 and bracket_depth == 0:
            parts.append(selector_list[start:index].strip())
            start = index + 1

    parts.append(selector_list[start:].strip())
    return [part for part in parts if part]


def consume_identifier(selector: str, index: int) -> int:
    while index < len(selector):
        char = selector[index]
        if char == "\\" and index + 1 < len(selector):
            index += 2
            continue
        if char.isalnum() or char in "_-":
            index += 1
            continue
        break
    return index


def consume_balanced(
    selector: str,
    index: int,
    opener: str,
    closer: str,
) -> tuple[int, str]:
    if selector[index] != opener:
        raise ValueError(f"expected {opener!r} at offset {index}")

    depth = 1
    quote: str | None = None
    escaped = False
    cursor = index + 1

    while cursor < len(selector):
        char = selector[cursor]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif quote is not None:
            if char == quote:
                quote = None
        elif char in {'"', "'"}:
            quote = char
        elif char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return cursor + 1, selector[index + 1 : cursor]
        cursor += 1

    raise ValueError(f"unbalanced {opener}{closer} in selector: {selector}")


def selector_specificity(selector: str) -> tuple[int, int, int]:
    """Calculate specificity for the selector forms used by this theme.

    Selectors Level 4 functional pseudo-classes :is(), :not(), and :has()
    contribute the maximum specificity of their argument selector list;
    :where() contributes zero.
    """

    ids = classes = types = 0
    index = 0

    while index < len(selector):
        char = selector[index]

        if char.isspace() or char in ">+~,":
            index += 1
            continue

        if char == "#":
            ids += 1
            index = consume_identifier(selector, index + 1)
            continue

        if char == ".":
            classes += 1
            index = consume_identifier(selector, index + 1)
            continue

        if char == "[":
            classes += 1
            index, _ = consume_balanced(selector, index, "[", "]")
            continue

        if char == ":":
            if index + 1 < len(selector) and selector[index + 1] == ":":
                types += 1
                index = consume_identifier(selector, index + 2)
                if index < len(selector) and selector[index] == "(":
                    index, _ = consume_balanced(selector, index, "(", ")")
                continue

            name_start = index + 1
            name_end = consume_identifier(selector, name_start)
            name = selector[name_start:name_end].lower()
            index = name_end

            if index < len(selector) and selector[index] == "(":
                index, arguments = consume_balanced(selector, index, "(", ")")
                if name in {"is", "not", "has"}:
                    argument_specificities = [
                        selector_specificity(argument)
                        for argument in split_selector_list(arguments)
                    ]
                    arg_ids, arg_classes, arg_types = max(
                        argument_specificities,
                        default=(0, 0, 0),
                    )
                    ids += arg_ids
                    classes += arg_classes
                    types += arg_types
                elif name != "where":
                    classes += 1
                continue

            classes += 1
            continue

        if char == "*":
            index += 1
            continue

        if char == "|":
            index += 1
            continue

        if char.isalpha() or char in "_-":
            types += 1
            index = consume_identifier(selector, index)
            continue

        raise ValueError(f"unsupported selector token {char!r} at offset {index}: {selector}")

    return ids, classes, types


class SrwfRegistrationStaticTests(unittest.TestCase):
    def test_reference_materializes_to_admitted_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "OWNER_REFERENCE_new_7.html"
            subprocess.run(["bash", str(REFERENCE), str(output)], check=True, capture_output=True, text=True)
            digest = hashlib.sha256(output.read_bytes()).hexdigest()
            self.assertEqual(REFERENCE_SHA256, digest)

    def test_css_uses_only_reviewed_gravity_forms_api_identifiers(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        used = set(re.findall(r"--gf-[a-z0-9-]+", css))
        self.assertEqual(REVIEWED_GF_API, used)

    def test_token_enforcement_specificity_outranks_orbital_per_form_scope(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        token_blocks = gf_token_blocks(css)
        self.assertEqual(1, len(token_blocks), "expected one SRWF --gf-* enforcement block")

        selector_group, _ = token_blocks[0]
        selectors = split_selector_list(selector_group)
        self.assertEqual(1, len(selectors), "token enforcement should not need parallel selector paths")

        host_specificity = selector_specificity(HOSTILE_ORBITAL_SELECTOR)
        enforcement_specificity = selector_specificity(selectors[0])

        self.assertEqual((1, 2, 0), host_specificity)
        self.assertGreater(
            enforcement_specificity,
            host_specificity,
            f"{selectors[0]} does not outrank {HOSTILE_ORBITAL_SELECTOR}",
        )

    def test_token_enforcement_boundary_is_documented_theme_framework_scope(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        token_blocks = gf_token_blocks(css)
        self.assertEqual(1, len(token_blocks))

        for selector in split_selector_list(token_blocks[0][0]):
            self.assertIn("head:has(#gravity_forms_theme_framework-css)", selector)
            self.assertIn(".gform-theme--framework", selector)
            self.assertIn(".gform-theme", selector)
            self.assertIn(ACTIVATION_CLASS, selector)
            self.assertNotRegex(selector, r"#gform_wrapper_\d+")

    def test_unrelated_form_is_excluded_from_token_enforcement_structurally(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        token_blocks = gf_token_blocks(css)
        self.assertEqual(
            1,
            len(token_blocks),
            "an alternate --gf-* block could bypass opt-in isolation",
        )

        selectors = split_selector_list(token_blocks[0][0])
        self.assertTrue(selectors)
        for selector in selectors:
            self.assertIn(
                ACTIVATION_CLASS,
                selector,
                f"token selector does not require SRWF opt-in: {selector}",
            )

    def test_every_reviewed_gf_token_is_under_the_repaired_boundary(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        token_blocks = gf_token_blocks(css)
        self.assertEqual(1, len(token_blocks))

        declarations = gf_token_declarations(token_blocks[0][1])
        self.assertEqual(REVIEWED_GF_API, {name for name, _ in declarations})

    def test_gf_token_values_have_single_implementation_source(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        declarations = [
            name
            for _, body in css_blocks(css)
            for name, _ in gf_token_declarations(body)
        ]
        counts = Counter(declarations)

        self.assertEqual(REVIEWED_GF_API, set(counts))
        self.assertTrue(
            all(count == 1 for count in counts.values()),
            f"duplicate --gf-* declarations found: {counts}",
        )

    def test_non_token_selectors_remain_under_the_bounded_opt_in_scope(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        for selector_group, body in css_blocks(css):
            if gf_token_declarations(body):
                continue
            for selector in split_selector_list(selector_group):
                self.assertTrue(
                    selector.startswith(NARROW_SCOPE) or selector.startswith(ENFORCED_SCOPE),
                    f"non-token selector escaped bounded SRWF scope: {selector}",
                )
                if selector.startswith(ENFORCED_SCOPE):
                    self.assertIn(".gform_button", selector, "strong enforcement is reserved for proven Submit conflict")

    def test_unresolved_values_are_not_promoted(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        self.assertNotIn("!important", css)
        self.assertNotIn("@media", css)
        self.assertNotIn("box-shadow", css)
        self.assertNotIn("--gf-form-gap-y", css)
        self.assertNotIn("grid-template-columns", css)
        self.assertNotIn("--gf-ctrl-outline-width-focus", css)
        self.assertNotIn("--gf-ctrl-outline-color-focus", css)
        title = re.search(
            r"\.gform-theme--framework\.srwf-registration-theme_wrapper \.gform_title\s*\{([^}]*)\}",
            css,
            re.S,
        )
        self.assertIsNotNone(title)
        title_body = title.group(1)
        self.assertIn('font-family: "Vazirmatn", system-ui, sans-serif;', title_body)
        for unresolved in ("font-size", "line-height", "margin", "padding"):
            self.assertNotIn(unresolved, title_body)
        self.assertNotRegex(css, r"#gform_wrapper_\d+")
        self.assertNotIn("[data-parent-form]", css)

    def test_submit_enforcement_reuses_mechanically_stronger_framework_sentinel(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        submit_selectors = [
            selector
            for selector_group, body in css_blocks(css)
            if "inline-size: 100%;" in body
            for selector in split_selector_list(selector_group)
            if ".gform_button" in selector
        ]
        self.assertEqual(2, len(submit_selectors))
        hostile_per_form = selector_specificity(HOSTILE_ORBITAL_SELECTOR)
        self.assertEqual((1, 2, 0), hostile_per_form)
        for selector in submit_selectors:
            self.assertTrue(selector.startswith(ENFORCED_SCOPE))
            self.assertIn(".gform_button", selector)
            repaired = selector_specificity(selector)
            self.assertEqual((1, 5, 2), repaired)
            self.assertGreater(repaired, hostile_per_form)

    def test_tom_select_adapter_is_runtime_proven_scoped_and_reuses_control_size(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        adapter = re.search(
            r"\.gform-theme--framework\.srwf-registration-theme_wrapper \.ts-wrapper \.ts-control\s*\{([^}]*)\}",
            css,
            re.S,
        )
        self.assertIsNotNone(adapter)
        self.assertIn("min-block-size: var(--gf-ctrl-size);", adapter.group(1))
        self.assertNotRegex(css, r"(?m)^\s*\.ts-control\s*\{")
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))

    def test_heading_family_projection_does_not_resolve_title_metrics(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        section = re.search(
            r"\.gfield--type-section \.gsection_title\s*\{([^}]*)\}",
            css,
            re.S,
        )
        self.assertIsNotNone(section)
        self.assertIn('font-family: "Vazirmatn", system-ui, sans-serif;', section.group(1))
        self.assertIn("font-size: 18px;", section.group(1))
        self.assertIn("font-weight: 700;", section.group(1))

    def test_gpfup_report_mapping_is_role_scoped_and_photo_safe(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        implementation_map = MAP.read_text(encoding="utf-8")
        self.assertIn(".gpfup__droparea", css)
        self.assertIn(".srwf-role-report-card-upload", css)
        self.assertIn(".gpfup:not(.gpfup--has-files)", css)
        self.assertNotIn("gpfup--images-only", css)
        self.assertIn("AUTHENTIC_RUNTIME_PROVEN_HOST_STATE", implementation_map)
        self.assertIn("Student Photo post-upload", implementation_map)
        self.assertIn("NOT_IMPLEMENTED", implementation_map)

    def test_activation_is_explicit_class_scoped_and_form_id_free(self) -> None:
        php = PHP.read_text(encoding="utf-8")
        self.assertIn("srwf-registration-theme", php)
        self.assertIn("gform_form_theme_slug", php)
        self.assertIn("gform_enqueue_scripts", php)
        self.assertIn("return 'orbital';", php)
        self.assertNotRegex(php, r"gform_(?:enqueue_scripts|form_theme_slug)_\d+")

    def test_no_mockup_behavior_javascript_was_added(self) -> None:
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))

    def test_no_premature_top_level_shared_implementation(self) -> None:
        shared_files = sorted(
            path.relative_to(REPO).as_posix()
            for path in (REPO / "src").glob("**/*")
            if path.is_file()
        )
        self.assertEqual(["src/README.md"], shared_files)

    def test_implementation_map_preserves_all_resolution_states(self) -> None:
        text = MAP.read_text(encoding="utf-8")
        for marker in (
            "RUNTIME_REQUIRED",
            "NOT_PROVEN",
            "NON_NORMATIVE_REFERENCE",
            "DEFER_NOT_PROVEN",
            "Desktop short-field pairings",
            "Desktop shadow",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
