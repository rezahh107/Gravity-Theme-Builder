# SRWF Registration — Visual Authority Lock

Status: **OWNER_CONFIRMED_EXACT_IMPLEMENTATION_TARGET**

This document locks the visual target for the **first reference theme** of Gravity Theme Builder.

## 1. Exact target

The first theme is not a redesign exercise and is not a new design derived from SRWF.

The implementation target is the approved SRWF Registration design artifact admitted in this directory as a connector-safe, lossless base64-split payload:

```text
OWNER_REFERENCE_new_7.html.gz.b64.part01
OWNER_REFERENCE_new_7.html.gz.b64.part02
OWNER_REFERENCE_new_7.html.gz.b64.part03
```

The three files are the exact Base64 encoding of a deterministic `gzip -n` archive of the approved HTML artifact. They are storage/transport parts, not separate visual references.

Materialize and verify the approved artifact before visual analysis or implementation:

```bash
bash themes/srwf-registration/reference/materialize_reference.sh
```

The materializer verifies both the reconstructed gzip payload and the decompressed HTML before returning the output path.

Identity of the approved source artifact:

```text
filename: OWNER_REFERENCE_new_7.html
sha256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
html_title: SRWF Student Registration — Final Contract-Corrected Mockup Set (v1.2)
artifact_marker: Final Correction Pass — v1.2 · Visual Design CLOSED
```

Identity of the deterministic compressed payload represented by the three Base64 parts:

```text
gzip_sha256: 696bc8466aa9503e782fee48f484a34c1a85d4c30210bcc645ecc7e8171c9340
compression: gzip -n (lossless; timestamp-neutral)
base64_part_lengths: 8000, 8000, 7360
```

Repository blob identities for the exact Base64 parts:

```text
part01: c26472d1641514f6550948630feef882a0d409cd
part02: 1e8a00ff68ad3ae812b1dd5470a173425249f1ca
part03: f93e7fb191746ade608229e43891c079731c92c2
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

## 3. Registered visual authority chain

The repository uses the following stable authority IDs. `IMPLEMENTATION_MAP.md` may cite only IDs registered in this block.

<!-- SRWF_VISUAL_AUTHORITY_REGISTRY_BEGIN -->
```yaml
visual_authority_registry:
  VA:ARTIFACT:
    type: admitted_visual_artifact
    repository_path: themes/srwf-registration/reference/OWNER_REFERENCE_new_7.html.gz.b64.part01+part02+part03
    materialized_filename: OWNER_REFERENCE_new_7.html
    materialized_sha256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
    role: exact_composition_state_and_geometry_reference

  VA:VC-1.0.0:
    type: historical_base_visual_contract
    repository: rezahh107/Gravity-Presentation-Profiles
    path: docs/visual/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.0.md
    source_blob_sha: 7400b7d0f97f245f090fd84893deb62c3ec83956
    role: admitted_base_contract_and_provenance

  VA:VC-1.0.1:
    type: current_owner_visual_contract_revision
    repository: rezahh107/Gravity-Theme-Builder
    path: themes/srwf-registration/reference/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md
    repository_blob_sha: 3fac5772cbe356965d98de64950ef0fbec8d7f21
    upstream_provider: Google Drive
    upstream_file_id: 1t0fDtg-hnq5iHiLIO0wMJyTvOc-dVf4AJ2ULfYdfLgQ
    upstream_revision_id: "3"
    upstream_revision_modified_at: 2026-09-18T05:25:12.441Z
    upstream_export_mime: text/plain
    upstream_export_sha256: 032750fc4ae763b45b2fb136fc56b4543f38b9638617563d4082993a0cf54f58
    upstream_display_title_note: "Drive display title still says v1.0.0; revision 3 content self-identifies as Visual / UX Contract v1.0.1."
    role: current_owner_contract_revision_including_2026_09_18_resolution
