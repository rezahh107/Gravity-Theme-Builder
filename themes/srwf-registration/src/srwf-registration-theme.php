<?php
/**
 * Plugin Name: SRWF Registration Gravity Forms Theme
 * Description: Theme-local SRWF Registration presentation for opt-in Gravity Forms.
 * Version: 0.1.14
 * Text Domain: gravity-theme-builder
 */

defined( 'ABSPATH' ) || exit;

const SRWF_REGISTRATION_THEME_CLASS = 'srwf-registration-theme';
const SRWF_REGISTRATION_THEME_VERSION = '0.1.14';
const SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE = 'gravity_forms_orbital_theme';
const SRWF_REGISTRATION_CONTEXT_REGISTRATION = 'registration';
const SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL = 'gravity_flow_entry_detail';
const SRWF_REGISTRATION_CONTEXT_EVIDENCE_REGISTRATION = 'registration_default';
const SRWF_REGISTRATION_CONTEXT_EVIDENCE_FLOW_EARLY_ENQUEUE = 'gravity_flow_early_enqueue';
const SRWF_REGISTRATION_CONTEXT_EVIDENCE_FLOW_CONTENT = 'gravity_flow_content_bracket';

/**
 * Return whether the form explicitly opts into the SRWF Registration presentation.
 *
 * Gravity Forms stores Form Settings -> CSS Class Name in the form object's cssClass
 * value. This is form identity only; it does not establish ownership of the current
 * rendering surface.
 *
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return bool
 */
function srwf_registration_theme_is_target_form( $form ) {
    if ( ! is_array( $form ) ) {
        return false;
    }

    $class_value = isset( $form['cssClass'] ) ? trim( (string) $form['cssClass'] ) : '';
    if ( '' === $class_value ) {
        return false;
    }

    $classes = preg_split( '/\s+/', $class_value );

    return is_array( $classes ) && in_array( SRWF_REGISTRATION_THEME_CLASS, $classes, true );
}

/**
 * Read or adjust the request-local Gravity Flow Entry Detail content depth.
 *
 * @param int $delta Positive to enter, negative to leave, zero to read.
 * @return int
 */
function srwf_registration_theme_entry_detail_context_depth( $delta = 0 ) {
    static $depth = 0;

    $delta = (int) $delta;
    if ( 0 !== $delta ) {
        $depth = max( 0, $depth + $delta );
    }

    return $depth;
}

/**
 * Enter the authentic Gravity Flow Entry Detail primary-content bracket.
 *
 * @param array<string,mixed> $form  Current Gravity Forms form object.
 * @param array<string,mixed> $entry Current Gravity Forms entry object.
 * @return void
 */
function srwf_registration_theme_enter_entry_detail_context( $form, $entry ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    srwf_registration_theme_entry_detail_context_depth( 1 );
}

/**
 * Leave the authentic Gravity Flow Entry Detail primary-content bracket.
 *
 * @param array<string,mixed> $form  Current Gravity Forms form object.
 * @param array<string,mixed> $entry Current Gravity Forms entry object.
 * @return void
 */
function srwf_registration_theme_leave_entry_detail_context( $form, $entry ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    srwf_registration_theme_entry_detail_context_depth( -1 );
}

/**
 * Classify the current rendering context.
 *
 * The early Gravity Flow route signal is request-local and source-qualified for the
 * pre-content script enqueue phase. The content bracket remains the authentic later
 * signal for primary-content rendering. Neither signal is persisted in form config.
 *
 * @return array{context:string,evidence:string}
 */
function srwf_registration_theme_rendering_context() {
    if ( srwf_registration_theme_entry_detail_context_depth() > 0 ) {
        return array(
            'context'  => SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL,
            'evidence' => SRWF_REGISTRATION_CONTEXT_EVIDENCE_FLOW_CONTENT,
        );
    }

    if ( srwf_registration_theme_is_gravity_flow_entry_detail_early() ) {
        return array(
            'context'  => SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL,
            'evidence' => SRWF_REGISTRATION_CONTEXT_EVIDENCE_FLOW_EARLY_ENQUEUE,
        );
    }

    return array(
        'context'  => SRWF_REGISTRATION_CONTEXT_REGISTRATION,
        'evidence' => SRWF_REGISTRATION_CONTEXT_EVIDENCE_REGISTRATION,
    );
}

