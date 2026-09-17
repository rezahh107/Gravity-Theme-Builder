<?php
/**
 * Plugin Name: GTB SRWF Runtime Diagnostic
 * Description: Admin-gated privacy-safe structural/presentation diagnostic for SRWF Registration.
 * Version: 0.2.0
 */

defined( 'ABSPATH' ) || exit;

const GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '0.2.0';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_QUERY = 'gtb_srwf_diag';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_THEME_CLASS = 'srwf-registration-theme';

/**
 * Return whether the rendered form is the explicit SRWF target.
 *
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return bool
 */
function gtb_srwf_runtime_diagnostic_is_target_form( $form ) {
    if ( ! is_array( $form ) ) {
        return false;
    }

    $class_value = isset( $form['cssClass'] ) ? trim( (string) $form['cssClass'] ) : '';
    if ( '' === $class_value ) {
        return false;
    }

    $classes = preg_split( '/\s+/', $class_value );

    return is_array( $classes ) && in_array( GTB_SRWF_RUNTIME_DIAGNOSTIC_THEME_CLASS, $classes, true );
}

/**
 * Require an explicit v0.2 diagnostic request.
 *
 * @return bool
 */
function gtb_srwf_runtime_diagnostic_requested() {
    if ( ! isset( $_GET[ GTB_SRWF_RUNTIME_DIAGNOSTIC_QUERY ] ) ) {
        return false;
    }

    $requested = sanitize_key( wp_unslash( $_GET[ GTB_SRWF_RUNTIME_DIAGNOSTIC_QUERY ] ) );

    return 'v0.2' === $requested;
}

/**
 * Load the read-only diagnostic only for an administrator explicitly requesting it
 * on a rendered SRWF target form. There is no server endpoint or remote transport.
 *
 * @param array<string,mixed> $form    Gravity Forms form object.
 * @param bool                $is_ajax Whether Gravity Forms is using AJAX submission.
 * @return void
 */
function gtb_srwf_runtime_diagnostic_enqueue( $form, $is_ajax ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! gtb_srwf_runtime_diagnostic_requested() ) {
        return;
    }

    if ( ! gtb_srwf_runtime_diagnostic_is_target_form( $form ) ) {
        return;
    }

    wp_enqueue_script(
        'gtb-srwf-runtime-diagnostic-v02',
        plugins_url( 'assets/runtime-diagnostic.js', __FILE__ ),
        array(),
        GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION,
        true
    );
}
add_action( 'gform_enqueue_scripts', 'gtb_srwf_runtime_diagnostic_enqueue', 30, 2 );
