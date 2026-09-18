# SRWF Runtime Diagnostic v0.3.2

This repository-managed diagnostic is the Owner test companion for the SRWF Registration theme. The existing v0.3 structural/presentation collector remains intact; v0.3.2 extends the bounded context-admission companion so the repaired early Entry Detail timing can be inspected without turning the diagnostic into a DOM dump, route classifier, or transport service.

## Owner path

Install it as a separate WordPress plugin alongside the production SRWF Registration package. When an administrator renders an explicitly opted-in SRWF form identity, the plugin loads automatically and shows:

- `دانلود گزارش GTB` — existing v0.3 structural/presentation report;
- `دانلود تصمیم GTB` — v0.3.2 admission/timing report.

No URL query flag is required. Both controls remain separate from the form and the diagnostic has no server endpoint or remote transport. Downloads are created locally in the browser as JSON.

Diagnostic observability is deliberately independent from presentation ownership. A target form that is excluded from GTB presentation inside authentic Gravity Flow Entry Detail can still expose the admission report to an administrator.

## Rendering-context admission report

Each server admission decision is reduced to bounded enumerated facts:

- `formIdentityMatched`;
- `presentationAdmitted`;
- `renderingContext` — `registration`, `gravity_flow_entry_detail`, or `unknown`;
- `contextEvidence` — `registration_default`, `gravity_flow_early_enqueue`, `gravity_flow_content_bracket`, or `unknown`;
- `exclusionReason` — `gravity_flow_entry_detail`, `unrelated_form`, `production_admission_unavailable`, or `null`.

The browser report additionally records one boolean:

- `srwfStylesheetPresent` — whether the WordPress style element with the production handle ID `srwf-registration-theme-css` exists in the completed document.

This lets the Owner distinguish “Entry Detail was eventually recognized” from the actual acceptance requirement: the earliest presentation-relevant target decision is already excluded **and** the SRWF production stylesheet is absent.

The diagnostic consumes `srwf_registration_theme_get_admission_decision()` from the production plugin when available. It does **not** create a second URL/page/form-ID/GPP-based context classifier. If the production admission API is unavailable, it reports `production_admission_unavailable`/`unknown` rather than inventing a result.

The payload is attached only for an administrator and only when the stored target identity class is present. It contains no form ID, page ID, entry ID, URL, label text, field value, submitted value, filename, user identity or arbitrary DOM text. The browser companion retains at most eight admission decisions and marks truncation.

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
- unconditional grouping such as a CSS layer block may remain transparent.

## Privacy and boundedness

The structural collector never serializes user-entered control content, textarea content, selected option identity, option text/values, file names, arbitrary label/description/message text, cookies, authentication/profile data, submissions, raw payloads, or generic displayed text. The admission companion accepts only the enumerated server-decision fields above and a boolean style-handle presence observation; arbitrary properties are discarded.

Large selects remain aggregate-only and bounded. Conditional cascade evidence remains independently bounded. GPFUP existence is detected only through the runtime-proven class family. PersianGravity-specific consumers remain `NOT_PROVEN` until an identifying runtime consumer is observed.

## Evidence boundary

PR #12's v0.3.1 diagnostic produced the authentic evidence that narrowed this defect: an early admitted Registration decision was followed by a later correct Entry Detail exclusion in the same request, while the SRWF stylesheet was already present. v0.3.2 is designed to prove whether the repaired first presentation-relevant decision now carries `contextEvidence=gravity_flow_early_enqueue`, `presentationAdmitted=false`, and whether `srwfStylesheetPresent=false` at document completion.

Repository tests prove boundedness, allowlisting, privacy guardrails and deterministic fixture behavior. They do not prove the Owner site follows the expected Gravity Flow 3.1.0 / Gravity Forms 3.1.1.1 lifecycle. The repaired boundary remains `OWNER_RUNTIME_REQUIRED` until the authentic site test is performed.
