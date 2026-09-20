## SRWF Registration production candidate

Current production package line: **0.1.18**.

The SRWF Registration implementation is theme-local under `src/`. It is **not production-qualified** until the bounded Owner WordPress/browser checks are completed.

### Install-required source tree

Install/copy the complete `src/` tree as one WordPress plugin directory:

```text
src/
├── srwf-registration-theme.php
├── srwf-registration-settings.php
├── srwf-registration-layout.php
├── srwf-registration.css
└── icons/
    ├── report-card-file.svg
    ├── student-photo-upload.svg
    ├── section-contact.svg
    ├── section-education.svg
    ├── section-identity.svg
    ├── section-school-documents.svg
    └── section-student-photo.svg
```

The CSS uses relative local `icons/...` URLs. Deterministic package checks verify the full dependency closure.

### Per-form activation and semantic setup

Normal operation does not require the Owner to maintain GTB-owned Custom CSS Class tokens manually. Use **Gravity Forms → Form Settings → GTB Theme**.

The settings surface uses Gravity Forms' supported `gform_form_settings_menu` and `gform_form_settings_page_gtb_theme` seams. There is no top-level GTB admin menu. Activation is stored separately from explicit semantic mappings. Numeric field IDs in this admin UI are internal Form Object references only; they are never public CSS identity.

The current Owner lock does **not** require a semantic mapping to obtain Radio card presentation. Every authentic Gravity Forms Radio field inside an admitted SRWF Registration render uses the same card presentation based on host field type. Existing binary semantic roles remain compatible configuration data but do not gate cards.

### SRWF Form Presentation Readiness

The GTB Theme page reports the host-owned Form Layout destination:

- Label Placement: `top_label`;
- Description Placement: `above`;
- Validation Message Placement: `above`;
- Sub-label Placement: `above`;
- Validation Summary: `true`;
- Required Field Indicator: `asterisk`.

Together these establish the intended **above-input** presentation where Gravity Forms supports it. **Apply Recommended SRWF Form Layout** remains a separate explicit action using `GFAPI::update_form()`. Gravity Forms remains authoritative for required state, ARIA, validation, rerender lifecycle, and its native required legend.

### Rendering-context ownership boundary

The stored `srwf-registration-theme` class establishes form identity only. Presentation is admitted only when the current rendering context permits Registration ownership.

Normal Registration, validation rerenders, and legitimate Registration AJAX renders remain admitted. Gravity Flow Entry Detail remains excluded using the source-qualified early enqueue classification plus the authentic `gravityflow_entry_detail_content_before` / `gravityflow_entry_detail_content_after` bracket. GTB does not parse URLs, query strings, page IDs, labels, form IDs, or GPP state.

### Authorized responsive and desktop-shell presentation

Theme `0.1.18` preserves the established component system and adds only the Owner-approved Desktop Full Width shell refinement:

- mobile-first fluid SRWF wrapper with canonical `16px` inline padding;
- desktop threshold at **960px** and no 320/360/390/393/412/430 device-specific production media queries;
- desktop border-box primary surface with `904px` outer max width and `32px` inline padding, preserving the `840px` authentic content geometry target;
- desktop `32px` block padding;
- surface `#FFFFFF` and outer radius `16px`;
- non-layout-affecting `1px #E4E7EC` visual ring plus restrained depth equivalent to `0 1px 2px rgba(16,24,40,0.04), 0 12px 32px rgba(16,24,40,0.06)`;
- no literal wrapper border that would reduce the content box, and no `overflow:hidden` that could clip focus, Tom Select, GPFUP, or validation consumers;
- all authentic Radio fields retain the common card family and intrinsic `.gchoice { flex: 1 1 9.5rem; }` wrapping with `--gf-label-space-x-secondary: 0`;
- native/enhanced Select behavior and existing GP Advanced Select / Tom Select presentation remain unchanged;
- shared initial GPFUP family remains limited to `:not(.gpfup--has-files)`, with its existing `13rem` intrinsic content basis, `student-photo-upload.svg` photo glyph, and Report Card glyph;
- Submit remains full available form width under the existing bounded rule.

