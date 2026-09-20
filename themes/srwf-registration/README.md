# SRWF Registration Theme

Status: **Desktop Full Width shell statically implemented through 0.1.18 / Owner runtime requalification required**

This directory is the first real theme built with Gravity Theme Builder.

## Mission lock

The deliverable is not a new SRWF-inspired design. It is faithful implementation of the current admitted SRWF Registration destination under `reference/`.

Before visual implementation planning or review, read:

1. `reference/VISUAL_AUTHORITY.md`;
2. `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md` — current Owner project authority for resolved decisions, including the later Desktop Full Width shell decision;
3. `reference/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` — exact historical Drive-backed predecessor retained for provenance/inherited rules;
4. `reference/README.md`;
5. run `reference/materialize_reference.sh` and inspect the verified `OWNER_REFERENCE_new_7.html` where composition/state/geometry matters.

Gravity Forms Theme Framework and inspected runtime evidence determine **HOW** the design is implemented. They do not redefine **WHAT** the current Owner authority says.

## Runtime boundary

GTB owns presentation, not form structure or behavior. Preserve Gravity Forms and applicable add-on ownership of fields/order/Section Break structure, validation/submission, conditional logic, accessibility semantics/state, persistence, enhanced-select behavior, upload/crop behavior, and Persian/Iranian field behavior where applicable.

The same configured form can render in Gravity Flow Entry Detail. Registration presentation admission therefore remains a separate request-local context decision; admin configuration state does not disable the existing Entry Detail isolation boundary.

## Current implementation state

The current theme implementation is `0.1.18`; the current runtime diagnostic is `0.3.6`.

Theme `0.1.18` preserves:

- Owner-authorized `16px` mobile inline padding and `320 CSS px` hard acceptance width;
- the `960px` desktop threshold and exact `904px` outer / `840px` content desktop geometry;
- ordinary controls minimum `52px`, Submit minimum `56px` and full available width;
- all authentic SRWF Radio groups using the common card family with intrinsic reflow and the 0.1.17 full-cell repair;
- mapped section icon tiles and authentic Section Break semantics;
- native Select plus GP Advanced Select / Tom Select presentation/behavior ownership;
- initial GPFUP family and `.gpfup--has-files` isolation;
- existing per-form configuration/readiness and Registration-versus-Entry-Detail context isolation.

It modernizes only the desktop primary form shell at and above `960px`:

- `32px` block padding while retaining `32px` inline padding;
- white `#FFFFFF` primary surface and `16px` radius;
- non-layout-affecting `1px #E4E7EC` visual ring;
- restrained depth `0 1px 2px rgba(16,24,40,0.04), 0 12px 32px rgba(16,24,40,0.06)`.

The ring is implemented as an outer box-shadow layer, not a literal border, so `904 - 32 - 32 = 840` remains intact. The wrapper deliberately does not add `overflow:hidden`; focus outlines, Tom Select dropdowns, GPFUP states, and validation consumers must not be clipped merely to contain rounded-corner visuals.

## Fluid Section hierarchy

The theme keeps one dominant white primary form surface. It does not turn Section Breaks or following fields into independent cards.

The current Gravity Forms vertical gap is `24px`, while the authentic Section Break has the existing `8px` block-start margin. Together they produce the approved `32px` major section rhythm without inventory-sensitive rules. No `nth-child`, field ID, page ID, label/option text, sibling count, fixed-height section container, or artificial empty cell is used.

## Host width and desktop canvas boundary

The former whole-form narrowness is no longer a GTB width problem. The Owner previously configured the dedicated Registration page through the host theme's native full-width content option. GeneratePress is the currently proven host example; it is **not** a GTB dependency.

The implementation-facing prerequisite remains:

> The page hosting the SRWF Registration surface must provide the required full-width content area; GTB then owns its scoped responsive wrapper geometry.

The preferred surrounding desktop canvas is `#F6F8FB`. Current GTB source does not expose a truthful durable page-level authentication seam for the admitted SRWF Registration page independent of numeric IDs, DOM position, text, or host-theme internals. Therefore 0.1.18 intentionally does not target `html`, `body`, `.site-content`, `.content-area`, `.site-main`, `.inside-article`, `.entry-content`, page IDs, GeneratePress layout classes, negative margins, or viewport breakouts.

The smallest host-side integration requirement is to configure the Registration page/theme so the surrounding desktop canvas is `#F6F8FB` while retaining the already-proven full-width content area. The form-local surface remains complete and isolated without that host canvas.

## Radio full-cell repair retained

The 0.1.17 repair neutralizes Gravity Forms' documented `--gf-label-space-x-secondary` only inside admitted SRWF Radio groups because the authentic Radio input is moved out of flow and its visible circular cue is rendered inside the associated label. It is not a `+12px` width hack: the explicit `12px` option gap, `.gchoice { flex: 1 1 9.5rem; }`, content-driven card height, and native Radio state relationship remain unchanged.

The Owner subsequently confirmed that repair at mobile runtime. Theme 0.1.18 changes no Radio rule and requires only regression requalification as part of the new installable package.

## Add-on boundaries

- **GP File Upload Pro**: presentation remains limited to authentic initial states via `:not(.gpfup--has-files)`. Report Card uses `icons/report-card-file.svg`; image-only Student Photo uses `icons/student-photo-upload.svg`. Post-upload/crop/re-crop/delete remains `OWNER_RUNTIME_REQUIRED / NOT_PROVEN` and GPFUP-owned.
- **GP Advanced Select / Tom Select**: existing visual adapter remains unchanged; open/close/search/results/value behavior remains add-on-owned.
- **Gravity Flow Entry Detail**: Registration theme admission remains excluded there.

## Verification and Owner runtime requalification

Diagnostic `0.3.6` remains sufficient and is not bumped; no diagnostic source/schema changed.

Static/exact-head CI can prove the visual-reference hash, CSS scoping, exact breakpoint/shell declarations, 904/840 arithmetic, non-layout ring/depth, absence of host/page takeover, component-rule preservation, version coherence, and deterministic package closure. It does **not** prove visual browser acceptance.

Owner runtime should requalify desktop `960`, `1024`, representative `1366`/`1440`, and a wide desktop near the previous `~1859 CSS px` baseline where practical, plus responsive regression at `320 / 360 / 390 / 393 / 412 / 430 CSS px`. Also recheck authentic keyboard focus, invalid submission, GPAS open state, GPFUP post-upload where available, conditional reveal, no horizontal overflow/clipping, and full-width Submit.

## Reuse rule

Keep this shell theme-local. Do not promote it into shared GTB core, a GeneratePress adapter, or a page-layout subsystem without a second real reuse case or a proven project-wide invariant.
