# SRWF Registration — Implementation Map

Status: **DESKTOP_FULL_WIDTH_SHELL_STATICALLY_IMPLEMENTED / OWNER_RUNTIME_REQUALIFICATION_REQUIRED**

This map distinguishes current Owner authority, repository/static evidence, host ownership, and evidence that still requires the real Owner WordPress/browser runtime. CI/static success is not production visual qualification.

Evidence vocabulary: `OWNER_AUTHORIZED`, `DOCUMENTED`, `SOURCE_PROVEN`, `STATICALLY_PROVEN`, `HISTORICAL_OWNER_RUNTIME_PROVEN`, `OWNER_RUNTIME_PROVEN`, `OWNER_RUNTIME_REQUIRED`, `HOST_OWNED`, `HOST_INTEGRATION_REQUIRED`, `NOT_PROVEN`.

## Authority inputs

Registered immutable/exact IDs remain defined in `reference/VISUAL_AUTHORITY.md`:

- `VA:ARTIFACT` — admitted `OWNER_REFERENCE_new_7.html`, exact SHA-256 registered there;
- `VA:VC-1.0.0` — historical/base contract;
- `VA:VC-1.0.1` — exact historical Drive-backed Owner revision, including §27.

`OWNER:SRWF-2026-09-19`, recorded in `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md`, remains implementation-driving for the current destination, including the later Owner-supplied 2026-09-20 Desktop Full Width shell decision now recorded there. It supersedes only contradictory/unresolved historical states it explicitly resolves. Historical artifacts/contracts remain provenance and must not roll back newer Owner decisions.

Current static theme implementation: `0.1.18`.

Owner runtime of theme `0.1.14` is retained as historical evidence for the initial GPFUP repair: both admitted glyphs rendered, but the authentic direct content child remained visually detached from the icon. Theme `0.1.15` is the prior static icon/content-cluster repair. Theme `0.1.16` added bounded intrinsic Radio and initial GPFUP narrow/mobile reflow. Theme `0.1.17` repaired the runtime-proven Radio full-cell defect by neutralizing the Gravity Forms secondary-label horizontal reserve only inside admitted SRWF Radio groups; the Owner subsequently confirmed the repaired mobile Radio geometry/runtime. Theme `0.1.18` preserves those component rules and changes only the desktop primary form surface plus implementation-facing evidence/tests.

## Implementation traceability

