---
title: "Gravity Forms Theme Framework — Canonical Engineering Reference"
document_type: "local-engineering-reference"
authority_domain: "implementation-fact-evidence"
authority_source: "Official Gravity Forms Documentation"
source_roots:
  - "https://docs.css.gravity.com/"
  - "https://docs.gravityforms.com/"
snapshot_date: "2026-09-17"
status: "canonical-project-reference"
update_policy: "revalidate-on-gravity-forms-theme-framework-change"
identifier_policy: "zero-invention"
api_fidelity_policy: "verify-identifier-owner-default-and-dependency"
---

# Gravity Forms Theme Framework — Canonical Engineering Reference

## 0. How to Use This Reference

This document is a **versioned local engineering snapshot** of the public Gravity Forms Theme Framework contract and its current documented CSS API.

Its authority domain is **implementation-fact evidence**. It exists to help coding agents verify current Gravity Forms implementation facts before they write or review theme code. It is **not** the normative authority for project goals, product decisions, visual design intent, or repository-specific architecture.

Current official Gravity Forms documentation remains authoritative for Gravity Forms implementation facts. If current official documentation conflicts with this snapshot, the current official documentation wins and this file must be revalidated and updated.

Use this decision order:

1. Consult this reference first.
2. Prefer documented Gravity Forms Theme Framework APIs.
3. Never invent a `--gf-*` property.
4. Prefer an appropriate higher-level documented token before overriding several downstream tokens.
5. Apply documented properties at the narrowest appropriate documented scope.
6. If required behavior is absent, classify it as `UNKNOWN_FROM_LOCAL_REFERENCE`.
7. Consult the current official Gravity Forms documentation.
8. If current official documentation conflicts with this snapshot, current official documentation wins.
9. Update this reference when the public contract changes.

### REFERENCE AUTHORITY RULE

When implementing or reviewing Gravity Forms Theme Framework code:

1. Consult this reference before inventing selectors, variables, wrapper classes, or framework behavior.
2. Prefer documented Gravity Forms Theme Framework APIs and CSS custom properties when they provide the required capability.
3. Never invent `--gf-*` properties.
4. Preserve documented framework layering, scoping, inheritance, and component boundaries.
5. If required behavior is not documented here, classify it as `UNKNOWN_FROM_LOCAL_REFERENCE`.
6. Only then consult the current official Gravity Forms documentation.
7. If current official documentation conflicts with this snapshot, current official documentation wins and this reference should be updated.

### Evidence classifications

| Label | Meaning |
|---|---|
| `DOCUMENTED PUBLIC CONTRACT` | Explicitly documented by current official Gravity Forms documentation or CSS API reference. |
| `IMPLEMENTATION DETAIL` | Visible in official implementation-oriented material but not established as stable public API. |
| `DOCUMENTATION AMBIGUOUS` | Official documentation is incomplete, conflicting, malformed, or unclear. |
| `NOT DOCUMENTED IN OFFICIAL REFERENCE` | Plausible behavior or identifier not established by inspected official documentation. |
| `UNKNOWN_FROM_LOCAL_REFERENCE` | Information is absent from this snapshot and must be revalidated upstream. |

### Identifier safety rule

A name that *looks like* a Gravity Forms property is not evidence that it exists.

```text
Plausible-looking name
        ≠
Documented API identifier
```

No naming pattern may be extrapolated into a new `--gf-*` property. Exact spelling is part of the API contract.

---

## 1. Framework Mental Model

Gravity Forms introduced the Theme Framework in Gravity Forms 2.7. At its core is a CSS API based on native CSS custom properties. Orbital is the default implementation of that framework.

```text
WordPress / site theme
        │
        │ typography and surrounding site context
        ▼
┌──────────────────────────┐
│ Reset                    │
│ scoped GF reset          │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ Foundation               │
│ functional form/layout   │
│ behavior                 │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ Theme Framework          │
│ public CSS API           │
│ global --gf-* properties │
│ Orbital defaults         │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ Local/component API      │
│ controls / fields / form │
│ UI                       │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ Project customization    │
│ documented overrides     │
└──────────────────────────┘
```

A separate integration mechanism exists around the CSS framework:

```text
Block/style settings
        │
        ▼
Theme Layers
        │
        ├── group/enqueue styles
        ├── manage settings
        ├── connect settings → CSS API
        ├── control application
        └── control priority
        │
        ▼
Theme Framework
```

Keep these concepts separate:

```text
Theme Framework = CSS/API contract
Theme Layers     = integration/orchestration mechanism
Foundation       = functional/layout base
Orbital          = default Theme Framework implementation
```

Official architecture sources:

- https://docs.gravityforms.com/theme-framework-introduction/
- https://docs.gravityforms.com/quick-start-guide/
- https://docs.gravityforms.com/theme-framework/
- https://docs.gravityforms.com/theme-layers/
- https://docs.gravityforms.com/css-api/

---

## 2. Framework Layers

Gravity Forms documents three primary stylesheet layers loaded in order:

```text
Reset
  ↓
Foundation
  ↓
Theme Framework
```

### 2.1 Reset

`DOCUMENTED PUBLIC CONTRACT`

The Reset layer:

- applies within Gravity Forms markup;
- establishes a predictable base;
- intentionally allows typography such as headings, paragraphs, and links to inherit from the WordPress theme;
- uses `:where(...)` with exclusions;
- is required by the Theme Framework.

Official implementation file documented by Gravity Forms:

```text
assets/css/src/theme/framework/gravity-forms-theme-reset.pcss
```

### 2.2 Foundation

`DOCUMENTED PUBLIC CONTRACT`

Foundation is not intended to be used as a standalone visual theme.

It provides functional styles required by form themes, including:

- field functionality;
- field layout;
- enhanced controls;
- supporting form behavior.

Gravity Forms explicitly states that Foundation should remain included when creating a custom theme.

Official implementation file:

```text
assets/css/src/theme/foundation/gravity-forms-theme-foundation.pcss
```

### 2.3 Theme Framework

`DOCUMENTED PUBLIC CONTRACT`

The Theme Framework:

- contains most of the CSS API;
- exposes public customization properties;
- applies Orbital-compatible defaults;
- depends on Reset and Foundation.

Official implementation file:

```text
assets/css/src/theme/framework/gravity-forms-theme-framework.pcss
```

### 2.4 Internal framework taxonomy

Gravity Forms describes these source areas:

| Area | Responsibility |
|---|---|
| `api` | Global API/custom-property abstraction |
| `base` | Base/global form styling |
| `controls` | Raw form controls/components |
| `fields` | Gravity Forms field-specific UI |
| `form` | Form-level UI |
| `layout` | Layout behavior |

This taxonomy is useful for understanding ownership but should not be treated as permission to depend on arbitrary internal selectors.

---

## 3. Scoping and Inheritance

### 3.1 Documented theme wrapper classes

| Theme/scope | Preferred current wrapper from current wrapper-specific documentation |
|---|---|
| Legacy & Gravity Forms 2.5 without Framework | `.gform-theme--no-framework` |
| Legacy pre-2.5 | `.gform_legacy_markup_wrapper` |
| Gravity Forms 2.5 Theme | `.gravity-theme` |
| Theme Framework | `.gform-theme` |
| Foundation | `.gform-theme--foundation` |
| Framework | `.gform-theme--framework` |
| Orbital | `.gform-theme--orbital` |

A normal Orbital form can carry:

```text
.gform-theme
.gform-theme--foundation
.gform-theme--framework
.gform-theme--orbital
```

**Gravity Forms 2.5 wrapper warning:** current official documentation is internally inconsistent. Quick Start, Core Concepts, and CSS Element Naming Structure publish `.gravity-theme`, while the current Theme Framework FAQ still publishes `.gform_theme` in its “Writing different styles for different form themes” example. This is preserved as `DOCUMENTATION AMBIGUOUS` in §16. Do not treat the two spellings as interchangeable without runtime/source verification.

### 3.2 Form and field identifiers

Documented form wrapper pattern:

```text
#gform_wrapper_{form_id}
```

Documented field wrapper pattern:

```text
#field_{form_id}_{field_id}
```

### 3.3 Scope hierarchy

```text
Global/framework scope
        ↓
all matching forms

Form scope
        ↓
one form wherever targeted

Rendered/block scope
        ↓
one embedded instance

Field-type scope
        ↓
one family of fields

Field scope
        ↓
one field
```

Multiple forms can exist on the same page. Scope isolation is therefore a first-class requirement.

### 3.4 Documented targeting patterns

All Theme Framework forms:

```css
.gform-theme--framework
```

One form:

```css
.gform-theme--framework#gform_wrapper_{form_id}
```

Forms on one WordPress page:

```css
.page-id-{page_id} .gform-theme--framework
```

A field type:

```css
.gform-theme--framework .gfield--type-{type}
```

One field:

```css
.gform-theme--framework #field_{form_id}_{field_id}
```

### 3.5 Field type classes

Documented field classes include:

```text
.gfield--type-{field type}
.gfield--type-choice
.gfield--input-type-{input type}
```

`gfield--type-choice` applies when the field type is checkbox, radio, consent, or an applicable field input-type setting is checkbox/radio.

### 3.6 Exclusion/reset utilities

Documented utilities:

```text
.gform-theme__disable
.gform-theme__disable-reset
.gform-theme__disable-framework
.gform-theme__no-reset--el
.gform-theme__no-reset--children
```

| Class | Effect |
|---|---|
| `.gform-theme__disable` | Exclude framework and reset for the element and descendants |
| `.gform-theme__disable-reset` | Exclude reset |
| `.gform-theme__disable-framework` | Exclude framework styling |
| `.gform-theme__no-reset--el` | Documented design utility for avoiding reset on an element |
| `.gform-theme__no-reset--children` | Documented design utility for avoiding reset on descendants |

### 3.7 CSS inheritance

Theme Framework properties are native CSS custom properties and follow CSS cascade/inheritance.

```css
.gform-theme--framework {
    --gf-color-primary: #2563eb;
}
```

Do not assume every component consumes every higher-level property. Follow documented dependencies.

---

## 4. CSS API Mental Model

Gravity Forms documents globally and locally scoped custom properties. The current CSS API article recommends favoring the global API where appropriate.

```text
GLOBAL CSS API
        ↓
high-level and component global properties
        ↓
LOCAL CSS API
        ↓
element-local properties
        ↓
CSS declaration
```

### 4.1 Global CSS API

Global properties are scoped to applicable framework wrappers such as:

```text
.gform-theme--foundation
.gform-theme--framework
```

Examples:

```text
--gf-color-primary
--gf-ctrl-bg-color
--gf-ctrl-radius
```

### 4.2 Local CSS API

Current official CSS API documentation gives examples including:

```text
--gf-local-bg-color
--gf-local-radius
--gf-local-shadow
--gf-local-color
```

Representative flow:

```text
--gf-ctrl-bg-color
        ↓
--gf-local-bg-color
        ↓
background-color
```

Do not extrapolate additional `--gf-local-*` identifiers from naming patterns.

### 4.3 Dependency examples

```text
--gf-color-in-ctrl
        ↓
--gf-ctrl-bg-color
        ↓
--gf-local-bg-color
        ↓
background-color
```

```text
--gf-color-primary
        ↓
--gf-ctrl-border-color-focus
```

```text
--gf-radius
        ↓
--gf-ctrl-radius
        ↓
component radius
```

When one high-level token correctly represents the desired semantic change, prefer that token over manually overriding all downstream values.

### 4.4 State-specific properties

Many APIs expose explicit state variants:

```text
base
hover
focus
disabled
error
selected
active
complete
loading
```

Do not assume a base property controls every state.

---

# 5. Base / Global API

Current CSS API taxonomy exposes these base groups:

```text
Borders
Colors
Field Layout & Spacing
Form Layout & Spacing
Icons
Transitions & Animation
Typography
```

## 5.1 Borders

| Property | Purpose | Default |
|---|---|---|
| `--gf-radius` | Base form UI radius | `3px` |
| `--gf-radius-max-sm` | Max radius for small-sized controls | `2px` |
| `--gf-radius-max-md` | Max radius for medium-sized controls | `3px` |
| `--gf-radius-max-lg` | Max radius for large-sized controls | `8px` |

Source: https://docs.css.gravity.com/framework.api._borders.html

## 5.2 Colors

### Primary

| Property | Default |
|---|---|
| `--gf-color-primary` | `#204ce5` |
| `--gf-color-primary-rgb` | `45, 127, 251` |
| `--gf-color-primary-contrast` | `#fff` |
| `--gf-color-primary-contrast-rgb` | `255, 255, 255` |
| `--gf-color-primary-darker` | `#044ad3` |
| `--gf-color-primary-lighter` | `#044ad3` |

The current official CSS API publishes the same displayed default for `--gf-color-primary-darker` and `--gf-color-primary-lighter`. Do not silently “correct” official values.

### Secondary

| Property | Default |
|---|---|
| `--gf-color-secondary` | `#fff` |
| `--gf-color-secondary-rgb` | `255, 255, 255` |
| `--gf-color-secondary-contrast` | `#112337` |
| `--gf-color-secondary-contrast-rgb` | `17, 35, 55` |
| `--gf-color-secondary-darker` | `#f2f3f5` |
| `--gf-color-secondary-lighter` | `#f2f3f5` |

### Outside-control dark

| Property | Default |
|---|---|
| `--gf-color-out-ctrl-dark` | `#585e6a` |
| `--gf-color-out-ctrl-dark-rgb` | `88, 94, 106` |
| `--gf-color-out-ctrl-dark-darker` | `#112337` |
| `--gf-color-out-ctrl-dark-lighter` | `#686e77` |

### Outside-control light

