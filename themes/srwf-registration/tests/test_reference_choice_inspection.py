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

        print("\n=== APPROVED REFERENCE: CHOICE FAMILY MARKUP ===")
        for marker in ('class="choice-row"', 'class="vertical-choices"'):
            print(f"\n### {marker} ###")
            for index, match in enumerate(re.finditer(re.escape(marker), html), start=1):
                if index > 12:
                    break
                start = max(0, match.start() - 650)
                end = min(len(html), match.end() + 1500)
                snippet = html[start:end]
                print(f"\n--- occurrence {index} ---\n{snippet}")

        print("\n=== APPROVED REFERENCE: CHOICE/RADIO CSS BLOCKS ===")
        css_chunks = re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I)
        css = "\n".join(css_chunks)
        for selector_name in (
            ".choice-row",
            ".choice-btn",
            ".choice-btn.active",
            ".vertical-choices",
            ".vertical-choice",
            ".vertical-choice.active",
            ".vertical-choice .radio-dot",
            ".vertical-choice.active .radio-dot",
            ".vertical-choice.active .radio-dot::after",
        ):
            match = re.search(re.escape(selector_name) + r"\s*\{([^{}]*)\}", css, flags=re.S)
            if match:
                print(f"{selector_name} {{{match.group(1).strip()}}}")
            else:
                print(f"{selector_name} NOT FOUND")

        self.assertIn('class="choice-row"', html)
        self.assertIn('class="vertical-choices"', html)


if __name__ == "__main__":
    unittest.main()
