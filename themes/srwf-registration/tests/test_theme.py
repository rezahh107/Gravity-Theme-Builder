from __future__ import annotations

import hashlib
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / "themes" / "srwf-registration"
CSS = THEME / "src" / "srwf-registration.css"
PHP = THEME / "src" / "srwf-registration-theme.php"
MAP = THEME / "IMPLEMENTATION_MAP.md"
REFERENCE = THEME / "reference" / "materialize_reference.sh"
SCOPE = ".gform-theme--framework.srwf-registration-theme_wrapper"
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

    def test_every_css_selector_is_under_the_opt_in_framework_scope(self) -> None:
        css = strip_comments(CSS.read_text(encoding="utf-8"))
        for match in re.finditer(r"([^{}]+)\{", css):
            selector_group = match.group(1).strip()
            if selector_group.startswith("@"):
                continue
            for selector in selector_group.split(","):
                selector = selector.strip()
                self.assertTrue(
                    selector.startswith(SCOPE),
                    f"unscoped selector: {selector}",
                )

    def test_unresolved_values_are_not_promoted(self) -> None:
        css = CSS.read_text(encoding="utf-8")
        self.assertNotIn("!important", css)
        self.assertNotIn("@media", css)
        self.assertNotIn("box-shadow", css)
        self.assertNotIn("--gf-form-gap-y", css)
        self.assertNotIn("grid-template-columns", css)
        self.assertNotIn("--gf-ctrl-outline-width-focus", css)
        self.assertNotIn("--gf-ctrl-outline-color-focus", css)
        self.assertNotRegex(css, r"\.gform_title\s*\{")

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
