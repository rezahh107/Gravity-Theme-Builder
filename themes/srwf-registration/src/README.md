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

Normal operation does not require the Owner to maintain GTB-owned Custom CSS Class tokens manually. Use:

**Gravity Forms → Form Settings → GTB Theme**

The settings surface uses Gravity Forms' supported `gform_form_settings_menu` and `gform_form_settings_page_gtb_theme` seams. There is no top-level GTB admin menu.

Activation is stored separately from explicit semantic mappings. Numeric field IDs in this admin UI are internal Form Object references only; they are never public CSS identity. **Save GTB Configuration** validates the mapping, preserves unrelated Custom CSS classes, projects only GTB-owned semantic tokens, and persists through `GFAPI::update_form()`. Read-only checks never guess semantic roles from label/type/order.

The current Owner lock does **not** require a semantic mapping to obtain Radio card presentation. Every authentic Gravity Forms Radio field inside an admitted SRWF Registration render uses the same card presentation based on the host field type. Existing binary semantic roles remain compatible configuration data but do not gate cards.

### SRWF Form Presentation Readiness

The GTB Theme page reports the host-owned Form Layout destination:

- Label Placement: `top_label`;
- Description Placement: `above`;
- Validation Message Placement: `above`;
- Sub-label Placement: `above`;
- Validation Summary: `true`;
- Required Field Indicator: `asterisk`.

Together these placement values establish the intended **above-input** presentation where Gravity Forms supports it. **Apply Recommended SRWF Form Layout** remains a separate explicit action which re-reads the current Form Object, changes only the admitted properties, persists through `GFAPI::update_form()`, and verifies read-back. Gravity Forms remains authoritative for required state, ARIA, validation, rerender lifecycle, and its native required legend.

### Rendering-context ownership boundary

The stored `srwf-registration-theme` class establishes form identity only. Presentation is admitted only when the current rendering context permits Registration ownership.

Normal Registration, validation rerenders, and legitimate Registration AJAX renders remain admitted. Gravity Flow Entry Detail remains excluded using the source-qualified early enqueue classification plus the authentic `gravityflow_entry_detail_content_before` / `gravityflow_entry_detail_content_after` bracket. GTB does not parse URLs, query strings, page IDs, labels, form IDs, or GPP state.

#### Retained Entry Detail source qualification

PR #12 established an earlier timing assumption that later Owner runtime evidence disproved. The repaired boundary is based on the qualified source order for Gravity Flow `3.1.0` with Gravity Forms `3.1.1.1`: during `wp_enqueue_scripts`, Gravity Flow `enqueue_frontend_scripts()` reaches Gravity Forms `enqueue_form_scripts()`, which invokes the form-owned `gform_enqueue_scripts` and `gform_form_theme_slug` paths before the later Entry Detail content bracket. `gravityflow_enqueue_frontend_scripts` is the source-proven post-enqueue boundary, while `is_workflow_detail_page()` is the authentic host route predicate.

This timing remains `SOURCE_PROVEN`; fresh browser behavior remains `OWNER_RUNTIME_REQUIRED`. The retained source-qualification identities are `16666115e37a7704b8331973eba0a0499e039d3fdfc6b47ed8a8e95a41779a79`, `ac0573b75831380417a21a455176e25eb746d718bbbd0bb70d6da6f48cba5404`, and `542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b`.

### Authorized responsive presentation

Theme `0.1.18` preserves the accepted responsive/component destination and modernizes only the desktop primary surface:

- mobile-first fluid SRWF wrapper with canonical `16px` inline padding;
- desktop threshold at **960px**;
- desktop border-box surface with `904px` outer max width, `32px` inline padding (`840 + 32 + 32`), `32px` block padding, white surface, and `16px` radius;
- desktop boundary is a non-layout `1px #E4E7EC` ring expressed as the first `box-shadow` layer, so the authentic content width remains `840px`;
- desktop depth is `0 1px 2px rgba(16, 24, 40, 0.04)` plus `0 12px 32px rgba(16, 24, 40, 0.06)`;
- no `overflow:hidden` is added to the primary wrapper;
- all authentic Radio fields retain the common card family and intrinsic `.gchoice { flex: 1 1 9.5rem; }` wrapping;
- no device-specific media query for `320`, `360`, `390`, `393`, `412`, or `430`;
- native/enhanced Select behavior and existing GP Advanced Select / Tom Select presentation remain unchanged;
- shared initial GPFUP family remains limited to `:not(.gpfup--has-files)`, with its existing `13rem` intrinsic content basis, `student-photo-upload.svg` photo glyph, and existing Report Card glyph;
- Submit remains full available form width under the existing bounded rule.

The existing `--gf-form-gap-y:24px` plus authentic Section Break `margin-block-start:8px` already produces the Owner's `32px` major section rhythm. No independent section cards, DOM-position rules, or field-count assumptions are added.

