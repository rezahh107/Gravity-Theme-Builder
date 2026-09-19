<?php
/**
 * Plugin Name: GTB SRWF Runtime Diagnostic
 * Description: Admin-gated privacy-safe structural/presentation diagnostic for SRWF Registration.
 * Version: 0.3.5
 */

defined( 'ABSPATH' ) || exit;

const GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION = '0.3.5';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_COLLECTOR_VERSION = '0.3.5';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_ADMISSION_VERSION = '0.3.2';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_QUALIFICATION_VERSION = '0.3.5';
const GTB_SRWF_RUNTIME_DIAGNOSTIC_THEME_CLASS = 'srwf-registration-theme';

function gtb_srwf_runtime_diagnostic_is_target_form( $form ) {
    if ( ! is_array( $form ) ) { return false; }
    $class_value = isset( $form['cssClass'] ) ? trim( (string) $form['cssClass'] ) : '';
    if ( '' === $class_value ) { return false; }
    $classes = preg_split( '/\s+/', $class_value );
    return is_array( $classes ) && in_array( GTB_SRWF_RUNTIME_DIAGNOSTIC_THEME_CLASS, $classes, true );
}

function gtb_srwf_runtime_diagnostic_admission_decision( $form ) {
    $identity_matched = gtb_srwf_runtime_diagnostic_is_target_form( $form );
    if ( function_exists( 'srwf_registration_theme_get_admission_decision' ) ) {
        $decision = srwf_registration_theme_get_admission_decision( $form );
        if ( is_array( $decision ) ) {
            $context = isset( $decision['renderingContext'] ) ? (string) $decision['renderingContext'] : 'unknown';
            if ( ! in_array( $context, array( 'registration', 'gravity_flow_entry_detail' ), true ) ) { $context = 'unknown'; }
            $evidence = isset( $decision['contextEvidence'] ) ? (string) $decision['contextEvidence'] : 'unknown';
            if ( ! in_array( $evidence, array( 'registration_default', 'gravity_flow_early_enqueue', 'gravity_flow_content_bracket' ), true ) ) { $evidence = 'unknown'; }
            $reason = isset( $decision['exclusionReason'] ) ? $decision['exclusionReason'] : null;
            if ( ! in_array( $reason, array( null, 'unrelated_form', 'gravity_flow_entry_detail' ), true ) ) { $reason = null; }
            return array(
                'formIdentityMatched' => true === ( $decision['formIdentityMatched'] ?? false ),
                'presentationAdmitted' => true === ( $decision['presentationAdmitted'] ?? false ),
                'renderingContext' => $context,
                'contextEvidence' => $evidence,
                'exclusionReason' => $reason,
            );
        }
    }
    return array(
        'formIdentityMatched' => $identity_matched,
        'presentationAdmitted' => null,
        'renderingContext' => 'unknown',
        'contextEvidence' => 'unknown',
        'exclusionReason' => $identity_matched ? 'production_admission_unavailable' : 'unrelated_form',
    );
}

function gtb_srwf_runtime_diagnostic_field_get( $field, $key ) {
    if ( is_object( $field ) && isset( $field->{$key} ) ) { return $field->{$key}; }
    return is_array( $field ) && array_key_exists( $key, $field ) ? $field[ $key ] : null;
}

function gtb_srwf_runtime_diagnostic_form_layout_readiness( $form ) {
    $expected = array(
        'labelPlacement' => 'top_label',
        'descriptionPlacement' => 'above',
        'validationPlacement' => 'above',
        'subLabelPlacement' => 'above',
        'validationSummary' => true,
        'requiredIndicator' => 'asterisk',
    );
    $properties = array();
    $matching = true;
    foreach ( $expected as $property => $target ) {
        $current = array_key_exists( $property, $form ) ? $form[ $property ] : null;
        $current = is_bool( $current ) ? $current : ( null === $current ? null : (string) $current );
        $matches = $current === $target;
        $matching = $matching && $matches;
        $properties[ $property ] = array( 'expected' => $target, 'current' => $current, 'state' => $matches ? 'MATCHING' : 'NEEDS ATTENTION' );
    }
    $field_expected = array( 'labelPlacement' => 'top_label', 'descriptionPlacement' => 'above', 'subLabelPlacement' => 'above' );
    $override_count = 0;
    foreach ( isset( $form['fields'] ) && is_array( $form['fields'] ) ? $form['fields'] : array() as $field ) {
        foreach ( $field_expected as $property => $target ) {
            $current = gtb_srwf_runtime_diagnostic_field_get( $field, $property );
            if ( null === $current || '' === (string) $current || $target === (string) $current ) { continue; }
            $override_count++;
        }
    }
    return array(
        'state' => $matching && 0 === $override_count ? 'READY' : 'NEEDS ATTENTION',
        'properties' => $properties,
        'conflictingFieldOverrideCount' => $override_count,
    );
}

function gtb_srwf_runtime_diagnostic_enqueue( $form, $is_ajax ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    if ( ! current_user_can( 'manage_options' ) || ! gtb_srwf_runtime_diagnostic_is_target_form( $form ) ) { return; }

    wp_enqueue_script( 'gtb-srwf-runtime-diagnostic-v03', plugins_url( 'assets/runtime-diagnostic.js', __FILE__ ), array(), GTB_SRWF_RUNTIME_DIAGNOSTIC_COLLECTOR_VERSION, true );
    wp_enqueue_script( 'gtb-srwf-radio-card-geometry-v035', plugins_url( 'assets/binary-choice-geometry.js', __FILE__ ), array( 'gtb-srwf-runtime-diagnostic-v03' ), GTB_SRWF_RUNTIME_DIAGNOSTIC_QUALIFICATION_VERSION, true );
    wp_enqueue_script( 'gtb-srwf-admission-diagnostic-v032', plugins_url( 'assets/admission-diagnostic.js', __FILE__ ), array(), GTB_SRWF_RUNTIME_DIAGNOSTIC_ADMISSION_VERSION, true );
    wp_enqueue_script( 'gtb-srwf-v1-qualification-v035', plugins_url( 'assets/srwf-v1-qualification.js', __FILE__ ), array( 'gtb-srwf-runtime-diagnostic-v03', 'gtb-srwf-radio-card-geometry-v035' ), GTB_SRWF_RUNTIME_DIAGNOSTIC_QUALIFICATION_VERSION, true );

    $decision = gtb_srwf_runtime_diagnostic_admission_decision( $form );
    $json = wp_json_encode( $decision );
    if ( is_string( $json ) ) {
        wp_add_inline_script( 'gtb-srwf-admission-diagnostic-v032', 'window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS = window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS || []; window.GTB_SRWF_RUNTIME_ADMISSION_DECISIONS.push(' . $json . ');', 'before' );
    }

    $form_id = isset( $form['id'] ) ? (int) $form['id'] : 0;
    if ( $form_id > 0 ) {
        $layout_json = wp_json_encode( gtb_srwf_runtime_diagnostic_form_layout_readiness( $form ) );
        $form_key_json = wp_json_encode( (string) $form_id );
        if ( is_string( $layout_json ) && is_string( $form_key_json ) ) {
            wp_add_inline_script( 'gtb-srwf-v1-qualification-v035', 'window.GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID = window.GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID || {}; window.GTB_SRWF_RUNTIME_FORM_LAYOUT_READINESS_BY_FORM_ID[' . $form_key_json . '] = ' . $layout_json . ';', 'before' );
        }
    }
}
add_action( 'gform_enqueue_scripts', 'gtb_srwf_runtime_diagnostic_enqueue', 30, 2 );
