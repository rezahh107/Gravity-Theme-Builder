from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = (THEME / "src" / "srwf-registration.css").read_text(encoding="utf-8")

SCOPE = ".gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio"
GROUP_SELECTOR = f"{SCOPE} .gfield_radio"
CHOICE_SELECTOR = f"{SCOPE} .gchoice"
INPUT_SELECTOR = f"{SCOPE} .gfield-choice-input"
LABEL_SELECTOR = f"{SCOPE} .gchoice label"


def rule_body(css: str, selector: str) -> str:
    match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", css, flags=re.S)
    if not match:
        raise AssertionError(f"missing CSS rule: {selector}")
    return match.group(1)


def top_level_selectors(css: str) -> list[str]:
    clean = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    selectors: list[str] = []
    for match in re.finditer(r"([^{}]+)\{[^{}]*\}", clean, flags=re.S):
        prefix = match.group(1).strip()
        if prefix.startswith("@"):
            continue
        selectors.extend(part.strip() for part in prefix.split(",") if part.strip())
    return selectors


class RadioSecondaryLabelSpacingTests(unittest.TestCase):
    def test_runtime_proven_12px_deficit_maps_to_documented_secondary_label_spacer(self) -> None:
        # Owner runtime: 173 -> 161 in paired rows and 358 -> 346 in full rows.
        # Gravity Forms' documented --gf-label-space-x-secondary default is 12px.
        self.assertEqual(12, 173 - 161)
        self.assertEqual(12, 358 - 346)

        group = rule_body(CSS, GROUP_SELECTOR)
        self.assertRegex(group, r"--gf-label-space-x-secondary\s*:\s*0\s*;")
        self.assertRegex(group, r"\bgap\s*:\s*12px\s*;")
        self.assertNotRegex(group, r"(?:calc\(|\+\s*12px|inline-size\s*:\s*(?:calc|[0-9]))")

    def test_visible_label_full_cell_contract_closes_both_known_layout_causes(self) -> None:
        group = rule_body(CSS, GROUP_SELECTOR)
        choice = rule_body(CSS, CHOICE_SELECTOR)
        label = rule_body(CSS, LABEL_SELECTOR)

        self.assertRegex(group, r"--gf-label-space-x-secondary\s*:\s*0\s*;")
        self.assertRegex(choice, r"\bdisplay\s*:\s*flex\s*;")
        self.assertRegex(label, r"\bdisplay\s*:\s*flex\s*;")
        self.assertRegex(label, r"\bflex\s*:\s*1 1 auto\s*;")
        self.assertRegex(label, r"\binline-size\s*:\s*100%\s*;")
        self.assertRegex(label, r"\bmin-inline-size\s*:\s*0\s*;")

    def test_radio_repair_stays_srwf_scoped_and_does_not_take_host_layout_ownership(self) -> None:
        radio_selectors = [
            selector
            for selector in top_level_selectors(CSS)
            if ".gfield_radio" in selector or ".gchoice" in selector or ".gfield-choice-input" in selector
        ]
        self.assertTrue(radio_selectors)
        for selector in radio_selectors:
            self.assertTrue(selector.startswith(".gform-theme--framework.srwf-registration-theme_wrapper"))
            self.assertIn(".gfield.gfield--type-radio", selector)
            self.assertNotIn("body", selector)

        forbidden_host_ownership = (
            ".site-content",
            ".content-area",
            ".site-main",
            ".inside-article",
            ".entry-content",
            "generatepress",
            ".page-id-",
            "100vw",
            "calc(100vw",
        )
        lowered = CSS.lower()
        for forbidden in forbidden_host_ownership:
            self.assertNotIn(forbidden, lowered)
        self.assertNotRegex(CSS, r"(?m)\bmargin-(?:inline|left|right)(?:-start|-end)?\s*:\s*-")

    def test_mobile_gutter_and_desktop_contract_remain_unchanged(self) -> None:
        wrapper = rule_body(CSS, ".gform-theme--framework.srwf-registration-theme_wrapper")
        self.assertRegex(wrapper, r"\binline-size\s*:\s*100%\s*;")
        self.assertRegex(wrapper, r"\bmax-inline-size\s*:\s*100%\s*;")
        self.assertRegex(wrapper, r"\bpadding-inline\s*:\s*16px\s*;")

        self.assertEqual(1, CSS.count("@media (min-width: 960px)"))
        desktop = CSS.split("@media (min-width: 960px)", 1)[1]
        self.assertIn("max-inline-size: 904px", desktop)
        self.assertIn("padding-inline: 32px", desktop)
        self.assertNotRegex(CSS, r"@media[^\{]*(?:320|360|390|393|412|430)px")

    def test_native_radio_state_and_intrinsic_wrapping_are_preserved(self) -> None:
        group = rule_body(CSS, GROUP_SELECTOR)
        choice = rule_body(CSS, CHOICE_SELECTOR)
        input_rule = rule_body(CSS, INPUT_SELECTOR)
        label = rule_body(CSS, LABEL_SELECTOR)

        self.assertRegex(group, r"\bflex-flow\s*:\s*row wrap\s*;")
        self.assertRegex(choice, r"\bflex\s*:\s*1 1 9\.5rem\s*;")
        self.assertRegex(choice, r"\bmin-inline-size\s*:\s*0\s*;")
        self.assertRegex(input_rule, r"\bposition\s*:\s*absolute\s*;")
        self.assertNotIn("display: none", input_rule)
        self.assertNotIn("visibility: hidden", input_rule)
        self.assertRegex(label, r"\bmin-block-size\s*:\s*52px\s*;")
        self.assertNotRegex(label, r"(?m)^\s*(?:height|block-size)\s*:")
        self.assertIn(":checked + label", CSS)
        self.assertIn(":focus-visible + label", CSS)

    def test_unrelated_gpfup_gpas_and_submit_contracts_remain_present(self) -> None:
        self.assertIn(".ts-wrapper .ts-control", CSS)
        self.assertIn("padding-inline: var(--gf-ctrl-select-padding-x)", CSS)
        self.assertIn(".gpfup:not(.gpfup--has-files) .gpfup__droparea", CSS)
        self.assertIn("flex: 0 1 13rem", CSS)
        self.assertNotIn(".gpfup--has-files) .gpfup__droparea", CSS.replace(":not(.gpfup--has-files)", ""))
        self.assertIn(".gform-footer .gform_button", CSS)
        self.assertIn("inline-size: 100%", CSS)


if __name__ == "__main__":
    unittest.main()
