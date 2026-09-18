from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
THEME = REPO / 'themes' / 'srwf-registration'
PRODUCTION_PHP = THEME / 'src' / 'srwf-registration-theme.php'
PRODUCTION_README = THEME / 'src' / 'README.md'
DIAGNOSTIC_PHP = THEME / 'diagnostic' / 'srwf-runtime-diagnostic.php'
ADMISSION_JS = THEME / 'diagnostic' / 'assets' / 'admission-diagnostic.js'


class SrwfRenderContextBoundaryTests(unittest.TestCase):
    def test_identity_and_context_are_separate_and_combined_once(self) -> None:
        php = PRODUCTION_PHP.read_text(encoding='utf-8')
        self.assertIn('function srwf_registration_theme_is_target_form', php)
        self.assertIn('function srwf_registration_theme_is_registration_context_permitted', php)
        self.assertIn('function srwf_registration_theme_is_presentation_admitted', php)
        self.assertIn('function srwf_registration_theme_get_admission_decision', php)
        self.assertIsNotNone(re.search(
            r"function srwf_registration_theme_is_presentation_admitted\( \$form \).*?"
            r"srwf_registration_theme_get_admission_decision\( \$form \).*?presentationAdmitted",
            php,
            re.S,
        ))

    def test_authentic_entry_detail_hooks_bracket_request_local_depth(self) -> None:
        php = PRODUCTION_PHP.read_text(encoding='utf-8')
        self.assertIn("add_action( 'gravityflow_entry_detail_content_before', 'srwf_registration_theme_enter_entry_detail_context', 0, 2 );", php)
        self.assertIn("add_action( 'gravityflow_entry_detail_content_after', 'srwf_registration_theme_leave_entry_detail_context', PHP_INT_MAX, 2 );", php)
        self.assertIn('static $depth = 0;', php)
        self.assertIn('$depth = max( 0, $depth + $delta );', php)
        self.assertNotIn('update_option(', php)
        self.assertNotIn('set_transient(', php)
        self.assertNotIn('update_user_meta(', php)
        self.assertNotIn('setcookie(', php)

    def test_theme_and_stylesheet_share_combined_admission(self) -> None:
        php = PRODUCTION_PHP.read_text(encoding='utf-8')
        force = re.search(r'function srwf_registration_theme_force_orbital\(.*?\n}', php, re.S)
        enqueue = re.search(r'function srwf_registration_theme_enqueue_styles\(.*?\n}', php, re.S)
        self.assertIsNotNone(force)
        self.assertIsNotNone(enqueue)
        self.assertIn('srwf_registration_theme_is_presentation_admitted( $form )', force.group(0))
        self.assertIn('srwf_registration_theme_is_presentation_admitted( $form )', enqueue.group(0))

    def test_no_forbidden_context_heuristics_or_gpp_dependency(self) -> None:
        php = PRODUCTION_PHP.read_text(encoding='utf-8')
        lowered = php.lower()
        for token in (
            'request_uri', 'query_string', '$_get', '$_request', 'get_query_var(',
            'gpp-enabled', 'gpp-profile', 'gravity-presentation-profiles',
        ):
            self.assertNotIn(token, lowered, f'forbidden production context dependency: {token}')
        self.assertNotRegex(php, r"\['cssClass'\]\s*=")
        self.assertNotRegex(php, r"unset\s*\(\s*\$form\s*\[\s*['\"]cssClass")
        self.assertNotRegex(php, r"(?:form|field)[_-]?id\s*===?\s*\d+")

    def test_source_qualification_is_version_bounded_and_runtime_honest(self) -> None:
        source = PRODUCTION_README.read_text(encoding='utf-8')
        for required in (
            'Gravity Flow `3.1.0`',
            'Gravity Forms `3.1.1.1`',
            'gravityflow_entry_detail_content_before',
            'gravityflow_entry_detail_content_after',
            'GFFormDisplay::get_form()',
            'gform_enqueue_scripts',
            'gform_form_theme_slug',
            'SOURCE_PROVEN',
            'OWNER_RUNTIME_REQUIRED',
            'ac0573b75831380417a21a455176e25eb746d718bbbd0bb70d6da6f48cba5404',
            '542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b',
        ):
            self.assertIn(required, source)
        self.assertNotRegex(source, r'(?m)^rendering_context_boundary:\s*RUNTIME_PROVEN\s*$')
        self.assertIn('This is not yet a `RUNTIME_PROVEN rendering-context boundary` claim.', source)

    def test_admission_diagnostic_is_bounded_and_private(self) -> None:
        php = DIAGNOSTIC_PHP.read_text(encoding='utf-8')
        js = ADMISSION_JS.read_text(encoding='utf-8')
        self.assertIn("function_exists( 'srwf_registration_theme_get_admission_decision' )", php)
        self.assertIn("'presentationAdmitted'", php)
        self.assertIn("'renderingContext'", php)
        self.assertIn("'exclusionReason'", php)
        self.assertIn('production_admission_unavailable', php)
        self.assertNotIn('gpp-enabled', php.lower())
        self.assertNotIn('gpp-profile', php.lower())
        for token in (
            '.value', 'textContent', 'innerText', 'selectedOptions',
            'document.cookie', 'localStorage', 'sessionStorage', 'FormData('
        ):
            self.assertNotIn(token, js, f'prohibited admission diagnostic access: {token}')
        self.assertNotIn('location.href', js)
        self.assertNotIn('location.search', js)

    def test_admission_diagnostic_node_fixture(self) -> None:
        completed = subprocess.run(
            ['node', str(THEME / 'tests' / 'test_admission_diagnostic_v031.js')],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn('PASS: admission diagnostic v0.3.1 bounded/privacy-safe context fixture', completed.stdout)


if __name__ == '__main__':
    unittest.main()
