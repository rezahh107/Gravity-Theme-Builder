<?php
$hooks = array();
$updates = array();
$allow_edit_forms = true;
define( 'ABSPATH', __DIR__ );
define( 'SRWF_REGISTRATION_THEME_CLASS', 'srwf-registration-theme' );

function add_filter( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'filter', $hook, $callback, $priority, $args ); }
function add_action( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'action', $hook, $callback, $priority, $args ); }
function absint( $value ) { return max( 0, (int) $value ); }
function sanitize_key( $value ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/', '', (string) $value ) ); }
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function wp_unslash( $value ) { return $value; }
function current_user_can( $capability ) { global $allow_edit_forms; return $allow_edit_forms && $capability === 'gravityforms_edit_forms'; }
function wp_die( $message ) { throw new RuntimeException( $message ); }
function esc_html__( $text, $domain = null ) { return $text; }
function esc_html( $text ) { return htmlspecialchars( (string) $text, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $text ) { return htmlspecialchars( (string) $text, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $text ) { return (string) $text; }
function selected( $selected, $current, $echo = true ) { $out = ( (string) $selected === (string) $current ) ? ' selected="selected"' : ''; if ( $echo ) { echo $out; } return $out; }
function checked( $checked, $current, $echo = true ) { $out = ( (bool) $checked === (bool) $current ) ? ' checked="checked"' : ''; if ( $echo ) { echo $out; } return $out; }
function wp_nonce_field( $action, $name ) { echo '<input type="hidden" name="' . $name . '" value="nonce">'; }
function check_admin_referer( $action, $name ) { if ( ! isset( $_POST[ $name ] ) || $_POST[ $name ] !== 'nonce' ) { throw new RuntimeException( 'invalid nonce' ); } return true; }
function add_query_arg( $args, $url ) { return $url . '?' . http_build_query( $args ); }
function admin_url( $path = '' ) { return 'https://example.test/wp-admin/' . $path; }
class WP_Error {
    private $code;
    private $message;
    public function __construct( $code, $message ) { $this->code = $code; $this->message = $message; }
    public function get_error_message() { return $this->message; }
}
class GFAPI {
    public static $forms = array();
    public static $update_result = true;
    public static $update_calls = 0;
    public static function update_form( $form ) {
        global $updates;
        self::$update_calls++;
        $updates[] = $form;
        if ( true === self::$update_result ) {
            self::$forms[ $form['id'] ] = $form;
        }
        return self::$update_result;
    }
    public static function get_form( $id ) { return isset( self::$forms[ $id ] ) ? self::$forms[ $id ] : false; }
}
class GFFormSettings {
    public static function page_header() { echo '<div class="gf-page">'; }
    public static function page_footer() { echo '</div>'; }
}
class TestField {
    public $id;
    public $type;
    public $label;
    public $cssClass;
    public function __construct( $id, $type, $label, $css = '' ) { $this->id = $id; $this->type = $type; $this->label = $label; $this->cssClass = $css; }
    public function get_input_type() { return $this->type; }
}
function srwf_registration_theme_is_target_form( $form ) {
    return in_array( SRWF_REGISTRATION_THEME_CLASS, preg_split( '/\s+/', trim( isset( $form['cssClass'] ) ? $form['cssClass'] : '' ) ), true );
}
function check( $condition, $message ) { if ( ! $condition ) { fwrite( STDERR, "FAIL: $message\n" ); exit( 1 ); } }
function field_css( $form, $id ) { foreach ( $form['fields'] as $field ) { if ( $field->id === $id ) { return $field->cssClass; } } return null; }

require __DIR__ . '/../src/srwf-registration-settings.php';

check( array_filter( $hooks, fn( $h ) => $h[0] === 'filter' && $h[1] === 'gform_form_settings_menu' && $h[2] === 'srwf_registration_gtb_settings_menu' ) !== array(), 'GTB Theme form settings menu hook missing' );
check( array_filter( $hooks, fn( $h ) => $h[0] === 'action' && $h[1] === 'gform_form_settings_page_gtb_theme' && $h[2] === 'srwf_registration_gtb_settings_page' ) !== array(), 'GTB Theme form settings page hook missing' );
check( array_filter( $hooks, fn( $h ) => $h[1] === 'admin_menu' ) === array(), 'top-level admin menu hook must not be registered' );

$form = array(
    'id' => 91,
    'cssClass' => "host-one  host-two",
    'fields' => array(
        new TestField( 6, 'radio', 'Any gender label', 'foreign-a' ),
        new TestField( 17, 'radio', 'Any graduation label', 'foreign-b' ),
        new TestField( 22, 'fileupload', 'Any upload label', 'foreign-c' ),
        new TestField( 31, 'section', 'Any identity label', 'foreign-d' ),
        new TestField( 32, 'section', 'Any contact label', 'foreign-e' ),
        new TestField( 33, 'section', 'Any education label', 'foreign-f' ),
        new TestField( 34, 'section', 'Any school label', 'foreign-g' ),
        new TestField( 35, 'section', 'Any photo label', 'foreign-h' ),
        new TestField( 99, 'radio', 'Unrelated radio', 'leave-me' ),
    ),
);
$config = srwf_registration_gtb_default_config();
$config['enabled'] = true;
$config['roles'] = array(
    'gender' => 6,
    'graduation_status' => 17,
    'report_card_upload' => 22,
    'section_identity' => 31,
    'section_contact' => 32,
    'section_education' => 33,
    'section_school_documents' => 34,
    'section_student_photo' => 35,
);

check( srwf_registration_gtb_validate_config( $form, $config ) === array(), 'valid complete config rejected' );
$projected = srwf_registration_gtb_project_config( $form, $config );
check( $form['cssClass'] === 'host-one  host-two', 'projection mutated original form object' );
check( field_css( $form, 6 ) === 'foreign-a', 'projection mutated original field object' );
check( $projected['cssClass'] === 'host-one host-two srwf-registration-theme', 'activation token projection wrong or foreign form classes lost' );
check( field_css( $projected, 6 ) === 'foreign-a srwf-role-binary-choice', 'Gender token projection failed' );
check( field_css( $projected, 17 ) === 'foreign-b srwf-role-binary-choice', 'Graduation token projection failed' );
check( field_css( $projected, 22 ) === 'foreign-c srwf-role-report-card-upload', 'Report Card token projection failed' );
check( field_css( $projected, 31 ) === 'foreign-d srwf-role-section-identity', 'Identity section token projection failed' );
check( field_css( $projected, 32 ) === 'foreign-e srwf-role-section-contact', 'Contact section token projection failed' );
check( field_css( $projected, 33 ) === 'foreign-f srwf-role-section-education', 'Education section token projection failed' );
check( field_css( $projected, 34 ) === 'foreign-g srwf-role-section-school-documents', 'School/Documents section token projection failed' );
check( field_css( $projected, 35 ) === 'foreign-h srwf-role-section-student-photo', 'Student Photo section token projection failed' );
check( field_css( $projected, 99 ) === 'leave-me', 'unrelated field class changed' );

$twice = srwf_registration_gtb_project_config( $projected, $config );
check( $twice['cssClass'] === $projected['cssClass'], 'repeated activation projection not idempotent' );
foreach ( array( 6, 17, 22, 31, 32, 33, 34, 35, 99 ) as $id ) {
    check( field_css( $twice, $id ) === field_css( $projected, $id ), "repeated field projection not idempotent for $id" );
}

$disabled = $config;
$disabled['enabled'] = false;
$disabled_projected = srwf_registration_gtb_project_config( $projected, $disabled );
check( $disabled_projected['cssClass'] === 'host-one host-two', 'disabling did not remove exactly the activation token' );
check( field_css( $disabled_projected, 6 ) === 'foreign-a srwf-role-binary-choice', 'disabling unexpectedly destroyed configured role token' );

$remap = $config;
$remap['roles']['gender'] = 99;
$remapped = srwf_registration_gtb_project_config( $projected, $remap );
check( field_css( $remapped, 6 ) === 'foreign-a', 'stale Gender token not removed from old field' );
check( field_css( $remapped, 99 ) === 'leave-me srwf-role-binary-choice', 'new Gender field did not receive token or foreign class lost' );
check( field_css( $remapped, 17 ) === 'foreign-b srwf-role-binary-choice', 'shared binary token removed from active Graduation mapping' );

$missing = $config;
$missing['roles']['gender'] = 404;
check( srwf_registration_gtb_validate_config( $form, $missing ) !== array(), 'missing mapped field accepted' );
$wrong = $config;
$wrong['roles']['gender'] = 22;
check( srwf_registration_gtb_validate_config( $form, $wrong ) !== array(), 'wrong field type accepted for binary role' );
$wrong_section = $config;
$wrong_section['roles']['section_identity'] = 6;
check( srwf_registration_gtb_validate_config( $form, $wrong_section ) !== array(), 'non-section accepted for section role' );
$duplicate = $config;
$duplicate['roles']['graduation_status'] = 6;
check( srwf_registration_gtb_validate_config( $form, $duplicate ) !== array(), 'duplicate semantic mapping accepted' );
GFAPI::$update_calls = 0;
$result = srwf_registration_gtb_save_config( $form, $wrong );
check( is_wp_error( $result ), 'invalid save did not fail closed' );
check( GFAPI::$update_calls === 0, 'invalid save mutated Gravity Forms' );

GFAPI::$update_result = true;
GFAPI::$update_calls = 0;
$result = srwf_registration_gtb_save_config( $form, $config );
check( true === $result, 'valid save failed' );
check( GFAPI::$update_calls === 1, 'valid save did not use exactly one Gravity Forms update' );
$saved = GFAPI::$forms[91];
check( $saved[ SRWF_REGISTRATION_GTB_CONFIG_KEY ]['roles']['gender'] === 6, 'bounded per-form config not persisted with form' );
check( field_css( $saved, 6 ) === 'foreign-a srwf-role-binary-choice', 'saved form missing projected role token' );

GFAPI::$update_result = new WP_Error( 'host_failure', 'host failed' );
$before = $form;
$result = srwf_registration_gtb_save_config( $form, $config );
check( is_wp_error( $result ) && $result->get_error_message() === 'host failed', 'host update failure not surfaced' );
check( $form['cssClass'] === $before['cssClass'] && field_css( $form, 6 ) === field_css( $before, 6 ), 'host update failure mutated input form' );
GFAPI::$update_result = true;

$ready = srwf_registration_gtb_readiness( $saved );
check( $ready['state'] === 'READY', 'complete projected config not READY' );
$partial_config = $config;
$partial_config['roles']['section_student_photo'] = 0;
$partial = srwf_registration_gtb_project_config( $form, $partial_config );
check( srwf_registration_gtb_readiness( $partial )['state'] === 'NEEDS SETUP', 'missing required role not NEEDS SETUP' );
$disabled_state = srwf_registration_gtb_project_config( $form, $disabled );
check( srwf_registration_gtb_readiness( $disabled_state )['state'] === 'DISABLED', 'disabled theme not DISABLED' );
$drift = $saved;
$drift['cssClass'] = 'host-one host-two';
check( srwf_registration_gtb_readiness( $drift )['state'] === 'ATTENTION REQUIRED', 'activation projection drift not ATTENTION REQUIRED' );
$stale = $saved;
foreach ( $stale['fields'] as $field ) { if ( $field->id === 99 ) { $field->cssClass .= ' srwf-role-report-card-upload'; } }
check( srwf_registration_gtb_readiness( $stale )['state'] === 'ATTENTION REQUIRED', 'stale owned role token not detected as projection drift' );

$renamed = $saved;
foreach ( $renamed['fields'] as $field ) { $field->label = 'Completely changed label ' . $field->id; }
check( srwf_registration_gtb_get_config( $renamed )['roles'] === $config['roles'], 'field label change altered semantic mapping' );

$legacy = $form;
foreach ( $legacy['fields'] as $field ) {
    if ( $field->id === 22 ) { $field->cssClass .= ' srwf-role-report-card-upload'; }
    if ( $field->id === 31 ) { $field->cssClass .= ' srwf-role-section-identity'; }
}
$recommended = srwf_registration_gtb_recommended_draft( $legacy, srwf_registration_gtb_default_config() );
check( $recommended['config']['enabled'] === true, 'recommended draft did not enable SRWF' );
check( $recommended['config']['roles']['report_card_upload'] === 22, 'unique Report Card token not adopted into draft' );
check( $recommended['config']['roles']['section_identity'] === 31, 'unique section token not adopted into draft' );
check( $recommended['config']['roles']['gender'] === 0 && $recommended['config']['roles']['graduation_status'] === 0, 'shared binary roles were guessed' );
check( count( $recommended['changes'] ) >= 3, 'recommended draft did not report proposed changes' );

GFAPI::$update_calls = 0;
srwf_registration_gtb_readiness( $saved );
srwf_registration_gtb_recommended_draft( $legacy, srwf_registration_gtb_default_config() );
check( GFAPI::$update_calls === 0, 'read-only verification/recommendation mutated host form' );

GFAPI::$forms[91] = $saved;
GFAPI::$update_calls = 0;
$allow_edit_forms = false;
$_GET = array( 'id' => '91' );
$_POST = array( 'gtb_action' => 'save', SRWF_REGISTRATION_GTB_NONCE_NAME => 'nonce' );
try {
    ob_start();
    srwf_registration_gtb_settings_page();
    ob_end_clean();
    check( false, 'capability failure did not stop settings page' );
} catch ( RuntimeException $exception ) {
    if ( ob_get_level() ) { ob_end_clean(); }
    check( strpos( $exception->getMessage(), 'permission' ) !== false, 'capability failure message changed' );
}
check( GFAPI::$update_calls === 0, 'capability failure mutated Gravity Forms' );
$allow_edit_forms = true;

GFAPI::$update_calls = 0;
$_GET = array( 'id' => '91' );
$_POST = array( 'gtb_action' => 'save', SRWF_REGISTRATION_GTB_NONCE_NAME => 'bad' );
try {
    ob_start();
    srwf_registration_gtb_settings_page();
    ob_end_clean();
    check( false, 'nonce failure did not stop Save' );
} catch ( RuntimeException $exception ) {
    if ( ob_get_level() ) { ob_end_clean(); }
    check( $exception->getMessage() === 'invalid nonce', 'nonce failure path changed' );
}
check( GFAPI::$update_calls === 0, 'nonce failure mutated Gravity Forms' );

GFAPI::$forms[91] = $saved;
GFAPI::$update_calls = 0;
$_GET = array( 'id' => '91' );
$_POST = array();
ob_start();
srwf_registration_gtb_settings_page();
$page = ob_get_clean();
check( GFAPI::$update_calls === 0, 'opening GTB settings page mutated configuration' );
check( strpos( $page, 'GTB Theme' ) !== false && strpos( $page, 'READY' ) !== false, 'settings page did not render status surface' );

GFAPI::$update_calls = 0;
$_GET = array( 'id' => '91', 'gtb_check' => '1' );
$_POST = array();
ob_start();
srwf_registration_gtb_settings_page();
$check_page = ob_get_clean();
check( GFAPI::$update_calls === 0, 'Check Again mutated configuration' );
check( strpos( $check_page, 'made no configuration changes' ) !== false, 'Check Again did not explain read-only behavior' );

GFAPI::$forms[91] = $legacy;
GFAPI::$update_calls = 0;
$_GET = array( 'id' => '91' );
$_POST = array( 'gtb_action' => 'recommend', SRWF_REGISTRATION_GTB_NONCE_NAME => 'nonce' );
ob_start();
srwf_registration_gtb_settings_page();
$recommend_page = ob_get_clean();
check( GFAPI::$update_calls === 0, 'recommended setup draft mutated Gravity Forms before Save' );
check( strpos( $recommend_page, 'Nothing changes in Gravity Forms until Save GTB Configuration succeeds.' ) !== false, 'recommended setup did not explain deferred mutation' );
check( strpos( $recommend_page, 'Proposal:' ) !== false, 'recommended setup did not report its proposed changes' );

GFAPI::$update_calls = 0;
$_POST = array(
    'gtb_action' => 'save',
    SRWF_REGISTRATION_GTB_NONCE_NAME => 'nonce',
    'gtb_enabled' => '1',
    'gtb_roles' => array_map( 'strval', $config['roles'] ),
);
ob_start();
srwf_registration_gtb_settings_page();
$save_page = ob_get_clean();
check( GFAPI::$update_calls === 1, 'explicit Save did not perform exactly one host mutation' );
check( strpos( $save_page, 'was saved' ) !== false, 'successful Save feedback missing' );

$_GET = array();
$_POST = array();

echo "PASS: per-form GTB Theme configuration and token projection contract\n";