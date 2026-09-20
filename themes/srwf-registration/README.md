# SRWF Registration Theme

Status: **First reference implementation / Desktop Full Width shell modernization statically implemented through 0.1.18 / Owner runtime requalification required**

This directory is the first real theme built with Gravity Theme Builder.

## Mission lock

The deliverable is not a new SRWF-inspired design. It is faithful implementation of the current admitted SRWF Registration destination under `reference/`.

Before visual implementation planning or review, read:

1. `reference/VISUAL_AUTHORITY.md`;
2. `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md` — current Owner project authority for resolved decisions;
3. `reference/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` — exact historical Drive-backed predecessor retained for provenance/inherited rules;
4. `reference/README.md`;
5. run `reference/materialize_reference.sh` and inspect the verified `OWNER_REFERENCE_new_7.html` where composition/state/geometry matters.

Gravity Forms Theme Framework and inspected runtime evidence determine **HOW** the design is implemented. They do not redefine **WHAT** the current Owner authority says.

## Runtime boundary

GTB owns presentation, not form structure or behavior. Preserve Gravity Forms and applicable add-on ownership of fields/order/Section Break structure, validation/submission, conditional logic, accessibility semantics/state, persistence, enhanced-select behavior, upload/crop behavior, and Persian/Iranian field behavior where applicable.

The same configured form can render in Gravity Flow Entry Detail. Registration presentation admission therefore remains a separate request-local context decision; admin configuration state does not disable the existing Entry Detail isolation boundary.

## Current implementation state

The current theme implementation is `0.1.18`; the current runtime diagnostic is `0.3.6`.

The statically implemented presentation set preserves:

- Owner-authorized `16px` mobile inline padding and `320 CSS px` hard acceptance width;
- the `960px` desktop threshold and `904px` outer / `840px` content desktop geometry;
- `32px` desktop block and inline padding, white surface, `16px` radius, non-layout `#E4E7EC` ring, and the approved restrained two-layer depth;
- helper `14/400/1.5`, ordinary controls minimum `52px`, Submit minimum `56px` and full available width;
- all authentic SRWF Radio groups using the common card family with content-driven intrinsic reflow and the 0.1.17 full-cell repair unchanged;
- mapped section icon tiles and the existing `24px + 8px = 32px` major-section rhythm unchanged;
- the repaired native single-Select and GP Advanced Select / Tom Select presentation family unchanged;
- Report Card and image-only Student Photo initial GPFUP geometry and intrinsic wrapping unchanged;
- existing per-form configuration/readiness and Registration-versus-Entry-Detail context isolation.

Owner runtime of theme `0.1.14` remains historical upload-family evidence: both admitted initial icon glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` is the prior static cluster repair. Theme `0.1.16` added bounded intrinsic Radio/GPFUP mobile responsive polish. Theme `0.1.17` added the runtime-proven Radio full-cell geometry repair. Theme `0.1.18` changes only the primary desktop surface boundary/depth/block padding plus the corresponding version/docs/tests.

## Desktop Full Width shell

At and above `960 CSS px`, the admitted SRWF wrapper remains the single dominant white form surface:

```text
outer max: 904px
inline padding: 32px + 32px
content target: 840px
block padding: 32px
surface: #FFFFFF
radius: 16px
boundary: 1px #E4E7EC, non-layout ring
shadow 1: 0 1px 2px rgba(16,24,40,0.04)
shadow 2: 0 12px 32px rgba(16,24,40,0.06)
```

The visible boundary is implemented as the first `box-shadow` layer rather than a literal border. It therefore does not consume two pixels of the existing border-box geometry. No `overflow:hidden` is added to the wrapper, so the implementation does not intentionally clip focus rings, Tom Select dropdowns, upload UI, or validation consumers.

The Section Break hierarchy is not converted into section cards. The existing Gravity Forms field gap (`24px`) plus Section Break start margin (`8px`) already provides the approved `32px` major section rhythm without depending on field count, section count, DOM position, or wording.

## Proven host-width and canvas requirement

The former whole-form narrowness is no longer an unresolved GTB width problem. The Owner configured the dedicated Registration page through the host theme's native full-width content option. GeneratePress is the currently proven Owner-site example; it is **not** a GTB dependency.

Fresh Owner runtime at `390 CSS px` proved the intended chain:

```text
viewport / host full-width content: 390px
→ SRWF wrapper: 390px with 16px inline padding
→ form / ordinary controls / Submit: 358px
```

`document.clientWidth == document.scrollWidth == 390`, with no horizontal scrolling and no visible overflow among the sampled consumers.

The implementation-facing width prerequisite remains:

> The page hosting the SRWF Registration surface must provide the required full-width content area; GTB then owns its canonical `16px` mobile inline gutter.

For the preferred desktop `#F6F8FB` canvas, repository inspection found no existing safe authenticated page-level GTB seam. GTB therefore does not target `html`, `body`, `.site-content`, `.content-area`, `.site-main`, `.inside-article`, `.entry-content`, numeric page IDs, or GeneratePress internals. The host/page must provide `#F6F8FB` for the dedicated Registration canvas if that visual is required.

