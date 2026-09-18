# Historical Owner Runtime Evidence — GTB Per-Form Configuration — 2026-09-18

Status: **HISTORICAL_OWNER_RUNTIME_PROVEN_PRODUCT_PATH / CURRENT_0.1.8_RECHECK_REQUIRED**

This record preserves Owner-supplied runtime evidence produced on the prior PR #14 candidate. It is settings/product-path evidence, not current visual authority and not proof that the reconciled `0.1.8` branch has been runtime-tested.

## Evidence identity

Owner-supplied artifacts and SHA-256:

| Artifact | SHA-256 |
|---|---|
| `gtb-srwf-runtime-diagnostic-v0.3.0 (8).json` | `d3e0aee6b59b4b3ee9f8ae2d7d640b70068f56bfa48802875f2decbb12ec1480` |
| `gtb-srwf-admission-diagnostic-v0.3.2 (4).json` | `1cce85819bf4e3d3f064f275c393a9962dd33512c41dfe63fb4abbe70b29d1a0` |
| Registration screenshot `screencapture-kanoonshiraz-ir-2010-2-2026-09-18-19_27_58.jpg` | `20184898682f818d8107def53e55eb29db2f4a14b5a0050573b303f7470d91ae` |
| GTB Theme settings screenshot `screencapture-kanoonshiraz-ir-wp-admin-admin-php-2026-09-18-19_30_00.jpg` | `ea37eef5a6eb70ae2ade539b8e31c8d234db7c4efc1ad26bd9722100a2704593` |

The original bytes were supplied out-of-repository. This file preserves their identities and bounded observed claims; it does not regenerate or substitute those artifacts.

## Observed settings behavior on the prior candidate

The Owner admin screenshot showed the native Gravity Forms per-form **Settings → GTB Theme** surface after the Gravity Forms permission-resolver repair.

Observed:

- save notice reported configuration saved and GTB tokens projected;
- readiness: `READY`;
- saved profile: `SRWF Registration / Enabled`;
- all eight semantic mappings were selected and reported ready.

Runtime references from that exact form:

| Semantic role | Runtime field/section reference | GTB token |
|---|---:|---|
| Gender | `#92` | `srwf-role-binary-choice` |
| Graduation Status | `#205` | `srwf-role-binary-choice` |
| Report Card upload | `#208` | `srwf-role-report-card-upload` |
| Identity Section Break | `#180` | `srwf-role-section-identity` |
| Contact Section Break | `#181` | `srwf-role-section-contact` |
| Education Section Break | `#182` | `srwf-role-section-education` |
| School/Documents Section Break | `#183` | `srwf-role-section-school-documents` |
| Student Photo Section Break | `#184` | `srwf-role-section-student-photo` |

Those numbers are evidence references for that exact Owner form only. They are not public selectors or durable presentation identity.

## Runtime diagnostic observation

The runtime diagnostic reported:

- `collectorFailures: []`;
- one SRWF target;
- Foundation/Framework/Orbital/SRWF wrapper classes;
- form activation class present;
- `srwf-registration-theme-css` present at stylesheet index `16`, version `0.1.6`;
- GTB stylesheet after the observed Gravity Forms theme styles;
- all eight configured semantic roles present in runtime field signatures;
- submit observed at `840×56` in that capture.

Field signatures included:

- `field_11_92` → `srwf-role-binary-choice`;
- `field_11_205` → `srwf-role-binary-choice`;
- `field_11_208` → `srwf-role-report-card-upload`;
- `field_11_180` → `srwf-role-section-identity`;
- `field_11_181` → `srwf-role-section-contact`;
- `field_11_182` → `srwf-role-section-education`;
- `field_11_183` → `srwf-role-section-school-documents`;
- `field_11_184` → `srwf-role-section-student-photo`.

This historically proves that the prior candidate's explicit Save path persisted a bounded per-form configuration and projected the intended semantic tokens into authentic Gravity Forms objects/runtime.

## Admission observation

The admission diagnostic reported two non-truncated Registration decisions with:

- `formIdentityMatched: true`;
- `presentationAdmitted: true`;
- `renderingContext: registration`;
- `contextEvidence: registration_default`;
- `exclusionReason: null`;
- `srwfStylesheetPresent: true`.

This is historical evidence for Registration admission on that prior candidate. Entry Detail isolation remains supported by its separate evidence/regression chain.

## What this evidence supports today

It supports the claim that the per-form product path was previously Owner-runtime-proven to:

- be reachable through native Gravity Forms Form Settings after the native permission resolver was used;
- save successfully;
- persist the bounded configuration;
- reach `READY`;
- map eight semantic slots to compatible authentic host objects;
- project the activation and semantic role tokens;
- admit Registration presentation in the captured Registration runtime.

## What it does not prove

It does **not** prove the exact reconciled branch/head or `0.1.8` package has run on the Owner site. It also does not prove final desktop/mobile visual equivalence, current newly resolved 960px/card/title/helper/error/rhythm/focus destination, 320px reflow, keyboard/focus, validation states, text enlargement/spacing, Student Photo post-upload behavior, or final production accessibility/conformance.

Some visual values that were unresolved at the time of this capture have since been resolved by `reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md`. That later authority change does not retroactively turn this historical capture into proof of those newly authorized values.
