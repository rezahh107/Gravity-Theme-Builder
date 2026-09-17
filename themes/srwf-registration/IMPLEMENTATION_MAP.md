# SRWF Registration — Implementation Map

Status: **FIRST_IMPLEMENTATION / STATICALLY_QUALIFIED_ONLY**

This map is the traceability layer from the admitted SRWF visual authority to the first production implementation. It is intentionally not a property dump.

Evidence labels used here: `OWNER_APPROVED`, `DOCUMENTED`, `STATICALLY_PROVEN`, `RUNTIME_PROVEN`, `RUNTIME_REQUIRED`, `NOT_PROVEN`, `NON_NORMATIVE_REFERENCE`.

Preserved contract resolution identifiers (verbatim):

```yaml
focus_ring_exact_geometry: NOT_PROVEN
focus_ring_exact_alpha: NOT_PROVEN
desktop_short_field_pairings: NOT_PROVEN
desktop_shadow_exact_value: NOT_PROVEN
exact_production_breakpoint: NOT_PROVEN
```

## Activation and delivery

The theme is opt-in per Gravity Form. Configure **Form Settings → Form Layout → CSS Class Name** with exactly `srwf-registration`, then load/activate the theme-local `srwf-registration.php` bootstrap as WordPress plugin code. The bootstrap uses the documented `gform_enqueue_scripts` lifecycle and the form object's documented `cssClass` property to enqueue the stylesheet only for opted-in forms. No form ID is hard-coded.

This is `DOCUMENTED` + `STATICALLY_PROVEN`; it is not `RUNTIME_PROVEN` until exercised in the supported WordPress/Gravity Forms runtime.

## Material requirement map

