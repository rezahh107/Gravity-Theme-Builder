<?php
/** SRWF Registration host-owned Form Layout readiness and explicit bounded apply path. */
defined( 'ABSPATH' ) || exit;

const SRWF_REGISTRATION_GTB_LAYOUT_NONCE_ACTION = 'srwf_registration_gtb_layout_apply';
const SRWF_REGISTRATION_GTB_LAYOUT_NONCE_NAME = 'srwf_registration_gtb_layout_nonce';

/**
 * Owner-authorized Gravity Forms Form Layout destination.
 *
 * @return array<string,mixed>
 */
function srwf_registration_gtb_layout_expected() {
    return array(
        'labelPlacement'       => 'top_label',
        'descriptionPlacement' => 'above',
        'validationPlacement'  => 'above',
        'subLabelPlacement'    => 'above',
        'validationSummary'    => true,
        'requiredIndicator'    => 'asterisk',
    );
}

/** @return array<string,string> */
function srwf_registration_gtb_layout_labels() {
    return array(
        'labelPlacement'       => 'Label Placement',
        'descriptionPlacement' => 'Description Placement',
        'validationPlacement'  => 'Validation Message Placement',
        'subLabelPlacement'    => 'Sub-label Placement',
        'validationSummary'    => 'Validation Summary',
        'requiredIndicator'    => 'Required Field Indicator',
    );
}

/**
 * Normalize a bounded layout value only for comparison/reporting.
 *
 * @param mixed $value Value from the current Form Object.
 * @return mixed
 */
function srwf_registration_gtb_layout_compare_value( $value ) {
    return is_bool( $value ) ? $value : ( null === $value ? null : (string) $value );
}

/**
 * Return only the form-level properties that differ from the SRWF destination.
 *
 * @param array<string,mixed> $form Current Form Object.
 * @return array<string,array{current:mixed,expected:mixed}>
 */
function srwf_registration_gtb_layout_diff( $form ) {
    $diff = array();
    foreach ( srwf_registration_gtb_layout_expected() as $property => $expected ) {
        $current = array_key_exists( $property, $form ) ? $form[ $property ] : null;
        $current = srwf_registration_gtb_layout_compare_value( $current );
        if ( $current !== $expected ) {
            $diff[ $property ] = array( 'current' => $current, 'expected' => $expected );
        }
    }
    return $diff;
}

/**
 * Detect supported explicit field-level placement values that defeat the form-level destination.
 * Empty values are inherited and therefore are not conflicts.
 *
 * @param array<string,mixed> $form Current Form Object.
 * @return array<int,array{field_id:int,field_type:string,property:string,current:string,expected:string}>
 */
function srwf_registration_gtb_layout_field_override_conflicts( $form ) {
    $conflicts = array();
    $expected = array(
        'labelPlacement'       => 'top_label',
        'descriptionPlacement' => 'above',
        'subLabelPlacement'    => 'above',
    );

    foreach ( isset( $form['fields'] ) && is_array( $form['fields'] ) ? $form['fields'] : array() as $field ) {
        foreach ( $expected as $property => $required ) {
            $value = srwf_registration_gtb_field_get( $field, $property );
            if ( null === $value || '' === (string) $value ) {
                continue;
            }
            if ( (string) $value === $required ) {
                continue;
            }
            $conflicts[] = array(
                'field_id'   => srwf_registration_gtb_field_id( $field ),
                'field_type' => srwf_registration_gtb_field_type( $field ),
                'property'   => $property,
                'current'    => (string) $value,
                'expected'   => $required,
            );
        }
    }

    return $conflicts;
}

/**
 * Read the current Form Layout state without mutation.
 *
 * @param array<string,mixed> $form Current Form Object.
 * @return array{state:string,properties:array<string,array{expected:mixed,current:mixed,state:string}>,field_override_conflicts:array<int,array<string,mixed>>}
 */
