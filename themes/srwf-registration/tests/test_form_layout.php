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
function wp_nonce_field( $action, $name ) { echo '<input type="hidden" name="' . esc_attr( $name ) . '" value="nonce">'; }
function check_admin_referer( $action, $name ) { if ( ! isset( $_POST[ $name ] ) || 'nonce' !== $_POST[ $name ] ) { throw new RuntimeException( 'invalid nonce' ); } return true; }
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
    public static $update_calls = 0;
    public static $update_hook = null;
    public static function current_user_can_any( $capability ) { global $allow_edit_forms; return $allow_edit_forms && 'gravityforms_edit_forms' === $capability; }
    public static function get_form( $id ) { return self::$forms[ $id ] ?? false; }
    public static function update_form( $form ) {
        global $updates;
        self::$update_calls++;
        $updates[] = $form;
        if ( is_callable( self::$update_hook ) ) {
            return call_user_func( self::$update_hook, $form );
        }
        self::$forms[ $form['id'] ] = $form;
        return true;
    }
}
class GFFormSettings {
    public static function page_header() { echo '<div>'; }
    public static function page_footer() { echo '</div>'; }
}
class TestField {
    public $id;
    public $type;
    public $label;
    public $cssClass = '';
    public $labelPlacement = '';
    public $descriptionPlacement = '';
    public $subLabelPlacement = '';
    public function __construct( $id, $type ) { $this->id = $id; $this->type = $type; $this->label = 'Field ' . $id; }
    public function get_input_type() { return $this->type; }
}
function srwf_registration_theme_is_target_form( $form ) { return strpos( (string) ( $form['cssClass'] ?? '' ), 'srwf-registration-theme' ) !== false; }
function check( $condition, $message ) { if ( ! $condition ) { fwrite( STDERR, "FAIL: $message\n" ); exit( 1 ); } }

require __DIR__ . '/../src/srwf-registration-settings.php';

$form = array(
    'id' => 91,
    'cssClass' => 'foreign-class srwf-registration-theme',
    'title' => 'Keep title',
    'description' => 'Keep description',
    'notifications' => array( 'n1' => array( 'name' => 'Keep notification' ) ),
    'confirmations' => array( 'c1' => array( 'name' => 'Keep confirmation' ) ),
    'pagination' => array( 'type' => 'percentage' ),
    'save' => array( 'enabled' => true ),
    'customRequiredIndicator' => '<span>custom untouched</span>',
    'labelPlacement' => 'right_label',
    'descriptionPlacement' => 'below',
    'validationPlacement' => 'below',
    'subLabelPlacement' => 'below',
    'validationSummary' => false,
    'requiredIndicator' => 'text',
    'fields' => array( new TestField( 4, 'text' ), new TestField( 8, 'name' ) ),
);
GFAPI::$forms[91] = $form;

$expected = srwf_registration_gtb_layout_expected();
check( $expected === array(
    'labelPlacement' => 'top_label',
    'descriptionPlacement' => 'above',
    'validationPlacement' => 'above',
    'subLabelPlacement' => 'above',
    'validationSummary' => true,
    'requiredIndicator' => 'asterisk',
), 'authorized expected Form Layout values changed' );

GFAPI::$update_calls = 0;
$readiness = srwf_registration_gtb_layout_readiness( GFAPI::$forms[91] );
check( 'NEEDS ATTENTION' === $readiness['state'], 'mismatching form incorrectly READY' );
check( 0 === GFAPI::$update_calls, 'readiness evaluation mutated form' );

// Explicit field overrides block overall readiness but are never silently normalized.
GFAPI::$forms[91]['fields'][0]->descriptionPlacement = 'below';
$readiness = srwf_registration_gtb_layout_readiness( GFAPI::$forms[91] );
check( 1 === count( $readiness['field_override_conflicts'] ), 'explicit field-level conflict not reported' );
check( 4 === $readiness['field_override_conflicts'][0]['field_id'], 'safe field reference missing' );
check( 'descriptionPlacement' === $readiness['field_override_conflicts'][0]['property'], 'wrong conflict property reported' );

