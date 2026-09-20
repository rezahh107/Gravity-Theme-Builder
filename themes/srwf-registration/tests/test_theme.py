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
    "--gf-ctrl-line-height",
    "--gf-ctrl-select-padding-x",
    "--gf-ctrl-outline-color-focus",
    "--gf-ctrl-outline-width-focus",
    "--gf-ctrl-outline-offset",
    "--gf-ctrl-outline-style",
    "--gf-ctrl-label-color-primary",
    "--gf-ctrl-label-font-size-primary",
    "--gf-ctrl-label-font-weight-primary",
    "--gf-ctrl-label-line-height-primary",
    "--gf-label-space-primary",
    "--gf-label-space-x-secondary",
    "--gf-ctrl-desc-color",
    "--gf-ctrl-desc-font-size",
    "--gf-ctrl-desc-font-weight",
    "--gf-ctrl-desc-line-height",
    "--gf-ctrl-desc-color-error",
    "--gf-ctrl-desc-font-size-error",
    "--gf-ctrl-desc-font-weight-error",
    "--gf-ctrl-desc-line-height-error",
    "--gf-desc-space",
    "--gf-ctrl-btn-bg-color-primary",
    "--gf-ctrl-btn-bg-color-hover-primary",
    "--gf-ctrl-btn-bg-color-focus-primary",
    "--gf-ctrl-btn-color-primary",
    "--gf-ctrl-btn-radius",
    "--gf-ctrl-btn-size",
    "--gf-ctrl-btn-font-size",
    "--gf-ctrl-btn-font-weight",
    "--gf-ctrl-btn-line-height",
    "--gf-ctrl-file-zone-radius",
    "--gf-field-section-border-color",
    "--gf-form-validation-heading-color",
    "--gf-form-gap-y",
}


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def css_blocks(css: str) -> list[tuple[str, str]]:
    clean = strip_comments(css)
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean, flags=re.S)]


def gf_token_declarations(body: str) -> list[tuple[str, str]]:
    return re.findall(r"(?m)^\s*(--gf-[a-z0-9-]+)\s*:\s*([^;]+);", body)


def gf_token_blocks(css: str) -> list[tuple[str, str]]:
    return [(selectors, body) for selectors, body in css_blocks(css) if gf_token_declarations(body)]


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


