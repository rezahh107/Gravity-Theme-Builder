# SRWF Registration — Implementation Map

Status: **RADIO_FULL_CELL_REPAIR_STATICALLY_IMPLEMENTED / OWNER_RUNTIME_REQUALIFICATION_REQUIRED**

This map distinguishes current Owner authority, repository/static evidence, host ownership, and evidence that still requires the real Owner WordPress/browser runtime. CI/static success is not production visual qualification.

Evidence vocabulary: `OWNER_AUTHORIZED`, `DOCUMENTED`, `SOURCE_PROVEN`, `STATICALLY_PROVEN`, `HISTORICAL_OWNER_RUNTIME_PROVEN`, `OWNER_RUNTIME_PROVEN`, `OWNER_RUNTIME_REQUIRED`, `HOST_OWNED`, `HOST_INTEGRATION_REQUIRED`, `NOT_PROVEN`.

## Authority inputs

Registered immutable/exact IDs remain defined in `reference/VISUAL_AUTHORITY.md`:

- `VA:ARTIFACT` — admitted `OWNER_REFERENCE_new_7.html`, exact SHA-256 registered there;
- `VA:VC-1.0.0` — historical/base contract;
- `VA:VC-1.0.1` — exact historical Drive-backed Owner revision, including §27.

`OWNER:SRWF-2026-09-19`, recorded in `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md`, remains implementation-driving for the current destination. It supersedes only contradictory/unresolved historical states it explicitly resolves. The historical artifact and contract remain provenance and must not roll back a newer Owner decision.

Current static theme implementation: `0.1.17`.

