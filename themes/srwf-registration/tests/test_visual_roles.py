from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / "themes" / "srwf-registration"
CSS = THEME / "src" / "srwf-registration.css"
ICONS = THEME / "src" / "icons"
FIXTURES = THEME / "tests" / "fixtures" / "semantic-roles-runtime-shapes.md"

BINARY_ROLE = "srwf-role-binary-choice"
REPORT_ROLE = "srwf-role-report-card-upload"
SECTION_ICONS = {
    "srwf-role-section-identity": (
        "section-identity.svg",
        '<circle cx="12" cy="8" r="4"/>',
        '<path d="M4 21c0-4 4-7 8-7s8 3 8 7"/>',
    ),
    "srwf-role-section-contact": (
        "section-contact.svg",
        '<rect x="6" y="2" width="12" height="20" rx="2"/>',
        '<line x1="12" y1="18" x2="12" y2="18"/>',
    ),
    "srwf-role-section-education": (
        "section-education.svg",
        '<path d="M22 10L12 5 2 10l10 5 10-5z"/>',
        '<path d="M6 12v5c0 1 3 3 6 3s6-2 6-3v-5"/>',
    ),
    "srwf-role-section-school-documents": (
        "section-school-documents.svg",
        '<path d="M3 21h18"/>',
        '<path d="M5 21V7l7-4 7 4v14"/>',
        '<path d="M9 21v-6h6v6"/>',
    ),
    "srwf-role-section-student-photo": (
        "section-student-photo.svg",
        '<path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>',
        '<circle cx="12" cy="13" r="4"/>',
    ),
}


def blocks(css: str) -> list[tuple[str, str]]:
    clean = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [
        (match.group(1).strip(), match.group(2))
        for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean, flags=re.S)
    ]


class SrwfVisualRoleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.css = CSS.read_text(encoding="utf-8")
        self.fixtures = FIXTURES.read_text(encoding="utf-8")

    def test_binary_cards_require_explicit_semantic_role(self) -> None:
        binary_selectors = [selector for selector, body in blocks(self.css) if BINARY_ROLE in selector or BINARY_ROLE in body]
        self.assertTrue(binary_selectors)
        for selector in binary_selectors:
            self.assertIn(f".gfield.{BINARY_ROLE}", selector)
        self.assertNotRegex(self.css, r"\.gfield--type-radio\s+\.gfield_radio\s*\{")
        self.assertNotRegex(self.css, r"\.gfield--choice-align-vertical\s+\.gfield_radio\s*\{")

    def test_binary_fixtures_preserve_authentic_radio_label_structure(self) -> None:
        binary_class = (
            'class="gfield gfield--type-radio gfield--type-choice gfield--input-type-radio '
            'gfield--width-half srwf-role-binary-choice gfield--choice-align-vertical"'
        )
        self.assertEqual(2, self.fixtures.count(binary_class))
        self.assertIn('class="ginput_container ginput_container_radio"', self.fixtures)
        self.assertIn('class="gfield-choice-input" type="radio"', self.fixtures)
        self.assertIn('<label for="fixture_gender_choice_a"></label>', self.fixtures)
        self.assertIn('<label for="fixture_gender_choice_b"></label>', self.fixtures)
        self.assertIn('name="fixture_gender_choice" value="b" checked', self.fixtures)
        self.assertIn('<label for="fixture_graduation_choice_a"></label>', self.fixtures)
        self.assertIn('<label for="fixture_graduation_choice_b"></label>', self.fixtures)
        self.assertIn('name="fixture_graduation_choice" value="b" checked', self.fixtures)

    def test_binary_selection_uses_native_checked_state_and_exact_focus_projection(self) -> None:
        input_block = next(body for selector, body in blocks(self.css) if selector.endswith(f".gfield.{BINARY_ROLE} .gfield-choice-input"))
        self.assertIn("position: absolute;", input_block)
        self.assertIn("opacity: 0;", input_block)
        self.assertNotIn("display: none", input_block)
        self.assertNotIn("visibility: hidden", input_block)
        checked_block = next(body for selector, body in blocks(self.css) if f".gfield.{BINARY_ROLE} .gfield-choice-input:checked + label" in selector)
        self.assertIn("background: #EDF1FC;", checked_block)
        self.assertIn("border-color: #1D4ED8;", checked_block)
        self.assertIn("border-width: 2px;", checked_block)
        self.assertIn("font-weight: 700;", checked_block)
        focus_block = next(body for selector, body in blocks(self.css) if f".gfield.{BINARY_ROLE} .gfield-choice-input:focus-visible + label" in selector)
        self.assertIn("outline: 2px solid #1D4ED8;", focus_block)
        self.assertIn("outline-offset: 2px;", focus_block)
        self.assertIn("box-shadow: none;", focus_block)

    def test_binary_cards_keep_equal_intrinsic_row_tracks_without_binary_breakpoint(self) -> None:
        choice = next(body for selector, body in blocks(self.css) if selector.endswith(f".gfield.{BINARY_ROLE} .gchoice"))
        row = next(body for selector, body in blocks(self.css) if selector.endswith(f".gfield.{BINARY_ROLE} .gfield_radio"))
        label = next(body for selector, body in blocks(self.css) if selector.endswith(f".gfield.{BINARY_ROLE} .gchoice label"))
        self.assertIn("display: flex;", row)
        self.assertIn("flex-direction: row;", row)
        self.assertIn("gap: 12px;", row)
        self.assertIn("flex: 1 1 0;", choice)
        self.assertIn("min-inline-size: 0;", choice)
        self.assertIn("min-block-size: 52px;", label)
        self.assertIn("border-radius: 10px;", label)
        self.assertIn("overflow-wrap: anywhere;", label)
        self.assertNotIn("grid-template-columns", self.css)
        self.assertEqual(1, self.css.count("@media (min-width: 960px)"))

    def test_ordinary_vertical_radio_remains_host_owned(self) -> None:
        ordinary = '<fieldset class="gfield gfield--type-radio gfield--type-choice gfield--input-type-radio gfield--choice-align-vertical">'
        self.assertIn(ordinary, self.fixtures)
        ordinary_selectors = [selector for selector, _ in blocks(self.css) if ".gfield--type-radio" in selector or ".gfield--choice-align-vertical" in selector]
        self.assertEqual([], ordinary_selectors)
        self.assertNotRegex(self.css, r"(?m)^\s*\.gfield_radio\s*\{")
        self.assertNotRegex(self.css, r"(?m)^\s*\.gchoice\s*\{")

    def test_binary_role_supports_both_consumers_without_numeric_identity(self) -> None:
        self.assertEqual(2, self.fixtures.count("srwf-role-binary-choice gfield--choice-align-vertical"))
        self.assertNotRegex(self.css, r"#(?:field|input|choice|label|gform_wrapper|gform)_\d+")
        self.assertNotIn(":nth-child", self.css)
        self.assertNotIn(":nth-of-type", self.css)

    def test_binary_runtime_shape_uses_native_radios_not_fake_buttons(self) -> None:
        binary_sections = self.fixtures.split("## Ordinary radio field", 1)[0]
        self.assertGreaterEqual(binary_sections.count('type="radio"'), 4)
        self.assertNotIn("<button", binary_sections)
        self.assertNotIn('role="radio"', binary_sections)
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))

    def test_semantic_binding_never_uses_labels_or_numeric_form_field_ids(self) -> None:
        for label in ("جنسیت", "وضعیت فارغ‌التحصیلی", "بارگذاری کارنامه", "هویت دانش‌آموز"):
            self.assertNotIn(label, self.css)
        self.assertNotRegex(self.css, r"#(?:field|input|gform_wrapper|gform)_\d+")
        self.assertNotRegex(self.css, r"\[for=[^\]]*\d+")

    def test_section_icons_are_exact_local_assets_bound_only_to_explicit_roles(self) -> None:
        for role, expected in SECTION_ICONS.items():
            filename, *geometry = expected
            self.assertIn(f".{role} .gsection_title::before", self.css)
            self.assertIn(f'background-image: url("icons/{filename}");', self.css)
            self.assertIn(f"gsection {role}", self.fixtures)
            asset = (ICONS / filename).read_text(encoding="utf-8")
            self.assertIn('viewBox="0 0 24 24"', asset)
            self.assertIn('stroke="#1D4ED8"', asset)
            for fragment in geometry:
                self.assertIn(fragment, asset)
        tile_block = next(body for selector, body in blocks(self.css) if "srwf-role-section-identity .gsection_title::before" in selector and "srwf-role-section-contact" in selector)
        self.assertIn("flex: 0 0 40px;", tile_block)
        self.assertIn("inline-size: 40px;", tile_block)
        self.assertIn("block-size: 40px;", tile_block)
        self.assertIn("border-radius: 10px;", tile_block)
        self.assertIn("background-color: #EDF1FC;", tile_block)
        self.assertIn("background-size: 20px 20px;", tile_block)
        self.assertNotIn(".gfield--type-section .gsection_title::before {", self.css)
        self.assertNotIn("aria-label", "".join(path.read_text(encoding="utf-8") for path in ICONS.glob("section-*.svg")))

    def test_unmapped_section_fixture_receives_no_inferred_icon(self) -> None:
        self.assertIn('class="gfield gfield--type-section gsection"><h3 class="gsection_title"></h3></div>', self.fixtures)
        self.assertNotIn(":nth-child", self.css)
        self.assertNotIn(":nth-of-type", self.css)

    def test_report_card_initial_gpfup_is_explicit_role_scoped_and_exact(self) -> None:
        self.assertIn(f"gfield--input-type-fileupload {REPORT_ROLE}", self.fixtures)
        self.assertIn('class="gpfup gpfup--strict gform-theme__no-reset--children"', self.fixtures)
        report_blocks = [(selector, body) for selector, body in blocks(self.css) if "gpfup" in selector or "gform_fileupload_rules" in selector]
        self.assertTrue(report_blocks)
        for selector, _ in report_blocks:
            self.assertIn(f".gfield.{REPORT_ROLE}", selector)
        initial = [(selector, body) for selector, body in report_blocks if ".gpfup__droparea" in selector or ".gpfup__select-files" in selector]
        for selector, _ in initial:
            self.assertIn(".gpfup:not(.gpfup--has-files)", selector)
        droparea = next(body for selector, body in blocks(self.css) if selector.endswith(".gpfup:not(.gpfup--has-files) .gpfup__droparea"))
        self.assertIn("min-block-size: 96px;", droparea)
        self.assertIn("padding: 16px;", droparea)
        self.assertIn("border: 1.5px dashed #8690A1;", droparea)
        self.assertIn("border-radius: 12px;", droparea)
        self.assertIn("min-inline-size: 0;", droparea)
        self.assertIn('background-image: url("icons/report-card-file.svg");', self.css)

    def test_report_has_files_fixture_remains_host_owned_and_usable(self) -> None:
        self.assertIn("gpfup--has-files", self.fixtures)
        self.assertIn('class="gpfup__files"', self.fixtures)
        self.assertIn('class="gpfup__delete"', self.fixtures)
        report_source = self._role_bodies(REPORT_ROLE)
        self.assertNotIn("display: none", report_source)
        self.assertNotIn("visibility: hidden", report_source)
        self.assertNotIn(".gpfup__files", self.css)
        self.assertNotIn(".gpfup__delete", self.css)
        self.assertIn(".gpfup:not(.gpfup--has-files) .gpfup__droparea", self.css)

    def test_photo_fixture_does_not_receive_report_specific_or_post_upload_rules(self) -> None:
        self.assertIn('class="gpfup gpfup--strict gpfup--images-only gform-theme__no-reset--children"', self.fixtures)
        self.assertNotIn("gpfup--images-only", self._role_bodies(REPORT_ROLE))
        self.assertNotIn("gpfup--images-only", self.css)
        self.assertNotIn("srwf-role-student-photo-upload", self.css)

    def test_report_surface_is_intrinsically_narrow_safe(self) -> None:
        droparea = next(body for selector, body in blocks(self.css) if selector.endswith(".gpfup:not(.gpfup--has-files) .gpfup__droparea"))
        self.assertIn("box-sizing: border-box;", droparea)
        self.assertIn("display: flex;", droparea)
        self.assertIn("min-inline-size: 0;", droparea)
        self.assertNotIn("inline-size: 840px", droparea)

    def test_no_production_javascript_or_behavior_takeover_added(self) -> None:
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))
        self.assertNotIn("onclick", self.css)

    def _role_bodies(self, role: str) -> str:
        return "\n".join(body for selector, body in blocks(self.css) if role in selector)


if __name__ == "__main__":
    unittest.main()
