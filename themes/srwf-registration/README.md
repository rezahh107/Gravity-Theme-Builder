# SRWF Registration Theme

Status: **First reference implementation / current Owner authority admitted / visual repair statically implemented through 0.1.15 / Owner runtime qualification required**

This directory is the first real theme built with Gravity Theme Builder.

## Mission lock

The deliverable is not a new SRWF-inspired design. It is faithful implementation of the current admitted SRWF Registration destination under `reference/`.

Before visual implementation planning or review, read:

1. `reference/VISUAL_AUTHORITY.md`;
2. `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md` — current Owner project authority for resolved decisions;
3. `reference/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` — exact historical Drive-backed predecessor retained for provenance/inherited rules;
4. `reference/README.md`;
5. run `reference/materialize_reference.sh` and inspect the verified `OWNER_REFERENCE_new_7.html` where composition/state/geometry matters.

The exact historical v1.0.1 mirror is intentionally not rewritten because doing so would falsify its admitted Drive revision/export and repository blob identity. The 2026-09-19 reconciliation is current where it explicitly supersedes that historical state; no unavailable Drive revision/hash has been invented for the newer Owner input.

Gravity Forms Theme Framework and inspected runtime evidence determine **HOW** the design is implemented. They do not redefine **WHAT** the current Owner authority says.

## Current configuration surface

Normal operation uses:

**Gravity Forms → Form Settings → GTB Theme**

There is no top-level GTB admin menu.

The settings surface manages SRWF activation separately from explicit semantic role mappings and projects GTB-owned tokens into authentic Gravity Forms Form/Field objects only on explicit Save. Numeric field/section IDs are internal form references, not durable presentation identity.

Readiness is reported as `DISABLED`, `NEEDS SETUP`, `ATTENTION REQUIRED`, or `READY`. `Check Again` and the recommended setup draft are read-only. The recommended draft never guesses semantic roles from labels, field order, numeric IDs, DOM position, generic field type, or unrelated plugins.

## Runtime boundary

GTB owns presentation, not form structure or behavior. Preserve Gravity Forms and applicable add-on ownership of:

- fields/order/Section Break structure;
- validation and submission;
- conditional logic;
- accessibility semantics and state;
- persistence;
- enhanced-select behavior;
- upload/crop behavior;
- Persian/Iranian field behavior where applicable.

The same configured form can render in Gravity Flow Entry Detail. Registration presentation admission therefore remains a separate request-local context decision; admin configuration state does not disable the existing Entry Detail isolation boundary.

## Scope

Expected responsibilities include public Registration presentation, RTL/Persian typography/layout, field/control appearance, explicit semantic role presentation, responsive behavior, validation/error appearance, keyboard/focus presentation, add-on visual integration, and host isolation.

Out of scope unless separately authorized: Gravity Flow Inbox/Entry Detail visual design, workflow UI, dossier/print, business validation/data logic, a generic page builder, a second theme, or broad behavior replacement.

## Current implementation state

The current merged theme implementation is `0.1.15`; the runtime diagnostic remains `0.3.5`.

The statically implemented presentation set includes:

- the Owner-authorized `960px` desktop threshold, desktop white-card geometry/no-shadow, mobile padding, typography, spacing, focus, and full-width primary action;
- all authentic SRWF Radio groups using the common card presentation without semantic-role gating;
- mapped section icon tiles;
- the repaired native single-Select and GP Advanced Select / Tom Select presentation family;
- the shared initial GPFUP outer family and icon/content-cluster presentation for Report Card and authentic image-only Student Photo;
- existing per-form configuration/readiness and Registration-versus-Entry-Detail context isolation.

Owner runtime of theme `0.1.14` remains historical evidence for the upload family: both admitted initial icon glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` statically repairs that residual defect by centering only the two admitted initial dropareas and constraining only their authentic direct content child into one shrinkable icon/instruction/select-file cluster.

This does **not** mean `0.1.15` is production-qualified. Static/CI evidence proves repository/source/package behavior only for exercised scenarios.

## Current batch boundary

The visual implementation batches authorized so far are no longer waiting on a speculative CSS repair. The next step is **Owner runtime qualification on the exact current `0.1.15` package** and evidence-driven repair only if that runtime exposes a real defect.

Current runtime obligations include, as applicable:

- Report Card and Student Photo initial icon/content-cluster alignment and narrow/mobile wrapping;
- a real `.gpfup--has-files` transition without initial-state leakage;
- native Select and GPAS/Tom Select geometry and dynamic states on the current package;
- Radio checked/keyboard-focused/conditional states;
- validation/error behavior and preserved host semantics;
- exact `320 CSS px` reflow, `200%` text resize, text-spacing resilience, contrast and target-size acceptance;
- relevant PersianGravity/add-on consumers when authentically present.

Page background `#F6F8FB` remains a host-integration responsibility where an authenticated ownership seam exists; GTB must not seize global `html/body` ownership to force it. Student Photo post-upload/crop/re-crop/delete composition remains runtime-dependent / `NOT_PROVEN` and host-owned rather than invented.

## Implementation priority

For each visual requirement:

1. start from the admitted authority chain;
2. use the repository canonical Gravity Forms Theme Framework source/current official Gravity Forms documentation;
3. prefer supported host/Theme Framework APIs;
4. use the smallest theme-scoped direct CSS rule for a demonstrated gap;
5. add an adapter only after real runtime inspection proves a consumer-specific need;
6. never turn an unresolved runtime fact into guessed behavior.

`IMPLEMENTATION_MAP.md` records the current destination, implementation disposition, and evidence status.

## Acceptance

Final production qualification requires real supported-runtime evidence for desktop/mobile composition, 320px reflow, RTL/Persian content, validation/error states, keyboard focus, text enlargement/text spacing, contrast, target sizing, required add-ons/custom fields, isolation, and no submission/validation regression.

Static tests and exact-head CI are necessary regression evidence; they are not final Owner-site/browser qualification.

## Reuse rule

Do not move SRWF code into top-level shared `src/` merely because it looks generic. Promote only after a second real theme or a clearly project-wide invariant proves reuse.
