## First real implementation

The first real presentation implementation is theme-local under `src/`. It is not production-qualified until the required Gravity Forms runtime checks are completed.

### Install-required source tree

The production CSS has local runtime dependencies and the plugin now includes the native per-form GTB Theme configuration surface. Install/copy the **complete `src/` tree as one WordPress plugin directory**:

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

The relative `url("icons/...")` references in `srwf-registration.css` resolve from the stylesheet location. Omitting or relocating any referenced SVG breaks that production presentation dependency. The deterministic package test enumerates local CSS URL dependencies and fails when a referenced local asset does not resolve inside the installable tree.

### Per-form activation and guided setup

Normal operation no longer requires the Owner to type or maintain GTB-owned Custom CSS Class tokens manually.

1. install/activate the complete `src/` tree described above;
2. open **Gravity Forms → the intended form → Settings → GTB Theme**;
3. enable **SRWF Registration** and map each semantic role to a compatible real field/Section Break;
4. click **Save GTB Configuration** to validate the whole requested mapping, store the bounded per-form configuration and project GTB-owned tokens;
5. use **Check Again** as a read-only verification step;
6. keep authentic Gravity Forms **Description Placement** and **Validation Message Placement** below inputs and enable the Gravity Forms **Validation Summary** according to the approved visual contract.

The page uses current Gravity Forms field labels only so the Owner can recognize real host objects. Labels, admin labels, DOM position and field order are never used to infer semantic identity. Candidate selectors are filtered by authentic host type: the two binary roles accept Radio fields, Report Card accepts File Upload fields, and section-icon roles accept Section Breaks.

The stored per-form record is `gtb_srwf_registration`. It keeps SRWF enablement and separate semantic slots for Gender, Graduation Status, Report Card, and the five section roles. Numeric field IDs are only references inside that form configuration; they are not CSS selectors, public theme identity, durable visual-contract identity, or a hard-coded Form 11 path.

### Token projection and preservation

The semantic GTB classes remain the durable presentation contract consumed by the existing CSS. **Save GTB Configuration** projects them into Gravity Forms form/field `cssClass` values.

GTB projection:

- adds/removes only `srwf-registration-theme` and the documented GTB-owned role tokens;
- preserves unrelated form/field class tokens;
- normalizes class whitespace only during explicit Save;
- avoids duplicate tokens and is idempotent across repeated Save;
- removes stale GTB-owned role tokens when a mapping moves;
- preserves a shared token when another configured role still legitimately requires it;
- validates the complete request before calling the Gravity Forms update API;
- never rewrites classes merely because the settings page or frontend form rendered.

The **Apply Recommended SRWF Configuration** action prepares only mappings supported by unambiguous existing GTB semantic-token evidence. It does not guess the two binary-choice roles from labels or from their shared token, and it does not persist anything until **Save GTB Configuration** succeeds.

Readiness fails closed:

- `DISABLED` — SRWF Registration is disabled and its activation token is absent;
- `NEEDS SETUP` — enabled, but one or more required semantic roles are still unmapped;
- `ATTENTION REQUIRED` — a mapped host object is missing/incompatible or the saved configuration and projected owned tokens disagree;
- `READY` — all required mappings are valid and exact GTB-owned projection matches the saved configuration.

**Check Again** only re-reads current state. It does not repair or mutate the form.

### Runtime presentation and rendering-context ownership boundary

The stored `srwf-registration-theme` class establishes **form identity only**. Production presentation is admitted only when that identity is present **and** the current rendering context permits Registration ownership. Normal Registration, validation rerenders and legitimate Registration AJAX renders remain admitted. Gravity Flow Entry Detail is excluded without mutating the stored form class.

For an admitted Registration render, the integration selects the `orbital` form theme through `gform_form_theme_slug` and enqueues the stylesheet through `gform_enqueue_scripts`. Unrelated forms and context-excluded renders are left untouched. Non-token layout, direction, and presentation adapters remain under `.gform-theme--framework.srwf-registration-theme_wrapper`.

Gravity Flow Entry Detail may render the same underlying Gravity Forms form while preserving its configured `cssClass`. GTB therefore keeps form identity and rendering-context ownership as separate predicates and combines them only at presentation admission. The GTB Theme settings feature does not inspect GPP and does not weaken this boundary.

#### PR #12: useful classification, insufficient timing

PR #12 introduced the first request-local Entry Detail classification using:

- `gravityflow_entry_detail_content_before` → enter Entry Detail content context;
- `gravityflow_entry_detail_content_after` → leave it.

That work was useful because authentic Owner runtime then exposed the exact timing defect: on the same Entry Detail request the diagnostic recorded an early admitted `registration` decision, followed later by the expected excluded `gravity_flow_entry_detail` decision, while `srwf-registration-theme-css` version `0.1.4` was already present. The later OFF decision was therefore correct but too late to undo the earlier production enqueue.

This does **not** invalidate the content bracket. It proves that the bracket is insufficient as the *first* Entry Detail boundary because Gravity Flow performs form presentation enqueue work earlier in the request.

#### Repaired early boundary

The repair keeps the content bracket for the actual Entry Detail render and adds a narrower, source-proven early lifecycle classification for Gravity Flow's own enqueue phase.

GTB does not parse `$_GET`, URLs, query strings, page IDs, numeric form IDs, labels, or GPP state. It delegates route identity to Gravity Flow's public `is_workflow_detail_page()` predicate and bounds the early classification to the host enqueue lifecycle:

- front end: while `wp_enqueue_scripts` is executing, the Gravity Flow shortcode/block is present, `is_workflow_detail_page()` is true, and `gravityflow_enqueue_frontend_scripts` has not yet fired;
- admin: while `admin_enqueue_scripts` is executing, `is_workflow_detail_page()` is true, and `gravityflow_enqueue_admin_scripts` has not yet fired.

