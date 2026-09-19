# SRWF Registration — Visual Authority Lock

Status: **OWNER_CONFIRMED_EXACT_IMPLEMENTATION_TARGET / CURRENT_OWNER_RECONCILIATION_ADMITTED**

This document locks the visual target for the first Gravity Theme Builder reference theme and records which authority is current versus historical.

## 1. Exact admitted visual artifact

The first theme is faithful implementation of the approved SRWF Registration design, not a redesign.

The exact visual artifact is stored as the connector-safe, lossless payload:

```text
OWNER_REFERENCE_new_7.html.gz.b64.part01
OWNER_REFERENCE_new_7.html.gz.b64.part02
OWNER_REFERENCE_new_7.html.gz.b64.part03
```

Materialize it with:

```bash
bash themes/srwf-registration/reference/materialize_reference.sh
```

Exact source identity:

```text
filename: OWNER_REFERENCE_new_7.html
sha256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
html_title: SRWF Student Registration — Final Contract-Corrected Mockup Set (v1.2)
artifact_marker: Final Correction Pass — v1.2 · Visual Design CLOSED
```

Deterministic compressed payload:

```text
gzip_sha256: 696bc8466aa9503e782fee48f484a34c1a85d4c30210bcc645ecc7e8171c9340
compression: gzip -n
base64_part_lengths: 8000, 8000, 7360
```

Repository blob identities for the exact Base64 parts:

```text
part01: c26472d1641514f6550948630feef882a0d409cd
part02: 1e8a00ff68ad3ae812b1dd5470a173425249f1ca
part03: f93e7fb191746ade608229e43891c079731c92c2
```

## 2. Exact-target interpretation

`VA:ARTIFACT` is the approved composition/state/geometry reference. It is not permission to copy demo behavior into production or to promote approximate prototype values when a current Owner contract says otherwise.

Do not redesign, modernize, simplify, embellish, substitute another design system, infer presentation identity from labels/IDs/order, or mix in Gravity Flow Inbox / Entry Detail / Print authority.

Gravity Forms and applicable add-ons remain behavior owners for markup, validation, submission, conditional logic, accessibility state, search, upload/crop lifecycle, and persistence.

## 3. Registered historical/exact visual authority chain

The exact immutable sources remain registered with stable IDs. `IMPLEMENTATION_MAP.md` may cite only IDs registered in this block when it uses a `VA:*` identifier.

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
    type: historical_exact_upstream_visual_contract_revision
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
    role: exact historical predecessor preserving the 2026-09-18 decision state