## Radio full-cell repair retained

The corrected host width exposed an independent, repeatable Radio defect at `390 CSS px`:

- `.gfield_radio`: `358px`;
- pair gap: `12px`;
- paired `.gchoice`: `173px` each, visible label/card: `161px` each;
- full-row `.gchoice`: `358px`, visible label/card: `346px`;
- diagnostic: `allVisibleLabelsFillChoices: false`.

The exact `12px` deficit matched Gravity Forms' documented secondary-label horizontal reserve, `--gf-label-space-x-secondary`. Theme `0.1.17` neutralized that reserve only inside admitted SRWF Radio groups because the authentic Radio input is moved out of flow and the visible cue is drawn inside the associated label.

Theme `0.1.18` preserves that repair unchanged. The explicit `12px` group gap, `.gchoice { flex: 1 1 9.5rem; }`, content-height labels, native Radio input, checked/focus relationship, validation, conditional visibility, persistence, and submission remain host-owned.

## Unchanged adjacent surfaces

The desktop shell refinement does not alter production rules for:

- GP File Upload Pro initial or `.gpfup--has-files` behavior;
- GP Advanced Select / Tom Select;
- normal text/select controls;
- Section Break layout/icons;
- Radio geometry/state rules;
- Submit width/behavior;
- Entry Detail isolation.

Diagnostic `0.3.6` remains sufficient and is not bumped because no diagnostic source/schema changed.

## Owner runtime requalification

Static tests and exact-head CI are necessary regression evidence; they are not final Owner-site/browser qualification.

Desktop requalification should cover:

- `960 CSS px`;
- `1024 CSS px`;
- approximately `1366` or `1440 CSS px`;
- a wide desktop near the prior `~1859 CSS px` baseline where practical.

Responsive regression should cover the full `320 / 360 / 390 / 393 / 412 / 430 CSS px` matrix.

Expected evidence includes:

- desktop surface remains centered and fixed at the authorized maximum rather than expanding with the monitor;
- computed `904/840` geometry is preserved;
- ring/depth are subtle and do not create card-within-card clutter;
- host `#F6F8FB` canvas is present only when configured by the host;
- mobile retains the canonical `16px` gutter and receives no desktop shadow/nesting;
- no document horizontal overflow;
- Radio `allVisibleLabelsFillChoices = true` and intrinsic wrapping remains clean;
- GPFUP / GPAS / Submit do not regress;
- authentic focus/invalid/conditional states remain host-owned and visible.

Where practical, also recheck keyboard `:focus-visible`, authentic invalid submission, GPAS open state, GPFUP post-upload state, and conditional reveal. Student Photo post-upload/crop/re-crop/delete composition remains runtime-dependent / `NOT_PROVEN` and GPFUP-owned. PersianGravity/Jalali presentation also remains runtime-dependent until an authentic consumer is captured.

## Reuse rule

Do not move this shell refinement, host requirement, or Radio repair into a shared multi-theme abstraction merely because the mechanism looks reusable. Promote only after a second real theme or a clearly project-wide invariant proves reuse.