# SRWF Registration — Implementation Map

Status: **VISUAL_REPAIR_STATICALLY_IMPLEMENTED / GPFUP_INITIAL_ICON_FAMILY_STATICALLY_IMPLEMENTED / OWNER_RUNTIME_QUALIFICATION_REQUIRED**

This map distinguishes Owner authority, static/source evidence, host ownership, and evidence that still requires the real Owner runtime. Production qualification is intentionally open.

Evidence vocabulary: `OWNER_AUTHORIZED`, `DOCUMENTED`, `SOURCE_PROVEN`, `STATICALLY_PROVEN`, `HISTORICAL_OWNER_RUNTIME_PROVEN`, `OWNER_RUNTIME_REQUIRED`, `HOST_OWNED`, `HOST_INTEGRATION_REQUIRED`, `NOT_PROVEN`.

## Authority inputs

Registered immutable/exact IDs remain defined in `reference/VISUAL_AUTHORITY.md`:

- `VA:ARTIFACT` — admitted `OWNER_REFERENCE_new_7.html`, exact SHA-256 registered there;
- `VA:VC-1.0.0` — historical/base contract;
- `VA:VC-1.0.1` — exact historical Drive-backed Owner revision, including §27.

`OWNER:SRWF-2026-09-19`, recorded in `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md`, is implementation-driving for the current destination. The current Owner lock requires every authentic Gravity Forms Radio field inside admitted SRWF Registration to use card presentation and requires both authentic initial GPFUP upload surfaces to present a consistent decorative icon slot. These decisions leave the exact historical v1.0.1 mirror byte-preserved.

Historical labels such as `RUNTIME_REQUIRED`, `NOT_PROVEN`, `NON_NORMATIVE_REFERENCE`, and `DEFER_NOT_PROVEN` remain provenance rather than current destination truth where the current reconciliation resolves them. Historical desktop short-field pairings remain superseded by `HOST_OWNED / OWNER_CONFIGURABLE`; the authorized desktop card remains shadowless.

## Implementation traceability

