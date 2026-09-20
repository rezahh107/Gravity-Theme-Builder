from __future__ import annotations

import re
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
CSS_PATH = THEME / "src" / "srwf-registration.css"
PHP_PATH = THEME / "src" / "srwf-registration-theme.php"
DIAGNOSTIC_PATH = THEME / "diagnostic" / "assets" / "runtime-diagnostic.js"
SRC = THEME / "src"
CSS = CSS_PATH.read_text(encoding="utf-8")
PHP = PHP_PATH.read_text(encoding="utf-8")
DIAGNOSTIC = DIAGNOSTIC_PATH.read_text(encoding="utf-8")

SCOPE = ".gform-theme--framework.srwf-registration-theme_wrapper"
NATIVE_SELECT_SELECTOR = (
    f"{SCOPE} .gfield--type-select "
    "select.gfield_select:not([multiple]):not(.tomselected):not(.ts-hidden-accessible)"
)
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
    def test_standard_text_input_and_select_family_baseline_is_explicit(self) -> None:
        for declaration in (
            "--gf-ctrl-size: 52px;",
            "--gf-ctrl-font-size: 16px;",
            "--gf-ctrl-font-weight: 400;",
            "--gf-ctrl-line-height: 1.5;",
            "--gf-ctrl-border-color: #8690A1;",
            "--gf-ctrl-border-color-focus: #1D4ED8;",
            "--gf-ctrl-radius: 10px;",
            "--gf-ctrl-select-padding-x: 24px 32px;",
            "--gf-ctrl-outline-color-focus: #1D4ED8;",
            "--gf-ctrl-outline-width-focus: 2px;",
            "--gf-ctrl-outline-offset: 2px;",
            "--gf-ctrl-outline-style: solid;",
        ):
            self.assertIn(declaration, CSS)

    def test_native_single_select_gets_only_runtime_proven_vertical_optical_compensation(self) -> None:
        body = rule_body(NATIVE_SELECT_SELECTOR)
        self.assertRegex(body, r"\bpadding-block-start\s*:\s*14px\s*;")
        self.assertNotRegex(body, r"padding-(?:top|right|bottom|left)\s*:")
        self.assertNotIn("padding-inline", body)
        self.assertNotIn("block-size", body)
        self.assertNotIn("height", body)

    def test_native_select_identity_excludes_enhanced_sources_and_incidental_layout_state(self) -> None:
        self.assertIn(":not([multiple])", NATIVE_SELECT_SELECTOR)
        self.assertIn(":not(.tomselected)", NATIVE_SELECT_SELECTOR)
        self.assertIn(":not(.ts-hidden-accessible)", NATIVE_SELECT_SELECTOR)
        openable_source = "\n".join(
            selector for selector in selectors() if "select.gfield_select" in selector or ".ts-wrapper" in selector
        )
        for forbidden in (
            "form_sublabel_above",
            "gfield--no-description",
            ":nth-child",
            ":nth-of-type",
        ):
            self.assertNotIn(forbidden, openable_source)
        self.assertNotRegex(openable_source, r"#(?:field|input|choice|label|gform_wrapper|gform)_\d+")
        self.assertNotRegex(openable_source, r"(?i)school|مدرس")

    def test_gpas_visible_control_reuses_the_same_select_family_inline_contract(self) -> None:
        body = rule_body(CONTROL_SELECTOR)
        self.assertRegex(body, r"\bbox-sizing\s*:\s*border-box\s*;")
        self.assertRegex(body, r"\bmin-block-size\s*:\s*var\(--gf-ctrl-size\)\s*;")
        self.assertRegex(body, r"\bpadding-block\s*:\s*0\s*;")
        self.assertRegex(body, r"\bpadding-inline\s*:\s*var\(--gf-ctrl-select-padding-x\)\s*;")
        self.assertRegex(body, r"\bline-height\s*:\s*var\(--gf-ctrl-line-height\)\s*;")
        self.assertNotRegex(body, r"\b(?:block-size|height)\s*:\s*52px")
        self.assertNotIn("width:", body)

    def test_indicator_remains_host_owned_with_only_the_documented_inline_reserve(self) -> None:
        body = rule_body(CONTROL_SELECTOR)
        self.assertIn("padding-inline: var(--gf-ctrl-select-padding-x);", body)
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

    def test_openable_repair_is_srwf_scoped_and_behavior_neutral(self) -> None:
        openable = [
            selector
            for selector in selectors()
            if "select.gfield_select" in selector or ".ts-wrapper" in selector or ".ts-control" in selector
        ]
        self.assertEqual([NATIVE_SELECT_SELECTOR, CONTROL_SELECTOR, FOCUS_SELECTOR], openable)
        for selector in openable:
            self.assertTrue(selector.startswith(SCOPE))
        self.assertEqual([], list(SRC.glob("**/*.js")))
        clean = strip_comments(CSS)
        self.assertNotRegex(clean, r"\.ts-dropdown\s*\{")
        self.assertNotRegex(clean, r"\.ts-wrapper[^\{]*\.(?:dropdown-active|active|has-items)\b[^\{]*\{")
        for behavior_marker in ("TomSelect(", "addEventListener(", "querySelector(", "dropdown-active"):
            self.assertNotIn(behavior_marker, PHP)

    def test_diagnostic_still_distinguishes_tom_select_source_from_visible_control(self) -> None:
        self.assertIn("select.tomselected, select.ts-hidden-accessible", DIAGNOSTIC)
        self.assertIn("boundedQuery(wrapper, '.ts-control', 2)", DIAGNOSTIC)
        self.assertIn("tomSelectEvidence", DIAGNOSTIC)

    def test_unrelated_contracts_include_current_mobile_polish_without_openable_scope_leakage(self) -> None:
        radio = rule_body(RADIO_SELECTOR)
        self.assertRegex(radio, r"display\s*:\s*flex\s*;")
        self.assertRegex(radio, r"flex\s*:\s*1 1 9\.5rem\s*;")
        self.assertRegex(radio, r"min-inline-size\s*:\s*0\s*;")

        upload = rule_body(UPLOAD_SELECTOR)
        self.assertRegex(upload, r"min-block-size\s*:\s*96px\s*;")
        self.assertRegex(upload, r"padding\s*:\s*16px\s*;")
        self.assertRegex(upload, r"border\s*:\s*1px dashed #8690A1\s*;")
        self.assertRegex(upload, r"flex-wrap\s*:\s*wrap\s*;")

        self.assertRegex(CSS, r"(?s)\.gform-footer \.gform_button.*?inline-size:\s*100%;")
        self.assertRegex(CSS, r"(?s)@media \(min-width: 960px\).*?max-inline-size:\s*904px;")
        self.assertRegex(CSS, r"(?s)@media \(min-width: 960px\).*?padding-inline:\s*32px;")
        self.assertNotRegex(CSS, r"@media[^\{]*(?:320|360|390|393|412|430)px")
        self.assertNotIn("#F6F8FB", CSS)

    def test_repair_uses_no_priority_escape_or_global_openable_selector(self) -> None:
        self.assertNotIn("!important", CSS)
        self.assertNotRegex(CSS, r"(?m)^\s*\.ts-(?:wrapper|control)\b")
        self.assertNotRegex(CSS, r"(?m)^\s*select\b")


if __name__ == "__main__":
    unittest.main()
