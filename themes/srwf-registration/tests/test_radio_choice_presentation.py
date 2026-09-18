from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = THEME / "src" / "srwf-registration.css"
BINARY_ROLE = "srwf-role-binary-choice"
ORDINARY_SCOPE = f".gfield--type-radio:not(.{BINARY_ROLE})"


def blocks(css: str) -> list[tuple[str, str]]:
    clean = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [
        (match.group(1).strip(), match.group(2))
        for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean, flags=re.S)
    ]


def body_for(css: str, selector_suffix: str) -> str:
    return next(
        body
        for selector, body in blocks(css)
        if selector.endswith(selector_suffix)
    )


class SrwfRadioChoicePresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.css = CSS.read_text(encoding="utf-8")

    def test_binary_cards_override_host_vertical_alignment_with_two_equal_tracks(self) -> None:
        row = body_for(self.css, f".gfield.{BINARY_ROLE} .gfield_radio")
        choice = body_for(self.css, f".gfield.{BINARY_ROLE} .gchoice")
        label = body_for(self.css, f".gfield.{BINARY_ROLE} .gchoice label")

        self.assertIn("display: flex;", row)
        self.assertIn("flex-direction: row;", row)
        self.assertIn("gap: 12px;", row)
        self.assertIn("inline-size: 100%;", row)
        self.assertIn("flex: 1 1 0;", choice)
        self.assertIn("inline-size: 0;", choice)
        self.assertIn("min-inline-size: 0;", choice)
        self.assertIn("inline-size: 100%;", label)
        self.assertIn("min-block-size: 48px;", label)
        self.assertIn("padding: 12px 16px;", label)

    def test_ordinary_radios_use_approved_vertical_card_family_and_exclude_binary_roles(self) -> None:
        row = body_for(self.css, f"{ORDINARY_SCOPE} .gfield_radio")
        choice = body_for(self.css, f"{ORDINARY_SCOPE} .gchoice")
        input_body = body_for(self.css, f"{ORDINARY_SCOPE} .gfield-choice-input")

        self.assertIn("--gf-ctrl-choice-size: 20px;", self.css)
        self.assertIn("--gf-ctrl-radio-check-size: 10px;", self.css)
        self.assertIn("border-width: 2px;", input_body)
        self.assertIn("border-color: #8690A1;", input_body)

        self.assertIn("display: flex;", row)
        self.assertIn("flex-direction: column;", row)
        self.assertIn("gap: 10px;", row)
        self.assertIn("inline-size: 100%;", row)

        for declaration in (
            "min-block-size: 48px;",
            "inline-size: 100%;",
            "padding: 14px 16px;",
            "border: 1.5px solid #8690A1;",
            "border-radius: 10px;",
            "background: #FFFFFF;",
            "font-size: 15px;",
            "font-weight: 500;",
            "gap: 10px;",
        ):
            self.assertIn(declaration, choice)

    def test_ordinary_selected_card_derives_from_native_checked_state(self) -> None:
        selected_selector = f"{ORDINARY_SCOPE} .gchoice:has(.gfield-choice-input:checked)"
        selected = body_for(self.css, selected_selector)
        checked_input = body_for(self.css, f"{ORDINARY_SCOPE} .gfield-choice-input:checked")
        self.assertIn("border-color: #1D4ED8;", selected)
        self.assertIn("background: #EEF2FF;", selected)
        self.assertIn("color: #1D4ED8;", selected)
        self.assertIn("border-color: #1D4ED8;", checked_input)

        input_body = body_for(self.css, f"{ORDINARY_SCOPE} .gfield-choice-input")
        self.assertNotIn("display: none", input_body)
        self.assertNotIn("visibility: hidden", input_body)
        self.assertNotIn("opacity: 0", input_body)
        self.assertIn("inline-size: var(--gf-ctrl-choice-size);", input_body)
        self.assertIn("block-size: var(--gf-ctrl-choice-size);", input_body)

    def test_choice_fix_does_not_invent_a_responsive_breakpoint(self) -> None:
        self.assertNotIn("@media", self.css)
        self.assertNotRegex(self.css, r"#(?:field|input|gform_wrapper|gform)_\d+")


if __name__ == "__main__":
    unittest.main()