function srwf_registration_gtb_layout_readiness( $form ) {
    $diff = srwf_registration_gtb_layout_diff( $form );
    $properties = array();
    foreach ( srwf_registration_gtb_layout_expected() as $property => $expected ) {
        $current = array_key_exists( $property, $form ) ? srwf_registration_gtb_layout_compare_value( $form[ $property ] ) : null;
        $properties[ $property ] = array(
            'expected' => $expected,
            'current'  => $current,
            'state'    => array_key_exists( $property, $diff ) ? 'NEEDS ATTENTION' : 'MATCHING',
        );
    }

    $overrides = srwf_registration_gtb_layout_field_override_conflicts( $form );
    return array(
        'state'                    => empty( $diff ) && empty( $overrides ) ? 'READY' : 'NEEDS ATTENTION',
        'properties'               => $properties,
        'field_override_conflicts' => $overrides,
    );
}

/**
 * Apply only the authorized form-level layout properties to the latest Form Object.
 *
 * The current Form Object is re-read inside this function immediately before diffing,
 * so a stale page-render snapshot is never used as the mutation source.
 *
 * @param int $form_id Gravity Forms form id.
 * @return array<string,mixed>|WP_Error
 */
function srwf_registration_gtb_apply_layout( $form_id ) {
    if ( ! srwf_registration_gtb_current_user_can_edit_form() ) {
        return new WP_Error( 'gtb_layout_forbidden', 'You do not have permission to edit this Gravity Forms form.' );
    }
    if ( ! class_exists( 'GFAPI' ) || ! is_callable( array( 'GFAPI', 'get_form' ) ) || ! is_callable( array( 'GFAPI', 'update_form' ) ) ) {
        return new WP_Error( 'gtb_layout_gravity_forms_unavailable', 'Gravity Forms is not available to update Form Layout settings.' );
    }

    $current = GFAPI::get_form( absint( $form_id ) );
    if ( ! is_array( $current ) ) {
        return new WP_Error( 'gtb_layout_form_unavailable', 'GTB could not re-read the current Gravity Forms form.' );
    }

    $diff = srwf_registration_gtb_layout_diff( $current );
    if ( empty( $diff ) ) {
        return array(
            'status'    => 'ALREADY MATCHING',
            'wrote'     => false,
            'form'      => $current,
            'readiness' => srwf_registration_gtb_layout_readiness( $current ),
        );
    }

    $next = $current;
    foreach ( $diff as $property => $change ) {
        $next[ $property ] = $change['expected'];
    }

    $result = GFAPI::update_form( $next );
    if ( is_wp_error( $result ) ) {
        return $result;
    }
    if ( true !== $result ) {
        return new WP_Error( 'gtb_layout_update_failed', 'Gravity Forms did not confirm the Form Layout update.' );
    }

    $fresh = GFAPI::get_form( absint( $form_id ) );
    if ( ! is_array( $fresh ) ) {
        return new WP_Error( 'gtb_layout_readback_failed', 'GTB could not re-read the Form Object after the update.' );
    }
    if ( ! empty( srwf_registration_gtb_layout_diff( $fresh ) ) ) {
        return new WP_Error( 'gtb_layout_persistence_failed', 'Gravity Forms did not persist all requested SRWF Form Layout properties.' );
    }

    return array(
        'status'    => 'APPLIED',
        'wrote'     => true,
        'form'      => $fresh,
        'readiness' => srwf_registration_gtb_layout_readiness( $fresh ),
    );
}

/** @param mixed $value Value to display in the admin readiness table. */
function srwf_registration_gtb_layout_display_value( $value ) {
    if ( true === $value ) {
        return 'true';
    }
    if ( false === $value ) {
        return 'false';
    }
    if ( null === $value || '' === (string) $value ) {
        return '(not set)';
    }
    return (string) $value;
}

/**
 * Render the bounded Owner-facing SRWF Form Presentation Readiness surface.
 * Ordinary rendering is read-only. Only the explicit Apply action mutates.
 *
 * @param int $form_id Gravity Forms form id.
 * @return void
 */
