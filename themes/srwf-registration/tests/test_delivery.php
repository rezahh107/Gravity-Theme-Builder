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

function apply_registered_filter( $hook_name, $value, ...$args ) {
    global $hooks;
    $matching = array_values( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === $hook_name ) );
    usort( $matching, fn( $a, $b ) => $a[3] <=> $b[3] );
    foreach ( $matching as $hook ) {
        $accepted = max( 1, (int) $hook[4] );
        $call_args = array_slice( array_merge( array( $value ), $args ), 0, $accepted );
        $value = call_user_func_array( $hook[2], $call_args );
    }
    return $value;
}

check( SRWF_REGISTRATION_THEME_VERSION === '0.1.10', 'unexpected SRWF test package version' );
check( SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE === 'gravity_forms_orbital_theme', 'verified Orbital handle changed' );

$target = array( 'cssClass' => 'host-class srwf-registration-theme gpp-enabled gpp-profile-srwf-registration', 'requiredIndicator' => 'asterisk' );
$unrelated = array( 'cssClass' => 'plain-form gpp-enabled', 'requiredIndicator' => 'asterisk' );
$stored_target = $target;

check( srwf_registration_theme_is_target_form( $target ), 'target identity not detected' );
check( ! srwf_registration_theme_is_target_form( $unrelated ), 'unrelated identity falsely detected' );

$normal = srwf_registration_theme_get_admission_decision( $target );
check( $normal['formIdentityMatched'] === true, 'normal target identity decision false' );
check( $normal['presentationAdmitted'] === true, 'normal Registration render not admitted' );
check( $normal['renderingContext'] === 'registration', 'normal Registration context mislabeled' );
check( $normal['contextEvidence'] === 'registration_default', 'normal Registration context evidence changed' );
check( $normal['exclusionReason'] === null, 'normal Registration render has exclusion reason' );

$plain = srwf_registration_theme_get_admission_decision( $unrelated );
check( $plain['formIdentityMatched'] === false, 'unrelated form identity decision true' );
check( $plain['presentationAdmitted'] === false, 'unrelated form admitted' );
check( $plain['exclusionReason'] === 'unrelated_form', 'unrelated form exclusion reason changed' );

check( srwf_registration_theme_force_orbital( 'gravity-theme', $unrelated ) === 'gravity-theme', 'unrelated form theme changed' );
check( srwf_registration_theme_force_orbital( 'gravity-theme', $target ) === 'orbital', 'normal target not forced to Orbital' );

srwf_registration_theme_enqueue_styles( $unrelated, false );
check( count( $styles ) === 0, 'unrelated form enqueued SRWF' );
srwf_registration_theme_enqueue_styles( $target, false );
check( count( $styles ) === 1, 'normal target did not enqueue exactly once' );
check( $styles[0]['deps'] === array( 'gravity_forms_orbital_theme' ), 'SRWF is not dependent on Orbital handle' );
check( $styles[0]['handle'] === 'srwf-registration-theme', 'unexpected SRWF style handle' );
check( $styles[0]['ver'] === '0.1.10', 'stylesheet package version not propagated' );

// Native Gravity Forms required legend is the sole explanation surface. The fixture
// includes the native legend so a parallel GTB explanation is mechanically falsifiable.
$native_required_html = '<div class="gform_wrapper"><div class="gform_heading"><div class="gform_required_legend"><span class="gfield_required gfield_required_asterisk">*</span> Required fields</div></div><form method="post"><div class="gform-body"></div></form></div>';
$filtered = apply_registered_filter( 'gform_get_form_filter', $native_required_html, $target );
check( $filtered === $native_required_html, 'GTB changed native required-legend HTML through whole-form filtering' );
check( substr_count( $filtered, 'gform_required_legend' ) === 1, 'native required legend is not a single explanation surface' );
check( strpos( $filtered, 'srwf-required-note' ) === false, 'parallel GTB required note rendered beside native legend' );
check( apply_registered_filter( 'gform_get_form_filter', $filtered, $target ) === $native_required_html, 'rerender/refilter changed or duplicated native legend' );
check( apply_registered_filter( 'gform_get_form_filter', $native_required_html, $unrelated ) === $native_required_html, 'unrelated form HTML changed' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === 'gform_get_form_filter' ) === array(), 'obsolete whole-form required-note hook remains' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === 'gform_required_legend' ) === array(), 'GTB recreates or suppresses native required legend semantics' );
$theme_source = file_get_contents( __DIR__ . '/../src/srwf-registration-theme.php' );
$theme_css = file_get_contents( __DIR__ . '/../src/srwf-registration.css' );
check( strpos( $theme_source, 'srwf-required-note' ) === false, 'obsolete required-note production source path remains' );
check( strpos( $theme_source, 'gform_get_form_filter' ) === false, 'obsolete whole-form form-string filter remains' );
check( strpos( $theme_css, '.srwf-required-note' ) === false, 'obsolete required-note CSS remains' );

