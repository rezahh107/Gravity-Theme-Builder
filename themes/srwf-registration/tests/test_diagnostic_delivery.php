<?php
$hooks = array();
$scripts = array();
$is_admin_user = true;
define( 'ABSPATH', __DIR__ );
function add_action( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( $hook, $callback, $priority, $args ); }
function plugins_url( $path, $file ) { return 'https://example.test/plugins/diag/' . $path; }
function current_user_can( $capability ) { global $is_admin_user; return $capability === 'manage_options' && $is_admin_user; }
function sanitize_key( $value ) { return strtolower( preg_replace( '/[^a-z0-9._-]/', '', (string) $value ) ); }
function wp_unslash( $value ) { return $value; }
function wp_enqueue_script( $handle, $src, $deps, $ver, $footer ) { global $scripts; $scripts[] = compact( 'handle', 'src', 'deps', 'ver', 'footer' ); }
function check( $condition, $message ) { if ( ! $condition ) { fwrite( STDERR, "FAIL: $message\n" ); exit( 1 ); } }
require __DIR__ . '/../diagnostic/srwf-runtime-diagnostic.php';
$form = array( 'cssClass' => 'srwf-registration-theme gpp-enabled gpp-profile-srwf-registration' );
$_GET = array();
gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 0, 'diagnostic loaded without explicit request' );
$_GET['gtb_srwf_diag'] = 'v0.2';
$is_admin_user = false;
gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 0, 'diagnostic loaded for non-admin' );
$is_admin_user = true;
gtb_srwf_runtime_diagnostic_enqueue( array( 'cssClass' => 'plain-form' ), false );
check( count( $scripts ) === 0, 'diagnostic loaded for unrelated form' );
gtb_srwf_runtime_diagnostic_enqueue( $form, false );
check( count( $scripts ) === 1, 'diagnostic did not load for explicit admin target' );
check( $scripts[0]['handle'] === 'gtb-srwf-runtime-diagnostic-v02', 'wrong diagnostic handle' );
check( $scripts[0]['ver'] === '0.2.0' && $scripts[0]['footer'] === true, 'wrong diagnostic delivery metadata' );
echo "PASS: diagnostic delivery contract\n";
