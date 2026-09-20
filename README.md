# Gravity Theme Builder

A reusable engineering project for implementing approved visual designs on the **Gravity Forms Theme Framework**.

The repository is intentionally **design-authority driven**: an approved visual contract defines visual intent; Gravity Forms remains the owner of form behavior, markup, validation, accessibility semantics, and lifecycle.

## Status

**First reference implementation active / SRWF mobile responsive polish statically implemented / Owner runtime qualification still open.**

The first reference implementation is:

- `SRWF Registration` — a real-world RTL/Persian public registration form theme.

SRWF is the first proving ground for the system, not a special case that defines every future theme. The current theme implementation is `0.1.16`; diagnostic `0.3.6` adds the mobile width-chain evidence needed for the next Owner qualification pass. Automated/static qualification is necessary evidence, but it does not by itself establish production-browser qualification.

## Current first implementation target

The current first concrete deliverable is **not merely an SRWF-inspired theme**. It is the faithful implementation of the exact owner-approved SRWF Registration design admitted under:

`themes/srwf-registration/reference/`

For the authoritative interpretation of this current target, read:

1. `themes/srwf-registration/README.md`
2. `themes/srwf-registration/reference/VISUAL_AUTHORITY.md`
3. `themes/srwf-registration/reference/SRWF_PUBLIC_REGISTRATION_OWNER_RECONCILIATION_2026-09-19.md`
4. `themes/srwf-registration/AGENTS.md` before implementation or visual-analysis work

The admitted `OWNER_REFERENCE_new_7.html` design is the historical composition/state/geometry reference where it has not been superseded by the current Owner reconciliation. Do not use it to roll back a newer explicit Owner decision.

Gravity Forms Theme Framework and inspected runtime evidence determine **HOW** that approved design is implemented; they do not redefine **WHAT** the first deliverable should look like.

## Current implementation reality

The SRWF work currently includes:

- native per-form GTB configuration/readiness;
- Registration-versus-Gravity-Flow-Entry-Detail presentation isolation;
- the Owner-authorized responsive shell, typography, spacing, focus, Submit, section-icon, and all-Radio card presentation;
- the repaired native Select / GP Advanced Select presentation family;
- the shared initial GPFUP icon/content-cluster presentation for Report Card and image-only Student Photo;
- theme `0.1.16` intrinsic Radio and initial-GPFUP narrow-width reflow, without device-specific mobile breakpoints or post-upload behavior takeover;
- diagnostic `0.3.6` evidence for viewport/DPR, host/GF/GTB width chain, and representative control widths.

Remaining work is evidence-driven runtime qualification on the exact current packages, including the `320/360/390/393/412/430 CSS px` mobile matrix, responsive/accessibility states, and authentic dynamic add-on states. The Owner-observed narrow whole-form column has **not** been worked around with global page/container CSS: the exact constraining host ancestor must first be identified by diagnostic evidence. Page-background ownership still requires an authentic host seam; Student Photo post-upload/crop composition and PersianGravity presentation remain runtime-dependent and must not be guessed.

## Core approach

Gravity Theme Builder follows this preference order:

1. Preserve Gravity Forms behavior and Foundation mechanics.
2. Use the official Gravity Forms Theme Framework / CSS API first.
3. Express visual intent through semantic theme decisions rather than DOM-specific patches.
4. Add direct CSS only for a demonstrated API gap.
5. Keep adapters narrowly scoped to the actual runtime consumer.
6. Validate on a real Gravity Forms runtime before treating a mapping as proven.

The project does **not** aim to replace Gravity Forms, fork Orbital, recreate form controls, or maintain a parallel validation/layout engine.

## Repository map

```text
.
├── AGENTS.md                         # Repository instructions for coding agents
├── README.md
├── docs/
│   ├── PROJECT_CHARTER.md            # Governing project scope and authority
│   ├── ARCHITECTURE.md               # Technical architecture and boundaries
│   └── THEME_AUTHORING_CONTRACT.md   # Rules for implementing a theme
├── src/                              # Reusable code only after reuse is proven
├── themes/
│   └── srwf-registration/            # First reference implementation
└── tests/                            # Cross-theme / framework validation
```

## Project rules

- Approved design is **input**, not a prompt to redesign.
- Availability of a Gravity Forms API does not authorize a new visual value.
- A visual decision belongs to the theme; the implementation mechanism should belong to the narrowest official Gravity Forms API that can express it.
- `--gf-*` properties are preferred over brittle selector overrides when they provide the required control.
- Foundation/host behavior is preserved unless a concrete requirement proves that an override is necessary.
- `!important`, high-specificity selectors, global `html/body` ownership, and duplicated host behavior require explicit justification.
- New generic abstractions are extracted from repeated real needs; they are not invented in advance.

## First milestone

Implement and production-qualify the approved **SRWF Registration** visual design as a bounded reference theme in a real Gravity Forms environment, including RTL, validation states, responsive behavior, accessibility, Persian content, and required add-ons.

Only after real theme evidence demonstrates reuse should reusable machinery be promoted from `themes/srwf-registration/` into `src/`.

## Documentation authority

`docs/PROJECT_CHARTER.md` governs repository engineering rules and project boundaries. Theme visual authority governs **WHAT** an admitted theme should look like, while current official Gravity Forms documentation/source and inspected runtime evidence govern version-sensitive implementation facts about **HOW** the host behaves.

## License

No license has been selected yet. Do not assume a license until the repository owner chooses one.
