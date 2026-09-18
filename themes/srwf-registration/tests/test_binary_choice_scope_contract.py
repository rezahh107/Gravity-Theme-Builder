from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = (THEME / "src" / "srwf-registration.css").read_text(encoding="utf-8")
ROLE = "srwf-role-binary-choice"


def selectors(css: str) -> list[str]:
    clean = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    result: list[str] = []
    for match in re.finditer(r"([^{}]+)\{[^{}]*\}", clean, flags=re.S):
        result.extend(part.strip() for part in match.group(1).split(",") if part.strip())
    return result


class BinaryChoiceScopeContractTests(unittest.TestCase):
    def test_radio_choice_presentation_is_role_scoped(self) -> None:
        relevant = [
            selector
            for selector in selectors(CSS)
            if ".gfield_radio" in selector or ".gchoice" in selector or ".gfield-choice-input" in selector
        ]
        self.assertTrue(relevant)
        for selector in relevant:
            self.assertIn(f".gfield.{ROLE}", selector)

    def test_no_generic_radio_or_vertical_alignment_override_exists(self) -> None:
        for selector in selectors(CSS):
            if ROLE in selector:
                continue
            self.assertNotIn(".gfield--type-radio", selector)
            self.assertNotIn(".gfield--choice-align-vertical", selector)
            self.assertNotEqual(selector, ".gfield_radio")
            self.assertNotEqual(selector, ".gchoice")

    def test_no_durable_numeric_or_label_identity(self) -> None:
        self.assertNotRegex(CSS, r"#(?:field|input|choice|label|gform_wrapper|gform)_\d+")
        self.assertNotIn(":nth-child", CSS)
        self.assertNotIn(":nth-of-type", CSS)
        self.assertNotIn("جنسیت", CSS)
        self.assertNotIn("فارغ", CSS)


if __name__ == "__main__":
    unittest.main()
