<?php
/** Per-form GTB configuration for SRWF Registration. */
defined( 'ABSPATH' ) || exit;

const SRWF_REGISTRATION_GTB_SETTINGS_VIEW = 'gtb_theme';
const SRWF_REGISTRATION_GTB_CONFIG_KEY = 'gtb_srwf_registration';
const SRWF_REGISTRATION_GTB_CONFIG_SCHEMA = 1;
const SRWF_REGISTRATION_GTB_PROFILE = 'srwf-registration';
const SRWF_REGISTRATION_GTB_CAPABILITY = 'gravityforms_edit_forms';
const SRWF_REGISTRATION_GTB_NONCE_ACTION = 'srwf_registration_gtb_theme_save';
const SRWF_REGISTRATION_GTB_NONCE_NAME = 'srwf_registration_gtb_theme_nonce';

function srwf_registration_gtb_role_definitions() {
    return array(
        'gender' => array( 'label' => 'Gender', 'token' => 'srwf-role-binary-choice', 'types' => array( 'radio' ), 'feature' => 'approved two-card Gender choice presentation' ),
        'graduation_status' => array( 'label' => 'Graduation Status', 'token' => 'srwf-role-binary-choice', 'types' => array( 'radio' ), 'feature' => 'approved two-card Graduation Status presentation when Gravity Forms reveals the field' ),
        'report_card_upload' => array( 'label' => 'Report Card upload', 'token' => 'srwf-role-report-card-upload', 'types' => array( 'fileupload' ), 'feature' => 'approved initial Report Card upload surface' ),
        'section_identity' => array( 'label' => 'Identity Section Break', 'token' => 'srwf-role-section-identity', 'types' => array( 'section' ), 'feature' => 'approved Identity section icon' ),
        'section_contact' => array( 'label' => 'Contact Section Break', 'token' => 'srwf-role-section-contact', 'types' => array( 'section' ), 'feature' => 'approved Contact section icon' ),
        'section_education' => array( 'label' => 'Education Section Break', 'token' => 'srwf-role-section-education', 'types' => array( 'section' ), 'feature' => 'approved Education section icon' ),
        'section_school_documents' => array( 'label' => 'School/Documents Section Break', 'token' => 'srwf-role-section-school-documents', 'types' => array( 'section' ), 'feature' => 'approved School/Documents section icon' ),
        'section_student_photo' => array( 'label' => 'Student Photo Section Break', 'token' => 'srwf-role-section-student-photo', 'types' => array( 'section' ), 'feature' => 'approved Student Photo section icon' ),
    );
}

function srwf_registration_gtb_owned_role_tokens() {
    $tokens = array();
    foreach ( srwf_registration_gtb_role_definitions() as $definition ) {
        $tokens[] = $definition['token'];
    }
    return array_values( array_unique( $tokens ) );
}

function srwf_registration_gtb_class_tokens( $value ) {
    $parts = preg_split( '/\s+/', trim( (string) $value ) );
    $tokens = array();
    foreach ( is_array( $parts ) ? $parts : array() as $part ) {
        if ( '' !== $part && ! in_array( $part, $tokens, true ) ) {
            $tokens[] = $part;
        }
    }
    return $tokens;
}

function srwf_registration_gtb_project_class_tokens( $value, $remove, $add ) {
    $result = array();
    foreach ( srwf_registration_gtb_class_tokens( $value ) as $token ) {
        if ( ! in_array( $token, $remove, true ) ) {
            $result[] = $token;
        }
    }
    foreach ( $add as $token ) {
        if ( '' !== $token && ! in_array( $token, $result, true ) ) {
            $result[] = $token;
        }
    }
    return implode( ' ', $result );
}

function srwf_registration_gtb_field_get( $field, $key ) {
    if ( is_object( $field ) && isset( $field->{$key} ) ) {
        return $field->{$key};
    }
    return is_array( $field ) && array_key_exists( $key, $field ) ? $field[ $key ] : null;
}

