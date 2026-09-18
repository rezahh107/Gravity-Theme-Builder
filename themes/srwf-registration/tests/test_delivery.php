<?php
$hooks = array();
$styles = array();
define( 'ABSPATH', __DIR__ );
function add_filter( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'filter', $hook, $callback, $priority, $args ); }
function add_action( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'action', $hook, $callback, $priority, $args ); }
function plugins_url( $path, $file ) { return 'https://example.test/plugins/srwf/' . $path; }
function wp_enqueue_style( $handle, $src, $deps, $ver ) { global $styles; $styles[] = compact( 'handle', 'src', 'deps', 'ver' ); }
function check( $condition, $message ) { if ( ! $condition ) { fwrite( STDERR, "FAIL: $message\n" ); exit( 1 ); } }
require __DIR__ . '/../src/srwf-registration-theme.php';
check( SRWF_REGISTRATION_THEME_VERSION === '0.1.3', 'unexpected SRWF test package version' );
check( SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE === 'gravity_forms_orbital_theme', 'verified Orbital handle changed' );
check( srwf_registration_theme_force_orbital( 'gravity', array( 'cssClass' => 'plain-form' ) ) === 'gravity', 'unrelated form theme changed' );
check( srwf_registration_theme_force_orbital( 'gravity', array( 'cssClass' => 'srwf-registration-theme' ) ) === 'orbital', 'target not forced to Orbital' );
srwf_registration_theme_enqueue_styles( array( 'cssClass' => 'plain-form' ), false );
check( count( $styles ) === 0, 'unrelated form enqueued SRWF' );
srwf_registration_theme_enqueue_styles( array( 'cssClass' => 'srwf-registration-theme gpp-enabled gpp-profile-srwf-registration' ), false );
check( count( $styles ) === 1, 'target with unrelated coexistence classes did not enqueue exactly once' );
check( $styles[0]['deps'] === array( 'gravity_forms_orbital_theme' ), 'SRWF is not dependent on Orbital handle' );
check( $styles[0]['handle'] === 'srwf-registration-theme', 'unexpected SRWF style handle' );
check( $styles[0]['ver'] === '0.1.3', 'stylesheet package version not propagated' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gform_enqueue_scripts' && $h[2] === 'srwf_registration_theme_enqueue_styles' ) !== array(), 'delivery hook missing' );
echo "PASS: production delivery contract\n";
