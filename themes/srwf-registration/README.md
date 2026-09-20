# SRWF Registration Theme

Status: **First reference implementation / registered Desktop Full Width shell statically implemented through 0.1.19 / Owner runtime requalification required**

This directory is the first real theme built with Gravity Theme Builder.

## Mission lock

The deliverable is not a new SRWF-inspired design. It is faithful implementation of the current admitted SRWF Registration destination under `reference/`.

Before visual implementation planning or review, read:

1. `reference/VISUAL_AUTHORITY.md`;
2. `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md` — base current Owner project authority for unaffected decisions;
3. `reference/SRWF_DESKTOP_SHELL_OWNER_DECISION_2026-09-20.md` — separately registered scoped Owner authority for the Desktop Full Width shell;
4. `reference/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` — exact historical Drive-backed predecessor retained for provenance/inherited rules;
5. `reference/README.md`;
6. run `reference/materialize_reference.sh` and inspect the verified `OWNER_REFERENCE_new_7.html` where composition/state/geometry matters.

Gravity Forms Theme Framework and inspected runtime evidence determine **HOW** the design is implemented. They do not redefine **WHAT** the current Owner authority says. A later Owner decision must be independently admitted/registered before it can supersede current authority; implementation prose cannot create that authority.

## Runtime boundary

GTB owns presentation, not form structure or behavior. Preserve Gravity Forms and applicable add-on ownership of fields/order/Section Break structure, validation/submission, conditional logic, accessibility semantics/state, persistence, enhanced-select behavior, upload/crop behavior, and Persian/Iranian field behavior where applicable.

The same configured form can render in Gravity Flow Entry Detail. Registration presentation admission therefore remains a separate request-local context decision; admin configuration state does not disable the existing Entry Detail isolation boundary.

## Current implementation state

The current theme implementation is `0.1.19`; the current runtime diagnostic is `0.3.6`.

The statically implemented presentation set preserves:

- Owner-authorized `16px` mobile inline padding and `320 CSS px` hard acceptance width;
- the `960px` desktop threshold and `904px` outer / `840px` content desktop destination;
- desktop `32px` inline and block padding, `#FFFFFF` surface, `16px` radius, non-layout `#E4E7EC` ring, and restrained approved depth;
- helper `14/400/1.5`, ordinary controls minimum `52px`, Submit minimum `56px` and full available width;
- all authentic SRWF Radio groups using the common card family with content-driven intrinsic reflow;
- mapped section icon tiles unchanged;
- the repaired native single-Select and GP Advanced Select / Tom Select presentation family unchanged;
- Report Card and image-only Student Photo initial GPFUP geometry and intrinsic wrapping unchanged;
- existing per-form configuration/readiness and Registration-versus-Entry-Detail context isolation.

Owner runtime of theme `0.1.14` remains historical upload-family evidence: both admitted initial icon glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` is the prior static cluster repair. Theme `0.1.16` added the bounded intrinsic Radio/GPFUP mobile responsive polish. Theme `0.1.17` added the runtime-proven Radio full-cell geometry repair. Theme `0.1.18` repaired the authority-boundary defect `PRI-FND-001` and restored the then-admitted no-depth shell. Theme `0.1.19` consumes the newly separate registered Owner desktop-shell authority while preserving every unrelated component/runtime lock.

## Desktop Full Width shell authority

The authority chain is now explicit:

```text
OWNER:SRWF-2026-09-19
→ base current Owner reconciliation for unaffected decisions

OWNER:SRWF-2026-09-20-DESKTOP-SHELL
→ separately registered scoped supersession for Desktop Full Width shell only
```

The later handle is recorded in `reference/SRWF_DESKTOP_SHELL_OWNER_DECISION_2026-09-20.md` and registered in `reference/VISUAL_AUTHORITY.md`. It is direct Owner-supplied current project authority, not Executor-authored implementation prose and not a fabricated immutable Drive source.

At and above `960px`, theme `0.1.19` implements:

```text
outer max: 904px
content target: 840px
inline padding: 32px per side
block padding: 32px
surface: #FFFFFF
radius: 16px
boundary: non-layout 1px #E4E7EC ring
depth: 0 1px 2px rgba(16,24,40,0.04),
       0 12px 32px rgba(16,24,40,0.06)
