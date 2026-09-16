# SRWF Registration Theme

Status: **First reference implementation / not production-qualified yet**

This directory is the first real theme built with Gravity Theme Builder.

## Mission

Implement the approved SRWF public registration visual design on the Gravity Forms Theme Framework while preserving Gravity Forms behavior and using the official CSS API before direct CSS.

This theme is intentionally independent from Gravity Flow Inbox, Entry Detail, and Print work. Those surfaces are outside this theme's scope.

## Scope

Expected responsibilities include:

- public registration form presentation;
- RTL / Persian typography and layout;
- field/control styling;
- field and section rhythm;
- responsive behavior;
- validation/error presentation;
- keyboard/focus presentation;
- required custom/add-on field integration;
- host isolation.

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
├── README.md
├── reference/        # Approved visual authority
├── src/              # Theme-local implementation
├── adapters/         # Only proven host/add-on gaps
└── tests/            # Theme-specific validation
```

Directories should gain code only when the implementation requires it; empty architecture should not be manufactured for appearance.

## Implementation priority

For each requirement:

1. Gravity Forms Theme Framework / CSS API.
2. Supported Gravity Forms host mechanism.
3. Small theme-scoped direct CSS rule.
4. Bounded adapter after real runtime inspection.

## First implementation map

Before substantial styling, create a theme-local `IMPLEMENTATION_MAP.md` that maps approved visual requirements to actual Gravity Forms mechanisms and labels each mapping with its evidence state.

Do not create a mapping from memory when the property is version-sensitive.

## Acceptance expectations

Production qualification will require real runtime evidence for the supported environment, including as applicable:

- approved desktop visual reference;
- approved mobile visual reference;
- RTL / Persian content;
- long labels and values;
- validation/error state;
- keyboard focus;
- text enlargement and narrow reflow;
- required PersianGravity / selected add-ons or custom fields;
- host/theme isolation;
- no submission or validation regression.

## Reuse rule

Do not move SRWF code into top-level `src/` merely because it looks generic. Promote only after a second real theme or a clearly project-wide invariant proves reuse.
