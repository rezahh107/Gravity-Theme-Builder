from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / "themes" / "srwf-registration"
CSS = THEME / "src" / "srwf-registration.css"
ICONS = THEME / "src" / "icons"
FIXTURES = THEME / "tests" / "fixtures" / "semantic-roles-runtime-shapes.md"

RADIO_SCOPE = ".gfield.gfield--type-radio"
REPORT_ROLE = "srwf-role-report-card-upload"
STUDENT_PHOTO_UPLOAD_ICON = "student-photo-upload.svg"
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

    def test_all_authentic_radio_fields_share_card_presentation_without_role_gate(self) -> None:
        ordinary = '<fieldset class="gfield gfield--type-radio gfield--type-choice gfield--input-type-radio gfield--choice-align-vertical">'
        self.assertIn(ordinary, self.fixtures)
        relevant = [
            selector
            for selector, _ in blocks(self.css)
            if ".gfield_radio" in selector or ".gchoice" in selector or ".gfield-choice-input" in selector
        ]
        self.assertTrue(relevant)
        for selector in relevant:
            self.assertIn(RADIO_SCOPE, selector)
            self.assertNotIn("srwf-role-binary-choice", selector)
        self.assertNotRegex(self.css, r"(?m)^\s*\.gfield_radio\s*\{")
        self.assertNotRegex(self.css, r"(?m)^\s*\.gchoice\s*\{")

    def test_radio_cards_preserve_native_input_label_checked_and_focus_ownership(self) -> None:
        input_block = next(body for selector, body in blocks(self.css) if selector.endswith(f"{RADIO_SCOPE} .gfield-choice-input"))
        self.assertIn("position: absolute;", input_block)
        self.assertIn("inline-size: 1px;", input_block)
        self.assertIn("block-size: 1px;", input_block)
        self.assertIn("opacity: 0;", input_block)
        self.assertNotIn("display: none", input_block)
        self.assertNotIn("visibility: hidden", input_block)

        label_block = next(body for selector, body in blocks(self.css) if selector.endswith(f"{RADIO_SCOPE} .gchoice label"))
        self.assertIn("inline-size: 100%;", label_block)
        self.assertIn("min-block-size: 52px;", label_block)
        self.assertIn("border: 1px solid #8690A1;", label_block)
        self.assertIn("border-radius: 10px;", label_block)
        self.assertIn("overflow-wrap: anywhere;", label_block)

        checked_block = next(body for selector, body in blocks(self.css) if f"{RADIO_SCOPE} .gfield-choice-input:checked + label" in selector and "::before" not in selector)
        self.assertIn("background: #EDF1FC;", checked_block)
        self.assertIn("border-color: #1D4ED8;", checked_block)
        self.assertIn("border-width: 2px;", checked_block)
        self.assertIn("font-weight: 700;", checked_block)

        cue_block = next(body for selector, body in blocks(self.css) if f"{RADIO_SCOPE} .gfield-choice-input:checked + label::before" in selector)
        self.assertIn("background: #1D4ED8;", cue_block)
        self.assertIn("box-shadow: inset 0 0 0 3px #EDF1FC;", cue_block)

        focus_block = next(body for selector, body in blocks(self.css) if f"{RADIO_SCOPE} .gfield-choice-input:focus-visible + label" in selector)
        self.assertIn("outline: 2px solid #1D4ED8;", focus_block)
        self.assertIn("outline-offset: 2px;", focus_block)
        self.assertIn("box-shadow: none;", focus_block)

        radio_sections = self.fixtures.split("## Report Card", 1)[0]
        self.assertGreaterEqual(radio_sections.count('type="radio"'), 6)
        self.assertNotIn("<button", radio_sections)
        self.assertNotIn('role="radio"', radio_sections)

    def test_radio_layout_is_content_driven_wrap_safe_and_not_binary_count_specific(self) -> None:
        row = next(body for selector, body in blocks(self.css) if selector.endswith(f"{RADIO_SCOPE} .gfield_radio"))
        choice = next(body for selector, body in blocks(self.css) if selector.endswith(f"{RADIO_SCOPE} .gchoice"))
        self.assertIn("display: flex;", row)
        self.assertIn("flex-flow: row wrap;", row)
        self.assertIn("gap: 12px;", row)
        self.assertIn("flex: 1 1 8rem;", choice)
        self.assertIn("min-inline-size: 0;", choice)
        self.assertNotIn("grid-template-columns", self.css)
        self.assertEqual(1, self.css.count("@media (min-width: 960px)"))

    def test_presentation_identity_avoids_ids_labels_option_text_and_dom_position(self) -> None:
        for label in ("جنسیت", "وضعیت فارغ‌التحصیلی", "بارگذاری کارنامه", "هویت دانش‌آموز"):
            self.assertNotIn(label, self.css)
        self.assertNotRegex(self.css, r"#(?:field|input|choice|label|gform_wrapper|gform)_\d+")
        self.assertNotRegex(self.css, r"\[for=[^\]]*\d+")
        self.assertNotIn(":nth-child", self.css)
        self.assertNotIn(":nth-of-type", self.css)

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
        heading_block = next(body for selector, body in blocks(self.css) if "srwf-role-section-identity .gsection_title" in selector and "::before" not in selector)
        self.assertIn("gap: 12px;", heading_block)
        self.assertNotIn(".gfield--type-section .gsection_title::before {", self.css)
        self.assertNotIn("aria-label", "".join(path.read_text(encoding="utf-8") for path in ICONS.glob("section-*.svg")))

    def test_unmapped_section_fixture_receives_no_inferred_icon(self) -> None:
        self.assertIn('class="gfield gfield--type-section gsection"><h3 class="gsection_title"></h3></div>', self.fixtures)
        self.assertNotIn(":nth-child", self.css)
        self.assertNotIn(":nth-of-type", self.css)

    def test_initial_gpfup_family_has_shared_icon_slot_and_bounded_glyph_specializations(self) -> None:
        self.assertIn(f"gfield--input-type-fileupload {REPORT_ROLE}", self.fixtures)
        self.assertIn('class="gpfup gpfup--strict gform-theme__no-reset--children"', self.fixtures)
        self.assertIn('class="gpfup gpfup--strict gpfup--images-only gform-theme__no-reset--children"', self.fixtures)

        shared = next(
            body
            for selector, body in blocks(self.css)
            if selector.endswith(".gfield--type-fileupload .gpfup:not(.gpfup--has-files) .gpfup__droparea")
        )
        self.assertIn("min-block-size: 96px;", shared)
        self.assertIn("padding: 16px;", shared)
        self.assertIn("border: 1px dashed #8690A1;", shared)
        self.assertIn("border-radius: 12px;", shared)
        self.assertIn("min-inline-size: 0;", shared)
        self.assertIn("flex-wrap: wrap;", shared)

        icon_selector, icon_slot = next(
            (selector, body)
            for selector, body in blocks(self.css)
            if f".gfield.{REPORT_ROLE} .gpfup:not(.gpfup--has-files) .gpfup__droparea::before" in selector
            and ".gpfup.gpfup--images-only:not(.gpfup--has-files) .gpfup__droparea::before" in selector
        )
        self.assertIn(".srwf-registration-theme_wrapper", icon_selector)
        self.assertIn("flex: 0 0 40px;", icon_slot)
        self.assertIn("inline-size: 40px;", icon_slot)
        self.assertIn("block-size: 40px;", icon_slot)
        self.assertIn("border-radius: 10px;", icon_slot)
        self.assertIn("background-color: #F1F5F9;", icon_slot)
        self.assertIn("background-position: center;", icon_slot)
        self.assertIn("background-repeat: no-repeat;", icon_slot)
        self.assertIn("background-size: 24px 24px;", icon_slot)
        self.assertNotIn("background-image", icon_slot, "shared slot must not collapse glyph identity into one asset")

        report_icon = next(
            body
            for selector, body in blocks(self.css)
            if selector.strip().endswith(f".gfield.{REPORT_ROLE} .gpfup:not(.gpfup--has-files) .gpfup__droparea::before")
            and "," not in selector
        )
        self.assertEqual('background-image: url("icons/report-card-file.svg");', report_icon.strip())

        photo_icon = next(
            body
            for selector, body in blocks(self.css)
            if selector.strip().endswith(".gfield--type-fileupload .gpfup.gpfup--images-only:not(.gpfup--has-files) .gpfup__droparea::before")
            and "," not in selector
        )
        self.assertEqual(f'background-image: url("icons/{STUDENT_PHOTO_UPLOAD_ICON}");', photo_icon.strip())

        asset = (ICONS / STUDENT_PHOTO_UPLOAD_ICON).read_text(encoding="utf-8")
        self.assertIn('viewBox="0 0 24 24"', asset)
        self.assertIn('stroke="#475467"', asset)
        self.assertIn('<path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>', asset)
        self.assertIn('<circle cx="12" cy="13" r="4"/>', asset)
        self.assertNotIn("aria-label", asset)

    def test_gpfup_post_upload_behavior_remains_host_owned(self) -> None:
        self.assertIn("gpfup--has-files", self.fixtures)
        self.assertIn('class="gpfup__files"', self.fixtures)
        self.assertIn('class="gpfup__delete"', self.fixtures)
        selectors = "\n".join(selector for selector, _ in blocks(self.css)).lower()
        self.assertNotIn(".gpfup__files", selectors)
        self.assertNotIn(".gpfup__delete", selectors)
        self.assertNotIn("crop", selectors)
        self.assertNotIn("preview", selectors)
        self.assertIn(".gpfup:not(.gpfup--has-files) .gpfup__droparea", self.css)
        for selector, _ in blocks(self.css):
            if ".gpfup__droparea::before" in selector:
                self.assertIn(":not(.gpfup--has-files)", selector)

    def test_upload_family_is_intrinsically_narrow_safe(self) -> None:
        shared = next(
            body
            for selector, body in blocks(self.css)
            if selector.endswith(".gfield--type-fileupload .gpfup:not(.gpfup--has-files) .gpfup__droparea")
        )
        self.assertIn("box-sizing: border-box;", shared)
        self.assertIn("display: flex;", shared)
        self.assertIn("min-inline-size: 0;", shared)
        self.assertNotIn("inline-size: 840px", shared)

    def test_no_production_javascript_or_behavior_takeover_added(self) -> None:
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))
        self.assertNotIn("onclick", self.css)


if __name__ == "__main__":
    unittest.main()
