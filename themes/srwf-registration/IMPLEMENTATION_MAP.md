# SRWF Registration — Implementation Map

Status: **AUTHORIZED_V1_STATICALLY_IMPLEMENTED / OWNER_RUNTIME_QUALIFICATION_REQUIRED**

This map distinguishes Owner authority, static/source evidence, host ownership, and evidence that still requires the real Owner runtime. Production qualification is intentionally open.

Evidence vocabulary: `OWNER_AUTHORIZED`, `DOCUMENTED`, `SOURCE_PROVEN`, `STATICALLY_PROVEN`, `HISTORICAL_OWNER_RUNTIME_PROVEN`, `OWNER_RUNTIME_REQUIRED`, `HOST_OWNED`, `HOST_INTEGRATION_REQUIRED`, `NOT_PROVEN`.

## Authority inputs

Registered immutable/exact IDs remain defined in `reference/VISUAL_AUTHORITY.md`:

- `VA:ARTIFACT` — admitted `OWNER_REFERENCE_new_7.html`, exact SHA-256 registered there;
- `VA:VC-1.0.0` — historical/base contract;
- `VA:VC-1.0.1` — exact historical Drive-backed Owner revision, including §27.

`OWNER:SRWF-2026-09-19`, recorded in `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md`, is implementation-driving for the resolved destination. It has no immutable upstream Drive revision/hash claim. `VA:VC-1.0.1` remains inherited historical authority only where not superseded.

Historical labels such as `RUNTIME_REQUIRED`, `NOT_PROVEN`, `NON_NORMATIVE_REFERENCE`, and `DEFER_NOT_PROVEN` remain provenance rather than current destination truth where the reconciliation resolves them. In particular, historical **Desktop short-field pairings** and **Desktop shadow** are superseded: pairings are now `HOST_OWNED / OWNER_CONFIGURABLE`, and the authorized desktop card has no shadow. The old below-input choice superseded by the current reconciliation is retained only as history.

## Implementation traceability

