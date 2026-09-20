# Gravity Theme Builder

A reusable engineering project for implementing approved visual designs on the **Gravity Forms Theme Framework**.

The repository is intentionally **design-authority driven**: an approved visual contract defines visual intent; Gravity Forms remains the owner of form behavior, markup, validation, accessibility semantics, and lifecycle.

## Status

**First reference implementation active / SRWF Desktop Full Width shell statically implemented / Owner runtime requalification still open.**

The first reference implementation is:

- `SRWF Registration` — a real-world RTL/Persian public registration form theme.

SRWF is the first proving ground for the system, not a special case that defines every future theme. The current theme implementation is `0.1.18`; diagnostic `0.3.6` remains the bounded runtime-evidence package. Automated/static qualification is necessary evidence, but it does not by itself establish production-browser qualification.

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
- theme `0.1.17` Radio full-cell repair, which neutralizes the Gravity Forms secondary-label horizontal reserve only inside admitted SRWF Radio groups while retaining the explicit `12px` option gap and native Radio semantics; the Owner subsequently confirmed this repair at mobile runtime;
- theme `0.1.18` Desktop Full Width shell modernization, preserving the `904px` outer / `840px` content geometry while adding `32px` desktop block padding, a non-layout `#E4E7EC` boundary ring, and the approved restrained depth;
- diagnostic `0.3.6` evidence for viewport/DPR, host/GF/GTB width chain, representative control widths, and Radio label-fill geometry.

Owner runtime at `390 CSS px` previously proved the intended host-width chain after the dedicated Registration page was configured through the host's native full-width content option (GeneratePress is the currently proven example): the host supplies the full available content area, then GTB owns only its canonical `16px` mobile inline gutter. GTB therefore does not add a GeneratePress dependency, site-wide container override, page-ID rule, negative-margin breakout, or viewport-width hack.

For desktop, the preferred surrounding canvas is `#F6F8FB`. Current GTB source has no safe durable page-level seam that authenticates the admitted Registration page without numeric IDs, DOM position, text, or host-theme internals. The canvas therefore remains a host integration requirement rather than a GTB `html/body/site-content` takeover. The form-local white surface, boundary, depth, and exact width geometry are implemented independently.

Remaining work is evidence-driven runtime requalification of exact theme `0.1.18` + diagnostic `0.3.6`. Desktop should cover `960`, `1024`, representative `1366`/`1440`, and a wide desktop near the prior `~1859 CSS px` baseline where practical. Responsive regression should cover `320/360/390/393/412/430 CSS px`, including Radio full-cell fill, intrinsic wrapping, no horizontal overflow, and unchanged GPFUP/GPAS/Submit behavior. Dynamic focus/validation/open/upload/conditional states remain runtime-sensitive and must not be described as passed from static evidence alone.

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