Once the corresponding Gravity Flow post-enqueue action has fired, the early phase is over. This is deliberately **not** a request-wide monotonic suppression. A later independent Registration render in the same request is not suppressed merely because Gravity Flow performed its earlier enqueue work.

The existing primary-content before/after depth counter remains request-local and depth-safe for the later Entry Detail render itself. Nothing is persisted in options, transients, user meta, cookies, form configuration, or entry data by this context classifier.

If Gravity Flow is absent, the early predicate fails closed and normal Registration admission is unchanged. GPP is neither detected nor required.

#### Host-source qualification

Evidence state:

- official Gravity Flow documentation describes `gravityflow_entry_detail_content_before` as running before the primary form elements and `gravityflow_entry_detail_content_after` as running after them: `DOCUMENTED`;
- exact Owner-supplied Gravity Flow `3.1.0` and Gravity Forms `3.1.1.1` source packages were byte-verified and inspected for the earlier enqueue order: `SOURCE_PROVEN`;
- authentic Owner runtime disproved PR #12's assumption that the content bracket was early enough for every presentation decision: `RUNTIME_PROVEN_TIMING_DEFECT`;
- authentic Owner-site execution of this repaired early boundary is still `OWNER_RUNTIME_REQUIRED`.

Pinned package/source identities:

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

The pinned source order that confirms the PR #13 repair remains:

1. Gravity Flow `3.1.0` registers `enqueue_frontend_scripts()` on `wp_enqueue_scripts` and calls `enqueue_form_scripts()` before firing `gravityflow_enqueue_frontend_scripts`.
2. Gravity Flow's `enqueue_form_scripts()` obtains the current form and invokes the Gravity Forms form enqueue path; Gravity Forms then fires `gform_enqueue_scripts`.
3. The Gravity Forms Theme Layer reaches `gform_form_theme_slug` while resolving the form theme during that enqueue path.
4. Only later, while Gravity Flow renders Entry Detail, `gravityflow_entry_detail_content_before` fires. That is why PR #12's content bracket could not prevent the earlier theme/style admission.
5. The repaired early classifier delegates route identity to `is_workflow_detail_page()` and is bounded to the authentic Gravity Flow enqueue lifecycle rather than introducing a request-wide or URL-parsing heuristic.

This source-qualified ordering remains version-bounded to the inspected Gravity Flow `3.1.0` / Gravity Forms `3.1.1.1` call order and still needs the Owner runtime recheck.

### Host stylesheet order contract

For admitted Registration renders, the SRWF stylesheet remains a WordPress dependency consumer of the verified Gravity Forms Orbital handle:

`gravity_forms_orbital_theme -> srwf-registration-theme`

This preserves the previously runtime-proven Registration ordering repair. Entry Detail isolation prevents GTB admission earlier; it does not dequeue Gravity Forms assets, fight the host cascade, or introduce `!important`.

The hook priority remains `20`; stylesheet order correctness does not depend on that priority. No GPP class or stylesheet is an activation, dependency, rendering-context detector, or visual-authority requirement.

Vazirmatn delivery remains owned by the embedding SRWF environment; this package does not fetch fonts from a third-party CDN.

### Runtime-proven / bounded add-on adapters

The production tree currently contains two narrow, evidence-backed add-on presentation integrations:

- GP Advanced Select / Tom Select: the runtime-proven `.ts-wrapper > .ts-control` consumer receives the SRWF minimum control height. Search/open/keyboard behavior remains add-on-owned.
- GP File Upload Pro — **Report Card only**: the explicit `srwf-role-report-card-upload` field role styles the authentic initial `.gpfup` drop area while `:not(.gpfup--has-files)` is true. Upload rules, upload lifecycle, uploaded file rows and delete behavior remain GPFUP-owned.

Student Photo post-upload / preview / crop / re-crop / delete presentation remains **`RUNTIME_REQUIRED / NOT_IMPLEMENTED`** because its authentic post-upload DOM/state has not been captured. The Report Card adapter must not be generalized to Student Photo by type, label, DOM position or numeric field ID.

### Deliberately unresolved

The production breakpoint, desktop short-field pairings, desktop shadow, exact focus-ring geometry/alpha, form-title sizing/line-height, helper/error font sizes, and exact field/section rhythm remain unresolved exactly as the admitted contract requires. PersianGravity Jalali UI and Student Photo post-upload/crop presentation remain unresolved until their authentic runtime consumers are inspected.

Run deterministic checks with:

```bash
bash themes/srwf-registration/reference/materialize_reference.sh /tmp/OWNER_REFERENCE_new_7.html
python3 -m unittest discover -s themes/srwf-registration/tests -p 'test_*.py' -v
php themes/srwf-registration/tests/test_form_settings.php
php themes/srwf-registration/tests/test_delivery.php
php themes/srwf-registration/tests/test_entry_detail_early_sequence.php
php themes/srwf-registration/tests/test_diagnostic_delivery.php
node themes/srwf-registration/tests/test_diagnostic_v03.js
node themes/srwf-registration/tests/test_admission_diagnostic_v032.js
php -l themes/srwf-registration/src/srwf-registration-theme.php
php -l themes/srwf-registration/src/srwf-registration-settings.php
php -l themes/srwf-registration/diagnostic/srwf-runtime-diagnostic.php
```

These checks are repository/static/source-qualification evidence only. They do not qualify the new admin settings surface or the repaired rendering-context boundary against the Owner WordPress + Gravity Forms + Gravity Flow runtime.