The major Section rhythm remains content/host driven. Current Gravity Forms `--gf-form-gap-y:24px` plus the existing authentic Section Break `margin-block-start:8px` already yields the intended `32px`; theme `0.1.18` therefore adds no per-section card, fixed-height wrapper, DOM-count rule, field-ID rule, `nth-child`, label-text, or option-text layout identity.

### Host full-width and canvas prerequisites

Owner runtime previously established the intended width chain after the dedicated Registration page was configured through its host theme's native full-width content option. GeneratePress is the currently proven host example; it is **not** a dependency of GTB.

The framework-neutral width requirement remains:

> The page hosting the SRWF Registration surface must provide the required full-width content area. GTB then owns its scoped wrapper geometry.

For the preferred Desktop Full Width hierarchy, the surrounding host/page canvas should be `#F6F8FB`. Current GTB source has no truthful durable page-level seam that authenticates the SRWF Registration page independently of numeric IDs, DOM position, text, or GeneratePress internals. Theme `0.1.18` therefore intentionally leaves the canvas **host-owned / HOST_INTEGRATION_REQUIRED** instead of styling generic `html`, `body`, `.site-content`, `.content-area`, `.site-main`, `.inside-article`, `.entry-content`, page IDs, using negative margins, or using `100vw` breakout logic.

The form-local white surface/boundary/depth is complete without that host canvas. To obtain the full approved composition, configure the Registration host page/theme so its surrounding desktop canvas is `#F6F8FB` while preserving the existing full-width content area.

### Radio full-cell repair retained from 0.1.17

After host width was corrected, Owner runtime isolated a repeatable Radio defect: Gravity Forms' secondary-label horizontal reserve remained active even though SRWF moves the authentic Radio input out of flow and draws the visible cue inside its label. Theme `0.1.17` neutralized only `--gf-label-space-x-secondary` inside admitted SRWF Radio groups.

The Owner subsequently confirmed the repaired mobile Radio presentation/runtime. Theme `0.1.18` does not alter that repair, the explicit `12px` group gap, the `9.5rem` intrinsic basis, selected/unselected values, or native Radio input/label/checked/focus semantics.

### Add-on presentation boundaries

- **GP File Upload Pro — initial state only**: all GPFUP presentation rules remain limited to `:not(.gpfup--has-files)`. Report Card specialization remains explicit, while Student Photo uses the authentic `gpfup--images-only` initial-state seam.
- Student Photo post-upload/crop/re-crop/delete structure remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN**.
- Upload/progress/validation/preview/delete/crop/storage remain GPFUP-owned.
- GP Advanced Select / Tom Select retains its existing visual adapter only; open/close/search/value behavior remains add-on-owned.

### Diagnostic / Owner requalification

Diagnostic package **0.3.6** remains current and is unchanged because this batch adds no diagnostic source/schema requirement. Its existing bounded, admin-gated collectors provide the width chain, overflow, Radio geometry, and representative component evidence required for requalification.

Static tests and exact-head CI can prove scoping, source contracts, package closure, exact visual-reference identity, shell geometry declarations, version coherence, and absence of host-layout takeover. They do **not** prove browser visual fidelity or dynamic host states.

Requalify exact theme `0.1.18` + diagnostic `0.3.6` at desktop `960`, `1024`, representative `1366`/`1440`, and a wide desktop near the earlier `~1859 CSS px` baseline where practical. Responsive regression should cover `320 / 360 / 390 / 393 / 412 / 430 CSS px`.

Where practical also check authentic keyboard `:focus-visible`, invalid submission, GPAS open state, GPFUP post-upload state, and conditional field reveal. The Owner browser must establish that the 904/840 geometry, restrained ring/shadow, Submit width, two-column GF layout, RTL flow, no clipping, and mobile transition behave as intended.

### Reuse boundary

This shell remains theme-local. It is not a shared multi-theme abstraction, GeneratePress adapter, page-layout subsystem, or replacement Gravity Forms layout engine.