| Property | Default |
|---|---|
| `--gf-color-out-ctrl-light` | `#e5e7eb` |
| `--gf-color-out-ctrl-light-rgb` | `229, 231, 235` |
| `--gf-color-out-ctrl-light-darker` | `#d2d5db` |
| `--gf-color-out-ctrl-light-lighter` | `#f2f3f5` |

### Inside-control

| Property | Default |
|---|---|
| `--gf-color-in-ctrl` | `#fff` |
| `--gf-color-in-ctrl-rgb` | `255, 255, 255` |
| `--gf-color-in-ctrl-contrast` | `#112337` |
| `--gf-color-in-ctrl-contrast-rgb` | `17, 35, 55` |
| `--gf-color-in-ctrl-darker` | `#f2f3f5` |
| `--gf-color-in-ctrl-lighter` | `#f2f3f5` |

### Inside-control primary

| Property | Default |
|---|---|
| `--gf-color-in-ctrl-primary` | `var(--gf-color-primary)` |
| `--gf-color-in-ctrl-primary-rgb` | `var(--gf-color-primary-rgb)` |
| `--gf-color-in-ctrl-primary-contrast` | `var(--gf-color-primary-contrast)` |
| `--gf-color-in-ctrl-primary-contrast-rgb` | `var(--gf-color-primary-contrast-rgb)` |
| `--gf-color-in-ctrl-primary-darker` | `var(--gf-color-primary-darker)` |
| `--gf-color-in-ctrl-primary-lighter` | `var(--gf-color-primary-lighter)` |

### Inside-control dark

| Property | Default |
|---|---|
| `--gf-color-in-ctrl-dark` | `#585e6a` |
| `--gf-color-in-ctrl-dark-rgb` | `88, 94, 106` |
| `--gf-color-in-ctrl-dark-darker` | `#112337` |
| `--gf-color-in-ctrl-dark-lighter` | `#686e77` |

### Inside-control light

| Property | Default |
|---|---|
| `--gf-color-in-ctrl-light` | `#e5e7eb` |
| `--gf-color-in-ctrl-light-rgb` | `229, 231, 235` |
| `--gf-color-in-ctrl-light-darker` | `#d2d5db` |
| `--gf-color-in-ctrl-light-lighter` | `#f2f3f5` |

### Semantic colors

| Property | Default |
|---|---|
| `--gf-color-danger` | `#c02b0a` |
| `--gf-color-danger-rgb` | `192, 43, 10` |
| `--gf-color-danger-contrast` | `#fff` |
| `--gf-color-danger-contrast-rgb` | `255, 255, 255` |
| `--gf-color-success` | `#399f4b` |
| `--gf-color-success-rgb` | `57, 159, 75` |
| `--gf-color-success-contrast` | `#fff` |
| `--gf-color-success-contrast-rgb` | `255, 255, 255` |

Source: https://docs.css.gravity.com/framework.api._colors.html

### Focus-property upstream conflict

`DOCUMENTATION AMBIGUOUS`

The current Colors API page lists `--gf-ctrl-shadow-color-focus` in the **Used by** column for `--gf-color-primary-rgb`, but the current dedicated **Controls — Base** API inventory does not define `--gf-ctrl-shadow-color-focus`.

For new code:

- do **not** treat `--gf-ctrl-shadow-color-focus` as a verified current public API identifier;
- use the dedicated Controls — Base page as the exact current control identifier inventory;
- use the currently documented focus APIs there, including `--gf-ctrl-border-color-focus`, `--gf-ctrl-outline-color-focus`, and `--gf-ctrl-outline-width-focus`.

Sources:

- https://docs.css.gravity.com/framework.api._colors.html
- https://docs.css.gravity.com/framework.controls.default._api-global.html

## 5.3 Field Layout & Spacing

| Property | Default |
|---|---|
| `--gf-padding-x` | `12px` |
| `--gf-padding-y` | `12px` |
| `--gf-label-space-primary` | `8px` |
| `--gf-label-choice-field-space-primary` | `12px` |
| `--gf-label-space-x-secondary` | `12px` |
| `--gf-label-space-y-sm-secondary` | `-1px` |
| `--gf-label-space-y-md-secondary` | `0` |
| `--gf-label-space-y-lg-secondary` | `1px` |
| `--gf-label-space-y-xl-secondary` | `4px` |
| `--gf-label-space-y-secondary` | `var(--gf-label-space-y-md-secondary)` |
| `--gf-label-space-tertiary` | `8px` |
| `--gf-desc-space` | `8px` |
| `--gf-desc-choice-field-space` | `12px` |

Source: https://docs.css.gravity.com/framework.api._layout.html

## 5.4 Form Layout & Spacing

| Property | Default |
|---|---|
| `--gf-form-gap-x` | `16px` |
| `--gf-form-gap-y` | `40px` |
| `--gf-form-footer-margin-y-start` | `24px` |
| `--gf-form-footer-gap` | `8px` |
| `--gf-field-gap-x` | `12px` |
| `--gf-field-gap-y` | `12px` |
| `--gf-field-date-width` | `168px` |
| `--gf-field-time-width` | `110px` |
| `--gf-field-list-btns-gap` | `8px` |
| `--gf-field-list-btns-width` | `calc(32px + var(--gf-field-list-btns-gap) + var(--gf-field-gap-x))` |
| `--gf-field-pg-steps-gap-y` | `8px` |
| `--gf-field-pg-steps-gap-x` | `24px` |
| `--gf-label-width` | `30%` |
| `--gf-label-req-gap` | `6px` |

Source: https://docs.css.gravity.com/foundation.api._layout.html

## 5.5 Icons

Documented icon API:

```text
--gf-icon-font-family
--gf-icon-font-size
--gf-icon-ctrl-checkbox
--gf-icon-ctrl-select-down
--gf-icon-ctrl-select-up
--gf-icon-ctrl-select
--gf-icon-ctrl-search
--gf-icon-ctrl-cancel
--gf-icon-ctrl-number
--gf-icon-ctrl-pwd-hidden
--gf-icon-ctrl-pwd-visible
--gf-icon-ctrl-list-item-add
--gf-icon-ctrl-list-item-remove
--gf-icon-ctrl-save-continue
--gf-icon-ctrl-pg-numbers-complete
--gf-icon-ctrl-file
--gf-icon-ctrl-file-completed
--gf-icon-ctrl-file-cancel
--gf-icon-ctrl-file-remove
--gf-icon-ctrl-datepicker
--gf-icon-ctrl-datepicker-left
--gf-icon-ctrl-datepicker-right
--gf-icon-ctrl-img-choice-placeholder
--gf-icon-tooltip-error
```

Key defaults:

```text
--gf-icon-font-family = "gform-icons-orbital"
--gf-icon-font-size   = 20px
```

Several icon properties use encoded SVG data URIs. This reference intentionally does not duplicate large encoded SVG literals. Retrieve the literal from the official API page if exact data is required.

Source: https://docs.css.gravity.com/framework.api._icons.html

## 5.6 Transitions

| Property | Default |
|---|---|
| `--gf-transition-duration` | `0.15s` |
| `--gf-transition-ctrl` | `var(--gf-transition-duration)` |

Source: https://docs.css.gravity.com/framework.api._transitions.html

## 5.7 Typography

### Base

| Property | Default |
|---|---|
| `--gf-font-family-base` | `initial` |
| `--gf-font-style-base` | `normal` |

`--gf-font-family-base: initial` is documented as allowing inheritance from the surrounding theme font family.

### Primary

| Property | Default |
|---|---|
| `--gf-font-family-primary` | `var(--gf-font-family-base)` |
| `--gf-font-size-primary` | `14px` |
| `--gf-font-style-primary` | `var(--gf-font-style-base)` |
| `--gf-font-weight-primary` | `400` |
| `--gf-letter-spacing-primary` | `0` |
| `--gf-line-height-primary` | `1.5` |

### Secondary

| Property | Default |
|---|---|
| `--gf-font-family-secondary` | `var(--gf-font-family-base)` |
| `--gf-font-size-secondary` | `14px` |
| `--gf-font-style-secondary` | `var(--gf-font-style-base)` |
| `--gf-font-weight-secondary` | `500` |
| `--gf-letter-spacing-secondary` | `0` |
| `--gf-line-height-secondary` | `1.43` |

### Tertiary

| Property | Default |
|---|---|
| `--gf-font-family-tertiary` | `var(--gf-font-family-base)` |
| `--gf-font-size-tertiary` | `14px` |
| `--gf-font-style-tertiary` | `var(--gf-font-style-base)` |
| `--gf-font-weight-tertiary` | `400` |
| `--gf-letter-spacing-tertiary` | `0` |
| `--gf-line-height-tertiary` | `1.43` |

Source: https://docs.css.gravity.com/framework.api._typography.html

---

# 6. Controls API

## 6.1 Base Control

### Background

| Property | Default |
|---|---|
| `--gf-ctrl-bg-color` | `var(--gf-color-in-ctrl)` |
| `--gf-ctrl-bg-color-hover` | `var(--gf-ctrl-bg-color)` |
| `--gf-ctrl-bg-color-focus` | `var(--gf-ctrl-bg-color)` |
| `--gf-ctrl-bg-color-disabled` | `var(--gf-color-in-ctrl-light-lighter)` |
| `--gf-ctrl-bg-color-error` | `var(--gf-ctrl-bg-color)` |

### Border / outline

| Property | Default |
|---|---|
| `--gf-ctrl-border-color` | `var(--gf-color-in-ctrl-dark-lighter)` |
| `--gf-ctrl-border-color-hover` | `var(--gf-ctrl-border-color)` |
| `--gf-ctrl-border-color-focus` | `var(--gf-color-primary)` |
| `--gf-ctrl-border-color-disabled` | `var(--gf-color-in-ctrl-light-darker)` |
| `--gf-ctrl-border-color-error` | `var(--gf-color-danger)` |
| `--gf-ctrl-border-style` | `solid` |
| `--gf-ctrl-border-width` | `1px` |
| `--gf-ctrl-radius` | `var(--gf-radius)` |
| `--gf-ctrl-radius-max-sm` | `min(var(--gf-ctrl-radius), var(--gf-radius-max-sm))` |
| `--gf-ctrl-radius-max-md` | `min(var(--gf-ctrl-radius), var(--gf-radius-max-md))` |
| `--gf-ctrl-radius-max-lg` | `min(var(--gf-ctrl-radius), var(--gf-radius-max-lg))` |
| `--gf-ctrl-outline-color` | `transparent` |
| `--gf-ctrl-outline-color-focus` | `rgba(var(--gf-color-primary-rgb), 0.65)` |
| `--gf-ctrl-outline-offset` | `1px` |
| `--gf-ctrl-outline-style` | `solid` |
| `--gf-ctrl-outline-width` | `0` |
| `--gf-ctrl-outline-width-focus` | `3px` |

### Text / icon

| Property | Default |
|---|---|
| `--gf-ctrl-color` | `var(--gf-color-in-ctrl-contrast)` |
| `--gf-ctrl-color-hover` | `var(--gf-ctrl-color)` |
| `--gf-ctrl-color-focus` | `var(--gf-ctrl-color)` |
| `--gf-ctrl-color-disabled` | `rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.6)` |
| `--gf-ctrl-color-error` | `var(--gf-ctrl-color)` |
| `--gf-ctrl-icon-color` | `var(--gf-color-in-ctrl-dark-lighter)` |
| `--gf-ctrl-icon-color-hover` | `var(--gf-color-in-ctrl-dark-darker)` |
| `--gf-ctrl-icon-color-focus` | `var(--gf-ctrl-icon-color-hover)` |
| `--gf-ctrl-icon-color-disabled` | `var(--gf-ctrl-icon-color)` |

### Effects / sizing / spacing

| Property | Default |
|---|---|
| `--gf-ctrl-shadow` | `0 1px 4px rgba(18, 25, 97, 0.0779552)` |
| `--gf-ctrl-accent-color` | `var(--gf-color-in-ctrl-primary)` |
| `--gf-ctrl-appearance` | `none` |
| `--gf-ctrl-size-sm` | `35px` |
| `--gf-ctrl-size-md` | `38px` |
| `--gf-ctrl-size-lg` | `47px` |
| `--gf-ctrl-size-xl` | `54px` |
| `--gf-ctrl-size` | `var(--gf-ctrl-size-md)` |
| `--gf-ctrl-padding-x` | `var(--gf-padding-x)` |
| `--gf-ctrl-padding-y` | `0` |
| `--gf-ctrl-transition` | `var(--gf-transition-ctrl)` |

### Typography

| Property | Default |
|---|---|
| `--gf-ctrl-font-family` | `var(--gf-font-family-primary)` |
| `--gf-ctrl-font-size` | `var(--gf-font-size-primary)` |
| `--gf-ctrl-font-style` | `var(--gf-font-style-base)` |
| `--gf-ctrl-font-weight` | `var(--gf-font-weight-primary)` |
| `--gf-ctrl-letter-spacing` | `var(--gf-letter-spacing-primary)` |
| `--gf-ctrl-line-height` | `var(--gf-ctrl-size)` |

### Placeholder

| Property | Default |
|---|---|
| `--gf-ctrl-placeholder-color` | `rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.7)` |
| `--gf-ctrl-placeholder-font-family` | `var(--gf-ctrl-font-family)` |
| `--gf-ctrl-placeholder-font-size` | `var(--gf-ctrl-font-size)` |
| `--gf-ctrl-placeholder-font-style` | `var(--gf-ctrl-font-style)` |
| `--gf-ctrl-placeholder-font-weight` | `var(--gf-ctrl-font-weight)` |
| `--gf-ctrl-placeholder-letter-spacing` | `var(--gf-ctrl-letter-spacing)` |
| `--gf-ctrl-placeholder-opacity` | `1` |

