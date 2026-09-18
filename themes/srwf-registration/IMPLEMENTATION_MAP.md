# SRWF Registration — Implementation Map

Status: **AUTHORITY_RECONCILED / PER_FORM_CONFIGURATION_FOUNDATION / CURRENT_PRESENTATION_PRESERVED / OWNER_RUNTIME_RECHECK_REQUIRED**

This map traces current SRWF destination authority to the current production implementation. It deliberately distinguishes **authorized destination** from **implemented/runtime-proven behavior**.

Evidence labels used here: `OWNER_AUTHORIZED`, `DOCUMENTED`, `SOURCE_PROVEN`, `STATICALLY_PROVEN`, `OWNER_RUNTIME_PROVEN`, `OWNER_RUNTIME_REQUIRED`, `NOT_PROVEN`, `HOST_OWNED`, `NEXT_VISUAL_BATCH`.

## Authority inputs

Registered immutable/exact IDs are defined in `reference/VISUAL_AUTHORITY.md`:

- `VA:ARTIFACT` — admitted `OWNER_REFERENCE_new_7.html`, exact SHA-256 registered there;
- `VA:VC-1.0.0` — historical/base contract;
- `VA:VC-1.0.1` — exact historical Drive-backed Owner revision, including §27.

Current Owner-supplied project authority for the newly resolved destination is `OWNER:SRWF-2026-09-19`, recorded in `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md`. No immutable upstream Drive revision/hash is claimed for that newer authority input.

`VA:VC-1.0.1` remains valid historical/inherited authority where it is not superseded. `OWNER:SRWF-2026-09-19` governs the explicitly reconciled breakpoint, layout ownership, desktop card, title/helper/error/rhythm/focus, placement, required indication, binary dimensions/tint, section tile dimensions, upload dimensions, and accessibility acceptance.

### Historical resolution-state preservation

The exact v1.0.1 predecessor intentionally preserves earlier resolution labels such as `NOT_PROVEN`, `NON_NORMATIVE_REFERENCE`, `DEFER_NOT_PROVEN`, and `RUNTIME_REQUIRED`. They remain provenance/history, not current destination truth where `OWNER:SRWF-2026-09-19` explicitly resolves the question. In particular, the historical **Desktop short-field pairings** and **Desktop shadow** states are now superseded by the Owner-authorized host-owned pairing rule and no-shadow card destination. This distinction prevents future work from treating old unresolved markers as current while preserving why earlier implementation intentionally deferred them.

## Implementation traceability

