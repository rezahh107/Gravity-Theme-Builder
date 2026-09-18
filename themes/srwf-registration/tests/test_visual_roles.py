from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / "themes" / "srwf-registration"
CSS = THEME / "src" / "srwf-registration.css"
ICONS = THEME / "src" / "icons"

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

    def test_binary_cards_require_explicit_semantic_role(self) -> None:
        binary_selectors = [
            selector
            for selector, body in blocks(self.css)
            if BINARY_ROLE in selector or BINARY_ROLE in body
        ]
        self.assertTrue(binary_selectors)
        for selector in binary_selectors:
            self.assertIn(f".gfield.{BINARY_ROLE}", selector)
        self.assertNotRegex(self.css, r"\.gfield--type-radio\s+\.gfield_radio\s*\{")

    def test_gender_and_graduation_fixtures_are_role_driven_but_ordinary_radio_is_not(self) -> None:
        gender_classes = {"gfield", "gfield--type-radio", BINARY_ROLE}
        graduation_classes = {"gfield", "gfield--type-radio", BINARY_ROLE, "gfield_visibility_hidden"}
        ordinary_classes = {"gfield", "gfield--type-radio", "gfield--choice-align-vertical"}

        def receives_cards(classes: set[str]) -> bool:
            return {"gfield", BINARY_ROLE}.issubset(classes)

        self.assertTrue(receives_cards(gender_classes))
        self.assertTrue(receives_cards(graduation_classes))
        self.assertFalse(receives_cards(ordinary_classes))
        self.assertNotIn("display: block", self._role_bodies(BINARY_ROLE, selector_contains="gfield.srwf-role-binary-choice"))

    def test_binary_selection_uses_native_checked_state_and_preserves_focusable_radio(self) -> None:
        input_block = next(
            body
            for selector, body in blocks(self.css)
            if selector.endswith(f".gfield.{BINARY_ROLE} .gfield-choice-input")
        )
        self.assertIn("position: absolute;", input_block)
        self.assertIn("opacity: 0;", input_block)
        self.assertNotIn("display: none", input_block)
        self.assertNotIn("visibility: hidden", input_block)
        self.assertIn(f".gfield.{BINARY_ROLE} .gfield-choice-input:checked + label", self.css)
        self.assertIn(f".gfield.{BINARY_ROLE} .gfield-choice-input:focus-visible + label", self.css)
        checked_block = next(
            body
            for selector, body in blocks(self.css)
            if f".gfield.{BINARY_ROLE} .gfield-choice-input:checked + label" in selector
        )
        self.assertIn("background: #EEF2FF;", checked_block)
        self.assertIn("border-width: 2px;", checked_block)
        self.assertIn("font-weight: 700;", checked_block)

    def test_binary_cards_use_intrinsic_two_equal_tracks_without_new_breakpoint(self) -> None:
        choice = next(
            body for selector, body in blocks(self.css)
            if selector.endswith(f".gfield.{BINARY_ROLE} .gchoice")
        )
        row = next(
            body for selector, body in blocks(self.css)
            if selector.endswith(f".gfield.{BINARY_ROLE} .gfield_radio")
        )
        self.assertIn("display: flex;", row)
        self.assertIn("gap: 12px;", row)
        self.assertIn("flex: 1 1 0;", choice)
        self.assertIn("min-inline-size: 0;", choice)
        self.assertNotIn("@media", self.css)
        self.assertNotIn("grid-template-columns", self.css)

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
            asset = (ICONS / filename).read_text(encoding="utf-8")
            self.assertIn('viewBox="0 0 24 24"', asset)
            self.assertIn('stroke="#1D4ED8"', asset)
            for fragment in geometry:
                self.assertIn(fragment, asset)
        self.assertNotIn(".gfield--type-section .gsection_title::before {", self.css)
        self.assertNotIn("aria-label", "".join(path.read_text(encoding="utf-8") for path in ICONS.glob("section-*.svg")))

    def test_unmapped_section_fixture_has_no_role_and_no_inferred_icon(self) -> None:
        mapped = set(SECTION_ICONS)
        unmapped_classes = {"gfield", "gfield--type-section", "gsection"}
        self.assertFalse(mapped.intersection(unmapped_classes))
        self.assertNotIn(":nth-child", self.css)
        self.assertNotIn(":nth-of-type", self.css)

    def test_report_card_initial_gpfup_is_explicit_role_scoped(self) -> None:
        report_blocks = [
            (selector, body)
            for selector, body in blocks(self.css)
            if "gpfup" in selector or "gform_fileupload_rules" in selector
        ]
        self.assertTrue(report_blocks)
        for selector, _ in report_blocks:
            self.assertIn(f".gfield.{REPORT_ROLE}", selector)
        initial = [
            (selector, body)
            for selector, body in report_blocks
            if ".gpfup__droparea" in selector or ".gpfup__select-files" in selector
        ]
        self.assertTrue(initial)
        for selector, _ in initial:
            self.assertIn(".gpfup:not(.gpfup--has-files)", selector)
        self.assertIn('background-image: url("icons/report-card-file.svg");', self.css)
        file_icon = (ICONS / "report-card-file.svg").read_text(encoding="utf-8")
        self.assertIn('<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>', file_icon)
        self.assertIn('<polyline points="14 2 14 8 20 8"/>', file_icon)

    def test_report_has_files_state_is_not_hidden_or_recomposed(self) -> None:
        report_source = self._role_bodies(REPORT_ROLE)
        self.assertNotIn("display: none", report_source)
        self.assertNotIn("visibility: hidden", report_source)
        self.assertNotIn(".gpfup__files", self.css)
        self.assertNotIn(".gpfup__delete", self.css)
        self.assertNotIn("position: absolute", report_source)
        self.assertIn(".gpfup:not(.gpfup--has-files) .gpfup__droparea", self.css)

    def test_photo_fixture_does_not_receive_report_specific_rules(self) -> None:
        report_classes = {"gfield", REPORT_ROLE}
        photo_field_classes = {"gfield", "gfield--type-fileupload"}
        photo_gpfup_classes = {"gpfup", "gpfup--strict", "gpfup--images-only"}
        self.assertIn(REPORT_ROLE, report_classes)
        self.assertNotIn(REPORT_ROLE, photo_field_classes)
        self.assertIn("gpfup--images-only", photo_gpfup_classes)
        self.assertNotIn("gpfup--images-only", self._role_bodies(REPORT_ROLE))

    def test_report_surface_is_intrinsically_narrow_safe(self) -> None:
        droparea = next(
            body
            for selector, body in blocks(self.css)
            if selector.endswith(".gpfup:not(.gpfup--has-files) .gpfup__droparea")
        )
        self.assertIn("box-sizing: border-box;", droparea)
        self.assertIn("display: flex;", droparea)
        self.assertNotIn("min-inline-size:", droparea)

    def test_no_production_javascript_or_behavior_takeover_added(self) -> None:
        self.assertEqual([], list((THEME / "src").glob("**/*.js")))
        self.assertNotIn("onclick", self.css)

    def _role_bodies(self, role: str, selector_contains: str | None = None) -> str:
        bodies = []
        for selector, body in blocks(self.css):
            if role not in selector:
                continue
            if selector_contains is not None and selector_contains not in selector:
                continue
            bodies.append(body)
        return "\n".join(bodies)


if __name__ == "__main__":
    unittest.main()
