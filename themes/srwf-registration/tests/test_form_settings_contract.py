from pathlib import Path
import re
import unittest

THEME = Path(__file__).resolve().parents[1]
SETTINGS = (THEME / 'src' / 'srwf-registration-settings.php').read_text(encoding='utf-8')


class FormSettingsContractTests(unittest.TestCase):
    def test_native_form_settings_seam_only(self):
        self.assertIn("gform_form_settings_menu", SETTINGS)
        self.assertIn("gform_form_settings_page_", SETTINGS)
        self.assertNotIn("admin_menu", SETTINGS)
        self.assertNotIn("GFAddOn", SETTINGS)

    def test_no_label_or_dom_inference(self):
        self.assertNotIn("adminLabel", SETTINGS)
        self.assertNotIn("nth-child", SETTINGS)
        self.assertNotIn("querySelector", SETTINGS)
        self.assertNotRegex(SETTINGS, r"preg_(?:match|replace).*label")

    def test_no_durable_numeric_selector_or_form_11_contract(self):
        self.assertNotIn("#gform_wrapper_", SETTINGS)
        self.assertNotRegex(SETTINGS, r"#field_[0-9]+_[0-9]+")
        self.assertNotRegex(SETTINGS, r"form[_ ]?id\s*(?:===|==|=)\s*11\b")

    def test_explicit_mutation_security_boundary(self):
        self.assertIn("GFAPI::current_user_can_any( SRWF_REGISTRATION_GTB_CAPABILITY )", SETTINGS)
        self.assertIn("current_user_can( SRWF_REGISTRATION_GTB_CAPABILITY )", SETTINGS)
        self.assertIn("check_admin_referer( SRWF_REGISTRATION_GTB_NONCE_ACTION", SETTINGS)
        self.assertEqual(SETTINGS.count("GFAPI::update_form("), 1)
        self.assertIn("'save' === $action", SETTINGS)
        self.assertIn("'recommend' === $action", SETTINGS)
        self.assertIn("made no configuration changes", SETTINGS)

    def test_recommended_draft_is_explicit_and_never_saved_implicitly(self):
        self.assertIn("Load Recommended SRWF Draft", SETTINGS)
        self.assertIn("unsaved draft", SETTINGS)
        self.assertIn("Proposal:", SETTINGS)
        self.assertIn("Nothing changes in Gravity Forms until Save GTB Configuration succeeds.", SETTINGS)
        self.assertIn("$current_config = srwf_registration_gtb_get_config( $form );", SETTINGS)
        self.assertIn("Current saved theme profile:", SETTINGS)
        self.assertIn("$current_config['enabled']", SETTINGS)

    def test_admin_assets_not_globalized(self):
        self.assertNotIn("admin_enqueue_scripts", SETTINGS)
        self.assertNotIn("wp_enqueue_script", SETTINGS)
        self.assertNotIn("wp_enqueue_style", SETTINGS)


if __name__ == '__main__':
    unittest.main()