| Requirement | Current destination | Authority locator | Mechanism / ownership | Current disposition |
|---|---|---|---|---|
| Theme activation boundary | Explicit opt-in; unrelated forms untouched | Charter §9; Theme Authoring Contract §7 | form `cssClass` identity + rendering-context admission | `STATICALLY_PROVEN`; runtime history exists |
| Per-form setup surface | Gravity Forms → Form Settings → GTB Theme; no top-level GTB menu | official Gravity Forms Form Settings hooks + current Owner requirement | `gform_form_settings_menu` + `gform_form_settings_page_gtb_theme` | `IMPLEMENTED`; exact branch `OWNER_RUNTIME_REQUIRED` |
| Configuration persistence | Activation + semantic mappings stored with the Form Object | current Owner requirement | one validated `GFAPI::update_form()` mutation | `STATICALLY_PROVEN`; historical prior-candidate Owner runtime proof |
| Mutation/read-only split | Save mutates; Check Again and ordinary render do not | current Owner requirement | explicit POST+nonce Save; read-only GET check | `STATICALLY_PROVEN` |
| Permission handling | legitimate Gravity Forms form editors admitted | Gravity Forms permission API | `GFAPI::current_user_can_any('gravityforms_edit_forms')`, WP fallback only if API unavailable | `DOCUMENTED`/`STATICALLY_PROVEN`; exact branch runtime recheck required |
| Semantic identity | explicit per-form role mapping; IDs internal only | `OWNER:SRWF-2026-09-19` | stored field references project GTB-owned class tokens | `STATICALLY_PROVEN` |
| Projection safety | preserve unrelated Custom CSS Class tokens; remove stale GTB-owned tokens; idempotent | current Owner requirement | clone/build intended form, full validation, one update | `STATICALLY_PROVEN` |
| Entry Detail isolation | same target form excluded on Gravity Flow Entry Detail | merged PR #13/#15 source/runtime evidence | existing request-local content + early enqueue classification | current-main behavior preserved; regression tests retained |
| Theme Framework base | Orbital only for admitted Registration render | canonical GF reference | `gform_form_theme_slug` + `gform_enqueue_scripts` | current-main implementation preserved |
| Persian composition | RTL | `VA:VC-1.0.1` §10 | bounded theme CSS | implemented; runtime recheck as needed |
| Font family target | Vazirmatn, delivery host-owned | `OWNER:SRWF-2026-09-19` | current CSS names family; environment delivers font | partially implemented; delivery `HOST_OWNED` |
| Field label typography | `15px / 600` | `OWNER:SRWF-2026-09-19` | Gravity Forms Theme Framework tokens | existing implementation |
| Control value typography | `16px / 400` | `OWNER:SRWF-2026-09-19` | Gravity Forms Theme Framework tokens | existing implementation |
| Section heading typography | `18px / 700` | `OWNER:SRWF-2026-09-19` | authentic Section Break heading | existing implementation |
| Form title | mobile `24px`, desktop `26px`, `700 / 1.5` | `OWNER:SRWF-2026-09-19` | bounded theme CSS/Theme Framework consumer after implementation review | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH` |
| Helper typography | `14px / 400 / 1.5` | `OWNER:SRWF-2026-09-19` | host description consumer | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH` |
| Field error typography | `14px / 600 / 1.5` | `OWNER:SRWF-2026-09-19` | authentic Gravity Forms validation consumer | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH` |
| Helper / validation / sub-label placement | above input where Gravity Forms supports recommended accessible placement | `OWNER:SRWF-2026-09-19` | Gravity Forms form settings; no JS reordering | `HOST_OWNED CONFIGURATION / NEXT_RUNTIME_QUALIFICATION`; old below-input choice superseded |
| Required indication | native required semantics; asterisk-only preferred + short form-level explanation | `OWNER:SRWF-2026-09-19` | Gravity Forms required indicator/configuration | `HOST_OWNED CONFIGURATION / NEXT_RUNTIME_QUALIFICATION` |
| Visible keyboard focus | `:focus-visible`; `2px solid #1D4ED8`; offset `2px`; no glow/layout shift | `OWNER:SRWF-2026-09-19` | bounded focus styling without suppressing host focus | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH` |
| Field rhythm | `24px` | `OWNER:SRWF-2026-09-19` | Theme Framework/layout after cascade review | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH` |
| Major section rhythm | `32px` | `OWNER:SRWF-2026-09-19` | authentic Section Break/layout | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH` |
| Primary action | full available form width; min `56px`; `16px / 700` | `OWNER:SRWF-2026-09-19` + inherited prior evidence | real Gravity Forms submit; existing sentinel-scoped width repair | current submit repair preserved; new batch does not rewrite CSS |
| Production breakpoint | `960 CSS px` | `OWNER:SRWF-2026-09-19` | theme presentation threshold, not device preset | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH`; runtime acceptance required |
| Desktop short-field pairings | `HOST_OWNED / OWNER_CONFIGURABLE`; no GTB canonical pair list | `OWNER:SRWF-2026-09-19` | style authentic Gravity Forms layout | no inference / no production pair map |
| Desktop card | page `#F6F8FB`; surface `#FFFFFF`; content `840px`; inline pad `32px`; outer max `904px`; radius `16px`; shadow none | `OWNER:SRWF-2026-09-19` | bounded wrapper/shell integration to be implemented | `OWNER_AUTHORIZED / NEXT_VISUAL_BATCH` |
| 320px acceptance | no ordinary horizontal scroll; mobile inline pad `16px` | `OWNER:SRWF-2026-09-19` | responsive implementation + real browser qualification | `OWNER_RUNTIME_REQUIRED` |
| Accessibility acceptance | reflow, 200% text, text spacing, contrast, focus, target size, native semantics | `OWNER:SRWF-2026-09-19` | host semantics + bounded styling | `OWNER_RUNTIME_REQUIRED` |
| School selector / GP Advanced Select | appearance only; host owns search/filter/selection/keyboard/mobile/screen-reader/Populate Anything | `OWNER:SRWF-2026-09-19` | current `.ts-wrapper > .ts-control` adapter only for proven visual gap | behavior remains `HOST_OWNED` |
| PersianGravity Jalali date | integrate authentic runtime control only | inherited host boundary | inspect real consumer first | `OWNER_RUNTIME_REQUIRED`; no speculative selector |
| Page/global scope | no broad global `html`, `body`, unrestricted `.gform_wrapper` styling | Charter + authoring contract | activation/context-scoped rules only | protected by tests |

## Existing semantic visual roles preserved from v1.0.1 §27

