# Gravity Theme Builder — Architecture

Status: **Initial architecture**

This document describes the current technical shape of the repository. It is intentionally narrower than the Project Charter and may evolve as real themes produce evidence.

## 1. Architectural goal

Translate approved theme-specific visual decisions into the narrowest stable Gravity Forms Theme Framework mechanisms while keeping Gravity Forms in control of behavior.

## 2. Layer model

```text
Approved visual/UX reference
        ↓
Theme-specific semantic decisions
        ↓
Gravity Theme Builder mapping
        ↓
┌────────────────────────────────────┐
│ Preferred: Gravity Forms CSS API   │
│ / Theme Framework mechanisms       │
└────────────────────────────────────┘
        ↓
Bounded adapters for proven API gaps
        ↓
Gravity Forms Foundation / runtime
        ↓
Real form UI
```

The repository must not invert this relationship by making the approved design depend on Orbital defaults.

## 3. Repository layers

### `themes/<theme>/`

Primary home of a concrete theme.

A theme owns:

- its approved reference artifacts;
- its semantic visual decisions;
- Theme Framework/CSS API mappings;
- theme-scoped CSS;
- bounded adapters;
- theme-specific fixtures and validation.

Theme code should stay here until a pattern is proven reusable.

### `src/`

Shared implementation code across themes.

`src/` is deliberately empty at project start. Code may be promoted here only when repeated real use proves that sharing reduces duplication or risk without erasing theme-specific differences.

### `tests/`

Cross-theme invariants and reusable validation tooling.

Theme-specific tests remain inside their theme directory. A test moves to top-level `tests/` only when the assertion is truly project-wide.

### `docs/`

Governing and architectural documentation.

## 4. Theme package model

A concrete theme should converge toward a shape like:

```text
themes/example-theme/
├── README.md
├── reference/
│   └── ... approved artifacts ...
├── src/
│   └── ... theme implementation ...
├── adapters/
│   └── ... proven host/add-on gaps ...
└── tests/
    └── ... theme validation ...
```

This is a repository organization contract, not a promise that every directory must contain custom code.

## 5. Mapping hierarchy

For each visual requirement, implementation preference is:

1. Existing official Gravity Forms Theme Framework/CSS API property.
2. Existing official host mechanism exposed at the correct runtime scope.
3. Theme-scoped direct CSS using stable host selectors.
4. Narrow adapter for a proven custom-field/add-on/runtime consumer.

Avoid lower levels when a higher level can express the same requirement safely.

## 6. Semantic ownership

Theme decisions should be expressed semantically before being mapped to host properties.

Example:

```text
Theme decision: field vertical rhythm
        ↓
Host mapping: --gf-form-gap-y
```

The project should not make `--gf-form-gap-y` itself the design authority. If Gravity Forms changes an implementation detail later, the theme decision remains stable while the adapter/mapping may change.

## 7. Orbital relationship

Orbital is treated as a host implementation/reference within the Gravity Forms Theme Framework ecosystem, not as the product architecture of this repository.

The project may rely on supported Theme Framework and Foundation mechanics used by Orbital, but must not:

- copy Orbital wholesale;
- preserve Orbital defaults when they conflict with approved theme intent;
- build a growing override war against Orbital selectors;
- infer that a visual behavior belongs to Orbital without inspecting its actual source/consumer.

## 8. Foundation relationship

Foundation mechanics should remain intact unless a named visual requirement cannot be satisfied without a bounded change.

A theme is a presentation layer, not a replacement layout/validation engine.

## 9. Adapter boundary

An adapter is allowed only when all are true:

- a concrete approved visual requirement exists;
- the preferred Theme Framework/API mechanism is insufficient or not consumed by the target runtime surface;
- the actual runtime consumer/markup is inspected;
- the adapter is scoped to that consumer/theme;
- host semantics/behavior remain unchanged;
- a regression test can describe the reason the adapter exists.

Adapters should carry their justification close to the implementation.

## 10. Responsive architecture

Responsive behavior belongs to the theme contract, not automatically to the viewport.

Use the narrowest mechanism appropriate to the real owner of the responsive decision:

- intrinsic layout / Grid / Flex first;
- container-driven adaptation for component-owned constraints when the runtime container supports it;
- media queries for true viewport/host-owned behavior;
- fixed values only where the design role is intentionally fixed.

Do not introduce modern CSS features solely because they are available.

## 11. Sizing architecture

Default guidance:

- typography: semantic relative units where appropriate;
- line height: unitless where appropriate;
- controls: content-driven with minimum size rather than brittle fixed height when the host allows it;
- optical borders/radii/details: may remain pixel-based when that is the intended visual role;
- layout: intrinsic sizing, `%`, `fr`, `minmax()`, logical sizing, and bounded caps as appropriate;
- print/physical output: separate physical-unit rules if a future theme requires them.

Exact choices remain theme-specific and must follow the approved design plus real host behavior.

## 12. Runtime ownership boundary

The theme may define presentation but should not take over:

- submission;
- validation logic;
- ARIA/state generation;
- field persistence;
- add-on business behavior;
- JavaScript lifecycle unless a proven visual integration requires a bounded adapter.

## 13. Compatibility strategy

Compatibility is evidence-based rather than version-name based.

For every supported Gravity Forms version:

- verify version-sensitive Theme Framework properties before use;
- keep mappings localized so API drift has a small repair surface;
- distinguish documented compatibility from runtime-proven compatibility;
- do not silently preserve obsolete properties for hypothetical versions.

## 14. Promotion rule into shared core

A theme-local implementation may be promoted into `src/` only when:

1. at least two real theme requirements need materially the same mechanism, or a single project-wide invariant clearly requires centralization;
2. the abstraction reduces duplication/risk rather than hiding meaningful differences;
3. tests can state the shared contract independently of one theme;
4. promotion does not make the first theme harder to understand.

Until then, duplication of a small proven pattern is preferable to a speculative framework.
