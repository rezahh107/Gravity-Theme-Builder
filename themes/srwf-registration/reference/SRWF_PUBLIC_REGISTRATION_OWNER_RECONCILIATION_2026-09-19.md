# SRWF Public Registration — Current Owner Reconciliation — 2026-09-19

Status: **CURRENT_OWNER_PROJECT_AUTHORITY / RUNTIME_VALIDATION_REQUIRED**

Authority handle: `OWNER:SRWF-2026-09-19`

This document records the current Owner-supplied SRWF Registration destination for Gravity Theme Builder. It is the current project authority for the decisions enumerated here and supersedes contradictory or unresolved states in the exact historical `SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` mirror.

## Provenance and preservation rule

The authority input was supplied directly by the Owner for this execution on 2026-09-19. The Executor does **not** have an exact immutable upstream Google Drive revision/export identity for this newer authority input.

Therefore:

- no Drive revision ID, modified timestamp, export hash, or immutable upstream blob is asserted for this document;
- the admitted v1.0.1 Drive-backed mirror remains byte-preserved and registered with its existing immutable provenance;
- where this document explicitly resolves or supersedes a v1.0.1 state, this document is current;
- v1.0.1 remains historical evidence of the earlier decision state, not current destination authority on those points;
- all v1.0.1 rules not contradicted here remain inherited unless another current Owner decision says otherwise.

Recording a current Owner decision is not runtime proof. All runtime-sensitive claims remain subject to supported WordPress / Gravity Forms / add-on validation.

## Authority/evidence decision principle

For design and implementation decisions:

1. applicable mandatory standards and safety/accessibility requirements;
2. current official platform/vendor documentation for factual/support questions;
3. strong professional consensus and credible empirical/research evidence;
4. established best practice;
5. local preference only where stronger authority does not settle the question.

A lone expert opinion or isolated article is not sufficient authority for a material decision. Runtime facts still require proof against the supported real environment.

## Form structure and durable identity

- GTB owns presentation, not business/content structure.
- Field order, Section Break order, wording, inventory, and Owner-configured Gravity Forms layout may change without theme-code changes.
- Presentation identity must not depend on DOM position, `nth-child`, label text, artifact order, or numeric Form/Field IDs.
- Explicit semantic roles/configuration are the durable binding mechanism.
- Numeric IDs may exist only as internal per-form host-object references inside configuration/evidence.

## Desktop layout ownership

`desktop_short_field_pairings: HOST_OWNED / OWNER_CONFIGURABLE`

GTB must style the authentic Gravity Forms layout. GTB does not define a canonical short-field pairing list and must not infer one from labels, IDs, screenshots, order, or DOM position.

## Responsive destination

- hard acceptance width: `320 CSS px`;
- canonical mobile horizontal padding: `16px`;
- production desktop breakpoint: `960 CSS px`;
- the breakpoint is a theme presentation threshold, not a device-name preset.

The `exact_production_breakpoint: NOT_PROVEN` state in v1.0.1 is superseded by the Owner-authorized `960 CSS px` destination. Runtime/browser acceptance at that threshold remains required.

## Desktop card destination

- page background: `#F6F8FB`;
- card surface: `#FFFFFF`;
- content max width: `840px`;
- card internal inline padding: `32px` per side;
- resulting desktop outer max width: `904px`;
- outer radius: `16px`;
- box shadow: `none`.

The prior `desktop_shadow_exact_value: NOT_PROVEN` state is superseded. Page-shell ownership and actual cascade/consumer behavior remain runtime-sensitive implementation facts.

## Primary Submit

- full available form width on desktop and mobile;
- desktop content remains bounded by the `840px` content cap;
- minimum height: `56px`;
- Gravity Forms owns submit behavior and lifecycle.

## Typography destination

Target family: `Vazirmatn`.

| Role | Size | Weight | Line height |
|---|---:|---:|---:|
| Form title — mobile | `24px` | `700` | `1.5` |
| Form title — desktop | `26px` | `700` | `1.5` |
| Section heading | `18px` | `700` | inherited/current unless separately resolved |
| Field label | `15px` | `600` | inherited/current unless separately resolved |
| Control value | `16px` | `400` | inherited/current unless separately resolved |
| Helper | `14px` | `400` | `1.5` |
| Field error | `14px` | `600` | `1.5` |
| Primary action | `16px` | `700` | inherited/current unless separately resolved |