Source: https://docs.css.gravity.com/framework.controls.default._api-global.html

## 6.2 Buttons

### Button base

```text
--gf-ctrl-btn-radius
--gf-ctrl-btn-shadow
--gf-ctrl-btn-shadow-hover
--gf-ctrl-btn-shadow-focus
--gf-ctrl-btn-shadow-disabled
--gf-ctrl-btn-opacity
--gf-ctrl-btn-opacity-disabled
--gf-ctrl-btn-size-xs
--gf-ctrl-btn-size-sm
--gf-ctrl-btn-size-md
--gf-ctrl-btn-size-lg
--gf-ctrl-btn-size-xl
--gf-ctrl-btn-size
--gf-ctrl-btn-padding-x-xs
--gf-ctrl-btn-padding-x-sm
--gf-ctrl-btn-padding-x-md
--gf-ctrl-btn-padding-x-lg
--gf-ctrl-btn-padding-x-xl
--gf-ctrl-btn-padding-x
--gf-ctrl-btn-padding-y
--gf-ctrl-btn-font-family
--gf-ctrl-btn-font-size-xs
--gf-ctrl-btn-font-size-sm
--gf-ctrl-btn-font-size-md
--gf-ctrl-btn-font-size-lg
--gf-ctrl-btn-font-size-xl
--gf-ctrl-btn-font-size
--gf-ctrl-btn-font-style
--gf-ctrl-btn-font-weight
--gf-ctrl-btn-letter-spacing
--gf-ctrl-btn-line-height
--gf-ctrl-btn-text-decoration
--gf-ctrl-btn-text-transform
--gf-ctrl-btn-icon
--gf-ctrl-btn-icon-size
--gf-ctrl-btn-icon-gap
--gf-ctrl-btn-icon-transition
```

Key published defaults include:

| Property | Default |
|---|---|
| `--gf-ctrl-btn-radius` | `var(--gf-radius)` |
| `--gf-ctrl-btn-shadow` | `0 1px 4px rgba(18, 25, 97, 0.0779552)` |
| `--gf-ctrl-btn-opacity` | `1` |
| `--gf-ctrl-btn-opacity-disabled` | `0.5` |
| `--gf-ctrl-btn-size-xs` | `30px` |
| `--gf-ctrl-btn-size-sm` | `var(--gf-ctrl-size-sm)` |
| `--gf-ctrl-btn-size-md` | `var(--gf-ctrl-size-md)` |
| `--gf-ctrl-btn-size-lg` | `var(--gf-ctrl-size-lg)` |
| `--gf-ctrl-btn-size-xl` | `var(--gf-ctrl-size-xl)` |
| `--gf-ctrl-btn-size` | `var(--gf-ctrl-btn-size-md)` |
| `--gf-ctrl-btn-padding-x-xs` | `8px` |
| `--gf-ctrl-btn-padding-x-sm` | `12px` |
| `--gf-ctrl-btn-padding-x-md` | `16px` |
| `--gf-ctrl-btn-padding-x-lg` | `20px` |
| `--gf-ctrl-btn-padding-x-xl` | `24px` |
| `--gf-ctrl-btn-padding-x` | `var(--gf-ctrl-btn-padding-x-md)` |
| `--gf-ctrl-btn-padding-y` | `0` |
| `--gf-ctrl-btn-font-size-xs` | `12px` |
| `--gf-ctrl-btn-font-size-sm` | `14px` |
| `--gf-ctrl-btn-font-size-md` | `14px` |
| `--gf-ctrl-btn-font-size-lg` | `16px` |
| `--gf-ctrl-btn-font-size-xl` | `16px` |
| `--gf-ctrl-btn-font-size` | `var(--gf-ctrl-btn-font-size-md)` |
| `--gf-ctrl-btn-font-weight` | `500` |
| `--gf-ctrl-btn-line-height` | `1` |
| `--gf-ctrl-btn-text-decoration` | `none` |
| `--gf-ctrl-btn-text-transform` | `none` |
| `--gf-ctrl-btn-icon` | `none` |
| `--gf-ctrl-btn-icon-size` | `var(--gf-icon-font-size)` |
| `--gf-ctrl-btn-icon-gap` | `6px` |

### Primary button

```text
--gf-ctrl-btn-bg-color-primary
--gf-ctrl-btn-bg-color-hover-primary
--gf-ctrl-btn-bg-color-focus-primary
--gf-ctrl-btn-bg-color-disabled-primary
--gf-ctrl-btn-border-color-primary
--gf-ctrl-btn-border-color-hover-primary
--gf-ctrl-btn-border-color-focus-primary
--gf-ctrl-btn-border-color-disabled-primary
--gf-ctrl-btn-border-style-primary
--gf-ctrl-btn-border-width-primary
--gf-ctrl-btn-color-primary
--gf-ctrl-btn-color-hover-primary
--gf-ctrl-btn-color-focus-primary
--gf-ctrl-btn-color-disabled-primary
--gf-ctrl-btn-icon-color-primary
--gf-ctrl-btn-icon-color-hover-primary
--gf-ctrl-btn-icon-color-focus-primary
--gf-ctrl-btn-icon-color-disabled-primary
```

Important relationships:

```text
--gf-ctrl-btn-bg-color-primary
    = var(--gf-color-primary)

--gf-ctrl-btn-bg-color-hover-primary
    = var(--gf-color-primary-darker)

--gf-ctrl-btn-color-primary
    = var(--gf-color-primary-contrast)
```

### Secondary button

```text
--gf-ctrl-btn-bg-color-secondary
--gf-ctrl-btn-bg-color-hover-secondary
--gf-ctrl-btn-bg-color-focus-secondary
--gf-ctrl-btn-bg-color-disabled-secondary
--gf-ctrl-btn-border-color-secondary
--gf-ctrl-btn-border-color-hover-secondary
--gf-ctrl-btn-border-color-focus-secondary
--gf-ctrl-btn-border-color-disabled-secondary
--gf-ctrl-btn-border-style-secondary
--gf-ctrl-btn-border-width-secondary
--gf-ctrl-btn-color-secondary
--gf-ctrl-btn-color-hover-secondary
--gf-ctrl-btn-color-focus-secondary
--gf-ctrl-btn-color-disabled-secondary
--gf-ctrl-btn-icon-color-secondary
--gf-ctrl-btn-icon-color-hover-secondary
--gf-ctrl-btn-icon-color-focus-secondary
--gf-ctrl-btn-icon-color-disabled-secondary
```

The current official default for `--gf-ctrl-btn-border-color-focus-secondary` is:

```text
var(--gf-ctrl-btn-bg-color-hover-primary)
```

Preserve that published dependency unless official documentation changes.

### Control button

```text
--gf-ctrl-btn-bg-color-ctrl
--gf-ctrl-btn-bg-color-hover-ctrl
--gf-ctrl-btn-bg-color-focus-ctrl
--gf-ctrl-btn-bg-color-disabled-ctrl
--gf-ctrl-btn-border-color-ctrl
--gf-ctrl-btn-border-color-hover-ctrl
--gf-ctrl-btn-border-color-focus-ctrl
--gf-ctrl-btn-border-color-disabled-ctrl
--gf-ctrl-btn-border-style-ctrl
--gf-ctrl-btn-border-width-ctrl
--gf-ctrl-btn-color-ctrl
--gf-ctrl-btn-color-hover-ctrl
--gf-ctrl-btn-color-focus-ctrl
--gf-ctrl-btn-color-disabled-ctrl
--gf-ctrl-btn-icon-color-ctrl
--gf-ctrl-btn-icon-color-hover-ctrl
--gf-ctrl-btn-icon-color-focus-ctrl
--gf-ctrl-btn-icon-color-disabled-ctrl
```

### Simple button

```text
--gf-ctrl-btn-bg-color-simple
--gf-ctrl-btn-bg-color-hover-simple
--gf-ctrl-btn-bg-color-focus-simple
--gf-ctrl-btn-bg-color-disabled-simple
--gf-ctrl-btn-border-color-simple
--gf-ctrl-btn-border-color-hover-simple
--gf-ctrl-btn-border-color-focus-simple
--gf-ctrl-btn-border-color-disabled-simple
--gf-ctrl-btn-border-style-simple
--gf-ctrl-btn-border-width-simple
--gf-ctrl-btn-color-simple
--gf-ctrl-btn-color-hover-simple
--gf-ctrl-btn-color-focus-simple
--gf-ctrl-btn-color-disabled-simple
--gf-ctrl-btn-shadow-simple
--gf-ctrl-btn-shadow-hover-simple
--gf-ctrl-btn-shadow-focus-simple
--gf-ctrl-btn-shadow-disabled-simple
--gf-ctrl-btn-size-simple
--gf-ctrl-btn-icon-color-simple
--gf-ctrl-btn-icon-color-hover-simple
--gf-ctrl-btn-icon-color-focus-simple
--gf-ctrl-btn-icon-color-disabled-simple
```

`DOCUMENTATION AMBIGUOUS`

The current official API publishes:

```text
--gf-ctrl-btn-icon-color-focus-simple
    = var(--gf-ctrl-btn-icon-color-focus-simple)
```

This is self-referential. Do not guess a replacement dependency.

Source: https://docs.css.gravity.com/framework.controls.button._api-global.html

## 6.3 Choice Controls

### Choice base

| Property | Default |
|---|---|
| `--gf-ctrl-choice-check-color` | `var(--gf-color-in-ctrl-primary)` |
| `--gf-ctrl-choice-check-color-disabled` | `rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.2)` |
| `--gf-ctrl-choice-size-sm` | `18px` |
| `--gf-ctrl-choice-size-md` | `20px` |
| `--gf-ctrl-choice-size-lg` | `22px` |
| `--gf-ctrl-choice-size-xl` | `28px` |
| `--gf-ctrl-choice-size` | `var(--gf-ctrl-choice-size-md)` |

### Checkbox

**Exact current identifiers:**

| Property | Default |
|---|---|
| `--gf-ctrl-checkbox-check-radius` | `var(--gf-ctrl-radius-max-sm)` |
| `--gf-ctrl-checkbox-check-size-sm` | `12px` |
| `--gf-ctrl-checkbox-check-size-md` | `initial` |
| `--gf-ctrl-checkbox-check-size-lg` | `15px` |
| `--gf-ctrl-checkbox-check-size-xl` | `19px` |
| `--gf-ctrl-checkbox-check-size` | `var(--gf-ctrl-checkbox-check-size-md)` |

### Radio

**Exact current identifiers:**

| Property | Default |
|---|---|
| `--gf-ctrl-radio-check-radius` | `50%` |
| `--gf-ctrl-radio-check-content` | `""` |
| `--gf-ctrl-radio-check-size-sm` | `6px` |
| `--gf-ctrl-radio-check-size-md` | `7px` |
| `--gf-ctrl-radio-check-size-lg` | `8px` |
| `--gf-ctrl-radio-check-size-xl` | `10px` |
| `--gf-ctrl-radio-check-size` | `var(--gf-ctrl-radio-check-size-md)` |

### Explicitly rejected nonexistent aliases

The following are listed **only as negative examples**. They are absent from the current official Choice Controls API and are not current API identifiers:

```text
--gf-ctrl-choice-checkbox-radius
--gf-ctrl-choice-checkbox-check-size-md
--gf-ctrl-choice-radio-radius
--gf-ctrl-choice-radio-size-md
```

Source: https://docs.css.gravity.com/framework.controls.choice._api-global.html

## 6.4 Date Picker Control

### Base

```text
--gf-ctrl-date-picker-bg-color
--gf-ctrl-date-picker-shadow
--gf-ctrl-date-picker-padding-y
--gf-ctrl-date-picker-padding-y-viewport-sm
--gf-ctrl-date-picker-padding-x
--gf-ctrl-date-picker-padding-x-viewport-sm
--gf-ctrl-date-picker-margin-y-start
--gf-ctrl-date-picker-radius
--gf-ctrl-date-picker-width
--gf-ctrl-date-picker-width-viewport-sm
```

Published defaults include:

```text
background             = var(--gf-ctrl-bg-color)
padding-y              = 16px 12px
padding-y viewport-sm  = 16px
padding-x              = 12px
padding-x viewport-sm  = 16px
margin-y-start         = 12px
radius                 = var(--gf-ctrl-radius-max-md)
width                  = 250px
width viewport-sm      = 300px
```

### Header/icon

```text
--gf-ctrl-date-picker-header-icons-width
--gf-ctrl-date-picker-header-icons-color
--gf-ctrl-date-picker-header-icons-color-hover
--gf-ctrl-date-picker-header-icons-font-size
```

### Title

```text
--gf-ctrl-date-picker-title-color
--gf-ctrl-date-picker-title-font-size
--gf-ctrl-date-picker-title-font-size-viewport-sm
--gf-ctrl-date-picker-title-font-weight
--gf-ctrl-date-picker-title-gap
--gf-ctrl-date-picker-title-gap-viewport-sm
--gf-ctrl-date-picker-title-line-height
--gf-ctrl-date-picker-title-margin-x
--gf-ctrl-date-picker-title-margin-x-viewport-sm
```

### Dropdown

```text
--gf-ctrl-date-picker-dropdown-bg-img
--gf-ctrl-date-picker-dropdown-bg-position
--gf-ctrl-date-picker-dropdown-bg-size
--gf-ctrl-date-picker-dropdown-border-color
--gf-ctrl-date-picker-dropdown-border-style
--gf-ctrl-date-picker-dropdown-border-width
--gf-ctrl-date-picker-dropdown-shadow
--gf-ctrl-date-picker-dropdown-text-align
```

### Table / cells