| Requirement | Current destination | Mechanism / ownership | Current disposition |
|---|---|---|---|
| Theme activation | explicit SRWF opt-in; unrelated forms untouched | stored form class establishes identity; rendering context separately gates admission | `STATICALLY_PROVEN`; exact-head browser `OWNER_RUNTIME_REQUIRED` |
| Gravity Flow Entry Detail | excluded even for same stored form | retained source-proven early enqueue + content bracket admission boundary | regression-tested; fresh Owner runtime `OWNER_RUNTIME_REQUIRED` |
| Per-form setup | Gravity Forms → Form Settings → GTB Theme | supported Form Settings hooks; no top-level menu | `STATICALLY_PROVEN` |
| Semantic mapping | explicit internal references project GTB-owned specialization tokens | no label/ID/order/DOM inference; semantic roles do not gate all-Radio cards | `STATICALLY_PROVEN` |
| Production breakpoint | `960 CSS px` | one viewport media query; not a device-name preset | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime matrix `OWNER_RUNTIME_REQUIRED` |
| Mobile shell | fluid; `16px` inline padding; hard acceptance `320 CSS px`; no desktop block padding/shadow requirement | SRWF wrapper only; no mobile max-width | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; prior `390 CSS px` width chain `OWNER_RUNTIME_PROVEN`; exact 0.1.18 regression `OWNER_RUNTIME_REQUIRED` |
| Desktop primary surface | white; `840px` content + `32px` + `32px` = `904px` outer; `32px` block padding; radius `16px`; subtle `#E4E7EC` boundary; restrained depth | existing border-box wrapper at `min-width:960px`; boundary is a non-layout `0 0 0 1px` shadow ring plus approved depth, so no inline border consumes the 840px content box | `OWNER_AUTHORIZED / STATICALLY_PROVEN`; real browser/computed/visual acceptance `OWNER_RUNTIME_REQUIRED` |
| Section hierarchy | one primary form surface; authentic Section Breaks remain separators; major rhythm `32px` | existing `--gf-form-gap-y:24px` plus Section `margin-block-start:8px`; no section wrappers/cards or DOM-position selectors added | `OWNER_AUTHORIZED / STATICALLY_PROVEN`; visual hierarchy `OWNER_RUNTIME_REQUIRED` |
| Page / host width | page hosting Registration must provide the required full-width content area; GTB then owns its canonical mobile gutter and bounded desktop surface | host/page configuration; GeneratePress native Full Width is the currently proven Owner-site example, not a GTB dependency | `HOST_OWNED`; intended width chain historically `OWNER_RUNTIME_PROVEN`; no GTB host-layout override required or desired |
| Page canvas | preferred desktop `#F6F8FB` only where an authenticated page-shell ownership seam exists | no truthful durable page-level SRWF seam was found in current GTB; surrounding page remains host-owned | `HOST_INTEGRATION_REQUIRED`; GTB does not seize `html/body/.site-content/.content-area/.site-main` or GeneratePress internals |
| Form title | mobile `24px`, desktop `26px`, `700 / 1.5` | bounded framework-sentinel selector | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Section title | `18px / 700 / 1.5` | authentic Section Break title | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Field label | `15px / 600 / 1.5` | Gravity Forms Theme Framework API | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Control value | `16px / 400 / 1.5`, min `52px` | Theme Framework `--gf-ctrl-*` tokens | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Helper | `14px / 400 / 1.5` | Gravity Forms description CSS API | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Field error | `14px / 600 / 1.5` | Gravity Forms error-description API | `DOCUMENTED / STATICALLY_IMPLEMENTED`; authentic invalid submission pending |
| Primary action | `16px / 700 / 1.5`, full available width, min `56px` | Theme Framework tokens + bounded SRWF width enforcement | `STATICALLY_PROVEN`; exact 0.1.18 browser recheck `OWNER_RUNTIME_REQUIRED` |
| Field-internal spacing | no-helper label→control `8px`; label→helper/error `6px`; final helper/error→control `8px`; intermediate helper/error spacing remains content/host-driven | `--gf-label-space-primary:8px`, `--gf-desc-space:8px`, bounded `--gf-label-space-primary:6px` for authentic above-input consumers | `OWNER_AUTHORIZED / STATICALLY_PROVEN`; computed browser geometry `OWNER_RUNTIME_REQUIRED` |
| Visible focus | `2px solid #1D4ED8`, offset `2px`, no intended glow | GF focus API; hidden native Radio focus projects to visible card; desktop wrapper deliberately does not use `overflow:hidden` | `DOCUMENTED / STATICALLY_IMPLEMENTED`; authentic keyboard runtime pending |
| Native single Select | shared control family + documented `--gf-ctrl-select-padding-x:24px 32px`; retained runtime-proven vertical optical compensation | bounded native-only selector excludes enhanced Tom Select source | unchanged; exact-head browser recheck `OWNER_RUNTIME_REQUIRED` |
| All Radio choices | every authentic admitted `.gfield--type-radio` uses cards; visible label fills assigned `.gchoice`; `12px` option gap; min `52px`; radius `10px`; unselected `1px #8690A1`; selected `2px #1D4ED8` + `#EDF1FC` + non-color dot cue | `.gfield_radio` keeps intrinsic Flex wrapping; `--gf-label-space-x-secondary:0`; `.gchoice` retains `flex:1 1 9.5rem`; native input/label/checked/focus semantics retained | root cause `OWNER_RUNTIME_PROVEN`; 0.1.17 repair `OWNER_RUNTIME_PROVEN` at mobile; 0.1.18 regression `OWNER_RUNTIME_REQUIRED` |
| Conditional Radio fields | inherit same cards when Gravity Forms reveals them | same field-type rule; GTB does not control conditional visibility | selector coverage `STATICALLY_PROVEN`; authentic reveal runtime pending |
| Section icon tiles | explicit mapped section roles only; `40×40`, radius `10`, icon `20`, tint `#EDF1FC`, heading gap `12px` | admitted local SVGs | unchanged; `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED` |
| Shared initial GPFUP family | min `96px`; pad `16px`; radius `12px`; `1px` dashed `#8690A1`; `40×40` icon slot; `24px` glyph | authentic initial state only; direct child intrinsic `13rem` basis + `max-inline-size:100%` | unchanged; exact 0.1.18 regression `OWNER_RUNTIME_REQUIRED` |
| Report Card initial GPFUP | shared family + file/document glyph | explicit `srwf-role-report-card-upload`; `icons/report-card-file.svg`; only `:not(.gpfup--has-files)` | unchanged; runtime recheck pending |
| Report Card `.gpfup--has-files` | do not force initial state over uploaded UI | all theme upload rules stop before authentic has-files state | `HOST_OWNED`; real transition `OWNER_RUNTIME_REQUIRED` |
| Student Photo initial | shared initial family + photo/camera glyph | authentic `gpfup--images-only:not(.gpfup--has-files)`; `icons/student-photo-upload.svg` | unchanged; runtime recheck pending |
| Student Photo post-upload | style only authentic exposed preview/replace/re-crop/delete states | no speculative post-upload/crop composition; crop config host-owned | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`; `HOST_OWNED` |
| GPAS / Tom Select | same select-family metric/focus, host owns behavior | proven `.ts-wrapper > .ts-control`; wrapper does not clip dropdowns | unchanged; behavior `HOST_OWNED`; exact 0.1.18 dynamic runtime regression `OWNER_RUNTIME_REQUIRED` |
| PersianGravity / Jalali | style only authentic consumer if admitted | no selector/adapter invented | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN` |
| Desktop short-field pairings | Gravity Forms configuration remains authoritative | no GTB pair map | `HOST_OWNED / OWNER_CONFIGURABLE` |
| Accessibility / reflow | `320px`, `200%` text resize, text spacing, contrast, target/focus acceptance | intrinsic wrapping + host responsive mechanics | `OWNER_RUNTIME_REQUIRED` |

