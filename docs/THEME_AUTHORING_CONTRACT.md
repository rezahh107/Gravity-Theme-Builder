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

`--gf-form-gap-y exists`

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

When the same configured Gravity Forms form can be reused by the host in more than one rendering surface, the activation boundary must distinguish **form identity** from **rendering-context ownership**. A stored opt-in class may identify which form is intended for a theme, but it does not by itself authorize that theme on every host surface that reuses the form.

In such cases, theme admission must require both the explicit form opt-in and a permitted rendering context, and must fail closed on host surfaces outside the theme's presentation domain. The context boundary must be enforced by the theme itself and must not depend on another presentation plugin being installed or exposing a class/state. Prefer an authentic supported host seam; if none exists, use the narrowest version-bounded alternative supported by runtime evidence. Do not substitute URL/page-ID heuristics, DOM-text inference, unrelated-plugin detection, or stored-form mutation for a real context boundary.

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

## 20. Per-form configuration and semantic role management

Where a theme requires explicit form activation or semantic presentation-role bindings, the preferred product experience is a native per-form Gravity Forms settings surface managed by GTB rather than requiring users to hand-edit GTB-owned CSS class tokens.

Use supported Gravity Forms per-form settings mechanisms for the supported runtime. Current official Gravity Forms documentation exposes `gform_form_settings_menu` plus `gform_form_settings_page_{VIEW}` for custom Form Settings views, and the current implementation must verify the exact supported host seam/version before coding.

The settings surface may store or manage real form/field/section identifiers as configuration references, because those identifiers point to actual host objects in that form. They must not become the durable CSS/presentation identity. Theme CSS and presentation logic should bind through semantic GTB-owned role tokens/classes or another equally explicit semantic contract.

The configuration layer must:

- preserve unrelated host Custom CSS Class tokens when adding/removing GTB-owned tokens;
- distinguish form activation from field/section semantic roles;
- expose truthful readiness such as READY, NEEDS_SETUP, AMBIGUOUS, DISABLED, or equivalent bounded states;
- provide an explicit apply/save action for mutations and a separate read-only verification action where useful;
- avoid silent mutation on ordinary admin/frontend render;
- avoid label-text, DOM position, `nth-child`, generic field-type, or unrelated-plugin heuristics as semantic identity;
- fail closed when a required role cannot be mapped safely;
- retain theme/runtime context-isolation rules independently of configuration UI state;
- keep admin assets scoped to the GTB settings surface;
- remain a configuration/diagnostic surface, not a visual page builder or arbitrary design editor.

A theme may provide a one-click recommended configuration for a known first-party/approved target when the mapping is authoritative and verifiable. Such an operation must be explicit, capability/nonce protected, repeatable without duplicate tokens, and must report exactly what it changed or could not establish.

When the recommended configuration includes host-owned Form Object presentation/layout properties, use a read-only readiness view plus a separate explicit Apply action. At mutation time, re-read the current full host object, compute the bounded authorized diff, perform no write when already matching, change only the admitted properties through the supported host API, re-read after persistence, and verify the resulting state. Field-level overrides or other conflicts that exceed the admitted mutation boundary must be surfaced truthfully rather than silently rewritten. Preserve unrelated form state and host semantics.

A top-level GTB admin menu is not the default for a single-theme/single-form operational case. Prefer the native per-form settings location. A broader overview is justified only after multiple active forms/themes create a recurring cross-form management responsibility.

For WordPress admin UX implementation only, project-specific non-authoritative references may be admitted. For the current GTB work, `rezahh107/Personal-Preference-Decision-Model` → `knowledge/current/domains/wordpress-plugin-ui-ux/` at commit `94ed79c9f8fe57357d2834ded5633d4767e4abe7` is an approved implementation reference. It does not override this contract, the Project Charter, current Gravity Forms documentation/runtime evidence, or any theme visual authority.

## 21. Form structure and ordering independence