```text
--gf-ctrl-date-picker-table-margin-y-start
--gf-ctrl-date-picker-table-margin-y-end
--gf-ctrl-date-picker-head-cell-font-size
--gf-ctrl-date-picker-head-cell-font-weight
--gf-ctrl-date-picker-head-cell-line-height
--gf-ctrl-date-picker-cell-padding
--gf-ctrl-date-picker-cell-padding-y
--gf-ctrl-date-picker-cell-padding-y-viewport-sm
--gf-ctrl-date-picker-cell-height
--gf-ctrl-date-picker-cell-height-viewport-sm
--gf-ctrl-date-picker-cell-font-size
--gf-ctrl-date-picker-cell-font-weight
--gf-ctrl-date-picker-cell-line-height
```

### Cell content

```text
--gf-ctrl-date-picker-cell-content-align-items
--gf-ctrl-date-picker-cell-content-bg-color-disabled
--gf-ctrl-date-picker-cell-content-bg-color-hover
--gf-ctrl-date-picker-cell-content-bg-color-selected
--gf-ctrl-date-picker-cell-content-border
--gf-ctrl-date-picker-cell-content-radius
--gf-ctrl-date-picker-cell-content-color
--gf-ctrl-date-picker-cell-content-color-disabled
--gf-ctrl-date-picker-cell-content-color-hover
--gf-ctrl-date-picker-cell-content-color-selected
--gf-ctrl-date-picker-cell-content-width
--gf-ctrl-date-picker-cell-content-width-viewport-sm
```

Key published defaults include:

```text
cell padding                   = 1px
cell padding-y                 = 6px
cell height                    = 29px
cell height viewport-sm        = 40px
cell font-size                 = 14px
cell font-weight               = 400
selected background            = var(--gf-color-in-ctrl-primary)
selected color                 = var(--gf-color-in-ctrl-primary-contrast)
cell content width             = 27px
cell content width viewport-sm = 100%
```

Two published defaults currently refer to internal-looking properties:

```text
--gf-ctrl-date-picker-cell-content-bg-color-hover
    → var(--gform-theme-color-uber-light-blue)

--gf-ctrl-date-picker-cell-content-color-disabled
    → var(--gform-theme-color-uber-light)
```

Treat those `--gform-theme-*` dependencies as `IMPLEMENTATION DETAIL`. Do not promote them into the public `--gf-*` contract.

Source: https://docs.css.gravity.com/framework.controls.date._api-global.html

## 6.5 Description

### Standard

```text
--gf-ctrl-desc-color
--gf-ctrl-desc-font-family
--gf-ctrl-desc-font-size
--gf-ctrl-desc-font-style
--gf-ctrl-desc-font-weight
--gf-ctrl-desc-letter-spacing
--gf-ctrl-desc-line-height
```

### Validation/error

```text
--gf-ctrl-desc-color-error
--gf-ctrl-desc-font-family-error
--gf-ctrl-desc-font-size-error
--gf-ctrl-desc-font-style-error
--gf-ctrl-desc-font-weight-error
--gf-ctrl-desc-letter-spacing-error
--gf-ctrl-desc-line-height-error
```

### Consent

```text
--gf-ctrl-desc-border-color-consent
--gf-ctrl-desc-border-color-consent-focus
--gf-ctrl-desc-border-style-consent
--gf-ctrl-desc-border-width-consent
--gf-ctrl-desc-max-height-consent
```

`--gf-ctrl-desc-max-height-consent` defaults to `456px`.

Source: https://docs.css.gravity.com/framework.controls.description._api-global.html

## 6.6 File Controls

### Native file input

```text
--gf-ctrl-file-padding-x
```

Default:

```text
0 var(--gf-ctrl-padding-x)
```

### Native file button

```text
--gf-ctrl-file-btn-bg-color
--gf-ctrl-file-btn-bg-color-hover
--gf-ctrl-file-btn-bg-color-focus
--gf-ctrl-file-btn-bg-color-disabled
--gf-ctrl-file-btn-border-inline-end-width
--gf-ctrl-file-btn-border-inline-end-style
--gf-ctrl-file-btn-border-inline-end-color
--gf-ctrl-file-btn-border-inline-end-color-hover
--gf-ctrl-file-btn-border-inline-end-color-focus
--gf-ctrl-file-btn-border-inline-end-color-disabled
--gf-ctrl-file-btn-radius
--gf-ctrl-file-btn-color
--gf-ctrl-file-btn-color-hover
--gf-ctrl-file-btn-color-focus
--gf-ctrl-file-btn-color-disabled
--gf-ctrl-file-btn-font-family
--gf-ctrl-file-btn-font-size
--gf-ctrl-file-btn-font-style
--gf-ctrl-file-btn-font-weight
--gf-ctrl-file-btn-letter-spacing
--gf-ctrl-file-btn-line-height
--gf-ctrl-file-btn-text-decoration
--gf-ctrl-file-btn-text-transform
--gf-ctrl-file-btn-margin-x
--gf-ctrl-file-btn-padding-x
--gf-ctrl-file-btn-transition
```

Key published defaults include:

```text
button bg        = var(--gf-color-secondary-darker)
button bg hover  = var(--gf-color-secondary)
button radius    = var(--gf-ctrl-radius)
font size        = 14px
font weight      = 500
margin-x         = 0 12px
padding-x        = 12px
```

### Enhanced upload zone

```text
--gf-ctrl-file-zone-border-style
--gf-ctrl-file-zone-radius
--gf-ctrl-file-zone-color
--gf-ctrl-file-zone-height
--gf-ctrl-file-zone-padding-x
--gf-ctrl-file-zone-padding-y
--gf-ctrl-file-zone-instructions-margin-y-end
--gf-ctrl-file-zone-font-weight
--gf-ctrl-file-zone-line-height
--gf-ctrl-file-zone-icon-color
--gf-ctrl-file-zone-icon-font-size
--gf-ctrl-file-zone-icon-margin-y-end
```

Key defaults include:

```text
border-style       = dashed
radius             = var(--gf-ctrl-radius-max-lg)
color              = rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.725)
height             = auto
padding-x          = 40px
padding-y          = 40px
instructions end   = 12px
font-weight        = 500
line-height        = 1
icon color         = var(--gf-color-in-ctrl-primary)
icon font-size     = 36px
icon margin end    = 8px
```

### Upload progress

```text
--gf-ctrl-file-prog-ui-gap
--gf-ctrl-file-prog-ui-size
--gf-ctrl-file-prog-bar-bg-color
--gf-ctrl-file-prog-bar-bg-color-loading
--gf-ctrl-file-prog-bar-height
--gf-ctrl-file-prog-bar-radius
--gf-ctrl-file-prog-bar-transition
--gf-ctrl-file-prog-text-color
--gf-ctrl-file-prog-text-min-width
--gf-ctrl-file-prog-text-font-size
--gf-ctrl-file-prog-btn-inset-y-start
--gf-ctrl-file-prog-btn-inset-x-end
--gf-ctrl-file-prog-btn-position
--gf-ctrl-file-prog-btn-font-size-cancel
--gf-ctrl-file-prog-btn-icon-size
--gf-ctrl-file-prog-btn-icon-color-complete
```

Notable defaults include:

```text
progress gap          = 12px
progress bar bg       = var(--gf-color-out-ctrl-light)
loading bar bg        = var(--gf-color-primary)
bar height            = 6px
complete icon color   = var(--gf-color-success)
```

### Upload preview

```text
--gf-ctrl-file-prev-area-gap
--gf-ctrl-file-prev-area-margin-y-start
--gf-ctrl-file-prev-font-family
--gf-ctrl-file-prev-font-size
--gf-ctrl-file-prev-font-style
--gf-ctrl-file-prev-font-weight
--gf-ctrl-file-prev-letter-spacing
--gf-ctrl-file-prev-line-height
--gf-ctrl-file-prev-gap
--gf-ctrl-file-prev-name-color
--gf-ctrl-file-prev-name-line-height
--gf-ctrl-file-prev-name-overflow
--gf-ctrl-file-prev-name-padding-x-end
--gf-ctrl-file-prev-name-text-overflow
--gf-ctrl-file-prev-name-white-space
--gf-ctrl-file-prev-size-color
```

Source: https://docs.css.gravity.com/framework.controls.file._api-global.html

## 6.7 Labels

### Primary

```text
--gf-ctrl-label-color-primary
--gf-ctrl-label-font-family-primary
--gf-ctrl-label-font-size-primary
--gf-ctrl-label-font-style-primary
--gf-ctrl-label-font-weight-primary
--gf-ctrl-label-letter-spacing-primary
--gf-ctrl-label-line-height-primary
```

### Secondary

```text
--gf-ctrl-label-color-secondary
--gf-ctrl-label-font-family-secondary
--gf-ctrl-label-font-size-secondary
--gf-ctrl-label-font-style-secondary
--gf-ctrl-label-font-weight-secondary
--gf-ctrl-label-letter-spacing-secondary
--gf-ctrl-label-line-height-secondary
```

### Tertiary

```text
--gf-ctrl-label-color-tertiary
--gf-ctrl-label-font-family-tertiary
--gf-ctrl-label-font-size-tertiary
--gf-ctrl-label-font-style-tertiary
--gf-ctrl-label-font-weight-tertiary
--gf-ctrl-label-letter-spacing-tertiary
--gf-ctrl-label-line-height-tertiary
```

### Quaternary

```text
--gf-ctrl-label-color-quaternary
--gf-ctrl-label-font-family-quaternary
--gf-ctrl-label-font-size-quaternary
--gf-ctrl-label-font-style-quaternary
--gf-ctrl-label-font-weight-quaternary
--gf-ctrl-label-letter-spacing-quaternary
--gf-ctrl-label-line-height-quaternary
```

### Required

```text
--gf-ctrl-label-color-req
--gf-ctrl-label-font-family-req
--gf-ctrl-label-font-size-req
--gf-ctrl-label-font-style-req
--gf-ctrl-label-font-weight-req
--gf-ctrl-label-letter-spacing-req
--gf-ctrl-label-line-height-req
```

The required indicator color defaults to `var(--gf-color-danger)`.

Source: https://docs.css.gravity.com/framework.controls.label._api-global.html

## 6.8 Number

| Property | Default |
|---|---|
| `--gf-ctrl-number-spin-btn-appearance` | `var(--gf-ctrl-appearance)` |
| `--gf-ctrl-number-spin-btn-bg-position` | `center center` |
| `--gf-ctrl-number-spin-btn-bg-size` | `8px 14px` |
| `--gf-ctrl-number-spin-btn-width` | `8px` |
| `--gf-ctrl-number-spin-btn-opacity` | `1` |

Source: https://docs.css.gravity.com/framework.controls.number._api-global.html

## 6.9 Readonly

```text
--gf-ctrl-readonly-color
--gf-ctrl-readonly-font-family
--gf-ctrl-readonly-font-size
--gf-ctrl-readonly-font-style
--gf-ctrl-readonly-font-weight
--gf-ctrl-readonly-letter-spacing
--gf-ctrl-readonly-line-height
```

Readonly typography derives from normal control typography; the documented font weight is `500` and line height is `1`.

Source: https://docs.css.gravity.com/framework.controls.readonly._api-global.html

## 6.10 Select

### Native select

```text
--gf-ctrl-select-icon
--gf-ctrl-select-icon-hover
--gf-ctrl-select-icon-focus
--gf-ctrl-select-icon-disabled
--gf-ctrl-select-icon-position
--gf-ctrl-select-icon-size
--gf-ctrl-select-ms-expand
--gf-ctrl-select-padding-x
```

Published defaults include:

```text
select icon       = var(--gf-icon-ctrl-select)
select icon size  = 10px
-ms-expand        = none
```

### Native multi-select

```text
--gf-ctrl-multiselect-height
--gf-ctrl-multiselect-radius
--gf-ctrl-multiselect-line-height
--gf-ctrl-multiselect-padding-y
```

Published defaults:

```text
height       = 130px
radius       = var(--gf-ctrl-radius-max-lg)
line-height  = 1.5
```

### Enhanced select

```text
--gf-ctrl-select-dropdown-border-color
--gf-ctrl-select-dropdown-radius
--gf-ctrl-select-dropdown-shadow
--gf-ctrl-select-dropdown-option-bg-color-hover
--gf-ctrl-select-dropdown-option-shadow-hover
--gf-ctrl-select-search-icon-size
--gf-ctrl-select-search-icon-position
--gf-ctrl-select-search-padding-x
```

`DOCUMENTATION AMBIGUOUS`

The current API publishes no default value for:

```text
--gf-ctrl-select-dropdown-option-shadow-hover
```

Do not invent one.

### Enhanced multi-select

```text
--gf-ctrl-multiselect-close-icon-size
--gf-ctrl-multiselect-close-icon-inset-y-start
--gf-ctrl-multiselect-close-icon-inset-x-end
--gf-ctrl-multiselect-selected-item-bg-color
--gf-ctrl-multiselect-selected-item-radius
--gf-ctrl-multiselect-selected-item-color
--gf-ctrl-multiselect-selected-item-font-size
--gf-ctrl-multiselect-selected-item-font-weight
--gf-ctrl-multiselect-selected-item-remove-icon-color
```

Current default:

```text
--gf-ctrl-multiselect-selected-item-font-weight
    = var(--gform-theme-font-weight-semibold)
```

Treat `--gform-theme-font-weight-semibold` as `IMPLEMENTATION DETAIL`, not public `--gf-*` API.

Source: https://docs.css.gravity.com/framework.controls.select._api-global.html

## 6.11 Textarea

| Property | Default |
|---|---|
| `--gf-ctrl-textarea-height` | `130px` |
| `--gf-ctrl-textarea-radius` | `var(--gf-ctrl-radius-max-lg)` |
| `--gf-ctrl-textarea-line-height` | `1.5` |
| `--gf-ctrl-textarea-padding-y` | `var(--gf-padding-y)` |
| `--gf-ctrl-textarea-resize` | `vertical` |

