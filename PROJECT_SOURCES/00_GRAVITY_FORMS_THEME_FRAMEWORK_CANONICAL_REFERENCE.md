# Gravity Forms Theme Framework — Canonical Engineering Reference

## 0. How to Use This Reference

This document is a **versioned local snapshot** of the public Gravity Forms Theme Framework contract and its current CSS API.

Its purpose is to prevent coding agents from guessing Gravity Forms selectors, wrapper classes, CSS custom properties, framework layers, or component behavior.

Use this order:

1. Consult this reference first.
2. Prefer documented Theme Framework APIs and documented `--gf-*` custom properties.
3. Never invent a `--gf-*` property.
4. Prefer an appropriate higher-level documented token before overriding multiple downstream component tokens.
5. If required information is absent, classify it as `UNKNOWN_FROM_LOCAL_REFERENCE`.
6. Consult the current official Gravity Forms documentation.
7. If current official documentation conflicts with this snapshot, the current official documentation wins and this reference should be updated.

### REFERENCE AUTHORITY RULE

When implementing or reviewing Gravity Forms Theme Framework code:

1. Consult this reference before inventing selectors, variables, wrapper classes, or framework behavior.
2. Prefer documented Gravity Forms Theme Framework APIs and CSS custom properties when they provide the required capability.
3. Never invent `--gf-*` properties.
4. Preserve documented framework layering, scoping, inheritance, and component boundaries.
5. If required behavior is not documented here, classify it as `UNKNOWN_FROM_LOCAL_REFERENCE`.
6. Only then consult the current official Gravity Forms documentation.
7. If current official documentation conflicts with this snapshot, current official documentation wins and this reference should be updated.

### Evidence labels

| Label                                  | Meaning                                                      |
| -------------------------------------- | ------------------------------------------------------------ |
| `DOCUMENTED PUBLIC CONTRACT`           | Explicitly documented by current official Gravity Forms documentation. |
| `IMPLEMENTATION DETAIL`                | Visible in official implementation-oriented documentation but not established as a stable public API. |
| `DOCUMENTATION AMBIGUOUS`              | Current official documentation is incomplete, self-conflicting, malformed, or conflicts with another current official page. |
| `NOT DOCUMENTED IN OFFICIAL REFERENCE` | Plausible behavior or identifier that was not established by the official material inspected. |
| `UNKNOWN_FROM_LOCAL_REFERENCE`         | The answer is not present in this snapshot; re-check current official documentation. |

The Theme Framework was introduced in Gravity Forms 2.7. Its core is a CSS API made from native CSS custom properties, while Theme Layers connect styles/settings to that framework. Orbital is the default implementation of the Theme Framework, not a separate replacement API.

------

## 1. Framework Mental Model

A useful mental model is:

```text
WordPress / site theme
        │
        │ typography and surrounding site context
        ▼
┌──────────────────────────┐
│ 1. Reset                 │
│ scoped Gravity Forms     │
│ reset                    │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ 2. Foundation            │
│ functional field/layout  │
│ behavior                 │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ 3. Theme Framework       │
│ public CSS API           │
│ global --gf-* properties │
│ + Orbital defaults       │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ Component / local API    │
│ controls, fields, form   │
│ UI                       │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐
│ Project customization    │
│ documented property      │
│ overrides                │
└──────────────────────────┘
```

Separately:

```text
Block settings / style settings
             │
             ▼
        Theme Layers
             │
             ├── group/enqueue styles
             ├── manage settings
             ├── connect settings → CSS API
             ├── choose where styles apply
             └── control style priority
             │
             ▼
       Theme Framework API
```

Gravity Forms documents three stylesheet/layer levels loaded in order: **Reset → Foundation → Theme Framework**. Reset is scoped to Gravity Forms markup; Foundation supplies functional styles and is required by custom themes; Theme Framework exposes most of the CSS API and applies Orbital-compatible defaults.

------

## 2. Framework Layers

### 2.1 Reset

```
DOCUMENTED PUBLIC CONTRACT
```

The Reset layer:

- applies only inside Gravity Forms markup;
- establishes the clean base used by the framework;
- intentionally allows typographic styles such as headings, paragraphs, and links to inherit from the WordPress theme;
- uses `:where(...)` with exclusions;
- is required by the Theme Framework.

Official implementation source identified by Gravity Forms:

```
assets/css/src/theme/framework/gravity-forms-theme-reset.pcss
```

### 2.2 Foundation

```
DOCUMENTED PUBLIC CONTRACT
```

Foundation is **not intended to be a standalone visual theme**. It contains functional styles required for forms, including layout/field behavior and supporting styles for enhanced controls. Gravity Forms explicitly states that a custom theme should include Foundation.

Official implementation source:

```
assets/css/src/theme/foundation/gravity-forms-theme-foundation.pcss
```

### 2.3 Theme Framework

```
DOCUMENTED PUBLIC CONTRACT
```

The Theme Framework layer contains most of the public CSS API and applies the default styling represented by Orbital. It requires Reset and Foundation.

Official implementation source:

```
assets/css/src/theme/framework/gravity-forms-theme-framework.pcss
```

### 2.4 Internal stylesheet taxonomy

Gravity Forms describes its Foundation/Framework source structure with these areas:

| Area       | Role                                   |
| ---------- | -------------------------------------- |
| `api`      | Global API/custom-property abstraction |
| `base`     | Base/global form styles                |
| `controls` | Raw form controls/components           |
| `fields`   | Gravity Forms field-type UI            |
| `form`     | Form-level UI                          |
| `layout`   | Layout styles                          |

### 2.5 Theme Layers

Theme Layers are the integration mechanism around the CSS framework. They can group and enqueue styles, manage block settings, connect settings to the CSS API, and control application/priority. They support contexts including WordPress blocks, site editing, page builders, shortcodes, and PHP rendering.

Do not confuse:

```text
Theme Framework = CSS/API contract
Theme Layers     = integration/orchestration layer
Orbital          = default user-facing implementation
```

------

## 3. Scoping and Inheritance

### 3.1 Documented wrapper classes

| Scope/theme                                  | Documented wrapper             |
| -------------------------------------------- | ------------------------------ |
| Legacy & Gravity Forms 2.5 without Framework | `.gform-theme--no-framework`   |
| Legacy pre-2.5                               | `.gform_legacy_markup_wrapper` |
| Gravity Forms 2.5                            | `.gravity-theme`               |
| Theme Framework                              | `.gform-theme`                 |
| Foundation                                   | `.gform-theme--foundation`     |
| Framework                                    | `.gform-theme--framework`      |
| Orbital                                      | `.gform-theme--orbital`        |

The normal Orbital form wrapper is documented as carrying:

```text
.gform-theme
.gform-theme--foundation
.gform-theme--framework
.gform-theme--orbital
```

The wrapper ID follows:

```text
#gform_wrapper_{form_id}
```

and individual field wrappers use:

```text
#field_{form_id}_{field_id}
```

### 3.2 Scope levels

Gravity Forms explicitly identifies three important scopes:

```text
Global scope
    ↓
all qualifying forms

Form scope
    ↓
a particular form wherever rendered

Block/embed scope
    ↓
one particular rendered instance
```

Because several forms can coexist on one page, theme-specific styles must remain correctly scoped.

### 3.3 CSS custom-property inheritance

The framework uses normal CSS custom-property inheritance. A property placed on a framework/form wrapper can cascade to descendants that consume it.

Block style settings generate property overrides inside a `<style>` element placed as the first child of the form wrapper and scoped to the individual rendered form.

### 3.4 Documented targeting patterns

Current official design documentation describes these scopes:

```text
All Theme Framework forms:
.gform-theme--framework

One form:
.gform-theme--framework#gform_wrapper_{form_id}

Forms on a page:
.page-id-{page_id} .gform-theme--framework

A field type:
.gform-theme--framework .gfield--type-{type}

One field:
.gform-theme--framework #field_{form_id}_{field_id}
```

### 3.5 Field type classes

Documented classes include:

```text
.gfield--type-{field type}
.gfield--type-choice
.gfield--input-type-{input type}
```

`gfield--type-choice` applies to choice-oriented field types/settings such as checkbox, radio, and consent.

### 3.6 Framework exclusion classes

| Class                              | Effect                                                       |
| ---------------------------------- | ------------------------------------------------------------ |
| `.gform-theme__disable`            | Excludes the element and descendants from Reset and Framework styling |
| `.gform-theme__disable-reset`      | Excludes Reset                                               |
| `.gform-theme__disable-framework`  | Excludes Framework styling                                   |
| `.gform-theme__no-reset--el`       | Documented design utility for avoiding reset on an element   |
| `.gform-theme__no-reset--children` | Documented design utility for avoiding reset on descendants  |

The first three are documented in Core Concepts; the latter two are documented in the current design overview.

### 3.7 Important scoping rule

Do **not** assume that a selector observed in Orbital's generated CSS is automatically a public Theme Framework contract.

Prefer, in order:

```text
documented Theme Framework custom property
        ↓
documented wrapper / utility / component class
        ↓
documented structural selector
        ↓
direct implementation-specific selector only when required
```

------

## 4. CSS API Mental Model

Gravity Forms describes two kinds of custom properties:

```text
GLOBAL PROPERTY
    ↓ default/input for
LOCAL/COMPONENT PROPERTY
    ↓ consumed by
CSS rule / component
```

Global properties apply broadly. Local properties exist in narrower component contexts and commonly default to global properties. Gravity Forms recommends favoring the global scope where appropriate.

A representative documented relationship is:

```text
--gf-color-in-ctrl
        ↓
--gf-ctrl-bg-color
        ↓
--gf-local-bg-color
        ↓
background
```

The CSS API article explicitly documents local-property examples including:

```text
--gf-local-bg-color
--gf-local-radius
--gf-local-shadow
--gf-local-color
```

Do not extrapolate additional `--gf-local-*` identifiers unless documented.

### 4.1 Override strategy

When a default is expressed as:

```text
--component-token: var(--higher-level-token)
```

that relationship is part of the documented API.

Example:

```text
--gf-ctrl-bg-color: var(--gf-color-in-ctrl)
--gf-ctrl-border-color-focus: var(--gf-color-primary)
--gf-ctrl-radius: var(--gf-radius)
```

Therefore:

```text
Want system-wide intent?
    → change higher-level token

Want all controls only?
    → change --gf-ctrl-* token

Want one component?
    → change component token

Want one form/field instance?
    → scope the documented token more narrowly
```

This follows the documented property dependency structure rather than inventing an independent dependency graph.

### 4.2 State-specific properties

Many component APIs expose explicit states:

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

Use those documented state properties rather than assuming one base value controls all states.

------

# 5. Base / Global API

The current CSS API root exposes these Base categories:

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

