# SRWF Registration Theme

Status: **First reference implementation / current Owner authority admitted / mobile responsive polish statically implemented through 0.1.16 / Owner runtime qualification required**

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

Normal operation uses **Gravity Forms → Form Settings → GTB Theme**. There is no top-level GTB admin menu.

The settings surface manages SRWF activation separately from explicit semantic role mappings and projects GTB-owned tokens into authentic Gravity Forms Form/Field objects only on explicit Save. Numeric field/section IDs are internal form references, not durable presentation identity.

Readiness is reported as `DISABLED`, `NEEDS SETUP`, `ATTENTION REQUIRED`, or `READY`. `Check Again` and the recommended setup draft are read-only. The recommended draft never guesses semantic roles from labels, field order, numeric IDs, DOM position, generic field type, or unrelated plugins.

## Runtime boundary

GTB owns presentation, not form structure or behavior. Preserve Gravity Forms and applicable add-on ownership of fields/order/Section Break structure, validation/submission, conditional logic, accessibility semantics/state, persistence, enhanced-select behavior, upload/crop behavior, and Persian/Iranian field behavior where applicable.

The same configured form can render in Gravity Flow Entry Detail. Registration presentation admission therefore remains a separate request-local context decision; admin configuration state does not disable the existing Entry Detail isolation boundary.

## Current implementation state

The current theme implementation is `0.1.16`; the current runtime diagnostic is `0.3.6`.

The statically implemented presentation set preserves:

- Owner-authorized `16px` mobile inline padding and `320 CSS px` hard acceptance width;
- the `960px` desktop threshold and `904px` outer / `840px` content desktop destination;
- helper `14/400/1.5`, ordinary controls minimum `52px`, Submit minimum `56px` and full available width;
- all authentic SRWF Radio groups using the common card family, now with content-driven intrinsic reflow rather than the previous permissive `8rem` basis;
- mapped section icon tiles unchanged;
- the repaired native single-Select and GP Advanced Select / Tom Select presentation family unchanged;
- Report Card and image-only Student Photo initial GPFUP geometry unchanged while their authentic content cluster can wrap naturally at narrow real component widths;
- existing per-form configuration/readiness and Registration-versus-Entry-Detail context isolation.

Owner runtime of theme `0.1.14` remains historical upload-family evidence: both admitted initial icon glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` is the prior static cluster repair. Theme `0.1.16` keeps that repair and adds the bounded mobile responsive polish.

## Mobile width-loss boundary

Static source proves that the SRWF wrapper itself is fluid below the desktop transition: `inline-size:100%`, `max-inline-size:100%`, and `padding-inline:16px`. It does **not** identify which Owner-site WordPress/page-layout ancestor produced the observed narrow whole-form column.

For that reason `0.1.16` does not add negative margins, `html/body` width rules, arbitrary WordPress-container overrides, or an unscoped breakout. Diagnostic `0.3.6` adds the missing bounded evidence: viewport CSS width, DPR, wrapper/GF/ancestor computed geometry, and representative text/Radio/initial-GPFUP/Submit widths. A host integration width repair is allowed only after that evidence proves a dedicated safe SRWF integration seam.

The admin-only diagnostic download controls remain functional but are parked in normal flow so qualification captures are not obstructed by fixed overlays.

## Responsive component changes

The common Radio row remains a wrapping flex layout with `12px` gap. `.gchoice` now uses `flex: 1 1 9.5rem` and its associated label flexes to fill the assigned row height. This keeps cards content-height driven, allows a narrow real container to stack before label text is crushed, and still permits short pairs to share a row when sufficient component width exists. No `320/360/390/393/412/430` device-specific breakpoint is added.

The two admitted initial GPFUP variants keep min `96px`, padding `16px`, radius `12px`, dashed `#8690A1`, a `40×40` icon slot, and `24px` glyph. Their authentic direct content child now uses an intrinsic `13rem` basis with `max-inline-size:100%`; it may wrap below the icon instead of shrinking into a tiny text column. Every production upload selector still stops before `.gpfup--has-files`.

## Current runtime obligations

Owner runtime qualification is required on exact theme `0.1.16` + diagnostic `0.3.6` at `320`, `360`, `390`, `393`, `412`, and `430 CSS px`, including:

- the exact width chain and any constraining host ancestor;
- no ordinary horizontal scrolling;
- clean Radio one-column fallback where two columns would compress, with balanced two-column rows where they genuinely fit;
- coherent initial Report Card / Student Photo GPFUP wrapping;
- full-width Submit and readable helper/error text;
- a real `.gpfup--has-files` transition without initial-state leakage;
- native Select and GPAS/Tom Select geometry/dynamic states;
- Radio checked/keyboard-focused/conditional/validation states;
- `200%` text resize, text-spacing resilience, contrast and target-size acceptance;
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

Static tests and exact-head CI are necessary regression evidence; they are not final Owner-site/browser qualification. Production acceptance still requires the real supported runtime and the mobile matrix above.

## Reuse rule

Do not move SRWF code into top-level shared `src/` merely because it looks generic. Promote only after a second real theme or a clearly project-wide invariant proves reuse.
