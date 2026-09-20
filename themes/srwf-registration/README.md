# SRWF Registration Theme

Status: **First reference implementation / authority-provenance repair statically implemented through 0.1.18 / Owner runtime requalification required**

This directory is the first real theme built with Gravity Theme Builder.

## Mission lock

The deliverable is not a new SRWF-inspired design. It is faithful implementation of the current admitted SRWF Registration destination under `reference/`.

Before visual implementation planning or review, read:

1. `reference/VISUAL_AUTHORITY.md`;
2. `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md` — current Owner project authority for resolved decisions;
3. `reference/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` — exact historical Drive-backed predecessor retained for provenance/inherited rules;
4. `reference/README.md`;
5. run `reference/materialize_reference.sh` and inspect the verified `OWNER_REFERENCE_new_7.html` where composition/state/geometry matters.

Gravity Forms Theme Framework and inspected runtime evidence determine **HOW** the design is implemented. They do not redefine **WHAT** the current Owner authority says. A later Owner decision must be independently admitted/registered before it can supersede the current authority; implementation prose cannot create that authority.

## Runtime boundary

GTB owns presentation, not form structure or behavior. Preserve Gravity Forms and applicable add-on ownership of fields/order/Section Break structure, validation/submission, conditional logic, accessibility semantics/state, persistence, enhanced-select behavior, upload/crop behavior, and Persian/Iranian field behavior where applicable.

The same configured form can render in Gravity Flow Entry Detail. Registration presentation admission therefore remains a separate request-local context decision; admin configuration state does not disable the existing Entry Detail isolation boundary.

## Current implementation state

The current theme implementation is `0.1.18`; the current runtime diagnostic is `0.3.6`.

The statically implemented presentation set preserves:

- Owner-authorized `16px` mobile inline padding and `320 CSS px` hard acceptance width;
- the `960px` desktop threshold and `904px` outer / `840px` content desktop destination;
- desktop `32px` inline padding, `#FFFFFF` surface, `16px` radius, and no visual-depth shadow or unauthorized `32px` block padding;
- helper `14/400/1.5`, ordinary controls minimum `52px`, Submit minimum `56px` and full available width;
- all authentic SRWF Radio groups using the common card family with content-driven intrinsic reflow;
- mapped section icon tiles unchanged;
- the repaired native single-Select and GP Advanced Select / Tom Select presentation family unchanged;
- Report Card and image-only Student Photo initial GPFUP geometry and intrinsic wrapping unchanged;
- existing per-form configuration/readiness and Registration-versus-Entry-Detail context isolation.

Owner runtime of theme `0.1.14` remains historical upload-family evidence: both admitted initial icon glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` is the prior static cluster repair. Theme `0.1.16` added the bounded intrinsic Radio/GPFUP mobile responsive polish. Theme `0.1.17` added the runtime-proven Radio full-cell geometry repair. Theme `0.1.18` preserves those component/runtime changes while repairing the authority-boundary defect identified as `PRI-FND-001`.

## Desktop shell authority/provenance repair

The verified current Owner authority remains `OWNER:SRWF-2026-09-19`. The admitted desktop shell is:

```text
breakpoint: 960px
outer max: 904px
content target: 840px
inline padding: 32px per side
surface: #FFFFFF
radius: 16px
visual-depth shadow: none
surrounding #F6F8FB canvas: host-owned unless an authenticated page seam exists
```

PR #28 starting Head `88dd1ae253edcd4bb7b09a76994b8915c57c5bc7` had inserted a purported direct `2026-09-20` Owner supersession into the same reconciliation, then made CSS/tests conform to that inserted prose. No independently registered/admitted later Owner authority source existed. Theme `0.1.18` restores the admitted no-depth shell and adds deterministic qualification that rejects a later-dated direct Owner supersession unless it references an explicitly registered/admitted Owner authority handle.

No page-shell takeover is introduced. GTB does not add CSS/PHP for GeneratePress `.site-content`, `.content-area`, `.site-main`, `.inside-article`, `.entry-content`, page IDs, `body` layout, negative-margin breakout, or viewport-width breakout. Host page layout remains host-owned.

## Proven host-width requirement

The former whole-form narrowness is not a GTB width problem. The Owner configured the dedicated Registration page through the host theme's native full-width content option. GeneratePress is the currently proven Owner-site example; it is **not** a GTB dependency.

Fresh Owner runtime at `390 CSS px` previously proved the intended chain:

```text
viewport / host full-width content: 390px
→ SRWF wrapper: 390px with 16px inline padding
→ form / ordinary controls / Submit: 358px
```

`document.clientWidth == document.scrollWidth == 390`, with no horizontal scrolling and no visible overflow among the sampled consumers.

The implementation-facing prerequisite remains:

> The page hosting the SRWF Registration surface must provide the required full-width content area; GTB then owns its canonical `16px` mobile inline gutter.

## Radio full-cell root cause and repair

The corrected host width exposed an independent, repeatable Radio defect at `390 CSS px`:

- `.gfield_radio`: `358px`;
- pair gap: `12px`;
- paired `.gchoice`: `173px` each, visible label/card: `161px` each;
- full-row `.gchoice`: `358px`, visible label/card: `346px`;
- diagnostic: `allVisibleLabelsFillChoices: false`.

The exact `12px` deficit matches Gravity Forms' documented secondary-label horizontal reserve, `--gf-label-space-x-secondary`, whose qualified default is `12px`. SRWF deliberately moves the authentic Radio input out of flow and renders its visible circular cue inside the associated label, so the input-to-label reserve is no longer semantically needed in this presentation.

Theme `0.1.17` neutralizes only that reserve inside admitted SRWF Radio groups:

```css
.gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio .gfield_radio {
    --gf-label-space-x-secondary: 0;
    display: flex;
    flex-flow: row wrap;
    gap: 12px;
}
```

Theme `0.1.18` preserves this repair unchanged. `.gchoice` remains `flex: 1 1 9.5rem`; selected border/background/cue values and native Radio semantics remain unchanged.

## Unchanged adjacent surfaces

The authority/shell repair does not alter production rules for:

- GP File Upload Pro initial or `.gpfup--has-files` behavior;
- GP Advanced Select / Tom Select;
- normal text/select controls;
- Section Break layout/icons;
- Submit width/behavior;
- Entry Detail isolation;
- mobile geometry or the sole product viewport breakpoint.

Diagnostic `0.3.6` remains sufficient and is not bumped.

## Owner runtime requalification

Static tests and exact-head CI are necessary regression evidence; they are not final Owner-site/browser qualification.

Requalify exact theme `0.1.18` + diagnostic `0.3.6` at desktop `960`, `1024`, approximately `1366/1440`, and a wide desktop where practical. Responsive regression remains `320 / 360 / 390 / 393 / 412 / 430 CSS px`.

Also recheck authentic keyboard focus, invalid submission, GPAS open state, GPFUP post-upload state where available, and conditional reveal. Until that is executed against the exact repaired package, browser acceptance remains `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`.

Page background `#F6F8FB` remains a host-integration responsibility where an authenticated ownership seam exists. Student Photo post-upload/crop/re-crop/delete composition remains runtime-dependent / `NOT_PROVEN` and GPFUP-owned. PersianGravity/Jalali presentation also remains runtime-dependent until an authentic consumer is captured.

## Reuse rule

Do not move this authority guard, host requirement, or Radio repair into a shared multi-theme abstraction merely because the mechanism looks reusable. Promote only after a second real theme or a clearly project-wide invariant proves reuse.