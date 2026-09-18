# SRWF Registration — Implementation Map

Status: **FIRST_IMPLEMENTATION / VISUAL_UX_V1.0.1_REGISTERED / SEMANTIC_VISUAL_ROLES_STATICALLY_PROVEN / OWNER_RUNTIME_RECHECK_REQUIRED**

This map is the traceability layer between the admitted SRWF visual authority and the production files in `src/`. It is intentionally limited to implementation-driving requirements.

Evidence labels used here: `OWNER_APPROVED`, `DOCUMENTED`, `STATICALLY_PROVEN`, `RUNTIME_PROVEN`, `RUNTIME_REQUIRED`, `NOT_PROVEN`, `NON_NORMATIVE_REFERENCE`.

## Visual authority for the current batch

Registered visual-authority IDs are defined only in `reference/VISUAL_AUTHORITY.md`:

- `VA:ARTIFACT` — admitted `OWNER_REFERENCE_new_7.html`, exact SHA-256 registered there;
- `VA:VC-1.0.0` — historical/base Visual/UX Contract source;
- `VA:VC-1.0.1` — current exact Owner revision, including §27 Owner resolution addendum dated 2026-09-18.

The implementation uses `VA:VC-1.0.1` for canonical rules and explicit resolution states. `VA:ARTIFACT` supplies composition/state and exact SVG geometry where §27 makes an artifact fragment implementation-driving. Gravity Forms and add-ons remain the behavioral owners. No authority ID may be introduced in this map without registration in `reference/VISUAL_AUTHORITY.md`.