| Requirement | Current destination | Mechanism / ownership | Current disposition |
|---|---|---|---|
| Theme activation | explicit SRWF opt-in, unrelated forms untouched | stored form class establishes identity; rendering context separately gates admission | `STATICALLY_PROVEN`; exact-head browser `OWNER_RUNTIME_REQUIRED` |
| Gravity Flow Entry Detail | excluded even for same stored form | retained source-proven early enqueue + content bracket admission boundary | regression-tested; fresh Owner runtime `OWNER_RUNTIME_REQUIRED` |
| Per-form setup | Gravity Forms → Form Settings → GTB Theme | supported Form Settings hooks; no top-level menu | `STATICALLY_PROVEN`; historical product-path runtime evidence exists |
| Semantic mapping | explicit internal references project GTB-owned specialization tokens | no label/ID/order/DOM inference; semantic roles are not required for all-radio card presentation | `STATICALLY_PROVEN` |
| Projection safety | preserve unrelated Custom CSS classes; remove stale GTB tokens; idempotent | existing validated full Form Object update | `STATICALLY_PROVEN` |
| Production breakpoint | `960 CSS px` | viewport media query | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime `OWNER_RUNTIME_REQUIRED` |
| Mobile shell | fluid; `16px` inline padding | SRWF wrapper only | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED` |
| Desktop card | white; `840px` content + `32px` + `32px` = `904px` outer; radius `16px`; shadow none | `border-box`, `max-inline-size:904px`, `padding-inline:32px` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Page background | `#F6F8FB` where an authenticated ownership seam exists | surrounding host/page integration | `HOST_INTEGRATION_REQUIRED`; GTB does not seize `html/body` |
| Form title | mobile `24px`, desktop `26px`, `700 / 1.5`; Vazirmatn-first full fallback stack | bounded stronger framework-sentinel selector at the real heading consumer | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Section title | `18px / 700 / 1.5`; Vazirmatn-first full fallback stack | authentic Section Break title with bounded framework-sentinel selector | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Field label | `15px / 600 / 1.5` | Gravity Forms Theme Framework API | `DOCUMENTED / STATICALLY_IMPLEMENTED`; runtime pending |
| Control value | `16px / 400 / 1.5`, min `52px` | Gravity Forms Theme Framework `--gf-ctrl-*` tokens; line-height separated from control size | `DOCUMENTED / STATICALLY_IMPLEMENTED`; runtime pending |
| Helper | `14px / 400 / 1.5` | Gravity Forms description CSS API | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Field error | `14px / 600 / 1.5` | Gravity Forms error-description CSS API | `DOCUMENTED / STATICALLY_IMPLEMENTED`; authentic invalid submission pending |
| Primary action | `16px / 700 / 1.5`, full available width, min `56px`, host submit lifecycle | Theme Framework tokens + retained source/runtime-qualified sentinel width repair | `STATICALLY_PROVEN` source geometry; runtime recheck required |
| Ordinary field rhythm | `24px` | `--gf-form-gap-y`; diagnostic v0.3.5 row-normalizes paired fields | `DOCUMENTED / STATICALLY_IMPLEMENTED`; actual visible-row geometry runtime pending |
| Major section rhythm | `32px` | host `24px` form gap + bounded `8px` Section Break offset | `STATICALLY_IMPLEMENTED`; actual geometry runtime pending |
| Field-internal spacing | no-helper label→control `8px`; label→helper/error `6px`; final helper/error→control `8px`; intermediate helper/error spacing remains content/host-driven | documented `--gf-label-space-primary:8px` and `--gf-desc-space:8px`; narrow SRWF field selectors reduce only the primary-label transition to `6px` when authentic above-input helper/error consumers are present | `OWNER_AUTHORIZED / STATICALLY_PROVEN`; computed browser geometry `OWNER_RUNTIME_REQUIRED` |
| Visible focus | `2px solid #1D4ED8`, offset `2px`, no intended glow | GF focus API; direct projection from native hidden radio focus to visible card | `DOCUMENTED / STATICALLY_IMPLEMENTED`; authentic keyboard runtime pending |
| Native single Select | same SRWF control/value family with `24px` logical content start, `32px` indicator reserve, and runtime-proven vertical optical alignment | documented `--gf-ctrl-select-padding-x:24px 32px`; bounded SRWF `.gfield--type-select select.gfield_select:not([multiple]):not(.tomselected):not(.ts-hidden-accessible)` applies only `padding-block-start:14px`; native GF value/keyboard/open behavior remains host-owned | Owner runtime proved the padding correction closes the visible misalignment; exact 0.1.14 computed browser recheck `OWNER_RUNTIME_REQUIRED` |
| All Radio choices | every authentic admitted `.gfield--type-radio` uses cards; fill assigned cell; `12px` gap; min `52px`; radius `10px`; unselected `1px #8690A1`; selected `2px #1D4ED8` + `#EDF1FC` + non-color dot cue | native GF radio/label state remains authority; CSS uses host field type, `:checked`, `:focus-visible`; flex-wrap/content-driven layout; no role/text/ID/order gate | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; checked/keyboard/320px runtime pending |
| Conditional Radio fields | inherit same cards when Gravity Forms reveals them | same field-type rule; GTB does not control conditional visibility | `STATICALLY_PROVEN` selector coverage; authentic reveal runtime pending |
| Section icon tiles | explicit mapped section roles only; `40×40`, radius `10`, icon `20`, tint `#EDF1FC`, heading gap `12px` | admitted local SVGs | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Shared initial GPFUP family | min `96px`; pad `16px`; radius `12px`; `1px` dashed `#8690A1`; every admitted initial surface has a visible `40×40` decorative icon slot with `24px` glyph and common icon/instruction/select-file alignment rhythm | authentic `.gfield--type-fileupload .gpfup:not(.gpfup--has-files)` shell plus a grouped, SRWF-scoped icon-slot rule covering only the admitted Report Card and image-only initial variants; GPFUP behavior remains host-owned | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; Owner-browser geometry `OWNER_RUNTIME_REQUIRED` |
| Report Card initial GPFUP | shared outer family + file/document icon `24px` in the shared icon-slot family | explicit `srwf-role-report-card-upload` only for glyph specialization; `icons/report-card-file.svg`; authentic initial GPFUP state | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime hierarchy recheck pending |
| Report Card has-files | do not force initial state over uploaded UI | initial rules stop at authentic `.gpfup--has-files` state | `HOST_OWNED`; regression-protected; real upload runtime pending |
| Student Photo initial | shared initial family + visible photo/camera icon aligned through the same icon-slot presentation as Report Card | authentic host/config seam `.gpfup.gpfup--images-only:not(.gpfup--has-files)`; `icons/student-photo-upload.svg`; GTB-owned local asset/CSS only; no field ID/text/order identity | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime confirmation required |
| Student Photo post-upload | style only authentic exposed GPFUP preview/replace/re-crop/delete states | no speculative post-upload selector/composition; crop ratio/dimensions remain host/config-owned | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN` |
| GPAS / Tom Select | same select-family inline metric, 52px minimum, zero block padding, SRWF focus visual; add-on behavior untouched | proven `.ts-wrapper > .ts-control` consumes the shared documented `--gf-ctrl-select-padding-x`; source `<select>` classes `.tomselected` / `.ts-hidden-accessible` are excluded from the native-only optical rule; diagnostic targets the visible `.ts-control` | behavior `HOST_OWNED`; exact 0.1.14 open/focus/results runtime pending |
| PersianGravity / Jalali | style only authentic consumer if admitted | no selector/adapter invented | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN` presentation |
| Desktop short-field pairings | Gravity Forms configuration remains authoritative | no GTB pair map | `HOST_OWNED / OWNER_CONFIGURABLE` |
| 320px/200%/text spacing/contrast | resilient intrinsic layout required | logical sizing/wrapping + host responsive mechanics | `OWNER_RUNTIME_REQUIRED` |

