## First real implementation

The SRWF Registration implementation is theme-local under `src/`. It is not production-qualified until the required Gravity Forms/runtime/browser checks are completed.

### Install-required source tree

Install/copy the **complete `src/` tree as one WordPress plugin directory**:

```text
src/
├── srwf-registration-theme.php
├── srwf-registration-settings.php
├── srwf-registration.css
└── icons/
    ├── report-card-file.svg
    ├── section-contact.svg
    ├── section-education.svg
    ├── section-identity.svg
    ├── section-school-documents.svg
    └── section-student-photo.svg
```

The CSS uses relative local `icons/...` URLs; omitting those files breaks the production presentation dependency. Deterministic tests verify that the package contains the full dependency closure.

### Per-form activation and semantic setup

Normal operation no longer requires the Owner to type or maintain GTB-owned Custom CSS Class tokens manually.

Use:

**Gravity Forms → Form Settings → GTB Theme**

The page is registered through Gravity Forms' supported per-form settings seams:

- `gform_form_settings_menu`;
- `gform_form_settings_page_gtb_theme`.

There is no top-level GTB admin menu.

The settings surface stores SRWF activation separately from eight semantic mappings: Gender, Graduation Status, Report Card upload, and the five mapped Section Break roles.

Numeric field IDs shown in the admin UI are internal references to objects in the current Gravity Forms Form Object only. They are not CSS/public presentation identity and are never used as durable selectors.

On explicit **Save GTB Configuration**, GTB validates the complete submitted mapping before mutation, builds the intended form state, removes only GTB-owned projection tokens, adds the exact tokens required by the mapping, preserves unrelated Custom CSS Class tokens in meaning, and performs one `GFAPI::update_form()` call. Invalid/ambiguous mappings fail closed before host mutation.

`Check Again` is read-only. Ordinary page render is read-only. `Load Recommended SRWF Draft` is also read-only: it can reuse only already-present explicit unique GTB semantic tokens, never infers the two shared binary roles, reports its proposed changes, and does not save until the explicit Save path succeeds.

Readiness states are `DISABLED`, `NEEDS SETUP`, `ATTENTION REQUIRED`, and `READY`.

The permission boundary prefers Gravity Forms' own `GFAPI::current_user_can_any( 'gravityforms_edit_forms' )` resolver and falls back to the WordPress capability check only when that Gravity Forms API is unavailable. Save/recommend POST actions are nonce-protected independently from authorization.

Historical Owner evidence from the prior PR #14 candidate proved this settings path could load, save, reach `READY`, persist configuration, and project the intended semantic tokens in the Owner runtime. That evidence is preserved in `../evidence/OWNER_RUNTIME_GTB_CONFIGURATION_2026-09-18.md`. It is historical product-path evidence, not runtime proof for this reconciled `0.1.8` branch.

### Presentation admission remains independent from admin state

The stored `srwf-registration-theme` class establishes form identity only. Production presentation is admitted only when that identity is present **and** the current rendering context permits Registration ownership.

Normal Registration, validation rerenders, and legitimate Registration AJAX renders remain admitted. Gravity Flow Entry Detail remains excluded without mutating stored form configuration. The per-form settings page does not weaken or replace that context boundary.

For an admitted Registration render, GTB selects Orbital through `gform_form_theme_slug` and enqueues the SRWF stylesheet through `gform_enqueue_scripts`. Unrelated forms and context-excluded renders are untouched.

### Rendering-context ownership boundary

Gravity Flow Entry Detail can render the same underlying Gravity Forms form while preserving its configured `cssClass`. GTB therefore keeps form identity and rendering-context ownership as separate predicates.

The current-main repair keeps the primary Entry Detail content bracket and a narrow, source-proven early lifecycle classification for Gravity Flow's own enqueue phase.

GTB does not parse `$_GET`, URLs, query strings, page IDs, numeric form IDs, labels, or GPP state. It delegates route identity to Gravity Flow's public `is_workflow_detail_page()` predicate and bounds early classification to the host enqueue lifecycle:

- front end: while `wp_enqueue_scripts` is executing, the Gravity Flow shortcode/block is present, `is_workflow_detail_page()` is true, and `gravityflow_enqueue_frontend_scripts` has not yet fired;
- admin: while `admin_enqueue_scripts` is executing, `is_workflow_detail_page()` is true, and `gravityflow_enqueue_admin_scripts` has not yet fired.

After the corresponding Gravity Flow post-enqueue action fires, the early phase ends. This is deliberately not request-wide monotonic suppression, so a later independent Registration render in the same request can still be admitted.

The primary-content `gravityflow_entry_detail_content_before` / `gravityflow_entry_detail_content_after` depth counter remains request-local and re-entrant-safe. Nothing is persisted in options, transients, user meta, cookies, form configuration, or entry data.

If Gravity Flow is absent, the early predicate fails closed and normal Registration admission is unchanged. GPP is neither detected nor required.

#### Host-source qualification retained from the current main line

PR #12 is retained in the evidence chronology because Owner runtime disproved its assumption that the later content bracket alone covered Gravity Flow's early form enqueue. The follow-up source-qualified repair inspected exact Gravity Flow `3.1.0` and Gravity Forms `3.1.1.1` behavior and established the order from `wp_enqueue_scripts` → Gravity Flow `enqueue_frontend_scripts()` → `enqueue_form_scripts()` → Gravity Forms `gform_enqueue_scripts` / `gform_form_theme_slug`, before `gravityflow_entry_detail_content_before`. The exact reconciled branch remains `OWNER_RUNTIME_REQUIRED`; static/source proof does not convert this new package into a fresh Owner runtime result.

