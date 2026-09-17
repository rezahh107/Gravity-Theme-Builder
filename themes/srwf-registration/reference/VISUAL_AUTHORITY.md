# SRWF Registration — Visual Authority Lock

Status: **OWNER_CONFIRMED_EXACT_IMPLEMENTATION_TARGET**

This document locks the visual target for the **first reference theme** of Gravity Theme Builder.

## 1. Exact target

The first theme is not a redesign exercise and is not a new design derived from SRWF.

The implementation target is the approved SRWF Registration design artifact admitted in this directory:

`OWNER_REFERENCE_new_7.html.gz`

The gzip file is a lossless repository copy of the approved HTML artifact. Materialize it before visual analysis or implementation:

```bash
gzip -dc themes/srwf-registration/reference/OWNER_REFERENCE_new_7.html.gz > /tmp/OWNER_REFERENCE_new_7.html
```

Identity of the decompressed approved source artifact:

```text
filename: OWNER_REFERENCE_new_7.html
sha256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
html_title: SRWF Student Registration — Final Contract-Corrected Mockup Set (v1.2)
artifact_marker: Final Correction Pass — v1.2 · Visual Design CLOSED
```

Identity of the stored gzip artifact:

```text
sha256: 696bc8466aa9503e782fee48f484a34c1a85d4c30210bcc645ecc7e8171c9340
compression: gzip -n (lossless; timestamp-neutral)
```

## 2. Required interpretation

For this first reference theme:

> The approved visual artifact is the implementation target itself — not inspiration, not a starting point, and not a request for a better design.

Do **not**:

- redesign it;
- reinterpret its visual language;
- modernize it;
- simplify or embellish it;
- substitute another design system;
- change visual values merely because another value is easier to express with Gravity Forms;
- use the separate Gravity Flow Inbox / Entry Detail / Print reference as authority for this theme.

The job is to reproduce the approved SRWF Registration presentation as faithfully as the real Gravity Forms runtime permits.

## 3. Visual Contract relationship

The owner-approved SRWF Public Registration Visual/UX Contract remains the authority for exact canonical visual rules and explicit resolution states.

Its exact admitted provenance is:

```text
repository: rezahh107/Gravity-Presentation-Profiles
path: docs/visual/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.0.md
source_blob_sha: 7400b7d0f97f245f090fd84893deb62c3ec83956
status: OWNER_APPROVED_VISUAL_AUTHORITY__EXPLICIT_RESOLUTION_STATES__RUNTIME_VALIDATION_REQUIRED
```

This file records the exact source identity; it does **not** claim that the legacy GPP repository architecture governs Gravity Theme Builder. In this repository, `docs/PROJECT_CHARTER.md` remains the normative repository authority and the contract is used only in its visual-intent / WHAT domain.

If the HTML artifact and the Visual/UX Contract differ on an exact canonical value or an explicit `NOT_PROVEN` / `NON_NORMATIVE_REFERENCE` item, **the Visual/UX Contract governs that visual rule**. The HTML remains the approved composition/state reference; it does not turn approximate mockup values into production authority.

Do not use this relationship to weaken the owner's exact-design intent. It exists to prevent prototype values, demo behavior, or unresolved measurements from being silently promoted into production facts.

## 4. WHAT vs HOW

```text
Approved SRWF visual artifact + owner-approved Visual/UX Contract
        ↓
WHAT must be reproduced

Gravity Forms Theme Framework + current host/runtime evidence
        ↓
HOW it is implemented
```

Theme Framework availability does not authorize changing the design. Conversely, the visual artifact does not authorize replacing Gravity Forms behavior.

Gravity Forms and required add-ons remain behavioral owners for markup, validation, submission, conditional logic, accessibility semantics, search/upload/crop lifecycle, and other host behavior.

## 5. Mockup behavior firewall

The admitted HTML contains interactive/demo behavior used to illustrate states. Those scripts and simulated states are **reference-only** unless independently proven to match the real host/runtime contract.

In particular, do not copy mockup JavaScript as production behavior for:

- validation;
- conditional logic;
- school search/filtering;
- upload/crop lifecycle;
- submission;
- success transitions;
- host state management.

Reproduce the **appearance of authentic host states**, not a shadow implementation of the host behavior.

## 6. Deviation gate

A visual deviation from the approved target is not allowed merely because it is easier, more modern, more idiomatic, or preferred by the implementer.

A deviation may be considered only when at least one of these is true:

1. the approved artifacts are genuinely ambiguous on the affected point; or
2. inspected Gravity Forms/add-on/runtime evidence proves that exact reproduction is infeasible or would violate a binding host/accessibility constraint.

Any such case must be surfaced explicitly. Do not silently change the design. Preserve the approved target, record the constraint, and use the smallest authorized reconciliation.

Items marked `NOT_PROVEN` or `NON_NORMATIVE_REFERENCE` in the visual contract must remain unresolved rather than guessed.

## 7. First-theme acceptance intent

The first implementation succeeds visually when a reviewer can compare the real SRWF Registration form against the admitted approved artifact and conclude that it is the **same approved design implemented on Gravity Forms**, subject only to explicitly documented and authorized runtime reconciliations.

Implementation planning must therefore begin from these admitted artifacts, not from memory or a newly invented visual specification.
