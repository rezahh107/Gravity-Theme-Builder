<?php
/** Deterministic bootstrap behavior test; no WordPress/Gravity Forms runtime claim. */

define( 'ABSPATH', __DIR__ );

$registered_actions = array();
$enqueued_styles    = array();

function add_action( $hook, $callback, $priority = 10, $accepted_args = 1 ) {
	global $registered_actions;
	$registered_actions[] = array( $hook, $callback, $priority, $accepted_args );
}

function plugin_dir_url( $file ) {
	return 'https://example.invalid/srwf-registration/';
}

function wp_enqueue_style( $handle, $src, $deps = array(), $version = false ) {
	global $enqueued_styles;
	$enqueued_styles[] = array( $handle, $src, $deps, $version );
}

require dirname( __DIR__ ) . '/srwf-registration.php';

function assert_true( $condition, $message ) {
	if ( ! $condition ) {
		fwrite( STDERR, "FAIL: {$message}\n" );
		exit( 1 );
	}
}

assert_true( count( $registered_actions ) === 1, 'bootstrap registers exactly one lifecycle hook' );
assert_true( $registered_actions[0][0] === 'gform_enqueue_scripts', 'bootstrap uses gform_enqueue_scripts' );
assert_true( $registered_actions[0][2] === 10 && $registered_actions[0][3] === 2, 'hook priority/arity are explicit' );

gtb_srwf_registration_enqueue_styles( array( 'cssClass' => '' ), false );
gtb_srwf_registration_enqueue_styles( array( 'cssClass' => 'unrelated-form' ), false );
assert_true( count( $enqueued_styles ) === 0, 'unrelated forms do not enqueue SRWF CSS' );

gtb_srwf_registration_enqueue_styles( array( 'cssClass' => 'alpha srwf-registration omega' ), true );
assert_true( count( $enqueued_styles ) === 1, 'opted-in form enqueues exactly one stylesheet' );
assert_true( $enqueued_styles[0][0] === 'gtb-srwf-registration', 'expected stylesheet handle is used' );
assert_true( str_ends_with( $enqueued_styles[0][1], '/src/srwf-registration.css' ), 'expected theme-local stylesheet is delivered' );

$enqueued_styles = array();
gtb_srwf_registration_enqueue_styles( array( 'cssClass' => 'srwf-registration-extra' ), false );
assert_true( count( $enqueued_styles ) === 0, 'activation requires an exact class token, not a substring' );

echo "BOOTSTRAP CONTRACT CHECK: PASS\n";
echo "Proves: deterministic opt-in/enqueue behavior with WordPress functions stubbed; does NOT prove WordPress/Gravity Forms lifecycle execution.\n";
