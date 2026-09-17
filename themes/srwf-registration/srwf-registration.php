<?php
/**
 * Plugin Name: Gravity Theme Builder — SRWF Registration
 * Description: Theme-local delivery bootstrap for the owner-approved SRWF Registration presentation.
 * Version: 0.1.0
 * Requires PHP: 7.4
 */

defined( 'ABSPATH' ) || exit;

const GTB_SRWF_REGISTRATION_ACTIVATION_CLASS = 'srwf-registration';
const GTB_SRWF_REGISTRATION_STYLE_HANDLE     = 'gtb-srwf-registration';
const GTB_SRWF_REGISTRATION_VERSION          = '0.1.0';

/**
 * Enqueue the SRWF presentation only for an explicitly opted-in Gravity Form.
 *
 * Activation is configured in Gravity Forms via:
 * Form Settings -> Form Layout -> CSS Class Name -> "srwf-registration".
 * Gravity Forms remains the owner of rendering, validation, submission, and state.
 *
 * @param array $form    Current Gravity Forms form object.
 * @param bool  $is_ajax Whether the form is configured for AJAX submission.
 */
function gtb_srwf_registration_enqueue_styles( $form, $is_ajax ) {
	unset( $is_ajax );

	$classes = isset( $form['cssClass'] ) ? (string) $form['cssClass'] : '';
	$classes = preg_split( '/\s+/', trim( $classes ), -1, PREG_SPLIT_NO_EMPTY );

	if ( ! in_array( GTB_SRWF_REGISTRATION_ACTIVATION_CLASS, $classes, true ) ) {
		return;
	}

	wp_enqueue_style(
		GTB_SRWF_REGISTRATION_STYLE_HANDLE,
		plugin_dir_url( __FILE__ ) . 'src/srwf-registration.css',
		array(),
		GTB_SRWF_REGISTRATION_VERSION
	);
}
add_action( 'gform_enqueue_scripts', 'gtb_srwf_registration_enqueue_styles', 10, 2 );