GTB owns presentation, not the business/content structure of a Gravity Forms form. Field order, Section Break order, section wording, and the presence or absence of ordinary business fields remain under Owner/Gravity Forms configuration control unless a separate product requirement explicitly says otherwise.

A visual reference may demonstrate component appearance and admitted semantic-role presentation, but it must not be interpreted as freezing the order of sections/fields or requiring a specific business-field inventory. Reordering sections (for example moving Contact before Identity), adding/removing ordinary fields, or renaming section labels must not require theme code changes merely to preserve the theme's visual language.

Theme behavior must therefore bind to stable host semantics, supported field types, and explicit GTB semantic roles/configuration—not DOM position, `nth-child`, label text, or the sequence shown in an approved artifact. Where a component genuinely needs a role-specific presentation (for example binary choice, report-card upload, or an explicitly mapped section icon), the role mapping identifies presentation responsibility while the Owner remains free to place that role anywhere in the form.

Pixel/visual fidelity for GTB means fidelity of the presentation system and admitted component states within the actual configured form, not forced duplication of the reference artifact's business-field ordering, section order, or wording.

## 22. Standards-driven resolution rule

For theme-authoring decisions that are not product/business choices, do not ask the Owner to adjudicate routine details when recognized standards, current official Gravity Forms/WordPress/vendor documentation, converging professional guidance, or strong empirical evidence already provides a clear answer.

Operational order:

1. satisfy applicable mandatory standards and accessibility requirements;
2. follow current official host/platform documentation and supported mechanisms;
3. prefer conclusions supported by multiple reputable professional sources and, where relevant, empirical/academic evidence;
4. use established best practices where higher-authority sources leave implementation discretion;
5. use local preference only for the remaining genuinely open design choice.

Do not elevate a single expert opinion or isolated article into project authority by itself. Prefer convergence and traceable sources.

This rule may resolve micro-decisions such as spacing, focus treatment, responsive mechanics, error/helper presentation, control affordances, and similar implementation details without repeated Owner approval. It does not authorize changing business workflow, data semantics, product scope, or a materially different visual identity when more than one standards-compliant option remains. Runtime-dependent claims still require runtime evidence.

If an older theme-specific rule conflicts with a stronger applicable standard or current official host guidance, record the conflict and apply the smallest standards-compliant correction while preserving the approved product intent.

## 23. Theme-level radio presentation authority

A theme-specific visual authority may explicitly define presentation for an entire authentic Gravity Forms field type inside that theme's admitted activation boundary. When it does, that explicit authority is not a forbidden generic-field heuristic; it is the theme contract.

For SRWF Registration, the Owner has locked the following rule:

- every authentic Gravity Forms radio group rendered inside the admitted SRWF Registration theme must use the SRWF card-choice visual language;
- card presentation is mandatory, while layout/orientation is responsive and context-sensitive: choices may be horizontal, multi-column/wrapping, or vertical according to available space, option count/content, and the authentic host layout;
- binary/short choices should use equal track allocation when the available layout supports it; multi-option groups may use a responsive grid/wrap or vertical stack rather than forcing one row;
- each visible card must occupy its intended layout track/cell rather than shrink to label-content width;
- narrow layouts must reflow without horizontal scrolling or compressed/unreadable cards;
- the whole visible card label should remain operable while Gravity Forms retains the native radio input, checked state, keyboard interaction, validation, conditional logic, labels/legend, and accessibility semantics;
- selected state must include a non-color cue in addition to canonical color treatment;
- this rule must be scoped to admitted SRWF Registration radio fields and must not leak to unrelated forms, Gravity Flow Entry Detail, other themes, or checkbox/other choice types unless separately authorized.

This SRWF Owner lock supersedes the earlier SRWF interpretation that card presentation applied only to fields carrying `srwf-role-binary-choice`. The explicit binary role may remain useful for binary-specific geometry or diagnostics, but it is no longer the gate for whether an SRWF radio group is presented as cards.