| Property             | Purpose               | Default | Relationship                                   | Source |
| -------------------- | --------------------- | ------- | ---------------------------------------------- | ------ |
| `--gf-radius`        | Base framework radius | `3px`   | Feeds control/button/component radius defaults | B01    |
| `--gf-radius-max-sm` | Max small radius      | `2px`   | Used by size-bounded component radius          | B01    |
| `--gf-radius-max-md` | Max medium radius     | `3px`   | Used by size-bounded component radius          | B01    |
| `--gf-radius-max-lg` | Max large radius      | `8px`   | Used by larger controls/components             | B01    |

## 5.2 Colors

### Primary

| Property                          | Default         |
| --------------------------------- | --------------- |
| `--gf-color-primary`              | `#204ce5`       |
| `--gf-color-primary-rgb`          | `45, 127, 251`  |
| `--gf-color-primary-contrast`     | `#fff`          |
| `--gf-color-primary-contrast-rgb` | `255, 255, 255` |
| `--gf-color-primary-darker`       | `#044ad3`       |
| `--gf-color-primary-lighter`      | `#044ad3`       |

`--gf-color-primary` feeds documented focus, primary-button, spinner, progress, image-choice, and related component defaults. The current source displays the same default for `--gf-color-primary-darker` and `--gf-color-primary-lighter`; preserve that value rather than “correcting” it locally.

### Secondary

| Property                            | Default         |
| ----------------------------------- | --------------- |
| `--gf-color-secondary`              | `#fff`          |
| `--gf-color-secondary-rgb`          | `255, 255, 255` |
| `--gf-color-secondary-contrast`     | `#112337`       |
| `--gf-color-secondary-contrast-rgb` | `17, 35, 55`    |
| `--gf-color-secondary-darker`       | `#f2f3f5`       |
| `--gf-color-secondary-lighter`      | `#f2f3f5`       |

### Outside-control dark

| Property                           | Default       |
| ---------------------------------- | ------------- |
| `--gf-color-out-ctrl-dark`         | `#585e6a`     |
| `--gf-color-out-ctrl-dark-rgb`     | `88, 94, 106` |
| `--gf-color-out-ctrl-dark-darker`  | `#112337`     |
| `--gf-color-out-ctrl-dark-lighter` | `#686e77`     |

### Outside-control light

| Property                            | Default         |
| ----------------------------------- | --------------- |
| `--gf-color-out-ctrl-light`         | `#e5e7eb`       |
| `--gf-color-out-ctrl-light-rgb`     | `229, 231, 235` |
| `--gf-color-out-ctrl-light-darker`  | `#d2d5db`       |
| `--gf-color-out-ctrl-light-lighter` | `#f2f3f5`       |

### Inside-control base

| Property                          | Default         |
| --------------------------------- | --------------- |
| `--gf-color-in-ctrl`              | `#fff`          |
| `--gf-color-in-ctrl-rgb`          | `255, 255, 255` |
| `--gf-color-in-ctrl-contrast`     | `#112337`       |
| `--gf-color-in-ctrl-contrast-rgb` | `17, 35, 55`    |
| `--gf-color-in-ctrl-darker`       | `#f2f3f5`       |
| `--gf-color-in-ctrl-lighter`      | `#f2f3f5`       |

### Inside-control primary

| Property                                  | Default                                |
| ----------------------------------------- | -------------------------------------- |
| `--gf-color-in-ctrl-primary`              | `var(--gf-color-primary)`              |
| `--gf-color-in-ctrl-primary-rgb`          | `var(--gf-color-primary-rgb)`          |
| `--gf-color-in-ctrl-primary-contrast`     | `var(--gf-color-primary-contrast)`     |
| `--gf-color-in-ctrl-primary-contrast-rgb` | `var(--gf-color-primary-contrast-rgb)` |
| `--gf-color-in-ctrl-primary-darker`       | `var(--gf-color-primary-darker)`       |
| `--gf-color-in-ctrl-primary-lighter`      | `var(--gf-color-primary-lighter)`      |

### Inside-control dark/light

| Property                           | Default         |
| ---------------------------------- | --------------- |
| `--gf-color-in-ctrl-dark`          | `#585e6a`       |
| `--gf-color-in-ctrl-dark-rgb`      | `88, 94, 106`   |
| `--gf-color-in-ctrl-dark-darker`   | `#112337`       |
| `--gf-color-in-ctrl-dark-lighter`  | `#686e77`       |
| `--gf-color-in-ctrl-light`         | `#e5e7eb`       |
| `--gf-color-in-ctrl-light-rgb`     | `229, 231, 235` |
| `--gf-color-in-ctrl-light-darker`  | `#d2d5db`       |
| `--gf-color-in-ctrl-light-lighter` | `#f2f3f5`       |

### Semantic danger/success

| Property                          | Default         |
| --------------------------------- | --------------- |
| `--gf-color-danger`               | `#c02b0a`       |
| `--gf-color-danger-rgb`           | `192, 43, 10`   |
| `--gf-color-danger-contrast`      | `#fff`          |
| `--gf-color-danger-contrast-rgb`  | `255, 255, 255` |
| `--gf-color-success`              | `#399f4b`       |
| `--gf-color-success-rgb`          | `57, 159, 75`   |
| `--gf-color-success-contrast`     | `#fff`          |
| `--gf-color-success-contrast-rgb` | `255, 255, 255` |

## 5.3 Field Layout & Spacing

| Property                                | Default                                | Purpose                                  |
| --------------------------------------- | -------------------------------------- | ---------------------------------------- |
| `--gf-padding-x`                        | `12px`                                 | Shared horizontal padding                |
| `--gf-padding-y`                        | `12px`                                 | Shared vertical padding                  |
| `--gf-label-space-primary`              | `8px`                                  | Primary label spacing                    |
| `--gf-label-choice-field-space-primary` | `12px`                                 | Primary label spacing for choice fields  |
| `--gf-label-space-x-secondary`          | `12px`                                 | Secondary-label horizontal spacing       |
| `--gf-label-space-y-sm-secondary`       | `-1px`                                 | Secondary-label vertical spacing, small  |
| `--gf-label-space-y-md-secondary`       | `0`                                    | Secondary-label vertical spacing, medium |
| `--gf-label-space-y-lg-secondary`       | `1px`                                  | Secondary-label vertical spacing, large  |
| `--gf-label-space-y-xl-secondary`       | `4px`                                  | Secondary-label vertical spacing, XL     |
| `--gf-label-space-y-secondary`          | `var(--gf-label-space-y-md-secondary)` | Current secondary vertical spacing       |
| `--gf-label-space-tertiary`             | `8px`                                  | Tertiary label spacing                   |
| `--gf-desc-space`                       | `8px`                                  | Description spacing                      |
| `--gf-desc-choice-field-space`          | `12px`                                 | Choice-field description spacing         |

## 5.4 Form Layout & Spacing

| Property                          | Default                                                      | Purpose                                |
| --------------------------------- | ------------------------------------------------------------ | -------------------------------------- |
| `--gf-form-gap-x`                 | `16px`                                                       | Form horizontal gap                    |
| `--gf-form-gap-y`                 | `40px`                                                       | Form vertical gap                      |
| `--gf-form-footer-margin-y-start` | `24px`                                                       | Footer start margin                    |
| `--gf-form-footer-gap`            | `8px`                                                        | Footer item gap                        |
| `--gf-field-gap-x`                | `12px`                                                       | Field horizontal gap                   |
| `--gf-field-gap-y`                | `12px`                                                       | Field vertical gap                     |
| `--gf-field-date-width`           | `168px`                                                      | Date field width                       |
| `--gf-field-time-width`           | `110px`                                                      | Time field width                       |
| `--gf-field-list-btns-gap`        | `8px`                                                        | List-button gap                        |
| `--gf-field-list-btns-width`      | `calc(32px + var(--gf-field-list-btns-gap) + var(--gf-field-gap-x))` | Reserved list-button width             |
| `--gf-field-pg-steps-gap-y`       | `8px`                                                        | Page-step vertical gap                 |
| `--gf-field-pg-steps-gap-x`       | `24px`                                                       | Page-step horizontal gap               |
| `--gf-label-width`                | `30%`                                                        | Label width used by applicable layouts |
| `--gf-label-req-gap`              | `6px`                                                        | Required-indicator gap                 |

## 5.5 Icons

| Property                                | Default / meaning            |
| --------------------------------------- | ---------------------------- |
| `--gf-icon-font-family`                 | `"gform-icons-orbital"`      |
| `--gf-icon-font-size`                   | `20px`                       |
| `--gf-icon-ctrl-checkbox`               | `"\e900"`                    |
| `--gf-icon-ctrl-select-down`            | `"\e901"`                    |
| `--gf-icon-ctrl-select-up`              | `"\e902"`                    |
| `--gf-icon-ctrl-select`                 | Official inline SVG data URI |
| `--gf-icon-ctrl-search`                 | Official inline SVG data URI |
| `--gf-icon-ctrl-cancel`                 | `"\e918"`                    |
| `--gf-icon-ctrl-number`                 | Official inline SVG data URI |
| `--gf-icon-ctrl-pwd-hidden`             | `"\e90a"`                    |
| `--gf-icon-ctrl-pwd-visible`            | `"\e909"`                    |
| `--gf-icon-ctrl-list-item-add`          | `"\e90f"`                    |
| `--gf-icon-ctrl-list-item-remove`       | `"\e90e"`                    |
| `--gf-icon-ctrl-save-continue`          | `"\e910"`                    |
| `--gf-icon-ctrl-pg-numbers-complete`    | `"\e90b"`                    |
| `--gf-icon-ctrl-file`                   | `"\e911"`                    |
| `--gf-icon-ctrl-file-completed`         | `"\e90c"`                    |
| `--gf-icon-ctrl-file-cancel`            | `"\e904"`                    |
| `--gf-icon-ctrl-file-remove`            | `"\e919"`                    |
| `--gf-icon-ctrl-datepicker`             | `"\e91a"`                    |
| `--gf-icon-ctrl-datepicker-left`        | `"\e91b"`                    |
| `--gf-icon-ctrl-datepicker-right`       | `"\e91c"`                    |
| `--gf-icon-ctrl-img-choice-placeholder` | `"\e922"`                    |
| `--gf-icon-tooltip-error`               | `"\e906"`                    |

For large SVG data URI defaults, this normalized reference intentionally records the exact API identifier and the default's type instead of duplicating the complete encoded SVG. Retrieve the literal from B05 if required.

## 5.6 Transitions

| Property                   | Default                         |
| -------------------------- | ------------------------------- |
| `--gf-transition-duration` | `0.15s`                         |
| `--gf-transition-ctrl`     | `var(--gf-transition-duration)` |

## 5.7 Typography