| Requirement | Approved value/state | Authority locator | Responsibility class | Intended host mechanism | Mechanism evidence | Implementation disposition | Runtime inspection required | Fallback | Implementation locator |
|---|---|---|---|---|---|---|---|---|---|
| Theme activation boundary | Explicit opt-in; unrelated forms must remain untouched | Charter §9; Theme Authoring Contract §7 | isolation / activation | Gravity Forms Form Settings → CSS Class Name + `gform_form_theme_slug` + `gform_enqueue_scripts` | `DOCUMENTED` | `IMPLEMENT` | yes — final lifecycle/cascade on supported runtime | none; fail closed when class is absent | `src/srwf-registration-theme.php`; `.srwf-registration-theme_wrapper` |
| Theme Framework base | Use Gravity Forms Theme Framework; Orbital is current implementation | Canonical GF reference §§1–3 | host integration | force `orbital` only for opted-in form | `DOCUMENTED` | `IMPLEMENT` | yes — confirm emitted framework wrapper/classes | no legacy fallback | `src/srwf-registration-theme.php` |
| Persian composition | RTL | `VA:VC-1.0.1` §10 | directionality | theme-scoped CSS `direction: rtl` | `OWNER_APPROVED`; CSS mechanism `DOCUMENTED` | `IMPLEMENT` | yes — real fields and reading order | preserve host semantics | root scope in `srwf-registration.css` |
| Inherently LTR numeric/phone values | LTR where semantics require it | `VA:VC-1.0.1` §10 | directionality | semantic input types/inputmode; optional field CSS class `srwf-ltr-value` | consumer coverage `RUNTIME_REQUIRED` | `IMPLEMENT` for generic semantics | yes — National ID/Jalali/add-on controls | narrow field class after runtime inspection | final rule in `srwf-registration.css` |
| Font family target | `Vazirmatn`; delivery remains host-owned | `VA:VC-1.0.1` §9 | typography | `--gf-font-family-base` + direct family projection to runtime-proven title/section consumers | CSS API `DOCUMENTED`; consumers runtime-observed | `IMPLEMENTED_STATIC_ONLY`; delivery `HOST_OWNED` | yes | system fallback only | root scope + `.gform_title` + `.gsection_title` |
| Primary color | `#1D4ED8` | `VA:VC-1.0.1` §8 | color | `--gf-color-primary` + RGB representation | `DOCUMENTED` | `IMPLEMENT` | yes | none | root scope |
| Pressed primary action | `#1E40AF` | `VA:VC-1.0.1` §8 | state / color | primary button hover mapping through CSS API | `DOCUMENTED` | `IMPLEMENT` | yes | host behavior | root scope |
| Error semantic color | `#B42318` | `VA:VC-1.0.1` §§8,15 | state / color | danger/error CSS APIs | `DOCUMENTED` | `IMPLEMENT` | yes | no custom validation lifecycle | root scope |
| Success semantic color | `#18794E` | `VA:VC-1.0.1` §8 | state / color | `--gf-color-success` | `DOCUMENTED` | `IMPLEMENT` | yes | host defaults if not consumed | root scope |
| Control fill/text/border/radius | white / `#172033` / `#8690A1` / `10px` | `VA:VC-1.0.1` §§8,13,16 | control | documented control CSS API | `DOCUMENTED` | `IMPLEMENT` | yes | scoped direct CSS only after proven gap | root scope |
| Control minimum sizing intent | `52px` minimum | `VA:VC-1.0.1` §§8,13 | control sizing | `--gf-ctrl-size` | `DOCUMENTED`; Tom Select consumer separately runtime-proven | `IMPLEMENT` | yes — text enlargement/content clipping | narrower min-size adapter only after proven need | root scope + Tom Select adapter |
| Field label typography | `15px / 600` | `VA:VC-1.0.1` §9 | typography | primary label CSS API | `DOCUMENTED` | `IMPLEMENT` | yes | scoped direct CSS only after proven gap | root scope |
| Control value typography | `16px / 400` | `VA:VC-1.0.1` §9 | typography | control CSS API | `DOCUMENTED` | `IMPLEMENT` | yes | none | root scope |
| Section heading typography | `Vazirmatn / 18px / 700` | `VA:VC-1.0.1` §9 | typography / section | authentic Section Break heading + direct family/size/weight projection | consumer runtime-observed | `IMPLEMENTED_STATIC_ONLY` | yes | no guessed alternate primitive | `.gfield--type-section .gsection_title` |
| Decorative divider color | `#E4E7EC` | `VA:VC-1.0.1` §§8,12 | section / divider | `--gf-field-section-border-color` | `DOCUMENTED` | `IMPLEMENT` | yes | no invented divider width/rhythm | root scope |
| Helper text color/placement | muted `#667085`, below input; exact size unresolved | `VA:VC-1.0.1` §§7,8,13,14 | help / typography | description color API + GF Description Placement | `DOCUMENTED` | color `IMPLEMENT`; placement `HOST_OWNED`; size `DEFER_NOT_PROVEN` | yes | no DOM reordering | root scope + form setting |
| Field error placement | below input; exact size unresolved | `VA:VC-1.0.1` §§7,13,15 | validation / state | GF Validation Message Placement + danger APIs | `DOCUMENTED` | appearance `IMPLEMENT`; placement `HOST_OWNED`; size `DEFER_NOT_PROVEN` | yes | no shadow validation | root scope + form setting |
| Validation summary | authentic GF summary; SRWF danger language | `VA:VC-1.0.1` §§13,15 | validation / state | GF validation summary + danger API | `DOCUMENTED` | semantic color `IMPLEMENT`; lifecycle `HOST_OWNED` | yes | preserve host summary | root scope |
| Visible keyboard focus | primary color basis; exact ring geometry/alpha unresolved | `VA:VC-1.0.1` §§7,8,20,27 | focus | host focus + approved color basis | `DOCUMENTED`; exact geometry `NOT_PROVEN` | `DEFER_NOT_PROVEN` for custom ring | yes | preserve visible host/UA focus | no custom global ring |
| Primary action | full-width, blue, 56px minimum, `16px / 700` | `VA:VC-1.0.1` §§8,9,13 + `VA:ARTIFACT` | action / control | button CSS API + real `<button.gform_button>` + sentinel-scoped width repair | Submit conflict and final repair `RUNTIME_PROVEN` by Owner after PR #9 | `RUNTIME_PROVEN` | regression recheck for this artifact | no IDs/JS/`!important` | button properties + sentinel footer rule |
| School selector / GP Advanced Select | ordinary-control visual family, minimum ~52px | `VA:VC-1.0.1` §§13,18,22 | add-on integration | runtime-proven `.ts-wrapper > .ts-control`; scoped min-size adapter | repaired consumer `RUNTIME_PROVEN` by Owner after PR #9 | `RUNTIME_PROVEN` | regression recheck for this artifact | no behavior JS | `.ts-wrapper .ts-control` |
| Gender binary card role | two equal-width approved card choices; native radio owns state | `VA:VC-1.0.1` §27 `gender_binary_choice` + `VA:ARTIFACT` | choice presentation | GF field Custom CSS Class `srwf-role-binary-choice`; style real `.gfield_radio`, `.gchoice`, native radio + label | mechanism `DOCUMENTED`; production selector/tests `STATICALLY_PROVEN` | `IMPLEMENTED_STATIC_ONLY` | yes — semantic class must be configured and real click/keyboard checked | native ordinary radio when class absent | `.srwf-role-binary-choice` rules |
| Graduation Status binary card role | same approved two-card family when GF reveals field | `VA:VC-1.0.1` §27 `graduation_status_binary_choice` + `VA:ARTIFACT` | conditional choice presentation | same `srwf-role-binary-choice`; no display/visibility ownership | authentic field existence runtime-proven; CSS/tests `STATICALLY_PROVEN` | `IMPLEMENTED_STATIC_ONLY` | yes — configure class and exercise authentic conditional reveal | GF retains conditional logic and ordinary radio fallback | `.srwf-role-binary-choice` rules |
| Section iconography | exact admitted icon geometry only on explicit mapped Section Break roles | `VA:VC-1.0.1` §27 `section_heading_iconography` + `VA:ARTIFACT` | decorative section presentation | one semantic CSS class per mapped Section Break + local SVG assets | mapping and SVG geometry mechanically trace to artifact; selectors `STATICALLY_PROVEN` | `IMPLEMENTED_STATIC_ONLY` | yes — configure classes and verify authentic Section Break consumers | no icon when role absent | `src/icons/section-*.svg`; mapped selectors |
| Report Card initial GPFUP | compact dashed initial surface, exact file icon, persistent host rules | `VA:VC-1.0.1` §27 `report_card_upload_initial` + `VA:ARTIFACT` | add-on presentation | GF field Custom CSS Class `srwf-role-report-card-upload` + authentic `.gpfup` consumer; initial-state guard `:not(.gpfup--has-files)` | GPFUP consumer `RUNTIME_PROVEN`; new presentation `STATICALLY_PROVEN` | `IMPLEMENTED_STATIC_ONLY` | yes — configure role and inspect empty state | host-native GPFUP when role absent | `.srwf-role-report-card-upload` rules + `report-card-file.svg` |
| Report Card `.gpfup--has-files` | preserve authentic uploaded row/info/delete rather than inventing a replacement state | `VA:VC-1.0.1` §§19,27 host-owned GPFUP lifecycle + Owner runtime host-state evidence | regression preservation | initial styling stops at authentic `.gpfup--has-files`; no `.gpfup__files`/`.gpfup__delete` production styling | `AUTHENTIC_RUNTIME_PROVEN_HOST_STATE`; preservation tests `STATICALLY_PROVEN` | `REGRESSION_TARGET` | yes — upload/delete recheck | host-native uploaded state | state-aware Report Card selectors |
| Student Photo post-upload | approved destination exists, but authentic post-upload consumer structure is not captured | `VA:VC-1.0.1` §27 `student_photo_uploaded_state` + `VA:ARTIFACT` | add-on presentation boundary | none until authentic post-upload GPFUP DOM is captured | `RUNTIME_REQUIRED`; exact crop ratio/dimensions remain runtime/configuration evidence | `NOT_IMPLEMENTED` | yes | preserve host-native photo behavior | no production post-upload selector |
| PersianGravity Jalali date | integrate authentic runtime control; picker UI not proven | `VA:VC-1.0.1` §§13,22 | custom-field integration | inspect real consumer first | `RUNTIME_REQUIRED` | `RUNTIME_REQUIRED` | yes | no speculative selectors | none |
| Form max width | `840px` | `VA:VC-1.0.1` §§8,11,17 | layout | intrinsic `max-inline-size` on activation wrapper | CSS mechanism stable; Owner target runtime observed | `IMPLEMENT` | regression recheck | none | root scope |
| Mobile horizontal padding | `16px` | `VA:VC-1.0.1` §§8,11 | responsive / shell | needs resolved host/breakpoint ownership | value `OWNER_APPROVED`; production breakpoint `NOT_PROVEN` | `DEFER_NOT_PROVEN` | yes | host shell may temporarily own | none |
| Desktop white-card surface | white / radius `16px`; exact shadow unresolved | `VA:VC-1.0.1` §§5,8,11,17 | responsive / surface | no stable semantic desktop/card activation boundary yet | visual values `OWNER_APPROVED`; activation threshold `NOT_PROVEN` | `BLOCKED_NOT_PROVEN` | yes | do not apply globally | none |
| Page background | `#F6F8FB` | `VA:VC-1.0.1` §§8,17 | surrounding surface | current theme scope ends at GF wrapper | `OWNER_APPROVED`; ownership boundary unresolved | `HOST_INTEGRATION_REQUIRED` | yes | no global `body`/`html` styling | none |
| Production breakpoint | `NOT_PROVEN` | `VA:VC-1.0.1` §§11,22,27 | responsive | none authorized | `NOT_PROVEN` | `DEFER_NOT_PROVEN` | yes | intrinsic layout only | no `@media` |
| Desktop short-field pairings | target pairing set `NOT_PROVEN` | `VA:VC-1.0.1` §§7,11,27 | responsive / layout | no inferred production mapping | current runtime layout != design authority | `BLOCKED_NOT_PROVEN` | yes | preserve host layout | none |
| Desktop shadow | exact value `NOT_PROVEN` | `VA:VC-1.0.1` §§7,11,17,27 | surface / optical | none | `NOT_PROVEN` | `DEFER_NOT_PROVEN` | yes | no shadow declaration | none |
| Form title size/line-height and desktop enhancement | `NON_NORMATIVE_REFERENCE` | `VA:VC-1.0.1` §§7,9,27 | typography | none authorized | `NON_NORMATIVE_REFERENCE` | `DEFER_NOT_PROVEN` | no until resolved | inherit host/site | none |
| Field/section rhythm | `NON_NORMATIVE_REFERENCE` | `VA:VC-1.0.1` §§7,12,27 | spacing | no exact production values authorized | `NON_NORMATIVE_REFERENCE` | `DEFER_NOT_PROVEN` | no until resolved | retain Foundation layout | no `--gf-form-gap-y` override |

