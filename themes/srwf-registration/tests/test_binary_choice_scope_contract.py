from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = (THEME / "src" / "srwf-registration.css").read_text(encoding="utf-8")
RADIO_SCOPE = ".gfield.gfield--type-radio"


def selectors(css: str) -> list[str]:
    clean = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    result: list[str] = []
    for match in re.finditer(r"([^{}]+)\{[^{}]*\}", clean, flags=re.S):
        result.extend(part.strip() for part in match.group(1).split(",") if part.strip())
    return result


class RadioCardScopeContractTests(unittest.TestCase):
    def test_every_radio_card_presentation_rule_is_field_type_scoped(self) -> None:
        relevant = [
            selector
            for selector in selectors(CSS)
            if ".gfield_radio" in selector or ".gchoice" in selector or ".gfield-choice-input" in selector
        ]
        self.assertTrue(relevant)
        for selector in relevant:
            self.assertIn(RADIO_SCOPE, selector)
            self.assertTrue(selector.startswith(".gform-theme--framework.srwf-registration-theme_wrapper"))

    def test_card_presentation_is_not_gated_by_binary_semantic_role(self) -> None:
        for selector in selectors(CSS):
            if ".gfield_radio" in selector or ".gchoice" in selector or ".gfield-choice-input" in selector:
                self.assertNotIn("srwf-role-binary-choice", selector)
        self.assertIn(RADIO_SCOPE, CSS)

    def test_visible_label_fills_choice_and_selected_state_has_non_color_cue(self) -> None:
        self.assertRegex(
            CSS,
            r"(?s)\.gfield\.gfield--type-radio \.gchoice label\s*\{[^}]*inline-size:\s*100%;",
        )
        self.assertRegex(
            CSS,
            r"(?s)\.gfield\.gfield--type-radio \.gchoice label\s*\{[^}]*border:\s*1px solid #8690A1;",
        )
        self.assertRegex(
            CSS,
            r"(?s)\.gfield-choice-input:checked \+ label\s*\{[^}]*border-width:\s*2px;[^}]*background:\s*#EDF1FC;",
        )
        self.assertRegex(
            CSS,
            r"(?s)\.gfield-choice-input:checked \+ label::before\s*\{[^}]*background:\s*#1D4ED8;[^}]*box-shadow:",
        )

    def test_radio_layout_is_content_driven_and_wraps(self) -> None:
        self.assertRegex(
            CSS,
            r"(?s)\.gfield\.gfield--type-radio \.gfield_radio\s*\{[^}]*flex-flow:\s*row wrap;[^}]*gap:\s*12px;",
        )
        self.assertRegex(
            CSS,
            r"(?s)\.gfield\.gfield--type-radio \.gchoice\s*\{[^}]*flex:\s*1 1 8rem;",
        )
        self.assertNotIn("grid-template-columns", "\n".join(
            selector for selector in selectors(CSS) if RADIO_SCOPE in selector
        ))

    def test_no_durable_numeric_text_or_position_identity(self) -> None:
        self.assertNotRegex(CSS, r"#(?:field|input|choice|label|gform_wrapper|gform)_\d+")
        self.assertNotIn(":nth-child", CSS)
        self.assertNotIn(":nth-of-type", CSS)
        self.assertNotIn("جنسیت", CSS)
        self.assertNotIn("فارغ", CSS)


if __name__ == "__main__":
    unittest.main()