| Group     | Property                        | Default                      |
| --------- | ------------------------------- | ---------------------------- |
| Base      | `--gf-font-family-base`         | `initial`                    |
| Base      | `--gf-font-style-base`          | `normal`                     |
| Primary   | `--gf-font-family-primary`      | `var(--gf-font-family-base)` |
| Primary   | `--gf-font-size-primary`        | `14px`                       |
| Primary   | `--gf-font-style-primary`       | `var(--gf-font-style-base)`  |
| Primary   | `--gf-font-weight-primary`      | `400`                        |
| Primary   | `--gf-letter-spacing-primary`   | `0`                          |
| Primary   | `--gf-line-height-primary`      | `1.5`                        |
| Secondary | `--gf-font-family-secondary`    | `var(--gf-font-family-base)` |
| Secondary | `--gf-font-size-secondary`      | `14px`                       |
| Secondary | `--gf-font-style-secondary`     | `var(--gf-font-style-base)`  |
| Secondary | `--gf-font-weight-secondary`    | `500`                        |
| Secondary | `--gf-letter-spacing-secondary` | `0`                          |
| Secondary | `--gf-line-height-secondary`    | `1.43`                       |
| Tertiary  | `--gf-font-family-tertiary`     | `var(--gf-font-family-base)` |
| Tertiary  | `--gf-font-size-tertiary`       | `14px`                       |
| Tertiary  | `--gf-font-style-tertiary`      | `var(--gf-font-style-base)`  |
| Tertiary  | `--gf-font-weight-tertiary`     | `400`                        |
| Tertiary  | `--gf-letter-spacing-tertiary`  | `0`                          |
| Tertiary  | `--gf-line-height-tertiary`     | `1.43`                       |

The base font family intentionally permits inheritance from the surrounding WordPress/site theme.

------

# 6. Controls API

## 6.1 Control Base

The Base Control API is the common default layer for form controls.

### Background and border

| Property                          | Default                                               |
| --------------------------------- | ----------------------------------------------------- |
| `--gf-ctrl-bg-color`              | `var(--gf-color-in-ctrl)`                             |
| `--gf-ctrl-bg-color-hover`        | `var(--gf-ctrl-bg-color)`                             |
| `--gf-ctrl-bg-color-focus`        | `var(--gf-ctrl-bg-color)`                             |
| `--gf-ctrl-bg-color-disabled`     | `var(--gf-color-in-ctrl-light-lighter)`               |
| `--gf-ctrl-bg-color-error`        | `var(--gf-ctrl-bg-color)`                             |
| `--gf-ctrl-border-color`          | `var(--gf-color-in-ctrl-dark-lighter)`                |
| `--gf-ctrl-border-color-hover`    | `var(--gf-ctrl-border-color)`                         |
| `--gf-ctrl-border-color-focus`    | `var(--gf-color-primary)`                             |
| `--gf-ctrl-border-color-disabled` | `var(--gf-color-in-ctrl-light-darker)`                |
| `--gf-ctrl-border-color-error`    | `var(--gf-color-danger)`                              |
| `--gf-ctrl-border-style`          | `solid`                                               |
| `--gf-ctrl-border-width`          | `1px`                                                 |
| `--gf-ctrl-radius`                | `var(--gf-radius)`                                    |
| `--gf-ctrl-radius-max-sm`         | `min(var(--gf-ctrl-radius), var(--gf-radius-max-sm))` |
| `--gf-ctrl-radius-max-md`         | `min(var(--gf-ctrl-radius), var(--gf-radius-max-md))` |
| `--gf-ctrl-radius-max-lg`         | `min(var(--gf-ctrl-radius), var(--gf-radius-max-lg))` |
| `--gf-ctrl-outline-color`         | `transparent`                                         |
| `--gf-ctrl-outline-color-focus`   | `rgba(var(--gf-color-primary-rgb), 0.65)`             |
| `--gf-ctrl-outline-offset`        | `1px`                                                 |
| `--gf-ctrl-outline-style`         | `solid`                                               |
| `--gf-ctrl-outline-width`         | `0`                                                   |
| `--gf-ctrl-outline-width-focus`   | `3px`                                                 |

### Color, effects, sizing, typography

| Property                        | Default                                           |
| ------------------------------- | ------------------------------------------------- |
| `--gf-ctrl-color`               | `var(--gf-color-in-ctrl-contrast)`                |
| `--gf-ctrl-color-hover`         | `var(--gf-ctrl-color)`                            |
| `--gf-ctrl-color-focus`         | `var(--gf-ctrl-color)`                            |
| `--gf-ctrl-color-disabled`      | `rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.6)` |
| `--gf-ctrl-color-error`         | `var(--gf-ctrl-color)`                            |
| `--gf-ctrl-icon-color`          | `var(--gf-color-in-ctrl-dark-lighter)`            |
| `--gf-ctrl-icon-color-hover`    | `var(--gf-color-in-ctrl-dark-darker)`             |
| `--gf-ctrl-icon-color-focus`    | `var(--gf-ctrl-icon-color-hover)`                 |
| `--gf-ctrl-icon-color-disabled` | `var(--gf-ctrl-icon-color)`                       |
| `--gf-ctrl-shadow`              | `0 1px 4px rgba(18, 25, 97, 0.0779552)`           |
| `--gf-ctrl-accent-color`        | `var(--gf-color-in-ctrl-primary)`                 |
| `--gf-ctrl-appearance`          | `none`                                            |
| `--gf-ctrl-size-sm`             | `35px`                                            |
| `--gf-ctrl-size-md`             | `38px`                                            |
| `--gf-ctrl-size-lg`             | `47px`                                            |
| `--gf-ctrl-size-xl`             | `54px`                                            |
| `--gf-ctrl-size`                | `var(--gf-ctrl-size-md)`                          |
| `--gf-ctrl-padding-x`           | `var(--gf-padding-x)`                             |
| `--gf-ctrl-padding-y`           | `0`                                               |
| `--gf-ctrl-transition`          | `var(--gf-transition-ctrl)`                       |
| `--gf-ctrl-font-family`         | `var(--gf-font-family-primary)`                   |
| `--gf-ctrl-font-size`           | `var(--gf-font-size-primary)`                     |
| `--gf-ctrl-font-style`          | `var(--gf-font-style-base)`                       |
| `--gf-ctrl-font-weight`         | `var(--gf-font-weight-primary)`                   |
| `--gf-ctrl-letter-spacing`      | `var(--gf-letter-spacing-primary)`                |
| `--gf-ctrl-line-height`         | `var(--gf-ctrl-size)`                             |

### Placeholder

| Property                               | Default                                           |
| -------------------------------------- | ------------------------------------------------- |
| `--gf-ctrl-placeholder-color`          | `rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.7)` |
| `--gf-ctrl-placeholder-font-family`    | `var(--gf-ctrl-font-family)`                      |
| `--gf-ctrl-placeholder-font-size`      | `var(--gf-ctrl-font-size)`                        |
| `--gf-ctrl-placeholder-font-style`     | `var(--gf-ctrl-font-style)`                       |
| `--gf-ctrl-placeholder-font-weight`    | `var(--gf-ctrl-font-weight)`                      |
| `--gf-ctrl-placeholder-letter-spacing` | `var(--gf-ctrl-letter-spacing)`                   |
| `--gf-ctrl-placeholder-opacity`        | `1`                                               |

## 6.2 Button

### Base button

| Property                         | Default                                 |
| -------------------------------- | --------------------------------------- |
| `--gf-ctrl-btn-radius`           | `var(--gf-radius)`                      |
| `--gf-ctrl-btn-shadow`           | `0 1px 4px rgba(18, 25, 97, 0.0779552)` |
| `--gf-ctrl-btn-shadow-hover`     | `var(--gf-ctrl-btn-shadow)`             |
| `--gf-ctrl-btn-shadow-focus`     | `var(--gf-ctrl-btn-shadow)`             |
| `--gf-ctrl-btn-shadow-disabled`  | `var(--gf-ctrl-btn-shadow)`             |
| `--gf-ctrl-btn-opacity`          | `1`                                     |
| `--gf-ctrl-btn-opacity-disabled` | `0.5`                                   |
| `--gf-ctrl-btn-size-xs`          | `30px`                                  |
| `--gf-ctrl-btn-size-sm`          | `var(--gf-ctrl-size-sm)`                |
| `--gf-ctrl-btn-size-md`          | `var(--gf-ctrl-size-md)`                |
| `--gf-ctrl-btn-size-lg`          | `var(--gf-ctrl-size-lg)`                |
| `--gf-ctrl-btn-size-xl`          | `var(--gf-ctrl-size-xl)`                |
| `--gf-ctrl-btn-size`             | `var(--gf-ctrl-btn-size-md)`            |
| `--gf-ctrl-btn-padding-x-xs`     | `8px`                                   |
| `--gf-ctrl-btn-padding-x-sm`     | `12px`                                  |
| `--gf-ctrl-btn-padding-x-md`     | `16px`                                  |
| `--gf-ctrl-btn-padding-x-lg`     | `20px`                                  |
| `--gf-ctrl-btn-padding-x-xl`     | `24px`                                  |
| `--gf-ctrl-btn-padding-x`        | `var(--gf-ctrl-btn-padding-x-md)`       |
| `--gf-ctrl-btn-padding-y`        | `0`                                     |
| `--gf-ctrl-btn-font-family`      | `var(--gf-font-family-base)`            |
| `--gf-ctrl-btn-font-size-xs`     | `12px`                                  |
| `--gf-ctrl-btn-font-size-sm`     | `14px`                                  |
| `--gf-ctrl-btn-font-size-md`     | `14px`                                  |
| `--gf-ctrl-btn-font-size-lg`     | `16px`                                  |
| `--gf-ctrl-btn-font-size-xl`     | `16px`                                  |
| `--gf-ctrl-btn-font-size`        | `var(--gf-ctrl-btn-font-size-md)`       |
| `--gf-ctrl-btn-font-style`       | `var(--gf-font-style-base)`             |
| `--gf-ctrl-btn-font-weight`      | `500`                                   |
| `--gf-ctrl-btn-letter-spacing`   | `var(--gf-letter-spacing-primary)`      |
| `--gf-ctrl-btn-line-height`      | `1`                                     |
| `--gf-ctrl-btn-text-decoration`  | `none`                                  |
| `--gf-ctrl-btn-text-transform`   | `none`                                  |
| `--gf-ctrl-btn-icon`             | `none`                                  |
| `--gf-ctrl-btn-icon-size`        | `var(--gf-icon-font-size)`              |
| `--gf-ctrl-btn-icon-gap`         | `6px`                                   |
| `--gf-ctrl-btn-icon-transition`  | `var(--gf-ctrl-transition)`             |

### Primary button

The complete state families are:

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

Important defaults:

