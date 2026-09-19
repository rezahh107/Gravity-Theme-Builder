from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
REFERENCE = THEME / "reference"
CURRENT = REFERENCE / "SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md"
HISTORICAL = REFERENCE / "SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md"
VISUAL_AUTHORITY = REFERENCE / "VISUAL_AUTHORITY.md"
IMPLEMENTATION_MAP = THEME / "IMPLEMENTATION_MAP.md"
SRC_README = THEME / "src" / "README.md"
CSS = THEME / "src" / "srwf-registration.css"

HISTORICAL_BLOB_SHA = "3fac5772cbe356965d98de64950ef0fbec8d7f21"


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()


class CurrentOwnerAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = CURRENT.read_text(encoding="utf-8")
        cls.historical = HISTORICAL.read_text(encoding="utf-8")
        cls.authority = VISUAL_AUTHORITY.read_text(encoding="utf-8")
        cls.implementation_map = IMPLEMENTATION_MAP.read_text(encoding="utf-8")
        cls.src_readme = SRC_README.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")

    def test_historical_drive_backed_v101_mirror_remains_byte_exact(self) -> None:
        self.assertEqual(HISTORICAL_BLOB_SHA, git_blob_sha(HISTORICAL))
        self.assertIn("upstream_revision_id: \"3\"", self.authority)
        self.assertIn("032750fc4ae763b45b2fb136fc56b4543f38b9638617563d4082993a0cf54f58", self.authority)
        self.assertIn("exact historical predecessor", self.authority)

    def test_current_owner_reconciliation_has_honest_provenance(self) -> None:
        self.assertIn("OWNER:SRWF-2026-09-19", self.current)
        self.assertIn("CURRENT_OWNER_PROJECT_AUTHORITY", self.current)
        self.assertIn("does **not** have an exact immutable upstream Google Drive revision", self.current)
        self.assertNotIn("upstream_revision_id:", self.current)
        self.assertNotIn("upstream_export_sha256:", self.current)
        self.assertIn("immutable_upstream_drive_revision: NOT_AVAILABLE_TO_EXECUTOR", self.authority)

    def test_current_owner_destination_includes_visual_repair_lock(self) -> None:
        required = (
            "production desktop breakpoint: `960 CSS px`",
            "`desktop_short_field_pairings: HOST_OWNED / OWNER_CONFIGURABLE`",
            "resulting desktop outer max width: `904px`",
            "box shadow: `none`",
            "Form title — mobile | `24px` | `700` | `1.5`",
            "Form title — desktop | `26px` | `700` | `1.5`",
            "Section heading | `18px` | `700` | `1.5`",
            "Field label | `15px` | `600` | `1.5`",
            "Control value | `16px` | `400` | `1.5`",
            "Helper | `14px` | `400` | `1.5`",
            "Field error | `14px` | `600` | `1.5`",
            "Primary action | `16px` | `700` | `1.5`",
            "field vertical rhythm: `24px`",
            "major section rhythm: `32px`",
            "outline: `2px solid #1D4ED8`",
            "outline offset: `2px`",
            "above the input where supported",
            "Every authentic Gravity Forms Radio field inside admitted SRWF Registration uses card presentation",
            "minimum card/control target height: `52px`",
            "gap: `12px`",
            "unselected card border: `1px solid #8690A1`",
            "selected card border: `2px solid #1D4ED8`",
            "visible non-color dot/shape cue",
            "tile: `40px × 40px`",
            "minimum height: `96px`",
            "every admitted initial upload surface has a visible decorative icon",
            "visible photo/camera icon",
        )
        for value in required:
            self.assertIn(value, self.current)

    def test_current_authority_preserves_host_owned_boundaries(self) -> None:
        for value in (
            "GTB owns presentation, not business/content structure",
            "must not depend on DOM position, `nth-child`, label text",
            "GTB does not define a canonical short-field pairing list",
            "Gravity Forms remains authoritative for validation lifecycle",
            "GTB does not define crop ratio or crop dimensions for v1",
            "GTB owns appearance only",
        ):
            self.assertIn(value, self.current)

    def test_implementation_docs_track_repaired_destination_and_unresolved_boundaries(self) -> None:
        self.assertIn("Production breakpoint | `960 CSS px`", self.implementation_map)
        self.assertIn("HOST_OWNED / OWNER_CONFIGURABLE", self.implementation_map)
        self.assertIn("All Radio choices", self.implementation_map)
        self.assertIn("gpfup--images-only", self.implementation_map)
        self.assertIn("student-photo-upload.svg", self.implementation_map)
        self.assertIn("Diagnostic package v0.3.5", self.implementation_map)
        self.assertIn("OWNER_RUNTIME_REQUIRED", self.implementation_map)
        self.assertIn("0.1.14", self.src_readme)
        self.assertIn("student-photo-upload.svg", self.src_readme)
        self.assertIn("960px", self.src_readme)
        self.assertIn("above-input", self.src_readme)
        self.assertIn("--gf-ctrl-select-padding-x", self.implementation_map)

    def test_current_authorized_visual_destination_is_present_without_broad_page_takeover(self) -> None:
        self.assertIn("@media (min-width: 960px)", self.css)
        self.assertIn("--gf-form-gap-y: 24px", self.css)
        self.assertIn("--gf-ctrl-line-height: 1.5", self.css)
        self.assertIn("--gf-ctrl-select-padding-x: 24px 32px", self.css)
        self.assertIn("--gf-ctrl-label-line-height-primary: 1.5", self.css)
        self.assertIn("--gf-ctrl-btn-line-height: 1.5", self.css)
        self.assertIn("max-inline-size: 904px", self.css)
        self.assertIn("padding-inline: 32px", self.css)
        self.assertIn("box-shadow: none", self.css)
        self.assertIn(".gfield.gfield--type-radio", self.css)
        self.assertNotIn(".gfield.srwf-role-binary-choice .gfield_radio", self.css)
        self.assertIn("background: #EDF1FC", self.css)
        self.assertIn('background-image: url("icons/student-photo-upload.svg")', self.css)
        self.assertNotIn("#F6F8FB", self.css, "page background must remain host-integration-owned until a safe seam is proven")
        self.assertNotIn("!important", self.css)


if __name__ == "__main__":
    unittest.main()
