from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
SETTINGS = THEME / "src" / "srwf-registration-settings.php"


class FormSettingsNativePermissionTests(unittest.TestCase):
    def test_gravity_forms_permission_resolver_is_preferred_over_raw_wordpress_capability(self) -> None:
        source = SETTINGS.read_text(encoding="utf-8")
        self.assertIn("GFAPI::current_user_can_any( SRWF_REGISTRATION_GTB_CAPABILITY )", source)
        self.assertIn("srwf_registration_gtb_current_user_can_edit_form()", source)
        self.assertNotIn(
            "if ( ! current_user_can( SRWF_REGISTRATION_GTB_CAPABILITY ) )",
            source,
        )

        harness = textwrap.dedent(
            f"""\
            <?php
            define( 'ABSPATH', __DIR__ );
            define( 'SRWF_REGISTRATION_THEME_CLASS', 'srwf-registration-theme' );
            function add_filter( $hook, $callback, $priority = 10, $args = 1 ) {{}}
            function add_action( $hook, $callback, $priority = 10, $args = 1 ) {{}}
            function current_user_can( $capability ) {{ return false; }}
            class GFAPI {{
                public static $allowed = true;
                public static function current_user_can_any( $capability ) {{
                    return self::$allowed && 'gravityforms_edit_forms' === $capability;
                }}
            }}
            require {SETTINGS.as_posix()!r};
            if ( ! srwf_registration_gtb_current_user_can_edit_form() ) {{
                fwrite( STDERR, "native Gravity Forms permission was rejected\n" );
                exit( 1 );
            }}
            GFAPI::$allowed = false;
            if ( srwf_registration_gtb_current_user_can_edit_form() ) {{
                fwrite( STDERR, "denied Gravity Forms permission was accepted\n" );
                exit( 1 );
            }}
            echo "PASS: native Gravity Forms permission resolver\n";
            """
        )

        with tempfile.NamedTemporaryFile("w", suffix=".php", encoding="utf-8", delete=False) as handle:
            handle.write(harness)
            script = Path(handle.name)

        try:
            completed = subprocess.run(
                ["php", str(script)],
                check=False,
                capture_output=True,
                text=True,
            )
        finally:
            script.unlink(missing_ok=True)

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("PASS: native Gravity Forms permission resolver", completed.stdout)


if __name__ == "__main__":
    unittest.main()