```text
bg                  = var(--gf-color-primary)
bg hover            = var(--gf-color-primary-darker)
text                = var(--gf-color-primary-contrast)
border base/hover   = transparent
border focus        = var(--gf-ctrl-btn-bg-color-hover-primary)
border width        = 1px
border style        = solid
```

### Secondary button

State families:

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

Key defaults:

```text
bg                = var(--gf-color-secondary)
bg hover          = var(--gf-color-secondary-darker)
border            = var(--gf-color-in-ctrl-light-darker)
text              = var(--gf-color-secondary-contrast)
border width      = 1px
border style      = solid
```

The current official API lists:

```text
--gf-ctrl-btn-border-color-focus-secondary:
var(--gf-ctrl-btn-bg-color-hover-primary)
```

Preserve that published dependency unless current documentation changes.

### Control button

Used for button UI inside controls such as enhanced file upload.

State families:

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

Primary defaults derive from `--gf-color-in-ctrl-primary*`.

### Simple/icon button

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

Important defaults include:

```text
background        = transparent
border base       = transparent
focus border      = var(--gf-ctrl-border-color-focus)
shadow            = none
size              = 24px
```

`DOCUMENTATION AMBIGUOUS`: the current table defines:

```text
--gf-ctrl-btn-icon-color-focus-simple:
var(--gf-ctrl-btn-icon-color-focus-simple)
```

which is a self-reference. Do not “fix” it by assumption.

## 6.3 Choice Controls

| Property                                  | Default                                           |
| ----------------------------------------- | ------------------------------------------------- |
| `--gf-ctrl-choice-check-color`            | `var(--gf-color-in-ctrl-primary)`                 |
| `--gf-ctrl-choice-check-color-disabled`   | `rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.2)` |
| `--gf-ctrl-choice-size-sm`                | `18px`                                            |
| `--gf-ctrl-choice-size-md`                | `20px`                                            |
| `--gf-ctrl-choice-size-lg`                | `22px`                                            |
| `--gf-ctrl-choice-size-xl`                | `28px`                                            |
| `--gf-ctrl-choice-size`                   | `var(--gf-ctrl-choice-size-md)`                   |
| `--gf-ctrl-choice-checkbox-radius`        | `var(--gf-ctrl-radius-max-sm)`                    |
| `--gf-ctrl-choice-checkbox-check-size-sm` | `12px`                                            |
| `--gf-ctrl-choice-checkbox-check-size-md` | `initial`                                         |
| `--gf-ctrl-choice-checkbox-check-size-lg` | `15px`                                            |
| `--gf-ctrl-choice-checkbox-check-size-xl` | `19px`                                            |
| `--gf-ctrl-choice-checkbox-check-size`    | `var(--gf-ctrl-choice-checkbox-check-size-md)`    |
| `--gf-ctrl-choice-radio-radius`           | `50%`                                             |
| `--gf-ctrl-choice-radio-content`          | `""`                                              |
| `--gf-ctrl-choice-radio-size-sm`          | `6px`                                             |
| `--gf-ctrl-choice-radio-size-md`          | `7px`                                             |
| `--gf-ctrl-choice-radio-size-lg`          | `8px`                                             |
| `--gf-ctrl-choice-radio-size-xl`          | `10px`                                            |
| `--gf-ctrl-choice-radio-size`             | `var(--gf-ctrl-choice-radio-size-md)`             |

## 6.4 Date Picker

Base/date-picker API:

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

Defaults include:

```text
background                = var(--gf-ctrl-bg-color)
padding-y                 = 16px 12px
padding-y viewport-sm     = 16px
padding-x                 = 12px
padding-x viewport-sm     = 16px
margin-y-start            = 12px
radius                    = var(--gf-ctrl-radius-max-md)
width                     = 250px
width viewport-sm         = 300px
```

Header/title API:

```text
--gf-ctrl-date-picker-header-icons-width
--gf-ctrl-date-picker-header-icons-color
--gf-ctrl-date-picker-header-icons-color-hover
--gf-ctrl-date-picker-header-icons-font-size

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

Dropdown/table API:

```text
--gf-ctrl-date-picker-dropdown-bg-img
--gf-ctrl-date-picker-dropdown-bg-position
--gf-ctrl-date-picker-dropdown-bg-size
--gf-ctrl-date-picker-dropdown-border-color
--gf-ctrl-date-picker-dropdown-border-style
--gf-ctrl-date-picker-dropdown-border-width
--gf-ctrl-date-picker-dropdown-shadow
--gf-ctrl-date-picker-dropdown-text-align

--gf-ctrl-date-picker-table-margin-y-start
--gf-ctrl-date-picker-table-margin-y-end

--gf-ctrl-date-picker-head-cell-font-size
--gf-ctrl-date-picker-head-cell-font-weight
--gf-ctrl-date-picker-head-cell-line-height
```

Cell API:

```text
--gf-ctrl-date-picker-cell-padding
--gf-ctrl-date-picker-cell-padding-y
--gf-ctrl-date-picker-cell-padding-y-viewport-sm
--gf-ctrl-date-picker-cell-height
--gf-ctrl-date-picker-cell-height-viewport-sm
--gf-ctrl-date-picker-cell-font-size
--gf-ctrl-date-picker-cell-font-weight
--gf-ctrl-date-picker-cell-line-height

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

Important exact defaults:

```text
cell padding                         = 1px
cell padding-y                       = 6px
cell height                          = 29px
cell height viewport-sm              = 40px
cell font-size                       = 14px
cell font-weight                     = 400
cell selected background             = var(--gf-color-in-ctrl-primary)
cell selected color                  = var(--gf-color-in-ctrl-primary-contrast)
cell content width                   = 27px
cell content width viewport-sm       = 100%
```

Two published defaults depend on `--gform-theme-*` identifiers rather than public `--gf-*` API identifiers:

```text
--gf-ctrl-date-picker-cell-content-bg-color-hover
    → var(--gform-theme-color-uber-light-blue)

--gf-ctrl-date-picker-cell-content-color-disabled
    → var(--gform-theme-color-uber-light)
```

Treat those `--gform-theme-*` names as `IMPLEMENTATION DETAIL`, not as public Theme Framework properties to customize.

## 6.5 Description

### Standard description

```text
--gf-ctrl-desc-color
--gf-ctrl-desc-font-family
--gf-ctrl-desc-font-size
--gf-ctrl-desc-font-style
--gf-ctrl-desc-font-weight
--gf-ctrl-desc-letter-spacing
--gf-ctrl-desc-line-height
```

Defaults derive from the outside-control dark color and tertiary typography system.

### Error description

```text
--gf-ctrl-desc-color-error
--gf-ctrl-desc-font-family-error
--gf-ctrl-desc-font-size-error
--gf-ctrl-desc-font-style-error
--gf-ctrl-desc-font-weight-error
--gf-ctrl-desc-letter-spacing-error
--gf-ctrl-desc-line-height-error
```

The error color defaults to `var(--gf-color-danger)`.

### Consent description

```text
--gf-ctrl-desc-border-color-consent
--gf-ctrl-desc-border-color-consent-focus
--gf-ctrl-desc-border-style-consent
--gf-ctrl-desc-border-width-consent
--gf-ctrl-desc-max-height-consent
```

`--gf-ctrl-desc-max-height-consent` defaults to `456px`.

## 6.6 File

### Native file control

```text
--gf-ctrl-file-padding-x
```

Default:

```text
0 var(--gf-ctrl-padding-x)
```

### Native file-button API

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

Key defaults:

```text
button bg            = var(--gf-color-secondary-darker)
button bg hover      = var(--gf-color-secondary)
button radius        = var(--gf-ctrl-radius)
font size            = 14px
font weight          = 500
margin-x             = 0 12px
padding-x            = 12px
```

### Enhanced drop zone

```text
--gf-ctrl-file-zone-border-style        = dashed
--gf-ctrl-file-zone-radius              = var(--gf-ctrl-radius-max-lg)
--gf-ctrl-file-zone-color               = rgba(var(--gf-color-in-ctrl-contrast-rgb), 0.725)
--gf-ctrl-file-zone-height              = auto
--gf-ctrl-file-zone-padding-x           = 40px
--gf-ctrl-file-zone-padding-y           = 40px
--gf-ctrl-file-zone-instructions-margin-y-end = 12px
--gf-ctrl-file-zone-font-weight         = 500
--gf-ctrl-file-zone-line-height         = 1
--gf-ctrl-file-zone-icon-color          = var(--gf-color-in-ctrl-primary)
--gf-ctrl-file-zone-icon-font-size      = 36px
--gf-ctrl-file-zone-icon-margin-y-end   = 8px
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

Notable defaults:

```text
progress gap             = 12px
progress bar bg          = var(--gf-color-out-ctrl-light)
loading bar bg           = var(--gf-color-primary)
bar height               = 6px
complete icon color      = var(--gf-color-success)
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

## 6.7 Label

The label API exposes four typography roles plus required-indicator styling.

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

### Required indicator

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

## 6.8 Number

```text
--gf-ctrl-number-spin-btn-appearance
--gf-ctrl-number-spin-btn-bg-position
--gf-ctrl-number-spin-btn-bg-size
--gf-ctrl-number-spin-btn-width
--gf-ctrl-number-spin-btn-opacity
```

Defaults:

```text
appearance       = var(--gf-ctrl-appearance)
background-pos   = center center
background-size  = 8px 14px
width            = 8px
opacity          = 1
```

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

Readonly typography derives from the normal control typography, with font weight documented as `500` and line height as `1`.

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

--gf-ctrl-multiselect-height
--gf-ctrl-multiselect-radius
--gf-ctrl-multiselect-line-height
--gf-ctrl-multiselect-padding-y
```

Defaults include:

```text
select icon        = var(--gf-icon-ctrl-select)
select icon size   = 10px
-ms-expand         = none
multi height       = 130px
multi radius       = var(--gf-ctrl-radius-max-lg)
multi line-height  = 1.5
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

`DOCUMENTATION AMBIGUOUS`: the official table currently publishes **no default value** for:

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

`--gf-ctrl-multiselect-selected-item-font-weight` currently defaults to:

```text
var(--gform-theme-font-weight-semibold)
```

Treat that `--gform-theme-*` dependency as `IMPLEMENTATION DETAIL`, not as a public `--gf-*` API to depend on directly.

## 6.11 Textarea

| Property                         | Default                        |
| -------------------------------- | ------------------------------ |
| `--gf-ctrl-textarea-height`      | `130px`                        |
| `--gf-ctrl-textarea-radius`      | `var(--gf-ctrl-radius-max-lg)` |
| `--gf-ctrl-textarea-line-height` | `1.5`                          |
| `--gf-ctrl-textarea-padding-y`   | `var(--gf-padding-y)`          |
| `--gf-ctrl-textarea-resize`      | `vertical`                     |

------

# 7. Fields API

## 7.1 Choice Fields