function srwf_registration_gtb_field_set( &$field, $key, $value ) {
    if ( is_object( $field ) ) {
        $field->{$key} = $value;
    } elseif ( is_array( $field ) ) {
        $field[ $key ] = $value;
    }
}

function srwf_registration_gtb_field_type( $field ) {
    if ( is_object( $field ) && is_callable( array( $field, 'get_input_type' ) ) ) {
        $input_type = (string) $field->get_input_type();
        if ( '' !== $input_type ) {
            return strtolower( $input_type );
        }
    }
    return strtolower( (string) srwf_registration_gtb_field_get( $field, 'type' ) );
}

function srwf_registration_gtb_field_id( $field ) {
    return absint( srwf_registration_gtb_field_get( $field, 'id' ) );
}

function srwf_registration_gtb_field_label( $field ) {
    $label = trim( (string) srwf_registration_gtb_field_get( $field, 'label' ) );
    return '' === $label ? '(Untitled field)' : $label;
}

function srwf_registration_gtb_find_field( $form, $field_id ) {
    foreach ( isset( $form['fields'] ) && is_array( $form['fields'] ) ? $form['fields'] : array() as $field ) {
        if ( srwf_registration_gtb_field_id( $field ) === (int) $field_id ) {
            return $field;
        }
    }
    return null;
}

function srwf_registration_gtb_default_config() {
    $roles = array();
    foreach ( srwf_registration_gtb_role_definitions() as $key => $unused ) {
        $roles[ $key ] = 0;
    }
    return array( 'schema' => SRWF_REGISTRATION_GTB_CONFIG_SCHEMA, 'profile' => SRWF_REGISTRATION_GTB_PROFILE, 'enabled' => false, 'roles' => $roles );
}

function srwf_registration_gtb_get_config( $form ) {
    $config = srwf_registration_gtb_default_config();
    $stored = isset( $form[ SRWF_REGISTRATION_GTB_CONFIG_KEY ] ) && is_array( $form[ SRWF_REGISTRATION_GTB_CONFIG_KEY ] ) ? $form[ SRWF_REGISTRATION_GTB_CONFIG_KEY ] : array();
    $config['schema'] = isset( $stored['schema'] ) ? absint( $stored['schema'] ) : $config['schema'];
    $config['profile'] = isset( $stored['profile'] ) ? sanitize_key( (string) $stored['profile'] ) : $config['profile'];
    $config['enabled'] = ! empty( $stored['enabled'] );
    $stored_roles = isset( $stored['roles'] ) && is_array( $stored['roles'] ) ? $stored['roles'] : array();
    foreach ( $config['roles'] as $key => $unused ) {
        $config['roles'][ $key ] = isset( $stored_roles[ $key ] ) ? absint( $stored_roles[ $key ] ) : 0;
    }
    return $config;
}

function srwf_registration_gtb_config_from_request( $request ) {
    $config = srwf_registration_gtb_default_config();
    $config['enabled'] = ! empty( $request['gtb_enabled'] );
    $roles = isset( $request['gtb_roles'] ) && is_array( $request['gtb_roles'] ) ? $request['gtb_roles'] : array();
    foreach ( $config['roles'] as $key => $unused ) {
        $config['roles'][ $key ] = isset( $roles[ $key ] ) ? absint( $roles[ $key ] ) : 0;
    }
    return $config;
}

function srwf_registration_gtb_type_label( $types ) {
    $labels = array( 'radio' => 'a Radio field', 'fileupload' => 'a File Upload field', 'section' => 'a Section Break field' );
    return implode( ' or ', array_map( function ( $type ) use ( $labels ) { return isset( $labels[ $type ] ) ? $labels[ $type ] : $type; }, $types ) );
}