Owner runtime of theme `0.1.14` is retained as historical evidence for the initial GPFUP repair: both admitted glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` is the prior static icon/content-cluster repair. Theme `0.1.16` added bounded intrinsic Radio and initial GPFUP narrow/mobile reflow. Theme `0.1.17` retains those behaviors and closes the newly runtime-proven Radio full-cell defect by neutralizing the Gravity Forms secondary-label horizontal reserve only inside admitted SRWF Radio groups.

## Implementation traceability

| Requirement | Current destination | Mechanism / ownership | Current disposition |
|---|---|---|---|
| Theme activation | explicit SRWF opt-in; unrelated forms untouched | stored form class establishes identity; rendering context separately gates admission | `STATICALLY_PROVEN`; exact-head browser `OWNER_RUNTIME_REQUIRED` |
| Gravity Flow Entry Detail | excluded even for same stored form | retained source-proven early enqueue + content bracket admission boundary | regression-tested; fresh Owner runtime `OWNER_RUNTIME_REQUIRED` |
| Per-form setup | Gravity Forms → Form Settings → GTB Theme | supported Form Settings hooks; no top-level menu | `STATICALLY_PROVEN` |
| Semantic mapping | explicit internal references project GTB-owned specialization tokens | no label/ID/order/DOM inference; semantic roles do not gate all-Radio cards | `STATICALLY_PROVEN` |
| Production breakpoint | `960 CSS px` | one viewport media query; not a device-name preset | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime matrix `OWNER_RUNTIME_REQUIRED` |
| Mobile shell | fluid; `16px` inline padding; hard acceptance `320 CSS px` | SRWF wrapper only; no mobile max-width | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; `390 CSS px` width chain `OWNER_RUNTIME_PROVEN` |
| Desktop card | white; `840px` content + `32px` + `32px` = `904px` outer; radius `16px`; shadow none | `border-box`, `max-inline-size:904px`, `padding-inline:32px` at `min-width:960px` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Page / host width | page hosting Registration must provide the required full-width content area; GTB then owns only its canonical `16px` mobile inline gutter | host/page configuration; GeneratePress native Full Width is the currently proven Owner-site example, not a GTB dependency | `HOST_OWNED`; intended chain `OWNER_RUNTIME_PROVEN` at `390 CSS px`; no GTB host-layout override required or desired |
| Page background | `#F6F8FB` only where an authenticated ownership seam exists | surrounding page integration | `HOST_INTEGRATION_REQUIRED`; GTB does not seize `html/body` |
| Form title | mobile `24px`, desktop `26px`, `700 / 1.5` | bounded framework-sentinel selector | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Section title | `18px / 700 / 1.5` | authentic Section Break title | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Field label | `15px / 600 / 1.5` | Gravity Forms Theme Framework API | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Control value | `16px / 400 / 1.5`, min `52px` | Theme Framework `--gf-ctrl-*` tokens | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Helper | `14px / 400 / 1.5` | Gravity Forms description CSS API | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Field error | `14px / 600 / 1.5` | Gravity Forms error-description API | `DOCUMENTED / STATICALLY_IMPLEMENTED`; authentic invalid submission pending |
| Primary action | `16px / 700 / 1.5`, full available width, min `56px` | Theme Framework tokens + bounded SRWF width enforcement | `STATICALLY_PROVEN`; `390 CSS px` full-width result historically observed; exact 0.1.17 recheck required |
| Field-internal spacing | no-helper label→control `8px`; label→helper/error `6px`; final helper/error→control `8px`; intermediate helper/error spacing remains content/host-driven | `--gf-label-space-primary:8px`, `--gf-desc-space:8px`, bounded `--gf-label-space-primary:6px` when authentic above-input helper/error consumers exist | `OWNER_AUTHORIZED / STATICALLY_PROVEN`; computed browser geometry `OWNER_RUNTIME_REQUIRED` |
| Visible focus | `2px solid #1D4ED8`, offset `2px`, no intended glow | GF focus API; hidden native Radio focus projects to visible card | `DOCUMENTED / STATICALLY_IMPLEMENTED`; authentic keyboard runtime pending |
| Native single Select | shared control family + documented `--gf-ctrl-select-padding-x:24px 32px`; retained runtime-proven vertical optical compensation | bounded native-only selector excludes enhanced Tom Select source | historical runtime evidence exists; current exact-head browser recheck `OWNER_RUNTIME_REQUIRED` |
| All Radio choices | every authentic admitted `.gfield--type-radio` uses cards; visible label fills assigned `.gchoice`; `12px` option gap; min `52px`; radius `10px`; unselected `1px #8690A1`; selected `2px #1D4ED8` + `#EDF1FC` + non-color dot cue | `.gfield_radio` keeps intrinsic Flex wrapping and explicit `12px` option gap; documented `--gf-label-space-x-secondary` is neutralized only in SRWF Radio because the authentic input is out of flow and the visible cue lives inside the label; `.gchoice` retains `flex:1 1 9.5rem`; native input/label/checked/focus semantics retained | root cause `RUNTIME_PROVEN`; repair `STATICALLY_IMPLEMENTED`; post-fix `allVisibleLabelsFillChoices=true` is `OWNER_RUNTIME_REQUIRED` |
| Conditional Radio fields | inherit same cards when Gravity Forms reveals them | same field-type rule; GTB does not control conditional visibility | selector coverage `STATICALLY_PROVEN`; authentic reveal runtime pending |
| Section icon tiles | explicit mapped section roles only; `40×40`, radius `10`, icon `20`, tint `#EDF1FC`, heading gap `12px` | admitted local SVGs | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Shared initial GPFUP family | min `96px`; pad `16px`; radius `12px`; `1px` dashed `#8690A1`; `40×40` icon slot; `24px` glyph | authentic initial state only; direct content child uses intrinsic `13rem` basis + `max-inline-size:100%` so it wraps before being crushed | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; exact 0.1.17 runtime regression check required |
| Report Card initial GPFUP | shared family + file/document glyph | explicit `srwf-role-report-card-upload`; `icons/report-card-file.svg`; only `:not(.gpfup--has-files)` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime recheck pending |
| Report Card `.gpfup--has-files` | do not force initial state over uploaded UI | all theme upload rules stop before authentic has-files state | `HOST_OWNED`; real transition `OWNER_RUNTIME_REQUIRED` |
| Student Photo initial | shared initial family + photo/camera glyph | authentic `gpfup--images-only:not(.gpfup--has-files)`; `icons/student-photo-upload.svg` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime recheck pending |
| Student Photo post-upload | style only authentic exposed preview/replace/re-crop/delete states | no speculative post-upload/crop composition; crop config host-owned | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`; `HOST_OWNED` |
| GPAS / Tom Select | same select-family metric/focus, host owns behavior | proven `.ts-wrapper > .ts-control` consumer | behavior `HOST_OWNED`; exact 0.1.17 dynamic runtime regression check required |
| PersianGravity / Jalali | style only authentic consumer if admitted | no selector/adapter invented | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN` |
| Desktop short-field pairings | Gravity Forms configuration remains authoritative | no GTB pair map | `HOST_OWNED / OWNER_CONFIGURABLE` |
| Accessibility / reflow | `320px`, `200%` text resize, text spacing, contrast, target/focus acceptance | intrinsic wrapping + host responsive mechanics | `OWNER_RUNTIME_REQUIRED` |

