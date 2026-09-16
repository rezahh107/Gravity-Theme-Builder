# Gravity Theme Builder — Project Charter

Status: **Governing project document**

This document defines the stable purpose, scope, authority, and non-negotiable engineering boundaries of the repository.

## 1. Purpose

Gravity Theme Builder exists to turn an **approved visual design** into a production-ready theme implementation on the **Gravity Forms Theme Framework** with the smallest safe amount of custom code.

The repository should accumulate reusable knowledge and tooling only when real theme implementations prove that reuse is warranted.

## 2. Product model

The project is not a single SRWF theme. It is a reusable engineering system capable of producing multiple Gravity Forms visual themes over time.

The first reference implementation is:

- `SRWF Registration`

SRWF is intentionally the first proving ground. It must not be used to justify speculative abstractions for future themes that do not yet exist.

## 3. Authority model

For a theme implementation, authority is ordered as follows:

1. Explicit current owner decision.
2. Approved visual/UX contract and reference artifacts for that theme.
3. This Project Charter.
4. `docs/THEME_AUTHORING_CONTRACT.md`.
5. `docs/ARCHITECTURE.md`.
6. Theme-specific implementation documentation.
7. Current official Gravity Forms documentation and inspected runtime behavior for implementation facts.
8. General engineering knowledge.

Visual references determine **what the theme should look like**. Gravity Forms documentation/runtime determines **how the host can safely express it**. Neither source substitutes for the other.

## 4. Core architectural position

Gravity Forms remains the behavioral host.

Gravity Theme Builder may control presentation but should preserve native ownership of:

- form markup and field lifecycle;
- validation and submission behavior;
- accessibility semantics and state;
- persistence and data handling;
- native Foundation mechanics;
- add-on behavior unless an adapter is explicitly required.

Theme implementation should prefer the official Theme Framework and CSS API. Direct CSS is an escape hatch for proven gaps, not the primary architecture.

## 5. Non-goals

Unless a later explicit decision changes this Charter, the repository does not aim to:

- replace Gravity Forms;
- fork or copy Orbital as a maintained codebase;
- create a custom form renderer;
- own validation/business logic;
- reimplement Foundation layout mechanics;
- create a page builder;
- build a universal design-to-code AI system;
- invent a generic theme SDK before repeated real needs justify one;
- redesign supplied visual references.

## 6. Minimal-change principle

A new abstraction, adapter, compatibility layer, or framework feature must solve a named problem observed in a real implementation.

Default rule:

> Keep a solution local to the theme until a second real use case proves that moving it into shared `src/` materially reduces duplication or risk.

This repository values a small proven core over a large speculative platform.

## 7. Theme acceptance model

A theme is acceptable only when both are true:

### Visual acceptance

The implementation preserves the approved visual intent across required surfaces, responsive states, content lengths, and interaction states.

### Runtime acceptance

The implementation is proven against the intended Gravity Forms runtime and required add-ons/custom fields without taking over host behavior or introducing regressions.

Static HTML/CSS similarity alone is insufficient for production qualification.

## 8. API-first rule

For every visual requirement:

1. Look for the narrowest current official Theme Framework/CSS API mechanism.
2. Prefer that mechanism when it can express the approved requirement.
3. If it cannot, document the API gap and use the smallest scoped CSS/runtime adapter.
4. Do not treat the existence of an API property as permission to invent a new visual value.

## 9. Host isolation

A theme must not assume ownership of the entire WordPress document.

Global root changes such as `html`, `body`, unrestricted `.gform_wrapper`, or site-wide tokens are prohibited by default. Theme styling must be scoped to an explicit theme activation/runtime boundary unless the host contract explicitly grants broader ownership.

## 10. Evidence states

Material technical claims should be classifiable as:

- `DOCUMENTED`
- `RUNTIME_PROVEN`
- `REFERENCE_ONLY`
- `ASSUMED`
- `NOT_PROVEN`

Do not promote assumptions to project architecture merely because they appear plausible.

## 11. Repository evolution

The expected evolution is:

```text
Approved Design
    ↓
Theme-local implementation
    ↓
Real runtime validation
    ↓
Repeated pattern observed
    ↓
Shared abstraction candidate
    ↓
Cross-theme proof
    ↓
Promotion to src/
```

The reverse flow — designing a generic framework first and forcing themes into it — is intentionally avoided.

## 12. First reference implementation: SRWF Registration

SRWF Registration is expected to exercise important real-world constraints, including:

- Persian / RTL presentation;
- responsive public form use;
- real validation/error states;
- theme isolation;
- custom or add-on fields;
- long Persian values;
- accessibility and keyboard focus;
- host Theme Framework integration.

The SRWF implementation may discover shared capabilities, but it must remain valid as a standalone theme implementation even before any reusable core exists.

## 13. Definition of project success

The project succeeds when it can repeatedly implement approved Gravity Forms visual designs with:

- high visual fidelity;
- low selector/cascade fragility;
- minimal host coupling;
- explicit evidence of runtime behavior;
- bounded, understandable adapters;
- reusable abstractions only where reuse is proven;
- straightforward maintenance across supported Gravity Forms versions.

## 14. Change control

Changes to the following require an explicit owner decision and a direct update to this Charter:

- project purpose;
- authority model;
- API-first rule;
- host-behavior ownership boundary;
- speculative-abstraction prohibition;
- definition of the repository as a reusable multi-theme project.