| Requirement | Approved value/state | Authority locator | Responsibility class | Intended host mechanism | Mechanism evidence | Implementation disposition | Runtime inspection required | Fallback | Implementation locator |
|---|---|---|---|---|---|---|---|---|---|
| Target isolation | only intended SRWF registration form | Project Charter §9; Theme Authoring Contract §7 | activation / isolation | GF Form Settings CSS Class + `Form Object.cssClass` + `gform_enqueue_scripts` | `DOCUMENTED`; static exact-token check | IMPLEMENT | yes — prove class placement/enqueue lifecycle in supported runtime | none; fail closed when class absent | `srwf-registration.php`; activation class `srwf-registration` |
| Persian composition | RTL | Visual/UX Contract §10 | directionality | scoped CSS `direction`; GF keeps semantics | `OWNER_APPROVED` + CSS semantics | IMPLEMENT | yes — inspect actual mixed-direction fields | host semantics unchanged | `src/srwf-registration.css` activation scope |
| Font family target | Vazirmatn; delivery owner = Vazir | Visual/UX Contract §9 | typography | scoped inherited `font-family`; no font delivery | `OWNER_APPROVED`; consumer static only | IMPLEMENT | yes — prove real site supplies Vazirmatn | system UI fallback without claiming fidelity | activation scope `font-family` |
| Primary color | `#1D4ED8` | Visual/UX Contract §8 | color | `--gf-color-primary` | `DOCUMENTED` CSS API | IMPLEMENT | yes — verify consumers/computed styles | scoped direct CSS only for a proven gap | activation scope token |
| Pressed primary action | `#1E40AF` | Visual/UX Contract §8 | state / action | authentic submit `:active` presentation | selector `DOCUMENTED`; runtime consumer unproven | IMPLEMENT | yes — GF 3.x button/cascade | add a narrower runtime adapter only if host CSS defeats it | submit `:active` rule |
| Error semantic color | `#B42318` | Visual/UX Contract §8, §15 | validation state | `--gf-color-danger`, control error and validation-summary CSS API tokens | `DOCUMENTED` | IMPLEMENT | yes — authentic failed validation | no shadow validation logic | activation/error token rules |
| Success semantic color | `#18794E` | Visual/UX Contract §8 | success state | real consumer not established in this repository | `RUNTIME_REQUIRED` | RUNTIME_REQUIRED | yes — identify authentic host/add-on success consumer | none | not emitted as production constant |
| Control surface | white `#FFFFFF` | Visual/UX Contract §8, §13 | control | `--gf-ctrl-bg-color` | `DOCUMENTED` | IMPLEMENT | yes — computed styles | narrow consumer rule if API is not consumed | activation scope token |
| Control border | `#8690A1` | Visual/UX Contract §5, §8, §16 | control | `--gf-ctrl-border-color` | `DOCUMENTED` | IMPLEMENT | yes — contrast + actual consumer | narrow consumer rule if required | activation scope token |
| Control radius | `10px` | Visual/UX Contract §8 | control | `--gf-ctrl-radius` | `DOCUMENTED` | IMPLEMENT | yes — add-ons may not consume it | bounded adapter only after inspection | activation scope token |
| Control minimum height | `52px` | Visual/UX Contract §8, §13 | control sizing | Theme Framework `--gf-ctrl-size` | `DOCUMENTED`; runtime minimum-size behavior unproven | IMPLEMENT | yes — text enlargement/content clipping | scoped `min-block-size` only if runtime proves token insufficient | activation scope token |
| Control value typography | `16px / 400` | Visual/UX Contract §9 | typography | `--gf-ctrl-font-size`; `--gf-ctrl-font-weight` | `DOCUMENTED` CSS API | IMPLEMENT | yes — computed controls/add-ons | narrow consumer rule after evidence | activation scope control tokens |
| Field label typography | `15px / 600` | Visual/UX Contract §9 | typography | `--gf-ctrl-label-font-size-primary`; `--gf-ctrl-label-font-weight-primary` | `DOCUMENTED` | IMPLEMENT | yes — compound/add-on labels | narrow field adapter after inspection | activation scope label tokens |
| Section heading typography | `18px / 700` | Visual/UX Contract §9 | section | documented Orbital `.gsection_title` selector + scoped CSS | `DOCUMENTED` selector | IMPLEMENT | yes — real Section field | none unless markup differs | `.gsection_title` scoped rule |
| Decorative divider color | `#E4E7EC` | Visual/UX Contract §8, §12 | section / divider | preserve host Section border geometry; set only color | selector `DOCUMENTED`; geometry intentionally host-owned | IMPLEMENT | yes — confirm actual divider exists | bounded direct border only after runtime evidence | `.gsection { border-color }` |
| Muted/help text color | `#667085`; placement below input | Visual/UX Contract §8, §14 | help text | `--gf-ctrl-desc-color`; GF Form Settings owns placement | color API `DOCUMENTED`; placement host setting | IMPLEMENT | yes — verify `description_below` and semantic association | do not move descriptions in theme code | activation scope description token |
| Help text exact font size | `NON_NORMATIVE_REFERENCE` | Visual/UX Contract §7, §9 | typography | none | `NON_NORMATIVE_REFERENCE` | DEFER_NOT_PROVEN | no implementation until authority changes | host default | absent |
| Field-error exact font size | `NON_NORMATIVE_REFERENCE` | Visual/UX Contract §7, §15 | typography / error | none | `NON_NORMATIVE_REFERENCE` | DEFER_NOT_PROVEN | no implementation until authority changes | host default | absent |
| Validation message below input | below input | Visual/UX Contract §5, §15 | validation presentation | Gravity Forms Form Settings / native validation | `OWNER_APPROVED` + `DOCUMENTED` host setting | HOST_OWNED | yes — programmatic association/read order mandatory | none | no lifecycle code |
| Validation summary | authentic GF summary; SRWF red semantic language | Visual/UX Contract §13, §15 | validation presentation | native `.gform_validation_errors` + documented validation CSS API | `DOCUMENTED` | IMPLEMENT | yes — authentic failed submission | host native default if API changes | scoped validation token rule |
| Visible focus | primary color basis; exact ring geometry/alpha `NOT_PROVEN` | Visual/UX Contract §8, §20 | focus | primary/focus border API; retain host focus semantics and geometry | focus APIs `DOCUMENTED`; exact geometry `NOT_PROVEN` | IMPLEMENT | yes — keyboard focus and settled host state | keep host outline; no invented shadow/ring | `--gf-ctrl-border-color-focus`; no ring geometry |
| Form title size/line-height | `NON_NORMATIVE_REFERENCE` | Visual/UX Contract §7, §9 | typography | none | insufficient authority | DEFER_NOT_PROVEN | no | host/site inherited values | absent |
| Field vertical rhythm | `NON_NORMATIVE_REFERENCE` | Visual/UX Contract §7, §12 | spacing | `--gf-form-gap-y` exists but value is unauthorized | API `DOCUMENTED`; value unresolved | DEFER_NOT_PROVEN | no | host default | absent |
| Major-section rhythm | `NON_NORMATIVE_REFERENCE` | Visual/UX Contract §7, §12 | spacing | no production value authorized | insufficient authority | DEFER_NOT_PROVEN | no | host default | absent |
| Mobile horizontal padding | `16px` | Visual/UX Contract §5, §8, §11 | layout | intrinsic scoped logical padding; no media query | CSS behavior static | IMPLEMENT | yes — 320px real reflow | adjust only with runtime evidence and contract-compatible scope | activation scope `padding-inline` |
| Content maximum width | `840px` | Visual/UX Contract §8, §11 | layout | intrinsic `max-inline-size` + auto margins | CSS behavior static | IMPLEMENT | yes — embedding context | none | activation scope |
| Production breakpoint | `NOT_PROVEN` | Visual/UX Contract §11 | responsive | none | `NOT_PROVEN` | DEFER_NOT_PROVEN | yes before any breakpoint is introduced | intrinsic single-column baseline | no `@media` rule |
| Desktop short-field pairs | `NOT_PROVEN` | Visual/UX Contract §7, §11 | layout | GF Foundation/form layout remains owner | `NOT_PROVEN` | DEFER_NOT_PROVEN | yes | fail closed to no theme-authored pairing | no pairing CSS |
| Desktop white-card surface | `OWNER_APPROVED`; radius `16px`; exact shadow `NOT_PROVEN` | Visual/UX Contract §5, §11, §17 | surface | needs a proven desktop activation threshold/container context | value approved, conditional application unresolved | RUNTIME_REQUIRED | yes — distinguish desktop from mobile without inventing breakpoint | preserve host/embed surface until resolved | absent from production CSS |
| Desktop shadow | `NOT_PROVEN` | Visual/UX Contract §7, §17 | optical | none | `NOT_PROVEN` | DEFER_NOT_PROVEN | no | no shadow | absent |
| Phone values | LTR where applicable | Visual/UX Contract §10, §13 | directionality | scoped `input[type=tel]` direct CSS | HTML input semantics; runtime field type still required | IMPLEMENT | yes | field-specific class only after real inspection | scoped tel rule |
| National ID / other numeric codes | LTR where applicable | Visual/UX Contract §10, §13 | directionality | exact field identity/type unavailable | `RUNTIME_REQUIRED` | RUNTIME_REQUIRED | yes | no speculative field selectors | absent |
| Choice selected state | shape/text + color, not color-only | Visual/UX Contract §13, §20 | choice state | native GF choice semantics + primary Theme Framework color | API documented; exact runtime presentation unproven | HOST_OWNED | yes | bounded style only after real choice markup inspection | no shadow choice behavior |
| Jalali field | integrate authentic PersianGravity control | Visual/UX Contract §13, §22 | add-on | actual PersianGravity widget | `RUNTIME_REQUIRED` | RUNTIME_REQUIRED | yes | no speculative selector | absent |
| School selector | GP Advanced Select authentic states | Visual/UX Contract §13, §18, §22 | add-on | actual GP Advanced Select consumer | `RUNTIME_REQUIRED` | RUNTIME_REQUIRED | yes | no speculative selector | absent |
| Report-card upload | authentic GF/GPFUP states; upload radius `12px` where applicable | Visual/UX Contract §8, §13, §19 | add-on / upload | actual configured upload consumer | `RUNTIME_REQUIRED` | RUNTIME_REQUIRED | yes | no speculative selector | absent |
| Student photo/crop | authentic GPFUP state | Visual/UX Contract §13, §19, §22 | add-on / upload | actual GP File Upload Pro consumer | `RUNTIME_REQUIRED` | RUNTIME_REQUIRED | yes | no speculative selector | absent |
| Primary action typography/height | `16px / 700`, minimum `56px` | Visual/UX Contract §8, §9, §13 | action | documented primary button CSS API + scoped `min-block-size` | API/selector `DOCUMENTED`; min height statically expressed | IMPLEMENT | yes — GF 3.x submit markup and AJAX state | narrow adapter only after inspection | submit rule |
| Page background | `#F6F8FB` | Visual/UX Contract §8, §17 | outer surface | embedding/site page owns area outside form | visual value approved; ownership boundary outside form | HOST_OWNED | yes — integration page | page/template configuration, not global theme CSS | no `body`/`html` rule |

## Runtime qualification still required

The current repository/environment does not contain WordPress, Gravity Forms, PersianGravity, GP Advanced Select, or GP File Upload Pro runtime assets. Before production qualification, exercise the exact opted-in form in the supported stack and verify: stylesheet enqueue/class scope; real Orbital markup/cascade; 320 CSS px reflow; desktop surface strategy without an invented breakpoint; RTL and mixed-direction values; authentic validation summary/field errors; keyboard focus; long Persian content/text enlargement; submission/AJAX behavior; isolation from another form on the same page; and each installed add-on/custom-field consumer.