```
<!-- SRWF_VISUAL_AUTHORITY_REGISTRY_END -->

### Relationship between v1.0.0 and v1.0.1

`VA:VC-1.0.0` remains registered as the historical/base contract whose provenance was already admitted. It is not deleted or rewritten.

`VA:VC-1.0.1` is the exact later Owner revision. Sections 1–26 retain the prior contract rules/resolution states, and Section 27 adds the Owner resolution dated `2026-09-18`. Section 27 explicitly supersedes only the prior interpretation that the named visual fragments were non-normative; it does **not** silently resolve other `NOT_PROVEN` or `NON_NORMATIVE_REFERENCE` items.

The newly closed Section 27 decisions are:

- `gender_binary_choice`;
- `graduation_status_binary_choice`;
- `report_card_upload_initial`;
- `student_photo_uploaded_state` as an approved destination over authentic GPFUP state, not an authorization to invent post-upload DOM/behavior;
- `section_heading_iconography` for sections explicitly mapped by the admitted artifact.

The exact section-icon and report-card file-icon **geometry** is supplied by `VA:ARTIFACT`; Section 27 of `VA:VC-1.0.1` makes the named artifact fragments implementation-driving. The contract alone does not encode those SVG path coordinates, so geometry claims must be mechanically compared against the admitted artifact rather than inferred from prose.

The following remain unresolved exactly as the current Owner revision records:

- `exact_production_breakpoint`;
- `desktop_short_field_pairings`;
- `desktop_shadow_exact_value`;
- form-title exact size/line-height and desktop title enhancement;
- helper/error exact sizes;
- field/major-section rhythm;
- focus-ring exact geometry/alpha;
- exact GPFUP crop ratio/dimensions and other runtime/configuration-only facts.

## 4. Visual Contract relationship

The owner-approved SRWF Public Registration Visual/UX Contract remains the authority for exact canonical visual rules and explicit resolution states. `VA:VC-1.0.1` is the current registered revision for implementation-driving decisions; `VA:VC-1.0.0` remains the registered historical/base source.

These files record visual authority only. They do **not** make the legacy GPP repository architecture govern Gravity Theme Builder. In this repository, `docs/PROJECT_CHARTER.md` remains the normative repository authority and the visual contract is consumed only in its visual-intent / WHAT domain.

If the HTML artifact and the current Visual/UX Contract differ on an exact canonical value or an explicit `NOT_PROVEN` / `NON_NORMATIVE_REFERENCE` item, **the current Visual/UX Contract governs that visual rule**. The HTML remains the approved composition/state/geometry reference; it does not turn approximate mockup values into production authority.

Do not use this relationship to weaken the owner's exact-design intent. It exists to prevent prototype values, demo behavior, or unresolved measurements from being silently promoted into production facts.

## 5. WHAT vs HOW

```text
Approved SRWF visual artifact + registered owner-approved Visual/UX Contract revision
        ↓
WHAT must be reproduced

Gravity Forms Theme Framework + current host/runtime evidence
        ↓
HOW it is implemented
```

Theme Framework availability does not authorize changing the design. Conversely, the visual artifact does not authorize replacing Gravity Forms behavior.

Gravity Forms and required add-ons remain behavioral owners for markup, validation, submission, conditional logic, accessibility semantics, search/upload/crop lifecycle, and other host behavior.

## 6. Mockup behavior firewall

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

## 7. Deviation gate

A visual deviation from the approved target is not allowed merely because it is easier, more modern, more idiomatic, or preferred by the implementer.

A deviation may be considered only when at least one of these is true:

1. the approved artifacts are genuinely ambiguous on the affected point; or
2. inspected Gravity Forms/add-on/runtime evidence proves that exact reproduction is infeasible or would violate a binding host/accessibility constraint.

Any such case must be surfaced explicitly. Do not silently change the design. Preserve the approved target, record the constraint, and use the smallest authorized reconciliation.

Items marked `NOT_PROVEN` or `NON_NORMATIVE_REFERENCE` in the current visual contract must remain unresolved rather than guessed.

## 8. First-theme acceptance intent

The first implementation succeeds visually when a reviewer can compare the real SRWF Registration form against the admitted approved artifact and conclude that it is the **same approved design implemented on Gravity Forms**, subject only to explicitly documented and authorized runtime reconciliations.

Implementation planning must therefore begin from these admitted artifacts and registered authority sources, not from memory or a newly invented visual specification.
