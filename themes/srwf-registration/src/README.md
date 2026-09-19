## SRWF Registration production candidate

Current production package line: **0.1.9**.

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

**Save GTB Configuration** validates the mapping, preserves unrelated Custom CSS classes, projects only GTB-owned semantic tokens, and persists through `GFAPI::update_form()`. `Check Again`, ordinary page render, and `Load Recommended SRWF Draft` are read-only. Shared binary roles are never guessed from label/type/order.

### SRWF Form Presentation Readiness

The same GTB Theme page now reports the host-owned Form Layout destination:

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

The repair delegates route identity to `is_workflow_detail_page()` and ends its early phase at `gravityflow_enqueue_frontend_scripts`. That lifecycle is `SOURCE_PROVEN`; this exact 0.1.9 candidate remains `OWNER_RUNTIME_REQUIRED`.

Pinned source/package evidence retained from the qualified host stack:

- Gravity Flow 3.1.0 package SHA-256: `ac0573b75831380417a21a455176e25eb746d718bbbd0bb70d6da6f48cba5404`;
- Gravity Flow `class-gravity-flow.php` SHA-256: `16666115e37a7704b8331973eba0a0499e039d3fdfc6b47ed8a8e95a41779a79`;
- Gravity Forms 3.1.1.1 package SHA-256: `542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b`.

### Authorized v1 presentation now implemented

The 2026-09-19 Owner reconciliation is implementation-driving. The current CSS implements the safely expressible destination while preserving host behavior ownership:

- mobile-first fluid shell with `16px` inline padding;
- desktop threshold at **960px**;
- desktop border-box card with `904px` outer max width, `32px` inline padding (`840 + 32 + 32`), white surface, `16px` radius, no shadow;
- title `24px` mobile / `26px` desktop, `700 / 1.5`;
- section `18px / 700`, field label `15px / 600`, value `16px / 400`, primary action `16px / 700`;
- helper `14px / 400 / 1.5`, field error `14px / 600 / 1.5`;
- ordinary field rhythm through documented `--gf-form-gap-y:24px`, with a bounded Section Break offset targeting the authorized `32px` major transition;
- documented Gravity Forms focus API values `2px solid #1D4ED8`, offset `2px`; binary cards project native radio focus onto the associated label;
- explicit binary roles only: equal flexible tracks, `12px` gap, minimum `52px`, `10px` radius, `#EDF1FC` selected tint plus non-color border/weight cue;
- explicit mapped Section Break roles only: `40×40` tile, `10px` radius, `20px` admitted local SVG, `#EDF1FC` tint;
- explicit Report Card role only: initial GPFUP min `96px`, pad `16px`, `12px` radius, dashed `#8690A1`; `.gpfup--has-files` remains host-owned.

The implementation uses intrinsic sizing, wrapping, logical properties, and no binary device breakpoint. Host-configured Gravity Forms columns remain authoritative.

### Runtime-proven / bounded add-on adapters

- GP Advanced Select / Tom Select: only the already-proven `.ts-wrapper > .ts-control` minimum visual integration is used. Search/filter/results/selection/keyboard/mobile behavior remains add-on-owned.
- GP File Upload Pro — **Report Card only**: the explicit `srwf-role-report-card-upload` styles only the authentic initial `.gpfup` surface while `:not(.gpfup--has-files)` is true. Upload/progress/validation/preview/delete/crop/storage remain GPFUP-owned.

Student Photo post-upload/crop/re-crop/delete structure remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN**. The historical compatibility label is `RUNTIME_REQUIRED / NOT_IMPLEMENTED`. GPFUP owns that lifecycle and crop configuration. No Report Card markup assumption is generalized to Photo.

PersianGravity/Jalali presentation remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN** until an authentic consumer is captured. No selector or adapter is invented.

### Intentionally unresolved host boundaries

The surrounding page color `#F6F8FB` is **HOST_INTEGRATION_REQUIRED** because the repository does not currently prove a narrow SRWF-owned page/embed container. GTB therefore does not seize `html`, `body`, page IDs, URLs, or unrelated theme wrappers.

### Verification boundary

Repository tests verify authority hash integrity, scoping, CSS/API constants, semantic-role isolation, Entry Detail exclusion, settings/readiness mutation contracts, diagnostic privacy, PHP syntax, and deterministic package closure. They do not prove computed browser layout, real keyboard behavior, actual upload lifecycle, real validation/AJAX behavior, PersianGravity structure, page-background integration, 200% text, increased text spacing, or rendered contrast on the Owner site.