## Exact section/icon mapping

Authority for requiring the mapped icon tiles is `VA:VC-1.0.1` §27; authority for the exact SVG geometry and section-to-icon mapping is `VA:ARTIFACT`.

| Semantic section role | Approved section | Exact admitted icon | Local asset |
|---|---|---|---|
| `srwf-role-section-identity` | هویت دانش‌آموز | person: circle head + shoulder path | `src/icons/section-identity.svg` |
| `srwf-role-section-contact` | اطلاعات تماس | phone/device rectangle + bottom point | `src/icons/section-contact.svg` |
| `srwf-role-section-education` | تحصیلات | graduation cap | `src/icons/section-education.svg` |
| `srwf-role-section-school-documents` | مدرسه و مدارک | school/building | `src/icons/section-school-documents.svg` |
| `srwf-role-section-student-photo` | عکس دانش‌آموز | camera | `src/icons/section-student-photo.svg` |

The local SVG child geometry is required to match the exact SVG child geometry in `VA:ARTIFACT`; the deterministic authority test performs that comparison. The authentic Gravity Forms Section Break heading remains the accessible text source.

## Semantic role configuration

These are presentation roles, not schema identifiers. Configure them in Gravity Forms on the corresponding real fields/Section Breaks using the field **Custom CSS Class** setting:

- Gender: `srwf-role-binary-choice`
- Graduation Status: `srwf-role-binary-choice`
- Report Card upload: `srwf-role-report-card-upload`
- Identity Section Break: `srwf-role-section-identity`
- Contact Section Break: `srwf-role-section-contact`
- Education Section Break: `srwf-role-section-education`
- School/Documents Section Break: `srwf-role-section-school-documents`
- Student Photo Section Break: `srwf-role-section-student-photo`

No numeric Form ID or Field ID is part of the durable presentation contract. No label text, substring, DOM position, `nth-child`, generic radio type, or generic GPFUP type is used to infer these roles. If a role class is absent, the associated custom presentation fails closed and Gravity Forms/add-on presentation remains authoritative.

Current Owner runtime evidence did not yet contain these new role classes, therefore the newly implemented roles remain `STATICALLY_PROVEN` + `RUNTIME_REQUIRED` until the one-time GF configuration is applied and observed.

## Runtime evidence chronology

Owner diagnostic v0.2.5 established the authentic opted-in wrapper, Reset → Foundation → Framework → Orbital → GTB order, authentic native radio fields, Graduation Status as a real two-option conditional field, Tom Select, and the real initial GPFUP/photo consumers including `.gpfup`, `.gpfup--strict`, `.gpfup__droparea`, `.gpfup__select-files`, and the Student Photo `.gpfup--images-only` state. Separately, Owner runtime evidence supplied for this batch establishes the Report Card uploaded host state `.gpfup--has-files` with `.gpfup__files`, `.gpfup__droparea`, `.gpfup__delete`, and `.gpfup__select-files`.