## Desktop shell implementation decision

The current wrapper is already `box-sizing:border-box`, `max-inline-size:904px`, and uses `32px` inline padding at the admitted desktop threshold. A literal `1px` left/right border would consume two pixels from the content box and change the authorized `840px` content geometry to `838px`.

Theme `0.1.18` therefore keeps the existing shell and adds only:

```text
padding-block: 32px
boundary ring: 0 0 0 1px #E4E7EC
shadow 1: 0 1px 2px rgba(16, 24, 40, 0.04)
shadow 2: 0 12px 32px rgba(16, 24, 40, 0.06)
```

The ring is visual rather than layout-affecting. The static geometry remains `904 - 32 - 32 = 840`. No `border` and no `overflow:hidden` are added to the primary wrapper, avoiding deliberate clipping of focus rings, Tom Select dropdowns, GPFUP states, or validation consumers.

No additional Section spacing was added: the current Gravity Forms vertical grid gap (`24px`) plus the authentic Section Break's existing `8px` block-start margin already yields the authorized `32px` major section rhythm. This remains content/Section-type driven and tolerant of added, removed, or reordered Section Breaks.

## Host-width and canvas ownership boundary

The earlier narrow whole-form observation was resolved operationally by the Owner-site page layout. GeneratePress Full Width is the currently proven Owner-site configuration, but it is not a GTB dependency or selector contract.

Fresh historical Owner runtime at `390 CSS px` established the intended chain:

- viewport/client width `390px`;
- host full-width content provides the full page width;
- SRWF wrapper `390px` with `16px` inline padding;
- actual form/ordinary controls/Submit `358px` (`390 - 16 - 16`);
- no document horizontal scrolling in that capture.

Implementation prerequisite:

> The page hosting the SRWF Registration surface must provide the required full-width content area. GTB owns only its scoped Registration presentation; the preferred desktop `#F6F8FB` surrounding canvas remains host configuration unless a future authenticated GTB page-shell seam is proven.

