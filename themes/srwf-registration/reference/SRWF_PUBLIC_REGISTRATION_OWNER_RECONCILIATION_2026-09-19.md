# SRWF Public Registration — Current Owner Reconciliation — 2026-09-19

Status: **CURRENT_OWNER_PROJECT_AUTHORITY / VISUAL_REPAIR_IMPLEMENTED_STATICALLY / RUNTIME_VALIDATION_REQUIRED**

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
- Presentation identity must not depend on DOM position, `nth-child`, label text, option text, artifact order, or numeric Form/Field IDs.
- Explicit semantic roles/configuration remain the durable binding mechanism where a semantic specialization is actually required.
- Authentic Gravity Forms field type/configuration may itself be a presentation seam when the Owner rule intentionally applies to the whole host field family.
- Numeric IDs may exist only as internal per-form host-object references inside configuration/evidence; they are not presentation identity.

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

- page background: `#F6F8FB` where an authenticated GTB ownership seam exists;
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
- typography: `16px / 700 / 1.5`;
- Gravity Forms owns submit behavior and lifecycle.

## Typography destination

Target family stack: `Vazirmatn, Vazir, Tahoma, Arial, sans-serif`.

| Role | Size | Weight | Line height |
|---|---:|---:|---:|
| Form title — mobile | `24px` | `700` | `1.5` |
| Form title — desktop | `26px` | `700` | `1.5` |
| Section heading | `18px` | `700` | `1.5` |
| Field label | `15px` | `600` | `1.5` |
| Control value | `16px` | `400` | `1.5` |
| Helper | `14px` | `400` | `1.5` |
| Field error | `14px` | `600` | `1.5` |
| Primary action | `16px` | `700` | `1.5` |

The prior non-normative/unresolved form-title, helper, field-error, desktop-title, section/label/control/action line-height values are superseded by these exact Owner-authorized values.

## Spacing destination

- field vertical rhythm: `24px`;
- major section rhythm: `32px`;
- ordinary label → control gap with no helper/error: `8px`;
- label → helper/error: `6px`;
- final helper/error → control: `8px`;
- text-bearing blocks must remain content-driven rather than fixed-height.

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
- use the native Gravity Forms required legend as the single form-level explanation of what `*` means;
- do not create required semantics with CSS-generated content.

## Owner lock — all Radio choices use card presentation

Every authentic Gravity Forms Radio field inside admitted SRWF Registration uses card presentation. This explicitly supersedes the older binary-only interpretation that limited cards to Gender, Graduation Status, or `srwf-role-binary-choice`.

The authentic Gravity Forms `radio` field type inside the admitted SRWF theme is sufficient presentation identity. Existing semantic role mappings may remain for compatibility or unrelated specialization, but **must not gate card presentation**.

For every authentic Radio group:

- every visible option is a card filling its assigned layout cell;
- the whole visible associated label/card remains operable through the authentic radio;
- minimum card/control target height: `52px`;
- radius: `10px`;
- gap: `12px` by default;
- unselected card surface: `#FFFFFF`;
- unselected card border: `1px solid #8690A1`;
- selected card border: `2px solid #1D4ED8`;
- selected surface: `#EDF1FC`;
- selected presentation includes a visible non-color dot/shape cue in addition to color;
- text may wrap; card height must not be fixed;
- two short choices may share one equal-width row where space supports it;
- larger/longer groups may use content/space-driven columns, wrapping, or vertical stacking;
- narrow widths must reflow rather than compress or overflow;
- conditional/hidden Radio fields inherit the same presentation automatically when Gravity Forms reveals them;
- presentation identity must not use option text, label text, numeric field IDs, `nth-child`, DOM position, or artifact order;
- Gravity Forms remains authoritative for radio/fieldset semantics, checked state, keyboard behavior, validation, conditional visibility, persistence, and submission.

## Section icon tiles

Only explicitly mapped semantic section roles receive an icon tile.

- tile: `40px × 40px`;
- radius: `10px`;
- icon: `20px`;
- subtle primary tint: `#EDF1FC`;
- icon-heading gap: `12px`;
- divider: `1px #E4E7EC`, decorative only;
- no inference from section label or DOM position.

The admitted artifact remains the geometry/mapping reference for the already-approved icons; these tile dimensions are the current Owner destination.

## Upload initial visual family

Authentic initial GPFUP upload surfaces admitted to SRWF Registration share one presentation family:

- minimum height: `96px`;
- padding: `16px`;
- radius: `12px`;
- `1px` dashed border: `#8690A1`;
- visible icon/instruction/authentic select-file/helper hierarchy where the authentic consumer provides those parts;
- persistent helper/file-rule text remains legible at the Owner helper typography;
- drag-and-drop must not be the only usable path;
- Gravity Forms / GP File Upload Pro own actual upload behavior.

### Report Card

The explicit Report Card semantic role retains its file-icon specialization over the shared initial upload family:

- file icon visible size: `24px`;
- the already-authorized `96px` / `16px` / `12px` / `1px dashed #8690A1` outer shell is preserved;
- GTB styles presentation only and does not replace GPFUP upload/progress/error/delete behavior.

### Student Photo

The authentic GPFUP image-only configuration class `gpfup--images-only` is an admitted host/configuration seam for the **initial** Student Photo upload-family presentation. It does not encode field identity, wording, numeric ID, DOM position, or artifact order.

GTB does not define crop ratio or crop dimensions for v1. Uploaded/preview/replace/re-crop/delete states may be styled only when authentic GPFUP runtime evidence exposes those consumers. GTB must not invent post-upload composition or lifecycle.

`gpfup_crop_ratio_dimensions` therefore remains runtime/configuration-owned and not a GTB visual constant.

## GP Advanced Select / Tom Select

GTB owns appearance only. Search/filter/selection/keyboard/mobile/screen-reader/Populate Anything behavior remains host/add-on-owned.

- resting minimum height: `52px`;
- radius: `10px`;
- white surface with `#8690A1` boundary;
- canonical focus presentation applies to the visible `.ts-control` consumer;
- dropdown/open/results/no-results/error qualification remains runtime-state dependent.

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

## Visual-repair implementation boundary

The 2026-09-19 visual-fidelity repair statically implements the evidenced presentation differences authorized above while preserving host ownership and existing admission/isolation boundaries. In particular:

- every authentic SRWF Radio field is now presented through the common card system without semantic-role gating;
- target typography/line-height and section icon-heading gap are represented through supported Theme Framework tokens or bounded SRWF selectors;
- initial GPFUP surfaces share the authorized upload-family geometry, with Report Card icon specialization and image-only Student Photo admission kept bounded;
- the diagnostic package adds visible-consumer qualification and explicit module-version provenance without fabricating dynamic runtime states.

This static/automated implementation state is **not** full runtime or production qualification. Authentic Owner runtime evidence is still required for checked/keyboard-focused Radio behavior, validation, GPAS dynamic states, GPFUP post-upload states, exact `320 CSS px`, `200%` text resize, text spacing, complete contrast/target-size acceptance, and other runtime-sensitive obligations.