## Visual-role authority traceability

The exact historical v1.0.1/artifact path remains retrievable. The current Owner reconciliation supersedes only the specific presentation interpretations it explicitly resolves; it does not erase historical semantic roles or their provenance.

| Requirement | Authority path | Implementation | Current disposition |
|---|---|---|---|
| Gender historical binary role | `VA:VC-1.0.1` §27 + `VA:ARTIFACT` + current Owner reconciliation | `srwf-role-binary-choice` may remain configured, but card presentation comes from authentic radio field type | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Graduation Status historical binary role | same historical chain + current all-radio lock | same: semantic role no longer gates cards; conditional visibility stays host-owned | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Other authentic Radio groups | current Owner all-radio lock | same `.gfield--type-radio` card system automatically covers visible/conditional groups | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Section iconography | `VA:VC-1.0.1` §27 `section_heading_iconography` + `VA:ARTIFACT` + current reconciliation | explicit mapped Section Break tokens + local SVGs | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Report Card initial GPFUP | `VA:VC-1.0.1` §27 `report_card_upload_initial` + `VA:ARTIFACT` + current reconciliation | shared initial GPFUP family + shared `40×40` slot + Report Card `24px` file/document glyph | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Report Card `.gpfup--has-files` | `VA:VC-1.0.1` §§19,27 + host-owned GPFUP lifecycle | initial rules stop at authentic `.gpfup--has-files` state | `HOST_OWNED`; runtime recheck pending |
| Student Photo initial | current Owner upload-family icon/alignment lock + authentic GPFUP image-only runtime/config evidence (`gpfup--images-only`) | shared initial shell and icon slot + `src/icons/student-photo-upload.svg` photo/camera glyph | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Student Photo post-upload | `VA:VC-1.0.1` §27 + `VA:ARTIFACT` + current reconciliation | none until authentic Photo state/DOM is captured | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`; crop config `HOST_OWNED` |

## Gravity Forms Form Presentation Readiness

The GTB Theme settings page reports the current and expected host-owned Form Layout values without mutation:

| Form Object property | Expected |
|---|---|
| `labelPlacement` | `top_label` |
| `descriptionPlacement` | `above` |
| `validationPlacement` | `above` |
| `subLabelPlacement` | `above` |
| `validationSummary` | `true` |
| `requiredIndicator` | `asterisk` |

`Check Again` and ordinary render remain read-only. **Apply Recommended SRWF Form Layout** remains a separate explicit capability + nonce protected action. At mutation time it re-reads the current full Form Object, computes only the six-property diff, performs no write when already matching, changes only those properties, calls `GFAPI::update_form()` with the coherent current object, re-reads it, and verifies persistence. `customRequiredIndicator` and unrelated form state are preserved.

Explicit field-level `labelPlacement`, `descriptionPlacement`, and `subLabelPlacement` values that conflict with the destination are reported as `ATTENTION REQUIRED` with a field ID/type reference. They are not silently rewritten. Overall Form Presentation Readiness is not `READY` while a known conflict remains.

Evidence: Gravity Forms Form Object/settings/update behavior is `DOCUMENTED`/`SOURCE_PROVEN`; mutation/read-back/preservation is `STATICALLY_PROVEN` by the PHP harness; actual Owner-site current values remain `OWNER_RUNTIME_REQUIRED`.

## Required indicator explanation

For `requiredIndicator=asterisk`, Gravity Forms' native required legend remains the single explanation surface. GTB does not inject a parallel paragraph, suppress or replace the native legend, or recreate required state/indicator/ARIA/validation semantics.

## Diagnostic package v0.3.5

The package keeps previously proven collectors intact and adds bounded repair-specific evidence rather than pretending old modules were rewritten. Reports expose an explicit version map:

- package / provenance augmenter: `0.3.5`;
- structural collector: `0.3.0`;
- admission collector: `0.3.2`;
- existing SRWF v1 qualification: `0.3.4`;
- radio-card geometry collector: `0.3.5`;
- visual-repair qualification collector: `0.3.5`.

The existing v0.3.5 visual-repair collector already covers the new initial upload icon requirement without a source/version change. For both admitted upload consumers it records the drop-area rect/computed style plus `::before` width, height, background size, background image and radius. The updated deterministic fixture now exercises both the Report Card and image-only Student Photo pseudo-icon geometry.

The v0.3.5 collectors measure, within bounded admitted SRWF targets:

- **every authentic Radio field**, not only a semantic binary role, with visible/hidden distinction from actual geometry;
- visible `.gchoice` and associated label/card rects, label occupancy delta, current checked state when authentic, and visible pseudo-element selected-cue facts;
- row-normalized visible ordinary-field rhythm so same-row pairings do not create bogus negative gaps;
- user-relevant horizontal overflow from visible consumers against the actual SRWF wrapper instead of latent hidden/offscreen consumers;
- actual section heading gap, divider, icon pseudo geometry, and heading typography;
- representative ordinary field-label typography;
- local label/helper/error/control geometry chain where authentic consumers exist;
- Report Card drop-area/pseudo icon/internal child structure;
- Student Photo initial admission and pseudo-icon geometry when authentic GPFUP `gpfup--images-only` configuration exists; otherwise `NOT_PROVEN`;
- the visible Tom Select `.ts-control`, distinguished from the source `<select>`;
- primary-action typography;
- explicit runtime-only markers for checked/focus/validation/GPAS dynamic/GPFUP post-upload states instead of inferring PASS from latent CSS.

It intentionally excludes entered values, labels/arbitrary page text, select option contents, filenames, upload URLs, and query data. Static CSS capability does not convert dynamic runtime states into a PASS.

## Exact section/icon mapping

| Semantic section role | Approved section | Local asset |
|---|---|---|
| `srwf-role-section-identity` | هویت دانش‌آموز | `src/icons/section-identity.svg` |
| `srwf-role-section-contact` | اطلاعات تماس | `src/icons/section-contact.svg` |
| `srwf-role-section-education` | تحصیلات | `src/icons/section-education.svg` |
| `srwf-role-section-school-documents` | مدرسه و مدارک | `src/icons/section-school-documents.svg` |
| `srwf-role-section-student-photo` | عکس دانش‌آموز | `src/icons/section-student-photo.svg` |

Initial upload glyphs are likewise local presentation assets:

| Initial GPFUP variant | Authentic seam | Local glyph |
|---|---|---|
| Report Card | `srwf-role-report-card-upload` + initial `.gpfup:not(.gpfup--has-files)` | `src/icons/report-card-file.svg` |
| Student Photo | `.gpfup.gpfup--images-only:not(.gpfup--has-files)` | `src/icons/student-photo-upload.svg` |

## Batch boundary

Theme 0.1.14 statically implements the Owner-authorized shared initial GPFUP icon/alignment family through theme-local CSS and local SVG assets. It does not alter GPFUP markup or lifecycle and does not style Student Photo post-upload/crop composition.

The broader Owner runtime qualification remains open: initial Report Card/Student Photo icon visibility and alignment, `.gpfup--has-files` non-leakage in a real upload transition, PR #21 Select/Tom Select geometry, exact `320 CSS px`, accessibility states, and other runtime-only obligations still require authentic Owner-browser evidence.

`STATICALLY_IMPLEMENTED` / `STATICALLY_PROVEN` does **not** mean WordPress/browser production qualification. Exact-head CI and installable packages provide regression/build evidence only; the bounded Owner real-site runtime checklist remains required.
