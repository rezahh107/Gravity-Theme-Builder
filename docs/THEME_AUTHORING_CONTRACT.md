# Gravity Theme Builder — Theme Authoring Contract

Status: **Repository authoring contract**

This document defines how an approved visual design becomes a theme implementation in this repository.

## 1. Inputs required for a theme

A theme implementation should have, as applicable:

- an approved visual/UX reference or explicit visual contract;
- the target Gravity Forms version/runtime;
- known required add-ons/custom field types;
- required responsive states;
- required interaction states;
- required accessibility and content-resilience expectations.

Missing inputs must be marked explicitly; they must not be silently invented.

## 2. Visual authority

The approved reference defines the desired visual outcome.

Do not reinterpret or improve the design unless the owner explicitly reopens design decisions.

If the reference contains demo-only behavior, identify that behavior before implementation and keep it out of production unless separately authorized.

## 3. Requirement classification

Every material visual requirement should be classified before implementation:

- typography;
- color;
- spacing/rhythm;
- control sizing;
- radius/border/shadow/optical detail;
- layout;
- responsive behavior;
- icon/media sizing;
- validation/error/success presentation;
- focus/interaction state;
- host/add-on integration.

This classification helps choose the correct implementation mechanism rather than applying blanket conversions.

## 4. Implementation priority

Use this order:

### Level A — official Theme Framework / CSS API

Use documented `--gf-*` or other official Theme Framework mechanisms when they can express the approved requirement at the correct scope.

### Level B — official host mechanism

Use documented Gravity Forms hooks/classes/settings when CSS API alone is insufficient but an official supported mechanism exists.

### Level C — scoped direct CSS

Use direct CSS only for a requirement that cannot be expressed cleanly through A or B.

Direct CSS must:

- stay under the target theme activation scope;
- use stable host selectors where possible;
- avoid changing host behavior;
- avoid selector escalation beyond what is proven necessary.

### Level D — bounded adapter

Use an adapter for add-on/custom-field/runtime behavior only after inspecting the real consumer and proving that A–C are insufficient.

## 5. API availability is not design authority

Example:

```text
--gf-form-gap-y exists
```

means Gravity Forms exposes a supported mechanism for field gap.

It does **not** mean a specific gap value is approved.

The value must come from the theme's visual authority.

## 6. Semantic mapping record

Important mappings should be documented in a theme-local implementation map.

Recommended format:

| Visual requirement | Authority/value | Host mechanism | Evidence | Notes |
|---|---|---|---|---|
| Field vertical rhythm | approved design | `--gf-form-gap-y` | DOCUMENTED + RUNTIME_PROVEN | example |

The table should describe responsibilities, not merely list CSS declarations.

## 7. Scope and activation

A theme must have an explicit activation boundary.

Theme styling must not leak into unrelated Gravity Forms instances or the surrounding WordPress site.

Avoid by default:

- global `html` styling;
- global `body` styling;
- unscoped `.gform_wrapper` rules;
- form-ID-specific selectors as architectural identity;
- broad selectors that accidentally style third-party forms.

## 8. `!important` policy

`!important` is not categorically forbidden, because real host frameworks may create cascade conditions that require it.

However, every use must satisfy all of these:

- the exact host cascade conflict is inspected;
- a lower-specificity/API solution is insufficient;
- the declaration remains theme-scoped;
- the reason is documented;
- runtime evidence verifies the intended consumer.

## 9. Control sizing

Prefer host-supported control tokens and minimum-size semantics over brittle direct fixed heights.

Do not add `max-height` merely to preserve a screenshot if it risks clipping text or enlarged content.

If the runtime consumes a control token at a nested scope rather than the wrapper, project the same canonical theme value to the proven consumer rather than creating a second design authority.

## 10. Typography

Typography belongs to the theme but must not assume ownership of the entire document root.

Prefer theme-scoped font family, size, weight, and line-height mappings through the official CSS API where available.

Do not set a global root font size for a public form unless the embedding contract explicitly grants that ownership.

## 11. Spacing and rhythm

Distinguish:

- field rhythm;
- internal control padding;
- section rhythm;
- page/shell padding;
- component-local spacing.

Do not force all spacing through one generic token if the visual roles are different.

Use official spacing variables such as form/field gap properties when appropriate, but keep semantic design decisions separate from host property names.

## 12. Optical values

Borders, radii, hairlines, focus geometry, and similar optical details may legitimately use pixel units when that matches their role.

Do not mechanically convert every pixel value to `rem`.

## 13. Responsive behavior

Responsive rules must represent an actual design/runtime responsibility.

Prefer intrinsic layout first. Use container queries for component-owned constraints only when the real host container supports and benefits from them. Use media queries for viewport-owned behavior.

Do not copy breakpoints from a static reference without determining whether they were demo scaffolding or production intent.

## 14. Add-ons and custom fields

Do not assume Gravity Forms core Theme Framework properties are consumed identically by add-ons or custom field types.

For each non-core surface where styling matters:

1. inspect the actual runtime markup and computed properties;
2. identify whether official properties are consumed;
3. prefer those properties when available;
4. create the minimum adapter only when needed;
5. preserve add-on behavior and accessibility.

## 15. Validation states

Theme code may style validation states, but Gravity Forms remains the owner of validation semantics, message generation, ARIA, lifecycle, and persistence.

Do not move or recreate validation behavior in JavaScript merely to match a static mockup when CSS presentation can satisfy the requirement.

## 16. Focus behavior

Preserve native keyboard/focus semantics.

A theme may define visual focus intent through supported host mechanisms. It must not assume unsupported focus geometry APIs exist, and it must not suppress a visible focus indicator.

Runtime transitions should be tested at their settled state when the host intentionally animates focus presentation.

## 17. Required evidence before production qualification

As applicable, verify:

- supported Gravity Forms version;
- real form runtime, not only isolated markup;
- desktop and required mobile widths;
- RTL;
- long Persian labels/values;
- validation/error states;
- keyboard focus;
- text enlargement;
- narrow reflow;
- required add-ons/custom fields;
- no submission/validation regression;
- isolation from unrelated forms/site UI.

## 18. Reuse promotion

Theme-local code is the default.

Promote a mapping/helper/adapter into shared `src/` only when reuse is demonstrated and the shared abstraction preserves the real differences between themes.

## 19. Completion states

Use explicit states for material mappings:

- `IMPLEMENTED_STATIC_ONLY`
- `DOCUMENTED`
- `RUNTIME_PROVEN`
- `DEFERRED`
- `NOT_PROVEN`
- `BLOCKED`

A theme is not production-ready while decision-critical mappings remain `NOT_PROVEN` or `BLOCKED`.
