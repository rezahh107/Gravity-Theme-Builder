from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
REFERENCE = THEME / "reference"
CURRENT = REFERENCE / "SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md"
HISTORICAL = REFERENCE / "SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md"
VISUAL_AUTHORITY = REFERENCE / "VISUAL_AUTHORITY.md"
IMPLEMENTATION_MAP = THEME / "IMPLEMENTATION_MAP.md"
SRC_README = THEME / "src" / "README.md"
THEME_PHP = THEME / "src" / "srwf-registration-theme.php"
CSS = THEME / "src" / "srwf-registration.css"
DIAGNOSTIC_PHP = THEME / "diagnostic" / "srwf-runtime-diagnostic.php"
VISUAL_DIAGNOSTIC = THEME / "diagnostic" / "assets" / "visual-repair-qualification.js"

HISTORICAL_BLOB_SHA = "3fac5772cbe356965d98de64950ef0fbec8d7f21"
HISTORICAL_GPFUP_RUNTIME_VERSION = "0.1.14"
CURRENT_THEME_VERSION = "0.1.16"
CURRENT_DIAGNOSTIC_VERSION = "0.3.6"


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()


def theme_version(source: str) -> str:
    match = re.search(r"const SRWF_REGISTRATION_THEME_VERSION = '([^']+)';", source)
    if not match:
        raise AssertionError("SRWF theme version constant not found")
    return match.group(1)


def current_gpfup_provenance_errors(surfaces: dict[str, str], current_version: str) -> list[str]:
    errors: list[str] = []
    current_markers = {
        "implementation_map": f"Current static theme implementation: `{current_version}`.",
        "current": f"theme `{current_version}` is the current static implementation",
        "authority": f"Theme `{current_version}` is the current static implementation",
        "src_readme": f"Current production package line: **{current_version}**.",
    }
    for name, marker in current_markers.items():
        if marker not in surfaces[name]:
            errors.append(f"{name}: missing current implementation marker {marker}")

    historical_markers = (
        f"Owner runtime of theme `{HISTORICAL_GPFUP_RUNTIME_VERSION}`",
        "historical evidence",
        "glyphs rendered",
        "visually detached",
    )
    for name in ("implementation_map", "current", "authority"):
        for marker in historical_markers:
            if marker not in surfaces[name]:
                errors.append(f"{name}: missing historical runtime marker {marker}")

    stale_current_patterns = (
        f"Theme `{HISTORICAL_GPFUP_RUNTIME_VERSION}` statically implements",
        f"Theme {HISTORICAL_GPFUP_RUNTIME_VERSION} statically implements",
        f"theme `{HISTORICAL_GPFUP_RUNTIME_VERSION}` implements the shared initial GPFUP",
    )
    for name in ("implementation_map", "current", "authority"):
        for pattern in stale_current_patterns:
            if pattern in surfaces[name]:
                errors.append(f"{name}: stale current-implementation attribution {pattern}")

    return errors


class CurrentOwnerAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = CURRENT.read_text(encoding="utf-8")
        cls.historical = HISTORICAL.read_text(encoding="utf-8")
        cls.authority = VISUAL_AUTHORITY.read_text(encoding="utf-8")
        cls.implementation_map = IMPLEMENTATION_MAP.read_text(encoding="utf-8")
        cls.src_readme = SRC_README.read_text(encoding="utf-8")
        cls.theme_php = THEME_PHP.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.diagnostic_php = DIAGNOSTIC_PHP.read_text(encoding="utf-8")
        cls.visual_diagnostic = VISUAL_DIAGNOSTIC.read_text(encoding="utf-8")
        cls.current_version = theme_version(cls.theme_php)
        cls.provenance_surfaces = {
            "implementation_map": cls.implementation_map,
            "current": cls.current,
            "authority": cls.authority,
            "src_readme": cls.src_readme,
        }

    def test_historical_drive_backed_v101_mirror_remains_byte_exact(self) -> None:
        self.assertEqual(HISTORICAL_BLOB_SHA, git_blob_sha(HISTORICAL))
        self.assertIn('upstream_revision_id: "3"', self.authority)
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

    def test_current_implementation_version_is_synchronized_across_authority_surfaces(self) -> None:
        self.assertEqual(CURRENT_THEME_VERSION, self.current_version)
        self.assertEqual([], current_gpfup_provenance_errors(self.provenance_surfaces, self.current_version))
        self.assertIn(f"Version: {CURRENT_DIAGNOSTIC_VERSION}", self.diagnostic_php)
        self.assertIn(f"const GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '{CURRENT_DIAGNOSTIC_VERSION}';", self.diagnostic_php)
        self.assertIn(f"var VERSION = '{CURRENT_DIAGNOSTIC_VERSION}';", self.visual_diagnostic)

    def test_pre_repair_stale_0_1_14_current_attribution_is_rejected(self) -> None:
        stale = dict(self.provenance_surfaces)
        stale["implementation_map"] = (
            "Theme 0.1.14 statically implements the Owner-authorized shared initial GPFUP icon/alignment family.\n"
            + stale["implementation_map"]
        )
        stale["current"] = (
            "theme `0.1.14` implements the shared initial GPFUP icon/alignment destination.\n"
            + stale["current"]
        )
        stale["authority"] = (
            "Theme `0.1.14` statically implements the shared initial GPFUP icon/alignment destination.\n"
            + stale["authority"]
        )
        errors = current_gpfup_provenance_errors(stale, self.current_version)
        self.assertTrue(errors, "pre-repair 0.1.14 current attribution must fail provenance validation")
        self.assertTrue(any("stale current-implementation attribution" in error for error in errors))

    def test_historical_upload_evidence_and_current_runtime_qualification_stay_distinct(self) -> None:
        for text in (self.implementation_map, self.current, self.authority):
            self.assertIn("Owner runtime of theme `0.1.14`", text)
            self.assertIn("historical evidence", text)
            self.assertIn("glyphs rendered", text)
            self.assertIn("visually detached", text)
            self.assertIn("0.1.15", text)
            self.assertIn("0.1.16", text)
            self.assertIn(".gpfup--has-files", text)
        self.assertIn("OWNER_RUNTIME_REQUIRED", self.implementation_map)
        self.assertIn("OWNER_RUNTIME_REQUIRED", self.current)
        self.assertIn("NOT_PROVEN", self.authority)
        self.assertIn("post-upload/crop", self.implementation_map)
        self.assertIn("post-upload/crop", self.current)
        self.assertIn("post-upload/crop", self.authority)

    def test_implementation_docs_track_mobile_polish_and_unresolved_host_width(self) -> None:
        self.assertIn("Production breakpoint | `960 CSS px`", self.implementation_map)
        self.assertIn("HOST_OWNED / OWNER_CONFIGURABLE", self.implementation_map)
        self.assertIn("All Radio choices", self.implementation_map)
        self.assertIn("gpfup--images-only", self.implementation_map)
        self.assertIn("student-photo-upload.svg", self.implementation_map)
        self.assertIn("Diagnostic package v0.3.6", self.implementation_map)
        self.assertIn("devicePixelRatio", self.implementation_map)
        self.assertIn("HOST_INTEGRATION_REQUIRED", self.implementation_map)
        self.assertIn("OWNER_RUNTIME_REQUIRED", self.implementation_map)
        self.assertIn(CURRENT_THEME_VERSION, self.src_readme)
        self.assertIn(CURRENT_DIAGNOSTIC_VERSION, self.src_readme)
        self.assertIn("student-photo-upload.svg", self.src_readme)
        self.assertIn("960px", self.src_readme)
        self.assertIn("above-input", self.src_readme)
        self.assertIn("--gf-ctrl-select-padding-x", self.implementation_map)

    def test_current_authorized_visual_destination_is_present_without_broad_page_takeover(self) -> None:
        self.assertIn("@media (min-width: 960px)", self.css)
        self.assertEqual(1, self.css.count("@media (min-width: 960px)"))
        self.assertNotRegex(self.css, r"@media[^\{]*(?:320|360|390|393|412|430)px")
        self.assertIn("--gf-form-gap-y: 24px", self.css)
        self.assertIn("--gf-ctrl-line-height: 1.5", self.css)
        self.assertIn("--gf-ctrl-select-padding-x: 24px 32px", self.css)
        self.assertIn("--gf-ctrl-label-line-height-primary: 1.5", self.css)
        self.assertIn("--gf-ctrl-btn-line-height: 1.5", self.css)
        self.assertIn("max-inline-size: 904px", self.css)
        self.assertIn("padding-inline: 32px", self.css)
        self.assertIn("box-shadow: none", self.css)
        self.assertIn(".gfield.gfield--type-radio", self.css)
        self.assertIn("flex: 1 1 9.5rem", self.css)
        self.assertNotIn(".gfield.srwf-role-binary-choice .gfield_radio", self.css)
        self.assertIn("background: #EDF1FC", self.css)
        self.assertIn('background-image: url("icons/student-photo-upload.svg")', self.css)
        self.assertNotIn("#F6F8FB", self.css, "page background must remain host-integration-owned until a safe seam is proven")
        self.assertNotRegex(self.css, r"(?m)^\s*(?:html|body)\s*\{")
        self.assertNotIn("!important", self.css)


if __name__ == "__main__":
    unittest.main()
