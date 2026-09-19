from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS = THEME / "src" / "srwf-registration.css"

REPORT = ".gfield.srwf-role-report-card-upload .gpfup:not(.gpfup--has-files) .gpfup__droparea"
PHOTO = ".gfield--type-fileupload .gpfup.gpfup--images-only:not(.gpfup--has-files) .gpfup__droparea"


def blocks(css: str) -> list[tuple[str, str]]:
    clean = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [
        (match.group(1).strip(), match.group(2))
        for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean, flags=re.S)
    ]


class SrwfGpfupInitialContentClusterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.css = CSS.read_text(encoding="utf-8")
        self.blocks = blocks(self.css)

    def test_owner_runtime_alignment_defect_is_repaired_at_the_authentic_content_cluster(self) -> None:
        alignment_selector, alignment = next(
            (selector, body)
            for selector, body in self.blocks
            if REPORT in selector and PHOTO in selector and "> div" not in selector and "::before" not in selector
        )
        self.assertIn(".srwf-registration-theme_wrapper", alignment_selector)
        self.assertIn("justify-content: center;", alignment)

        cluster_selector, cluster = next(
            (selector, body)
            for selector, body in self.blocks
            if REPORT + " > div" in selector and PHOTO + " > div" in selector
        )
        self.assertIn(".srwf-registration-theme_wrapper", cluster_selector)
        self.assertIn("flex: 0 1 auto;", cluster)
        self.assertIn("inline-size: auto;", cluster)
        self.assertIn("min-inline-size: 0;", cluster)
        self.assertIn("max-inline-size: calc(100% - 52px);", cluster)

    def test_alignment_is_limited_to_the_two_admitted_initial_variants(self) -> None:
        cluster_selectors = [selector for selector, _ in self.blocks if ".gpfup__droparea > div" in selector]
        self.assertEqual(1, len(cluster_selectors))
        selector = cluster_selectors[0]
        self.assertIn("srwf-role-report-card-upload", selector)
        self.assertIn("gpfup--images-only", selector)
        self.assertEqual(2, selector.count(":not(.gpfup--has-files)"))
        self.assertNotRegex(selector, r"#(?:field|input|gform)_\d+")
        self.assertNotIn(":nth-child", selector)
        self.assertNotIn(":nth-of-type", selector)

    def test_outer_shell_and_icon_geometry_remain_unchanged(self) -> None:
        shell = next(
            body
            for selector, body in self.blocks
            if selector.endswith(".gfield--type-fileupload .gpfup:not(.gpfup--has-files) .gpfup__droparea")
        )
        for declaration in (
            "min-block-size: 96px;",
            "padding: 16px;",
            "border: 1px dashed #8690A1;",
            "border-radius: 12px;",
            "column-gap: 12px;",
            "flex-wrap: wrap;",
        ):
            self.assertIn(declaration, shell)

        icon = next(
            body
            for selector, body in self.blocks
            if REPORT + "::before" in selector and PHOTO + "::before" in selector
        )
        self.assertIn("flex: 0 0 40px;", icon)
        self.assertIn("inline-size: 40px;", icon)
        self.assertIn("block-size: 40px;", icon)
        self.assertIn("background-size: 24px 24px;", icon)

    def test_repair_adds_no_upload_behavior_or_post_upload_composition(self) -> None:
        production_js = list((THEME / "src").glob("**/*.js"))
        self.assertEqual([], production_js)
        selectors = "\n".join(selector for selector, _ in self.blocks).lower()
        self.assertNotIn(".gpfup__files", selectors)
        self.assertNotIn(".gpfup__delete", selectors)
        self.assertNotIn("crop", selectors)
        self.assertNotIn("preview", selectors)
        self.assertNotIn("!important", self.css)


if __name__ == "__main__":
    unittest.main()
