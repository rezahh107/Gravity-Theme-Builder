# SRWF Registration — Agent Instructions

These instructions apply to work under `themes/srwf-registration/` and supplement the repository-root `AGENTS.md`.

They do not replace or weaken root repository governance.

## 0. Mandatory visual-target preflight

Before any SRWF Registration implementation planning, styling, technical design, visual review, refactoring, debugging, or implementation decision, retrieve and read:

1. `reference/VISUAL_AUTHORITY.md`
2. `reference/README.md`
3. the exact approved visual artifact in `reference/OWNER_REFERENCE_new_7.html.gz`

Materialize the artifact losslessly before visual analysis:

```bash
gzip -dc themes/srwf-registration/reference/OWNER_REFERENCE_new_7.html.gz > /tmp/OWNER_REFERENCE_new_7.html
```

Verify the decompressed source identity when artifact fidelity matters:

```text
SHA-256: 436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000
```

Do not claim this preflight occurred if the artifact and authority lock were not actually inspected for the current task.

If the exact visual artifact or `VISUAL_AUTHORITY.md` is missing, unreadable, or does not match its recorded identity, stop visual implementation work and report:

`SRWF_VISUAL_TARGET_UNAVAILABLE`

Do not substitute model memory, screenshots from another conversation, the Gravity Flow visual reference, an older mockup, or a newly invented design.

## 1. Exact-target rule

For the first reference theme, the admitted SRWF Registration design is the implementation target itself.

The task is **faithful reproduction**, not redesign.

Do not:

- reinterpret the design language;
- modernize it;
- simplify it for convenience;
- embellish it;
- replace it with a preferred design system;
- change visual values merely because another value maps more easily to Gravity Forms.

The Theme Framework determines implementation mechanics, not a replacement visual specification.

## 2. Visual-contract resolution

Use the owner-approved SRWF Public Registration Visual/UX Contract identified by exact provenance in `reference/VISUAL_AUTHORITY.md` for:

- exact canonical visual values;
- owner-closed visual decisions;
- `NOT_PROVEN` items;
- `NON_NORMATIVE_REFERENCE` items;
- conflicts between approximate mockup values and canonical visual rules.

The admitted HTML is the exact approved composition/state target. It must not be used to promote demo-only or unresolved values into production authority.

If an item is `NOT_PROVEN`, do not guess it.

## 3. WHAT / HOW boundary

```text
Admitted visual artifact + owner-approved Visual/UX Contract
        → WHAT must be reproduced

Repository canonical Gravity Forms Theme Framework source
+ current official Gravity Forms evidence
+ inspected supported runtime
        → HOW it is implemented
```

Do not let implementation evidence silently redesign the target.

Do not let the visual artifact take ownership of Gravity Forms behavior.

## 4. Host behavior firewall

Gravity Forms and applicable add-ons remain owners of their runtime behavior.

Do not copy mockup simulation code into production as a replacement for authentic host behavior, including:

- validation;
- conditional logic;
- submission;
- school search/filter lifecycle;
- upload/crop lifecycle;
- accessibility state;
- persistence.

Style authentic host states to match the approved target.

## 5. Deviation gate

A visual deviation is not justified by ease, preference, convention, modernization, or implementation convenience.

Surface a deviation candidate only when:

1. the admitted visual authorities are genuinely ambiguous on that exact point; or
2. inspected host/runtime evidence proves exact reproduction infeasible or incompatible with a binding host/accessibility constraint.

Do not silently resolve such a case in code. Record the constraint and apply only the smallest authorized reconciliation.

## 6. Acceptance posture

The implementation should remain recognizable as **the same approved SRWF Registration design running on real Gravity Forms**.

Static visual similarity is necessary but not sufficient for production qualification; real runtime behavior and accessibility must still be validated under the repository's normal evidence rules.
