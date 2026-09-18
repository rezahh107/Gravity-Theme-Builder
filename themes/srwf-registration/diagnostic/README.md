# SRWF Runtime Diagnostic v0.3

This repository-managed diagnostic is the bounded Owner evidence tool for the real SRWF Registration runtime.

v0.3 brings the repository copy forward from the earlier v0.2 collector to the capabilities required by the Owner's v0.2.5 evidence and this desktop-fidelity batch:

- visible local **دانلود گزارش GTB** control for normal Owner testing;
- no query-string activation requirement;
- admin-only and explicit `srwf-registration-theme` target-form gating;
- independent bounded semantic collectors with collector-level failure isolation;
- stylesheet/order and canonical-property evidence;
- ordinary controls plus Submit/footer/ancestor evidence;
- bounded matched-cascade evidence for Submit, including relevant `--gf-local-*` resolutions and the SRWF stylesheet's matching rules;
- title and section-heading consumers;
- Tom Select source/wrapper/control/dropdown association without enumerating large option collections;
- GPFUP root / strict-mode / image-mode / `.gpfup__droparea` presentation evidence when actually present;
- authentic validation/focus state;
- bounded field signatures and unrelated-form isolation evidence.

## Activation and Owner path

Install the diagnostic as a separate WordPress plugin.

It loads only when:

- the current user has `manage_options`; and
- the rendered Gravity Form explicitly has the SRWF `srwf-registration-theme` class.

No URL flag is required. The browser shows **دانلود گزارش GTB**. Clicking it runs the collectors and creates a local JSON download named:

`gtb-srwf-runtime-diagnostic-v0.3.0.json`

The plugin has no server collection endpoint and no remote transport.

## Privacy boundary

The collector records only bounded structural/presentation evidence such as approved structural IDs/classes, safe state attributes, bounding rectangles, selected computed CSS properties, stylesheet paths/order, relevant matched CSS declarations, canonical SRWF custom properties, and aggregate option counts.

It never intentionally serializes:

- user-entered control or textarea values;
- selected option values or displayed option text;
- arbitrary labels, descriptions, validation text, `textContent`, or `innerText`;
- cookies, authentication/profile data, submissions, or form payloads;
- file names or selected file identities.

Large source `<select>` collections are represented by aggregate option count only. `<option>` descendants are not traversed, so Tom Select collection remains independent of a roughly 950-option school list.

GP File Upload Pro is reported `RUNTIME_PROVEN` only when the actual `.gpfup` consumer is observed. The collector captures the proven root and `.gpfup__droparea` presentation shells but does not inspect file names, crop values, upload payloads, or behavior. PersianGravity-specific consumers remain `NOT_PROVEN` unless a future runtime supplies an identifying consumer supported by evidence.

## Failure semantics

Collectors fail independently. A collector failure is recorded by collector name/state only and does not trigger a generic DOM dump. The visible download control is created before collection and remains present if a collector or the overall collection path fails.

Static/unit PASS proves the repository collector's bounded/privacy-safe behavior against fixtures. It does not prove the Owner browser's final computed styles, Tom Select search/keyboard lifecycle, GPFUP behavior, authentic validation/focus behavior, or unrelated-form isolation. Those remain runtime evidence.
