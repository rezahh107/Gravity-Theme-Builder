## First real implementation

The first real presentation implementation is theme-local under `src/`. It is not production-qualified until the required Gravity Forms runtime checks are completed.

### Install-required source tree

The production CSS has local runtime dependencies. Install/copy the **complete `src/` tree as one WordPress plugin directory**, not only the PHP and CSS files:

```text
src/
├── srwf-registration-theme.php
├── srwf-registration.css
└── icons/
    ├── report-card-file.svg
    ├── section-contact.svg
    ├── section-education.svg
    ├── section-identity.svg
    ├── section-school-documents.svg
    └── section-student-photo.svg
```

The relative `url("icons/...")` references in `srwf-registration.css` resolve from the stylesheet location. Omitting or relocating any referenced SVG breaks that production presentation dependency. The deterministic test suite enumerates local CSS URL dependencies and fails when a referenced local asset does not resolve inside this installable tree.

### Activation

The implementation uses Gravity Forms' own supported extension points rather than registering a parallel renderer:

1. install/activate the complete `src/` tree described above;
2. on the intended SRWF form only, set **Form Settings → Form Layout → CSS Class Name** to `srwf-registration-theme`;
3. configure the documented semantic field/section Custom CSS Classes from `../IMPLEMENTATION_MAP.md` on the intended real fields/Section Breaks;
4. keep **Description Placement** and **Validation Message Placement** below inputs and enable the authentic Gravity Forms **Validation Summary** per the approved visual contract.

The stored `srwf-registration-theme` class establishes **form identity only**. Production presentation is admitted only when that identity is present **and** the current rendering context permits Registration ownership. Normal Registration, validation rerenders and legitimate Registration AJAX renders remain admitted. Gravity Flow Entry Detail is explicitly excluded without mutating the stored form class.

For an admitted Registration render, the integration selects the `orbital` form theme through `gform_form_theme_slug` and enqueues the stylesheet through `gform_enqueue_scripts`. Unrelated forms and context-excluded renders are left untouched. Non-token layout, direction, and presentation adapters remain under `.gform-theme--framework.srwf-registration-theme_wrapper`. The SRWF `--gf-*` CSS API values use the documented Theme Framework stylesheet-sentinel scope plus `.gform-theme--framework.gform-theme.srwf-registration-theme_wrapper`, so the opted-in values can outrank per-form Orbital style settings without `!important` or form-ID identity.

### Rendering-context ownership boundary

Gravity Flow Entry Detail may render an editable copy of the same underlying Gravity Forms form while preserving its configured `cssClass`. GTB therefore keeps form identity and rendering-context ownership as separate predicates and combines them only at presentation admission.

Production uses the authentic Gravity Flow hooks:

- `gravityflow_entry_detail_content_before` → increment a request-local Entry Detail depth counter;
- `gravityflow_entry_detail_content_after` → decrement the counter, floored at zero.

The counter is memory/request-local only. It is not stored in options, transients, user meta, cookies, URLs, form settings or entry data. Nested/re-entrant brackets remain excluded until the outermost bracket exits. If Gravity Flow is absent, the hooks simply never fire and normal Registration admission is unchanged. GPP is neither detected nor required.

#### Host-source qualification

Evidence state for this mechanism:

- current Gravity Flow documentation describes `gravityflow_entry_detail_content_before` as running before the primary form elements and `gravityflow_entry_detail_content_after` as running after them: `DOCUMENTED`;
- exact owner-supplied Gravity Flow `3.1.0` and Gravity Forms `3.1.1.1` source packages were byte-verified and inspected for timing: `SOURCE_PROVEN`;
- authentic Owner-site execution of this new GTB boundary has not yet occurred: `OWNER_RUNTIME_REQUIRED`.

Pinned package/source identities used for the source proof:

```text
Gravity Flow 3.1.0 package SHA-256:
ac0573b75831380417a21a455176e25eb746d718bbbd0bb70d6da6f48cba5404

Gravity Flow includes/pages/class-entry-detail.php SHA-256:
a7634c5604184502457bcb22cdf1ade892e84c888cc60996aea8a810ced7680a

Gravity Flow includes/pages/class-entry-editor.php SHA-256:
92d3ae95f79b31321215a688f7f0ff21b62c5b7046f8315a07f7b9e7442fbdbf

Gravity Forms 3.1.1.1 package SHA-256:
542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b

Gravity Forms form_display.php SHA-256:
ced7ac432e5326bd557aa5e8c28d7f768933c9bfc883292ad9aa3a5847dfda48
```

The inspected Gravity Flow `3.1.0` order is mechanically sufficient for GTB's two decisions:

1. `Gravity_Flow_Entry_Detail::entry_detail()` fires `gravityflow_entry_detail_content_before` at source line 139.
2. It later calls `entry_detail_grid()` at line 161 and fires `gravityflow_entry_detail_content_after` at line 193.
3. When editable fields are present, `entry_detail_grid()` invokes `Gravity_Flow_Entry_Editor::render_edit_form()` at line 818.
4. `render_edit_form()` calls `GFFormDisplay::get_form()` at `class-entry-editor.php` line 139.
5. In the pinned Gravity Forms `3.1.1.1` `GFFormDisplay::get_form()` path, `enqueue_form_scripts()` is called at `form_display.php` line 1247 and the wrapper theme slug is obtained with `get_form_theme_slug()` at line 1286.
6. That same pinned file fires `gform_enqueue_scripts` from `enqueue_form_scripts()` at line 3392 and applies `gform_form_theme_slug` from `get_form_theme_slug()` at line 884.

Therefore the Gravity Flow `content_before` hook has already completed before the editable Entry Detail form reaches either GTB admission decision, while `content_after` executes only after the Entry Detail grid/editor render. `include_scripts()` occurs earlier in Entry Detail, but the inspected `3.1.0` method contains only the Entry Detail inline helpers and does not call `GFFormDisplay::get_form()`.

This timing claim is intentionally version-bounded to the inspected Gravity Flow `3.1.0` / Gravity Forms `3.1.1.1` pair. A future host version that materially changes this call order must be requalified rather than assumed compatible. This is not yet a `RUNTIME_PROVEN rendering-context boundary` claim.

### Host stylesheet order contract

Owner runtime proved that direct SRWF presentation was printed before Gravity Forms Reset/Foundation/Framework/Orbital, allowing later host CSS to defeat the full-width submit rule even though the runtime submit selector matched. The repair keeps the existing conditional `gform_enqueue_scripts` lifecycle but declares the SRWF stylesheet as a WordPress dependency consumer of the verified Gravity Forms Orbital style handle:

`gravity_forms_orbital_theme -> srwf-registration-theme`

Evidence boundary:

- the repository canonical Theme Framework snapshot remains the mandatory first implementation-fact lookup, but it does not inventory WordPress enqueue handles for this question;
- current official Gravity Forms Theme Layers documentation uses `gravity_forms_orbital_theme` as the Orbital stylesheet handle;
- the admitted Owner runtime shows Orbital is the last relevant Gravity Forms theme presentation asset on the target form;
- WordPress `wp_enqueue_style()` defines `$deps` as registered stylesheet handles and resolves dependencies before the dependent stylesheet;
- if the verified Orbital dependency is unavailable at print-time, WordPress does not process the dependent SRWF branch. This is intentional fail-closed behavior rather than printing GTB early under an unproven ordering assumption.

The hook priority remains `20`; stylesheet order correctness no longer depends on that priority. No GPP class or stylesheet is an activation, dependency, rendering-context detector, or visual-authority requirement. Extra unrelated classes may coexist on the same form without changing GTB's identity or context predicates.

Vazirmatn delivery remains owned by the embedding SRWF environment; this package does not fetch fonts from a third-party CDN.

### Runtime-proven / bounded add-on adapters

The production tree currently contains two narrow, evidence-backed add-on presentation integrations:

- GP Advanced Select / Tom Select: the runtime-proven `.ts-wrapper > .ts-control` consumer receives the SRWF minimum control height. Search/open/keyboard behavior remains add-on-owned.
- GP File Upload Pro — **Report Card only**: the explicit `srwf-role-report-card-upload` field role styles the authentic initial `.gpfup` drop area while `:not(.gpfup--has-files)` is true. Upload rules, upload lifecycle, uploaded file rows and delete behavior remain GPFUP-owned.

Student Photo post-upload / preview / crop / re-crop / delete presentation is still **`RUNTIME_REQUIRED / NOT_IMPLEMENTED`** because its authentic post-upload DOM/state has not been captured. The Report Card adapter must not be generalized to Student Photo by type, label, DOM position or numeric field ID.

### Deliberately unresolved

The production breakpoint, desktop short-field pairings, desktop shadow, exact focus-ring geometry/alpha, form-title sizing/line-height, helper/error font sizes, and exact field/section rhythm remain unresolved exactly as the admitted contract requires. PersianGravity Jalali UI and Student Photo post-upload/crop presentation remain unresolved until their authentic runtime consumers are inspected.

Run deterministic checks with:

```bash
bash themes/srwf-registration/reference/materialize_reference.sh /tmp/OWNER_REFERENCE_new_7.html
python3 -m unittest discover -s themes/srwf-registration/tests -p 'test_*.py' -v
php themes/srwf-registration/tests/test_delivery.php
php themes/srwf-registration/tests/test_diagnostic_delivery.php
node themes/srwf-registration/tests/test_diagnostic_v03.js
node themes/srwf-registration/tests/test_admission_diagnostic_v031.js
php -l themes/srwf-registration/src/srwf-registration-theme.php
php -l themes/srwf-registration/diagnostic/srwf-runtime-diagnostic.php
```

These checks are repository/static/source-qualification evidence only. They do not qualify the new rendering-context boundary against the Owner WordPress + Gravity Forms + Gravity Flow runtime.