The field-level Choice API covers checkbox/radio/consent/image-choice field composition.

### Base

| Property                                 | Default                             |
| ---------------------------------------- | ----------------------------------- |
| `--gf-field-choice-gap`                  | `var(--gf-label-space-x-secondary)` |
| `--gf-field-choice-align-x-gap-y`        | `var(--gf-field-choice-gap)`        |
| `--gf-field-choice-align-x-gap-x`        | `16px`                              |
| `--gf-field-choice-meta-margin-y-start`  | `4px`                               |
| `--gf-field-choice-meta-space`           | `16px`                              |
| `--gf-field-choice-other-ctrl-max-width` | `256px`                             |

### Image Choice base

| Property                                           | Default                                                      |
| -------------------------------------------------- | ------------------------------------------------------------ |
| `--gf-field-img-choice-aspect-ratio`               | `1/1`                                                        |
| `--gf-field-img-choice-gap`                        | `var(--gf-field-gap-x)`                                      |
| `--gf-field-img-choice-margin-y-end`               | `12px`                                                       |
| `--gf-field-img-choice-placeholder-icon-font-size` | `60px`                                                       |
| `--gf-field-img-choice-radius-square`              | `var(--gf-ctrl-radius-max-sm)`                               |
| `--gf-field-img-choice-radius-round`               | `50%`                                                        |
| `--gf-field-img-choice-shadow`                     | `0 0 0 rgba(18, 25, 97, 0.05), 0 2px 5px rgba(18, 25, 97, 0.1), 0 1px 1px rgba(18, 25, 97, 0.15)` |
| `--gf-field-img-choice-shadow-hover`               | official multi-shadow; see D01                               |
| `--gf-field-img-choice-size-sm`                    | `125px`                                                      |
| `--gf-field-img-choice-size-md`                    | `200px`                                                      |
| `--gf-field-img-choice-size-lg`                    | `300px`                                                      |
| `--gf-field-img-choice-size`                       | `var(--gf-field-img-choice-size-md)`                         |

### Image Choice card/no-card

```text
--gf-field-img-choice-card-placeholder-bg-color
--gf-field-img-choice-card-placeholder-color
--gf-field-img-choice-card-check-ind-bg-color
--gf-field-img-choice-card-check-ind-icon-color
--gf-field-img-choice-card-space-sm
--gf-field-img-choice-card-space-md
--gf-field-img-choice-card-space-lg
--gf-field-img-choice-card-space

--gf-field-img-choice-no-card-placeholder-bg-color
--gf-field-img-choice-no-card-placeholder-color
--gf-field-img-choice-no-card-check-ind-bg-color
--gf-field-img-choice-no-card-check-ind-icon-color
```

Card spacing defaults:

```text
small   = 8px
medium  = 12px
large   = 16px
current = var(--gf-field-img-choice-card-space-md)
```

### Checked indicator

| Property                                       | Default                                             |
| ---------------------------------------------- | --------------------------------------------------- |
| `--gf-field-img-choice-check-ind-icon`         | `var(--gf-icon-ctrl-checkbox)`                      |
| `--gf-field-img-choice-check-ind-radius`       | `50%`                                               |
| `--gf-field-img-choice-check-ind-shadow`       | documented three-part `drop-shadow(...)` value      |
| `--gf-field-img-choice-check-ind-size-sm`      | `24px`                                              |
| `--gf-field-img-choice-check-ind-size-md`      | `38px`                                              |
| `--gf-field-img-choice-check-ind-size-lg`      | `64px`                                              |
| `--gf-field-img-choice-check-ind-size`         | `var(--gf-field-img-choice-check-ind-size-md)`      |
| `--gf-field-img-choice-check-ind-icon-size-sm` | `12px`                                              |
| `--gf-field-img-choice-check-ind-icon-size-md` | `var(--gf-icon-font-size)`                          |
| `--gf-field-img-choice-check-ind-icon-size-lg` | `30px`                                              |
| `--gf-field-img-choice-check-ind-icon-size`    | `var(--gf-field-img-choice-check-ind-icon-size-md)` |

Miscellaneous:

```text
--gf-field-img-choice-ctrl-opacity          = 1
--gf-field-img-choice-ctrl-opacity-disabled = 0.5
--gf-field-img-choice-other-ctrl-margin-y-start = 16px
```

## 7.2 Date Field

```text
--gf-field-date-ctrl-padding-x-end
--gf-field-date-ctrl-icon-color
--gf-field-date-ctrl-icon-color-hover
--gf-field-date-ctrl-icon-transition
--gf-field-date-ctrl-icon-custom-max-height
--gf-field-date-ctrl-icon-custom-max-width
--gf-field-date-ctrl-icon-custom-opacity
--gf-field-date-ctrl-icon-custom-opacity-hover
```

Primary padding relationship:

```text
--gf-field-date-ctrl-padding-x-end:
calc(var(--gf-ctrl-padding-x) + var(--gf-icon-font-size) + 4px)
```

Custom date icon max dimensions are `16px`; opacity defaults to `0.6` and hover to `1`.

## 7.3 List Field

```text
--gf-field-list-btn-size       = 16px
--gf-field-list-btn-radius     = 50%
--gf-field-list-btn-font-size  = 0
--gf-field-list-btn-padding-y  = 0
--gf-field-list-btn-padding-x  = 0
```

## 7.4 Page / Multi-page UI

### Page/progress typography

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

Defaults include:

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

Published theme values:

```text
blue    #204ce5
green   #31c48d
orange  #ff5a1f
red     #c02b0a
radius  100px
height  10px
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

Key defaults:

```text
number size          = 32px
number radius        = 50%
border width         = 2px
completed background = var(--gf-color-primary)
completed color      = var(--gf-color-primary-contrast)
step gap             = 12px
```

## 7.5 Password

### Base

```text
--gf-field-pwd-ctrl-padding-x-end:
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

Documented state colors:

```text
mismatch = #c02b0a
short    = #c02b0a
bad      = #ff5a1f
good     = #8b6c32
strong   = #399f4b
```

### Strength bar/indicator

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
blank     0
mismatch  65px
short     22px
bad       37px
good      46px
strong    65px
```

The current documentation includes trailing semicolons inside several displayed `var(...)` default values. Treat that punctuation as documentation presentation, not as evidence for a different API identifier.

## 7.6 Product

```text
--gf-field-prod-price-color
--gf-field-prod-quant-margin-y-end
--gf-field-prod-quant-width
```

Current defaults include:

```text
price color      = var(--gf-ctrl-label-color-primary)
quantity margin = var(--gf-field-gap-y)
quantity width  = 150px
```

## 7.7 Repeater

```text
--gf-field-repeater-gap-y
--gf-field-repeater-btn-inline-gap
--gf-field-repeater-separator-color
--gf-field-repeater-separator-size
--gf-field-repeater-nested-border-color
--gf-field-repeater-nested-border-size
--gf-field-repeater-nested-border-style
--gf-field-repeater-nested-padding-x-start
```

Key defaults:

```text
gap-y                 = var(--gf-form-gap-y)
button inline gap     = var(--gf-form-gap-x)
separator color       = var(--gf-color-out-ctrl-light-darker)
separator size        = 1px
nested border size    = 1px
nested border style   = solid
nested padding start  = 20px
```

## 7.8 Section

```text
--gf-field-section-border-color
--gf-field-section-border-style
--gf-field-section-border-width
--gf-field-section-padding-y-end
```

Defaults:

```text
border color = var(--gf-color-out-ctrl-light-darker)
border style = solid
border width = 1px
padding end  = 8px
```

------

# 8. Form-Level API

## 8.1 Spinner

```text
--gf-form-spinner-fg-color = var(--gf-color-primary)
--gf-form-spinner-bg-color = rgba(var(--gf-color-primary-rgb), 0.1)
```

## 8.2 Validation

### Base

| Property                                   | Default                                                      |
| ------------------------------------------ | ------------------------------------------------------------ |
| `--gf-form-validation-bg-color`            | `rgba(var(--gf-color-danger-rgb), 0.03)`                     |
| `--gf-form-validation-border-color`        | `rgba(var(--gf-color-danger-rgb), 0.25)`                     |
| `--gf-form-validation-border-color-focus`  | `var(--gf-color-danger)`                                     |
| `--gf-form-validation-border-width`        | `1px`                                                        |
| `--gf-form-validation-border-style`        | `solid`                                                      |
| `--gf-form-validation-radius`              | `var(--gf-ctrl-radius-max-md)`                               |
| `--gf-form-validation-outline-color-focus` | `rgba(var(--gf-color-danger-rgb), 0.65)`                     |
| `--gf-form-validation-outline-focus`       | `var(--gf-ctrl-outline-width-focus) var(--gf-ctrl-outline-style) var(--gf-form-validation-outline-color-focus)` |
| `--gf-form-validation-shadow`              | `0 1px 4px rgba(18, 25, 97, 0.0779552)`                      |
| `--gf-form-validation-color`               | `var(--gf-color-danger)`                                     |
| `--gf-form-validation-font-family`         | `var(--gf-font-family-primary)`                              |
| `--gf-form-validation-font-size`           | `var(--gf-font-size-primary)`                                |
| `--gf-form-validation-line-height`         | `1.43`                                                       |
| `--gf-form-validation-gap`                 | `8px`                                                        |
| `--gf-form-validation-margin-y`            | `0 var(--gf-form-gap-y)`                                     |
| `--gf-form-validation-padding-y`           | `20px`                                                       |
| `--gf-form-validation-padding-x`           | `16px`                                                       |

### Heading/icon

```text
--gf-form-validation-heading-color
--gf-form-validation-heading-font-family
--gf-form-validation-heading-font-size
--gf-form-validation-heading-font-weight
--gf-form-validation-heading-line-height
--gf-form-validation-heading-gap

