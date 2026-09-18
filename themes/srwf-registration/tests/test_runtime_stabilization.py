from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / 'themes' / 'srwf-registration'
PHP = THEME / 'src' / 'srwf-registration-theme.php'
CSS = THEME / 'src' / 'srwf-registration.css'
DIAG_PHP = THEME / 'diagnostic' / 'srwf-runtime-diagnostic.php'
DIAG_JS = THEME / 'diagnostic' / 'assets' / 'runtime-diagnostic.js'
WORKFLOW = REPO / '.github' / 'workflows' / 'srwf-registration-static.yml'

NARROW_SCOPE = '.gform-theme--framework.srwf-registration-theme_wrapper'
ENFORCEMENT_SCOPE = 'head:has(#gravity_forms_theme_framework-css) + body .gform-theme--framework.gform-theme.srwf-registration-theme_wrapper'
HOST_SUBMIT_RULE = '.gform-theme.gform-theme--framework.gform_wrapper .button:where(:not(.gform-theme-no-framework):not(.gform-theme__disable):not(.gform-theme__disable *):not(.gform-theme__disable-framework):not(.gform-theme__disable-framework *))'
THEME_SUBMIT_RULE = ENFORCEMENT_SCOPE + ' .gform-footer .gform_button'


def without_where(selector: str) -> str:
    result = selector
    while ':where(' in result:
        start = result.index(':where(')
        depth = 0
        end = None
        for index in range(start + len(':where'), len(result)):
            char = result[index]
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            raise AssertionError('unbalanced :where() in modeled selector')
        result = result[:start] + result[end:]
    return result


def mechanical_id_class_specificity(selector: str) -> tuple[int, int]:
    modeled = without_where(selector).replace(':has', '')
    ids = len(re.findall(r'#[A-Za-z0-9_-]+', modeled))
    classes = len(re.findall(r'\.[A-Za-z0-9_-]+', modeled))
    return ids, classes


