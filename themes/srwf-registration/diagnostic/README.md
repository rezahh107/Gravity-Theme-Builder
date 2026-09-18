# SRWF Runtime Diagnostic v0.3.1

This repository-managed diagnostic is the Owner test companion for the SRWF Registration theme. The existing v0.3 structural/presentation collector remains intact; v0.3.1 adds a separate bounded rendering-context admission report without turning the diagnostic into a DOM dump, ownership detector, or transport service.

## Owner path

Install it as a separate WordPress plugin alongside the production SRWF Registration package. When an administrator renders an explicitly opted-in SRWF form identity, the plugin loads automatically and shows:

- `دانلود گزارش GTB` — existing v0.3 structural/presentation report;
- `دانلود تصمیم GTB` — v0.3.1 server-admission report.

No URL query flag is required. Both controls remain separate from the form and the diagnostic has no server endpoint or remote transport. Downloads are created locally in the browser as JSON.

Diagnostic observability is deliberately independent from presentation ownership. A target form that is excluded from GTB presentation because it is being rendered inside authentic Gravity Flow Entry Detail can still expose the admission report to an administrator.

## Rendering-context admission report

The admission report contains only bounded enumerated facts:

- `formIdentityMatched`;
- `presentationAdmitted`;
- `renderingContext` — `registration`, `gravity_flow_entry_detail`, or `unknown`;
- `exclusionReason` — `gravity_flow_entry_detail`, `unrelated_form`, `production_admission_unavailable`, or `null`.

The diagnostic consumes `srwf_registration_theme_get_admission_decision()` from the production SRWF plugin when that API is available. It does **not** create a second URL/page/form-ID/GPP-based context classifier. If the production admission API is unavailable, the diagnostic reports `production_admission_unavailable`/`unknown` instead of inventing a result.

The admission payload is attached only for an administrator and only when the stored target identity class is present. It contains no form ID, page ID, entry ID, URL, label text, field value, submitted value, filename, user identity or arbitrary DOM text. The browser companion allows at most eight admission decisions in one report and marks truncation rather than growing without bound.

## Structural/presentation collection model

The existing v0.3 report uses independent bounded collectors for:

- stylesheet order and the SRWF stylesheet version query when available;
- target wrapper/form and canonical `--gf-*` properties;
- ordinary controls;
- Submit, footer/ancestors, relevant matched cascade branches, and resolved local width variables;
- form title and section-heading consumers;
- Tom Select source/wrapper/control/dropdown structure;
- generic upload structure;
- proven GP File Upload Pro `.gpfup` roots and `.gpfup__droparea` presentation;
- validation/error state and current focus owner;
- field structural signatures;
- unrelated Gravity Forms wrapper evidence.

A collector failure is isolated and recorded without disabling later collectors or hiding the Owner download control.

### Cascade applicability semantics

`matchedCascade.matchedRules` is intentionally stricter than selector matching alone. A selector-matching rule is admitted as active cascade evidence only when every applicability-affecting grouping context above it is proven active.

- `@media` is evaluated through the current browser's `matchMedia()` when safely available.
- `@supports` is evaluated through the current browser's `CSS.supports()` when safely available.
- a proven inactive condition is excluded;
- an unassessable condition such as a container/scope/other unknown grouping context fails closed and is recorded as bounded `UNKNOWN` condition evidence;
- nested contexts are conjunctive: one inactive or unknown ancestor prevents active promotion;
- unconditional grouping such as a CSS layer block may remain transparent;
- selector-list branch splitting, declaration capture, stylesheet provenance, rule budgets, and inaccessible-stylesheet evidence remain separate concerns.

Active matched rules carry their proven active `applicabilityContext`. Unknown condition evidence never appears inside active `matchedRules`.

## Privacy and boundedness

The structural collector never serializes user-entered control content, textarea content, selected option identity, option text/values, file names, arbitrary label/description/message text, cookies, authentication/profile data, submissions, raw payloads, or generic displayed text. The new admission report is even narrower: it accepts only the four enumerated server-decision fields above and discards arbitrary properties.

Large selects are represented only by aggregate option count plus safe structure. Their option descendants are not traversed, so a roughly 950-option school selector cannot starve Tom Select or later collectors.

Conditional cascade evidence is independently bounded. If that evidence budget is exhausted, truncation is reported rather than turning unassessed context into positive cascade evidence.

GPFUP existence is runtime-detectable only through the exact observed class family (`.gpfup`, `.gpfup--strict`, `.gpfup__droparea`). The diagnostic does not infer crop configuration, file rules, or upload behavior.

PersianGravity-specific consumers remain `NOT_PROVEN` until an identifying runtime consumer is actually observed; no plugin-name-derived selector is invented.

## Evidence boundary

Repository tests can prove collector isolation, boundedness, privacy guardrails, deterministic structural targeting, admission-field allowlisting and deterministic conditional-cascade fixture semantics. They cannot prove that the Owner site actually traverses the expected Gravity Flow Entry Detail lifecycle or that GTB is excluded there. The new rendering-context admission boundary remains `OWNER_RUNTIME_REQUIRED` until the authentic site test is performed.