```
<!-- SRWF_VISUAL_AUTHORITY_REGISTRY_END -->

### Relationship between v1.0.0 and v1.0.1

`VA:VC-1.0.0` remains the historical/base contract whose provenance was already admitted.

`VA:VC-1.0.1` remains the exact later Drive-backed Owner revision. Its Section 27 explicitly supersedes only the prior interpretation that the named binary-choice, upload/photo, and mapped section-icon fragments were non-normative. The file is intentionally left byte-for-byte unchanged so its admitted repository blob and Drive export provenance remain truthful.

The exact section-icon and report-card file-icon **geometry** is supplied by `VA:ARTIFACT`; Section 27 of `VA:VC-1.0.1` made those named artifact fragments implementation-driving.

The unresolved values recorded inside v1.0.1 are preserved there as **historical decision state**. They are not current where the Owner reconciliation below explicitly supersedes them.

## 4. Current Owner-supplied reconciliation

Current project authority for the resolved SRWF destination is:

```text
authority_handle: OWNER:SRWF-2026-09-19
path: themes/srwf-registration/reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md
status: CURRENT_OWNER_PROJECT_AUTHORITY / VISUAL_REPAIR_IMPLEMENTED_STATICALLY / GPFUP_INITIAL_ICON_FAMILY_STATICALLY_IMPLEMENTED / RUNTIME_VALIDATION_REQUIRED
provenance: direct Owner-supplied project authority for this execution
immutable_upstream_drive_revision: NOT_AVAILABLE_TO_EXECUTOR
```

No Google Drive revision ID, timestamp, export hash, or immutable upstream blob has been invented for this newer authority input.

`OWNER:SRWF-2026-09-19` supersedes contradictory or unresolved v1.0.1 states only where the reconciliation document explicitly says so. Unchanged v1.0.1 rules remain inherited. The current resolved decisions include:

- production desktop breakpoint `960 CSS px`;
- desktop short-field pairings `HOST_OWNED / OWNER_CONFIGURABLE`, with no canonical pair list;
- desktop card: `#F6F8FB` page where an authenticated ownership seam exists, `#FFFFFF` surface, `840px` content cap, `32px` inline card padding, `904px` outer max, `16px` radius, no shadow;
- target family stack `Vazirmatn, Vazir, Tahoma, Arial, sans-serif` plus exact title/section/label/control/helper/error/action typography and line-height;
- `24px` / `32px` field/section rhythm and the local label/helper/error/control gap chain;
- exact `:focus-visible` outline geometry;
- Gravity Forms recommended above-input description/validation/sub-label placement where supported, superseding the old below-input Owner choice;
- native required indication with the native required legend as the single explanation surface;
- **all authentic Gravity Forms Radio groups inside admitted SRWF Registration use card presentation**; the host `radio` field type is sufficient presentation scope, and `srwf-role-binary-choice` must not gate cards;
- Radio cards use min `52px`, `10px` radius, default `12px` gap, unselected `1px #8690A1`, selected `2px #1D4ED8` + `#EDF1FC` + visible non-color cue, with content-driven wrap/reflow and native semantics retained;
- exact section-icon tile dimensions and `12px` icon-heading gap;
- shared initial GPFUP upload-family dimensions plus a **family-wide visible icon requirement for both initial Report Card and image-only Student Photo surfaces**, using consistent icon-slot/alignment presentation while retaining file/document versus photo/camera meaning;
- the upload-icon alignment goal is presentation-only and must not alter Gravity Forms / GP File Upload Pro core, markup ownership, upload/crop lifecycle, or add-on behavior;
- current accessibility acceptance requirements.

These are destination/acceptance decisions. Theme `0.1.14` statically implements the shared initial GPFUP icon/alignment destination through bounded SRWF CSS and GTB-owned local assets. Static implementation and CI do not establish the remaining Owner-browser runtime-sensitive states listed in the reconciliation and implementation map.

## 5. WHAT vs HOW

```text
VA:ARTIFACT + exact historical contract provenance + OWNER:SRWF-2026-09-19
        → WHAT / current destination

Canonical Gravity Forms engineering reference
+ current official Gravity Forms documentation/source
+ inspected supported runtime
        → HOW
```

The current Owner authority does not take ownership of Gravity Forms behavior. Theme Framework availability does not authorize redesign.

## 6. Mockup behavior firewall

Do not copy mockup JavaScript as production behavior for validation, conditional logic, school search/filtering, upload/crop lifecycle, submission, success transitions, or host state management. Style authentic host states.

## 7. Deviation and evidence gate

A visual deviation is admissible only when current authority is genuinely ambiguous or inspected host/runtime evidence proves exact reproduction infeasible or incompatible with a binding host/accessibility constraint.

Documented/Owner-authorized values still require runtime qualification where consumer, cascade, behavior, reflow, contrast, focus, add-on state, or accessibility behavior is runtime-sensitive.

## 8. Current batch boundary

The 2026-09-19 visual-fidelity repairs preserve immutable historical authority and host behavior ownership while implementing the current Owner-authorized presentation destination.

Theme `0.1.14` implements the shared initial GPFUP icon/alignment family only on the authentic admitted initial seams: Report Card retains its document glyph, image-only Student Photo receives a local photo/camera glyph, and both use the same icon-slot geometry. The implementation stops before `.gpfup--has-files`; it does **not** authorize or implement Student Photo post-upload/crop composition or any takeover of GPFUP behavior.

Final Owner runtime qualification remains open; CI/static success is not production qualification.