--gf-form-validation-heading-icon-bg-color
--gf-form-validation-heading-icon-border-color
--gf-form-validation-heading-icon-border-width
--gf-form-validation-heading-icon-border-style
--gf-form-validation-heading-icon-radius
--gf-form-validation-heading-icon-color
--gf-form-validation-heading-icon-font-size
--gf-form-validation-heading-icon-size
```

### Summary list

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

Published defaults include:

```text
summary font-weight       = 400
summary margin-y-start    = 4px
summary padding-x         = 48px
link text-decoration      = underline
```

## 8.3 Submit buttons

Current selector documentation is version-sensitive.

Starting with **Gravity Forms 3.0**, form buttons use `<button>` rather than `<input>`. The current submit-button documentation describes text submit buttons, image submit buttons, form/multipage footers, and inline submit placement.

Documented identifiers include:

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

For normal theme work, primary button presentation should be driven through the documented `--gf-ctrl-btn-*-primary` API where it provides the needed behavior.

### Gravity Forms 3.0 spinner change

Starting with 3.0, the spinner is rendered inside the button. The button receives:

```text
.gform-has-spinner
```

and the loader uses:

```text
.gform-loader
```

The old spinner URL hooks documented by Gravity Forms as removed in 3.0 include:

```text
gform_ajax_spinner_url
gform_spinner_url
gform_always_show_spinner
```

## 8.4 Save and Continue

Documented Save and Continue classes include:

```text
.gform_save_link
.gform-theme-button
.gform-theme-button--secondary
```

It is rendered within:

```text
.gform_footer
```

or:

```text
.gform_page_footer
```

Documented IDs:

```text
gform_save_{form_id}_{page_number}_link
gform_save_{form_id}_footer_link
```

Its Theme Framework appearance uses the documented secondary-button API, including `--gf-ctrl-btn-*-secondary`, plus relevant button/icon properties.

## 8.5 Confirmation

Current official selector documentation identifies:

```text
.gform_confirmation_message_{form_id}
.gform-theme--framework.gform_confirmation_wrapper
.form_saved_message
.form_saved_message_sent
```

No dedicated current `--gf-*` confirmation property group was found in the CSS API taxonomy.

Classification:

```text
Confirmation selectors → DOCUMENTED PUBLIC CONTRACT
Dedicated confirmation CSS API → NOT DOCUMENTED IN OFFICIAL REFERENCE
```

------

# 9. Layout and Design

## 9.1 CSS logical properties

Gravity Forms uses CSS logical properties to support different writing directions. Theme code should preserve logical-direction behavior rather than unnecessarily replacing it with left/right assumptions.

## 9.2 Complex field grid

Official Foundation utilities:

```text
.gform-grid-row
.gform-grid-col
.gform-grid-col--size-auto
```

Current dedicated CSS API documentation says:

```text
.gform-grid-row
    → creates a grid row

.gform-grid-col
    → creates a grid column

.gform-grid-col--size-auto
    → sizes the column to the width of its content
```

Gravity Forms examples place these within a complex field container carrying both:

```text
.ginput_complex
.ginput_container
```

## 9.3 Label placement

Current visual/design documentation identifies layout classes:

```text
.top_label
.left_label
.right_label
```

and documents `--gf-label-width` as the label-width API used by applicable layouts.

## 9.4 Custom classes

The official design overview states that a custom form CSS class such as:

```text
my_form
```

results in a wrapper class:

```text
.my_form_wrapper
```

A custom field CSS class is applied to that field's wrapper.

## 9.5 Ready classes

Legacy Gravity Forms Ready Classes are not the preferred Theme Framework layout mechanism. Current design documentation notes their deprecation in the context of the form editor layout improvements introduced from Gravity Forms 2.5 onward.

------

# 10. Utility Classes

## 10.1 Foundation utility classes

### `.gform-ul-reset`

Documented behavior:

```text
list-style-type: none
margin: 0
padding: 0
```

### `.gform-text-input-reset`

Documented behavior resets:

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

with documented values including transparent background, no border/shadow/outline, inherited typography, and `width: auto`.

## 10.2 Semantic framework utility classes

For add-on/custom field markup, Gravity Forms specifically recommends using documented semantic classes such as:

```text
.gform-field-label
.gform-field-description
```

so that custom/add-on elements participate correctly in Theme Framework styling.

## 10.3 Field-control base class

Current Core Concepts documents:

```text
.gform-theme-field-control
```

as a class for making a custom element participate in standard field-control styling.

The same page displays hover/focus/disabled and size modifier names using malformed en-dash/backtick formatting.

Classification:

```text
exact modifier spelling from that rendered article:
DOCUMENTATION AMBIGUOUS
```

Do not silently convert those displayed en-dashes into `--` and treat the result as a guaranteed API without separate official confirmation.

------

# 11. Theme Authoring Workflow

A framework-compliant workflow for an AI coding agent is:

```text
1. Confirm the form is using Theme Framework / Orbital-compatible layers.
        ↓
2. Identify presentation intent:
   global / form / field type / field / component / state.
        ↓
3. Search this reference for an existing documented --gf-* API.
        ↓
4. Follow dependency relationships upward:
   Can a base color/radius/typography token express the intent?
        ↓
5. If not, select the narrowest documented component token.
        ↓
6. Apply the override at the narrowest appropriate documented scope.
        ↓
7. Use direct element CSS only when the documented API does not expose
   the required presentation behavior.
        ↓
8. Never invent a --gf-* property.
        ↓
9. If an identifier/behavior is absent:
   UNKNOWN_FROM_LOCAL_REFERENCE.
        ↓
10. Check current official documentation.
        ↓
11. If the public contract changed, update this reference.
```

The current official design overview explicitly recommends overriding `--gf-*` variables as the primary customization mechanism and using direct element property rules when no corresponding variable exists.

### Current limitation: no custom form-theme registration API

As of this snapshot, the official FAQ states:

```text
You cannot currently register a form theme.
```

The documented alternatives are:

```text
gform_default_styles
```

for global CSS API defaults, and:

```text
gform_enqueue_scripts
```

for loading custom CSS.

Therefore a project described informally as a “custom Gravity Forms theme” should not assume the existenceence of a public first-class custom-theme registration mechanism.

------

# 12. Recommended Framework Usage Patterns

These patterns are derived from current documented capabilities.

## 12.1 Prefer semantic high-level tokens

Prefer:

```text
--gf-color-primary
        ↓
dependent primary/focus/component tokens
```

over separately changing every dependent focus, spinner, progress, and primary-button value when the intended design concept is genuinely the framework's primary accent.

## 12.2 Prefer component API before direct element styling

Prefer:

```text
--gf-ctrl-bg-color
--gf-ctrl-border-color
--gf-ctrl-radius
```

over direct styling of every input/select/textarea when the requirement is common control presentation.

## 12.3 Prefer state API for state changes

For focus/error behavior, use documented state properties such as:

```text
--gf-ctrl-border-color-focus
--gf-ctrl-outline-color-focus
--gf-ctrl-outline-width-focus

--gf-ctrl-border-color-error
--gf-ctrl-bg-color-error
--gf-ctrl-color-error
```

rather than assuming the base control property automatically represents all states.

## 12.4 Scope by intent

```text
site/system design
    → framework/global scope

one form identity
    → #gform_wrapper_{form_id}

field category
    → .gfield--type-{type}

single field
    → #field_{form_id}_{field_id}
```

## 12.5 Preserve Foundation

A custom presentation layer should not discard Foundation simply because the visual style is being replaced. Gravity Forms documents Foundation as containing functionality/layout styles required for a usable custom theme.

## 12.6 Keep Orbital implementation details separate

A property beginning with:

```text
--gform-theme-
```

is not equivalent to a documented public:

```text
--gf-
```

CSS API identifier.

Do not build a custom theme contract around internal Orbital tokens merely because a public `--gf-*` default happens to reference one.

------

# 13. Known Anti-Patterns

| Anti-pattern                                                 | Why                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Inventing `--gf-*` identifiers                               | Creates a nonexistent API contract                           |
| Guessing renamed 2.7 properties                              | 2.8 introduced a breaking CSS API rename                     |
| Treating `--gform-theme-*` as public API                     | These are not documented as equivalent to public `--gf-*` tokens |
| Copying Orbital selectors wholesale                          | Orbital implementation is not the Theme Framework API        |
| Styling every control directly when a documented control token exists | Bypasses the framework abstraction and increases maintenance |
| Removing Foundation for a visual rewrite                     | Foundation contains required functional/layout behavior      |
| Applying one form's overrides globally by accident           | Violates the framework's scoping model                       |
| Assuming all states inherit from a base token                | Many components expose explicit hover/focus/error/disabled APIs |
| Correcting suspicious official defaults by intuition         | Converts documentation uncertainty into invented behavior    |
| Assuming undocumented wrapper/modifier spelling              | Selector names must be verified                              |
| Treating historical API examples as current identifiers      | Older official pages can contain pre-2.8 names               |
| Extending core `--gf-*` namespace accidentally               | Add-on-defined properties are not Gravity Forms core API     |

Gravity Forms does document that an add-on can intentionally create its **own add-on-specific global custom properties**, including examples such as `--gf-myaddon-*`. Such a property remains an add-on extension, not a core Theme Framework identifier.

------

# 14. Orbital vs Theme Framework

| Concept         | Meaning                                                      |
| --------------- | ------------------------------------------------------------ |
| Theme Framework | Public architecture/CSS API used by framework-compatible themes |
| Foundation      | Functional/layout base required underneath custom visual styling |
| Orbital         | Default implementation and user-facing theme built on the Theme Framework |
| Theme Layers    | Integration mechanism that connects settings/styles/output to the framework |

Gravity Forms explicitly describes Orbital as the **default implementation** of the Theme Framework. Developers interact with the Theme Framework; users normally encounter Orbital as the form theme and its block style settings.

Therefore:

```text
Depend on:
documented Theme Framework CSS API
documented wrapper/utility/component contracts

