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
CURRENT_DIAGNOSTIC_VERSION = "0.3.6"
VERSION_PATTERN = r"[0-9]+\.[0-9]+\.[0-9]+"

IMPLEMENTATION_VERSION_PATTERNS = {
    "implementation_map": re.compile(r"Current static theme implementation: `([^`]+)`\."),
    "src_readme": re.compile(r"Current production package line: \*\*([^*]+)\*\*\."),
}

AUTHORITY_CURRENT_PACKAGE_PATTERNS = (
    re.compile(
        rf"\btheme\s+`?{VERSION_PATTERN}`?\s+(?:is|remains)\s+the\s+current\s+(?:static\s+)?implementation\b",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b(?:current|final)\s+Owner[- ]runtime\s+qualification\b.*\btheme\s+`?{VERSION_PATTERN}`?",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\bAuthentic\s+Owner\s+runtime\s+evidence\b.*\brequired\b.*\btheme\s+`?{VERSION_PATTERN}`?",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\bdiagnostic\s+package\s+`?{VERSION_PATTERN}`?\s+(?:is|remains)\s+the\s+current\b",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\bcurrent\s+(?:theme|production\s+package|implementation\s+package)\b.*`?{VERSION_PATTERN}`?",
        re.IGNORECASE,
    ),
)


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()


def theme_version(source: str) -> str:
    match = re.search(r"const SRWF_REGISTRATION_THEME_VERSION = '([^']+)';", source)
    if not match:
        raise AssertionError("SRWF theme version constant not found")
    return match.group(1)