// The existing Gravity Forms AJAX argument does not exclude legitimate Registration lifecycle renders.
check( srwf_registration_theme_force_orbital( 'gravity-theme', $target ) === 'orbital', 'validation-style rerender lost Orbital admission' );
srwf_registration_theme_enqueue_styles( $target, false );
check( count( $styles ) === 2, 'validation-style rerender lost SRWF stylesheet admission' );
srwf_registration_theme_enqueue_styles( $target, true );
check( count( $styles ) === 3, 'Registration AJAX render lost SRWF stylesheet admission' );

// Authentic Gravity Flow Entry Detail primary-content context remains excluded.
srwf_registration_theme_enter_entry_detail_context( $target, array() );
$entry_detail = srwf_registration_theme_get_admission_decision( $target );
check( $entry_detail['formIdentityMatched'] === true, 'Entry Detail lost stored target identity' );
check( $entry_detail['presentationAdmitted'] === false, 'Entry Detail target was admitted' );
check( $entry_detail['renderingContext'] === 'gravity_flow_entry_detail', 'Entry Detail context not reported' );
check( $entry_detail['contextEvidence'] === 'gravity_flow_content_bracket', 'Entry Detail content evidence not reported' );
check( $entry_detail['exclusionReason'] === 'gravity_flow_entry_detail', 'Entry Detail exclusion reason not reported' );
check( apply_registered_filter( 'gform_get_form_filter', $native_required_html, $target ) === $native_required_html, 'Entry Detail native required legend was modified by GTB' );
check( srwf_registration_theme_force_orbital( 'gravity-theme', $target ) === 'gravity-theme', 'Entry Detail target forced Orbital' );
srwf_registration_theme_enqueue_styles( $target, false );
check( count( $styles ) === 3, 'Entry Detail target enqueued SRWF stylesheet' );
check( srwf_registration_theme_force_orbital( 'legacy', $unrelated ) === 'legacy', 'Entry Detail unrelated form theme changed' );
srwf_registration_theme_enqueue_styles( $unrelated, false );
check( count( $styles ) === 3, 'Entry Detail unrelated form enqueued SRWF stylesheet' );

// Re-entrant Entry Detail renders remain excluded until the outermost bracket leaves.
srwf_registration_theme_enter_entry_detail_context( $target, array() );
check( srwf_registration_theme_entry_detail_context_depth() === 2, 'Entry Detail nesting depth did not increment' );
srwf_registration_theme_leave_entry_detail_context( $target, array() );
check( srwf_registration_theme_entry_detail_context_depth() === 1, 'Entry Detail nesting depth did not decrement' );
check( ! srwf_registration_theme_is_presentation_admitted( $target ), 'nested Entry Detail suppression ended too early' );
srwf_registration_theme_leave_entry_detail_context( $target, array() );
check( srwf_registration_theme_entry_detail_context_depth() === 0, 'Entry Detail suppression leaked after leave' );

check( srwf_registration_theme_force_orbital( 'gravity-theme', $target ) === 'orbital', 'later normal target stayed suppressed after Entry Detail' );
srwf_registration_theme_enqueue_styles( $target, false );
check( count( $styles ) === 4, 'later normal target did not recover stylesheet admission' );

// A stray leave cannot create negative state or suppress later renders.
srwf_registration_theme_leave_entry_detail_context( $target, array() );
check( srwf_registration_theme_entry_detail_context_depth() === 0, 'Entry Detail context depth underflowed' );
check( srwf_registration_theme_is_presentation_admitted( $target ), 'stray leave altered later Registration admission' );

check( $target === $stored_target, 'admission logic mutated stored form configuration' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === 'gform_form_theme_slug' && $h[2] === 'srwf_registration_theme_force_orbital' ) !== array(), 'theme filter missing' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gform_enqueue_scripts' && $h[2] === 'srwf_registration_theme_enqueue_styles' ) !== array(), 'delivery hook missing' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gravityflow_entry_detail_content_before' && $h[2] === 'srwf_registration_theme_enter_entry_detail_context' && $h[3] === 0 && $h[4] === 2 ) !== array(), 'Entry Detail content enter hook missing or changed' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gravityflow_entry_detail_content_after' && $h[2] === 'srwf_registration_theme_leave_entry_detail_context' && $h[3] === PHP_INT_MAX && $h[4] === 2 ) !== array(), 'Entry Detail content leave hook missing or changed' );

check( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === 'gform_form_settings_menu' && $h[2] === 'srwf_registration_gtb_settings_menu' ) !== array(), 'GTB Theme settings menu hook missing from installable package' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gform_form_settings_page_gtb_theme' && $h[2] === 'srwf_registration_gtb_settings_page' ) !== array(), 'GTB Theme settings page hook missing from installable package' );

echo "PASS: production delivery, native required legend ownership, and rendering-context contract\n";