Evidence state:

- official Gravity Flow documentation describes `gravityflow_entry_detail_content_before` and `gravityflow_entry_detail_content_after`: `DOCUMENTED`;
- exact Owner-supplied Gravity Flow `3.1.0` and Gravity Forms `3.1.1.1` source packages were byte-verified and inspected for the early enqueue order: `SOURCE_PROVEN`;
- Owner runtime disproved the earlier assumption that the content bracket alone was early enough: `OWNER_RUNTIME_PROVEN_TIMING_DEFECT`;
- the repaired boundary is protected by deterministic regression tests; current exact-branch Owner runtime recheck remains appropriate when qualifying a new installable artifact.

Pinned identities retained as source evidence:

```text
Gravity Flow 3.1.0 package SHA-256:
ac0573b75831380417a21a455176e25eb746d718bbbd0bb70d6da6f48cba5404

Gravity Flow class-gravity-flow.php SHA-256:
16666115e37a7704b8331973eba0a0499e039d3fdfc6b47ed8a8e95a41779a79

Gravity Flow includes/pages/class-entry-detail.php SHA-256:
a7634c5604184502457bcb22cdf1ade892e84c888cc60996aea8a810ced7680a

Gravity Flow includes/pages/class-inbox.php SHA-256:
71cebf5a3dbefcf31a0d63ac26b2f7a0581e4b70147dbb2b7569c88120b36b53

Gravity Forms 3.1.1.1 package SHA-256:
542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b

Gravity Forms form_display.php SHA-256:
ced7ac432e5326bd557aa5e8c28d7f768933c9bfc883292ad9aa3a5847dfda48

Gravity Forms theme-layer Asset Enqueue Output Engine SHA-256:
0a8b62457eba016c1bb0837cb516b8e30fe45e717ab5113d238d1e689a541795
```

The source-qualified order remains:

1. Gravity Flow `3.1.0` registers `enqueue_frontend_scripts()` on `wp_enqueue_scripts` at priority `10`.
2. Its enqueue callback can call `enqueue_form_scripts()` before `gravityflow_enqueue_frontend_scripts` fires.
3. `enqueue_form_scripts()` reaches `GFFormDisplay::enqueue_form_scripts( $form )`.
4. Gravity Forms fires `gform_enqueue_scripts` from that path.
5. Theme-layer enqueue can reach `gform_form_theme_slug` before the later Entry Detail content bracket.
6. Therefore the early host predicate remains necessary to prevent GTB Registration admission on the standard Gravity Flow Entry Detail route.

### Host stylesheet order contract

For admitted Registration renders, the SRWF stylesheet remains a WordPress dependency consumer of:

`gravity_forms_orbital_theme -> srwf-registration-theme`

This preserves the previously repaired host order. Entry Detail isolation prevents GTB admission early; it does not dequeue host assets, fight the cascade, or add `!important`.

Vazirmatn delivery remains owned by the embedding SRWF environment.

### Runtime-proven / bounded add-on adapters

Current production remains limited to evidence-backed presentation integrations:

- GP Advanced Select / Tom Select: the runtime-proven `.ts-wrapper > .ts-control` consumer receives the SRWF minimum control height; search/open/keyboard behavior remains add-on-owned.
- GP File Upload Pro — **Report Card only**: explicit `srwf-role-report-card-upload` styles the authentic initial `.gpfup` drop area while `:not(.gpfup--has-files)` is true; upload lifecycle and uploaded rows/delete remain GPFUP-owned.

Student Photo post-upload / preview / crop / re-crop / delete presentation remains **`RUNTIME_REQUIRED / NOT_IMPLEMENTED`** on the production path; under the current evidence vocabulary this means Owner runtime is required before any implementation may assume authentic states. The Report Card adapter must not be generalized by type, label, DOM position, or numeric ID.

### Current authority vs current CSS

`../reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md` is now current authority for the newly resolved destination, including the `960px` breakpoint, host-owned desktop pairings, no-shadow card geometry, exact form-title/helper/error/rhythm/focus values, and Gravity Forms recommended above-input description/validation/sub-label placement.

This reconciliation batch intentionally **does not implement those newly resolved visual constants as a broad CSS repair**. The existing production CSS from current main, including PR #15's binary-choice row/equal-track behavior, is preserved unchanged. The next visual batch must implement and runtime-qualify the remaining destination without re-inventing host behavior.

Run deterministic checks with:

```bash
bash themes/srwf-registration/reference/materialize_reference.sh /tmp/OWNER_REFERENCE_new_7.html
python3 -m unittest discover -s themes/srwf-registration/tests -p 'test_*.py' -v
php themes/srwf-registration/tests/test_form_settings.php
php themes/srwf-registration/tests/test_delivery.php
php themes/srwf-registration/tests/test_entry_detail_early_sequence.php
php themes/srwf-registration/tests/test_diagnostic_delivery.php
node themes/srwf-registration/tests/test_diagnostic_v03.js
node themes/srwf-registration/tests/test_binary_choice_geometry.js
node themes/srwf-registration/tests/test_admission_diagnostic_v032.js
php -l themes/srwf-registration/src/srwf-registration-theme.php
php -l themes/srwf-registration/src/srwf-registration-settings.php
```

These checks prove repository/static/source contracts only. They do not by themselves prove the reconciled branch in the Owner WordPress + Gravity Forms + Gravity Flow browser runtime.