Current source inspection found no durable page-level seam that authenticates the admitted SRWF Registration page independently of numeric IDs, text, DOM position, or GeneratePress internals. GTB therefore does **not** target generic `html`, `body`, `.site-content`, `.content-area`, `.site-main`, `.inside-article`, `.entry-content`, page IDs, negative margins, or `100vw` breakouts. The safe form-local shell is complete without that page takeover.

Diagnostic package v0.3.6 remains sufficient for requalification. It already records `window.innerWidth`, `devicePixelRatio`, the wrapper width/max-width/padding chain, bounded ancestors, representative controls, overflow evidence, Radio geometry, upload-family evidence, and current admission state. No diagnostic schema/source changed in this batch.

## Radio full-cell historical repair

Owner runtime after host-width correction isolated a repeatable `12px` label-width deficit. Gravity Forms' documented `--gf-label-space-x-secondary` reserve remained active even though SRWF moves the authentic Radio input out of flow and draws its visible cue inside the label. Theme `0.1.17` neutralized only that reserve with `--gf-label-space-x-secondary:0`; it did not add width compensation, change the explicit `12px` option gap, change the `9.5rem` intrinsic basis, or replace native Radio semantics.

The Owner subsequently confirmed the repaired mobile Radio presentation/runtime. Theme `0.1.18` does not modify the Radio selectors or behavior; it requires regression requalification only because a new installable package is produced.

## Visual-role authority traceability

The exact historical v1.0.1/artifact path remains retrievable. The current Owner reconciliation supersedes only the presentation interpretations it explicitly resolves.

| Requirement | Authority path | Implementation | Current disposition |
|---|---|---|---|
| Gender historical binary role | `VA:VC-1.0.1` + `VA:ARTIFACT` + current Owner reconciliation | `srwf-role-binary-choice` may remain configured, but card presentation comes from authentic Radio field type | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; 0.1.18 regression pending |
| Graduation Status historical binary role | current all-radio lock | semantic role no longer gates cards; conditional visibility stays host-owned | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; 0.1.18 regression pending |
| Other authentic Radio groups | current Owner all-radio lock | same `.gfield--type-radio` card system automatically covers visible/conditional groups | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; 0.1.18 regression pending |
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

`Check Again` remains read-only. **Apply Recommended SRWF Form Layout** remains the separate capability + nonce protected action through `GFAPI::update_form()`. Gravity Forms retains validation/ARIA/rerender lifecycle ownership.

## Package / verification boundary

Theme package: `0.1.18`.
Diagnostic package: `0.3.6`.

The deterministic/static suite is expected to prove at minimum:

- exact historical visual-reference hash remains unchanged;
- only the admitted `960px` viewport threshold exists in production CSS;
- mobile wrapper remains `16px` inline padding with no desktop block padding leaking below `960px`;
- desktop wrapper stays `904px` max with `32px` inline padding and therefore a static `840px` content geometry target;
- desktop block padding is `32px`;
- white surface and `16px` radius remain;
- `#E4E7EC` boundary is non-layout-affecting and the two approved depth layers exist;
- no literal wrapper border, `overflow:hidden`, generic page/body/site takeover, GeneratePress dependency, numeric styling ID, `nth-child`, label/option-text identity, device-specific breakpoint matrix, or Section-card-by-position implementation is introduced;
- PR #26 Radio full-cell rules/native semantics, GPFUP initial-state isolation, GPAS/Tom Select adapter, Submit full width, Entry Detail exclusion, unrelated-form isolation, package/version coherence, and diagnostic privacy contracts remain intact;
- deterministic Owner package build/smoke succeeds.

These checks do **not** establish browser rendering. Exact-head Owner requalification remains required at desktop `960`, `1024`, representative `1366`/`1440`, and a wide desktop near the prior `~1859 CSS px` baseline where practical, plus responsive regression at `320 / 360 / 390 / 393 / 412 / 430 CSS px`.

Browser acceptance must also exercise, where practical, keyboard `:focus-visible`, authentic invalid submission, GPAS open state, GPFUP post-upload state, and conditional reveal. No production state is synthesized merely for testing. Visual acceptance of the preferred `#F6F8FB` canvas additionally requires the Owner/host page configuration because GTB intentionally does not own that surrounding page shell.