### Host full-width and canvas prerequisite

Owner runtime at `390 CSS px` established the intended width chain after the dedicated Registration page was configured through its host theme's native full-width content option. GeneratePress is the currently proven host example; it is not a dependency of GTB.

The product/framework-neutral width requirement is:

> The page hosting the SRWF Registration surface must provide the required full-width content area. GTB then owns its canonical `16px` mobile inline gutter.

In the proven Owner runtime, the host/content chain was `390px`, the SRWF wrapper was `390px` with `16px` inline padding, and the form/ordinary controls/Submit were `358px`; `document.clientWidth` and `scrollWidth` were both `390px`, with no visible overflow among the sampled consumers.

Repository inspection for the Desktop Full Width shell batch found no existing truthful GTB page-level authentication seam for styling the surrounding page canvas without relying on generic `html/body`/site containers, page IDs, or GeneratePress internals. Therefore theme `0.1.18` does **not** implement the preferred `#F6F8FB` page background itself.

The smallest host-side integration requirement is:

> Configure the dedicated SRWF Registration page/canvas to `#F6F8FB` on desktop while preserving the host's full-width content configuration.

Theme `0.1.18` does **not** add GeneratePress selectors, `.site-content`/page-container overrides, page IDs, negative margins, viewport breakout logic, or a new page-layout subsystem. Host page layout and canvas remain host-owned.

### Radio full-cell repair retained from 0.1.17

After the host width was corrected, Owner runtime isolated a separate repeatable Radio defect: paired `.gchoice` cells measured `173px` while their visible labels measured `161px`; full-row choices measured `358px` while labels measured `346px`. The deficit was exactly `12px` in both cases.

Gravity Forms publishes `--gf-label-space-x-secondary` for the horizontal reserve between a choice input and its secondary inline label, with a `12px` default in the qualified Theme Framework. SRWF deliberately moves the authentic Radio input out of flow and renders its visible circular cue inside the associated label. Theme `0.1.17` therefore neutralized only that reserve inside admitted SRWF Radio groups:

```css
.gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio .gfield_radio {
    --gf-label-space-x-secondary: 0;
    display: flex;
    flex-flow: row wrap;
    gap: 12px;
}
```

Theme `0.1.18` leaves this repair unchanged. It does not add `12px` back to card width, change the explicit group gap, alter the `9.5rem` intrinsic basis, or replace the authentic Radio input/label/checked/focus relationship.

### Add-on presentation boundaries

- **GP File Upload Pro — initial state only**: all GPFUP presentation rules remain limited to `:not(.gpfup--has-files)`. Report Card specialization remains explicit, while Student Photo uses the authentic `gpfup--images-only` initial-state seam.
- Student Photo post-upload/crop/re-crop/delete structure remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN**.
- Upload/progress/validation/preview/delete/crop/storage remain GPFUP-owned.
- GP Advanced Select / Tom Select retains its existing visual adapter only; open/close/search/value behavior remains add-on-owned.

### Diagnostic / Owner requalification

Diagnostic package **0.3.6** remains current. No diagnostic source/schema changed in the Desktop Full Width shell batch, so no diagnostic bump is made.

Static tests and exact-head CI can prove scoping, source contracts, package closure, visual-reference identity, version coherence, the `904/840` geometry, `32px` desktop block/inline padding, non-layout boundary and shadow declarations, mobile `16px` gutter retention, and absence of host-layout takeover. They do **not** prove the actual browser-rendered shadow/ring/canvas or non-clipping of authentic dynamic states.

Owner desktop requalification should cover at minimum:

- `960 CSS px`;
- `1024 CSS px`;
- approximately `1366` or `1440 CSS px`;
- a wide desktop close to the prior `~1859 CSS px` baseline where practical.

Responsive regression should cover `320 / 360 / 390 / 393 / 412 / 430 CSS px` and confirm:

- host content remains full-width;
- GTB retains the `16px` mobile gutter;
- no desktop ring/shadow leaks below `960px`;
- no horizontal overflow;
- `allVisibleLabelsFillChoices = true`;
- short choices remain side-by-side where real width permits and larger groups wrap intrinsically;
- GPFUP / GPAS / Submit do not regress;
- native checked/focus/validation/conditional Radio behavior remains Gravity Forms-owned.

Where practical, also recheck authentic keyboard `:focus-visible`, invalid submission, GPAS open state, GPFUP post-upload state, and conditional reveal. Student Photo post-upload/crop/re-crop/delete composition remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN** and GPFUP-owned. PersianGravity/Jalali presentation remains runtime-dependent until an authentic consumer is captured.

### Reuse boundary

The desktop shell refinement and retained Radio repair remain theme-local. They are not promoted to shared `src/`, and the host prerequisites do not create a GeneratePress adapter or page-layout subsystem inside GTB.