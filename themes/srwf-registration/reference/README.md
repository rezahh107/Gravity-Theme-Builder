# SRWF Registration — Admitted Visual Reference

Status: **APPROVED TARGET + CURRENT OWNER AUTHORITIES ADMITTED**

This directory contains the visual authority package for the first Gravity Theme Builder reference implementation.

## Mandatory read order for SRWF visual work

1. `VISUAL_AUTHORITY.md` — authority registry, current-vs-historical interpretation, provenance limits, and deviation gate.
2. `SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md` — **base current Owner-supplied destination authority** for unaffected decisions.
3. `SRWF_DESKTOP_SHELL_OWNER_DECISION_2026-09-20.md` — **later separately registered scoped Owner authority** for the Desktop Full Width shell/background/surface only.
4. `SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md` — exact historical Drive-backed Owner revision retained byte-for-byte for provenance and inherited rules not superseded by current Owner authority.
5. `materialize_reference.sh` — reconstructs and verifies the exact approved artifact.
6. Inspect the materialized `OWNER_REFERENCE_new_7.html` before implementation decisions that depend on composition/state or exact SVG geometry.

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

Identity:

```text
source_filename: OWNER_REFERENCE_new_7.html
source_sha256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
gzip_sha256: 696bc8466aa9503e782fee48f484a34c1a85d4c30210bcc645ecc7e8171c9340
base64_part_lengths: 8000, 8000, 7360
html_title: SRWF Student Registration — Final Contract-Corrected Mockup Set (v1.2)
visual_state: CLOSED
```

Successful materialization must reproduce those exact bytes. The artifact remains the approved composition/state target and exact geometry source where the authority chain explicitly uses it.

## Historical exact contract provenance

The historical/base contract remains registered as `VA:VC-1.0.0`.

The later Drive-backed v1.0.1 revision remains registered as `VA:VC-1.0.1` with its exact admitted identity:

```text
path: SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.1.md
repository_blob_sha: 3fac5772cbe356965d98de64950ef0fbec8d7f21
upstream_google_drive_file_id: 1t0fDtg-hnq5iHiLIO0wMJyTvOc-dVf4AJ2ULfYdfLgQ
upstream_revision_id: 3
upstream_revision_modified_at: 2026-09-18T05:25:12.441Z
upstream_text_plain_export_sha256: 032750fc4ae763b45b2fb136fc56b4543f38b9638617563d4082993a0cf54f58
```

That file is intentionally not rewritten. Its prior `NOT_PROVEN`, `NON_NORMATIVE_REFERENCE`, and below-input decisions are historical where current Owner authority explicitly supersedes them.

## Current Owner authority chain

Base current project authority is:

```text
authority_handle: OWNER:SRWF-2026-09-19
path: SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md
provenance: direct Owner-supplied project authority for this execution
immutable_upstream_drive_revision: NOT_AVAILABLE_TO_EXECUTOR
```

The later Desktop Full Width shell authority is separately identified and registered:

```text
authority_handle: OWNER:SRWF-2026-09-20-DESKTOP-SHELL
path: SRWF_DESKTOP_SHELL_OWNER_DECISION_2026-09-20.md
status: CURRENT_OWNER_SCOPE_AUTHORITY / DESKTOP_SHELL_APPROVED / RUNTIME_QUALIFICATION_REQUIRED
provenance: direct Owner-supplied current project authority after review of the real Full Width desktop runtime baseline
immutable_upstream_drive_revision: NOT_AVAILABLE_TO_EXECUTOR
scope: Desktop Full Width shell/background/surface presentation only
```

No Drive revision/hash is claimed or fabricated for either direct current Owner authority.

`OWNER:SRWF-2026-09-19` remains current for unaffected decisions. `OWNER:SRWF-2026-09-20-DESKTOP-SHELL` supersedes it only where they conflict inside the bounded desktop-shell scope. The later authority preserves the `960px` threshold, `904px` outer / `840px` content geometry, `32px` inline padding, `#FFFFFF` surface, and `16px` radius, and adds `32px` block padding, a non-layout `1px #E4E7EC` boundary, and restrained two-layer depth. The preferred `#F6F8FB` canvas remains host-owned unless a truthful authenticated GTB page-level seam exists.

The PR #28 provenance guard remains binding. A later Owner decision must be separately registered/admitted; implementation prose or an unknown handle cannot create authority.

These decisions define **WHAT / acceptance**. They do not prove that the current production CSS or real browser has qualified them.

## Exact-reproduction rule

For this first reference theme, the approved artifact plus current registered Owner authority define the implementation target. This is not inspiration, a redesign brief, or permission to modernize/simplify the design beyond admitted decisions.

## Behavior firewall

Gravity Forms and required add-ons remain responsible for actual validation, conditional logic, submission, search, upload/crop lifecycle, semantics, and persistence. Implement the appearance of authentic host states; do not copy mockup simulation behavior into production.

## Scope isolation

Do not substitute or mix in the separate Gravity Flow Inbox, Entry Detail, or Print/Dossier visual references. They are different surfaces and outside this theme's visual authority.