class SrwfRuntimeStabilizationTests(unittest.TestCase):
    def test_verified_orbital_dependency_is_declared_once(self) -> None:
        php = PHP.read_text(encoding='utf-8')
        self.assertIn("SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE = 'gravity_forms_orbital_theme'", php)
        enqueue = re.search(r"wp_enqueue_style\(\s*'srwf-registration-theme'.*?\);", php, re.S)
        self.assertIsNotNone(enqueue)
        self.assertIn('array( SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE )', enqueue.group(0))
        self.assertEqual(1, len(re.findall(r"wp_enqueue_style\(\s*'srwf-registration-theme'", php)))

    def test_submit_rule_uses_proven_enforcement_boundary_and_beats_modeled_host_rule(self) -> None:
        css = CSS.read_text(encoding='utf-8')
        self.assertIn(THEME_SUBMIT_RULE, css)
        self.assertIn(ENFORCEMENT_SCOPE + ' .gform_footer .gform_button', css)
        self.assertIn('inline-size: 100%;', css)
        self.assertNotIn('!important', css)
        self.assertNotRegex(css, r'#gform_submit_button_\d+')

        host_specificity = mechanical_id_class_specificity(HOST_SUBMIT_RULE)
        theme_specificity = mechanical_id_class_specificity(THEME_SUBMIT_RULE)
        self.assertGreater(
            theme_specificity,
            host_specificity,
            f'bounded SRWF Submit selector {theme_specificity} does not dominate modeled host rule {host_specificity}',
        )

        for invariant in (
            '--gf-ctrl-btn-size: 56px;',
            '--gf-ctrl-btn-font-size: 16px;',
            '--gf-ctrl-btn-font-weight: 700;',
        ):
            self.assertIn(invariant, css)

    def test_heading_font_projection_changes_family_without_promoting_title_metrics(self) -> None:
        css = CSS.read_text(encoding='utf-8')
        title = re.search(r'([^{}]*\.gform_title)\s*\{([^{}]*)\}', css, re.S)
        self.assertIsNotNone(title)
        self.assertIn('font-family: "Vazirmatn", system-ui, sans-serif;', title.group(2))
        self.assertNotIn('font-size', title.group(2))
        self.assertNotIn('line-height', title.group(2))
        self.assertNotIn('margin', title.group(2))

        section = re.search(r'([^{}]*\.gsection_title)\s*\{([^{}]*)\}', css, re.S)
        self.assertIsNotNone(section)
        self.assertIn('font-family: "Vazirmatn", system-ui, sans-serif;', section.group(2))
        self.assertIn('font-size: 18px;', section.group(2))
        self.assertIn('font-weight: 700;', section.group(2))

    def test_tom_select_adapter_is_bounded_and_reuses_canonical_control_size(self) -> None:
        css = CSS.read_text(encoding='utf-8')
        selector = NARROW_SCOPE + ' .ts-wrapper .ts-control'
        self.assertIn(selector, css)
        block = re.search(re.escape(selector) + r'\s*\{([^{}]*)\}', css, re.S)
        self.assertIsNotNone(block)
        self.assertIn('min-block-size: var(--gf-ctrl-size);', block.group(1))
        self.assertNotRegex(css, r'(?m)^\s*\.ts-control\s*\{')
        self.assertNotIn('TomSelect(', css)

    def test_gpp_is_not_an_activation_or_visual_dependency(self) -> None:
        php = PHP.read_text(encoding='utf-8')
        css = CSS.read_text(encoding='utf-8')
        self.assertNotIn('gpp-enabled', php)
        self.assertNotIn('gpp-profile', php)
        self.assertNotIn('gpp-enabled', css)
        self.assertNotIn('gpp-profile', css)
        self.assertIn("SRWF_REGISTRATION_THEME_CLASS = 'srwf-registration-theme'", php)

    def test_no_new_global_or_specificity_escape_hatches(self) -> None:
        css = CSS.read_text(encoding='utf-8')
        self.assertNotIn('!important', css)
        self.assertNotRegex(css, r'(?m)^\s*html(?:\s|,|\{)')
        self.assertNotRegex(css, r'(?m)^\s*body(?:\s|,|\{)')
        self.assertNotRegex(css, r'(?m)^\s*\.gform_wrapper(?:\s|,|\{)')
        self.assertNotIn('[data-parent-form]', css)

    def test_unresolved_visual_states_remain_absent(self) -> None:
        css = CSS.read_text(encoding='utf-8')
        for forbidden in (
            '@media',
            'box-shadow',
            '--gf-form-gap-y',
            'grid-template-columns',
            '--gf-ctrl-outline-width-focus',
            '--gf-ctrl-outline-color-focus',
        ):
            self.assertNotIn(forbidden, css)
        self.assertNotRegex(css, r'#gform_wrapper_\d+')
        self.assertNotIn('[data-parent-form]', css)

    def test_gpfup_diagnostic_uses_only_runtime_proven_presentation_consumers(self) -> None:
        js = DIAG_JS.read_text(encoding='utf-8')
        self.assertIn("boundedQuery(target, '.gpfup'", js)
        self.assertIn("boundedQuery(root, '.gpfup__droparea'", js)
        self.assertIn("'RUNTIME_PROVEN'", js)
        for speculative in ('gpfup__crop', 'cropper-', 'gpfup__zoom', 'gpfup__filename'):
            self.assertNotIn(speculative, js)

    def test_diagnostic_source_avoids_prohibited_content_access(self) -> None:
        js = DIAG_JS.read_text(encoding='utf-8')
        prohibited = (
            '.value', 'textContent', 'innerText', 'selectedOptions', '.files',
            'document.cookie', 'localStorage', 'sessionStorage', 'FormData(',
            'file.name', 'option.text', 'option.label',
        )
        for token in prohibited:
            self.assertNotIn(token, js, f'prohibited diagnostic access: {token}')
        self.assertIn("schemaVersion: SCHEMA_VERSION", js)
        self.assertIn("DIAGNOSTIC_VERSION = '0.3.0'", js)
        self.assertIn('دانلود گزارش GTB', js)
        self.assertIn('collectorFailures', js)

    def test_diagnostic_owner_path_is_admin_target_scoped_and_query_free(self) -> None:
        php = DIAG_PHP.read_text(encoding='utf-8')
        self.assertIn("GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '0.3.0'", php)
        self.assertIn("GTB_SRWF_RUNTIME_DIAGNOSTIC_THEME_CLASS = 'srwf-registration-theme'", php)
        self.assertIn("current_user_can( 'manage_options' )", php)
        self.assertNotIn('$_GET', php)
        self.assertNotIn('gtb_srwf_diag', php)

    def test_diagnostic_fixture_proves_bounded_failure_isolated_owner_path(self) -> None:
        completed = subprocess.run(
            ['node', str(THEME / 'tests' / 'test_diagnostic_v03.js')],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn('PASS: diagnostic v0.3 bounded/privacy-safe/failure-isolated fixture', completed.stdout)

    def test_main_push_ci_is_restored(self) -> None:
        workflow = WORKFLOW.read_text(encoding='utf-8')
        self.assertRegex(workflow, r"(?ms)^\s*push:\s*\n\s*branches:\s*\n\s*- main\s*$")
        self.assertIn('pull_request:', workflow)


if __name__ == '__main__':
    unittest.main()
