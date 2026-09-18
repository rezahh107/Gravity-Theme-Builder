from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = THEME / "src" / "srwf-registration.css"

BINARY_ROLE = "srwf-role-binary-choice"
REPORT_ROLE = "srwf-role-report-card-upload"

GENDER_FIXTURE = f"""
<fieldset class="gfield gfield--type-radio {BINARY_ROLE}">
  <legend class="gfield_label gform-field-label">Gender</legend>
  <div class="ginput_container ginput_container_radio">
    <div class="gfield_radio">
      <div class="gchoice">
        <input id="choice_gender_1" class="gfield-choice-input" type="radio" name="gender" value="a" required>
        <label class="gform-field-label gform-field-label--type-inline" for="choice_gender_1">A</label>
      </div>
      <div class="gchoice">
        <input id="choice_gender_2" class="gfield-choice-input" type="radio" name="gender" value="b" required>
        <label class="gform-field-label gform-field-label--type-inline" for="choice_gender_2">B</label>
      </div>
    </div>
  </div>
</fieldset>
"""

GRADUATION_FIXTURE = GENDER_FIXTURE.replace("gender", "graduation").replace("Gender", "Graduation Status")

REPORT_INITIAL_FIXTURE = f"""
<div class="gfield gfield--type-fileupload {REPORT_ROLE}">
  <div class="ginput_container ginput_container_fileupload">
    <div class="gform_fileupload_multifile">
      <div class="gpfup gpfup--strict">
        <div class="gpfup__droparea"><button class="gpfup__select-files gform_button_select_files" type="button">Select</button></div>
      </div>
    </div>
    <span class="gfield_description gform_fileupload_rules">Rules</span>
  </div>
</div>
"""

REPORT_HAS_FILES_FIXTURE = f"""
<div class="gfield gfield--type-fileupload {REPORT_ROLE}">
  <div class="ginput_container ginput_container_fileupload">
    <div class="gform_fileupload_multifile">
      <div class="gpfup gpfup--strict gpfup--has-files">
        <div class="gpfup__files"><div class="gpfup__file"><span class="gpfup__file-info">report.pdf</span><button class="gpfup__delete" type="button">Delete</button></div></div>
        <div class="gpfup__droparea"><button class="gpfup__select-files gform_button_select_files" type="button">Select</button></div>
      </div>
    </div>
    <span class="gfield_description gform_fileupload_rules">Rules</span>
  </div>
</div>
"""

PHOTO_EMPTY_FIXTURE = """
<div class="gfield gfield--type-fileupload">
  <div class="ginput_container ginput_container_fileupload">
    <div class="gpfup gpfup--strict gpfup--images-only">
      <div class="gpfup__droparea"><button class="gpfup__select-files" type="button">Select</button></div>
    </div>
  </div>
</div>
"""


class FixtureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.elements: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.elements.append((tag, dict(attrs)))

    def classes(self) -> set[str]:
        result: set[str] = set()
        for _, attrs in self.elements:
            result.update((attrs.get("class") or "").split())
        return result


class AuthenticRoleFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.css = CSS.read_text(encoding="utf-8")

    def parse(self, source: str) -> FixtureParser:
        parser = FixtureParser()
        parser.feed(source)
        return parser

    def test_native_binary_fixture_keeps_real_radio_and_label_association(self) -> None:
        for fixture in (GENDER_FIXTURE, GRADUATION_FIXTURE):
            parsed = self.parse(fixture)
            radios = [attrs for tag, attrs in parsed.elements if tag == "input" and attrs.get("type") == "radio"]
            labels = [attrs for tag, attrs in parsed.elements if tag == "label"]
            self.assertEqual(2, len(radios))
            self.assertEqual(2, len(labels))
            radio_ids = {attrs.get("id") for attrs in radios}
            self.assertEqual(radio_ids, {attrs.get("for") for attrs in labels})
            self.assertTrue(all("disabled" not in attrs for attrs in radios))
            self.assertTrue(all(attrs.get("tabindex") != "-1" for attrs in radios))
            self.assertIn(BINARY_ROLE, parsed.classes())

        self.assertIn(f".gfield.{BINARY_ROLE} .gfield-choice-input:checked + label", self.css)
        self.assertIn(f".gfield.{BINARY_ROLE} .gfield-choice-input:focus-visible + label", self.css)
        self.assertNotIn("display: none", self.binary_role_css())
        self.assertNotIn("visibility: hidden", self.binary_role_css())

    def test_report_initial_fixture_models_proven_gpfup_consumer(self) -> None:
        classes = self.parse(REPORT_INITIAL_FIXTURE).classes()
        for expected in (REPORT_ROLE, "gpfup", "gpfup--strict", "gpfup__droparea", "gpfup__select-files", "gform_fileupload_rules"):
            self.assertIn(expected, classes)
        self.assertNotIn("gpfup--has-files", classes)
        self.assertIn(f".gfield.{REPORT_ROLE} .gpfup:not(.gpfup--has-files) .gpfup__droparea", self.css)

    def test_report_has_files_fixture_preserves_host_file_and_delete_consumers(self) -> None:
        classes = self.parse(REPORT_HAS_FILES_FIXTURE).classes()
        for expected in (
            REPORT_ROLE,
            "gpfup",
            "gpfup--strict",
            "gpfup--has-files",
            "gpfup__files",
            "gpfup__droparea",
            "gpfup__delete",
            "gpfup__select-files",
        ):
            self.assertIn(expected, classes)

        # The approved custom geometry is empty-state only. Uploaded file/delete markup stays host-owned.
        self.assertNotRegex(self.css, rf"{re.escape(REPORT_ROLE)}[^{{,]*\.gpfup__files")
        self.assertNotRegex(self.css, rf"{re.escape(REPORT_ROLE)}[^{{,]*\.gpfup__delete")
        self.assertNotIn("display: none", self.report_role_css())
        self.assertNotIn("visibility: hidden", self.report_role_css())

    def test_photo_fixture_cannot_match_report_role_contract(self) -> None:
        classes = self.parse(PHOTO_EMPTY_FIXTURE).classes()
        self.assertIn("gpfup--images-only", classes)
        self.assertNotIn(REPORT_ROLE, classes)
        self.assertNotIn("gpfup--images-only", self.report_role_css())

    def test_changed_components_keep_intrinsic_narrow_width_invariants(self) -> None:
        binary = self.binary_role_css()
        report = self.report_role_css()
        self.assertIn("flex: 1 1 0;", binary)
        self.assertIn("min-inline-size: 0;", binary)
        self.assertIn("overflow-wrap: anywhere;", binary)
        self.assertNotRegex(binary, r"min-inline-size:\s*[1-9][0-9]*px")
        self.assertIn("box-sizing: border-box;", report)
        self.assertNotRegex(report, r"min-inline-size:\s*[1-9][0-9]*px")
        self.assertNotIn("@media", self.css)

    def binary_role_css(self) -> str:
        return "\n".join(
            match.group(0)
            for match in re.finditer(r"[^{}]*srwf-role-binary-choice[^{}]*\{[^{}]*\}", self.css, re.S)
        )

    def report_role_css(self) -> str:
        return "\n".join(
            match.group(0)
            for match in re.finditer(r"[^{}]*srwf-role-report-card-upload[^{}]*\{[^{}]*\}", self.css, re.S)
        )


if __name__ == "__main__":
    unittest.main()
