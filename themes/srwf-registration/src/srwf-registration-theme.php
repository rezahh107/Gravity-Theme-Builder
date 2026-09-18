<?php
/**
 * Plugin Name: SRWF Registration Gravity Forms Theme
 * Description: Theme-local SRWF Registration presentation for opt-in Gravity Forms.
 * Version: 0.1.4
 */

defined( 'ABSPATH' ) || exit;

const SRWF_REGISTRATION_THEME_CLASS = 'srwf-registration-theme';
const SRWF_REGISTRATION_THEME_VERSION = '0.1.4';
const SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE = 'gravity_forms_orbital_theme';
const SRWF_REGISTRATION_CONTEXT_REGISTRATION = 'registration';
const SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL = 'gravity_flow_entry_detail';

/**
 * Return whether the form explicitly opts into the SRWF Registration presentation.
 *
 * Gravity Forms stores Form Settings -> CSS Class Name in the form object's cssClass
 * value. The rendered wrapper receives the corresponding *_wrapper class. This is
 * form identity only; it does not establish ownership of the current render surface.
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
 * Read or adjust the request-local Gravity Flow Entry Detail nesting depth.
 *
 * State is process/request-local only. Nothing is stored in options, user meta,
 * transients, cookies, URLs, or form configuration. The floor at zero prevents an
 * unmatched leave callback from turning later renders into a negative-depth state.
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
 * Enter the authentic Gravity Flow Entry Detail rendering bracket.
 *
 * @param array<string,mixed> $form  Current Gravity Forms form object.
 * @param array<string,mixed> $entry Current Gravity Forms entry object.
 * @return void
 */
function srwf_registration_theme_enter_entry_detail_context( $form, $entry ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    srwf_registration_theme_entry_detail_context_depth( 1 );
}

/**
 * Leave the authentic Gravity Flow Entry Detail rendering bracket.
 *
 * @param array<string,mixed> $form  Current Gravity Forms form object.
 * @param array<string,mixed> $entry Current Gravity Forms entry object.
 * @return void
 */
function srwf_registration_theme_leave_entry_detail_context( $form, $entry ) { // phpcs:ignore Generic.CodeAnalysis.UnusedFunctionParameter.FoundAfterLastUsed
    srwf_registration_theme_entry_detail_context_depth( -1 );
}

/*
 * Gravity Flow 3.1.0 source-proven bracket around the primary Entry Detail content.
 * Priority 0 enters before the host continues to its field/editor render. The leave
 * callback runs last so other content-after callbacks remain inside Entry Detail.
 */
add_action( 'gravityflow_entry_detail_content_before', 'srwf_registration_theme_enter_entry_detail_context', 0, 2 );
add_action( 'gravityflow_entry_detail_content_after', 'srwf_registration_theme_leave_entry_detail_context', PHP_INT_MAX, 2 );

/**
 * Return the current rendering-context classification.
 *
 * @return string
 */
function srwf_registration_theme_rendering_context() {
    return srwf_registration_theme_entry_detail_context_depth() > 0
        ? SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL
        : SRWF_REGISTRATION_CONTEXT_REGISTRATION;
}

/**
 * Return whether Registration presentation owns the current render context.
 *
 * @return bool
 */
function srwf_registration_theme_is_registration_context_permitted() {
    return SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL !== srwf_registration_theme_rendering_context();
}

/**
 * Return a bounded, privacy-safe admission decision for the current form/render.
 *
 * This deliberately separates stored form identity from request-local presentation
 * ownership. It contains no form ID, entry ID, URL, labels, field values, or user data.
 *
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return array{formIdentityMatched:bool,presentationAdmitted:bool,renderingContext:string,exclusionReason:?string}
 */
function srwf_registration_theme_get_admission_decision( $form ) {
    $identity_matched = srwf_registration_theme_is_target_form( $form );
    $context          = srwf_registration_theme_rendering_context();
    $context_allowed  = SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL !== $context;

    $exclusion_reason = null;
    if ( ! $identity_matched ) {
        $exclusion_reason = 'unrelated_form';
    } elseif ( ! $context_allowed ) {
        $exclusion_reason = 'gravity_flow_entry_detail';
    }

    return array(
        'formIdentityMatched'  => $identity_matched,
        'presentationAdmitted' => $identity_matched && $context_allowed,
        'renderingContext'     => $context,
        'exclusionReason'      => $exclusion_reason,
    );
}

/**
 * Return whether the current form and render context admit SRWF presentation.
 *
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return bool
 */
function srwf_registration_theme_is_presentation_admitted( $form ) {
    $decision = srwf_registration_theme_get_admission_decision( $form );

    return true === $decision['presentationAdmitted'];
}

/**
 * Ensure only an admitted SRWF Registration render uses Theme Framework/Orbital.
 *
 * @param string              $slug Current Gravity Forms theme slug.
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return string
 */
function srwf_registration_theme_force_orbital( $slug, $form ) {
    if ( ! srwf_registration_theme_is_presentation_admitted( $form ) ) {
        return $slug;
    }

    return 'orbital';
}
add_filter( 'gform_form_theme_slug', 'srwf_registration_theme_force_orbital', 10, 2 );

/**
 * Enqueue SRWF presentation only for an admitted Registration render.
 *
 * The verified Gravity Forms Orbital style handle is declared as a WordPress style
 * dependency so dependency resolution places the SRWF stylesheet after Orbital even
 * when Gravity Forms enqueues its theme presentation later in its own lifecycle.
 * If that registered host dependency is unavailable, WordPress fails the dependent
 * branch closed instead of printing SRWF early with an invalid ordering assumption.
 *
 * @param array<string,mixed> $form    Gravity Forms form object.
 * @param bool                $is_ajax Whether Gravity Forms is using AJAX submission.
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
