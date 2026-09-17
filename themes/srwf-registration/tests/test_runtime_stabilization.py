from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / 'themes' / 'srwf-registration'
PHP = THEME / 'src' / 'srwf-registration-theme.php'
CSS = THEME / 'src' / 'srwf-registration.css'
DIAG_JS = THEME / 'diagnostic' / 'assets' / 'runtime-diagnostic.js'
WORKFLOW = REPO / '.github' / 'workflows' / 'srwf-registration-static.yml'


class SrwfRuntimeStabilizationTests(unittest.TestCase):
    def test_verified_orbital_dependency_is_declared_once(self) -> None:
        php = PHP.read_text(encoding='utf-8')
        self.assertIn("SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE = 'gravity_forms_orbital_theme'", php)
        enqueue = re.search(r"wp_enqueue_style\(\s*'srwf-registration-theme'.*?\);", php, re.S)
        self.assertIsNotNone(enqueue)
        self.assertIn('array( SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE )', enqueue.group(0))
        self.assertEqual(1, len(re.findall(r"wp_enqueue_style\(\s*'srwf-registration-theme'", php)))

    def test_submit_rule_still_matches_runtime_element_shape_without_form_id(self) -> None:
        css = CSS.read_text(encoding='utf-8')
        self.assertIn('.gform-theme--framework.srwf-registration-theme_wrapper .gform-footer .gform_button', css)
        self.assertIn('.gform-theme--framework.srwf-registration-theme_wrapper .gform_footer .gform_button', css)
        self.assertIn('inline-size: 100%;', css)
        self.assertNotRegex(css, r'#gform_submit_button_\d+')

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

    def test_diagnostic_source_avoids_prohibited_content_access(self) -> None:
        js = DIAG_JS.read_text(encoding='utf-8')
        prohibited = (
            '.value', 'textContent', 'innerText', 'selectedOptions',
            'document.cookie', 'localStorage', 'sessionStorage', 'FormData('
        )
        for token in prohibited:
            self.assertNotIn(token, js, f'prohibited diagnostic access: {token}')
        self.assertIn("schemaVersion: SCHEMA_VERSION", js)
        self.assertIn("SCHEMA_VERSION = 'v0.2'", js)

    def test_diagnostic_fixture_proves_bounded_large_select_path(self) -> None:
        completed = subprocess.run(
            ['node', str(THEME / 'tests' / 'test_diagnostic_v02.js')],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn('PASS: diagnostic v0.2 bounded/privacy-safe fixture', completed.stdout)

    def test_main_push_ci_is_restored(self) -> None:
        workflow = WORKFLOW.read_text(encoding='utf-8')
        self.assertRegex(workflow, r"(?ms)^\s*push:\s*\n\s*branches:\s*\n\s*- main\s*$")
        self.assertIn('pull_request:', workflow)


if __name__ == '__main__':
    unittest.main()
