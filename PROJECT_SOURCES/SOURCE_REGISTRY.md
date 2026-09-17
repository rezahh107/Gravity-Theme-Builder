# Project Source Registry

This registry records admitted local source snapshots used by **Gravity Theme Builder**.

The registry does not create a new cross-domain authority hierarchy. Repository normative authority remains governed by `docs/PROJECT_CHARTER.md`. Approved visual references remain authoritative for visual intent. Current official Gravity Forms documentation/source and inspected supported-runtime behavior remain authoritative for implementation facts when they conflict with a local snapshot.

## GF_THEME_FRAMEWORK_CANONICAL_REFERENCE

- **Path:** `PROJECT_SOURCES/00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_REFERENCE.md`
- **Validation evidence:** `PROJECT_SOURCES/00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_VALIDATION_2026-09-17.md`
- **Admission status:** `CANONICAL_READY`
- **Canonical status:** `ACTIVE`
- **Admitted:** `2026-09-17`
- **Authority domain:** `IMPLEMENTATION_FACT_EVIDENCE / HOW`
- **Purpose:** mandatory first local lookup for Theme Framework architecture, documented wrapper/classes, public `--gf-*` CSS API identifiers, scoping, known documentation ambiguities, and version-sensitive compatibility notes.
- **Canonical source SHA-256:** `a60f41da6752fdf982822cebb8eb1caccf7a5cd378805bb4a19ccb34930d2930`
- **Canonical source byte length:** `99413`
- **Validation report SHA-256:** `cdf8ce96a468bef127f09a46228b68c46bcff4e1e785cccd591291ec6a2f5bff`
- **Validation date:** `2026-09-17`
- **Current usable `--gf-*` identifiers validated:** `748`
- **Unverified current identifiers:** `0`
- **Integrity gates:** `A=PASS; B=PASS; C=PASS; D=PASS; E=PASS; F=PASS`
- **Official changelog version observed during admission review:** `Gravity Forms 3.1.1.2`
- **Update rule:** if current official Gravity Forms documentation/source or inspected supported-runtime behavior conflicts with the snapshot, current evidence wins for that factual implementation question and this local source must be reconciled and revalidated.
- **Absence rule:** if a required identifier or behavior is not present in the local reference, classify it as `UNKNOWN_FROM_LOCAL_REFERENCE` and check current official documentation rather than guessing.

### Admission review

The source is a project-owned, versioned local engineering snapshot. It is intentionally **not** normative authority for project goals, owner decisions, visual intent, or repository architecture. Its canonical status applies only inside the implementation-fact evidence domain.

The following high-risk/version-sensitive claims were independently checked against current official Gravity Forms-owned documentation during admission and were consistent with the validated snapshot:

- Theme Framework architecture uses Reset → Foundation → Theme Framework layers.
- Foundation remains required underneath custom visual styling.
- Orbital is the default implementation of the Theme Framework.
- Theme Layers provide the integration/orchestration mechanisms around settings and Theme Framework presentation.
- current wrapper/scoping guidance includes `.gform-theme`, `.gform-theme--foundation`, `.gform-theme--framework`, and `.gform-theme--orbital`.
- the current Gravity Forms 2.5 wrapper evidence is internally inconsistent upstream: wrapper-specific/current structure sources publish `.gravity-theme`, while the Theme Framework FAQ still contains `.gform_theme`; the local reference preserves this as `DOCUMENTATION_AMBIGUOUS` rather than treating them as aliases.
- the CSS API is the supported native custom-property contract; undocumented `--gf-*` identifiers must not be invented.
- current Choice Controls use `--gf-ctrl-checkbox-check-*`, `--gf-ctrl-radio-check-*`, and the documented `--gf-ctrl-choice-*` base family.
- current Date Field API uses `--gf-field-date-icon-*` and `--gf-field-date-custom-icon-*`, with `--gf-field-date-ctrl-padding-x-end` for end padding.
- `gform_default_styles` consumes documented style-setting keys rather than arbitrary raw `--gf-*` property names.
- `--gf-form-gap-y` is currently documented with a default of `40px`.
- current Controls Base documentation exposes focus border/outline properties including `--gf-ctrl-border-color-focus`, `--gf-ctrl-outline-color-focus`, and `--gf-ctrl-outline-width-focus`.
- Gravity Forms 2.8 introduced breaking Theme Framework CSS API renames.
- Gravity Forms 2.9 removed deprecated Theme Framework global CSS API properties and changed framework exclusion behavior for labels/descriptions.
- Gravity Forms 3.0 changed form buttons from `<input>` to `<button>`, moved the submission spinner inside the button, and changed the datepicker implementation from jQuery UI to WhatSock.
- the current official FAQ still states that a first-class form theme cannot currently be registered; documented alternatives include `gform_default_styles` and enqueued custom styles.