The v0.2.5 diagnostic originally exposed the 115px Submit and ~39.5px Tom Select gaps. The subsequent PR #9 repair was Owner-verified in the authentic runtime: Submit became approximately `840×56` and the visible Tom Select control approximately `840×52`. This batch preserves those repairs and does not reopen their implementation strategy.

The runtime evidence still does **not** resolve the production breakpoint, desktop short-field pairing target, desktop shadow, title metrics, field/section rhythm, exact focus-ring geometry/alpha, helper/error exact sizing, page-shell ownership, PersianGravity picker presentation, or Student Photo post-upload/crop DOM. Those remain explicitly unresolved under `VA:VC-1.0.1`.

## Activation contract

1. Install/activate the complete theme-local `src/` tree: plugin PHP, adjacent stylesheet, and `icons/` assets referenced by that stylesheet.
2. On the intended SRWF Gravity Form only, set **Form Settings → Form Layout → CSS Class Name** to `srwf-registration-theme`.
3. Configure the eight semantic field/section role classes listed above in the applicable real Gravity Forms field **Custom CSS Class** settings.
4. Keep Gravity Forms as behavioral owner. Configure authentic Description Placement and Validation Message Placement below inputs and enable Validation Summary according to `VA:VC-1.0.1`; this theme does not reorder or synthesize those states.
5. The plugin selects Orbital only for the opted-in form and enqueues the SRWF stylesheet only while that form is being enqueued.
6. Vazirmatn delivery remains host-owned; this package names the font but does not fetch it remotely.
7. Student Photo post-upload remains `RUNTIME_REQUIRED / NOT_IMPLEMENTED`; do not add assumed crop/preview/delete classes to production CSS.

`STATICALLY_PROVEN` in this repository does not mean `RUNTIME_PROVEN` in WordPress/Gravity Forms.