| Requirement | Current destination | Mechanism / ownership | Current disposition |
|---|---|---|---|
| Theme activation | explicit SRWF opt-in, unrelated forms untouched | stored form class establishes identity; rendering context separately gates admission | `STATICALLY_PROVEN`; exact-head browser `OWNER_RUNTIME_REQUIRED` |
| Gravity Flow Entry Detail | excluded even for same stored form | retained source-proven early enqueue + content bracket admission boundary | regression-tested; fresh Owner runtime `OWNER_RUNTIME_REQUIRED` |
| Per-form setup | Gravity Forms → Form Settings → GTB Theme | supported Form Settings hooks; no top-level menu | `STATICALLY_PROVEN`; historical product-path runtime evidence exists |
| Semantic mapping | eight explicit internal field references project GTB-owned tokens | no label/ID/order/DOM inference | `STATICALLY_PROVEN` |
| Projection safety | preserve unrelated Custom CSS classes; remove stale GTB tokens; idempotent | existing validated full Form Object update | `STATICALLY_PROVEN` |
| Production breakpoint | `960 CSS px` | viewport media query | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime `OWNER_RUNTIME_REQUIRED` |
| Mobile shell | fluid; `16px` inline padding | SRWF wrapper only | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED` |
| Desktop card | white; `840px` content + `32px` + `32px` = `904px` outer; radius `16px`; shadow none | `border-box`, `max-inline-size:904px`, `padding-inline:32px` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Page background | `#F6F8FB` | surrounding host/page integration | `HOST_INTEGRATION_REQUIRED`; GTB does not seize `html/body` |
| Form title | mobile `24px`, desktop `26px`, `700 / 1.5` | bounded SRWF title consumer | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED` |
| Section title | `18px / 700` | authentic Section Break title | existing + regression-protected |
| Field label | `15px / 600` | Gravity Forms Theme Framework API | existing + regression-protected |
| Value | `16px / 400` | Gravity Forms Theme Framework API | existing + regression-protected |
| Helper | `14px / 400 / 1.5` | Gravity Forms description CSS API | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Field error | `14px / 600 / 1.5` | Gravity Forms error-description CSS API | `DOCUMENTED / STATICALLY_IMPLEMENTED` |
| Primary action | `16px / 700`, full available width, host submit lifecycle | Theme Framework tokens + retained source/runtime-qualified sentinel width repair | `STATICALLY_PROVEN`; runtime recheck required |
| Ordinary field rhythm | `24px` | `--gf-form-gap-y` | `DOCUMENTED / STATICALLY_IMPLEMENTED`; actual geometry runtime pending |
| Major section rhythm | `32px` | host `24px` form gap + bounded `8px` Section Break offset | `STATICALLY_IMPLEMENTED`; actual geometry runtime pending |
| Visible focus | `2px solid #1D4ED8`, offset `2px`, no intended glow | GF focus API; direct projection only for visually-hidden binary native radio | `DOCUMENTED / STATICALLY_IMPLEMENTED`; keyboard runtime pending |
| Binary choices | explicit role only; equal tracks; `12px` gap; min `52px`; radius `10px`; tint `#EDF1FC`; non-color selected cue | native radios remain authority; CSS uses `:checked`/`:focus-visible` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; 320px + keyboard runtime pending |
| Section icon tiles | explicit mapped section roles only; `40×40`, radius `10`, icon `20`, tint `#EDF1FC` | admitted local SVGs | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; computed runtime pending |
| Report Card initial GPFUP | min `96px`; pad `16px`; radius `12px`; dashed `#8690A1` | `VA:VC-1.0.1` §27 `report_card_upload_initial` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19`; explicit Report Card role + authentic `.gpfup:not(.gpfup--has-files)` | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; upload runtime pending |
| Report Card has-files | do not force initial state over uploaded UI | no styling of file row/delete; initial rule excludes `.gpfup--has-files` | `HOST_OWNED`; regression-protected; real upload runtime pending |
| Student Photo post-upload | use authentic Photo consumer only | `VA:VC-1.0.1` §27 `student_photo_uploaded_state` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19`; no speculative selectors/composition | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`; crop ratio/dimensions `HOST_OWNED` |
| GPAS / Tom Select | appearance only | retained proven `.ts-wrapper > .ts-control` minimum integration | behavior `HOST_OWNED`; exact-head open/focus/results runtime pending |
| PersianGravity / Jalali | style only authentic consumer if admitted | no selector/adapter invented | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN` presentation |
| Desktop short-field pairings | Gravity Forms configuration remains authoritative | no GTB pair map | `HOST_OWNED / OWNER_CONFIGURABLE` |
| 320px/200%/text spacing/contrast | resilient intrinsic layout required | logical sizing/wrapping + host responsive mechanics | `OWNER_RUNTIME_REQUIRED` |

## Visual-role authority traceability

These exact rows preserve the retrievable v1.0.1/artifact authority path while the 2026-09-19 reconciliation supplies the final dimensions and acceptance values.

| Requirement | Authority path | Implementation | Current disposition |
|---|---|---|---|
| Gender binary card role | `VA:VC-1.0.1` §27 `gender_binary_choice` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | explicit `srwf-role-binary-choice`; native radio state | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Graduation Status binary card role | `VA:VC-1.0.1` §27 `graduation_status_binary_choice` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | explicit `srwf-role-binary-choice`; conditional visibility host-owned | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Section iconography | `VA:VC-1.0.1` §27 `section_heading_iconography` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | explicit mapped Section Break tokens + local SVGs | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Report Card initial GPFUP | `VA:VC-1.0.1` §27 `report_card_upload_initial` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | explicit `srwf-role-report-card-upload` + authentic initial GPFUP state | `OWNER_AUTHORIZED / STATICALLY_IMPLEMENTED`; runtime pending |
| Report Card `.gpfup--has-files` | `VA:VC-1.0.1` §§19,27 + host-owned GPFUP lifecycle | initial rules stop at authentic `.gpfup--has-files` state | `HOST_OWNED`; runtime recheck pending |
| Student Photo post-upload | `VA:VC-1.0.1` §27 `student_photo_uploaded_state` + `VA:ARTIFACT` + `OWNER:SRWF-2026-09-19` | none until authentic Photo state/DOM is captured | `OWNER_RUNTIME_REQUIRED / NOT_PROVEN`; crop config `HOST_OWNED` |

