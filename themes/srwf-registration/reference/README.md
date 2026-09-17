# SRWF Registration — Admitted Visual Reference

Status: **APPROVED TARGET ADMITTED**

This directory contains the visual authority package for the first Gravity Theme Builder reference implementation.

## Mandatory read order for SRWF visual work

1. `VISUAL_AUTHORITY.md` — exact-target interpretation and deviation gate.
2. `OWNER_REFERENCE_new_7.html.gz` — lossless repository copy of the approved HTML design artifact.
3. The owner-approved Visual/UX Contract identified below when an exact canonical value, resolution state, or visual-rule conflict must be resolved.

Do not begin SRWF visual implementation from memory, screenshots in another conversation, or a newly invented visual specification.

## Exact approved artifact

Stored artifact:

`OWNER_REFERENCE_new_7.html.gz`

It is a lossless, timestamp-neutral gzip copy of the approved source file:

`OWNER_REFERENCE_new_7.html`

Materialize it locally with:

```bash
gzip -dc themes/srwf-registration/reference/OWNER_REFERENCE_new_7.html.gz > /tmp/OWNER_REFERENCE_new_7.html
```

Identity:

```text
source_filename: OWNER_REFERENCE_new_7.html
source_sha256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
stored_gzip_sha256: 696bc8466aa9503e782fee48f484a34c1a85d4c30210bcc645ecc7e8171c9340
html_title: SRWF Student Registration — Final Contract-Corrected Mockup Set (v1.2)
visual_state: CLOSED
```

The compressed storage format does **not** alter the design artifact. Decompression reproduces the exact admitted HTML bytes identified by the source SHA-256 above.

## Visual/UX Contract provenance

The approved artifact is interpreted together with the owner-approved SRWF Public Registration Visual/UX Contract:

```text
repository: rezahh107/Gravity-Presentation-Profiles
path: docs/visual/SRWF_PUBLIC_REGISTRATION_VISUAL_UX_CONTRACT_v1.0.0.md
blob_sha: 7400b7d0f97f245f090fd84893deb62c3ec83956
status: OWNER_APPROVED_VISUAL_AUTHORITY__EXPLICIT_RESOLUTION_STATES__RUNTIME_VALIDATION_REQUIRED
```

For exact canonical visual values and explicit `NOT_PROVEN` / `NON_NORMATIVE_REFERENCE` states, that contract governs. The HTML remains the exact approved composition/state target.

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
