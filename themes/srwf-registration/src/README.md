## SRWF Registration production candidate

Current production package line: **0.1.16**.

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

Activation is stored separately from eight semantic mappings: Gender, Graduation Status, Report Card upload, and five Section Break roles. Numeric field IDs in this admin UI are internal Form Object references only; they are never public CSS identity.

**Save GTB Configuration** validates the mapping, preserves unrelated Custom CSS classes, projects only GTB-owned semantic tokens, and persists through `GFAPI::update_form()`. `Check Again`, ordinary page render, and `Load Recommended SRWF Draft` are read-only. Semantic roles are never guessed from label/type/order.

The current Owner lock does **not** require a semantic mapping to obtain Radio card presentation. Every authentic Gravity Forms Radio field inside an admitted SRWF Registration render uses the same card presentation based on the host field type. Existing binary semantic roles remain compatible configuration data but no longer gate cards.

### SRWF Form Presentation Readiness

The same GTB Theme page reports the host-owned Form Layout destination:

- Label Placement: `top_label`;
- Description Placement: `above`;
- Validation Message Placement: `above`;
- Sub-label Placement: `above`;
- Validation Summary: `true`;
- Required Field Indicator: `asterisk`.

Together these placement values establish the intended **above-input** presentation where Gravity Forms supports that placement. This supersedes the older below-input placement choice.

**Apply Recommended SRWF Form Layout** is a separate explicit action. It re-reads the current full Form Object at mutation time, computes only the six-property diff, performs no write if already matching, changes only those six properties, calls `GFAPI::update_form()`, then re-reads and verifies persistence. `customRequiredIndicator` and unrelated form properties are preserved.

Explicit supported field-level placement overrides that conflict with the intended form-level placement are reported as **ATTENTION REQUIRED** and are not silently normalized.

### Required indicator explanation

For `requiredIndicator=asterisk`, Gravity Forms' native required legend is the single explanation surface. GTB does not post-process the generated form HTML, insert a parallel required note, suppress the native legend, or recreate required semantics. Gravity Forms remains authoritative for required state, indicator semantics, ARIA, validation, rerender lifecycle, and legend output.

Unrelated forms and excluded Gravity Flow Entry Detail renders remain outside SRWF presentation ownership; no separate required-explanation path is attached to either surface.

### Rendering-context ownership boundary

The stored `srwf-registration-theme` class establishes form identity only. Presentation is admitted only when the current rendering context permits Registration ownership.

Normal Registration, validation rerenders, and legitimate Registration AJAX renders remain admitted. Gravity Flow Entry Detail remains excluded using the existing source-qualified early enqueue classification plus the authentic `gravityflow_entry_detail_content_before` / `gravityflow_entry_detail_content_after` bracket. GTB does not parse URLs, query strings, page IDs, labels, form IDs, or GPP state. GPP is neither detected nor required.

PR #12 was disproved by Owner runtime because the later content bracket alone did not cover Gravity Flow's early form enqueue. Exact Gravity Flow `3.1.0` and Gravity Forms `3.1.1.1` source qualification established the retained order:

`wp_enqueue_scripts` → Gravity Flow `enqueue_frontend_scripts()` → `enqueue_form_scripts()` → Gravity Forms `gform_enqueue_scripts` / `gform_form_theme_slug`, before `gravityflow_entry_detail_content_before`.

The repair delegates route identity to `is_workflow_detail_page()` and ends its early phase at `gravityflow_enqueue_frontend_scripts`. That lifecycle is `SOURCE_PROVEN`; this exact 0.1.16 candidate remains `OWNER_RUNTIME_REQUIRED`.

Pinned source/package evidence retained from the qualified host stack:

- Gravity Flow 3.1.0 package SHA-256: `ac0573b75831380417a21a455176e25eb746d718bbbd0bb70d6da6f48cba5404`;
- Gravity Flow `class-gravity-flow.php` SHA-256: `16666115e37a7704b8331973eba0a0499e039d3fdfc6b47ed8a8e95a41779a79`;
- Gravity Forms 3.1.1.1 package SHA-256: `542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b`.

### Authorized v1 visual repair and mobile responsive polish

The 2026-09-19 Owner reconciliation remains implementation-driving. Theme `0.1.16` preserves the accepted visual destination and tightens only content/space-driven responsive behavior:

- mobile-first fluid shell with `16px` inline padding;
- desktop threshold at **960px**;
- desktop border-box card with `904px` outer max width, `32px` inline padding (`840 + 32 + 32`), white surface, `16px` radius, no shadow;
- target font stack: `Vazirmatn, Vazir, Tahoma, Arial, sans-serif`;
- title `24px` mobile / `26px` desktop, `700 / 1.5`;
- section `18px / 700 / 1.5`, field label `15px / 600 / 1.5`, value `16px / 400 / 1.5`, primary action `16px / 700 / 1.5`;
- helper `14px / 400 / 1.5`, field error `14px / 600 / 1.5`;
- ordinary controls retain minimum `52px`; Submit retains minimum `56px` and full available form width;
- ordinary field rhythm remains `24px`; major section rhythm remains `32px`;
- documented Gravity Forms focus API values remain `2px solid #1D4ED8`, offset `2px`; native Radio focus still projects onto the visible associated card;
- native/enhanced Select behavior and the previously qualified select-family alignment remain unchanged;
- **all authentic Radio fields** inside admitted SRWF still use the common card family, but `.gchoice` now uses the intrinsic `9.5rem` basis and a flexible label-fill relationship. This causes a genuinely narrow component to stack before labels are crushed while still allowing short pairs to share a row when enough container width exists. Cards remain minimum-height, not fixed-height;
- no device-specific media query is added for `320`, `360`, `390`, `393`, `412`, or `430`;
- explicit mapped Section Break roles remain `40×40` tile, `10px` radius, `20px` local SVG, `#EDF1FC` tint, `12px` icon-heading gap;
- the shared initial GPFUP family remains min `96px`, pad `16px`, radius `12px`, `1px` dashed `#8690A1`, with one `40×40` icon slot and `24px` glyph for both Report Card and image-only Student Photo;
- the authentic initial GPFUP direct content child now uses an intrinsic `13rem` basis and `max-inline-size:100%`, so it may wrap below the icon rather than shrink into a tiny text column. The compact horizontal cluster remains possible where the real component width supports it;
- all GPFUP presentation rules remain limited to `:not(.gpfup--has-files)`. Upload/progress/validation/preview/delete/crop/storage remain host-owned.

