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

check( GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION === '0.3.5', 'unexpected diagnostic package version' );
check( GTB_SRWF_RUNTIME_DIAGNOSTIC_COLLECTOR_VERSION === '0.3.0', 'existing structural collector version changed' );
check( GTB_SRWF_RUNTIME_DIAGNOSTIC_ADMISSION_VERSION === '0.3.2', 'existing admission collector version changed' );
check( GTB_SRWF_RUNTIME_DIAGNOSTIC_QUALIFICATION_VERSION === '0.3.4', 'existing qualification core version changed' );
check( GTB_SRWF_RUNTIME_DIAGNOSTIC_VISUAL_REPAIR_VERSION === '0.3.5', 'visual repair diagnostic version missing' );

$form = array(
    'id' => 11,
    'cssClass' => 'srwf-registration-theme gpp-enabled gpp-profile-srwf-registration',
    'labelPlacement' => 'top_label',
    'descriptionPlacement' => 'above',
    'validationPlacement' => 'above',
    'subLabelPlacement' => 'above',
    'validationSummary' => true,
    'requiredIndicator' => 'asterisk',
    'fields' => array(
        array( 'id' => 4, 'labelPlacement' => '', 'descriptionPlacement' => '', 'subLabelPlacement' => '' ),
        array( 'id' => 7, 'descriptionPlacement' => 'below' ),
    ),
);
$is_admin_user = false;
gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 0, 'diagnostic loaded for non-admin' );

$is_admin_user = true;
gtb_srwf_runtime_diagnostic_enqueue( array( 'id' => 99, 'cssClass' => 'plain-form' ), false );
check( count( $scripts ) === 0, 'diagnostic loaded for unrelated form' );

gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 6, 'normal target did not load the complete diagnostic composition' );
check( $scripts[0]['handle'] === 'gtb-srwf-runtime-diagnostic-v03', 'wrong structural diagnostic handle' );
check( $scripts[0]['ver'] === '0.3.0' && $scripts[0]['footer'] === true, 'wrong structural diagnostic metadata' );
check( $scripts[1]['handle'] === 'gtb-srwf-radio-card-geometry-v035', 'wrong radio geometry diagnostic handle' );
check( $scripts[1]['src'] === 'https://example.test/plugins/diag/assets/binary-choice-geometry.js', 'radio geometry diagnostic asset path changed' );
check( $scripts[1]['deps'] === array( 'gtb-srwf-runtime-diagnostic-v03' ), 'radio geometry collector must load after structural diagnostic' );
check( $scripts[1]['ver'] === '0.3.5' && $scripts[1]['footer'] === true, 'wrong radio geometry collector metadata' );
check( $scripts[2]['handle'] === 'gtb-srwf-admission-diagnostic-v032', 'wrong admission diagnostic handle' );
check( $scripts[2]['ver'] === '0.3.2' && $scripts[2]['footer'] === true, 'wrong admission diagnostic metadata' );
check( $scripts[3]['handle'] === 'gtb-srwf-v1-qualification-v034', 'v1 qualification core missing' );
check( $scripts[3]['src'] === 'https://example.test/plugins/diag/assets/srwf-v1-qualification.js', 'qualification asset path changed' );
check( $scripts[3]['deps'] === array( 'gtb-srwf-runtime-diagnostic-v03', 'gtb-srwf-radio-card-geometry-v035' ), 'qualification core ordering changed' );
check( $scripts[3]['ver'] === '0.3.4' && $scripts[3]['footer'] === true, 'wrong qualification core metadata' );
check( $scripts[4]['handle'] === 'gtb-srwf-visual-repair-qualification-v035', 'visual repair collector missing' );
check( $scripts[4]['src'] === 'https://example.test/plugins/diag/assets/visual-repair-qualification.js', 'visual repair asset path changed' );
check( $scripts[4]['deps'] === array( 'gtb-srwf-runtime-diagnostic-v03', 'gtb-srwf-radio-card-geometry-v035', 'gtb-srwf-v1-qualification-v034' ), 'visual repair collector ordering changed' );
check( $scripts[4]['ver'] === '0.3.5' && $scripts[4]['footer'] === true, 'wrong visual repair metadata' );
check( $scripts[5]['handle'] === 'gtb-srwf-version-provenance-v035', 'final qualification composer missing' );
check( $scripts[5]['src'] === 'https://example.test/plugins/diag/assets/version-provenance.js', 'qualification composer asset path changed' );
check( $scripts[5]['deps'] === array( 'gtb-srwf-runtime-diagnostic-v03', 'gtb-srwf-radio-card-geometry-v035', 'gtb-srwf-v1-qualification-v034', 'gtb-srwf-visual-repair-qualification-v035' ), 'qualification composer must load after all component collectors' );
check( $scripts[5]['ver'] === '0.3.5' && $scripts[5]['footer'] === true, 'wrong qualification composer metadata' );

