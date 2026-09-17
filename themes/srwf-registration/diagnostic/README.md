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

## Privacy and boundedness

The collector never serializes user-entered control content, textarea content, selected option identity, option text/values, file names, arbitrary label/description/message text, cookies, authentication/profile data, submissions, raw payloads, or generic displayed text.

Large selects are represented only by aggregate option count plus safe structure. Their option descendants are not traversed, so a roughly 950-option school selector cannot starve Tom Select or later collectors.

GPFUP existence is now runtime-detectable only through the exact observed class family (`.gpfup`, `.gpfup--strict`, `.gpfup__droparea`). The diagnostic does not infer crop configuration, file rules, or upload behavior.

PersianGravity-specific consumers remain `NOT_PROVEN` until an identifying runtime consumer is actually observed; no plugin-name-derived selector is invented.

## Evidence boundary

A v0.3 repository test PASS proves collector isolation, boundedness, privacy guardrails, and deterministic structural targeting. It does not prove the Owner browser's computed Submit width, Tom Select behavior, GPFUP lifecycle, validation/focus behavior, or unrelated-form isolation. Those remain Owner-runtime checks.