Source: https://docs.css.gravity.com/framework.controls.textarea._api-global.html

---

# 7. Fields API

## 7.1 Choice Fields

### Base

```text
--gf-field-choice-gap
--gf-field-choice-align-x-gap-y
--gf-field-choice-align-x-gap-x
--gf-field-choice-meta-margin-y-start
--gf-field-choice-meta-space
--gf-field-choice-other-ctrl-max-width
```

Published defaults:

```text
gap                  = var(--gf-label-space-x-secondary)
align-x gap-y        = var(--gf-field-choice-gap)
align-x gap-x        = 16px
meta margin-y-start  = 4px
meta space           = 16px
other ctrl max-width = 256px
```

### Image Choice base

```text
--gf-field-img-choice-aspect-ratio
--gf-field-img-choice-gap
--gf-field-img-choice-margin-y-end
--gf-field-img-choice-placeholder-icon-font-size
--gf-field-img-choice-radius-square
--gf-field-img-choice-radius-round
--gf-field-img-choice-shadow
--gf-field-img-choice-shadow-hover
--gf-field-img-choice-size-sm
--gf-field-img-choice-size-md
--gf-field-img-choice-size-lg
--gf-field-img-choice-size
```

Published defaults include:

```text
aspect-ratio          = 1/1
gap                   = var(--gf-field-gap-x)
margin-y-end          = 12px
placeholder font-size = 60px
square radius         = var(--gf-ctrl-radius-max-sm)
round radius          = 50%
size sm               = 125px
size md               = 200px
size lg               = 300px
size                  = var(--gf-field-img-choice-size-md)
```

### Image Choice card

```text
--gf-field-img-choice-card-placeholder-bg-color
--gf-field-img-choice-card-placeholder-color
--gf-field-img-choice-card-check-ind-bg-color
--gf-field-img-choice-card-check-ind-icon-color
--gf-field-img-choice-card-space-sm
--gf-field-img-choice-card-space-md
--gf-field-img-choice-card-space-lg
--gf-field-img-choice-card-space
```

Card spacing defaults:

```text
small   = 8px
medium  = 12px
large   = 16px
current = var(--gf-field-img-choice-card-space-md)
```

### Image Choice no-card

```text
--gf-field-img-choice-no-card-placeholder-bg-color
--gf-field-img-choice-no-card-placeholder-color
--gf-field-img-choice-no-card-check-ind-bg-color
--gf-field-img-choice-no-card-check-ind-icon-color
```

### Checked indicator

```text
--gf-field-img-choice-check-ind-icon
--gf-field-img-choice-check-ind-radius
--gf-field-img-choice-check-ind-shadow
--gf-field-img-choice-check-ind-size-sm
--gf-field-img-choice-check-ind-size-md
--gf-field-img-choice-check-ind-size-lg
--gf-field-img-choice-check-ind-size
--gf-field-img-choice-check-ind-icon-size-sm
--gf-field-img-choice-check-ind-icon-size-md
--gf-field-img-choice-check-ind-icon-size-lg
--gf-field-img-choice-check-ind-icon-size
```

Published defaults include:

```text
icon           = var(--gf-icon-ctrl-checkbox)
radius         = 50%
size sm        = 24px
size md        = 38px
size lg        = 64px
size           = var(--gf-field-img-choice-check-ind-size-md)
icon size sm   = 12px
icon size md   = var(--gf-icon-font-size)
icon size lg   = 30px
icon size      = var(--gf-field-img-choice-check-ind-icon-size-md)
```

Miscellaneous:

```text
--gf-field-img-choice-ctrl-opacity
--gf-field-img-choice-ctrl-opacity-disabled
--gf-field-img-choice-other-ctrl-margin-y-start
```

Published defaults:

```text
opacity          = 1
disabled opacity = 0.5
other ctrl margin-y-start = 16px
```

Source: https://docs.css.gravity.com/framework.fields.choice._api-global.html

## 7.2 Date Field

### Exact current identifiers

| Property | Default |
|---|---|
| `--gf-field-date-ctrl-padding-x-end` | `calc(var(--gf-ctrl-padding-x) + var(--gf-icon-font-size) + 4px)` |
| `--gf-field-date-icon-color` | `var(--gf-ctrl-icon-color)` |
| `--gf-field-date-icon-color-hover` | `var(--gf-ctrl-icon-color-hover)` |
| `--gf-field-date-icon-transition` | `var(--gf-ctrl-transition)` |
| `--gf-field-date-custom-icon-max-height` | `16px` |
| `--gf-field-date-custom-icon-max-width` | `16px` |
| `--gf-field-date-custom-icon-opacity` | `0.6` |
| `--gf-field-date-custom-icon-opacity-hover` | `1` |

### Explicitly rejected nonexistent aliases

The following are listed **only as negative examples** and are absent from the current official Date Field API:

```text
--gf-field-date-ctrl-icon-color
--gf-field-date-ctrl-icon-color-hover
--gf-field-date-ctrl-icon-transition
--gf-field-date-ctrl-icon-custom-max-height
--gf-field-date-ctrl-icon-custom-max-width
--gf-field-date-ctrl-icon-custom-opacity
--gf-field-date-ctrl-icon-custom-opacity-hover
```

Source: https://docs.css.gravity.com/framework.fields.date._api-global.html

## 7.3 List Field

| Property | Default |
|---|---|
| `--gf-field-list-btn-size` | `16px` |
| `--gf-field-list-btn-radius` | `50%` |
| `--gf-field-list-btn-font-size` | `0` |
| `--gf-field-list-btn-padding-y` | `0` |
| `--gf-field-list-btn-padding-x` | `0` |

Source: https://docs.css.gravity.com/framework.fields.list._api-global.html

## 7.4 Page / Multi-page UI

### Base/progress text

```text
--gf-field-pg-prog-color
--gf-field-pg-prog-margin-y-end
--gf-field-pg-prog-title-margin-y-end
--gf-field-pg-prog-font-family
--gf-field-pg-prog-font-size
--gf-field-pg-prog-font-style
--gf-field-pg-prog-font-weight
--gf-field-pg-prog-letter-spacing
--gf-field-pg-prog-line-height
--gf-field-pg-prog-text-transform
```

Published defaults include:

```text
color             = var(--gf-color-out-ctrl-dark)
margin-y-end      = 24px
title margin      = 16px
font-size         = 14px
font-weight       = 600
line-height       = 1
text-transform    = uppercase
```

### Progress bar

```text
--gf-field-pg-prog-bar-bg-color
--gf-field-pg-prog-bar-bg-color-blue
--gf-field-pg-prog-bar-bg-color-gray
--gf-field-pg-prog-bar-bg-color-green
--gf-field-pg-prog-bar-bg-color-orange
--gf-field-pg-prog-bar-bg-color-red
--gf-field-pg-prog-bar-bg-gradient-spring
--gf-field-pg-prog-bar-bg-gradient-blues
--gf-field-pg-prog-bar-bg-gradient-rainbow
--gf-field-pg-prog-bar-radius
--gf-field-pg-prog-bar-height
```

Published values include:

```text
blue    = #204ce5
green   = #31c48d
orange  = #ff5a1f
red     = #c02b0a
radius  = 100px
height  = 10px
```

### Steps

```text
--gf-field-pg-steps-number-bg-color
--gf-field-pg-steps-number-bg-color-active
--gf-field-pg-steps-number-bg-color-complete
--gf-field-pg-steps-number-border-color
--gf-field-pg-steps-number-border-color-active
--gf-field-pg-steps-number-border-color-complete
--gf-field-pg-steps-number-border-style
--gf-field-pg-steps-number-border-width
--gf-field-pg-steps-number-radius
--gf-field-pg-steps-number-color
--gf-field-pg-steps-number-color-active
--gf-field-pg-steps-number-color-complete
--gf-field-pg-steps-icon-font-size
--gf-field-pg-steps-number-size
--gf-field-pg-steps-step-gap
```

Published defaults include:

```text
number size          = 32px
number radius        = 50%
border width         = 2px
completed background = var(--gf-color-primary)
completed color      = var(--gf-color-primary-contrast)
step gap             = 12px
```

Source: https://docs.css.gravity.com/framework.fields.page._api-global.html

## 7.5 Password

### Base

```text
--gf-field-pwd-ctrl-padding-x-end
```

Published default:

```text
calc(var(--gf-ctrl-padding-x) + var(--gf-icon-font-size) + 8px)
```

### Strength label

```text
--gf-field-pwd-str-bg-color
--gf-field-pwd-str-bg-color-mismatch
--gf-field-pwd-str-bg-color-short
--gf-field-pwd-str-bg-color-bad
--gf-field-pwd-str-bg-color-good
--gf-field-pwd-str-bg-color-strong
--gf-field-pwd-str-border-color
--gf-field-pwd-str-border-color-mismatch
--gf-field-pwd-str-border-color-short
--gf-field-pwd-str-border-color-bad
--gf-field-pwd-str-border-color-good
--gf-field-pwd-str-border-color-strong
--gf-field-pwd-str-border-style
--gf-field-pwd-str-border-width
--gf-field-pwd-str-radius
--gf-field-pwd-str-color
--gf-field-pwd-str-color-mismatch
--gf-field-pwd-str-color-short
--gf-field-pwd-str-color-bad
--gf-field-pwd-str-color-good
--gf-field-pwd-str-color-strong
--gf-field-pwd-str-margin-y-start
--gf-field-pwd-str-padding-y
--gf-field-pwd-str-padding-x
--gf-field-pwd-str-font-family
--gf-field-pwd-str-font-size
--gf-field-pwd-str-font-style
--gf-field-pwd-str-font-weight
--gf-field-pwd-str-letter-spacing
--gf-field-pwd-str-line-height
--gf-field-pwd-str-text-align
--gf-field-pwd-str-transition
```

Documented state colors include:

```text
mismatch = #c02b0a
short    = #c02b0a
bad      = #ff5a1f
good     = #8b6c32
strong   = #399f4b
```

### Strength indicator

```text
--gf-field-pwd-str-ind-bg-color
--gf-field-pwd-str-ind-bg-color-mismatch
--gf-field-pwd-str-ind-bg-color-short
--gf-field-pwd-str-ind-bg-color-bad
--gf-field-pwd-str-ind-bg-color-good
--gf-field-pwd-str-ind-bg-color-strong
--gf-field-pwd-str-ind-display
--gf-field-pwd-str-ind-inset-y-start
--gf-field-pwd-str-ind-inset-x-start
--gf-field-pwd-str-ind-position
--gf-field-pwd-str-ind-height
--gf-field-pwd-str-ind-width
--gf-field-pwd-str-ind-width-blank
--gf-field-pwd-str-ind-width-mismatch
--gf-field-pwd-str-ind-width-short
--gf-field-pwd-str-ind-width-bad
--gf-field-pwd-str-ind-width-good
--gf-field-pwd-str-ind-width-strong
--gf-field-pwd-str-ind-content
--gf-field-pwd-str-ind-transform
--gf-field-pwd-str-ind-transition
```

Published widths:

```text
blank     = 0
mismatch  = 65px
short     = 22px
bad       = 37px
good      = 46px
strong    = 65px
```

The current official page renders trailing semicolons inside several `var(...)` default-value cells. Treat that punctuation as documentation presentation, not a different identifier.

Source: https://docs.css.gravity.com/framework.fields.password._api-global.html

## 7.6 Product

| Property | Default |
|---|---|
| `--gf-field-prod-price-color` | `var(--gf-ctrl-label-color-primary)` |
| `--gf-field-prod-quant-margin-y-end` | `var(--gf-field-gap-y)` |
| `--gf-field-prod-quant-width` | `150px` |

Source: https://docs.css.gravity.com/framework.fields.product._api-global.html

## 7.7 Repeater

| Property | Default |
|---|---|
| `--gf-field-repeater-gap-y` | `var(--gf-form-gap-y)` |
| `--gf-field-repeater-btn-inline-gap` | `var(--gf-form-gap-x)` |
| `--gf-field-repeater-separator-color` | `var(--gf-color-out-ctrl-light-darker)` |
| `--gf-field-repeater-separator-size` | `1px` |
| `--gf-field-repeater-nested-border-color` | `var(--gf-color-out-ctrl-light-darker)` |
| `--gf-field-repeater-nested-border-size` | `1px` |
| `--gf-field-repeater-nested-border-style` | `solid` |
| `--gf-field-repeater-nested-padding-x-start` | `20px` |

Source: https://docs.css.gravity.com/framework.fields.repeater._api-global.html

## 7.8 Section

| Property | Default |
|---|---|
| `--gf-field-section-border-color` | `var(--gf-color-out-ctrl-light-darker)` |
| `--gf-field-section-border-style` | `solid` |
| `--gf-field-section-border-width` | `1px` |
| `--gf-field-section-padding-y-end` | `8px` |

Source: https://docs.css.gravity.com/framework.fields.section._api-global.html

---

# 8. Form-Level API

## 8.1 Spinner

| Property | Default |
|---|---|
| `--gf-form-spinner-fg-color` | `var(--gf-color-primary)` |
| `--gf-form-spinner-bg-color` | `rgba(var(--gf-color-primary-rgb), 0.1)` |

Source: https://docs.css.gravity.com/framework.form.spinner._api-global.html

## 8.2 Validation

### Base