## Host-width runtime evidence and ownership boundary

The earlier narrow whole-form observation is now explained operationally by the Owner-site page layout rather than by SRWF wrapper CSS. The Owner changed the dedicated SRWF Registration page to use its host theme's native full-width content configuration. GeneratePress is the currently proven host example; it is not a GTB dependency or selector contract.

Fresh Owner runtime at `390 CSS px` established the intended chain:

- viewport/client width `390px`;
- `.site-content`, `.content-area`, `.site-main`, article, `.inside-article`, and `.entry-content` each provide the full `390px` page width, with `.site-content` inline padding `0px`;
- the SRWF wrapper is `390px` wide and retains `16px` inline padding;
- the actual form, representative ordinary controls, and Submit are `358px` wide (`390 - 16 - 16`);
- `document.clientWidth == document.scrollWidth == 390`;
- no horizontal scrolling; `49` sampled visible consumers; `0` visible overflow consumers.

This is the implementation-facing host prerequisite:

> The page hosting the SRWF Registration surface must provide the required full-width content area. GTB then owns its canonical `16px` mobile inline gutter.

GTB does **not** remove host container padding, target `.site-content` or other theme-specific layout internals, depend on GeneratePress page classes, use body/page IDs, apply negative margins, or break out to viewport width for this requirement. No GTB host-layout repair is required or desired for the proven Owner site.

Diagnostic package v0.3.6 remains sufficient for requalification. It already records:

- `window.innerWidth` and `devicePixelRatio`;
- SRWF wrapper rect and computed width/max-width/padding/margin;
- immediate Gravity Forms form/body/fields geometry;
- bounded ancestors through the first captured `body`, including rect and computed width/max-width/padding/margin/overflow;
- representative text input, Radio group, initial GPFUP droparea, and Submit widths;
- visible-consumer overflow, typography, field rhythm, initial upload, Radio geometry, and `allVisibleLabelsFillChoices` qualification evidence.

The diagnostic remains admin-gated and does not read field content/values. Admin-only download controls remain functional and are parked in normal flow by the final composer.

## Radio full-cell root cause and repair

Owner runtime after the host-width correction proved the remaining Radio defect was independent of page width:

- group width `358px`, option gap `12px`;
- paired `.gchoice` cells `173px`, visible labels `161px`;
- full-row `.gchoice` `358px`, visible label `346px`;
- the repeatable deficit is exactly `12px` across authentic visible SRWF Radio fields;
- pre-repair diagnostic result: `allVisibleLabelsFillChoices: false`.

Gravity Forms documents `--gf-label-space-x-secondary` as the secondary-label horizontal spacer with a `12px` default. SRWF intentionally moves the authentic Radio input out of flow and renders the visible non-color cue inside the associated label. The normal input-to-secondary-label reserve therefore becomes orphaned in this presentation and consumes exactly the measured `12px` of cell width.

Theme `0.1.17` neutralizes that documented spacer with `--gf-label-space-x-secondary:0` only on the admitted SRWF Radio group. It does **not** add `12px` back to card width, use `calc()`, change the explicit `12px` option-to-option gap, change the `9.5rem` intrinsic basis, change selected/unselected visual values, or replace the native Radio input/label state relationship.

