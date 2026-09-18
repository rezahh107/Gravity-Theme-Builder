<?php
/**
 * Plugin Name: GTB SRWF Runtime Diagnostic
 * Description: Admin-gated privacy-safe structural/presentation diagnostic for SRWF Registration.
 * Version: 0.3.1
 */

defined( 'ABSPATH' ) || exit;

const GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '0.3.1';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_COLLECTOR_VERSION = '0.3.0';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_THEME_CLASS = 'srwf-registration-theme';

/**
 * Return whether the rendered form is the explicit SRWF target identity.
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
 * Return the production admission decision using only bounded enumerated facts.
 *
 * The diagnostic consumes the production plugin's decision API when available so it
 * does not create a second request-classification system. When the production plugin
 * is unavailable, the diagnostic says so rather than inventing a context decision.
 *
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return array{formIdentityMatched:bool,presentationAdmitted:?bool,renderingContext:string,exclusionReason:?string}
 */
function gtb_srwf_runtime_diagnostic_admission_decision( $form ) {
    $identity_matched = gtb_srwf_runtime_diagnostic_is_target_form( $form );

    if ( function_exists( 'srwf_registration_theme_get_admission_decision' ) ) {
        $decision = srwf_registration_theme_get_admission_decision( $form );
        if ( is_array( $decision ) ) {
            $context = isset( $decision['renderingContext'] ) ? (string) $decision['renderingContext'] : 'unknown';
            if ( ! in_array( $context, array( 'registration', 'gravity_flow_entry_detail' ), true ) ) {
                $context = 'unknown';
            }

            $reason = isset( $decision['exclusionReason'] ) ? $decision['exclusionReason'] : null;
            if ( ! in_array( $reason, array( null, 'unrelated_form', 'gravity_flow_entry_detail' ), true ) ) {
                $reason = null;
            }

            return array(
                'formIdentityMatched'  => true === ( $decision['formIdentityMatched'] ?? false ),
                'presentationAdmitted' => true === ( $decision['presentationAdmitted'] ?? false ),
                'renderingContext'     => $context,
                'exclusionReason'      => $reason,
            );
        }
    }

    return array(
        'formIdentityMatched'  => $identity_matched,
        'presentationAdmitted' => null,
        'renderingContext'     => 'unknown',
        'exclusionReason'      => $identity_matched ? 'production_admission_unavailable' : 'unrelated_form',
    );
}

/**
 * Load the local read-only diagnostics for an administrator whenever the SRWF target
 * identity is rendered. This intentionally remains available when production
 * presentation is context-excluded, because observability is not ownership.
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
        GTB_SRWF_RUNTIME_DIAGNOSTIC_COLLECTOR_VERSION,
        true
    );

    wp_enqueue_script(
        'gtb-srwf-admission-diagnostic-v031',
        plugins_url( 'assets/admission-diagnostic.js', __FILE__ ),
        array(),
        GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION,
        true
    );

    $decision = gtb_srwf_runtime_diagnostic_admission_decision( $form );
    $json     = wp_json_encode( $decision );
    if ( ! is_string( $json ) ) {
        return;
    }

    wp_add_inline_script(
        'gtb-srwf-admission-diagnostic-v031',
        'window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS = window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS || []; window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS.push(' . $json . ');',
        'before'
    );
}
add_action( 'gform_enqueue_scripts', 'gtb_srwf_runtime_diagnostic_enqueue', 30, 2 );