function srwf_registration_gtb_validate_config( $form, $config ) {
    $errors = array();
    if ( SRWF_REGISTRATION_GTB_PROFILE !== $config['profile'] || SRWF_REGISTRATION_GTB_CONFIG_SCHEMA !== $config['schema'] ) {
        return array( 'The requested GTB profile or configuration schema is not supported.' );
    }
    $used_ids = array();
    foreach ( srwf_registration_gtb_role_definitions() as $key => $definition ) {
        $field_id = isset( $config['roles'][ $key ] ) ? absint( $config['roles'][ $key ] ) : 0;
        if ( 0 === $field_id ) {
            continue;
        }
        if ( isset( $used_ids[ $field_id ] ) ) {
            $errors[] = sprintf( 'The same Gravity Forms field cannot be used for both "%s" and "%s".', $used_ids[ $field_id ], $definition['label'] );
            continue;
        }
        $used_ids[ $field_id ] = $definition['label'];
        $field = srwf_registration_gtb_find_field( $form, $field_id );
        if ( null === $field ) {
            $errors[] = sprintf( '%s points to a field that no longer exists in this form.', $definition['label'] );
            continue;
        }
        $type = srwf_registration_gtb_field_type( $field );
        if ( ! in_array( $type, $definition['types'], true ) ) {
            $errors[] = sprintf( '%s requires %s, but the selected field is type "%s".', $definition['label'], srwf_registration_gtb_type_label( $definition['types'] ), '' === $type ? 'unknown' : $type );
        }
    }
    return $errors;
}

function srwf_registration_gtb_clone_form_for_projection( $form ) {
    $copy = $form;
    if ( isset( $form['fields'] ) && is_array( $form['fields'] ) ) {
        $copy['fields'] = array();
        foreach ( $form['fields'] as $field ) {
            $copy['fields'][] = is_object( $field ) ? clone $field : $field;
        }
    }
    return $copy;
}

function srwf_registration_gtb_project_config( $form, $config ) {
    $next = srwf_registration_gtb_clone_form_for_projection( $form );
    $next[ SRWF_REGISTRATION_GTB_CONFIG_KEY ] = $config;
    $next['cssClass'] = srwf_registration_gtb_project_class_tokens(
        isset( $form['cssClass'] ) ? $form['cssClass'] : '',
        array( SRWF_REGISTRATION_THEME_CLASS ),
        $config['enabled'] ? array( SRWF_REGISTRATION_THEME_CLASS ) : array()
    );

    $desired_by_field = array();
    foreach ( srwf_registration_gtb_role_definitions() as $key => $definition ) {
        $field_id = isset( $config['roles'][ $key ] ) ? absint( $config['roles'][ $key ] ) : 0;
        if ( $field_id ) {
            $desired_by_field[ $field_id ] = isset( $desired_by_field[ $field_id ] ) ? $desired_by_field[ $field_id ] : array();
            if ( ! in_array( $definition['token'], $desired_by_field[ $field_id ], true ) ) {
                $desired_by_field[ $field_id ][] = $definition['token'];
            }
        }
    }

    $owned = srwf_registration_gtb_owned_role_tokens();
    if ( isset( $next['fields'] ) && is_array( $next['fields'] ) ) {
        foreach ( $next['fields'] as &$field ) {
            $field_id = srwf_registration_gtb_field_id( $field );
            srwf_registration_gtb_field_set(
                $field,
                'cssClass',
                srwf_registration_gtb_project_class_tokens(
                    srwf_registration_gtb_field_get( $field, 'cssClass' ),
                    $owned,
                    isset( $desired_by_field[ $field_id ] ) ? $desired_by_field[ $field_id ] : array()
                )
            );
        }
        unset( $field );
    }
    return $next;
}

function srwf_registration_gtb_save_config( $form, $config ) {
    $errors = srwf_registration_gtb_validate_config( $form, $config );
    if ( $errors ) {
        return new WP_Error( 'gtb_invalid_configuration', implode( ' ', $errors ) );
    }
    if ( ! class_exists( 'GFAPI' ) || ! is_callable( array( 'GFAPI', 'update_form' ) ) ) {
        return new WP_Error( 'gtb_gravity_forms_unavailable', 'Gravity Forms is not available to save this configuration.' );
    }
    $result = GFAPI::update_form( srwf_registration_gtb_project_config( $form, $config ) );
    if ( is_wp_error( $result ) ) {
        return $result;
    }
    return true === $result ? true : new WP_Error( 'gtb_form_update_failed', 'Gravity Forms did not confirm the form update.' );
}

