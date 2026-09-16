# Project Source Registry

This registry records admitted local source snapshots used by **Gravity Theme Builder**.

The registry does not create a new cross-domain authority hierarchy. Repository normative authority remains governed by `docs/PROJECT_CHARTER.md`. Approved visual references remain authoritative for visual intent. Current official Gravity Forms documentation/source and inspected supported-runtime behavior remain authoritative for implementation facts when they conflict with a local snapshot.

## GF_THEME_FRAMEWORK_CANONICAL_REFERENCE

- **Path:** `PROJECT_SOURCES/00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_REFERENCE.md`
- **Admission status:** `APPROVED_WITH_SUPPLEMENTAL_AMBIGUITY_NOTE`
- **Admitted:** `2026-09-17`
- **Authority domain:** `IMPLEMENTATION_FACT_EVIDENCE / HOW`
- **Purpose:** first local lookup for Theme Framework architecture, documented wrapper/classes, public `--gf-*` CSS API identifiers, scoping, known documentation ambiguities, and version-sensitive compatibility notes.
- **Uploaded source SHA-256:** `bf3d2707ff3737af3fd22be59208cc4a9df1b48d86b68901b7ce71dc6eae5e54`
- **Uploaded source byte length:** `112820`
- **Official changelog version observed during admission review:** `Gravity Forms 3.1.1.2`
- **Update rule:** if current official Gravity Forms documentation/source or inspected supported-runtime behavior conflicts with the snapshot, the current evidence wins for the factual implementation question and this local source must be reconciled/updated.
- **Absence rule:** if a required identifier or behavior is not present in the local reference, classify it as `UNKNOWN_FROM_LOCAL_REFERENCE` and check current official documentation rather than guessing.

### Admission review

The following high-risk/version-sensitive claims were independently checked against current official Gravity Forms-owned documentation at admission time and were consistent with the snapshot:

- Theme Framework architecture uses Reset → Foundation → Theme Framework layers.
- Foundation remains required underneath custom visual styling.
- Orbital is the default implementation of the Theme Framework.
- Theme Layers provide the integration/orchestration mechanisms around settings, CSS properties, assets, and markup output.
- current wrapper/scoping guidance includes `.gform-theme`, `.gform-theme--foundation`, `.gform-theme--framework`, and `.gform-theme--orbital`.
- the CSS API is the supported native custom-property contract; undocumented `--gf-*` identifiers must not be invented.
- `--gf-form-gap-y` is currently documented with a default of `40px`.
- current Controls Base documentation exposes focus outline properties including `--gf-ctrl-outline-color-focus` and `--gf-ctrl-outline-width-focus`.
- Gravity Forms 2.8 introduced breaking Theme Framework CSS API renames.
- Gravity Forms 2.9 removed deprecated Theme Framework global CSS API properties and changed framework exclusion behavior for labels/descriptions.
- Gravity Forms 3.0 changed form buttons from `<input>` to `<button>` and moved the submission spinner inside the button.
- the current official FAQ still states that a first-class form theme cannot currently be registered; documented alternatives include CSS API defaults and enqueued custom styles.

### Supplemental documentation ambiguity discovered during admission

`DOCUMENTATION AMBIGUOUS`

The current official **Colors** CSS API page still lists:

```text
--gf-ctrl-shadow-color-focus
```

in the `Used by` relationship for `--gf-color-primary-rgb`.

However, the current dedicated **Controls — Base** API does not publish `--gf-ctrl-shadow-color-focus` in its current control property inventory. It publishes focus-outline properties instead, including:

```text
--gf-ctrl-outline-color-focus
--gf-ctrl-outline-offset
--gf-ctrl-outline-style
--gf-ctrl-outline-width-focus
```

Therefore, do not promote `--gf-ctrl-shadow-color-focus` into project code merely because the Colors page cross-reference still names it. For current control-property inventory, prefer the dedicated Controls Base API and re-check current documentation/runtime if focus-shadow behavior becomes implementation-critical.

### Official pages checked during admission

- https://docs.gravityforms.com/theme-framework/
- https://docs.gravityforms.com/quick-start-guide/
- https://docs.gravityforms.com/theme-layers/
- https://docs.gravityforms.com/theme-framework-faq/
- https://docs.gravityforms.com/theme-framework-upgrade-guide/
- https://docs.gravityforms.com/gravity-forms-2-9-key-features/
- https://docs.gravityforms.com/submit-button-css-selectors/
- https://docs.gravityforms.com/gravityforms-change-log/
- https://docs.css.gravity.com/framework.controls.default._api-global.html
- https://docs.css.gravity.com/foundation.api._layout.html
- https://docs.css.gravity.com/framework.api._colors.html