```

The ring is part of the composed `box-shadow`, so the border-box content geometry stays `904 - 32 - 32 = 840px`. No literal width-consuming border or `overflow:hidden` is added. The existing `24px` field rhythm plus authentic Section Break `8px` start margin remains the `32px` major section rhythm; Sections are not converted into independent cards.

The preferred surrounding `#F6F8FB` canvas remains host-owned because no authenticated GTB page-level seam has been established. GTB does not add CSS/PHP for GeneratePress `.site-content`, `.content-area`, `.site-main`, `.inside-article`, `.entry-content`, page IDs, `body` layout, negative-margin breakout, or viewport-width breakout. GeneratePress Full Width remains only a proven host configuration example.

## Provenance guard retained from 0.1.18

PR #28 correctly established that later Owner authority cannot be created by inserting implementation/reconciliation prose. That deterministic guard remains active.

The new shell decision is accepted only because `OWNER:SRWF-2026-09-20-DESKTOP-SHELL` now exists as a separately identifiable Owner source and is explicitly registered in `VISUAL_AUTHORITY.md`. Qualification still rejects an unknown later handle, later direct Owner prose without a registered handle, fabricated implementation prose, and the current shell supersession if the new registration is removed.

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

The exact `12px` deficit matches Gravity Forms' documented secondary-label horizontal reserve, `--gf-label-space-x-secondary`, whose qualified default is `12px`. Theme `0.1.17` neutralized only that reserve inside admitted SRWF Radio groups:

```css
.gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio .gfield_radio {
    --gf-label-space-x-secondary: 0;
    display: flex;
    flex-flow: row wrap;
    gap: 12px;
}
```

Theme `0.1.19` preserves this repair unchanged. `.gchoice` remains `flex: 1 1 9.5rem`; selected border/background/cue values and native Radio semantics remain unchanged.

## Unchanged adjacent surfaces

The shell implementation does not alter production rules for:

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

Requalify exact theme `0.1.19` + diagnostic `0.3.6` at desktop `960`, `1024`, approximately `1366/1440`, and a wide desktop where practical. Responsive regression remains `320 / 360 / 390 / 393 / 412 / 430 CSS px`.

Also recheck authentic keyboard focus, invalid submission, GPAS open state, GPFUP post-upload state where available, and conditional reveal. Until that is executed against the exact package, browser acceptance remains `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`.

Page background `#F6F8FB` remains a host-integration responsibility. Student Photo post-upload/crop/re-crop/delete composition remains runtime-dependent / `NOT_PROVEN` and GPFUP-owned. PersianGravity/Jalali presentation also remains runtime-dependent until an authentic consumer is captured.

## Release system

SRWF Registration now has a dedicated manual exact-source release path in `.github/workflows/srwf-registration-release.yml`. It is intentionally SRWF-specific rather than a speculative multi-theme framework. The workflow verifies a full merged `main` source SHA, source version, deterministic qualification/package bytes, release notes, package boundaries, and tag/release identity before any publication; `publish=false` is the default dry-run mode. See `RELEASING.md` for the short Owner/operator procedure and `RELEASE_NOTES.md` for the source-local notes consumed by publication.

The runtime diagnostic remains separate evidence tooling and is not a default production Release asset.

## Reuse rule

Do not move this scoped shell, authority guard, host requirement, Radio repair, or release workflow into a shared multi-theme abstraction merely because the mechanism looks reusable. Promote only after a second real theme or a clearly project-wide invariant proves reuse.