/**
 * Return the bounded admission decision for diagnostics and runtime presentation.
 *
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return array{formIdentityMatched:bool,presentationAdmitted:bool,renderingContext:string,contextEvidence:string,exclusionReason:?string}
 */
function srwf_registration_theme_get_admission_decision( $form ) {
    $identity = srwf_registration_theme_is_target_form( $form );
    $context  = srwf_registration_theme_rendering_context();

    $admitted = $identity && SRWF_REGISTRATION_CONTEXT_REGISTRATION === $context['context'];
    $reason   = null;

    if ( ! $identity ) {
        $reason = 'unrelated_form';
    } elseif ( ! $admitted ) {
        $reason = $context['context'];
    }

    return array(
        'formIdentityMatched' => $identity,
        'presentationAdmitted' => $admitted,
        'renderingContext'     => $context['context'],
        'contextEvidence'      => $context['evidence'],
        'exclusionReason'      => $reason,
    );
}

/**
 * Return whether this form may receive Registration presentation in the current context.
 *
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return bool
 */
function srwf_registration_theme_is_presentation_admitted( $form ) {
    $decision = srwf_registration_theme_get_admission_decision( $form );

    return true === $decision['presentationAdmitted'];
}

/**
 * Detect the authentic Gravity Flow workflow-detail route during early enqueue.
 *
 * Gravity Flow owns route classification through is_workflow_detail_page(). Guard every
 * dependency because the registration theme must remain independently installable.
 *
 * @return bool
 */
function srwf_registration_theme_is_gravity_flow_entry_detail_early() {
    if ( ! class_exists( 'Gravity_Flow' ) || ! is_callable( array( 'Gravity_Flow', 'get_instance' ) ) ) {
        return false;
    }

    $gravity_flow = Gravity_Flow::get_instance();
    if ( ! is_object( $gravity_flow ) || ! is_callable( array( $gravity_flow, 'is_workflow_detail_page' ) ) ) {
        return false;
    }

    return (bool) $gravity_flow->is_workflow_detail_page();
}

/**
 * Force Orbital only for admitted SRWF Registration renders.
 *
 * @param string              $theme Current form theme slug.
 * @param array<string,mixed> $form  Gravity Forms form object.
 * @return string
 */
function srwf_registration_theme_force_orbital( $theme, $form ) {
    if ( srwf_registration_theme_is_presentation_admitted( $form ) ) {
        return 'orbital';
    }

    return $theme;
}
add_filter( 'gform_form_theme_slug', 'srwf_registration_theme_force_orbital', 20, 2 );

/**
 * Enqueue the local SRWF stylesheet only for admitted Registration renders.
 *
 * @param array<string,mixed> $form    Gravity Forms form object.
 * @param bool                $is_ajax Whether Gravity Forms considers this an AJAX render.
 * @return void
 */
function srwf_registration_theme_enqueue_styles( $form, $is_ajax ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    if ( ! srwf_registration_theme_is_presentation_admitted( $form ) ) {
        return;
    }

    wp_enqueue_style(
        'srwf-registration-theme',
        plugins_url( 'srwf-registration.css', __FILE__ ),
        array( SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE ),
        SRWF_REGISTRATION_THEME_VERSION
    );
}
add_action( 'gform_enqueue_scripts', 'srwf_registration_theme_enqueue_styles', 20, 2 );

/*
 * Gravity Flow exposes the primary Entry Detail content bracket after its early enqueue
 * phase. Retain this authentic later boundary as a second line of context ownership.
 */
add_action( 'gravityflow_entry_detail_content_before', 'srwf_registration_theme_enter_entry_detail_context', 0, 2 );
add_action( 'gravityflow_entry_detail_content_after', 'srwf_registration_theme_leave_entry_detail_context', PHP_INT_MAX, 2 );

require_once __DIR__ . '/srwf-registration-layout.php';
require_once __DIR__ . '/srwf-registration-settings.php';
