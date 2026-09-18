<?php
$hooks = array();
$styles = array();
$current_actions = array();
$did_actions = array();

define( 'ABSPATH', __DIR__ );

function add_filter( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'filter', $hook, $callback, $priority, $args ); }
function add_action( $hook, $callback, $priority = 10, $args = 1 ) { global $hooks; $hooks[] = array( 'action', $hook, $callback, $priority, $args ); }
function plugins_url( $path, $file ) { return 'https://example.test/plugins/srwf/' . $path; }
function wp_enqueue_style( $handle, $src, $deps, $ver ) { global $styles; $styles[] = compact( 'handle', 'src', 'deps', 'ver' ); }
function doing_action( $hook = null ) { global $current_actions; return null === $hook ? ! empty( $current_actions ) : in_array( $hook, $current_actions, true ); }
function did_action( $hook ) { global $did_actions; return isset( $did_actions[ $hook ] ) ? $did_actions[ $hook ] : 0; }
function check( $condition, $message ) { if ( ! $condition ) { fwrite( STDERR, "FAIL: $message\n" ); exit( 1 ); } }

class SrwfGravityFlowSequenceFixture {
    public $workflow_detail = false;
    public $shortcode_present = false;

    public function is_workflow_detail_page() {
        return $this->workflow_detail;
    }

    public function look_for_shortcode() {
        return $this->shortcode_present;
    }
}

$gravity_flow_fixture = new SrwfGravityFlowSequenceFixture();
function gravity_flow() { global $gravity_flow_fixture; return $gravity_flow_fixture; }

require __DIR__ . '/../src/srwf-registration-theme.php';

$target = array( 'cssClass' => 'srwf-registration-theme extra-host-class' );
$stored_target = $target;

// Reproduce the authentic Owner-observed failure order from pinned Flow 3.1.0:
// wp_enqueue_scripts -> Gravity_Flow::enqueue_frontend_scripts() ->
// Gravity_Flow::enqueue_form_scripts() -> GFFormDisplay::enqueue_form_scripts().
// The old gravityflow_entry_detail_content_before hook has NOT fired at this point.
$gravity_flow_fixture->workflow_detail = true;
$gravity_flow_fixture->shortcode_present = true;
$current_actions = array( 'wp_enqueue_scripts', 'gform_enqueue_scripts' );
$did_actions['gravityflow_enqueue_frontend_scripts'] = 0;

check( srwf_registration_theme_entry_detail_context_depth() === 0, 'fixture accidentally pre-entered old content bracket' );
$early = srwf_registration_theme_get_admission_decision( $target );
check( $early['formIdentityMatched'] === true, 'early sequence lost target identity' );
check( $early['presentationAdmitted'] === false, 'early Flow Entry Detail sequence still admits Registration' );
check( $early['renderingContext'] === 'gravity_flow_entry_detail', 'early Flow sequence not classified as Entry Detail' );
check( $early['contextEvidence'] === 'gravity_flow_early_enqueue', 'early Flow sequence lacks early-enqueue evidence' );
check( $early['exclusionReason'] === 'gravity_flow_entry_detail', 'early Flow sequence exclusion reason changed' );
check( srwf_registration_theme_force_orbital( 'host-owned-theme', $target ) === 'host-owned-theme', 'early Flow Entry Detail forced Orbital' );
srwf_registration_theme_enqueue_styles( $target, false );
check( count( $styles ) === 0, 'early Flow Entry Detail enqueued SRWF stylesheet before content hook' );

// Gravity Flow 3.1.0 fires this action after its early enqueue operation. Once that
// bounded host phase ends, suppression must not become request-wide.
$did_actions['gravityflow_enqueue_frontend_scripts'] = 1;
$current_actions = array();
$after_early_phase = srwf_registration_theme_get_admission_decision( $target );
check( $after_early_phase['presentationAdmitted'] === true, 'early enqueue suppression leaked request-wide' );
check( $after_early_phase['contextEvidence'] === 'registration_default', 'early enqueue phase did not close' );

// Later, the authentic primary-content bracket still suppresses the actual Entry Detail
// form render. This is complementary protection, not the first timing boundary.
srwf_registration_theme_enter_entry_detail_context( $target, array() );
$content = srwf_registration_theme_get_admission_decision( $target );
check( $content['presentationAdmitted'] === false, 'Entry Detail content render admitted Registration' );
check( $content['contextEvidence'] === 'gravity_flow_content_bracket', 'content bracket evidence missing' );
srwf_registration_theme_leave_entry_detail_context( $target, array() );
check( srwf_registration_theme_get_admission_decision( $target )['presentationAdmitted'] === true, 'content suppression leaked after Entry Detail' );

// A Flow component that is not the host-classified detail route must not suppress a
// legitimate target render during wp_enqueue_scripts.
$gravity_flow_fixture->workflow_detail = false;
$gravity_flow_fixture->shortcode_present = true;
$current_actions = array( 'wp_enqueue_scripts', 'gform_enqueue_scripts' );
$did_actions['gravityflow_enqueue_frontend_scripts'] = 0;
check( srwf_registration_theme_get_admission_decision( $target )['presentationAdmitted'] === true, 'non-detail Flow surface suppressed Registration' );

// A detail-shaped host predicate without a Flow shortcode/block does not arm the
// front-end early phase, preventing unrelated page work from being classified by URL.
$gravity_flow_fixture->workflow_detail = true;
$gravity_flow_fixture->shortcode_present = false;
check( srwf_registration_theme_get_admission_decision( $target )['presentationAdmitted'] === true, 'frontend detail predicate without Flow component suppressed Registration' );

// Admin Entry Detail uses the same host route classifier and Flow's admin post-enqueue
// action as a bounded early phase.
$current_actions = array( 'admin_enqueue_scripts', 'gform_enqueue_scripts' );
$did_actions['gravityflow_enqueue_admin_scripts'] = 0;
$admin_early = srwf_registration_theme_get_admission_decision( $target );
check( $admin_early['presentationAdmitted'] === false, 'admin early Entry Detail sequence admitted Registration' );
check( $admin_early['contextEvidence'] === 'gravity_flow_early_enqueue', 'admin early evidence missing' );
$did_actions['gravityflow_enqueue_admin_scripts'] = 1;
$current_actions = array();
check( srwf_registration_theme_get_admission_decision( $target )['presentationAdmitted'] === true, 'admin early suppression leaked request-wide' );

check( $target === $stored_target, 'early isolation mutated stored form CSS class' );

echo "PASS: authentic-order Entry Detail early enqueue regression\n";
