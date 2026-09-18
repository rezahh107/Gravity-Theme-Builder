<?php
/**
 * Plugin Name: GTB SRWF Runtime Diagnostic
 * Description: Admin-gated privacy-safe structural/presentation diagnostic for SRWF Registration.
 * Version: 0.3.0
 */

defined( 'ABSPATH' ) || exit;

const GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '0.3.0';
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
 * Load the read-only diagnostic automatically for an administrator when the real
 * SRWF target form is rendered. The browser-side control only creates a local JSON
 * download; there is no server endpoint or remote transport.
 *
 * @param array<string,mixed> $form    Gravity Forms form object.
 * @param bool                $is_ajax Whether Gravity Forms is using AJAX submission.
 * @return void
 */
function gtb_srwf_runtime_diagnostic_enqueue( $form, $is_ajax ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! gtb_srwf_runtime_diagnostic_is_target_form( $form ) ) {
        return;
    }

    wp_enqueue_script(
        'gtb-srwf-runtime-diagnostic-v03',
        plugins_url( 'assets/runtime-diagnostic.js', __FILE__ ),
        array(),
        GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION,
        true
    );
}
add_action( 'gform_enqueue_scripts', 'gtb_srwf_runtime_diagnostic_enqueue', 30, 2 );
