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

For that opted-in form, the integration selects the `orbital` form theme through `gform_form_theme_slug` and enqueues the stylesheet through `gform_enqueue_scripts`. Other forms are left untouched. Non-token layout, direction, and presentation adapters remain under `.gform-theme--framework.srwf-registration-theme_wrapper`. The SRWF `--gf-*` CSS API values use the documented Theme Framework stylesheet-sentinel scope plus `.gform-theme--framework.gform-theme.srwf-registration-theme_wrapper`, so the opted-in values can outrank per-form Orbital style settings without `!important` or form-ID identity.

### Host stylesheet order contract

Owner runtime proved that direct SRWF presentation was printed before Gravity Forms Reset/Foundation/Framework/Orbital, allowing later host CSS to defeat the full-width submit rule even though the runtime submit selector matched. The repair keeps the existing conditional `gform_enqueue_scripts` lifecycle but declares the SRWF stylesheet as a WordPress dependency consumer of the verified Gravity Forms Orbital style handle:

`gravity_forms_orbital_theme -> srwf-registration-theme`

Evidence boundary:

- the repository canonical Theme Framework snapshot remains the mandatory first implementation-fact lookup, but it does not inventory WordPress enqueue handles for this question;
- current official Gravity Forms Theme Layers documentation uses `gravity_forms_orbital_theme` as the Orbital stylesheet handle;
- the admitted Owner runtime shows Orbital is the last relevant Gravity Forms theme presentation asset on the target form;
- WordPress `wp_enqueue_style()` defines `$deps` as registered stylesheet handles and resolves dependencies before the dependent stylesheet;
- if the verified Orbital dependency is unavailable at print-time, WordPress does not process the dependent SRWF branch. This is intentional fail-closed behavior rather than printing GTB early under an unproven ordering assumption.

The hook priority remains `20`; stylesheet order correctness no longer depends on that priority. No GPP class or stylesheet is an activation, dependency, or visual-authority requirement. Extra GPP classes may coexist on the same form without changing GTB's opt-in identity.

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
php -l themes/srwf-registration/src/srwf-registration-theme.php
php -l themes/srwf-registration/diagnostic/srwf-runtime-diagnostic.php
```

These checks are repository/static evidence only. They do not qualify the theme against a real WordPress + Gravity Forms runtime.
