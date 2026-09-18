<?php
$hooks = array();
$styles = array();
define( 'ABSPATH', __DIR__ );
function add_filter( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'filter', $hook, $callback, $priority, $args ); }
function add_action( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'action', $hook, $callback, $priority, $args ); }
function plugins_url( $path, $file ) { return 'https://example.test/plugins/srwf/' . $path; }
function wp_enqueue_style( $handle, $src, $deps, $ver ) { global $styles; $styles[] = compact( 'handle', 'src', 'deps', 'ver' ); }
function esc_html__( $text, $domain = null ) { return htmlspecialchars( (string) $text, ENT_QUOTES, 'UTF-8' ); }
function check( $condition, $message ) { if ( ! $condition ) { fwrite( STDERR, "FAIL: $message\n" ); exit( 1 ); } }
require __DIR__ . '/../src/srwf-registration-theme.php';

check( SRWF_REGISTRATION_THEME_VERSION === '0.1.9', 'unexpected SRWF test package version' );
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
check( $styles[0]['ver'] === '0.1.9', 'stylesheet package version not propagated' );

// Required-indicator note is real inert content, idempotent per generated form string, and SRWF-only.
$html = '<div class="gform_wrapper"><form method="post"><div class="gform-body"></div></form></div>';
$noted = srwf_registration_theme_add_required_indicator_note( $html, $target );
check( substr_count( $noted, 'data-srwf-required-note="1"' ) === 1, 'required note not rendered exactly once' );
check( strpos( $noted, 'فیلدهای دارای * الزامی هستند.' ) !== false, 'localized required note wording missing' );
$noted_twice = srwf_registration_theme_add_required_indicator_note( $noted, $target );
check( substr_count( $noted_twice, 'data-srwf-required-note="1"' ) === 1, 'required note duplicated when filter repeated' );
check( srwf_registration_theme_add_required_indicator_note( $html, $unrelated ) === $html, 'required note leaked to unrelated form' );
$text_indicator = $target;
$text_indicator['requiredIndicator'] = 'text';
check( srwf_registration_theme_add_required_indicator_note( $html, $text_indicator ) === $html, 'required note rendered when asterisk indicator was not active' );

// A validation/AJAX rerender receives one fresh note without process-wide suppression.
$rerender = srwf_registration_theme_add_required_indicator_note( $html, $target );
check( substr_count( $rerender, 'data-srwf-required-note="1"' ) === 1, 'validation/AJAX-style rerender lost required note' );

// The existing Gravity Forms AJAX argument does not exclude legitimate Registration lifecycle renders.
check( srwf_registration_theme_force_orbital( 'gravity-theme', $target ) === 'orbital', 'validation-style rerender lost Orbital admission' );
srwf_registration_theme_enqueue_styles( $target, false );
check( count( $styles ) === 2, 'validation-style rerender lost SRWF stylesheet admission' );
srwf_registration_theme_enqueue_styles( $target, true );
check( count( $styles ) === 3, 'Registration AJAX render lost SRWF stylesheet admission' );

// Authentic Gravity Flow Entry Detail primary-content context remains excluded, including the note.
srwf_registration_theme_enter_entry_detail_context( $target, array() );
$entry_detail = srwf_registration_theme_get_admission_decision( $target );
check( $entry_detail['formIdentityMatched'] === true, 'Entry Detail lost stored target identity' );
check( $entry_detail['presentationAdmitted'] === false, 'Entry Detail target was admitted' );
check( $entry_detail['renderingContext'] === 'gravity_flow_entry_detail', 'Entry Detail context not reported' );
check( $entry_detail['contextEvidence'] === 'gravity_flow_content_bracket', 'Entry Detail content evidence not reported' );
check( $entry_detail['exclusionReason'] === 'gravity_flow_entry_detail', 'Entry Detail exclusion reason not reported' );
check( srwf_registration_theme_add_required_indicator_note( $html, $target ) === $html, 'required note leaked into excluded Entry Detail' );
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
check( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === 'gform_get_form_filter' && $h[2] === 'srwf_registration_theme_add_required_indicator_note' && $h[4] === 2 ) !== array(), 'required note rendering hook missing' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gform_enqueue_scripts' && $h[2] === 'srwf_registration_theme_enqueue_styles' ) !== array(), 'delivery hook missing' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gravityflow_entry_detail_content_before' && $h[2] === 'srwf_registration_theme_enter_entry_detail_context' && $h[3] === 0 && $h[4] === 2 ) !== array(), 'Entry Detail content enter hook missing or changed' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gravityflow_entry_detail_content_after' && $h[2] === 'srwf_registration_theme_leave_entry_detail_context' && $h[3] === PHP_INT_MAX && $h[4] === 2 ) !== array(), 'Entry Detail content leave hook missing or changed' );

check( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === 'gform_form_settings_menu' && $h[2] === 'srwf_registration_gtb_settings_menu' ) !== array(), 'GTB Theme settings menu hook missing from installable package' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gform_form_settings_page_gtb_theme' && $h[2] === 'srwf_registration_gtb_settings_page' ) !== array(), 'GTB Theme settings page hook missing from installable package' );

echo "PASS: production delivery, required note, and rendering-context contract\n";