function srwf_registration_gtb_field_has_token( $field, $token ) {
    return in_array( $token, srwf_registration_gtb_class_tokens( srwf_registration_gtb_field_get( $field, 'cssClass' ) ), true );
}

/** Read-only draft helper; semantic identity is never inferred from labels, IDs or DOM position. */
function srwf_registration_gtb_recommended_draft( $form, $config ) {
    $draft = $config;
    $draft['enabled'] = true;
    $notes = array();
    foreach ( srwf_registration_gtb_role_definitions() as $key => $definition ) {
        if ( in_array( $key, array( 'gender', 'graduation_status' ), true ) || ! empty( $draft['roles'][ $key ] ) ) {
            continue;
        }
        $matches = array();
        foreach ( isset( $form['fields'] ) && is_array( $form['fields'] ) ? $form['fields'] : array() as $field ) {
            if ( in_array( srwf_registration_gtb_field_type( $field ), $definition['types'], true ) && srwf_registration_gtb_field_has_token( $field, $definition['token'] ) ) {
                $matches[] = srwf_registration_gtb_field_id( $field );
            }
        }
        $matches = array_values( array_unique( array_filter( $matches ) ) );
        if ( 1 === count( $matches ) ) {
            $draft['roles'][ $key ] = $matches[0];
        } elseif ( count( $matches ) > 1 ) {
            $notes[] = sprintf( '%s has more than one existing GTB token candidate, so no automatic choice was made.', $definition['label'] );
        }
    }
    if ( empty( $draft['roles']['gender'] ) || empty( $draft['roles']['graduation_status'] ) ) {
        $notes[] = 'Gender and Graduation Status are intentionally not inferred from the shared binary-choice token. Select the two Radio fields explicitly.';
    }
    return array( 'config' => $draft, 'notes' => $notes );
}

