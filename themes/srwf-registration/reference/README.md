# SRWF Registration — Admitted Visual Reference

Status: **APPROVED TARGET + CURRENT OWNER VISUAL CONTRACT REVISION ADMITTED**

This directory contains the visual authority package for the first Gravity Theme Builder reference implementation.

## Mandatory read order for SRWF visual work

1. `VISUAL_AUTHORITY.md` — authority registry, exact-target interpretation, v1.0.0 → v1.0.1 relationship, and deviation gate.
2. `SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` — current exact Owner revision, including the 2026-09-18 resolution in §27.
3. `materialize_reference.sh` — reconstructs and verifies the exact approved artifact.
4. Inspect the materialized `OWNER_REFERENCE_new_7.html` before implementation decisions that depend on composition/state or exact SVG geometry.

Do not begin SRWF visual implementation from memory, screenshots in another conversation, current CSS, or a newly invented visual specification.

## Exact approved artifact

The approved HTML is stored as an exact, connector-safe Base64 payload split across:

```text
OWNER_REFERENCE_new_7.html.gz.b64.part01
OWNER_REFERENCE_new_7.html.gz.b64.part02
OWNER_REFERENCE_new_7.html.gz.b64.part03
```

These parts concatenate to the Base64 encoding of a deterministic `gzip -n` archive of the approved HTML. Reconstruct it with:

```bash
bash themes/srwf-registration/reference/materialize_reference.sh
```

The script verifies both payload stages.

Identity:

```text
source_filename: OWNER_REFERENCE_new_7.html
source_sha256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
gzip_sha256: 696bc8466aa9503e782fee48f484a34c1a85d4c30210bcc645ecc7e8171c9340
base64_part_lengths: 8000, 8000, 7360
html_title: SRWF Student Registration — Final Contract-Corrected Mockup Set (v1.2)
visual_state: CLOSED
```

The split storage format does **not** alter the design artifact. Successful materialization reproduces the exact admitted HTML bytes identified by the source SHA-256 above.

## Visual/UX Contract provenance

The historical/base contract remains registered for provenance:

```text
authority_id: VA:VC-1.0.0
repository: rezahh107/Gravity-Presentation-Profiles
path: docs/visual/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.0.md
blob_sha: 7400b7d0f97f245f090fd84893deb62c3ec83956
```

The current implementation authority is the later Owner revision admitted locally:

```text
authority_id: VA:VC-1.0.1
path: SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md
upstream_google_drive_file_id: 1t0fDtg-hnq5iHiLIO0wMJyTvOc-dVf4AJ2ULfYdfLgQ
upstream_revision_id: 3
upstream_revision_modified_at: 2026-09-18T05:25:12.441Z
upstream_text_plain_export_sha256: 032750fc4ae763b45b2fb136fc56b4543f38b9638617563d4082993a0cf54f58
status: OWNER_APPROVED_VISUAL_AUTHORITY__EXPLICIT_RESOLUTION_STATES__RUNTIME_VALIDATION_REQUIRED
```

The upstream Drive display title was not renamed when the Owner revised the content; revision 3 itself self-identifies as **Visual / UX Contract v1.0.1**. `VISUAL_AUTHORITY.md` records the repository blob identity of the admitted copy and the exact relationship to v1.0.0.

Section 27 resolves only the explicitly named binary-choice, Report Card initial upload, Student Photo uploaded destination, and mapped section-icon fragments. Previously unresolved breakpoint, pairing, shadow, title/help/error sizing, rhythm, focus geometry/alpha, crop configuration and runtime-only facts remain unresolved.

For exact canonical visual values and explicit `NOT_PROVEN` / `NON_NORMATIVE_REFERENCE` states, the current registered contract revision governs. The HTML remains the exact approved composition/state target and the geometry source where §27 explicitly makes an artifact fragment implementation-driving.

This is a domain-scoped visual relationship. It does not import the old repository's engineering architecture or create a cross-domain authority order in Gravity Theme Builder.

## Exact-reproduction rule

For this first reference theme, the approved artifact is **the implementation target itself**.

It is not:

- inspiration;
- a loose reference;
- a redesign brief;
- permission to modernize, simplify, embellish, or substitute a different design system.

The implementation should make the real Gravity Forms registration surface look like the approved design as faithfully as the supported runtime permits.

Read `VISUAL_AUTHORITY.md` for the complete lock and deviation rules.

## Behavior firewall

The HTML contains demo/interactivity code used to illustrate visual states. Demo behavior is not production behavior authority.

Gravity Forms and the required add-ons remain responsible for actual validation, conditional logic, submission, search, upload/crop lifecycle, semantics, and persistence. Implement the appearance of authentic host states; do not copy the mockup's simulated behavior into production merely because it appears in the reference.

## Scope isolation

Do not substitute or mix in the separate Gravity Flow Inbox, Entry Detail, or Print/Dossier visual references. They are different surfaces and are outside this theme's visual authority.