### Canonical validation evidence

The admitted reference includes a `Canonical Validation Record` and is accompanied by a separate validation report.

The validation established:

```text
GATE A — ZERO-INVENTION                 PASS
GATE B — API-FIDELITY                   PASS
GATE C — SOURCE-DOMAIN AUTHORITY        PASS
GATE D — INTERNAL TOKEN BOUNDARY        PASS
GATE E — HISTORICAL API BOUNDARY        PASS
GATE F — QUICK LOOKUP FIDELITY          PASS
```

The reported `748` current usable identifiers is mechanically consistent with the admitted artifact: the document contains 790 unique literal `--gf-*` token forms; 25 are explicitly wildcard/navigation shorthand and 17 are explicitly historical, negative, or documentation-conflict examples, leaving exactly 748 current usable identifiers.

### Preserved upstream ambiguities

Canonical status does not mean upstream Gravity Forms documentation is internally perfect. The reference explicitly preserves, rather than guesses through, current ambiguities including:

- Gravity Forms 2.5 wrapper: `.gravity-theme` vs `.gform_theme` across current official pages.
- Colors `Used by` references `--gf-ctrl-shadow-color-focus`, while the dedicated current Controls Base API does not define it.
- Design Overview contains stale/conflicting property-name examples relative to dedicated current CSS API pages.
- high-level/historical material can contain pre-2.8 identifiers.
- `--gf-ctrl-btn-icon-color-focus-simple` currently has a self-referential published default.
- `--gf-ctrl-select-dropdown-option-shadow-hover` currently has no published default.
- some public `--gf-*` defaults reference internal-looking `--gform-theme-*` dependencies.
- some Core Concepts modifier names are rendered with ambiguous dash typography.

These ambiguities do not authorize inference. When they are implementation-critical, re-check current official documentation and supported runtime.

### Official pages checked during admission

- https://docs.gravityforms.com/theme-framework-introduction/
- https://docs.gravityforms.com/quick-start-guide/
- https://docs.gravityforms.com/theme-framework/
- https://docs.gravityforms.com/css-api/
- https://docs.gravityforms.com/theme-layers/
- https://docs.gravityforms.com/theme-framework-faq/
- https://docs.gravityforms.com/theme-framework-upgrade-guide/
- https://docs.gravityforms.com/basic-structure/
- https://docs.gravityforms.com/design-overview/
- https://docs.gravityforms.com/form-themes-and-style-settings/
- https://docs.gravityforms.com/gform_default_styles/
- https://docs.gravityforms.com/submit-button-css-selectors/
- https://docs.gravityforms.com/save-and-continue-link-css/
- https://docs.gravityforms.com/form-confirmation/
- https://docs.gravityforms.com/gravity-forms-2-9-key-features/
- https://docs.gravityforms.com/checks-before-upgrading-to-gravity-forms-3-0/
- https://docs.gravityforms.com/gravityforms-change-log/
- https://docs.css.gravity.com/
