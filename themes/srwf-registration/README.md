# SRWF Registration Theme

Status: **First reference implementation / current Owner authority admitted / Radio full-cell repair statically implemented through 0.1.17 / Owner runtime requalification required**

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

The current theme implementation is `0.1.17`; the current runtime diagnostic is `0.3.6`.

The statically implemented presentation set preserves:

- Owner-authorized `16px` mobile inline padding and `320 CSS px` hard acceptance width;
- the `960px` desktop threshold and `904px` outer / `840px` content desktop destination;
- helper `14/400/1.5`, ordinary controls minimum `52px`, Submit minimum `56px` and full available width;
- all authentic SRWF Radio groups using the common card family with content-driven intrinsic reflow;
- mapped section icon tiles unchanged;
- the repaired native single-Select and GP Advanced Select / Tom Select presentation family unchanged;
- Report Card and image-only Student Photo initial GPFUP geometry and intrinsic wrapping unchanged;
- existing per-form configuration/readiness and Registration-versus-Entry-Detail context isolation.

Owner runtime of theme `0.1.14` remains historical upload-family evidence: both admitted initial icon glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` is the prior static cluster repair. Theme `0.1.16` added the bounded intrinsic Radio/GPFUP mobile responsive polish. Theme `0.1.17` adds only the runtime-proven Radio full-cell geometry repair plus implementation-facing evidence updates.

## Proven host-width requirement

The former whole-form narrowness is no longer an unresolved GTB width problem. The Owner configured the dedicated Registration page through the host theme's native full-width content option. GeneratePress is the currently proven Owner-site example; it is **not** a GTB dependency.

Fresh Owner runtime at `390 CSS px` proved the intended chain:

```text
viewport / host full-width content: 390px
→ SRWF wrapper: 390px with 16px inline padding
→ form / ordinary controls / Submit: 358px
```

`document.clientWidth == document.scrollWidth == 390`, with no horizontal scrolling and no visible overflow among the sampled consumers.

The implementation-facing prerequisite is therefore:

> The page hosting the SRWF Registration surface must provide the required full-width content area; GTB then owns its canonical `16px` mobile inline gutter.

GTB does not add CSS/PHP for GeneratePress `.site-content`, `.content-area`, `.site-main`, `.inside-article`, `.entry-content`, page IDs, `body` layout, negative-margin breakout, or viewport-width breakout. Host page layout remains host-owned.

## Radio full-cell root cause and repair

The corrected host width exposed an independent, repeatable Radio defect at `390 CSS px`:

- `.gfield_radio`: `358px`;
- pair gap: `12px`;
- paired `.gchoice`: `173px` each, visible label/card: `161px` each;
- full-row `.gchoice`: `358px`, visible label/card: `346px`;
- diagnostic: `allVisibleLabelsFillChoices: false`.

The exact `12px` deficit matches Gravity Forms' documented secondary-label horizontal reserve, `--gf-label-space-x-secondary`, whose qualified default is `12px`. That reserve normally separates an authentic choice input from its inline label. SRWF intentionally moves the authentic Radio input out of flow and draws the visible circular cue inside the associated label, so the input-to-label reserve is no longer semantically needed in this presentation.

Theme `0.1.17` neutralizes only that reserve inside admitted SRWF Radio groups:

```css
.gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio .gfield_radio {
    --gf-label-space-x-secondary: 0;
    display: flex;
    flex-flow: row wrap;
    gap: 12px;
}
```

This is deliberately **not** a `+12px` card-width hack. The group still owns an explicit `12px` option gap, `.gchoice` remains `flex: 1 1 9.5rem`, labels remain content-height driven, and no mobile device-specific breakpoint is introduced. The native Radio input remains present and authentic; checked, keyboard, validation, conditional visibility, persistence, and submission remain Gravity Forms-owned. Selected border `#1D4ED8`, selected background `#EDF1FC`, and the non-color circular selected cue are unchanged.

## Unchanged adjacent surfaces

The Radio repair does not alter production rules for:

- GP File Upload Pro initial or `.gpfup--has-files` behavior;
- GP Advanced Select / Tom Select;
- normal text/select controls;
- Section Break layout/icons;
- Submit width/behavior;
- Entry Detail isolation.

Diagnostic `0.3.6` remains sufficient and is not bumped: it already records the host/GF/GTB width chain, overflow evidence, per-choice label width delta, and `allVisibleLabelsFillChoices` needed for the next runtime pass.

## Owner runtime requalification

Static tests and exact-head CI are necessary regression evidence; they are not final Owner-site/browser qualification.

Requalify exact theme `0.1.17` + diagnostic `0.3.6` at minimum at:

- `360 CSS px`;
- `390 CSS px`.

Prefer the full matrix: `320 / 360 / 390 / 393 / 412 / 430 CSS px`.

Expected runtime evidence:

- host remains full-width;
- GTB retains its `16px` inline gutter;
- no document horizontal overflow;
- Radio `allVisibleLabelsFillChoices = true`;
- short choices remain side-by-side where actual component width supports them;
- larger groups wrap cleanly and intrinsically;
- selected/unselected visual design remains unchanged;
- GPFUP / GPAS / Submit do not regress;
- authentic checked/focus/validation/conditional Radio behavior remains host-owned.

Page background `#F6F8FB` remains a host-integration responsibility where an authenticated ownership seam exists. Student Photo post-upload/crop/re-crop/delete composition remains runtime-dependent / `NOT_PROVEN` and GPFUP-owned. PersianGravity/Jalali presentation also remains runtime-dependent until an authentic consumer is captured.

## Reuse rule

Do not move this host requirement or Radio repair into a shared multi-theme abstraction merely because the mechanism looks reusable. Promote only after a second real theme or a clearly project-wide invariant proves reuse.