| Property | Default |
|---|---|
| `--gf-form-validation-bg-color` | `rgba(var(--gf-color-danger-rgb), 0.03)` |
| `--gf-form-validation-border-color` | `rgba(var(--gf-color-danger-rgb), 0.25)` |
| `--gf-form-validation-border-color-focus` | `var(--gf-color-danger)` |
| `--gf-form-validation-border-width` | `1px` |
| `--gf-form-validation-border-style` | `solid` |
| `--gf-form-validation-radius` | `var(--gf-ctrl-radius-max-md)` |
| `--gf-form-validation-outline-color-focus` | `rgba(var(--gf-color-danger-rgb), 0.65)` |
| `--gf-form-validation-outline-focus` | `var(--gf-ctrl-outline-width-focus) var(--gf-ctrl-outline-style) var(--gf-form-validation-outline-color-focus)` |
| `--gf-form-validation-shadow` | `0 1px 4px rgba(18, 25, 97, 0.0779552)` |
| `--gf-form-validation-color` | `var(--gf-color-danger)` |
| `--gf-form-validation-font-family` | `var(--gf-font-family-primary)` |
| `--gf-form-validation-font-size` | `var(--gf-font-size-primary)` |
| `--gf-form-validation-line-height` | `1.43` |
| `--gf-form-validation-gap` | `8px` |
| `--gf-form-validation-margin-y` | `0 var(--gf-form-gap-y)` |
| `--gf-form-validation-padding-y` | `20px` |
| `--gf-form-validation-padding-x` | `16px` |

### Heading

```text
--gf-form-validation-heading-color
--gf-form-validation-heading-font-family
--gf-form-validation-heading-font-size
--gf-form-validation-heading-font-weight
--gf-form-validation-heading-line-height
--gf-form-validation-heading-gap
```

### Heading icon

```text
--gf-form-validation-heading-icon-bg-color
--gf-form-validation-heading-icon-border-color
--gf-form-validation-heading-icon-border-width
--gf-form-validation-heading-icon-border-style
--gf-form-validation-heading-icon-radius
--gf-form-validation-heading-icon-color
--gf-form-validation-heading-icon-font-size
--gf-form-validation-heading-icon-size
```

### Summary

```text
--gf-form-validation-summary-color
--gf-form-validation-summary-font-family
--gf-form-validation-summary-font-size
--gf-form-validation-summary-font-weight
--gf-form-validation-summary-line-height
--gf-form-validation-summary-margin-y-start
--gf-form-validation-summary-padding-x
--gf-form-validation-summary-item-link-text-decoration
```

Published summary defaults include:

```text
font-weight          = 400
margin-y-start       = 4px
padding-x            = 48px
link text-decoration = underline
```

Source: https://docs.css.gravity.com/framework.form.validation._api-global.html

## 8.3 Submit Buttons

Current Orbital selector documentation for Gravity Forms 3.0+ includes:

```text
button[type="submit"]
button.gform_image_button
.gform_footer
.gform_page_footer
#field_submit_{form_id}
.gfield--type-submit
.gform_button
.button
.gform-button
.gform-button--width-full
.gform-theme-button
#gform_submit_button_{form_id}
```

Primary submit-button presentation should normally use the documented primary button CSS API where it exposes the required behavior.

Source: https://docs.gravityforms.com/submit-button-css-selectors/

## 8.4 Gravity Forms 3.0 Submit Markup

Starting in Gravity Forms 3.0, form buttons use `<button>` rather than `<input>`.

During submission the button can receive:

```text
.gform-has-spinner
```

and the spinner/loader is rendered inside the button as:

```text
.gform-loader
```

Legacy spinner URL hooks documented as removed in 3.0:

```text
gform_ajax_spinner_url
gform_spinner_url
gform_always_show_spinner
```

Sources:

- https://docs.gravityforms.com/submit-button-css-selectors/
- https://docs.gravityforms.com/checks-before-upgrading-to-gravity-forms-3-0/
- https://docs.gravityforms.com/gravityforms-change-log/

## 8.5 Save and Continue

Documented classes:

```text
.gform_save_link
.gform-theme-button
.gform-theme-button--secondary
```

Documented containers:

```text
.gform_footer
.gform_page_footer
```

Documented IDs:

```text
gform_save_{form_id}_{page_number}_link
gform_save_{form_id}_footer_link
```

The Theme Framework secondary-button API is the relevant presentation surface.

Source: https://docs.gravityforms.com/save-and-continue-link-css/

## 8.6 Confirmation UI

Current confirmation selector documentation includes form/theme wrapper and confirmation message/wrapper selectors, including:

```text
#gform_confirmation_wrapper_{form_id}
.gform_confirmation_wrapper
#gform_confirmation_message_{form_id}
.gform_confirmation_message
.gform_confirmation_message_{form_id}
.gform-theme--framework.gform_confirmation_wrapper
.form_saved_message
.form_saved_message_sent
```

No dedicated confirmation-specific `--gf-*` API family was found in the current CSS API taxonomy.

Classification:

```text
Confirmation selectors:
DOCUMENTED PUBLIC CONTRACT

Dedicated confirmation CSS custom-property family:
NOT DOCUMENTED IN OFFICIAL REFERENCE
```

Source: https://docs.gravityforms.com/form-confirmation/

---

# 9. Layout and Design

## 9.1 CSS logical properties

Gravity Forms uses logical CSS properties to support languages of different writing directions. Custom themes should avoid unnecessary left/right assumptions when logical equivalents are available.

## 9.2 Complex field grid

Documented Foundation classes:

```text
.gform-grid-row
.gform-grid-col
.gform-grid-col--size-auto
```

Typical complex-field wrappers also use:

```text
.ginput_complex
.ginput_container
```

The dedicated current Field Grid page states that `.gform-grid-col--size-auto` sizes the column to the width of its content.

Source: https://docs.css.gravity.com/foundation.layout._grid.html

## 9.3 Label placement

Documented wrapper layout classes:

```text
.top_label
.left_label
.right_label
```

Relevant API:

```text
--gf-label-width
```

## 9.4 Custom form/field classes

Gravity Forms documents configurable custom CSS classes. Treat project-defined custom classes as project API, not as undocumented Gravity Forms API.

## 9.5 Ready Classes

Legacy Gravity Forms Ready Classes are documented as deprecated in the context of modern form editor layout improvements.

For modern Theme Framework/Orbital work, prefer:

- form editor layout;
- Foundation layout;
- CSS API layout variables;
- documented field wrappers/classes.

Source: https://docs.gravityforms.com/design-overview/

---

# 10. Utility Classes

## 10.1 Foundation utilities

### `.gform-ul-reset`

Documented behavior:

```css
list-style-type: none;
margin: 0;
padding: 0;
```

### `.gform-text-input-reset`

Documented reset covers:

```text
background-color
border
border-radius
box-shadow
color
font-family
font-size
outline
padding
width
```

Source: https://docs.css.gravity.com/foundation.base._utils.html

## 10.2 Semantic classes

Official Theme Framework documentation recommends semantic classes including:

```text
.gform-field-label
.gform-field-description
.gform-theme-field-control
```

for custom/add-on markup that should participate in framework presentation.

## 10.3 Malformed modifier documentation

`DOCUMENTATION AMBIGUOUS`

Core Concepts currently renders several field-control modifier names with ambiguous dash typography. Do not silently normalize rendered dash characters into presumed selectors unless another current official source confirms the exact literal selector.

---

# 11. Theme Authoring Workflow

Use this workflow:

```text
1. Identify target runtime/theme.
        ↓
2. Confirm Theme Framework/Foundation participation.
        ↓
3. Identify intent:
   global / form / field-type / field / component / state.
        ↓
4. Search this local reference.
        ↓
5. Find documented --gf-* capability.
        ↓
6. Check whether a higher-level token expresses the intent.
        ↓
7. If not, choose the narrowest documented component token.
        ↓
8. Apply it at the narrowest correct scope.
        ↓
9. Use direct element CSS only when no documented API
   exposes the required property.
        ↓
10. Never invent a --gf-* identifier.
        ↓
11. If absent:
    UNKNOWN_FROM_LOCAL_REFERENCE.
        ↓
12. Check current official documentation.
        ↓
13. Update this snapshot if the contract changed.
```

## 11.1 `gform_default_styles` — Important Input Contract

`gform_default_styles` filters global form theme styles.

Its dedicated current hook documentation defines `$styles` as an array or JSON-encoded string of **style-setting keys**, not arbitrary raw `--gf-*` CSS custom-property names.

Current documented accepted keys:

```text
theme
inputSize
inputBorderRadius
inputBorderColor
inputBackgroundColor
inputColor
inputPrimaryColor
labelFontSize
labelColor
descriptionFontSize
descriptionColor
buttonPrimaryBackgroundColor
buttonPrimaryColor
```

Image Choice-specific accepted keys:

```text
inputImageChoiceAppearance
inputImageChoiceStyle
inputImageChoiceSize
```

Therefore, this is not the documented hook contract:

```php
$styles['--gf-ctrl-radius'] = '8px';
```

The hook contract instead uses style-setting keys, for example:

```php
$styles['inputBorderRadius'] = '8';
```

Conceptually:

```text
gform_default_styles
        ↓
Gravity Forms style-setting keys
        ↓
Gravity Forms maps settings
        ↓
Theme Framework presentation
```

Direct CSS API overrides are a different mechanism:

```text
CSS selector
    +
documented --gf-* property
```

The dedicated hook documentation states that `gform_default_styles` was added in Gravity Forms 2.7.15.

Source: https://docs.gravityforms.com/gform_default_styles/

## 11.2 Current custom-theme registration limitation

Current official Theme Framework FAQ states:

```text
You cannot currently register a form theme.
```

Documented alternatives are:

```text
gform_default_styles
gform_enqueue_scripts
```

Theme Layers and CSS API capabilities do not, by themselves, establish a first-class public custom form-theme registration API.

For a project described informally as a “custom Gravity Forms theme”, the safe documented model is:

```text
Foundation
    +
Theme Framework APIs
    +
project-owned CSS/style integration
```

Source: https://docs.gravityforms.com/theme-framework-faq/

---

# 12. Recommended Framework Usage Patterns

## 12.1 Semantic token first

Prefer a high-level token when it genuinely represents the intended semantic change:

```text
--gf-color-primary
        ↓
documented dependent properties
```

Do not override many downstream properties when a documented semantic token expresses the same intent.

## 12.2 Component token second

If the change is control-specific:

```text
--gf-ctrl-bg-color
--gf-ctrl-border-color
--gf-ctrl-radius
```

may be more appropriate than changing the global semantic color/radius system.

## 12.3 Narrow scope third

For one form:

```css
.gform-theme--framework#gform_wrapper_{form_id}
```

For one field:

```css
.gform-theme--framework #field_{form_id}_{field_id}
```

Avoid global overrides when the requirement is local.

## 12.4 State-specific APIs

For focus/error/disabled behavior, use documented state APIs where available:

```text
--gf-ctrl-border-color-focus
--gf-ctrl-outline-color-focus
--gf-ctrl-outline-width-focus
--gf-ctrl-border-color-error
--gf-ctrl-bg-color-disabled
--gf-ctrl-color-disabled
```

Do not reintroduce `--gf-ctrl-shadow-color-focus` as current API from the Colors page’s `Used by` column; the dedicated current Controls — Base API does not define it.

## 12.5 Preserve Foundation

Do not remove Foundation merely to obtain a custom visual design. Foundation contains functional/layout behavior required underneath custom Theme Framework-based presentation.

## 12.6 Treat Orbital internals as separate

A property beginning with:

```text
--gform-theme-
```

is not automatically a documented public:

```text
--gf-
```

API identifier.

Do not make project architecture depend on an internal Orbital token merely because a public property's published default references it.

---

# 13. Known Anti-Patterns

| Anti-pattern | Problem |
|---|---|
| Inventing `--gf-*` names from naming patterns | Creates a false framework contract |
| Copying Orbital generated CSS as API | Couples to implementation detail |
| Using `--gform-theme-*` as if it were public `--gf-*` API | Breaks authority boundary |
| Using historical 2.7 identifiers in current code | 2.8 renamed large parts of the API |
| Passing raw `--gf-*` names to `gform_default_styles` | Violates its documented style-setting input contract |
| Removing Foundation for a visual rewrite | Risks breaking functional/layout behavior |
| Globally overriding a one-form requirement | Creates cross-form coupling |
| Ignoring hover/focus/error/disabled APIs | Produces incomplete state behavior |
| Guessing around documentation inconsistencies | Converts ambiguity into false fact |
| Assuming an observed selector is stable public API | May couple to Orbital internals |
| Correcting suspicious official defaults by intuition | Destroys source fidelity |
| Treating add-on-specific variables as core GF API | Expands the core contract incorrectly |

The FAQ documents that add-ons can define their own add-on-specific custom properties. Such properties are extension API owned by the add-on, not Gravity Forms core Theme Framework API.

---

# 14. Orbital vs Theme Framework

| Concept | Role |
|---|---|
| Theme Framework | Public CSS architecture/API |
| Foundation | Required functional/layout base |
| Theme Layers | Integration/settings orchestration |
| Orbital | Default Theme Framework implementation/user-facing form theme |

Preferred dependency direction:

```text
Custom presentation layer
        ↓
documented Theme Framework API
        ↓
Foundation/runtime contract
```

Avoid:

```text
Custom presentation layer
        ↓
copied Orbital implementation details
```

Only themes using the Theme Framework can participate in the Theme Framework block-style customization mechanism documented by Gravity Forms.

---

# 15. Compatibility and Upgrade Notes

## 15.1 Gravity Forms 2.7

The Theme Framework was introduced in Gravity Forms 2.7.

Source: https://docs.gravityforms.com/theme-framework-introduction/

## 15.2 Gravity Forms 2.7.15

Current official Form Themes documentation states that beginning with Gravity Forms 2.7.15:

- new installations apply Orbital globally by default;
- existing installations are not automatically converted;
- sites installed before 2.7.15 can retain the Gravity Forms 2.5 theme until manually changed.

