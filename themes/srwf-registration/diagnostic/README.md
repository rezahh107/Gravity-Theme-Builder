# SRWF Runtime Diagnostic v0.3

This repository-managed diagnostic is the Owner test companion for the SRWF Registration theme. It incorporates the semantic runtime evidence needed by the desktop fidelity pass without turning the diagnostic into a DOM dump or transport service.

## Owner path

Install it as a separate WordPress plugin. When an administrator renders an explicitly opted-in SRWF form, the plugin loads automatically and shows:

`دانلود گزارش GTB`

No URL query flag is required. The control remains separate from the form and the diagnostic has no server endpoint or remote transport. The download is created locally in the browser as JSON.

## Collection model

The report uses independent bounded collectors for:

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

The collector never serializes user-entered control content, textarea content, selected option identity, option text/values, file names, arbitrary label/description/message text, cookies, authentication/profile data, submissions, raw payloads, or generic displayed text.

Large selects are represented only by aggregate option count plus safe structure. Their option descendants are not traversed, so a roughly 950-option school selector cannot starve Tom Select or later collectors.

Conditional cascade evidence is independently bounded. If that evidence budget is exhausted, truncation is reported rather than turning unassessed context into positive cascade evidence.

GPFUP existence is now runtime-detectable only through the exact observed class family (`.gpfup`, `.gpfup--strict`, `.gpfup__droparea`). The diagnostic does not infer crop configuration, file rules, or upload behavior.

PersianGravity-specific consumers remain `NOT_PROVEN` until an identifying runtime consumer is actually observed; no plugin-name-derived selector is invented.

## Evidence boundary

A v0.3 repository test PASS proves collector isolation, boundedness, privacy guardrails, deterministic structural targeting, and the deterministic conditional-cascade fixture semantics. It does not prove the Owner browser's computed Submit width, Tom Select behavior, GPFUP lifecycle, validation/focus behavior, unrelated-form isolation, or the browser-specific availability/evaluation of every possible conditional CSSOM grouping type. Those remain Owner-runtime checks.
