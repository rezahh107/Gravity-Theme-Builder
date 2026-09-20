# SRWF Desktop Full Width Shell — Owner Decision — 2026-09-20

Status: **CURRENT_OWNER_SCOPE_AUTHORITY / DESKTOP_SHELL_APPROVED / RUNTIME_QUALIFICATION_REQUIRED**

Authority handle: `OWNER:SRWF-2026-09-20-DESKTOP-SHELL`

## Provenance

This authority records a direct Owner decision made in the active Gravity Theme Builder project conversation after the Owner reviewed the real SRWF Full Width desktop runtime baseline and explicitly approved the Desktop Full Width shell destination.

This is direct Owner-supplied current project authority. It is not Executor-authored implementation prose and it is not represented as an immutable historical Google Drive artifact. No upstream Drive revision ID, export timestamp, content hash, or immutable external blob is claimed for this decision.

## Scope and relationship to existing authority

This decision is bounded to the reopened SRWF Registration desktop shell/background/surface presentation.

`OWNER:SRWF-2026-09-19` remains the base current Owner reconciliation for all unaffected decisions. `OWNER:SRWF-2026-09-20-DESKTOP-SHELL` supersedes it only where the two conflict inside this desktop-shell scope.

All unrelated existing Owner authority remains inherited, including component behavior/presentation boundaries, mobile behavior, Radio, GPFUP, GP Advanced Select / Tom Select, Submit, focus/validation ownership, Section Break semantics, Gravity Flow Entry Detail isolation, and host-layout ownership.

## Approved Desktop Full Width shell destination

At and above the existing production threshold:

```text
min-width: 960 CSS px
```

Preserve:

- outer max width: `904px`;
- authentic content target: `840px`;
- inline padding: `32px` per side;
- surface: `#FFFFFF`;
- outer radius: `16px`.

Add:

- block padding: `32px`;
- subtle visible boundary equivalent to `1px #E4E7EC`;
- restrained depth equivalent to:
  - `0 1px 2px rgba(16,24,40,0.04)`;
  - `0 12px 32px rgba(16,24,40,0.06)`.

The boundary must not reduce the proven `840px` content width. Because the wrapper is `border-box`, a literal `1px` inline border that changes `904px - 32px - 32px = 840px` into an `838px` content result is not the approved geometry. A non-layout-affecting boundary mechanism is therefore preferred.

The approved conceptual composed shadow is:

```css
box-shadow:
    0 0 0 1px #E4E7EC,
    0 1px 2px rgba(16, 24, 40, 0.04),
    0 12px 32px rgba(16, 24, 40, 0.06);
```

The implementation may use an equivalent repository-supported method if it preserves the same authorized geometry and visual result.

Do not add `overflow:hidden` merely for rounded corners because focus rings, Tom Select dropdowns, upload UI, or validation consumers must not be clipped.

## Page canvas ownership

Preferred surrounding desktop canvas: `#F6F8FB`.

Page/background ownership remains host-owned unless GTB already has a truthful authenticated page-level seam for the admitted SRWF Registration presentation. This authority does not authorize generic `html`, `body`, `.site-content`, `.content-area`, `.site-main`, GeneratePress-global selectors, numeric page IDs, negative margins, or `100vw` breakout.

GeneratePress Full Width is a proven host configuration example, not a GTB dependency.

If no safe authenticated page-level seam exists, GTB must still implement the complete form-local white surface/boundary/depth shell and leave `#F6F8FB` as the host/page configuration requirement. A white host canvas alone does not invalidate the form-local shell; the approved boundary and depth should still distinguish the `904px` primary surface.

## Structure and inherited component locks

Keep one dominant primary form surface. This decision does not authorize Section cards, DOM restructuring, field/order assumptions, JavaScript layout reconstruction, or presentation identity based on labels, option text, numeric IDs, `nth-child`, current field counts, or current Section counts.

Below `960px`, the existing mobile system remains inherited: fluid wrapper, canonical `16px` inline gutter, no desktop block-padding requirement, no desktop shell depth requirement, intrinsic Radio/GFPUP reflow, current GPAS behavior, full-width Submit, and no device-name breakpoint matrix.

## Runtime acceptance boundary

This authority approves the destination; it does not prove browser acceptance. Exact implementation must be requalified in the real Owner runtime after static/CI verification. Until that occurs, browser-sensitive shell behavior remains `RUNTIME_QUALIFICATION_REQUIRED`.