## Gravity Forms Form Presentation Readiness

The GTB Theme settings page now reports the current and expected host-owned Form Layout values without mutation:

| Form Object property | Expected |
|---|---|
| `labelPlacement` | `top_label` |
| `descriptionPlacement` | `above` |
| `validationPlacement` | `above` |
| `subLabelPlacement` | `above` |
| `validationSummary` | `true` |
| `requiredIndicator` | `asterisk` |

`Check Again` and ordinary render remain read-only. **Apply Recommended SRWF Form Layout** is a separate explicit capability + nonce protected action. At mutation time it re-reads the current full Form Object, computes only the six-property diff, performs no write when already matching, changes only those properties, calls `GFAPI::update_form()` with the coherent current object, re-reads it, and verifies persistence. `customRequiredIndicator` and unrelated form state are preserved.

Explicit field-level `labelPlacement`, `descriptionPlacement`, and `subLabelPlacement` values that conflict with the destination are reported as `ATTENTION REQUIRED` with a field ID/type reference. They are not silently rewritten. Overall Form Presentation Readiness is not `READY` while a known conflict remains.

Evidence: Gravity Forms Form Object/settings/update behavior is `DOCUMENTED`/`SOURCE_PROVEN`; mutation/read-back/preservation is `STATICALLY_PROVEN` by the PHP harness; actual Owner-site current values remain `OWNER_RUNTIME_REQUIRED`.

## Required indicator explanation

When SRWF presentation is admitted and the Form Object uses `requiredIndicator=asterisk`, GTB inserts exactly one inert localized paragraph through `gform_get_form_filter`:

> فیلدهای دارای * الزامی هستند.

The marker makes repeated filtering of the same generated HTML idempotent without request-global suppression. A fresh validation/AJAX rerender can therefore render its own single note. Gravity Forms remains authoritative for required state, native indicators, ARIA, and validation. Unrelated forms and excluded Entry Detail renders receive no note.

## Diagnostic v0.3.4

The admin-gated diagnostic adds a bounded SRWF v1 qualification collector for:

- viewport width and admitted wrapper rect/padding/max width/surface/radius/shadow/horizontal overflow;
- representative title/section/helper/error computed typography;
- bounded ordinary and section rhythm samples;
- real currently-focused admitted consumer outline facts only (no synthetic focus);
- explicit section icon pseudo-element geometry;
- explicit Report Card drop-area geometry and `.gpfup--has-files` boolean;
- the already-proven GPAS/Tom Select control consumer;
- sanitized Form Layout readiness and conflicting-override count.

It intentionally excludes entered values, labels/arbitrary page text, select option contents, filenames, upload URLs, query data, and Student Photo/PersianGravity speculative internals. Student Photo and PersianGravity are emitted only as unresolved status markers.

## Exact section/icon mapping

| Semantic section role | Approved section | Local asset |
|---|---|---|
| `srwf-role-section-identity` | هویت دانش‌آموز | `src/icons/section-identity.svg` |
| `srwf-role-section-contact` | اطلاعات تماس | `src/icons/section-contact.svg` |
| `srwf-role-section-education` | تحصیلات | `src/icons/section-education.svg` |
| `srwf-role-section-school-documents` | مدرسه و مدارک | `src/icons/section-school-documents.svg` |
| `srwf-role-section-student-photo` | عکس دانش‌آموز | `src/icons/section-student-photo.svg` |

## Batch boundary

This batch implements all currently authorized SRWF v1 presentation constants that can be safely expressed through proven Gravity Forms/GPFUP/GPAS consumers. It deliberately leaves page background integration, Student Photo post-upload composition, and PersianGravity presentation unresolved where the required host seam/consumer is not proven. It does not add a second theme, shared core, GPAS behavior, GPFUP lifecycle behavior, or GPP dependency.

`STATICALLY_IMPLEMENTED` / `STATICALLY_PROVEN` does **not** mean WordPress/browser production qualification. The exact installable candidate still requires the bounded Owner real-site checklist.
