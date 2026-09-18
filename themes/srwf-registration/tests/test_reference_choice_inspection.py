from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
MATERIALIZER = THEME / "reference" / "materialize_reference.sh"


class TemporaryReferenceChoiceInspection(unittest.TestCase):
    def test_print_choice_reference_fragments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "OWNER_REFERENCE_new_7.html"
            subprocess.run(
                ["bash", str(MATERIALIZER), str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            html = output.read_text(encoding="utf-8")

        print("\n=== APPROVED REFERENCE: LABEL CONTEXTS ===")
        for needle in (
            "جنسیت",
            "وضعیت تحصیلی",
            "وضعیت ثبت",
            "مقطع تحصیلی",
            "مرکز ثبت",
        ):
            print(f"\n--- {needle} ---")
            found = False
            for match in re.finditer(re.escape(needle), html):
                start = max(0, match.start() - 900)
                end = min(len(html), match.end() + 1800)
                print(html[start:end])
                found = True
                break
            if not found:
                print("NOT FOUND")

        print("\n=== APPROVED REFERENCE: CHOICE/RADIO CSS BLOCKS ===")
        css_chunks = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I)
        css = "\n".join(css_chunks)
        for match in re.finditer(r"([^{}]*(?:radio|choice|segmented|gender)[^{}]*)\{([^{}]*)\}", css, flags=re.I):
            selector = match.group(1).strip()
            body = match.group(2).strip()
            if selector and body:
                print(f"{selector} {{{body}}}")

        self.assertIn("جنسیت", html)


if __name__ == "__main__":
    unittest.main()
