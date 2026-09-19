from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / "themes" / "srwf-registration"
REFERENCE = THEME / "reference"
VISUAL_AUTHORITY = REFERENCE / "VISUAL_AUTHORITY.md"
V101 = REFERENCE / "SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md"
MATERIALIZER = REFERENCE / "materialize_reference.sh"
IMPLEMENTATION_MAP = THEME / "IMPLEMENTATION_MAP.md"
SRC = THEME / "src"
CSS = SRC / "srwf-registration.css"
SRC_README = SRC / "README.md"

V101_REPOSITORY_BLOB_SHA = "3fac5772cbe356965d98de64950ef0fbec8d7f21"
V101_UPSTREAM_EXPORT_SHA256 = "032750fc4ae763b45b2fb136fc56b4543f38b9638617563d4082993a0cf54f58"
V101_UPSTREAM_FILE_ID = "1t0fDtg-hnq5iHiLIO0wMJyTvOc-dVf4AJ2ULfYdfLgQ"
V101_UPSTREAM_REVISION_ID = "3"
BASE_V100_BLOB_SHA = "7400b7d0f97f245f090fd84893deb62c3ec83956"
ARTIFACT_SHA256 = "436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000"

EXPECTED_LOCAL_URLS = {
    "icons/report-card-file.svg",
    "icons/section-contact.svg",
    "icons/section-education.svg",
    "icons/section-identity.svg",
    "icons/section-school-documents.svg",
    "icons/section-student-photo.svg",
}

SECTION_GEOMETRY = {
    "هویت دانش‌آموز": "section-identity.svg",
    "اطلاعات تماس": "section-contact.svg",
    "تحصیلات": "section-education.svg",
    "مدرسه و مدارک": "section-school-documents.svg",
    "عکس دانش‌آموز": "section-student-photo.svg",
}


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def authority_registry_ids(source: str) -> set[str]:
    match = re.search(
        r"<!-- SRWF_VISUAL_AUTHORITY_REGISTRY_BEGIN -->(.*?)<!-- SRWF_VISUAL_AUTHORITY_REGISTRY_END -->",
        source,
        re.S,
    )
    if not match:
        return set()
    return set(re.findall(r"(?m)^\s{2}(VA:[A-Z0-9._-]+):\s*$", match.group(1)))


def cited_authority_ids(source: str) -> set[str]:
    return set(re.findall(r"VA:[A-Z0-9._-]+", source))


def local_css_urls(css_source: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)", css_source):
        value = match.group(2).strip()
        if not value or value.startswith(("data:", "http://", "https://", "//", "#")):
            continue
        values.append(value.split("?", 1)[0].split("#", 1)[0])
    return values


def unresolved_local_urls(css_path: Path, install_root: Path) -> list[str]:
    css_source = css_path.read_text(encoding="utf-8")
    unresolved: list[str] = []
    root = install_root.resolve()
    for value in local_css_urls(css_source):
        candidate = (css_path.parent / value).resolve()
        try:
            inside = os.path.commonpath((str(root), str(candidate))) == str(root)
        except ValueError:
            inside = False
        if not inside or not candidate.is_file():
            unresolved.append(value)
    return unresolved


def svg_child_geometry(source: str) -> list[tuple[str, tuple[tuple[str, str], ...]]]:
    root = ET.fromstring(source.strip())
    result: list[tuple[str, tuple[tuple[str, str], ...]]] = []
    for child in list(root):
        tag = child.tag.rsplit("}", 1)[-1]
        result.append((tag, tuple(sorted(child.attrib.items()))))
    return result


def artifact_section_svg(html: str, heading: str) -> str:
    pattern = re.compile(
        r'<div class="group-heading">\s*<span class="g-icon">\s*'
        r'(<svg.*?</svg>)\s*</span>\s*([^<]+?)\s*</div>',
        re.S,
    )
    for match in pattern.finditer(html):
        if match.group(2).strip() == heading:
            return match.group(1)
    raise AssertionError(f"admitted artifact does not contain section icon for {heading}")


def artifact_report_file_svg(html: str) -> str:
    match = re.search(r'<div class="file-icon">\s*(<svg.*?</svg>)\s*</div>', html, re.S)
    if not match:
        raise AssertionError("admitted artifact does not contain Report Card file icon")
    return match.group(1)


class SrwfAuthorityAndDeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.authority = VISUAL_AUTHORITY.read_text(encoding="utf-8")
        cls.contract = V101.read_text(encoding="utf-8")
        cls.implementation_map = IMPLEMENTATION_MAP.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.src_readme = SRC_README.read_text(encoding="utf-8")

    def test_v101_has_stable_repository_and_upstream_revision_identity(self) -> None:
        self.assertEqual(V101_REPOSITORY_BLOB_SHA, git_blob_sha(V101))
        self.assertIn(V101_UPSTREAM_EXPORT_SHA256, self.authority)
        self.assertIn(V101_UPSTREAM_FILE_ID, self.authority)
        self.assertRegex(self.authority, rf"upstream_revision_id:\s*[\"']?{V101_UPSTREAM_REVISION_ID}[\"']?")
        self.assertIn(BASE_V100_BLOB_SHA, self.authority)
        self.assertIn(ARTIFACT_SHA256, self.authority)
        self.assertIn("SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md", self.authority)

    def test_v101_is_the_exact_named_owner_revision_and_preserves_unresolved_states(self) -> None:
        self.assertIn("# SRWF Public Registration — Visual / UX Contract v1.0.1", self.contract)
        self.assertIn("version: 1.0.1", self.contract)
        self.assertIn("## 27. Owner resolution addendum — 2026-09-18", self.contract)
        for decision in (
            "gender_binary_choice",
            "graduation_status_binary_choice",
            "report_card_upload_initial",
            "student_photo_uploaded_state",
            "section_heading_iconography",
        ):
            self.assertIn(f"`{decision}`", self.contract)
        for unresolved in (
            "exact_production_breakpoint",
            "desktop_short_field_pairings",
            "desktop_shadow_exact_value",
            "form-title exact size/line-height",
            "helper/error exact sizes",
            "field/section rhythm",
            "focus-ring exact geometry/alpha",
        ):
            self.assertIn(unresolved, self.contract)
        self.assertIn(
            "This addendum is explicit Owner authority and supersedes any prior interpretation",
            self.contract,
        )

    def test_visual_authority_explicitly_relates_v100_v101_and_artifact(self) -> None:
        registry = authority_registry_ids(self.authority)
        self.assertEqual({"VA:ARTIFACT", "VA:VC-1.0.0", "VA:VC-1.0.1"}, registry)
        self.assertIn("historical/base contract", self.authority)
        self.assertIn("Section 27", self.authority)
        self.assertIn("supersedes only the prior interpretation", self.authority)
        self.assertIn("exact section-icon and report-card file-icon **geometry** is supplied by `VA:ARTIFACT`", self.authority)

    def test_implementation_map_cannot_cite_an_unregistered_visual_authority(self) -> None:
        registered = authority_registry_ids(self.authority)
        cited = cited_authority_ids(self.implementation_map)
        self.assertTrue(cited)
        self.assertEqual(set(), cited - registered, f"unregistered visual authority IDs: {sorted(cited - registered)}")
        self.assertNotIn("v1.0.1 + 2026-09-18 addendum", self.implementation_map)
        self.assertNotRegex(self.implementation_map, r"(?<!VA:)Visual Contract §")

    def test_implementation_driving_roles_have_retrievable_current_authority_paths(self) -> None:
        required_rows = {
            "Gender historical binary role": ("VA:VC-1.0.1", "VA:ARTIFACT", "current Owner reconciliation"),
            "Graduation Status historical binary role": ("current all-radio lock",),
            "Other authentic Radio groups": ("current Owner all-radio lock", ".gfield--type-radio"),
            "Section iconography": ("VA:VC-1.0.1", "VA:ARTIFACT", "section_heading_iconography"),
            "Report Card initial GPFUP": ("VA:VC-1.0.1", "VA:ARTIFACT", "report_card_upload_initial"),
            "Report Card `.gpfup--has-files`": ("VA:VC-1.0.1", "host-owned GPFUP lifecycle"),
            "Student Photo initial": ("authentic GPFUP image-only runtime/config evidence", "gpfup--images-only"),
            "Student Photo post-upload": ("VA:VC-1.0.1", "VA:ARTIFACT", "current reconciliation"),
        }
        traceability = self.implementation_map.split("## Visual-role authority traceability", 1)[1]
        lines = traceability.splitlines()
        for label, required in required_rows.items():
            row = next((line for line in lines if line.startswith(f"| {label} |")), None)
            self.assertIsNotNone(row, f"missing implementation-map row: {label}")
            for token in required:
                self.assertIn(token, row, f"{label} is missing authority token {token}")

    def test_production_icon_geometry_matches_the_admitted_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "OWNER_REFERENCE_new_7.html"
            subprocess.run(["bash", str(MATERIALIZER), str(output)], check=True, capture_output=True, text=True)
            self.assertEqual(ARTIFACT_SHA256, hashlib.sha256(output.read_bytes()).hexdigest())
            html = output.read_text(encoding="utf-8")

            for heading, filename in SECTION_GEOMETRY.items():
                expected = svg_child_geometry(artifact_section_svg(html, heading))
                actual = svg_child_geometry((SRC / "icons" / filename).read_text(encoding="utf-8"))
                self.assertEqual(expected, actual, f"icon geometry drift for {heading}")

            expected_report = svg_child_geometry(artifact_report_file_svg(html))
            actual_report = svg_child_geometry((SRC / "icons" / "report-card-file.svg").read_text(encoding="utf-8"))
            self.assertEqual(expected_report, actual_report, "Report Card file-icon geometry drift")

    def test_all_production_local_url_dependencies_resolve_inside_installable_src(self) -> None:
        urls = local_css_urls(self.css)
        self.assertEqual(EXPECTED_LOCAL_URLS, set(urls))
        self.assertEqual(6, len(urls))
        self.assertEqual([], unresolved_local_urls(CSS, SRC))

    def test_missing_referenced_asset_is_detected_by_dependency_closure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "src"
            shutil.copytree(SRC, copied)
            missing = copied / "icons" / "section-identity.svg"
            missing.unlink()
            unresolved = unresolved_local_urls(copied / "srwf-registration.css", copied)
            self.assertIn("icons/section-identity.svg", unresolved)

    def test_install_documentation_describes_actual_asset_and_addon_boundaries(self) -> None:
        self.assertIn("complete `src/` tree", self.src_readme)
        self.assertIn("icons/", self.src_readme)
        for dependency in EXPECTED_LOCAL_URLS:
            self.assertIn(Path(dependency).name, self.src_readme)
        self.assertIn("GP File Upload Pro — initial state only", self.src_readme)
        self.assertIn("shared SRWF upload-family CSS stops at `.gpfup--has-files`", self.src_readme)
        self.assertIn("Report Card specialization is explicit", self.src_readme)
        self.assertIn("gpfup--images-only", self.src_readme)
        self.assertIn("Student Photo post-upload/crop/re-crop/delete structure", self.src_readme)
        self.assertIn("OWNER_RUNTIME_REQUIRED / NOT_PROVEN", self.src_readme)
        self.assertIn("Upload/progress/validation/preview/delete/crop/storage remain GPFUP-owned", self.src_readme)


if __name__ == "__main__":
    unittest.main()