def consume_balanced(selector: str, index: int, opener: str, closer: str) -> tuple[int, str]:
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
                    arg = max((selector_specificity(a) for a in split_selector_list(arguments)), default=(0, 0, 0))
                    ids += arg[0]
                    classes += arg[1]
                    types += arg[2]
                elif name != "where":
                    classes += 1
                continue
            classes += 1
            continue
        if char == "*" or char == "|":
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
            self.assertEqual(REFERENCE_SHA256, hashlib.sha256(output.read_bytes()).hexdigest())

    def test_css_uses_only_reviewed_gravity_forms_api_identifiers(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        self.assertEqual(REVIEWED_GF_API, set(re.findall(r"--gf-[a-z0-9-]+", css)))

    def test_token_enforcement_specificity_outranks_orbital_per_form_scope(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        root_token_blocks = [
            (selectors, body)
            for selectors, body in gf_token_blocks(css)
            if selectors.strip().startswith(ENFORCED_SCOPE)
        ]
        self.assertEqual(1, len(root_token_blocks), "expected one root SRWF --gf-* enforcement block")
        selectors = split_selector_list(root_token_blocks[0][0])
        self.assertEqual(1, len(selectors))
        self.assertEqual((1, 2, 0), selector_specificity(HOSTILE_ORBITAL_SELECTOR))
        self.assertGreater(selector_specificity(selectors[0]), selector_specificity(HOSTILE_ORBITAL_SELECTOR))
        self.assertIn("head:has(#gravity_forms_theme_framework-css)", selectors[0])
        self.assertIn(ACTIVATION_CLASS, selectors[0])
        self.assertNotRegex(selectors[0], r"#gform_wrapper_\d+")

    def test_every_reviewed_gf_token_has_expected_implementation_sources(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        declarations = [name for _, body in css_blocks(css) for name, _ in gf_token_declarations(body)]
        counts = Counter(declarations)
        self.assertEqual(REVIEWED_GF_API, set(counts))
        self.assertEqual(2, counts["--gf-label-space-primary"], "base 8px plus bounded 6px field override expected")
        self.assertTrue(
            all(count == 1 for name, count in counts.items() if name != "--gf-label-space-primary"),
            f"unexpected duplicate --gf declarations: {counts}",
        )

    def test_all_direct_presentation_selectors_remain_srwf_scoped(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        for selector_group, body in css_blocks(css):
            if gf_token_declarations(body):
                for selector in split_selector_list(selector_group):
                    self.assertTrue(
                        selector.startswith(NARROW_SCOPE) or selector.startswith(ENFORCED_SCOPE),
                        f"token selector escaped SRWF scope: {selector}",
                    )
                continue
            for selector in split_selector_list(selector_group):
                if selector.startswith("@media"):
                    self.assertIn("@media (min-width: 960px)", selector)
                    self.assertIn(NARROW_SCOPE, selector)
                    continue
                self.assertTrue(selector.startswith(NARROW_SCOPE) or selector.startswith(ENFORCED_SCOPE), f"selector escaped SRWF scope: {selector}")
                if selector.startswith(ENFORCED_SCOPE):
                    self.assertTrue(
                        any(marker in selector for marker in (".gform_button", ".gform_title", ".gsection_title")),
                        f"strong framework sentinel escaped proven heading/submit consumers: {selector}",
                    )
        self.assertNotRegex(css, r"(?m)^\s*(?:html|body)\s*\{")
        self.assertNotRegex(css, r"#gform_wrapper_\d+")
        self.assertNotIn("[data-parent-form]", css)
        self.assertNotIn(":nth-child", css)
        self.assertNotIn(":nth-of-type", css)
        self.assertNotIn("!important", css)

    def test_authorized_mobile_and_desktop_shell_geometry_is_explicit(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        root = re.search(r"\.gform-theme--framework\.srwf-registration-theme_wrapper\s*\{([^}]*)\}", css, re.S)
        self.assertIsNotNone(root)
        root_body = root.group(1)
        self.assertIn("box-sizing: border-box;", root_body)
        self.assertIn("inline-size: 100%;", root_body)
        self.assertIn("max-inline-size: 100%;", root_body)
        self.assertIn("padding-inline: 16px;", root_body)
        self.assertNotIn("padding-block: 32px;", root_body)

        self.assertEqual(1, css.count("@media (min-width: 960px)"))
        desktop = re.search(r"@media \(min-width: 960px\).*?\.gform-theme--framework\.srwf-registration-theme_wrapper\s*\{([^}]*)\}", css, re.S)
        self.assertIsNotNone(desktop)
        body = desktop.group(1)
        self.assertIn("max-inline-size: 904px;", body)
        self.assertIn("padding-inline: 32px;", body)
        self.assertIn("padding-block: 32px;", body)
        self.assertEqual(840, 904 - (2 * 32))
        self.assertIn("background: #FFFFFF;", body)
        self.assertIn("border-radius: 16px;", body)
        self.assertIn("0 0 0 1px #E4E7EC", body)
        self.assertIn("0 1px 2px rgba(16, 24, 40, 0.04)", body)
        self.assertIn("0 12px 32px rgba(16, 24, 40, 0.06)", body)
        self.assertNotRegex(body, r"(?m)^\s*border\s*:")
        self.assertNotIn("overflow: hidden", body)
        self.assertNotIn("#F6F8FB", css, "page background remains host integration owned")

    def test_title_helper_error_rhythm_and_focus_match_authorized_values(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        title = re.search(r"\.gform_title\s*\{([^}]*)\}", css, re.S)
        self.assertIsNotNone(title)
        self.assertIn('font-family: "Vazirmatn", "Vazir", Tahoma, Arial, sans-serif;', title.group(1))
        self.assertIn("font-size: 24px;", title.group(1))
        self.assertIn("font-weight: 700;", title.group(1))
        self.assertIn("line-height: 1.5;", title.group(1))
        self.assertRegex(css, r"(?s)@media \(min-width: 960px\).*?\.gform_title\s*\{[^}]*font-size: 26px;")
        self.assertRegex(css, r"(?s)\.gfield--type-section \.gsection_title\s*\{[^}]*font-size: 18px;[^}]*font-weight: 700;[^}]*line-height: 1.5;")
        self.assertIn("gap: 12px;", css)
        for declaration in (
            "--gf-ctrl-line-height: 1.5;",
            "--gf-ctrl-label-line-height-primary: 1.5;",
            "--gf-label-space-primary: 8px;",
            "--gf-ctrl-desc-font-size: 14px;",
            "--gf-ctrl-desc-font-weight: 400;",
            "--gf-ctrl-desc-line-height: 1.5;",
            "--gf-ctrl-desc-font-size-error: 14px;",
            "--gf-ctrl-desc-font-weight-error: 600;",
            "--gf-ctrl-desc-line-height-error: 1.5;",
            "--gf-desc-space: 8px;",
            "--gf-ctrl-btn-line-height: 1.5;",
            "--gf-form-gap-y: 24px;",
            "--gf-ctrl-outline-color-focus: #1D4ED8;",
            "--gf-ctrl-outline-width-focus: 2px;",
            "--gf-ctrl-outline-offset: 2px;",
            "--gf-ctrl-outline-style: solid;",
        ):
            self.assertIn(declaration, css)
        self.assertIn("--gf-ctrl-size: 52px;", css)
        self.assertIn("--gf-ctrl-btn-size: 56px;", css)
        self.assertRegex(css, r"(?s)\.gfield--type-section\s*\{[^}]*margin-block-start: 8px;")

    def test_submit_enforcement_reuses_mechanically_stronger_framework_sentinel(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        submit_selectors = [selector for selector_group, body in css_blocks(css) if "inline-size: 100%;" in body for selector in split_selector_list(selector_group) if ".gform_button" in selector]
        self.assertEqual(2, len(submit_selectors))
        hostile = selector_specificity(HOSTILE_ORBITAL_SELECTOR)
        for selector in submit_selectors:
            self.assertTrue(selector.startswith(ENFORCED_SCOPE))
            self.assertEqual((1, 5, 2), selector_specificity(selector))
            self.assertGreater(selector_specificity(selector), hostile)

    def test_tom_select_adapter_is_runtime_proven_scoped_and_behavior_neutral(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        adapter = re.search(r"\.gform-theme--framework\.srwf-registration-theme_wrapper \.ts-wrapper \.ts-control\s*\{([^}]*)\}", css, re.S)
        self.assertIsNotNone(adapter)
        self.assertIn("min-block-size: var(--gf-ctrl-size);", adapter.group(1))
        self.assertIn("padding-inline: var(--gf-ctrl-select-padding-x);", adapter.group(1))
        self.assertNotRegex(css, r"(?m)^\s*\.ts-control\s*\{")
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))

    def test_section_heading_and_upload_family_keep_specialization_bounded(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        section = re.search(r"\.gfield--type-section \.gsection_title\s*\{([^}]*)\}", css, re.S)
        self.assertIsNotNone(section)
        self.assertIn("font-size: 18px;", section.group(1))
        self.assertIn("font-weight: 700;", section.group(1))
        self.assertIn("line-height: 1.5;", section.group(1))
        self.assertIn(".srwf-role-report-card-upload", css)
        self.assertIn(".gfield--type-fileupload .gpfup:not(.gpfup--has-files) .gpfup__droparea", css)
        self.assertIn(".gpfup.gpfup--images-only:not(.gpfup--has-files)", css)
        self.assertRegex(css, r"(?s)\.gpfup:not\(\.gpfup--has-files\) \.gpfup__droparea\s*\{[^}]*min-block-size: 96px;[^}]*padding: 16px;[^}]*border: 1px dashed #8690A1;[^}]*border-radius: 12px;")
        self.assertRegex(css, r"(?s)\.srwf-role-report-card-upload .*?\.gpfup__droparea::before\s*\{[^}]*background-size: 24px 24px;")

    def test_activation_is_explicit_class_scoped_and_entry_detail_boundary_retained(self) -> None:
        php = PHP.read_text(encoding="utf-8")
        self.assertIn("srwf-registration-theme", php)
        self.assertIn("gform_form_theme_slug", php)
        self.assertIn("gform_enqueue_scripts", php)
        self.assertIn("gravityflow_entry_detail_content_before", php)
        self.assertIn("gravityflow_entry_detail_content_after", php)
        self.assertNotRegex(php, r"gform_(?:enqueue_scripts|form_theme_slug)_\d+")

    def test_no_mockup_behavior_javascript_or_shared_core_was_added(self) -> None:
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))
        shared_files = sorted(path.relative_to(REPO).as_posix() for path in (REPO / "src").glob("**/*") if path.is_file())
        self.assertEqual(["src/README.md"], shared_files)

    def test_implementation_map_keeps_unresolved_host_boundaries_truthful(self) -> None:
        text = MAP.read_text(encoding="utf-8")
        for marker in (
            "OWNER_RUNTIME_REQUIRED",
            "HOST_INTEGRATION_REQUIRED",
            "NOT_PROVEN",
            "HOST_OWNED / OWNER_CONFIGURABLE",
            "Student Photo post-upload",
            "PersianGravity",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