// Simulate page staleness: mutate an unrelated property after the first read, before Apply.
$stale_snapshot = GFAPI::$forms[91];
GFAPI::$forms[91]['title'] = 'Newest title from another editor';
GFAPI::$forms[91]['unrelated_new_state'] = array( 'keep' => true );
$before_apply = GFAPI::$forms[91];
GFAPI::$update_calls = 0;
$result = srwf_registration_gtb_apply_layout( 91 );
check( ! is_wp_error( $result ) && true === $result['wrote'], 'explicit layout apply failed' );
check( 1 === GFAPI::$update_calls, 'explicit layout apply did not perform exactly one write' );
$saved = GFAPI::$forms[91];
foreach ( $expected as $property => $value ) {
    check( $saved[ $property ] === $value, "layout property $property did not persist" );
}
check( 'Newest title from another editor' === $saved['title'], 'apply overwrote latest title from stale snapshot' );
check( $saved['unrelated_new_state'] === array( 'keep' => true ), 'apply lost latest unrelated state' );
check( $saved['notifications'] === $before_apply['notifications'], 'notifications changed' );
check( $saved['confirmations'] === $before_apply['confirmations'], 'confirmations changed' );
check( $saved['pagination'] === $before_apply['pagination'], 'pagination changed' );
check( $saved['save'] === $before_apply['save'], 'save-and-continue state changed' );
check( $saved['cssClass'] === $before_apply['cssClass'], 'CSS classes changed' );
check( $saved['customRequiredIndicator'] === $before_apply['customRequiredIndicator'], 'customRequiredIndicator was unnecessarily overwritten' );
check( $saved['fields'][0]->descriptionPlacement === 'below', 'field-level override was silently normalized' );
check( $stale_snapshot['title'] !== $saved['title'], 'test did not exercise current-object reread' );

// Second Apply is idempotent at form level: override remains attention-required, no unnecessary write.
GFAPI::$update_calls = 0;
$second = srwf_registration_gtb_apply_layout( 91 );
check( ! is_wp_error( $second ) && false === $second['wrote'], 'already-matching form-level layout was written again' );
check( 'ALREADY MATCHING' === $second['status'], 'idempotent result state changed' );
check( 0 === GFAPI::$update_calls, 'second Apply caused unnecessary write churn' );
check( 'NEEDS ATTENTION' === $second['readiness']['state'], 'field override should keep overall readiness non-ready' );

// Capability is independent from request intent/nonce.
$allow_edit_forms = false;
GFAPI::$update_calls = 0;
$forbidden = srwf_registration_gtb_apply_layout( 91 );
check( is_wp_error( $forbidden ), 'capability failure did not fail closed' );
check( 0 === GFAPI::$update_calls, 'capability failure mutated form' );
$allow_edit_forms = true;

// Renderer only mutates on explicit apply_layout and rejects a bad nonce before mutation.
GFAPI::$update_calls = 0;
$_POST = array( 'gtb_action' => 'apply_layout', SRWF_REGISTRATION_GTB_LAYOUT_NONCE_NAME => 'bad' );
try {
    ob_start();
    srwf_registration_gtb_render_form_presentation_readiness( 91 );
    ob_end_clean();
    check( false, 'bad Apply nonce was accepted' );
} catch ( RuntimeException $exception ) {
    if ( ob_get_level() ) { ob_end_clean(); }
    check( 'invalid nonce' === $exception->getMessage(), 'bad nonce failure changed' );
}
check( 0 === GFAPI::$update_calls, 'bad nonce mutated form' );

GFAPI::$update_calls = 0;
$_POST = array();
ob_start();
srwf_registration_gtb_render_form_presentation_readiness( 91 );
$page = ob_get_clean();
check( 0 === GFAPI::$update_calls, 'ordinary readiness render mutated form' );
check( strpos( $page, 'SRWF Form Presentation Readiness' ) !== false, 'readiness UI missing' );
check( strpos( $page, 'ATTENTION REQUIRED' ) !== false, 'field override attention not rendered' );
check( strpos( $page, 'Apply Recommended SRWF Form Layout' ) !== false, 'explicit Apply control missing' );

// Read-back verification fails truthfully if the host confirms update but does not persist it.
GFAPI::$forms[91]['requiredIndicator'] = 'text';
GFAPI::$update_hook = function ( $next ) {
    $stored = $next;
    $stored['requiredIndicator'] = 'text';
    GFAPI::$forms[ $next['id'] ] = $stored;
    return true;
};
GFAPI::$update_calls = 0;
$readback_failure = srwf_registration_gtb_apply_layout( 91 );
check( is_wp_error( $readback_failure ), 'failed persistence was reported as success' );
check( 1 === GFAPI::$update_calls, 'persistence failure did not exercise one host write' );
GFAPI::$update_hook = null;

$_POST = array();
echo "PASS: SRWF Form Layout readiness and bounded explicit apply contract\n";