function srwf_registration_gtb_readiness( $form ) {
    $config = srwf_registration_gtb_get_config( $form );
    $roles = array();
    $has_invalid = (bool) srwf_registration_gtb_validate_config( $form, $config );
    $has_missing = false;
    $has_projection_gap = false;
    $expected_by_field = array();

    foreach ( srwf_registration_gtb_role_definitions() as $key => $definition ) {
        $field_id = isset( $config['roles'][ $key ] ) ? absint( $config['roles'][ $key ] ) : 0;
        if ( ! $field_id ) {
            $has_missing = true;
            $roles[ $key ] = array( 'state' => 'NEEDS SETUP', 'message' => sprintf( 'No field is selected. %s is not under GTB semantic control.', $definition['feature'] ), 'field_id' => 0 );
            continue;
        }
        $field = srwf_registration_gtb_find_field( $form, $field_id );
        if ( null === $field ) {
            $has_invalid = true;
            $roles[ $key ] = array( 'state' => 'ATTENTION REQUIRED', 'message' => 'The saved field reference no longer exists. Select a replacement and save.', 'field_id' => $field_id );
            continue;
        }
        if ( ! in_array( srwf_registration_gtb_field_type( $field ), $definition['types'], true ) ) {
            $has_invalid = true;
            $roles[ $key ] = array( 'state' => 'ATTENTION REQUIRED', 'message' => sprintf( 'The saved field has an incompatible type. Select %s and save.', srwf_registration_gtb_type_label( $definition['types'] ) ), 'field_id' => $field_id );
            continue;
        }
        if ( ! srwf_registration_gtb_field_has_token( $field, $definition['token'] ) ) {
            $has_projection_gap = true;
            $roles[ $key ] = array( 'state' => 'ATTENTION REQUIRED', 'message' => 'The mapping is valid, but its GTB presentation token is not currently projected. Save configuration to repair it.', 'field_id' => $field_id );
        } else {
            $roles[ $key ] = array( 'state' => 'READY', 'message' => 'Mapped to a compatible field and the GTB presentation token is projected.', 'field_id' => $field_id );
        }
        $expected_by_field[ $field_id ] = isset( $expected_by_field[ $field_id ] ) ? $expected_by_field[ $field_id ] : array();
        if ( ! in_array( $definition['token'], $expected_by_field[ $field_id ], true ) ) {
            $expected_by_field[ $field_id ][] = $definition['token'];
        }
    }

    $owned = srwf_registration_gtb_owned_role_tokens();
    foreach ( isset( $form['fields'] ) && is_array( $form['fields'] ) ? $form['fields'] : array() as $field ) {
        $field_id = srwf_registration_gtb_field_id( $field );
        $actual = array_values( array_intersect( srwf_registration_gtb_class_tokens( srwf_registration_gtb_field_get( $field, 'cssClass' ) ), $owned ) );
        $expected = isset( $expected_by_field[ $field_id ] ) ? $expected_by_field[ $field_id ] : array();
        sort( $actual );
        sort( $expected );
        if ( $actual !== $expected ) {
            $has_projection_gap = true;
        }
    }

    $activation_projected = srwf_registration_theme_is_target_form( $form );
    if ( ! $config['enabled'] && ! $activation_projected ) {
        return array( 'state' => 'DISABLED', 'message' => 'SRWF Registration is disabled for this form. Gravity Forms continues to render the form without GTB Registration presentation.', 'roles' => $roles );
    }
    if ( $config['enabled'] !== $activation_projected || $has_invalid || $has_projection_gap ) {
        return array( 'state' => 'ATTENTION REQUIRED', 'message' => 'The saved GTB configuration and current Gravity Forms class projection do not fully agree, or a saved mapping is invalid.', 'roles' => $roles );
    }
    if ( $has_missing ) {
        return array( 'state' => 'NEEDS SETUP', 'message' => 'SRWF Registration is enabled, but one or more required semantic presentation roles still need an explicit field selection.', 'roles' => $roles );
    }
    return array( 'state' => 'READY', 'message' => 'All required SRWF Registration presentation roles are valid and their GTB-owned tokens are projected.', 'roles' => $roles );
}

function srwf_registration_gtb_settings_menu( $menu_items ) {
    foreach ( $menu_items as $item ) {
        if ( isset( $item['name'] ) && SRWF_REGISTRATION_GTB_SETTINGS_VIEW === $item['name'] ) {
            return $menu_items;
        }
    }
    $menu_items[] = array( 'name' => SRWF_REGISTRATION_GTB_SETTINGS_VIEW, 'label' => 'GTB Theme', 'icon' => 'dashicons-admin-appearance dashicons' );
    return $menu_items;
}
add_filter( 'gform_form_settings_menu', 'srwf_registration_gtb_settings_menu' );

function srwf_registration_gtb_requested_form_id() {
    return isset( $_GET['id'] ) ? absint( wp_unslash( $_GET['id'] ) ) : 0; // phpcs:ignore WordPress.Security.NonceVerification.Recommended
}