Do not depend on:
private Orbital implementation decisions
undocumented generated selectors
undocumented --gform-theme-* tokens
```

Only themes using the Theme Framework can participate in the Theme Framework block-style customization mechanism documented by Gravity Forms.

------

# 15. Compatibility and Upgrade Notes

## 15.1 Gravity Forms 2.7

Theme Framework introduced in Gravity Forms **2.7**.

## 15.2 Gravity Forms 2.7.15 default-theme behavior

Official Form Themes documentation states that, beginning with **2.7.15**, new installations default globally to Orbital. Existing installations were not automatically switched; older installations may continue using the Gravity Forms 2.5 theme until changed.

## 15.3 Gravity Forms 2.8 CSS API breaking rename

Gravity Forms 2.8 refactored the Theme Framework CSS for performance and stylesheet size and shortened many CSS API identifiers. Gravity Forms labels this as a breaking Theme Framework change.

The official replacement lexicon includes:

| Old segment           | 2.8+ segment          |
| --------------------- | --------------------- |
| `gform-theme`         | `gf`                  |
| `background`          | `bg`                  |
| `button`              | `btn`                 |
| `control`             | `ctrl`                |
| `password`            | `pwd`                 |
| `page`                | `pg`                  |
| `file-upload`         | `file`                |
| `spacing`             | `space`               |
| `gf-font-family`      | `gf-font-family-base` |
| `progress`            | `prog`                |
| `description`         | `desc`                |
| `outside`             | `out`                 |
| `inside`              | `in`                  |
| `box-shadow`          | `shadow`              |
| `preview`             | `prev`                |
| `ctrl-file-prev-file` | `ctrl-file-prev`      |
| `drop-area`           | `zone`                |
| `border-radius`       | `radius`              |
| `strength`            | `str`                 |
| `indicator`           | `ind`                 |
| `product`             | `prod`                |
| `quantity`            | `quant`               |
| `required`            | `req`                 |
| `col-gap`             | `gap-x`               |
| `row-gap`             | `gap-y`               |
| `vertical`            | `y`                   |
| `horizontal`          | `x`                   |
| `inline-size`         | `width`               |
| `block-size`          | `height`              |
| `padding-inline`      | `padding-x`           |
| `padding-block`       | `padding-y`           |
| `margin-inline`       | `margin-x`            |
| `margin-block`        | `margin-y`            |
| `inset-block-start`   | `inset-y-start`       |
| `inset-block-end`     | `inset-y-end`         |
| `inset-inline-start`  | `inset-x-start`       |
| `inset-inline-end`    | `inset-x-end`         |
| `table-cell`          | `cell`                |
| `table-head-cell`     | `head-cell`           |

The associated NPM design-token/mixin packages moved to version 4.0.

For current code, use the current CSS API identifiers rather than mechanically deriving names from this migration table.

## 15.4 Gravity Forms 2.9

Gravity Forms 2.9 removed deprecated Theme Framework global CSS API properties. It also changed `.gform-theme__disable` and `.gform-theme__disable-framework` behavior so framework styling is disabled for field labels/descriptions as part of those exclusions.

This matters when testing old themes that relied on deprecated 2.7-era properties or older exclusion behavior.

## 15.5 Gravity Forms 3.0

Gravity Forms 3.0 is a major-version transition and the current official changelog identifies 3.0.0 as released July 28, 2026. The current submit-button documentation documents an important presentation-level markup change: form buttons use `<button>` instead of `<input>`, and spinner handling moved inside the button.

A custom Theme Framework layer targeting button element type/markup must therefore be tested against 3.0 markup rather than assuming 2.x button structure.

------

# 16. Unknown / Not Publicly Documented Areas

## 16.1 No public custom-theme registration mechanism

As of this snapshot:

```text
custom form theme registration:
NOT DOCUMENTED / explicitly stated as unavailable
```

Use the documented customization/enqueue mechanisms instead.

## 16.2 No guarantee for arbitrary Orbital internals

Selectors, variables, DOM details, and generated CSS observed in Orbital but not exposed by current official API documentation must be classified:

```text
IMPLEMENTATION DETAIL
```

or:

```text
NOT DOCUMENTED IN OFFICIAL REFERENCE
```

## 16.3 Color-system overview is incomplete

```
DOCUMENTATION AMBIGUOUS
```

The current CSS API Color page exposes the actual properties/defaults but contains unfinished explanatory text in its color-system overview. Therefore this reference preserves the published API relationships without inventing a more elaborate undocumented color-generation model.

## 16.4 Current Design Overview contains stale-looking control names

```
DOCUMENTATION AMBIGUOUS
```

The current Design Overview uses examples including:

```text
--gf-ctrl-border-size
--gf-ctrl-padding-block
--gf-ctrl-padding-inline
```

while the current CSS API documents:

```text
--gf-ctrl-border-width
--gf-ctrl-padding-y
--gf-ctrl-padding-x
```

For current implementation, this reference treats the dedicated CSS API identifiers as authoritative and does **not** promote the conflicting Design Overview names into the current property inventory.

## 16.5 Historical upgrade example vs current error property

```
DOCUMENTATION AMBIGUOUS
```

The Theme Framework Upgrade Guide contains a historical example using:

```text
--gf-ctrl-color-invalid
```

while the current Controls Base API documents:

```text
--gf-ctrl-color-error
```

Use the current dedicated CSS API identifier for new work.

## 16.6 Historical naming example in CSS API article

The architectural CSS API article includes older-form naming examples such as:

```text
--gf-control-bg-color-focus
```

Current 2.8+ API uses shortened segments such as:

```text
--gf-ctrl-...
```

Treat the article as architectural evidence, not as a current identifier list. The dedicated CSS API pages are the canonical identifier inventory.

## 16.7 Field Grid `size-auto` conflict

```
DOCUMENTATION AMBIGUOUS
```

The dedicated current Field Grid page states that:

```text
.gform-grid-col--size-auto
```

sizes a column to the width of its content. Some Core Concepts wording describes older/different responsive behavior. Use the dedicated Field Grid documentation for current implementation and revalidate if this behavior is important.

## 16.8 Gravity Forms 2.5 wrapper conflict

```
DOCUMENTATION AMBIGUOUS
```

Current Quick Start/Core Concepts identify the Gravity Forms 2.5 theme wrapper as:

```text
.gravity-theme
```

while the Theme Framework FAQ includes an example using:

```text
.gform_theme
```

Do not silently treat these as interchangeable. For Theme Framework work, prefer the current wrapper table and re-check official markup if targeting the 2.5 theme specifically.

## 16.9 Internal `--gform-theme-*` dependencies

The current public CSS API contains some defaults that reference:

```text
--gform-theme-color-uber-light-blue
--gform-theme-color-uber-light
--gform-theme-font-weight-semibold
```

These dependencies are visible in official documentation but are not published as entries in the public `--gf-*` API taxonomy.

Classification:

```text
IMPLEMENTATION DETAIL
```

Do not use them as project-level Theme Framework authority without independent current documentation.

## 16.10 Select hover shadow has no published default

```text
--gf-ctrl-select-dropdown-option-shadow-hover
```

is real and documented, but its current table has an empty Default cell.

Classification:

```text
DOCUMENTATION AMBIGUOUS
```

## 16.11 Simple-button focus icon self-reference

Current default:

```text
--gf-ctrl-btn-icon-color-focus-simple:
var(--gf-ctrl-btn-icon-color-focus-simple)
```

Classification:

```text
DOCUMENTATION AMBIGUOUS
```

Do not substitute another property without testing/current documentation.

------

# 17. Quick Lookup Index

| Need to change                      | Prefer checking first                                        | Higher-level relationship                   |
| ----------------------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| Primary accent                      | `--gf-color-primary`                                         | Top-level semantic color                    |
| Primary contrast                    | `--gf-color-primary-contrast`                                | Primary button/selected UI                  |
| Generic control background          | `--gf-ctrl-bg-color`                                         | defaults from `--gf-color-in-ctrl`          |
| Generic control text                | `--gf-ctrl-color`                                            | defaults from `--gf-color-in-ctrl-contrast` |
| Generic control border              | `--gf-ctrl-border-color`                                     | control-level token                         |
| Focus border                        | `--gf-ctrl-border-color-focus`                               | defaults from `--gf-color-primary`          |
| Focus outline                       | `--gf-ctrl-outline-color-focus`, `--gf-ctrl-outline-width-focus` | primary color RGB                           |
| Error border                        | `--gf-ctrl-border-color-error`                               | danger color                                |
| Error control color                 | `--gf-ctrl-color-error`                                      | base control color by default               |
| Control radius                      | `--gf-ctrl-radius`                                           | defaults from `--gf-radius`                 |
| Global radius intent                | `--gf-radius`                                                | feeds control/component radii               |
| Control height                      | `--gf-ctrl-size`                                             | defaults to medium size                     |
| Control horizontal padding          | `--gf-ctrl-padding-x`                                        | defaults from `--gf-padding-x`              |
| Control typography                  | `--gf-ctrl-font-*`                                           | primary typography tokens                   |
| Placeholder                         | `--gf-ctrl-placeholder-*`                                    | control typography/color                    |
| Primary button                      | `--gf-ctrl-btn-*-primary`                                    | primary semantic colors                     |
| Secondary button / Save & Continue  | `--gf-ctrl-btn-*-secondary`                                  | secondary semantic colors                   |
| Button size                         | `--gf-ctrl-btn-size`                                         | control sizes                               |
| Button radius                       | `--gf-ctrl-btn-radius`                                       | `--gf-radius`                               |
| Field label                         | `--gf-ctrl-label-*-primary`                                  | typography/color system                     |
| Secondary/choice label              | `--gf-ctrl-label-*-secondary`                                | secondary typography                        |
| Required marker                     | `--gf-ctrl-label-*-req`                                      | danger color                                |
| Description                         | `--gf-ctrl-desc-*`                                           | tertiary typography                         |
| Error description                   | `--gf-ctrl-desc-*-error`                                     | danger color                                |
| Checkbox/radio size                 | `--gf-ctrl-choice-size`                                      | choice control API                          |
| Checkbox check                      | `--gf-ctrl-choice-checkbox-check-size`                       | choice size variants                        |
| Radio indicator                     | `--gf-ctrl-choice-radio-size`                                | choice size variants                        |
| Select arrow                        | `--gf-ctrl-select-icon*`                                     | Icons API                                   |
| Enhanced select dropdown            | `--gf-ctrl-select-dropdown-*`                                | control/select API                          |
| Selected enhanced multi-select item | `--gf-ctrl-multiselect-selected-item-*`                      | inside-control primary                      |
| Textarea height                     | `--gf-ctrl-textarea-height`                                  | textarea component                          |
| File drop area                      | `--gf-ctrl-file-zone-*`                                      | File API                                    |
| Upload progress                     | `--gf-ctrl-file-prog-*`                                      | primary/success colors                      |
| File preview                        | `--gf-ctrl-file-prev-*`                                      | file/label/description API                  |
| Date picker                         | `--gf-ctrl-date-picker-*`                                    | control/select/color APIs                   |
| Date field icon                     | `--gf-field-date-ctrl-*`                                     | field-level Date API                        |
| Image choices                       | `--gf-field-img-choice-*`                                    | Field Choice API                            |
| Password strength                   | `--gf-field-pwd-str-*`                                       | Password field API                          |
| Page progress                       | `--gf-field-pg-prog-*`                                       | Page field API                              |
| Page steps                          | `--gf-field-pg-steps-*`                                      | Page field API                              |
| Product quantity width              | `--gf-field-prod-quant-width`                                | Product field API                           |
| Form horizontal gap                 | `--gf-form-gap-x`                                            | Form layout                                 |
| Form vertical gap                   | `--gf-form-gap-y`                                            | Form layout                                 |
| Field gap                           | `--gf-field-gap-x`, `--gf-field-gap-y`                       | Foundation layout                           |
| Label width                         | `--gf-label-width`                                           | Applicable label layouts                    |
| Validation box                      | `--gf-form-validation-*`                                     | danger + control tokens                     |
| Validation heading                  | `--gf-form-validation-heading-*`                             | validation base                             |
| Validation summary list             | `--gf-form-validation-summary-*`                             | validation base                             |
| Spinner                             | `--gf-form-spinner-fg-color`, `--gf-form-spinner-bg-color`   | primary color                               |
| Complex field columns               | `.gform-grid-row`, `.gform-grid-col`                         | Foundation utility                          |
| Framework-only scope                | `.gform-theme--framework`                                    | theme wrapper                               |
| Orbital-specific scope              | `.gform-theme--orbital`                                      | Orbital wrapper                             |
| One form                            | `#gform_wrapper_{form_id}` combined with framework scope     | form scope                                  |
| One field                           | `#field_{form_id}_{field_id}`                                | field scope                                  |

