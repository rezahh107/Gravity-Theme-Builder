from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = (THEME / "src" / "srwf-registration.css").read_text(encoding="utf-8")
THEME_PHP = (THEME / "src" / "srwf-registration-theme.php").read_text(encoding="utf-8")
DIAGNOSTIC = (THEME / "diagnostic" / "assets" / "binary-choice-geometry.js").read_text(encoding="utf-8")

SCOPE = ".gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio"
CHOICE_SELECTOR = f"{SCOPE} .gchoice"
LABEL_SELECTOR = f"{SCOPE} .gchoice label"


def rule_body(css: str, selector: str) -> str:
    match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css, flags=re.S)
    if not match:
        raise AssertionError(f"missing CSS rule: {selector}")
    return match.group(1)


def fill_contract_closed(css: str) -> bool:
    choice = rule_body(css, CHOICE_SELECTOR)
    label = rule_body(css, LABEL_SELECTOR)
    return (
        re.search(r"\bdisplay\s*:\s*block\s*;", choice) is not None
        and re.search(r"\binline-size\s*:\s*100%\s*;", label) is not None
    )


class RadioCardFillRepairTests(unittest.TestCase):
    def test_pre_repair_choice_rule_fails_root_cause_contract(self) -> None:
        pre_repair = CSS.replace("    display: block;\n", "", 1)
        self.assertFalse(fill_contract_closed(pre_repair))
        self.assertTrue(fill_contract_closed(CSS))

    def test_srwf_radio_choice_neutralizes_gravity_forms_two_track_grid(self) -> None:
        body = rule_body(CSS, CHOICE_SELECTOR)
        self.assertRegex(body, r"\bdisplay\s*:\s*block\s*;")
        self.assertNotRegex(body, r"display\s*:\s*(?:inline-)?grid")
        self.assertNotIn("grid-template-columns", body)
        self.assertRegex(body, r"\bposition\s*:\s*relative\s*;")
        self.assertRegex(body, r"\bflex\s*:\s*1 1 8rem\s*;")
        self.assertRegex(body, r"\bmin-inline-size\s*:\s*0\s*;")

    def test_group_flex_wrap_strategy_is_unchanged(self) -> None:
        body = rule_body(CSS, f"{SCOPE} .gfield_radio")
        self.assertRegex(body, r"\bdisplay\s*:\s*flex\s*;")
        self.assertRegex(body, r"\bflex-flow\s*:\s*row wrap\s*;")
        self.assertRegex(body, r"\bgap\s*:\s*12px\s*;")

    def test_visible_associated_label_fills_full_choice_cell(self) -> None:
        body = rule_body(CSS, LABEL_SELECTOR)
        self.assertRegex(body, r"\bdisplay\s*:\s*flex\s*;")
        self.assertRegex(body, r"\binline-size\s*:\s*100%\s*;")
        self.assertRegex(body, r"\bmin-inline-size\s*:\s*0\s*;")
        self.assertRegex(body, r"\bmin-block-size\s*:\s*52px\s*;")

    def test_selected_and_unselected_card_language_is_unchanged(self) -> None:
        base = rule_body(CSS, LABEL_SELECTOR)
        selected = rule_body(CSS, f"{SCOPE} .gfield-choice-input:checked + label")
        cue = rule_body(CSS, f"{SCOPE} .gfield-choice-input:checked + label::before")
        self.assertRegex(base, r"border\s*:\s*1px solid #8690A1\s*;")
        self.assertRegex(base, r"background\s*:\s*#FFFFFF\s*;")
        self.assertRegex(selected, r"border-color\s*:\s*#1D4ED8\s*;")
        self.assertRegex(selected, r"border-width\s*:\s*2px\s*;")
        self.assertRegex(selected, r"background\s*:\s*#EDF1FC\s*;")
        self.assertRegex(cue, r"background\s*:\s*#1D4ED8\s*;")
        self.assertRegex(cue, r"box-shadow\s*:\s*inset 0 0 0 3px #EDF1FC\s*;")

    def test_native_input_state_and_focus_projection_remain_intact(self) -> None:
        input_rule = rule_body(CSS, f"{SCOPE} .gfield-choice-input")
        focus = rule_body(CSS, f"{SCOPE} .gfield-choice-input:focus-visible + label")
        self.assertRegex(input_rule, r"\bposition\s*:\s*absolute\s*;")
        self.assertNotIn("display: none", input_rule)
        self.assertNotIn("visibility: hidden", input_rule)
        self.assertRegex(focus, r"outline\s*:\s*2px solid #1D4ED8\s*;")
        self.assertRegex(focus, r"outline-offset\s*:\s*2px\s*;")
        self.assertIn(":checked + label", CSS)
        self.assertIn(":focus-visible + label", CSS)

    def test_repair_is_radio_and_registration_scoped_without_identity_hacks(self) -> None:
        for selector in re.findall(r"([^{}]+)\{[^{}]*\}", CSS, flags=re.S):
            if ".gchoice" in selector or ".gfield-choice-input" in selector or ".gfield_radio" in selector:
                for part in selector.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    self.assertTrue(part.startswith(".gform-theme--framework.srwf-registration-theme_wrapper"))
                    self.assertIn(".gfield.gfield--type-radio", part)
        self.assertNotRegex(CSS, r"#(?:field|input|choice|label|gform_wrapper|gform)_\d+")
        self.assertNotIn(":nth-child", CSS)
        self.assertNotIn(":nth-of-type", CSS)
        self.assertNotIn("!important", CSS)

    def test_fill_repair_rule_does_not_take_typography_ownership(self) -> None:
        body = rule_body(CSS, CHOICE_SELECTOR)
        for property_name in (
            "font-family",
            "font-size",
            "font-weight",
            "line-height",
            "letter-spacing",
            "text-transform",
        ):
            self.assertNotIn(property_name, body)

    def test_entry_detail_exclusion_and_diagnostic_version_are_unchanged(self) -> None:
        self.assertIn("SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL", THEME_PHP)
        self.assertIn("'exclusionReason'      => $exclusion_reason", THEME_PHP)
        self.assertIn("'gravity_flow_entry_detail'", THEME_PHP)
        self.assertIn("var VERSION = '0.3.5';", DIAGNOSTIC)
        self.assertIn("fillDelta <= 1", DIAGNOSTIC)
        self.assertIn("allVisibleLabelsFillChoices", DIAGNOSTIC)


if __name__ == "__main__":
    unittest.main()
