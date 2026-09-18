<?php
/**
 * Plugin Name: GTB SRWF Runtime Diagnostic
 * Description: Admin-gated privacy-safe structural/presentation diagnostic for SRWF Registration.
 * Version: 0.3.3
 */

defined( 'ABSPATH' ) || exit;

const GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '0.3.3';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_COLLECTOR_VERSION = '0.3.0';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_ADMISSION_VERSION = '0.3.2';
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
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return array{formIdentityMatched:bool,presentationAdmitted:?bool,renderingContext:string,contextEvidence:string,exclusionReason:?string}
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

            $evidence = isset( $decision['contextEvidence'] ) ? (string) $decision['contextEvidence'] : 'unknown';
            if ( ! in_array( $evidence, array( 'registration_default', 'gravity_flow_early_enqueue', 'gravity_flow_content_bracket' ), true ) ) {
                $evidence = 'unknown';
            }

            $reason = isset( $decision['exclusionReason'] ) ? $decision['exclusionReason'] : null;
            if ( ! in_array( $reason, array( null, 'unrelated_form', 'gravity_flow_entry_detail' ), true ) ) {
                $reason = null;
            }

            return array(
                'formIdentityMatched'  => true === ( $decision['formIdentityMatched'] ?? false ),
                'presentationAdmitted' => true === ( $decision['presentationAdmitted'] ?? false ),
                'renderingContext'     => $context,
                'contextEvidence'      => $evidence,
                'exclusionReason'      => $reason,
            );
        }
    }

    return array(
        'formIdentityMatched'  => $identity_matched,
        'presentationAdmitted' => null,
        'renderingContext'     => 'unknown',
        'contextEvidence'      => 'unknown',
        'exclusionReason'      => $identity_matched ? 'production_admission_unavailable' : 'unrelated_form',
    );
}

/**
 * Load the local read-only diagnostics for an administrator whenever the SRWF target
 * identity is rendered. Observability remains available when presentation is excluded.
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
        'gtb-srwf-binary-choice-geometry-v033',
        plugins_url( 'assets/binary-choice-geometry.js', __FILE__ ),
        array( 'gtb-srwf-runtime-diagnostic-v03' ),
        GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION,
        true
    );

    wp_enqueue_script(
        'gtb-srwf-admission-diagnostic-v032',
        plugins_url( 'assets/admission-diagnostic.js', __FILE__ ),
        array(),
        GTB_SRWF_RUNTIME_DIAGNOSTIC_ADMISSION_VERSION,
        true
    );

    $decision = gtb_srwf_runtime_diagnostic_admission_decision( $form );
    $json     = wp_json_encode( $decision );
    if ( ! is_string( $json ) ) {
        return;
    }

    wp_add_inline_script(
        'gtb-srwf-admission-diagnostic-v032',
        'window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS = window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS || []; window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS.push(' . $json . ');',
        'before'
    );
}
add_action( 'gform_enqueue_scripts', 'gtb_srwf_runtime_diagnostic_enqueue', 30, 2 );
