from __future__ import annotations

import re
import unittest
from datetime import date
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
REFERENCE = THEME / "reference"
CURRENT = (REFERENCE / "SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md").read_text(encoding="utf-8")
DESKTOP_SHELL = (REFERENCE / "SRWF_DESKTOP_SHELL_OWNER_DECISION_2026-09-20.md").read_text(encoding="utf-8")
AUTHORITY = (REFERENCE / "VISUAL_AUTHORITY.md").read_text(encoding="utf-8")
IMPLEMENTATION_MAP = (THEME / "IMPLEMENTATION_MAP.md").read_text(encoding="utf-8")

BASE_HANDLE = "OWNER:SRWF-2026-09-19"
DESKTOP_SHELL_HANDLE = "OWNER:SRWF-2026-09-20-DESKTOP-SHELL"

AUTHORITY_HANDLE_RE = re.compile(
    r"authority_handle:\s*`?(OWNER:SRWF-(\d{4}-\d{2}-\d{2})[A-Z0-9:._-]*)`?",
    re.IGNORECASE,
)
CURRENT_HANDLE_RE = re.compile(r"^Authority handle:\s*`([^`]+)`", re.MULTILINE)
DATED_OWNER_HANDLE_RE = re.compile(r"OWNER:SRWF-\d{4}-\d{2}-\d{2}[A-Z0-9:._-]*", re.IGNORECASE)
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")


def registered_owner_authorities(authority_text: str) -> dict[str, date]:
    return {
        match.group(1): date.fromisoformat(match.group(2))
        for match in AUTHORITY_HANDLE_RE.finditer(authority_text)
    }


def unregistered_later_owner_supersessions(reconciliation_text: str, authority_text: str) -> list[str]:
    registered = registered_owner_authorities(authority_text)
    current_match = CURRENT_HANDLE_RE.search(reconciliation_text)
    if current_match is None:
        return ["current reconciliation has no Authority handle"]

    current_handle = current_match.group(1)
    current_date = registered.get(current_handle)
    if current_date is None:
        return [f"current authority handle is not registered/admitted: {current_handle}"]

    errors: list[str] = []
    for line_number, raw_line in enumerate(reconciliation_text.splitlines(), start=1):
        line = " ".join(raw_line.split())
        lower = line.lower()
        if "owner" not in lower or "direct" not in lower:
            continue
        if "decision" not in lower and "supersed" not in lower:
            continue

        later_dates = [date.fromisoformat(value) for value in DATE_RE.findall(line) if date.fromisoformat(value) > current_date]
        if not later_dates:
            continue

        handles = DATED_OWNER_HANDLE_RE.findall(line)
        for claim_date in later_dates:
            if not handles:
                errors.append(
                    f"line {line_number}: later direct Owner supersession {claim_date.isoformat()} has no explicit admitted authority handle"
                )
                continue
            if not any(handle in registered and registered[handle] >= claim_date for handle in handles):
                errors.append(
                    f"line {line_number}: later direct Owner supersession {claim_date.isoformat()} references no registered authority handle"
                )
    return errors


class OwnerAuthorityProvenanceGateTests(unittest.TestCase):
    def test_existing_registered_owner_authority_remains_valid(self) -> None:
        registered = registered_owner_authorities(AUTHORITY)
        self.assertIn(BASE_HANDLE, registered)
        self.assertEqual(date(2026, 9, 19), registered[BASE_HANDLE])
        self.assertIn(
            "path: themes/srwf-registration/reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md",
            AUTHORITY,
        )

    def test_desktop_shell_owner_authority_is_separately_registered_and_valid(self) -> None:
        registered = registered_owner_authorities(AUTHORITY)
        self.assertIn(DESKTOP_SHELL_HANDLE, registered)
        self.assertEqual(date(2026, 9, 20), registered[DESKTOP_SHELL_HANDLE])
        self.assertIn(f"Authority handle: `{DESKTOP_SHELL_HANDLE}`", DESKTOP_SHELL)
        self.assertIn("CURRENT_OWNER_SCOPE_AUTHORITY", DESKTOP_SHELL)
        self.assertIn("DESKTOP_SHELL_APPROVED", DESKTOP_SHELL)
        self.assertIn("RUNTIME_QUALIFICATION_REQUIRED", DESKTOP_SHELL)
        self.assertIn("direct Owner decision", DESKTOP_SHELL)
        self.assertIn(
            "path: themes/srwf-registration/reference/SRWF_DESKTOP_SHELL_OWNER_DECISION_2026-09-20.md",
            AUTHORITY,
        )

    def test_registered_later_shell_supersession_passes_only_with_registered_handle(self) -> None:
        self.assertIn(
            f"Direct Owner decision 2026-09-20 under the separately registered authority handle `{DESKTOP_SHELL_HANDLE}`",
            CURRENT,
        )
        self.assertEqual([], unregistered_later_owner_supersessions(CURRENT, AUTHORITY))

        authority_without_registration = AUTHORITY.replace(
            f"authority_handle: {DESKTOP_SHELL_HANDLE}",
            "authority_handle: OWNER:SRWF-UNREGISTERED-DESKTOP-SHELL",
        )
        errors = unregistered_later_owner_supersessions(CURRENT, authority_without_registration)
        self.assertTrue(errors)
        self.assertTrue(any("2026-09-20" in error and "references no registered authority handle" in error for error in errors))

    def test_unknown_later_owner_handle_still_fails(self) -> None:
        injected = CURRENT + (
            "\nDirect Owner decision 2026-09-21 under OWNER:SRWF-2026-09-21-UNKNOWN "
            "supersedes the current desktop shell.\n"
        )
        errors = unregistered_later_owner_supersessions(injected, AUTHORITY)
        self.assertTrue(errors)
        self.assertTrue(any("2026-09-21" in error and "references no registered authority handle" in error for error in errors))

    def test_unhandled_later_direct_owner_prose_still_fails(self) -> None:
        injected = CURRENT + (
            "\nThe Owner's direct 2026-09-21 shell decision supersedes the current desktop shell.\n"
        )
        errors = unregistered_later_owner_supersessions(injected, AUTHORITY)
        self.assertTrue(errors)
        self.assertTrue(any("2026-09-21" in error and "no explicit admitted authority handle" in error for error in errors))

    def test_fabricated_implementation_prose_cannot_create_owner_authority(self) -> None:
        fabricated_handle = "OWNER:SRWF-2026-09-21-FABRICATED"
        fabricated_implementation_prose = IMPLEMENTATION_MAP + (
            f"\nauthority_handle: {fabricated_handle}\n"
            "Direct Owner decision 2026-09-21 supersedes the shell.\n"
        )
        self.assertIn(fabricated_handle, fabricated_implementation_prose)
        self.assertNotIn(fabricated_handle, registered_owner_authorities(AUTHORITY))

        injected = CURRENT + (
            f"\nDirect Owner decision 2026-09-21 under {fabricated_handle} supersedes the desktop shell.\n"
        )
        errors = unregistered_later_owner_supersessions(injected, AUTHORITY)
        self.assertTrue(errors)
        self.assertTrue(any("references no registered authority handle" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
