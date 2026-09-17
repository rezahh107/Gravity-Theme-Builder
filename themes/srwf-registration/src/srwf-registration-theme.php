<?php
/**
 * Plugin Name: SRWF Registration Gravity Forms Theme
 * Description: Theme-local SRWF Registration presentation for opt-in Gravity Forms.
 * Version: 0.1.1
 */

defined( 'ABSPATH' ) || exit;

const SRWF_REGISTRATION_THEME_CLASS = 'srwf-registration-theme';
const SRWF_REGISTRATION_THEME_VERSION = '0.1.1';
const SRWF_REGISTRATION_GRAVITY_FORMS_ORBITAL_STYLE_HANDLE = 'gravity_forms_orbital_theme';

/**
 * Return whether the form explicitly opts into the SRWF Registration presentation.
 *
 * Gravity Forms stores Form Settings -> CSS Class Name in the form object's cssClass
 * value. The rendered wrapper receives the corresponding *_wrapper class.
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
 * Ensure only the explicitly opted-in SRWF form uses the Theme Framework/Orbital layer.
 *
 * @param string              $slug Current Gravity Forms theme slug.
 * @param array<string,mixed> $form Gravity Forms form object.
 * @return string
 */
function srwf_registration_theme_force_orbital( $slug, $form ) {
    if ( ! srwf_registration_theme_is_target_form( $form ) ) {
        return $slug;
    }

    return 'orbital';
}
add_filter( 'gform_form_theme_slug', 'srwf_registration_theme_force_orbital', 10, 2 );

/**
 * Enqueue SRWF presentation only when an opted-in form is rendered.
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
    if ( ! srwf_registration_theme_is_target_form( $form ) ) {
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