function srwf_registration_gtb_render_role_row( $form, $key, $selected_id, $role_state ) {
    $definition = srwf_registration_gtb_role_definitions()[ $key ];
    $select_id = 'gtb-role-' . str_replace( '_', '-', $key );
    echo '<tr><th scope="row"><label for="' . esc_attr( $select_id ) . '">' . esc_html( $definition['label'] ) . '</label></th><td>';
    echo '<select class="regular-text" id="' . esc_attr( $select_id ) . '" name="gtb_roles[' . esc_attr( $key ) . ']">';
    echo '<option value="0">' . esc_html__( '— Select a compatible field —', 'gravity-theme-builder' ) . '</option>';
    foreach ( isset( $form['fields'] ) && is_array( $form['fields'] ) ? $form['fields'] : array() as $field ) {
        if ( ! in_array( srwf_registration_gtb_field_type( $field ), $definition['types'], true ) ) {
            continue;
        }
        $field_id = srwf_registration_gtb_field_id( $field );
        echo '<option value="' . esc_attr( (string) $field_id ) . '"' . selected( $selected_id, $field_id, false ) . '>' . esc_html( sprintf( '#%d — %s', $field_id, srwf_registration_gtb_field_label( $field ) ) ) . '</option>';
    }
    echo '</select>';
    echo '<p class="description"><strong>' . esc_html( $role_state['state'] ) . '.</strong> ' . esc_html( $definition['feature'] ) . '. ' . esc_html( $role_state['message'] ) . '</p>';
    echo '<p class="description">' . esc_html( 'Compatible type: ' . srwf_registration_gtb_type_label( $definition['types'] ) . '. Technical token: ' . $definition['token'] ) . '</p>';
    echo '</td></tr>';
}

function srwf_registration_gtb_notice( $class, $message ) {
    echo '<div class="notice notice-' . esc_attr( $class ) . ' inline"><p>' . esc_html( $message ) . '</p></div>';
}

