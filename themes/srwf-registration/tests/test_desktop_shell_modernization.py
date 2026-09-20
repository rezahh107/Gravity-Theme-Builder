from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = (THEME / "src" / "srwf-registration.css").read_text(encoding="utf-8")
PHP = (THEME / "src" / "srwf-registration-theme.php").read_text(encoding="utf-8")
DIAGNOSTIC = (THEME / "diagnostic" / "srwf-runtime-diagnostic.php").read_text(encoding="utf-8")


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def block(pattern: str, css: str = CSS) -> str:
    match = re.search(pattern, css, re.S)
    if match is None:
        raise AssertionError(f"CSS block not found: {pattern}")
    return match.group(1)


class DesktopShellModernizationTests(unittest.TestCase):
    def test_desktop_shell_preserves_904_840_geometry_with_non_layout_boundary(self) -> None:
        root = block(r"\.gform-theme--framework\.srwf-registration-theme_wrapper\s*\{([^}]*)\}")
        self.assertIn("box-sizing: border-box;", root)
        self.assertIn("padding-inline: 16px;", root)

        self.assertEqual(1, CSS.count("@media (min-width: 960px)"))
        desktop = block(
            r"@media \(min-width: 960px\).*?\.gform-theme--framework\.srwf-registration-theme_wrapper\s*\{([^}]*)\}"
        )

        max_width = int(re.search(r"max-inline-size:\s*(\d+)px", desktop).group(1))
        inline_padding = int(re.search(r"padding-inline:\s*(\d+)px", desktop).group(1))
        self.assertEqual(904, max_width)
        self.assertEqual(32, inline_padding)
        self.assertEqual(840, max_width - (2 * inline_padding))
        self.assertIn("padding-block: 32px;", desktop)
        self.assertIn("background: #FFFFFF;", desktop)
        self.assertIn("border-radius: 16px;", desktop)
        self.assertNotRegex(desktop, r"(?m)^\s*border\s*:")
        self.assertNotIn("overflow: hidden", desktop)
        self.assertIn("0 0 0 1px #E4E7EC", desktop)
        self.assertIn("0 1px 2px rgba(16, 24, 40, 0.04)", desktop)
        self.assertIn("0 12px 32px rgba(16, 24, 40, 0.06)", desktop)

    def test_no_device_matrix_or_page_shell_takeover_was_added(self) -> None:
        for width in (320, 360, 390, 393, 412, 430):
            self.assertNotRegex(CSS, rf"@media[^{{]*{width}px")

        clean = strip_comments(CSS)
        for forbidden in (
            ".site-content",
            ".content-area",
            ".site-main",
            ".inside-article",
            ".entry-content",
            ".page-id-",
            "100vw",
            "GeneratePress",
        ):
            self.assertNotIn(forbidden, clean)
        self.assertNotRegex(clean, r"(?m)^\s*(?:html|body)\s*\{")
        self.assertNotRegex(clean, r"#(?:gform_wrapper|field)_\d+")
        self.assertNotIn(":nth-child", clean)
        self.assertNotIn(":nth-of-type", clean)
        self.assertNotIn("#F6F8FB", clean)

    def test_existing_section_rhythm_and_component_contracts_remain_intact(self) -> None:
        self.assertIn("--gf-form-gap-y: 24px;", CSS)
        section = block(r"\.gform-theme--framework\.srwf-registration-theme_wrapper \.gfield--type-section\s*\{([^}]*)\}")
        self.assertIn("margin-block-start: 8px;", section)
        self.assertEqual(32, 24 + 8)

        self.assertIn("--gf-label-space-x-secondary: 0;", CSS)
        self.assertIn("flex: 1 1 9.5rem;", CSS)
        self.assertRegex(CSS, r"\.gfield-choice-input:checked \+ label")
        self.assertRegex(CSS, r"\.gfield-choice-input:focus-visible \+ label")
        self.assertNotIn("grid-template-columns", CSS)

        clean = strip_comments(CSS)
        self.assertIn(".gpfup:not(.gpfup--has-files)", clean)
        self.assertNotRegex(clean, r"\.gpfup--has-files(?:\s|\.|#|\[|:|\{|>)")
        self.assertIn(".ts-wrapper .ts-control", CSS)
        self.assertIn("padding-inline: var(--gf-ctrl-select-padding-x);", CSS)
        self.assertRegex(CSS, r"(?s)\.gform-footer \.gform_button.*?inline-size:\s*100%;")

    def test_package_version_advances_without_diagnostic_bump(self) -> None:
        self.assertIn("Version: 0.1.18", PHP)
        self.assertIn("SRWF_REGISTRATION_THEME_VERSION = '0.1.18'", PHP)
        self.assertIn("Version: 0.3.6", DIAGNOSTIC)
        self.assertIn("GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '0.3.6'", DIAGNOSTIC)


if __name__ == "__main__":
    unittest.main()