The prior non-normative/unresolved form-title, helper, field-error, and desktop-title values are superseded by these exact Owner-authorized values.

## Spacing destination

- field vertical rhythm: `24px`;
- major section rhythm: `32px`.

The prior `NON_NORMATIVE_REFERENCE` resolution states for these rhythms are superseded.

## Focus destination

Use `:focus-visible` where appropriate.

- outline: `2px solid #1D4ED8`;
- outline offset: `2px`;
- no glow;
- no layout shift;
- authentic keyboard focus must never be suppressed.

The prior unresolved focus-ring geometry/alpha state is superseded by this exact destination. Runtime focus ownership/consumer behavior and accessibility acceptance still require validation.

## Helper, validation, and sub-label placement

The earlier Owner choice to place helper and validation messages below the input is superseded.

Follow Gravity Forms' accessible recommended placement/configuration for descriptions, validation messages, and sub-labels **above the input where supported**.

- Gravity Forms remains authoritative for validation lifecycle, ARIA, focus, reading order, and value persistence.
- GTB must not fake/recreate validation semantics or reorder host behavior with custom JavaScript.
- Placement is a host configuration responsibility where Gravity Forms exposes the setting.

## Required indication

- use native Gravity Forms required semantics/indicator;
- preferred visible indicator: native asterisk-only;
- provide a short form-level explanation of what `*` means;
- do not create required semantics with CSS-generated content.

## Binary semantic choice roles

This applies only to explicitly mapped binary roles, not every Radio field.

- two equal-width cards;
- horizontal row where space is valid;
- gap: `12px`;
- minimum card/control target height: `52px`;
- selected state must use more than color alone;
- canonical primary treatment includes subtle tint `#EDF1FC`;
- preserve native Gravity Forms radio input, labels, checked state, keyboard, and validation behavior.

This keeps the semantic-role requirement from v1.0.1 §27 while superseding any earlier exact size value that conflicts with the `52px` minimum here.

## Section icon tiles

Only explicitly mapped semantic section roles receive an icon tile.

- tile: `40px × 40px`;
- radius: `10px`;
- icon: `20px`;
- subtle primary tint: `#EDF1FC`;
- no inference from section label or DOM position.

The admitted artifact remains the geometry/mapping reference for the already-approved icons; these tile dimensions are the current Owner destination.

## Upload initial visual family

- minimum height: `96px`;
- padding: `16px`;
- radius: `12px`;
- dashed border: `#8690A1`;
- visible icon/instruction/helper hierarchy;
- drag-and-drop must not be the only usable path;
- Gravity Forms / GP File Upload Pro own actual upload behavior.

## Student Photo

GTB does not define crop ratio or crop dimensions for v1. Those remain host/GPFUP configuration-owned. GTB styles only authentic upload/preview/replace/re-crop/delete states actually exposed by GPFUP.

`gpfup_crop_ratio_dimensions` therefore remains runtime/configuration-owned and not a GTB visual constant.

## GP Advanced Select / Tom Select

GTB owns appearance only. Search/filter/selection/keyboard/mobile/screen-reader/Populate Anything behavior remains host/add-on-owned.

## Accessibility acceptance

Acceptance requires, as applicable:

- `320px` reflow without ordinary horizontal scrolling;
- `200%` text resize resilience;
- text-spacing resilience;
- normal meaningful text contrast `>= 4.5:1`;
- UI/focus/non-text cues `>= 3:1`;
- visible keyboard focus;
- adequate target-size outcome or a valid exception;
- native semantics/ARIA/keyboard behavior preserved.

These are acceptance requirements, not claims that current production CSS has already passed them.

## Batch implementation boundary

This authority reconciliation does **not** authorize silently claiming the current production stylesheet already implements the newly resolved values.

For the reconciliation/foundation batch that admitted this document:

- current production presentation and the merged PR #15 binary-choice repair are preserved;
- per-form GTB configuration may be recovered because it is configuration foundation rather than a broad visual rewrite;
- the remaining visual destination above is `OWNER_AUTHORIZED / NEXT_VISUAL_IMPLEMENTATION_AND_RUNTIME_QUALIFICATION_REQUIRED` unless existing evidence already proves a narrower item;
- final SRWF production qualification remains open.