function srwf_registration_gtb_settings_page() {
    if ( ! current_user_can( SRWF_REGISTRATION_GTB_CAPABILITY ) ) {
        wp_die( esc_html__( 'You do not have permission to edit this Gravity Forms form.', 'gravity-theme-builder' ) );
    }
    $form_id = srwf_registration_gtb_requested_form_id();
    $form = $form_id && class_exists( 'GFAPI' ) ? GFAPI::get_form( $form_id ) : false;
    GFFormSettings::page_header();
    if ( ! is_array( $form ) ) {
        srwf_registration_gtb_notice( 'error', 'GTB could not load the current Gravity Forms form.' );
        GFFormSettings::page_footer();
        return;
    }

    $display_config = srwf_registration_gtb_get_config( $form );
    $errors = array();
    $notes = array();
    $saved = false;
    $action = isset( $_POST['gtb_action'] ) ? sanitize_key( wp_unslash( $_POST['gtb_action'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Missing

    if ( 'save' === $action ) {
        check_admin_referer( SRWF_REGISTRATION_GTB_NONCE_ACTION, SRWF_REGISTRATION_GTB_NONCE_NAME );
        $request = wp_unslash( $_POST );
        $requested = srwf_registration_gtb_config_from_request( is_array( $request ) ? $request : array() );
        $errors = srwf_registration_gtb_validate_config( $form, $requested );
        $display_config = $requested;
        if ( ! $errors ) {
            $result = srwf_registration_gtb_save_config( $form, $requested );
            if ( is_wp_error( $result ) ) {
                $errors[] = $result->get_error_message();
            } else {
                $saved = true;
                $form = srwf_registration_gtb_project_config( $form, $requested );
                $fresh = GFAPI::get_form( $form_id );
                if ( is_array( $fresh ) ) {
                    $form = $fresh;
                }
                $display_config = srwf_registration_gtb_get_config( $form );
            }
        }
    } elseif ( 'recommend' === $action ) {
        check_admin_referer( SRWF_REGISTRATION_GTB_NONCE_ACTION, SRWF_REGISTRATION_GTB_NONCE_NAME );
        $recommendation = srwf_registration_gtb_recommended_draft( $form, $display_config );
        $display_config = $recommendation['config'];
        $notes = $recommendation['notes'];
    }

    $readiness = srwf_registration_gtb_readiness( $form );
    $current_config = srwf_registration_gtb_get_config( $form );
    if ( $saved ) {
        srwf_registration_gtb_notice( 'success', 'GTB Theme configuration was saved and GTB-owned presentation tokens were projected.' );
    }
    if ( 'recommend' === $action ) {
        srwf_registration_gtb_notice( 'info', 'Recommended SRWF configuration is loaded as an unsaved draft. Current status and current profile still describe the saved form until Save GTB Configuration succeeds.' );
    }
    if ( isset( $_GET['gtb_check'] ) && '1' === (string) wp_unslash( $_GET['gtb_check'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
        srwf_registration_gtb_notice( 'info', 'Check Again completed. GTB re-read the current form and made no configuration changes.' );
    }
    foreach ( $errors as $error ) {
        srwf_registration_gtb_notice( 'error', $error );
    }
    foreach ( $notes as $note ) {
        srwf_registration_gtb_notice( 'warning', $note );
    }

    echo '<h2>' . esc_html__( 'GTB Theme', 'gravity-theme-builder' ) . '</h2>';
    echo '<p>' . esc_html__( 'GTB controls presentation only. Gravity Forms continues to own fields, behavior, validation, conditional logic, submission, accessibility semantics and data.', 'gravity-theme-builder' ) . '</p>';
    echo '<h3>' . esc_html__( 'Current status', 'gravity-theme-builder' ) . '</h3>';
    echo '<p><strong>' . esc_html( $readiness['state'] ) . '</strong> — ' . esc_html( $readiness['message'] ) . '</p>';
    echo '<p><strong>' . esc_html__( 'Current saved theme profile:', 'gravity-theme-builder' ) . '</strong> ' . esc_html( 'SRWF Registration / ' . ( $current_config['enabled'] ? 'Enabled' : 'Disabled' ) ) . '</p>';

    echo '<form method="post">';
    wp_nonce_field( SRWF_REGISTRATION_GTB_NONCE_ACTION, SRWF_REGISTRATION_GTB_NONCE_NAME );
    echo '<h3>' . esc_html__( 'Theme', 'gravity-theme-builder' ) . '</h3>';
    echo '<p><label><input type="checkbox" name="gtb_enabled" value="1"' . checked( true, $display_config['enabled'], false ) . '> ' . esc_html__( 'Enable SRWF Registration presentation for this form', 'gravity-theme-builder' ) . '</label></p>';
    echo '<p class="description">' . esc_html__( 'GTB projects the activation token only when you save. Rendering this page never rewrites the form.', 'gravity-theme-builder' ) . '</p>';
    echo '<h3>' . esc_html__( 'Role mappings', 'gravity-theme-builder' ) . '</h3><table class="form-table" role="presentation"><tbody>';
    foreach ( srwf_registration_gtb_role_definitions() as $key => $unused ) {
        $role_state = isset( $readiness['roles'][ $key ] ) ? $readiness['roles'][ $key ] : array( 'state' => 'NEEDS SETUP', 'message' => '', 'field_id' => 0 );
        srwf_registration_gtb_render_role_row( $form, $key, $display_config['roles'][ $key ], $role_state );
    }
    echo '</tbody></table><p>';
    echo '<button type="submit" class="button button-primary" name="gtb_action" value="save">' . esc_html__( 'Save GTB Configuration', 'gravity-theme-builder' ) . '</button> ';
    echo '<button type="submit" class="button" name="gtb_action" value="recommend">' . esc_html__( 'Apply Recommended SRWF Configuration', 'gravity-theme-builder' ) . '</button> ';
    $check_url = add_query_arg( array( 'page' => 'gf_edit_forms', 'view' => 'settings', 'subview' => SRWF_REGISTRATION_GTB_SETTINGS_VIEW, 'id' => $form_id, 'gtb_check' => '1' ), admin_url( 'admin.php' ) );
    echo '<a class="button" href="' . esc_url( $check_url ) . '">' . esc_html__( 'Check Again', 'gravity-theme-builder' ) . '</a></p>';
    echo '<p class="description">' . esc_html__( 'Recommended setup only prepares mappings that existing GTB semantic tokens prove unambiguously. Shared binary-choice roles are never guessed. Nothing changes in Gravity Forms until Save GTB Configuration succeeds.', 'gravity-theme-builder' ) . '</p>';
    echo '</form>';
    GFFormSettings::page_footer();
}
add_action( 'gform_form_settings_page_' . SRWF_REGISTRATION_GTB_SETTINGS_VIEW, 'srwf_registration_gtb_settings_page' );