Source: https://docs.gravityforms.com/form-themes-and-style-settings/

## 15.3 Gravity Forms 2.8

Gravity Forms 2.8 refactored Theme Framework CSS and introduced breaking CSS API renaming.

Documented rename vocabulary includes:

| Old segment | 2.8+ segment |
|---|---|
| `gform-theme` | `gf` |
| `background` | `bg` |
| `button` | `btn` |
| `control` | `ctrl` |
| `password` | `pwd` |
| `page` | `pg` |
| `file-upload` | `file` |
| `spacing` | `space` |
| `gf-font-family` | `gf-font-family-base` |
| `progress` | `prog` |
| `description` | `desc` |
| `outside` | `out` |
| `inside` | `in` |
| `box-shadow` | `shadow` |
| `preview` | `prev` |
| `ctrl-file-prev-file` | `ctrl-file-prev` |
| `drop-area` | `zone` |
| `border-radius` | `radius` |
| `strength` | `str` |
| `indicator` | `ind` |
| `product` | `prod` |
| `quantity` | `quant` |
| `required` | `req` |
| `col-gap` | `gap-x` |
| `row-gap` | `gap-y` |
| `vertical` | `y` |
| `horizontal` | `x` |
| `inline-size` | `width` |
| `block-size` | `height` |
| `padding-inline` | `padding-x` |
| `padding-block` | `padding-y` |
| `margin-inline` | `margin-x` |
| `margin-block` | `margin-y` |
| `inset-block-start` | `inset-y-start` |
| `inset-block-end` | `inset-y-end` |
| `inset-inline-start` | `inset-x-start` |
| `inset-inline-end` | `inset-x-end` |
| `table-cell` | `cell` |
| `table-head-cell` | `head-cell` |

Associated design-token/mixin NPM packages moved to version 4.0.

Do not mechanically derive a current property from this migration table. The dedicated current CSS API page remains the authority for exact current identifiers/defaults.

Source: https://docs.gravityforms.com/theme-framework-upgrade-guide/

## 15.4 Gravity Forms 2.9

Gravity Forms 2.9:

- removed deprecated Theme Framework global CSS API properties;
- changed `.gform-theme__disable` and `.gform-theme__disable-framework` behavior so framework styling is also disabled for applicable field labels/descriptions.

Themes carrying deprecated 2.7-era assumptions must be retested.

Source: https://docs.gravityforms.com/gravity-forms-2-9-key-features/

## 15.5 Gravity Forms 3.0

Gravity Forms 3.0.0 was released on **2026-07-28**.

Relevant presentation/runtime changes include:

### Submit controls

```text
<input>
    ↓
<button>
```

### Spinner

The spinner is rendered inside the button. Current selector documentation identifies `.gform-has-spinner` and `.gform-loader`.

### Datepicker

Gravity Forms 3.0 changed the datepicker implementation from jQuery UI to the WhatSock library for improved accessibility.

Therefore:

- do not depend on old jQuery UI datepicker implementation selectors;
- prefer the Theme Framework Date/Date Picker public CSS API;
- retest custom submit-button selectors;
- retest custom datepicker presentation.

Sources:

- https://docs.gravityforms.com/checks-before-upgrading-to-gravity-forms-3-0/
- https://docs.gravityforms.com/submit-button-css-selectors/
- https://docs.gravityforms.com/gravityforms-change-log/

---

# 16. Unknown / Ambiguous / Non-Public Areas

## 16.1 No public custom-theme registration API

Current official FAQ states custom form themes cannot currently be registered through a public first-class form-theme registration API.

Classification:

```text
NOT DOCUMENTED AS AVAILABLE
```

Source: https://docs.gravityforms.com/theme-framework-faq/

## 16.2 Orbital internals

Undocumented generated implementation selectors, internal custom properties, internal DOM details, and private component decisions must not be promoted into framework API.

Classification:

```text
IMPLEMENTATION DETAIL
```

unless separately established by current official public documentation.

## 16.3 Color-system overview incompleteness

`DOCUMENTATION AMBIGUOUS`

The current Colors API contains unfinished explanatory text in the color-system overview while its property tables are concrete. Use the published property tables and explicit dependencies; do not invent an undocumented color-generation algorithm.

Source: https://docs.css.gravity.com/framework.api._colors.html

## 16.4 Design Overview contains stale/conflicting property names

`DOCUMENTATION AMBIGUOUS`

The current Design Overview shows examples including:

```text
--gf-ctrl-border-size
--gf-ctrl-padding-block
--gf-ctrl-padding-inline
```

while the dedicated current Controls — Base API documents:

```text
--gf-ctrl-border-width
--gf-ctrl-padding-y
--gf-ctrl-padding-x
```

For exact current CSS API identifier/default evidence:

```text
dedicated current CSS API page
    >
high-level Design Overview example
```

This is domain-scoped authority, not one global precedence list.

Sources:

- https://docs.gravityforms.com/design-overview/
- https://docs.css.gravity.com/framework.controls.default._api-global.html

## 16.5 Historical CSS API examples

`DOCUMENTATION AMBIGUOUS / HISTORICAL CONTEXT`

The architectural CSS API article contains older-form examples such as:

```text
--gf-control-bg-color-focus
```

Current 2.8+ dedicated API uses the shortened `ctrl` naming. Treat the architecture article as architectural evidence, not as current identifier inventory.

Source: https://docs.gravityforms.com/css-api/

## 16.6 Historical invalid/error naming

`DOCUMENTATION AMBIGUOUS / HISTORICAL CONTEXT`

Upgrade/history material can contain examples such as:

```text
--gf-ctrl-color-invalid
```

while the current dedicated Controls — Base API documents:

```text
--gf-ctrl-color-error
```

For new code, use the current dedicated CSS API identifier.

## 16.7 Internal `--gform-theme-*` dependencies

Current public properties sometimes publish defaults that reference internal-looking values such as:

```text
--gform-theme-color-uber-light-blue
--gform-theme-color-uber-light
--gform-theme-font-weight-semibold
```

These dependencies are visible in official documentation but are not entries in the public `--gf-*` API taxonomy.

Classification:

```text
IMPLEMENTATION DETAIL
```

Do not use them as project-level Theme Framework public API without independent current public documentation.

## 16.8 Enhanced select hover shadow default

The current API defines:

```text
--gf-ctrl-select-dropdown-option-shadow-hover
```

but its official table currently leaves the Default cell empty.

Classification:

```text
DOCUMENTATION AMBIGUOUS
```

Do not invent the default.

## 16.9 Simple-button focus icon dependency

Current official table publishes:

```text
--gf-ctrl-btn-icon-color-focus-simple
    = var(--gf-ctrl-btn-icon-color-focus-simple)
```

Classification:

```text
DOCUMENTATION AMBIGUOUS
```

Do not substitute a guessed dependency.

## 16.10 Utility modifier typography

Some Core Concepts modifier names are rendered with ambiguous/malformed dash characters.

Do not normalize them into presumed selectors without a second current official source.

## 16.11 Gravity Forms 2.5 wrapper conflict

`DOCUMENTATION AMBIGUOUS`

Current official sources do **not** agree on the Gravity Forms 2.5 theme wrapper:

| Current official page | Published form |
|---|---|
| Quick Start Guide | `.gravity-theme` |
| Core Concepts | `.gravity-theme` |
| CSS Element Naming Structure | `.gravity-theme` |
| Theme Framework FAQ, “Writing different styles for different form themes” | `.gform_theme` |

The preferred wrapper table in §3.1 uses `.gravity-theme` because the current wrapper-specific/current structure documentation and Core Concepts agree on that spelling.

However:

```text
.gravity-theme
        ≠ automatically interchangeable with
.gform_theme
```

Do not silently treat them as aliases. If targeting the Gravity Forms 2.5 theme specifically, verify the actual runtime markup and the current official source relevant to that runtime before depending on either spelling.

Sources:

- https://docs.gravityforms.com/quick-start-guide/
- https://docs.gravityforms.com/theme-framework/
- https://docs.gravityforms.com/basic-structure/
- https://docs.gravityforms.com/theme-framework-faq/

## 16.12 Focus-shadow reference conflict

`DOCUMENTATION AMBIGUOUS`

The current Colors API lists:

```text
--gf-ctrl-shadow-color-focus
```

in the `Used by` column for `--gf-color-primary-rgb`.

The current dedicated Controls — Base API does **not** define that property.

For current new code, do not treat it as verified current API. Use the dedicated current Controls — Base focus properties instead:

```text
--gf-ctrl-border-color-focus
--gf-ctrl-outline-color-focus
--gf-ctrl-outline-width-focus
```

Sources:

- https://docs.css.gravity.com/framework.api._colors.html
- https://docs.css.gravity.com/framework.controls.default._api-global.html

---

# 17. Quick Lookup Index

| Need to change | Check first |
|---|---|
| Primary accent | `--gf-color-primary` |
| Primary contrast | `--gf-color-primary-contrast` |
| Base radius | `--gf-radius` |
| Generic control radius | `--gf-ctrl-radius` |
| Control background | `--gf-ctrl-bg-color` |
| Control text | `--gf-ctrl-color` |
| Control border | `--gf-ctrl-border-color` |
| Focus border | `--gf-ctrl-border-color-focus` |
| Focus outline | `--gf-ctrl-outline-color-focus`, `--gf-ctrl-outline-width-focus` |
| Error border | `--gf-ctrl-border-color-error` |
| Disabled control background | `--gf-ctrl-bg-color-disabled` |
| Control height | `--gf-ctrl-size` |
| Control padding | `--gf-ctrl-padding-x`, `--gf-ctrl-padding-y` |
| Placeholder | `--gf-ctrl-placeholder-*` |
| Primary button | `--gf-ctrl-btn-*-primary` family |
| Secondary button | `--gf-ctrl-btn-*-secondary` family |
| Button size | `--gf-ctrl-btn-size` |
| Button radius | `--gf-ctrl-btn-radius` |
| Main label | `--gf-ctrl-label-*-primary` |
| Choice label | `--gf-ctrl-label-*-secondary` |
| Required indicator | `--gf-ctrl-label-*-req` |
| Description | `--gf-ctrl-desc-*` |
| Error description | `--gf-ctrl-desc-*-error` |
| Choice check color | `--gf-ctrl-choice-check-color` |
| Choice control size | `--gf-ctrl-choice-size` |
| Checkbox checked radius | `--gf-ctrl-checkbox-check-radius` |
| Checkbox check size | `--gf-ctrl-checkbox-check-size` |
| Radio checked radius | `--gf-ctrl-radio-check-radius` |
| Radio check size | `--gf-ctrl-radio-check-size` |
| Select icon | `--gf-ctrl-select-icon*` |
| Enhanced select dropdown | `--gf-ctrl-select-dropdown-*` |
| Multi-select selected item | `--gf-ctrl-multiselect-selected-item-*` |
| Textarea | `--gf-ctrl-textarea-*` |
| File upload zone | `--gf-ctrl-file-zone-*` |
| File upload progress | `--gf-ctrl-file-prog-*` |
| File preview | `--gf-ctrl-file-prev-*` |
| Date picker | `--gf-ctrl-date-picker-*` |
| Date field end padding | `--gf-field-date-ctrl-padding-x-end` |
| Date field icon | `--gf-field-date-icon-*` |
| Custom date icon | `--gf-field-date-custom-icon-*` |
| Image choice | `--gf-field-img-choice-*` |
| Password strength | `--gf-field-pwd-str-*` |
| Page progress | `--gf-field-pg-prog-*` |
| Page steps | `--gf-field-pg-steps-*` |
| Product quantity width | `--gf-field-prod-quant-width` |
| Form horizontal gap | `--gf-form-gap-x` |
| Form vertical gap | `--gf-form-gap-y` |
| Field gap | `--gf-field-gap-x`, `--gf-field-gap-y` |
| Label width | `--gf-label-width` |
| Validation summary | `--gf-form-validation-*` |
| Spinner | `--gf-form-spinner-fg-color`, `--gf-form-spinner-bg-color` |
| Complex grid row | `.gform-grid-row` |
| Complex grid column | `.gform-grid-col` |
| Framework scope | `.gform-theme--framework` |
| Orbital scope | `.gform-theme--orbital` |
| One form | `#gform_wrapper_{form_id}` |
| One field | `#field_{form_id}_{field_id}` |

`*` in this Quick Lookup table is **navigation shorthand for an already enumerated documented family**, not a literal CSS property and not permission to infer an undocumented suffix.

---

# 18. Canonical Integrity Gates

This section is normative for maintenance of this local reference.

## 18.1 GATE A — ZERO-INVENTION IDENTIFIER GATE

Construct:

```text
REFERENCE_IDENTIFIER_SET
```

from every literal `--gf-*` identifier represented as current usable Gravity Forms API.

Construct:

```text
OFFICIAL_IDENTIFIER_SET
```

from current official Gravity Forms CSS API pages plus explicit current official Gravity Forms API documentation where applicable.

For every candidate:

```text
candidate ∈ OFFICIAL_IDENTIFIER_SET
```

must be proven by exact spelling.

Exclude only literals explicitly and unambiguously presented as:

- historical;
- obsolete;
- incorrect/nonexistent;
- documentation-conflict evidence;
- negative examples;
- wildcard/family navigation notation.

Failure means the document is not canonical until repaired.

## 18.2 GATE B — API-FIDELITY GATE

Identifier existence is insufficient.

Where the document reproduces a factual API record, validate all claimed dimensions that apply:

```text
identifier
owner/source page
category
default
dependency
state
purpose/description
```

Fail when a real identifier is attached to an incorrect owner, default, dependency, state, or current/historical classification.

## 18.3 GATE C — SOURCE-DOMAIN AUTHORITY

Apply domain-scoped authority:

```text
Exact CSS property identifier/default
    → dedicated current CSS API page

Hook parameter/input contract
    → dedicated hook documentation

Framework architecture/layering
    → current Theme Framework architecture documentation

Component markup/selector/version transition
    → dedicated selector/upgrade/current documentation
```

Do not flatten all official pages into one total precedence list.

## 18.4 GATE D — INTERNAL TOKEN BOUNDARY

Any `--gform-theme-*` occurrence must not be promoted into public `--gf-*` API unless a current public official source independently establishes it as public API.

Otherwise classify it as:

```text
IMPLEMENTATION DETAIL
```

## 18.5 GATE E — HISTORICAL API BOUNDARY

Properties shown only in version history, 2.7-era examples, migration tables, or deprecated material must not be represented as current API without current dedicated-reference confirmation.

## 18.6 GATE F — QUICK LOOKUP FIDELITY

Every exact property in §17 must resolve to:

1. a current API definition elsewhere in this reference; and
2. current official evidence.

Wildcard entries are navigation shorthand only.

## 18.7 Canonical release condition

The front matter may use:

```yaml
status: "canonical-project-reference"
```

only when:

```text
GATE A = PASS
GATE B = PASS
GATE C = PASS
GATE D = PASS
GATE E = PASS
GATE F = PASS
```

Any `FAIL` or `INCOMPLETE` suspends canonical status.

---

# 19. Official Source Index

Only Gravity Forms-owned official documentation is normative for this reference.

## Architecture / concepts / compatibility

| Source | Canonical URL | Used For |
|---|---|---|
| Theme Framework CSS API Reference | https://docs.css.gravity.com/ | Current CSS API taxonomy |
| Theme Framework Introduction | https://docs.gravityforms.com/theme-framework-introduction/ | Framework introduction/history |
| Quick Start Guide | https://docs.gravityforms.com/quick-start-guide/ | Architecture, Orbital, scoping, wrapper evidence |
| Core Concepts | https://docs.gravityforms.com/theme-framework/ | Reset/Foundation/Framework, wrappers, utilities |
| CSS API | https://docs.gravityforms.com/css-api/ | Global/local API mental model |
| Theme Layers | https://docs.gravityforms.com/theme-layers/ | Theme Layers role |
| Theme Framework FAQ | https://docs.gravityforms.com/theme-framework-faq/ | Customization, registration limitation, wrapper-conflict evidence |
| Theme Framework Upgrade Guide | https://docs.gravityforms.com/theme-framework-upgrade-guide/ | 2.8 API migration |
| CSS Element Naming Structure | https://docs.gravityforms.com/basic-structure/ | Current wrapper/ID evidence |
| CSS Visual Guide and Design Overview | https://docs.gravityforms.com/design-overview/ | Targeting/scoping/design guidance and stale-example conflict |
| Form Themes and Style Settings | https://docs.gravityforms.com/form-themes-and-style-settings/ | Orbital/style-setting/default-theme behavior |
| `gform_default_styles` | https://docs.gravityforms.com/gform_default_styles/ | Exact style-setting input contract |
| Submit Button CSS Selectors | https://docs.gravityforms.com/submit-button-css-selectors/ | Current submit markup/spinner behavior |
| Save and Continue Link CSS Selectors | https://docs.gravityforms.com/save-and-continue-link-css/ | Save/Continue selectors |
| Form Confirmation CSS Selectors | https://docs.gravityforms.com/form-confirmation/ | Confirmation selectors |
| Gravity Forms 2.9 Key Features | https://docs.gravityforms.com/gravity-forms-2-9-key-features/ | 2.9 compatibility |
| Checks Before Upgrading to Gravity Forms 3.0 | https://docs.gravityforms.com/checks-before-upgrading-to-gravity-forms-3-0/ | 3.0 markup/datepicker changes |
| Gravity Forms Changelog | https://docs.gravityforms.com/gravityforms-change-log/ | Release/version evidence |

## Base API

| API | Canonical URL |
|---|---|
| Borders | https://docs.css.gravity.com/framework.api._borders.html |
| Colors | https://docs.css.gravity.com/framework.api._colors.html |
| Field Layout & Spacing | https://docs.css.gravity.com/framework.api._layout.html |
| Form Layout & Spacing | https://docs.css.gravity.com/foundation.api._layout.html |
| Icons | https://docs.css.gravity.com/framework.api._icons.html |
| Transitions & Animation | https://docs.css.gravity.com/framework.api._transitions.html |
| Typography | https://docs.css.gravity.com/framework.api._typography.html |

## Controls API

| API | Canonical URL |
|---|---|
| Base | https://docs.css.gravity.com/framework.controls.default._api-global.html |
| Button | https://docs.css.gravity.com/framework.controls.button._api-global.html |
| Choice | https://docs.css.gravity.com/framework.controls.choice._api-global.html |
| Date | https://docs.css.gravity.com/framework.controls.date._api-global.html |
| Description | https://docs.css.gravity.com/framework.controls.description._api-global.html |
| File | https://docs.css.gravity.com/framework.controls.file._api-global.html |
| Label | https://docs.css.gravity.com/framework.controls.label._api-global.html |
| Number | https://docs.css.gravity.com/framework.controls.number._api-global.html |
| Readonly | https://docs.css.gravity.com/framework.controls.readonly._api-global.html |
| Select | https://docs.css.gravity.com/framework.controls.select._api-global.html |
| Textarea | https://docs.css.gravity.com/framework.controls.textarea._api-global.html |

## Fields API

| API | Canonical URL |
|---|---|
| Choice | https://docs.css.gravity.com/framework.fields.choice._api-global.html |
| Date | https://docs.css.gravity.com/framework.fields.date._api-global.html |
| List | https://docs.css.gravity.com/framework.fields.list._api-global.html |
| Page | https://docs.css.gravity.com/framework.fields.page._api-global.html |
| Password | https://docs.css.gravity.com/framework.fields.password._api-global.html |
| Product | https://docs.css.gravity.com/framework.fields.product._api-global.html |
| Repeater | https://docs.css.gravity.com/framework.fields.repeater._api-global.html |
| Section | https://docs.css.gravity.com/framework.fields.section._api-global.html |

## Form API

| API | Canonical URL |
|---|---|
| Spinner | https://docs.css.gravity.com/framework.form.spinner._api-global.html |
| Validation | https://docs.css.gravity.com/framework.form.validation._api-global.html |

## Utilities

| API | Canonical URL |
|---|---|
| Complex Field Grid | https://docs.css.gravity.com/foundation.layout._grid.html |
| Foundation Utility Classes | https://docs.css.gravity.com/foundation.base._utils.html |

---

# 20. Documentation Coverage Status

The current official CSS API navigation inspected for this snapshot contains:

```text
Base
├── Borders
├── Colors
├── Field Layout & Spacing
├── Form Layout & Spacing
├── Icons
├── Transitions & Animation
└── Typography

Controls
├── Base
├── Button
├── Choice
├── Date
├── Description
├── File
├── Label
├── Number
├── Readonly
├── Select
└── Textarea

Fields
├── Choice
├── Date
├── List
├── Page
├── Password
├── Product
├── Repeater
└── Section

Form
├── Spinner
└── Validation

Utility Classes
├── Field Grid
└── Foundation
```

Architecture/compatibility sources inspected include:

```text
Theme Framework Introduction
Quick Start Guide
Core Concepts
CSS API
Theme Layers
Theme Framework FAQ
Theme Framework Upgrade Guide
CSS Element Naming Structure
Design Overview
Form Themes and Style Settings
gform_default_styles
Submit Button CSS Selectors
Save and Continue CSS Selectors
Form Confirmation CSS Selectors
Gravity Forms 2.9 Key Features
Gravity Forms 3.0 upgrade checks
Gravity Forms changelog
```

## Documentation Coverage Gaps

No major CSS API branch exposed by the current official CSS API navigation was intentionally omitted.

Known upstream limitations remain:

1. Some high-level official pages contain historical/stale identifier examples.
2. Some official API tables expose incomplete or self-referential defaults.
3. Some public `--gf-*` defaults reference internal-looking `--gform-theme-*` values not separately exposed as public API.
4. Some Core Concepts modifier names are rendered with ambiguous dash typography.
5. Current official sources still conflict over the Gravity Forms 2.5 wrapper (`.gravity-theme` vs `.gform_theme`).
6. The Colors page still references `--gf-ctrl-shadow-color-focus` in a `Used by` relationship although the dedicated current Controls — Base inventory does not define it.
7. This file intentionally does not reproduce large encoded SVG data-URI literals.
8. This snapshot can become stale after future Gravity Forms changes.

These limitations are preserved as explicit ambiguity or implementation-detail boundaries; they do not authorize inference.

---

# 20.1 Canonical Validation Record

```yaml
validation_date: "2026-09-17"
official_sources_only: true
gate_a: PASS
gate_b: PASS
gate_c: PASS
gate_d: PASS
gate_e: PASS
gate_f: PASS
canonical_status: ACTIVE
current_gf_identifiers_validated: 748
failed_or_unverified_current_identifiers: 0
repaired_current_identifier_defects_this_pass: 0
```

### Validation scope

Gate A was executed by extracting every literal current usable `--gf-*` identifier from this candidate, excluding only explicitly labeled historical/incorrect/conflict/wildcard evidence, and checking exact spelling against the current owning official CSS API page or explicit current official CSS API architecture documentation.

Gate B was executed across every represented API record in §§4–8. Where this reference reproduces an identifier, owner/category, default, dependency, state, or purpose, the represented claim was checked against the owning current official page. No copied default/dependency mismatch remained after this pass.

### Defects repaired in this hardening pass

- Replaced broad front-matter authority metadata with domain-scoped implementation-fact-evidence metadata and both official source roots.
- Preserved `.gravity-theme` as the preferred current Gravity Forms 2.5 wrapper in the wrapper table while restoring the live `.gravity-theme` vs `.gform_theme` official-documentation conflict as `DOCUMENTATION AMBIGUOUS`.
- Revalidated the full `gform_default_styles` accepted-key list against its dedicated current hook documentation and retained the explicit “style-setting keys, not arbitrary raw `--gf-*` names” boundary.
- Added the live Colors `Used by` vs Controls — Base conflict for `--gf-ctrl-shadow-color-focus`; the property is not promoted into the current usable API set.
- Revalidated Choice Controls and Date Field exact identifiers and their explicitly rejected aliases.
- Revalidated Gravity Forms 3.0 submit-button/spinner/date-picker guidance and current custom-theme registration limitation.
- Reconfirmed internal `--gform-theme-*` references as implementation detail rather than public `--gf-*` API.

### Unresolved official documentation ambiguities

1. Gravity Forms 2.5 wrapper: `.gravity-theme` vs `.gform_theme`.
2. Colors `Used by` references `--gf-ctrl-shadow-color-focus`, while dedicated Controls — Base does not define it.
3. Design Overview publishes stale/conflicting control property names relative to dedicated current CSS API.
4. High-level/historical CSS API material contains pre-2.8 naming examples.
5. `--gf-ctrl-btn-icon-color-focus-simple` has a self-referential documented default.
6. `--gf-ctrl-select-dropdown-option-shadow-hover` has no published default in its current table.
7. Some public property defaults reference internal-looking `--gform-theme-*` values.
8. Some Core Concepts modifier names have ambiguous rendered dash characters.

---

# 21. Final Agent Safety Checklist

Before emitting or approving Gravity Forms Theme Framework code:

```text
[ ] Did I consult this reference first?

[ ] Does every literal current --gf-* identifier exist in the
    current official API?

[ ] Did I avoid inventing a property from naming convention?

[ ] Am I using current 2.8+ naming rather than historical names?

[ ] Did I distinguish public --gf-* API from --gform-theme-* internals?

[ ] Is the override placed at the correct global/form/field/component scope?

[ ] Did I consider a higher-level semantic token first?

[ ] Did I preserve separate hover/focus/error/disabled states where relevant?

[ ] Did I preserve Foundation?

[ ] Am I relying on a documented wrapper/class rather than an observed
    Orbital implementation detail?

[ ] If targeting the Gravity Forms 2.5 theme, did I account for the
    current .gravity-theme vs .gform_theme documentation conflict?

[ ] If using gform_default_styles, am I passing documented style-setting
    keys rather than arbitrary raw --gf-* property names?

[ ] Did I avoid treating --gf-ctrl-shadow-color-focus as verified current
    API merely because the Colors page references it?

[ ] Did I account for Gravity Forms 3.0 button markup where relevant?

[ ] Did I avoid depending on old jQuery UI datepicker implementation details?

[ ] If official sources conflict, did I apply domain-scoped authority?

[ ] Did I preserve ambiguity instead of guessing?

[ ] Would the ZERO-INVENTION gate pass?

[ ] Would the API-FIDELITY gate pass?

[ ] If current official documentation differs from this file,
    did I treat current official documentation as authoritative?
```

---

# 22. Maintenance Rule

This file is a **snapshot**, not an eternal source of truth.

Revalidate it when:

```text
Gravity Forms major/minor release
        OR
Theme Framework CSS API changes
        OR
official documentation changes
        OR
an implementation requires an undocumented capability
        OR
a property fails ZERO-INVENTION/API-FIDELITY validation
```

Maintenance sequence:

```text
current local reference
        ↓
detect missing/conflicting requirement
        ↓
current official documentation
        ↓
verify exact identifier / contract
        ↓
update local reference
        ↓
run integrity gates
        ↓
restore canonical status
```

Long-term contract:

```text
Local Reference
        ↓
Documented Theme Framework API
        ↓
Unknown?
        ↓
Official Current Documentation
        ↓
Reference Update
        ↓
Integrity Gates
```

**Never replace the final verification steps with inference.**
