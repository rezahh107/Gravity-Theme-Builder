from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / "themes" / "srwf-registration"
CSS_PATH = THEME / "src" / "srwf-registration.css"
OWNER = THEME / "reference" / "SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md"
CANONICAL = REPO / "PROJECT_SOURCES" / "00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_REFERENCE.md"
IMPLEMENTATION_MAP = THEME / "IMPLEMENTATION_MAP.md"
DIAGNOSTIC_FIXTURE = THEME / "tests" / "test_visual_repair_qualification_v035.js"
NARROW_SCOPE = ".gform-theme--framework.srwf-registration-theme_wrapper"

DESCRIPTION_SELECTOR = (
    NARROW_SCOPE
    + " .gfield.field_description_above:has(> .gfield_description:not(.gform_fileupload_rules))"
)
VALIDATION_SELECTOR = (
    NARROW_SCOPE
    + " .gfield.field_validation_above:has(.gfield_validation_message)"
)


def block_for(css: str, selector_fragment: str) -> str:
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", re.sub(r"/\*.*?\*/", "", css, flags=re.S), flags=re.S):
        selectors, body = match.groups()
        if selector_fragment in selectors:
            return body
    return ""


def spacing_contract_violations(css: str) -> list[str]:
    violations: list[str] = []
    if "--gf-label-space-primary: 8px;" not in css:
        violations.append("missing no-helper 8px label spacing")
    if "--gf-desc-space: 8px;" not in css:
        violations.append("missing final text-to-control 8px spacing")
    description = block_for(css, DESCRIPTION_SELECTOR)
    validation = block_for(css, VALIDATION_SELECTOR)
    if "--gf-label-space-primary: 6px;" not in description:
        violations.append("missing label-to-helper 6px override")
    if "--gf-label-space-primary: 6px;" not in validation:
        violations.append("missing label-to-error 6px override")
    return violations


class SrwfFieldInternalSpacingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.css = CSS_PATH.read_text(encoding="utf-8")
        cls.owner = OWNER.read_text(encoding="utf-8")
        cls.canonical = CANONICAL.read_text(encoding="utf-8")
        cls.implementation_map = IMPLEMENTATION_MAP.read_text(encoding="utf-8")
        cls.diagnostic_fixture = DIAGNOSTIC_FIXTURE.read_text(encoding="utf-8")

    def test_owner_authority_retains_exact_8_6_8_contract(self) -> None:
        for required in (
            "ordinary label → control gap with no helper/error: `8px`",
            "label → helper/error: `6px`",
            "final helper/error → control: `8px`",
            "text-bearing blocks must remain content-driven rather than fixed-height",
        ):
            self.assertIn(required, self.owner)

    def test_documented_gf_api_supports_only_the_8px_base_transitions_used_here(self) -> None:
        self.assertRegex(self.canonical, r"\| `--gf-label-space-primary` \| `8px` \|")
        self.assertRegex(self.canonical, r"\| `--gf-desc-space` \| `8px` \|")
        self.assertNotIn("--gf-label-helper-space", self.css)
        self.assertNotIn("--gf-label-error-space", self.css)

    def test_production_css_closes_owner_spacing_contract(self) -> None:
        self.assertEqual([], spacing_contract_violations(self.css))
        self.assertIn("field_description_above", self.css)
        self.assertIn("field_validation_above", self.css)

    def test_pre_repair_or_fixture_only_change_cannot_pass(self) -> None:
        candidate = self.css.replace("    --gf-label-space-primary: 8px;\n", "")
        candidate = candidate.replace("    --gf-desc-space: 8px;\n", "")
        candidate = re.sub(
            r"(?s)/\*\n \* Owner field-internal spacing contract\..*?\n\}\n\n",
            "",
            candidate,
            count=1,
        )
        violations = spacing_contract_violations(candidate)
        self.assertIn("missing no-helper 8px label spacing", violations)
        self.assertIn("missing final text-to-control 8px spacing", violations)
        self.assertIn("missing label-to-helper 6px override", violations)
        self.assertIn("missing label-to-error 6px override", violations)

    def test_no_helper_label_to_control_stays_8px(self) -> None:
        self.assertIn("--gf-label-space-primary: 8px;", self.css)
        self.assertNotIn("--gf-label-choice-field-space-primary:", self.css)

    def test_helper_above_input_is_6_then_8_without_fixed_text_height(self) -> None:
        body = block_for(self.css, DESCRIPTION_SELECTOR)
        self.assertIn("--gf-label-space-primary: 6px;", body)
        self.assertIn("--gf-desc-space: 8px;", self.css)
        self.assertNotRegex(body, r"(?:block-size|height|min-block-size|max-block-size)\s*:")

    def test_validation_above_input_is_6_then_8_without_behavior_takeover(self) -> None:
        body = block_for(self.css, VALIDATION_SELECTOR)
        self.assertIn("--gf-label-space-primary: 6px;", body)
        self.assertIn("--gf-desc-space: 8px;", self.css)
        self.assertNotIn("display:", body)
        self.assertNotIn("order:", body)
        self.assertNotIn("position:", body)

    def test_combined_helper_error_intermediate_gap_is_not_invented(self) -> None:
        self.assertNotRegex(self.css, r"\.gfield_description\s*[+~]\s*\.gfield_validation_message")
        self.assertNotRegex(self.css, r"\.gfield_validation_message\s*[+~]\s*\.gfield_description")
        self.assertNotIn("['helper', 6, 'error']", self.diagnostic_fixture)
        self.assertIn("AUTHORITY_NOT_INVENTED", self.diagnostic_fixture)
        self.assertIn("--gf-desc-space: 8px;", self.css)

    def test_spacing_enforcement_is_srwf_scoped_and_preserves_existing_rhythms(self) -> None:
        for selector in (DESCRIPTION_SELECTOR, VALIDATION_SELECTOR):
            self.assertTrue(selector.startswith(NARROW_SCOPE))
        self.assertIn("--gf-form-gap-y: 24px;", self.css)
        self.assertRegex(self.css, r"(?s)\.gfield--type-section\s*\{[^}]*margin-block-start: 8px;")
        radio = block_for(self.css, NARROW_SCOPE + " .gfield.gfield--type-radio .gfield_radio")
        self.assertIn("gap: 12px;", radio)
        self.assertNotIn("--gf-desc-choice-field-space:", self.css)
        self.assertNotRegex(self.css, r"#gform_wrapper_\d+")
        self.assertNotIn(":nth-child", self.css)
        self.assertNotIn(":nth-of-type", self.css)

    def test_implementation_map_describes_real_enforcement_and_runtime_limit(self) -> None:
        row = next(
            (line for line in self.implementation_map.splitlines() if line.startswith("| Field-internal spacing |")),
            None,
        )
        self.assertIsNotNone(row)
        for token in ("8px", "6px", "--gf-label-space-primary", "--gf-desc-space", "OWNER_RUNTIME_REQUIRED"):
            self.assertIn(token, row)
        self.assertIn("intermediate helper/error spacing", row)


if __name__ == "__main__":
    unittest.main()