check( count( $inline_scripts ) === 2, 'normal target missing bounded inline diagnostic payloads' );
check( $inline_scripts[0]['handle'] === 'gtb-srwf-admission-diagnostic-v032' && $inline_scripts[0]['position'] === 'before', 'admission payload attached to wrong script' );
check( strpos( $inline_scripts[0]['data'], '"presentationAdmitted":true' ) !== false, 'normal admission fact missing' );
check( strpos( $inline_scripts[0]['data'], '"renderingContext":"registration"' ) !== false, 'normal context fact missing' );
check( $inline_scripts[1]['handle'] === 'gtb-srwf-v1-qualification-v034' && $inline_scripts[1]['position'] === 'before', 'layout readiness payload attached to wrong script' );
check( strpos( $inline_scripts[1]['data'], 'GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID["11"]' ) !== false, 'form 11 readiness is not keyed to its rendered form' );
check( strpos( $inline_scripts[1]['data'], '"requiredIndicator":{"expected":"asterisk","current":"asterisk","state":"MATCHING"}' ) !== false, 'required indicator readiness missing' );
check( strpos( $inline_scripts[1]['data'], '"conflictingFieldOverrideCount":1' ) !== false, 'field override count missing' );
check( strpos( $inline_scripts[1]['data'], 'Field 7' ) === false, 'diagnostic leaked arbitrary field label/text' );
check( strpos( $inline_scripts[1]['data'], 'GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS =' ) === false, 'legacy unkeyed readiness singleton remains' );

$form_two = $form;
$form_two['id'] = 12;
$form_two['descriptionPlacement'] = 'below';
gtb_srwf_runtime_diagnostic_enqueue( $form_two, false );
check( count( $inline_scripts ) === 4, 'second target did not publish its own bounded payloads' );
check( $inline_scripts[3]['handle'] === 'gtb-srwf-v1-qualification-v034', 'second layout readiness attached to wrong script' );
check( strpos( $inline_scripts[3]['data'], 'GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID["12"]' ) !== false, 'form 12 readiness is not keyed to its rendered form' );
check( strpos( $inline_scripts[3]['data'], '"state":"NEEDS ATTENTION"' ) !== false, 'form 12 readiness state missing' );
check( strpos( $inline_scripts[3]['data'], '["11"]' ) === false, 'second target readiness cross-bound to form 11' );

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
check( count( $scripts ) === 6, 'context-excluded target lost admin diagnostic observability' );
check( count( $inline_scripts ) === 2, 'context-excluded target missing bounded payloads' );
check( strpos( $inline_scripts[0]['data'], '"presentationAdmitted":false' ) !== false, 'excluded presentation fact missing' );
check( strpos( $inline_scripts[0]['data'], '"renderingContext":"gravity_flow_entry_detail"' ) !== false, 'Entry Detail context fact missing' );
check( strpos( $inline_scripts[0]['data'], '"contextEvidence":"gravity_flow_early_enqueue"' ) !== false, 'early Entry Detail context evidence missing' );
check( strpos( $inline_scripts[0]['data'], '"exclusionReason":"gravity_flow_entry_detail"' ) !== false, 'Entry Detail exclusion reason missing' );
check( strpos( $inline_scripts[1]['data'], 'GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID["11"]' ) !== false, 'context-excluded target readiness lost per-form binding' );

check( array_filter( $hooks, fn( $h ) => $h[0] === 'gform_enqueue_scripts' && $h[1] === 'gtb_srwf_runtime_diagnostic_enqueue' && $h[2] === 30 && $h[3] === 2 ) !== array(), 'diagnostic delivery hook missing' );
echo "PASS: diagnostic v0.3.5 composition, provenance, and per-target bounded delivery contract\n";