def next_patch_version(version: str) -> str:
    major, minor, patch = (int(part) for part in version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def implementation_status_errors(theme_source: str, surfaces: dict[str, str]) -> list[str]:
    current_version = theme_version(theme_source)
    errors: list[str] = []
    for name, pattern in IMPLEMENTATION_VERSION_PATTERNS.items():
        matches = pattern.findall(surfaces[name])
        if len(matches) != 1:
            errors.append(f"{name}: expected exactly one current implementation/package marker, found {matches}")
            continue
        if matches[0] != current_version:
            errors.append(
                f"{name}: current implementation/package marker {matches[0]} does not match theme source {current_version}"
            )
    return errors


def authority_current_package_claims(surface_name: str, text: str) -> list[str]:
    errors: list[str] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = " ".join(raw_line.split())
        if not line:
            continue
        if re.match(r"^(?:[-*]\s*)?Historical evidence:", line, re.IGNORECASE):
            continue
        for pattern in AUTHORITY_CURRENT_PACKAGE_PATTERNS:
            if pattern.search(line):
                errors.append(f"{surface_name}:{line_number}: mutable current-package claim: {line}")
                break
    return errors


def authority_boundary_errors(surfaces: dict[str, str]) -> list[str]:
    errors: list[str] = []
    errors.extend(authority_current_package_claims("current", surfaces["current"]))
    errors.extend(authority_current_package_claims("authority", surfaces["authority"]))
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
        cls.surfaces = {
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
            "desktop internal block padding: `32px`",
            "visible surface boundary: the visual equivalent of `1px #E4E7EC`",
            "restrained depth: `0 1px 2px rgba(16,24,40,0.04), 0 12px 32px rgba(16,24,40,0.06)`",
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

    def test_current_implementation_version_is_derived_and_synchronized_only_on_implementation_surfaces(self) -> None:
        self.assertEqual([], implementation_status_errors(self.theme_php, self.surfaces))
        self.assertIn(f"Version: {CURRENT_DIAGNOSTIC_VERSION}", self.diagnostic_php)
        self.assertIn(f"const GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '{CURRENT_DIAGNOSTIC_VERSION}';", self.diagnostic_php)
        self.assertIn(f"var VERSION = '{CURRENT_DIAGNOSTIC_VERSION}';", self.visual_diagnostic)

    def test_future_theme_version_drift_is_rejected_without_a_second_version_registry(self) -> None:
        hypothetical_version = next_patch_version(self.current_version)
        mutated_theme_source = self.theme_php.replace(
            f"Version: {self.current_version}", f"Version: {hypothetical_version}"
        ).replace(
            f"SRWF_REGISTRATION_THEME_VERSION = '{self.current_version}'",
            f"SRWF_REGISTRATION_THEME_VERSION = '{hypothetical_version}'",
        )
        self.assertEqual(hypothetical_version, theme_version(mutated_theme_source))
        errors = implementation_status_errors(mutated_theme_source, self.surfaces)
        self.assertTrue(any(error.startswith("implementation_map:") for error in errors))
        self.assertTrue(any(error.startswith("src_readme:") for error in errors))

    def test_authority_surfaces_do_not_own_mutable_current_package_identity(self) -> None:
        self.assertEqual([], authority_boundary_errors(self.surfaces))
        self.assertIn("does **not** own mutable current theme/package identity", self.current)
        self.assertIn("Current implementation/package identity is intentionally not registered", self.authority)
        for text in (self.current, self.authority):
            self.assertIn("IMPLEMENTATION_MAP.md", text)
            self.assertIn("src/README.md", text)
        self.assertNotIn("MOBILE_RESPONSIVE_POLISH_STATICALLY_IMPLEMENTED", self.current.splitlines()[1])
        self.assertNotIn("MOBILE_RESPONSIVE_POLISH_STATICALLY_IMPLEMENTED", self.authority)

    def test_original_stale_current_implementation_claim_is_rejected(self) -> None:
        for surface_name in ("current", "authority"):
            mutated = dict(self.surfaces)
            mutated[surface_name] = "Theme `0.1.16` is the current static implementation.\n" + mutated[surface_name]
            errors = authority_boundary_errors(mutated)
            self.assertTrue(any(error.startswith(f"{surface_name}:") for error in errors))

    def test_version_specific_current_runtime_target_is_rejected(self) -> None:
        injected = (
            "Final Owner runtime qualification remains open for theme `9.9.9` + diagnostic `0.3.6`.\n"
        )
        for surface_name in ("current", "authority"):
            mutated = dict(self.surfaces)
            mutated[surface_name] = injected + mutated[surface_name]
            errors = authority_boundary_errors(mutated)
            self.assertTrue(any(error.startswith(f"{surface_name}:") for error in errors))

    def test_explicit_historical_evidence_may_retain_versioned_batch_history(self) -> None:
        historical_line = (
            "Historical evidence: Theme `0.1.16` was the mobile responsive-polish implementation for that batch."
        )
        self.assertEqual([], authority_current_package_claims("fixture", historical_line))
        for text in (self.current, self.authority):
            self.assertIn("Historical evidence:", text)
            self.assertIn("0.1.14", text)
            self.assertIn("0.1.15", text)
            self.assertIn("0.1.16", text)

    def test_historical_upload_evidence_and_current_runtime_qualification_stay_distinct(self) -> None:
        for text in (self.implementation_map, self.current, self.authority):
            self.assertIn("Owner runtime of theme `0.1.14`", text)
            self.assertIn("historical evidence", text.lower())
            self.assertIn("glyphs rendered", text)
            self.assertIn("visually detached", text)
            self.assertIn("0.1.15", text)
            self.assertIn("0.1.16", text)
            self.assertIn(".gpfup--has-files", text)
        self.assertIn("OWNER_RUNTIME_REQUIRED", self.implementation_map)
        self.assertIn("OWNER_RUNTIME_REQUIRED", self.current)
        self.assertIn("NOT_PROVEN", self.authority)
        self.assertIn("post-upload/crop", self.implementation_map.lower())
        self.assertIn("post-upload/crop", self.current.lower())
        self.assertIn("post-upload/crop", self.authority.lower())

    def test_implementation_docs_track_host_prerequisite_and_radio_fill_repair(self) -> None:
        self.assertIn("Production breakpoint | `960 CSS px`", self.implementation_map)
        self.assertIn("HOST_OWNED / OWNER_CONFIGURABLE", self.implementation_map)
        self.assertIn("All Radio choices", self.implementation_map)
        self.assertIn("gpfup--images-only", self.implementation_map)
        self.assertIn("student-photo-upload.svg", self.implementation_map)
        self.assertIn("Diagnostic package v0.3.6", self.implementation_map)
        self.assertIn("devicePixelRatio", self.implementation_map)
        self.assertIn("full-width content area", self.implementation_map)
        self.assertIn("GeneratePress", self.implementation_map)
        self.assertIn("--gf-label-space-x-secondary", self.implementation_map)
        self.assertIn("OWNER_RUNTIME_REQUIRED", self.implementation_map)
        self.assertIn(self.current_version, self.src_readme)
        self.assertIn(CURRENT_DIAGNOSTIC_VERSION, self.src_readme)
        self.assertIn("student-photo-upload.svg", self.src_readme)
        self.assertIn("960px", self.src_readme)
        self.assertIn("above-input", self.src_readme)
        self.assertIn("full-width content area", self.src_readme)
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
        self.assertIn("padding-block: 32px", self.css)
        self.assertIn("padding-inline: 32px", self.css)
        self.assertIn("0 0 0 1px #E4E7EC", self.css)
        self.assertIn("0 1px 2px rgba(16, 24, 40, 0.04)", self.css)
        self.assertIn("0 12px 32px rgba(16, 24, 40, 0.06)", self.css)
        self.assertIn(".gfield.gfield--type-radio", self.css)
        self.assertIn("--gf-label-space-x-secondary: 0", self.css)
        self.assertIn("flex: 1 1 9.5rem", self.css)
        self.assertNotIn(".gfield.srwf-role-binary-choice .gfield_radio", self.css)
        self.assertIn("background: #EDF1FC", self.css)
        self.assertIn('background-image: url("icons/student-photo-upload.svg")', self.css)
        self.assertNotIn("#F6F8FB", self.css, "page background remains host-owned")
        self.assertNotRegex(self.css, r"(?m)^\s*(?:html|body)\s*\{")
        self.assertNotIn(".site-content", self.css)
        self.assertNotIn(".content-area", self.css)
        self.assertNotIn(".site-main", self.css)
        self.assertNotIn(".inside-article", self.css)
        self.assertNotIn(".entry-content", self.css)
        self.assertNotIn(".page-id-", self.css)
        self.assertNotRegex(self.css, r"#gform_wrapper_\d+")
        self.assertNotIn(":nth-child", self.css)
        self.assertNotIn(":nth-of-type", self.css)
        self.assertNotIn("GeneratePress", self.css)
        self.assertNotIn("100vw", self.css)
        self.assertNotIn("overflow: hidden", self.css)
        self.assertNotIn("!important", self.css)


if __name__ == "__main__":
    unittest.main()