## Visual-role authority traceability

The exact historical v1.0.1/artifact path remains retrievable. The current Owner reconciliation supersedes only the presentation interpretations it explicitly resolves.

| Requirement | Authority path | Implementation | Current disposition |
|---|---|---|---|
| Gender historical binary role | `VA:VC-1.0.1` + `VA:ARTIFACT` + current Owner reconciliation | `srwf-role-binary-choice` may remain configured, but card presentation comes from authentic Radio field type | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; post-fix runtime pending |
| Graduation Status historical binary role | current all-radio lock | semantic role no longer gates cards; conditional visibility stays host-owned | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; post-fix runtime pending |
| Other authentic Radio groups | current Owner all-radio lock | same `.gfield--type-radio` card system automatically covers visible/conditional groups | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; post-fix runtime pending |
| Section iconography | `VA:VC-1.0.1` + `VA:ARTIFACT` + `section_heading_iconography` | explicit mapped Section Break tokens + local SVGs | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Report Card initial GPFUP | `VA:VC-1.0.1` + `VA:ARTIFACT` + `report_card_upload_initial` | shared initial family + `icons/report-card-file.svg` + intrinsic content wrapping | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Report Card `.gpfup--has-files` | `VA:VC-1.0.1` + host-owned GPFUP lifecycle | initial rules stop before authentic has-files state | `HOST_OWNED`; real transition `OWNER_RUNTIME_REQUIRED` |
| Student Photo initial | current Owner upload-family lock + authentic GPFUP image-only runtime/config evidence | shared initial family + authentic `gpfup--images-only` + `student-photo-upload.svg` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Student Photo post-upload | `VA:VC-1.0.1` + `VA:ARTIFACT` + current reconciliation | none until authentic Photo post-upload/crop state is captured | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`; host-owned |

## Gravity Forms Form Presentation Readiness

The GTB Theme settings page reports the host-owned Form Layout destination without silent mutation:

| Form Object property | Expected |
|---|---|
| `labelPlacement` | `top_label` |
| `descriptionPlacement` | `above` |
| `validationPlacement` | `above` |
| `subLabelPlacement` | `above` |
| `validationSummary` | `true` |
| `requiredIndicator` | `asterisk` |

`Check Again` and ordinary render remain read-only. **Apply Recommended SRWF Form Layout** remains a separate capability + nonce protected action that re-reads the current full Form Object, changes only the six approved properties, persists through `GFAPI::update_form()`, and verifies the read-back. Field-level placement conflicts are reported rather than silently normalized.

## Required indicator explanation

For `requiredIndicator=asterisk`, Gravity Forms' native required legend remains the single explanation surface. GTB does not inject a parallel paragraph, suppress or replace the native legend, or recreate required/ARIA/validation semantics.

## Package / verification boundary

Theme package: `0.1.17`.
Diagnostic package: `0.3.6`.

The deterministic/static suite is expected to prove SRWF scoping, current package constants, the secondary-label-spacer repair, Radio/GPFUP intrinsic rules, no fixed card height, no device-specific mobile breakpoint, `.gpfup--has-files` isolation, canonical mobile `16px` padding, desktop `960px` / `904px` contract retention, no host-theme/page-layout takeover, Entry Detail/unrelated-form isolation, diagnostic privacy/width-chain structure, and package/version coherence.

It does **not** prove the repaired card geometry in the Owner browser. The next Owner runtime pass must establish `allVisibleLabelsFillChoices = true`, no horizontal overflow, preserved side-by-side short choices and clean wrapping of larger groups, and no GPFUP/GPAS/Submit regression. Verify at minimum `360` and `390 CSS px`, preferably the full `320/360/390/393/412/430 CSS px` matrix. Authentic checked/focus/invalid/conditional states, real upload/progress/preview/delete/crop lifecycle, `200%` text resize, text-spacing, contrast, and target-size acceptance remain `OWNER_RUNTIME_REQUIRED`.