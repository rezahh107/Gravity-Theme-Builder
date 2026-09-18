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
        self.assertIn("historical exact predecessor", self.authority)

    def test_current_owner_reconciliation_has_honest_provenance(self) -> None:
        self.assertIn("OWNER:SRWF-2026-09-19", self.current)
        self.assertIn("CURRENT_OWNER_PROJECT_AUTHORITY", self.current)
        self.assertIn("does **not** have an exact immutable upstream Google Drive revision", self.current)
        self.assertNotIn("upstream_revision_id:", self.current)
        self.assertNotIn("upstream_export_sha256:", self.current)
        self.assertIn("immutable_upstream_drive_revision: NOT_AVAILABLE_TO_EXECUTOR", self.authority)

    def test_previously_unresolved_design_decisions_are_now_explicit_current_destination(self) -> None:
        required = (
            "production desktop breakpoint: `960 CSS px`",
            "`desktop_short_field_pairings: HOST_OWNED / OWNER_CONFIGURABLE`",
            "resulting desktop outer max width: `904px`",
            "box shadow: `none`",
            "Form title — mobile | `24px` | `700` | `1.5`",
            "Form title — desktop | `26px` | `700` | `1.5`",
            "Helper | `14px` | `400` | `1.5`",
            "Field error | `14px` | `600` | `1.5`",
            "field vertical rhythm: `24px`",
            "major section rhythm: `32px`",
            "outline: `2px solid #1D4ED8`",
            "outline offset: `2px`",
            "above the input where supported",
            "minimum card/control target height: `52px`",
            "gap: `12px`",
            "subtle primary tint `#EDF1FC`",
            "tile: `40px × 40px`",
            "minimum height: `96px`",
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

    def test_implementation_docs_do_not_present_superseded_states_as_current(self) -> None:
        self.assertIn("Production breakpoint | `960 CSS px`", self.implementation_map)
        self.assertIn("HOST_OWNED / OWNER_CONFIGURABLE", self.implementation_map)
        self.assertIn("old below-input choice superseded", self.implementation_map)
        self.assertIn("OWNER_AUTHORIZED / NEXT_VISUAL_BATCH", self.implementation_map)
        self.assertIn("960px", self.src_readme)
        self.assertIn("above-input", self.src_readme)
        self.assertNotIn("production breakpoint, desktop short-field pairings, desktop shadow", self.src_readme)

    def test_foundation_batch_did_not_silently_implement_new_visual_destination(self) -> None:
        self.assertNotIn("@media", self.css)
        self.assertNotIn("box-shadow", self.css)
        self.assertNotIn("--gf-form-gap-y", self.css)
        self.assertIn("production CSS from current main", self.src_readme)
        self.assertIn("including PR #15's binary-choice row/equal-track behavior, is preserved unchanged", self.src_readme)


if __name__ == "__main__":
    unittest.main()