If a desired change is absent from this table, search the relevant API section above before resorting to direct CSS.

------

# 18. Official Source Index

Only official Gravity Forms-owned documentation was used as normative evidence.

## Architecture, authoring, scoping, compatibility

| ID   | Source                                      | URL / navigation                                             | Used for                                                 |
| ---- | ------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------- |
| S01  | Gravity Forms Theme Framework Documentation | [Theme Framework CSS API root](https://docs.css.gravity.com/?utm_source=chatgpt.com) | Current CSS API taxonomy                                 |
| S02  | Quick Start — CSS API                       | [CSS API Quick Start](https://docs.css.gravity.com/docs.quick-start.html?utm_source=chatgpt.com) | CSS API usage orientation                                |
| A01  | Theme Framework Introduction                | [Theme Framework Introduction](https://docs.gravityforms.com/theme-framework-introduction/?utm_source=chatgpt.com) | Framework purpose/history                                |
| A02  | Quick Start Guide                           | [Theme Framework Quick Start Guide](https://docs.gravityforms.com/quick-start-guide/?utm_source=chatgpt.com) | Architecture, Orbital, wrappers, block settings          |
| A03  | Core Concepts                               | [Theme Framework Core Concepts](https://docs.gravityforms.com/theme-framework/?utm_source=chatgpt.com) | Reset/Foundation/Framework, scoping, utilities           |
| A04  | CSS API                                     | [Theme Framework CSS API architecture](https://docs.gravityforms.com/css-api/?utm_source=chatgpt.com) | Global/local API model and naming                        |
| A05  | Theme Layers                                | [Theme Layers](https://docs.gravityforms.com/theme-layers/?utm_source=chatgpt.com) | Theme Layers role                                        |
| A06  | Theme Framework Frequently Asked Questions  | [Theme Framework FAQ](https://docs.gravityforms.com/theme-framework-faq/?utm_source=chatgpt.com) | Custom authoring, wrappers, add-ons, current limitations |
| A07  | Theme Framework Upgrade Guide               | [Theme Framework Upgrade Guide](https://docs.gravityforms.com/theme-framework-upgrade-guide/?utm_source=chatgpt.com) | 2.8 breaking rename/migration                            |
| A08  | CSS Visual Guide and Design Overview        | [Design Overview](https://docs.gravityforms.com/design-overview/?utm_source=chatgpt.com) | Wrapper structure, scopes, design guidance               |
| A09  | Form Themes and Style Settings              | [Form Themes and Style Settings](https://docs.gravityforms.com/form-themes-and-style-settings/?utm_source=chatgpt.com) | Orbital/default-theme behavior                           |
| A10  | Submit Button CSS Selectors                 | [Submit Button CSS Selectors](https://docs.gravityforms.com/submit-button-css-selectors/?utm_source=chatgpt.com) | Button markup and 3.0 changes                            |
| A11  | Save and Continue Link CSS Selectors        | [Save and Continue CSS Selectors](https://docs.gravityforms.com/save-and-continue-link-css/) | Save/Continue selectors and secondary button             |
| A12  | Form Confirmation CSS Selectors             | [Form Confirmation CSS Selectors](https://docs.gravityforms.com/form-confirmation/) | Confirmation selectors                                   |
| A13  | Gravity Forms 2.9 Key Features              | [Gravity Forms 2.9 Key Features](https://docs.gravityforms.com/gravity-forms-2-9-key-features/?utm_source=chatgpt.com) | Deprecated property removal/exclusion changes            |
| A14  | Gravity Forms Changelog                     | [Gravity Forms Changelog](https://docs.gravityforms.com/gravityforms-change-log/?utm_source=chatgpt.com) | Current release/version context                          |

## Base CSS API

| ID   | Source                                  | URL / navigation                                             |
| ---- | --------------------------------------- | ------------------------------------------------------------ |
| B01  | Global CSS API: Borders                 | [Borders API](https://docs.css.gravity.com/framework.api._borders.html) |
| B02  | Global CSS API: Colors                  | [Colors API](https://docs.css.gravity.com/framework.api._colors.html?utm_source=chatgpt.com) |
| B03  | Global CSS API: Field Layout & Spacing  | [Field Layout & Spacing API](https://docs.css.gravity.com/framework.api._layout.html?utm_source=chatgpt.com) |
| B04  | Global CSS API: Form Layout & Spacing   | [Form Layout & Spacing API](https://docs.css.gravity.com/foundation.api._layout.html) |
| B05  | Global CSS API: Icons                   | [Icons API](https://docs.css.gravity.com/framework.api._icons.html?utm_source=chatgpt.com) |
| B06  | Global CSS API: Transitions & Animation | [Transitions API](https://docs.css.gravity.com/framework.api._transitions.html) |
| B07  | Global CSS API: Typography              | [Typography API](https://docs.css.gravity.com/framework.api._typography.html?utm_source=chatgpt.com) |

## Controls CSS API

| ID   | Source                 | URL / navigation                                             |
| ---- | ---------------------- | ------------------------------------------------------------ |
| C01  | Controls — Base        | [Control Base API](https://docs.css.gravity.com/framework.controls.default._api-global.html) |
| C02  | Controls — Button      | [Button API](https://docs.css.gravity.com/framework.controls.button._api-global.html) |
| C03  | Controls — Choice      | [Choice Control API](https://docs.css.gravity.com/framework.controls.choice._api-global.html) |
| C04  | Controls — Date        | [Date Control API](https://docs.css.gravity.com/framework.controls.date._api-global.html?utm_source=chatgpt.com) |
| C05  | Controls — Description | [Description API](https://docs.css.gravity.com/framework.controls.description._api-global.html) |
| C06  | Controls — File        | [File Control API](https://docs.css.gravity.com/framework.controls.file._api-global.html?utm_source=chatgpt.com) |
| C07  | Controls — Label       | [Label API](https://docs.css.gravity.com/framework.controls.label._api-global.html) |
| C08  | Controls — Number      | [Number API](https://docs.css.gravity.com/framework.controls.number._api-global.html) |
| C09  | Controls — Readonly    | [Readonly API](https://docs.css.gravity.com/framework.controls.readonly._api-global.html) |
| C10  | Controls — Select      | [Select API](https://docs.css.gravity.com/framework.controls.select._api-global.html?utm_source=chatgpt.com) |
| C11  | Controls — Textarea    | [Textarea API](https://docs.css.gravity.com/framework.controls.textarea._api-global.html) |

## Fields CSS API

| ID   | Source            | URL / navigation                                             |
| ---- | ----------------- | ------------------------------------------------------------ |
| D01  | Fields — Choice   | [Choice Field API](https://docs.css.gravity.com/framework.fields.choice._api-global.html?utm_source=chatgpt.com) |
| D02  | Fields — Date     | [Date Field API](https://docs.css.gravity.com/framework.fields.date._api-global.html?utm_source=chatgpt.com) |
| D03  | Fields — List     | [List Field API](https://docs.css.gravity.com/framework.fields.list._api-global.html) |
| D04  | Fields — Page     | [Page Field API](https://docs.css.gravity.com/framework.fields.page._api-global.html) |
| D05  | Fields — Password | [Password Field API](https://docs.css.gravity.com/framework.fields.password._api-global.html) |
| D06  | Fields — Product  | [Product Field API](https://docs.css.gravity.com/framework.fields.product._api-global.html) |
| D07  | Fields — Repeater | [Repeater Field API](https://docs.css.gravity.com/framework.fields.repeater._api-global.html) |
| D08  | Fields — Section  | [Section Field API](https://docs.css.gravity.com/framework.fields.section._api-global.html) |

## Form CSS API

| ID   | Source            | URL / navigation                                             |
| ---- | ----------------- | ------------------------------------------------------------ |
| F01  | Form — Spinner    | [Spinner API](https://docs.css.gravity.com/framework.form.spinner._api-global.html) |
| F02  | Form — Validation | [Validation API](https://docs.css.gravity.com/framework.form.validation._api-global.html) |

## Utility CSS API

| ID   | Source                           | URL / navigation                                             |
| ---- | -------------------------------- | ------------------------------------------------------------ |
| U01  | Layout: Complex Field Grid       | [Field Grid utilities](https://docs.css.gravity.com/foundation.layout._grid.html?utm_source=chatgpt.com) |
| U02  | Base: Foundation Utility Classes | [Foundation utilities](https://docs.css.gravity.com/foundation.base._utils.html) |

------

## Documentation Coverage Status

The current Theme Framework navigation and every major branch exposed by the current CSS API sidebar were inspected for this snapshot:

```text
Base
  Borders
  Colors
  Field Layout & Spacing
  Form Layout & Spacing
  Icons
  Transitions & Animation
  Typography

Controls
  Base
  Button
  Choice
  Date
  Description
  File
  Label
  Number
  Readonly
  Select
  Textarea

Fields
  Choice
  Date
  List
  Page
  Password
  Product
  Repeater
  Section

Form
  Spinner
  Validation

Utility Classes
  Field Grid
  Foundation
```

Architecture, Theme Layers, scoping, authoring FAQ, design guidance, Theme Framework upgrade guidance, relevant 2.9 compatibility information, and current 3.0 submit-button behavior were also inspected.

No major current CSS API branch visible in the official Theme Framework documentation navigation was intentionally omitted.

Known incomplete or conflicting official material is preserved in **§16 Unknown / Not Publicly Documented Areas** rather than silently reconciled.

Large encoded SVG icon defaults and a small number of very long decorative shadow/gradient literals are normalized by recording the exact property identifier, semantic role, and official source rather than duplicating opaque encoded payloads. When the literal value itself matters to implementation, retrieve it from the cited current official CSS API page.

------

## Final Agent Safety Check

Before emitting or approving Gravity Forms Theme Framework code, verify:

```text
[ ] Every --gf-* identifier exists in this reference or current official docs.
[ ] No --gf-* identifier was invented from naming patterns.
[ ] Historical 2.7 property names were not mistaken for current 2.8+ names.
[ ] Orbital/internal --gform-theme-* variables were not promoted to public API.
[ ] Wrapper and field selectors are documented for the intended theme/runtime.
[ ] Override scope matches global/form/block/field intent.
[ ] Higher-level tokens were considered before duplicating component overrides.
[ ] Focus/error/disabled states were considered separately where APIs exist.
[ ] Foundation was not removed merely to obtain a custom visual design.
[ ] Gravity Forms 3.0 button markup assumptions were respected where relevant.
[ ] Any documentation conflict is represented as uncertainty, not guessed away.
[ ] If current official docs differ from this snapshot, current docs win.
```
