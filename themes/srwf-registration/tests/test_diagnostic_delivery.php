<?php
$hooks = array();
$scripts = array();
$inline_scripts = array();
$is_admin_user = true;
$production_decision = array(
    'formIdentityMatched' => true,
    'presentationAdmitted' => true,
    'renderingContext' => 'registration',
    'contextEvidence' => 'registration_default',
    'exclusionReason' => null,
);
define( 'ABSPATH', __DIR__ );
function add_action( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( $hook, $callback, $priority, $args ); }
function plugins_url( $path, $file ) { return 'https://example.test/plugins/diag/' . $path; }
function current_user_can( $capability ) { global $is_admin_user; return $capability === 'manage_options' && $is_admin_user; }
function wp_enqueue_script( $handle, $src, $deps, $ver, $footer ) { global $scripts; $scripts[] = compact( 'handle', 'src', 'deps', 'ver', 'footer' ); }
function wp_add_inline_script( $handle, $data, $position = 'after' ) { global $inline_scripts; $inline_scripts[] = compact( 'handle', 'data', 'position' ); return true; }
function wp_json_encode( $value ) { return json_encode( $value ); }
function srwf_registration_theme_get_admission_decision( $form ) { global $production_decision; return $production_decision; }
function check( $condition, $message ) { if ( ! $condition ) { fwrite( STDERR, "FAIL: $message\n" ); exit( 1 ); } }
require __DIR__ . '/../diagnostic/srwf-runtime-diagnostic.php';

check( GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION === '0.3.2', 'unexpected diagnostic package version' );
check( GTB_SRWF_RUNTIME_DIAGNOSTIC_COLLECTOR_VERSION === '0.3.0', 'existing structural collector version changed' );

$form = array( 'cssClass' => 'srwf-registration-theme gpp-enabled gpp-profile-srwf-registration' );
$is_admin_user = false;
gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 0, 'diagnostic loaded for non-admin' );

$is_admin_user = true;
gtb_srwf_runtime_diagnostic_enqueue( array( 'cssClass' => 'plain-form' ), false );
check( count( $scripts ) === 0, 'diagnostic loaded for unrelated form' );

$production_decision = array(
    'formIdentityMatched' => true,
    'presentationAdmitted' => true,
    'renderingContext' => 'registration',
    'contextEvidence' => 'registration_default',
    'exclusionReason' => null,
);
gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 2, 'normal target did not load both diagnostic collectors' );
check( $scripts[0]['handle'] === 'gtb-srwf-runtime-diagnostic-v03', 'wrong structural diagnostic handle' );
check( $scripts[0]['ver'] === '0.3.0' && $scripts[0]['footer'] === true, 'wrong structural diagnostic metadata' );
check( $scripts[1]['handle'] === 'gtb-srwf-admission-diagnostic-v032', 'wrong admission diagnostic handle' );
check( $scripts[1]['ver'] === '0.3.2' && $scripts[1]['footer'] === true, 'wrong admission diagnostic metadata' );
check( count( $inline_scripts ) === 1, 'normal target missing bounded admission payload' );
check( $inline_scripts[0]['handle'] === 'gtb-srwf-admission-diagnostic-v032' && $inline_scripts[0]['position'] === 'before', 'admission payload attached to wrong script' );
check( strpos( $inline_scripts[0]['data'], '"presentationAdmitted":true' ) !== false, 'normal admission fact missing' );
check( strpos( $inline_scripts[0]['data'], '"renderingContext":"registration"' ) !== false, 'normal context fact missing' );
check( strpos( $inline_scripts[0]['data'], '"contextEvidence":"registration_default"' ) !== false, 'normal context evidence missing' );

$scripts = array();
$inline_scripts = array();
$production_decision = array(
    'formIdentityMatched' => true,
    'presentationAdmitted' => false,
    'renderingContext' => 'gravity_flow_entry_detail',
    'contextEvidence' => 'gravity_flow_early_enqueue',
    'exclusionReason' => 'gravity_flow_entry_detail',
);
gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 2, 'context-excluded target lost admin diagnostic observability' );
check( count( $inline_scripts ) === 1, 'context-excluded target missing admission payload' );
check( strpos( $inline_scripts[0]['data'], '"formIdentityMatched":true' ) !== false, 'excluded target identity fact missing' );
check( strpos( $inline_scripts[0]['data'], '"presentationAdmitted":false' ) !== false, 'excluded presentation fact missing' );
check( strpos( $inline_scripts[0]['data'], '"renderingContext":"gravity_flow_entry_detail"' ) !== false, 'Entry Detail context fact missing' );
check( strpos( $inline_scripts[0]['data'], '"contextEvidence":"gravity_flow_early_enqueue"' ) !== false, 'early Entry Detail context evidence missing' );
check( strpos( $inline_scripts[0]['data'], '"exclusionReason":"gravity_flow_entry_detail"' ) !== false, 'Entry Detail exclusion reason missing' );

check( array_filter( $hooks, fn( $h ) => $h[0] === 'gform_enqueue_scripts' && $h[1] === 'gtb_srwf_runtime_diagnostic_enqueue' && $h[2] === 30 && $h[3] === 2 ) !== array(), 'diagnostic delivery hook missing' );
echo "PASS: diagnostic delivery and earliest-context observability contract\n";