The implementation uses intrinsic sizing, wrapping, logical properties, and no field-ID/label/order specialization. Host-configured Gravity Forms columns remain authoritative.

### Mobile width ownership and diagnostic evidence

Static source establishes that the SRWF wrapper itself is `inline-size:100%`, `max-inline-size:100%`, with `16px` inline padding on mobile. Its artificial content cap appears only at `@media (min-width: 960px)` where the Owner-authorized desktop `904px` outer destination applies.

Therefore theme `0.1.16` does **not** add negative margins, global `html/body` sizing, arbitrary WordPress container overrides, or a page-template breakout to compensate for the Owner-observed narrow mobile screenshot. The exact ancestor that loses width on the real Owner page is a runtime fact, not something source inspection can identify truthfully.

Install diagnostic package **0.3.6** for the next qualification pass. It adds bounded privacy-safe width-chain evidence:

- `window.innerWidth` and `devicePixelRatio`;
- SRWF wrapper rect and computed width/max-width/padding;
- immediate Gravity Forms form/body/fields geometry;
- bounded ancestors up to `body`, including rect and computed width/max-width/padding/margin/overflow;
- representative text control, Radio group, initial GPFUP droparea, and Submit widths.

The diagnostic remains admin-gated and does not read field text or values. Its two download controls remain functional but are parked in normal document flow by the final composer so they do not remain fixed over product controls during captures.

### Runtime-proven / bounded add-on adapters

- Native Gravity Forms single Select: the documented `--gf-ctrl-select-padding-x` API owns the common inline text/indicator reserve. A direct SRWF-scoped `padding-block-start:14px` is retained only for authentic non-enhanced single-select controls because current public Select API exposes no select-specific vertical-padding token and Owner runtime proved that optical compensation closes the remaining value alignment defect. The rule does not depend on field ID, label text, description state, sub-label placement, or DOM order.
- GP Advanced Select / Tom Select: only the already-proven `.ts-wrapper > .ts-control` visible control is targeted. Its closed-control box reuses the same `--gf-ctrl-select-padding-x` family token plus the accepted SRWF 52px/1.5 metric family and established SRWF focus visual. The hidden source `<select>` is not treated as a native visible consumer. Tom Select still owns caret drawing, search/filter/results, open/close, selection, keyboard behavior, and synchronization. Authentic post-repair Owner-browser geometry remains `OWNER_RUNTIME_REQUIRED`.
- GP File Upload Pro — initial state only: Report Card specialization remains explicit through `srwf-role-report-card-upload` and its local document glyph; authentic `gpfup--images-only` Student Photo uses the same decorative icon-slot geometry with its own GTB-owned photo/camera glyph. Theme `0.1.16` changes only the intrinsic wrapping behavior of their authentic direct content child. Upload/progress/validation/preview/delete/crop/storage remain GPFUP-owned; the theme adds no replacement upload markup or JavaScript lifecycle.

Student Photo post-upload/crop/re-crop/delete structure remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN**. GPFUP owns that lifecycle and crop configuration. No post-upload composition is invented.

PersianGravity/Jalali presentation remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN** until an authentic consumer is captured. No selector or adapter is invented.

### Intentionally unresolved host boundaries

The surrounding page color `#F6F8FB` and any Owner-site mobile page/content width constraint are **HOST_INTEGRATION_REQUIRED** unless a dedicated authenticated SRWF page/integration seam is proven. GTB therefore does not seize `html`, `body`, page IDs, URLs, or unrelated theme wrappers.

### Verification boundary

Repository tests verify authority hash integrity, SRWF scoping, CSS/API constants, all-radio field-type coverage, intrinsic Radio/GPFUP rules, no fixed radio-card height, no device-width media queries, shared initial GPFUP geometry, local asset closure, Entry Detail exclusion, settings/readiness mutation contracts, diagnostic privacy, diagnostic width-chain structure, PHP/JavaScript syntax, exact-head package closure, and version coherence.

They do **not** prove the Owner-site ancestor width chain, computed browser layout at `320/360/390/393/412/430 CSS px`, visual balance, real keyboard/checked/invalid/open/uploaded states, PersianGravity structure, page-background integration, `200%` text resize, increased text spacing, or rendered contrast/target-size acceptance. Those remain Owner-runtime qualification obligations for theme `0.1.16` + diagnostic `0.3.6`.