| Requirement | Approved value/state | Authority locator | Mechanism | Current disposition |
|---|---|---|---|---|
| Gender binary card role | explicit mapped two-card role; native radio owns state; current destination adds min `52px`, `12px` gap, `#EDF1FC` tint | `VA:VC-1.0.1` §27 `gender_binary_choice` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | `srwf-role-binary-choice` projected only from explicit mapping | PR #15 row/equal-track repair preserved; remaining destination `NEXT_VISUAL_BATCH` |
| Graduation Status binary card role | same family only when explicitly mapped and host reveals field | `VA:VC-1.0.1` §27 `graduation_status_binary_choice` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | same explicit token; conditional logic host-owned | PR #15 behavior preserved |
| Section iconography | exact artifact geometry on explicitly mapped Section Break roles; tile `40×40`, radius `10`, icon `20`, tint `#EDF1FC` | `VA:VC-1.0.1` §27 `section_heading_iconography` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | mapped role token + local SVG | geometry current; new tile dimensions `NEXT_VISUAL_BATCH` |
| Report Card initial GPFUP | compact dashed initial surface; current destination min `96px`, pad `16px`, radius `12px`, border `#8690A1` | `VA:VC-1.0.1` §27 `report_card_upload_initial` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | `srwf-role-report-card-upload` + authentic GPFUP state | existing bounded adapter preserved; new exact dimensions `NEXT_VISUAL_BATCH` |
| Report Card `.gpfup--has-files` | preserve authentic uploaded row/info/delete | `VA:VC-1.0.1` §§19,27 host-owned GPFUP lifecycle | initial styling stops at authentic uploaded state | `AUTHENTIC_RUNTIME_PROVEN_HOST_STATE`; regression target |
| Student Photo post-upload | approved destination only over authentic GPFUP states; crop ratio/dimensions host-owned | `VA:VC-1.0.1` §27 `student_photo_uploaded_state` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | none until authentic state/DOM is qualified | `OWNER_RUNTIME_REQUIRED / NOT_IMPLEMENTED` |

## Exact section/icon mapping

Authority for the existing mapped icon geometry is `VA:VC-1.0.1` §27 + `VA:ARTIFACT`. Current tile dimensions come from `OWNER:SRWF-2026-09-19`.

| Semantic section role | Approved section | Local asset |
|---|---|---|
| `srwf-role-section-identity` | هویت دانش‌آموز | `src/icons/section-identity.svg` |
| `srwf-role-section-contact` | اطلاعات تماس | `src/icons/section-contact.svg` |
| `srwf-role-section-education` | تحصیلات | `src/icons/section-education.svg` |
| `srwf-role-section-school-documents` | مدرسه و مدارک | `src/icons/section-school-documents.svg` |
| `srwf-role-section-student-photo` | عکس دانش‌آموز | `src/icons/section-student-photo.svg` |

## Per-form GTB Theme configuration

Normal administration no longer requires manually maintaining GTB-owned Custom CSS Class tokens.

`Gravity Forms → Form Settings → GTB Theme` stores:

- activation (`enabled`) separately from semantic mappings;
- eight internal host-object references: Gender, Graduation Status, Report Card upload, and five Section Break roles.

Save behavior:

1. read submitted configuration;
2. validate supported profile/schema, object existence, compatible type, and distinct role references;
3. clone/build the intended form state;
4. remove only GTB-owned activation/role projection tokens;
5. add exactly the tokens required by submitted mappings while preserving unrelated classes in meaning;
6. persist configuration + projection with one `GFAPI::update_form()` call;
7. surface host failure truthfully.

Readiness states are `DISABLED`, `NEEDS SETUP`, `ATTENTION REQUIRED`, and `READY`.

`Check Again` and ordinary settings render are read-only. `Load Recommended SRWF Draft` only uses already-existing explicit unique GTB tokens and never guesses shared binary roles from label, type, ID, order, or DOM position; it reports proposed changes and never saves until the explicit Save path succeeds.

Historic Owner evidence from the superseded PR #14 candidate proved the product path could reach `READY` and project the intended tokens in the Owner runtime. That evidence is preserved under `evidence/`, but it does **not** prove this reconciled `0.1.8` exact branch; Owner runtime recheck remains required.

## Batch boundary

This branch intentionally does not implement the newly resolved broad visual constants. In particular it does not add the `960px` card layout, helper/error repositioning CSS/JS, new title/rhythm/focus/upload values, Student Photo state assumptions, GPAS behavior, PersianGravity behavior, or a second theme.

The existing production CSS, including the merged PR #15 binary-choice runtime row/equal-track repair, remains unchanged in this batch. `STATICALLY_PROVEN` does not mean final WordPress/browser production qualification.
