from __future__ import annotations

import re
import unittest
from datetime import date
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
REFERENCE = THEME / "reference"
CURRENT = (REFERENCE / "SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md").read_text(encoding="utf-8")
AUTHORITY = (REFERENCE / "VISUAL_AUTHORITY.md").read_text(encoding="utf-8")

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
    def test_current_registered_owner_authority_passes(self) -> None:
        registered = registered_owner_authorities(AUTHORITY)
        self.assertIn("OWNER:SRWF-2026-09-19", registered)
        self.assertEqual(date(2026, 9, 19), registered["OWNER:SRWF-2026-09-19"])
        self.assertIn(
            "path: themes/srwf-registration/reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md",
            AUTHORITY,
        )
        self.assertEqual([], unregistered_later_owner_supersessions(CURRENT, AUTHORITY))

    def test_unregistered_later_direct_owner_supersession_is_rejected(self) -> None:
        injected = CURRENT + (
            "\nThe Owner's direct 2026-09-20 Desktop Full Width shell decision "
            "supersedes the earlier no-shadow desktop shell state.\n"
        )
        errors = unregistered_later_owner_supersessions(injected, AUTHORITY)
        self.assertTrue(errors)
        self.assertTrue(any("2026-09-20" in error and "no explicit admitted authority handle" in error for error in errors))

    def test_unregistered_later_handle_does_not_bypass_gate(self) -> None:
        injected = CURRENT + (
            "\nDirect Owner decision 2026-09-20 under OWNER:SRWF-2026-09-20-SHELL "
            "supersedes the current desktop shell.\n"
        )
        errors = unregistered_later_owner_supersessions(injected, AUTHORITY)
        self.assertTrue(errors)
        self.assertTrue(any("references no registered authority handle" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