function srwf_registration_gtb_render_form_presentation_readiness( $form_id ) {
    $action = isset( $_POST['gtb_action'] ) ? sanitize_key( wp_unslash( $_POST['gtb_action'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing
    $result = null;

    if ( 'apply_layout' === $action ) {
        if ( ! srwf_registration_gtb_current_user_can_edit_form() ) {
            wp_die( esc_html__( 'You do not have permission to edit this Gravity Forms form.', 'gravity-theme-builder' ) );
        }
        check_admin_referer( SRWF_REGISTRATION_GTB_LAYOUT_NONCE_ACTION, SRWF_REGISTRATION_GTB_LAYOUT_NONCE_NAME );
        $result = srwf_registration_gtb_apply_layout( $form_id );
    }

    $form = class_exists( 'GFAPI' ) && is_callable( array( 'GFAPI', 'get_form' ) ) ? GFAPI::get_form( absint( $form_id ) ) : false;
    echo '<hr><h3>' . esc_html__( 'SRWF Form Presentation Readiness', 'gravity-theme-builder' ) . '</h3>';
    echo '<p class="description">' . esc_html__( 'These are host-owned Gravity Forms Form Layout settings. Opening this page and Check Again are read-only; Apply changes only the listed properties.', 'gravity-theme-builder' ) . '</p>';

    if ( is_wp_error( $result ) ) {
        srwf_registration_gtb_notice( 'error', $result->get_error_message() );
    } elseif ( is_array( $result ) ) {
        if ( ! empty( $result['wrote'] ) ) {
            srwf_registration_gtb_notice( 'success', 'Recommended SRWF Form Layout settings were applied and verified by re-reading the Form Object.' );
        } else {
            srwf_registration_gtb_notice( 'info', 'Form Layout already matched the SRWF destination. No Gravity Forms write was performed.' );
        }
    }

    if ( ! is_array( $form ) ) {
        srwf_registration_gtb_notice( 'error', 'GTB could not read the current Form Object for presentation readiness.' );
        return;
    }

    $readiness = srwf_registration_gtb_layout_readiness( $form );
    $labels = srwf_registration_gtb_layout_labels();
    echo '<p><strong>' . esc_html( $readiness['state'] ) . '</strong></p>';
    echo '<table class="widefat striped"><thead><tr><th>' . esc_html__( 'Property', 'gravity-theme-builder' ) . '</th><th>' . esc_html__( 'Expected', 'gravity-theme-builder' ) . '</th><th>' . esc_html__( 'Current', 'gravity-theme-builder' ) . '</th><th>' . esc_html__( 'Status', 'gravity-theme-builder' ) . '</th></tr></thead><tbody>';
    foreach ( $readiness['properties'] as $property => $state ) {
        echo '<tr><td>' . esc_html( isset( $labels[ $property ] ) ? $labels[ $property ] : $property ) . '</td><td><code>' . esc_html( srwf_registration_gtb_layout_display_value( $state['expected'] ) ) . '</code></td><td><code>' . esc_html( srwf_registration_gtb_layout_display_value( $state['current'] ) ) . '</code></td><td><strong>' . esc_html( $state['state'] ) . '</strong></td></tr>';
    }
    echo '</tbody></table>';

    if ( ! empty( $readiness['field_override_conflicts'] ) ) {
        echo '<h4>' . esc_html__( 'Field-level overrides — ATTENTION REQUIRED', 'gravity-theme-builder' ) . '</h4><ul>';
        foreach ( $readiness['field_override_conflicts'] as $conflict ) {
            echo '<li>' . esc_html( sprintf( 'Field #%d (%s): %s is %s; expected %s or inherited form setting.', $conflict['field_id'], $conflict['field_type'], $conflict['property'], $conflict['current'], $conflict['expected'] ) ) . '</li>';
        }
        echo '</ul><p class="description">' . esc_html__( 'GTB reports these explicit overrides but does not silently rewrite field-level configuration.', 'gravity-theme-builder' ) . '</p>';
    }

    echo '<form method="post">';
    wp_nonce_field( SRWF_REGISTRATION_GTB_LAYOUT_NONCE_ACTION, SRWF_REGISTRATION_GTB_LAYOUT_NONCE_NAME );
    echo '<p><button type="submit" class="button" name="gtb_action" value="apply_layout">' . esc_html__( 'Apply Recommended SRWF Form Layout', 'gravity-theme-builder' ) . '</button></p>';
    echo '<p class="description">' . esc_html__( 'Applies only Label, Description, Validation Message, Sub-label, Validation Summary, and Required Indicator settings. customRequiredIndicator and all unrelated form properties are preserved.', 'gravity-theme-builder' ) . '</p>';
    echo '</form>';
}
