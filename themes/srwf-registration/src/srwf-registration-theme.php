<?php
/**
 * Plugin Name: SRWF Registration Gravity Forms Theme
 * Description: Theme-local SRWF Registration presentation for opt-in Gravity Forms.
 * Version: 0.1.7
 */

defined( 'ABSPATH' ) || exit;

const SRWF_REGISTRATION_THEME_CLASS = 'srwf-registration-theme';
const SRWF_REGISTRATION_THEME_VERSION = '0.1.7';
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

add_action( 'gravityflow_entry_detail_content_before', 'srwf_registration_theme_enter_entry_detail_context', 0, 2 );
add_action( 'gravityflow_entry_detail_content_after', 'srwf_registration_theme_leave_entry_detail_context', PHP_INT_MAX, 2 );

/**
 * Detect the source-proven Gravity Flow 3.1.0 early Entry Detail enqueue phase.
 *
 * Gravity Flow calls GFFormDisplay::enqueue_form_scripts() from its own enqueue
 * callback before the entry-detail content hooks run. The host's own
 * is_workflow_detail_page() predicate identifies the route; GTB does not parse URLs,
 * query strings, page IDs, form IDs, or labels. The Gravity Flow post-enqueue actions
 * bound this early phase so a later independent Registration render in the same
 * request is not request-wide suppressed.
 *
 * @return bool
 */
function srwf_registration_theme_is_gravity_flow_early_entry_detail_enqueue() {
    if ( ! function_exists( 'gravity_flow' ) || ! function_exists( 'doing_action' ) || ! function_exists( 'did_action' ) ) {
        return false;
    }

    $flow = gravity_flow();
    if ( ! is_object( $flow ) || ! is_callable( array( $flow, 'is_workflow_detail_page' ) ) || ! $flow->is_workflow_detail_page() ) {
        return false;
    }

    if ( doing_action( 'wp_enqueue_scripts' ) ) {
        if ( ! is_callable( array( $flow, 'look_for_shortcode' ) ) || ! $flow->look_for_shortcode() ) {
            return false;
        }

        return 0 === did_action( 'gravityflow_enqueue_frontend_scripts' );
    }

    if ( doing_action( 'admin_enqueue_scripts' ) ) {
        return 0 === did_action( 'gravityflow_enqueue_admin_scripts' );
    }

    return false;
}

/**
 * Return the current rendering-context classification and bounded evidence source.
 *
 * @return array{renderingContext:string,contextEvidence:string}
 */
function srwf_registration_theme_rendering_context_decision() {
    if ( srwf_registration_theme_entry_detail_context_depth() > 0 ) {
        return array(
            'renderingContext' => SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL,
            'contextEvidence'  => SRWF_REGISTRATION_CONTEXT_EVIDENCE_FLOW_CONTENT,
        );
    }

    if ( srwf_registration_theme_is_gravity_flow_early_entry_detail_enqueue() ) {
        return array(
            'renderingContext' => SRWF_REGISTRATION_CONTEXT_GRAVITY_FLOW_ENTRY_DETAIL,
            'contextEvidence'  => SRWF_REGISTRATION_CONTEXT_EVIDENCE_FLOW_EARLY_ENQUEUE,
        );
    }

    return array(
        'renderingContext' => SRWF_REGISTRATION_CONTEXT_REGISTRATION,
        'contextEvidence'  => SRWF_REGISTRATION_CONTEXT_EVIDENCE_REGISTRATION,
    );
}

/**
 * Return the current rendering-context classification.
 *
 * @return string
 */
function srwf_registration_theme_rendering_context() {
    $decision = srwf_registration_theme_rendering_context_decision();
    return $decision['renderingContext'];
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
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return array{formIdentityMatched:bool,presentationAdmitted:bool,renderingContext:string,contextEvidence:string,exclusionReason:?string}
 */
function srwf_registration_theme_get_admission_decision( $form ) {
    $identity_matched = srwf_registration_theme_is_target_form( $form );
    $context_decision = srwf_registration_theme_rendering_context_decision();
    $context          = $context_decision['renderingContext'];
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
        'contextEvidence'      => $context_decision['contextEvidence'],
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
 * The verified Gravity Forms Orbital style handle remains a WordPress style
 * dependency so admitted Registration renders preserve the proven host order.
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
