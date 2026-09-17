# SRWF Registration Theme

Status: **First reference implementation / exact visual target admitted / not production-qualified yet**

This directory is the first real theme built with Gravity Theme Builder.

## Mission lock

The first deliverable is **not a new SRWF-inspired design**.

It is the faithful implementation of the exact approved SRWF Registration design admitted under:

`reference/`

Before implementation planning, technical design, styling, or visual review for this theme, read:

1. `reference/VISUAL_AUTHORITY.md`
2. `reference/README.md`
3. run `reference/materialize_reference.sh` and inspect the verified materialized `OWNER_REFERENCE_new_7.html`

The approved artifact is the implementation target itself. Do not redesign, reinterpret, modernize, simplify, embellish, or substitute it.

Gravity Forms Theme Framework and inspected runtime evidence determine **HOW** the approved design is implemented. They do not redefine **WHAT** the design should be.

## Visual authority

The admitted HTML artifact defines the approved composition and visual/state target.

The owner-approved SRWF Public Registration Visual/UX Contract, identified by exact provenance in `reference/VISUAL_AUTHORITY.md`, governs exact canonical visual rules and explicit resolution states when the mockup contains approximate, demo-only, `NOT_PROVEN`, or `NON_NORMATIVE_REFERENCE` material.

Do not infer production values for unresolved items from screenshots or prototype CSS.

## Runtime boundary

The visual reference does not own Gravity Forms behavior.

Preserve Gravity Forms and applicable add-on ownership of:

- form markup and lifecycle;
- validation and submission;
- conditional logic;
- accessibility semantics and state;
- persistence;
- enhanced-select behavior;
- upload/crop behavior;
- Persian/Iranian field behavior where applicable.

Mockup scripts are state demonstrations, not production implementation authority.

## Scope

Expected responsibilities include:

- public registration form presentation;
- RTL / Persian typography and layout;
- field/control styling;
- field and section composition;
- responsive behavior;
- validation/error presentation;
- keyboard/focus presentation;
- required custom/add-on field visual integration;
- host isolation.

This theme is intentionally independent from Gravity Flow Inbox, Entry Detail, and Print work. Those surfaces are outside this theme's scope.

## Out of scope

Unless explicitly added later:

- Gravity Flow Inbox;
- Gravity Flow Entry Detail;
- Gravity Flow workflow UI;
- dossier/print output;
- form business logic;
- validation logic;
- data persistence;
- redesign of the approved registration reference.

## Planned local structure

```text
srwf-registration/
├── AGENTS.md          # Theme-local exact-target execution rules
├── README.md
├── reference/         # Admitted visual target and authority lock
├── src/               # Theme-local implementation
├── adapters/          # Only proven host/add-on gaps
└── tests/             # Theme-specific validation
```

Directories should gain code only when implementation requires it; empty architecture should not be manufactured for appearance.

## Implementation priority

For each approved visual requirement:

1. Identify the exact requirement from the admitted visual authority.
2. Consult the repository canonical Gravity Forms Theme Framework source.
3. Use the narrowest supported Theme Framework / CSS API mechanism that can faithfully express the requirement.
4. Use a supported Gravity Forms host mechanism when appropriate.
5. Add the smallest theme-scoped direct CSS rule for a demonstrated API gap.
6. Add a bounded adapter only after real runtime inspection proves a consumer-specific need.
7. Never change the approved visual target merely to make implementation easier.

## First implementation map

Before substantial styling, create a theme-local `IMPLEMENTATION_MAP.md` that maps each implementation-driving visual requirement to the actual Gravity Forms mechanism and labels its evidence state.

The map must start from the admitted artifacts in `reference/`; it must not reconstruct visual intent from memory.

Do not create a mapping from memory when a property or runtime consumer is version-sensitive.

## Deviation rule

A difference from the approved design must never be silent.

A deviation is admissible for consideration only when the visual authority is genuinely ambiguous on the affected point or inspected host/runtime evidence proves exact reproduction infeasible or incompatible with a binding host/accessibility constraint.

Record the constraint and use the smallest authorized reconciliation. `NOT_PROVEN` and `NON_NORMATIVE_REFERENCE` values remain unresolved rather than guessed.

## Acceptance expectations

The visual acceptance question for this first theme is intentionally simple:

> Does the real Gravity Forms SRWF Registration surface reproduce the same approved design admitted in `reference/`, subject only to explicitly documented and authorized runtime reconciliations?

Production qualification additionally requires real runtime evidence for the supported environment, including as applicable:

- approved desktop/mobile composition;
- 320 CSS px reflow;
- RTL / Persian content;
- long labels and values;
- validation/error states;
- keyboard focus;
- text enlargement;
- required PersianGravity / selected add-ons or custom fields;
- host/theme isolation;
- no submission or validation regression.

Static HTML similarity alone does not prove runtime qualification.

## Reuse rule

Do not move SRWF code into top-level `src/` merely because it looks generic. Promote only after a second real theme or a clearly project-wide invariant proves reuse.
