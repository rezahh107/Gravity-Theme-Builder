from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS_PATH = THEME / "src" / "srwf-registration.css"
PHP_PATH = THEME / "src" / "srwf-registration-theme.php"
SRC = THEME / "src"
CSS = CSS_PATH.read_text(encoding="utf-8")
PHP = PHP_PATH.read_text(encoding="utf-8")

SCOPE = ".gform-theme--framework.srwf-registration-theme_wrapper"
CONTROL_SELECTOR = f"{SCOPE} .ts-wrapper .ts-control"
FOCUS_SELECTOR = f"{SCOPE} .ts-wrapper.focus .ts-control"
RADIO_SELECTOR = f"{SCOPE} .gfield.gfield--type-radio .gchoice"
UPLOAD_SELECTOR = f"{SCOPE} .gfield--type-fileupload .gpfup:not(.gpfup--has-files) .gpfup__droparea"


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def rule_body(selector: str) -> str:
    clean = strip_comments(CSS)
    match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", clean, flags=re.S)
    if not match:
        raise AssertionError(f"missing CSS rule: {selector}")
    return match.group(1)


def selectors() -> list[str]:
    clean = strip_comments(CSS)
    result: list[str] = []
    for match in re.finditer(r"([^{}]+)\{[^{}]*\}", clean, flags=re.S):
        group = match.group(1).strip()
        if group.startswith("@media"):
            continue
        result.extend(part.strip() for part in group.split(",") if part.strip())
    return result


class OpenableControlMetricTests(unittest.TestCase):
    def test_standard_text_input_metric_baseline_remains_canonical(self) -> None:
        """Lock the accepted family that the authentic Owner runtime measured on text inputs."""
        for declaration in (
            "--gf-ctrl-size: 52px;",
            "--gf-ctrl-font-size: 16px;",
            "--gf-ctrl-font-weight: 400;",
            "--gf-ctrl-line-height: 1.5;",
            "--gf-ctrl-border-color: #8690A1;",
            "--gf-ctrl-border-color-focus: #1D4ED8;",
            "--gf-ctrl-radius: 10px;",
            "--gf-ctrl-outline-color-focus: #1D4ED8;",
            "--gf-ctrl-outline-width-focus: 2px;",
            "--gf-ctrl-outline-offset: 2px;",
            "--gf-ctrl-outline-style: solid;",
        ):
            self.assertIn(declaration, CSS)

    def test_gpas_visible_control_converges_on_text_input_metrics(self) -> None:
        body = rule_body(CONTROL_SELECTOR)
        self.assertRegex(body, r"\bbox-sizing\s*:\s*border-box\s*;")
        self.assertRegex(body, r"\bmin-block-size\s*:\s*var\(--gf-ctrl-size\)\s*;")
        self.assertRegex(body, r"\bpadding-block\s*:\s*0\s*;")
        self.assertRegex(body, r"\bpadding-inline\s*:\s*12px 32px\s*;")
        self.assertRegex(body, r"\bline-height\s*:\s*var\(--gf-ctrl-line-height\)\s*;")
        self.assertNotRegex(body, r"\b(?:block-size|height)\s*:\s*52px")
        self.assertNotIn("width:", body)

    def test_indicator_remains_host_owned_with_only_logical_space_reserved(self) -> None:
        body = rule_body(CONTROL_SELECTOR)
        self.assertIn("padding-inline: 12px 32px;", body)
        for property_name in (
            "background-image",
            "background-position",
            "background-size",
            "content:",
            "transform:",
            "top:",
            "left:",
            "right:",
        ):
            self.assertNotIn(property_name, body)

    def test_focus_projects_existing_srwf_visual_without_taking_focus_behavior(self) -> None:
        body = rule_body(FOCUS_SELECTOR)
        self.assertRegex(body, r"border-color\s*:\s*var\(--gf-ctrl-border-color-focus\)\s*;")
        self.assertRegex(
            body,
            r"outline\s*:\s*var\(--gf-ctrl-outline-width-focus\) var\(--gf-ctrl-outline-style\) var\(--gf-ctrl-outline-color-focus\)\s*;",
        )
        self.assertRegex(body, r"outline-offset\s*:\s*var\(--gf-ctrl-outline-offset\)\s*;")
        self.assertRegex(body, r"box-shadow\s*:\s*none\s*;")
        self.assertNotIn(":focus", FOCUS_SELECTOR)
        self.assertIn(".ts-wrapper.focus", FOCUS_SELECTOR)

    def test_openable_rules_are_srwf_scoped_and_not_school_specific(self) -> None:
        openable = [selector for selector in selectors() if ".ts-wrapper" in selector or ".ts-control" in selector]
        self.assertEqual([CONTROL_SELECTOR, FOCUS_SELECTOR], openable)
        for selector in openable:
            self.assertTrue(selector.startswith(SCOPE))
        openable_source = "\n".join(openable + [rule_body(CONTROL_SELECTOR), rule_body(FOCUS_SELECTOR)])
        self.assertNotRegex(openable_source, r"(?i)school|مدرس")
        self.assertNotRegex(CSS, r"#(?:field|input|choice|label|gform_wrapper|gform)_\d+")
        self.assertNotIn(":nth-child", CSS)
        self.assertNotIn(":nth-of-type", CSS)

    def test_native_select_and_tom_select_behavior_are_not_reimplemented(self) -> None:
        clean = strip_comments(CSS)
        self.assertNotRegex(clean, re.escape(SCOPE) + r"[^\{]*(?:select\.gfield_select|\.ts-dropdown|\.option|\.active)\s*\{")
        self.assertEqual([], list(SRC.glob("**/*.js")))
        for behavior_marker in ("TomSelect(", "addEventListener(", "querySelector(", "dropdown-active"):
            self.assertNotIn(behavior_marker, PHP)

    def test_out_of_scope_radio_upload_submit_shell_and_background_contracts_stay_intact(self) -> None:
        radio = rule_body(RADIO_SELECTOR)
        self.assertRegex(radio, r"display\s*:\s*block\s*;")
        self.assertRegex(radio, r"flex\s*:\s*1 1 8rem\s*;")

        upload = rule_body(UPLOAD_SELECTOR)
        self.assertRegex(upload, r"min-block-size\s*:\s*96px\s*;")
        self.assertRegex(upload, r"padding\s*:\s*16px\s*;")
        self.assertRegex(upload, r"border\s*:\s*1px dashed #8690A1\s*;")

        self.assertRegex(CSS, r"(?s)\.gform-footer \.gform_button.*?inline-size:\s*100%;")
        self.assertRegex(CSS, r"(?s)@media \(min-width: 960px\).*?max-inline-size:\s*904px;")
        self.assertRegex(CSS, r"(?s)@media \(min-width: 960px\).*?padding-inline:\s*32px;")
        self.assertNotIn("#F6F8FB", CSS)

    def test_repair_uses_no_priority_escape_or_global_openable_selector(self) -> None:
        self.assertNotIn("!important", CSS)
        self.assertNotRegex(CSS, r"(?m)^\s*\.ts-(?:wrapper|control)\b")
        self.assertNotRegex(CSS, r"(?m)^\s*select\b")


if __name__ == "__main__":
    unittest.main()
