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

Authority in this repository is **domain-scoped**. Visual intent, repository engineering rules, and implementation facts are different authority domains. They must not be collapsed into one total precedence list or allowed to override one another outside their domain.

### 3.1 Owner decisions

Explicit current owner decisions govern authorized project and design decisions.

Where this Charter requires a direct amendment for a governed decision, the owner decision authorizes that change but does not silently rewrite the Charter; the Charter must be updated explicitly under Section 14.

### 3.2 Visual authority / WHAT

Approved visual/UX contracts and approved reference artifacts for a theme determine the intended presentation: **what the theme should look like and which visual states are required**.

Visual authority does not by itself authorize changes to Gravity Forms behavior, validation, lifecycle, accessibility semantics, persistence, Foundation mechanics, project non-goals, or other repository engineering boundaries.

A visual reference therefore cannot override this Charter outside the visual-intent domain.

### 3.3 Repository normative authority

For repository engineering rules, implementation boundaries, and authoring requirements, precedence is:

1. This `docs/PROJECT_CHARTER.md`.
2. `docs/THEME_AUTHORING_CONTRACT.md`.
3. `docs/ARCHITECTURE.md`.
4. Theme-specific implementation documentation.

This ordering applies to **normative repository instructions**. It does not make repository documentation authoritative for external runtime facts merely because that documentation is higher or lower in this list.

### 3.4 Implementation-fact evidence / HOW

Current official Gravity Forms documentation/source and inspected behavior in the supported runtime determine factual host capabilities, consumers, cascade behavior, markup, and other implementation facts.

Repository and theme-local documentation may record those facts, but they must not override contradictory current official documentation or inspected supported-runtime evidence. When a contradiction appears, surface it and reconcile the local documentation; treat the contradictory local factual claim as stale or not proven until reconciled.

Implementation-fact evidence does not authorize product or design decisions. It constrains **how** an authorized visual requirement can safely be implemented; it does not redefine **what** the approved design or repository boundaries should be.

### 3.5 General engineering knowledge

General engineering knowledge is a fallback only where higher-authority normative instructions, approved visual authority, or current factual evidence do not answer the question.

### 3.6 Cross-domain conflict rule

Do not resolve a cross-domain conflict by applying one flat precedence ranking.

Instead:

- use visual authority for visual intent;
- use repository normative authority for project/engineering rules;
- use current official documentation and inspected runtime behavior for implementation facts;
- use explicit owner decisions for authorized project/design decisions within the change-control rules above.

If a factual host constraint prevents an approved visual requirement from being implemented as expected, preserve the visual requirement as the target, report the factual constraint, and choose or request the smallest authorized reconciliation. Do not silently weaken the design and do not falsify host behavior.

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
