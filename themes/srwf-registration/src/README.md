## SRWF Registration production candidate

Current production package line: **0.1.19**.

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

### Authority chain and Desktop Full Width shell in 0.1.19

`OWNER:SRWF-2026-09-19` remains the base current Owner reconciliation for unaffected decisions.

The Desktop Full Width shell is separately admitted under:

```text
authority_handle: OWNER:SRWF-2026-09-20-DESKTOP-SHELL
path: ../reference/SRWF_DESKTOP_SHELL_OWNER_DECISION_2026-09-20.md
status: CURRENT_OWNER_SCOPE_AUTHORITY / DESKTOP_SHELL_APPROVED / RUNTIME_QUALIFICATION_REQUIRED
```

The handle is registered in `../reference/VISUAL_AUTHORITY.md`. It is direct Owner-supplied current project authority, not implementation prose and not a fabricated immutable Drive artifact. It supersedes `OWNER:SRWF-2026-09-19` only where the two conflict inside the bounded desktop-shell scope.

Theme `0.1.19` consumes that admitted destination at the existing **960px** desktop threshold:

- mobile-first fluid wrapper remains `16px` inline padding below the threshold;
- desktop outer max remains `904px`;
- desktop inline padding remains `32px` per side, preserving the authentic `840px` content target (`904 - 32 - 32`);
- desktop block padding is `32px`;
- primary surface remains `#FFFFFF` with `16px` radius;
- boundary is a non-layout `1px #E4E7EC` ring, so it does not consume content width;
- restrained depth is `0 1px 2px rgba(16,24,40,0.04)` plus `0 12px 32px rgba(16,24,40,0.06)`;
- no literal layout-consuming border or `overflow:hidden` is introduced;
- one dominant form surface remains; Section Breaks are not turned into independent cards;
- no device-specific media query is added for `320`, `360`, `390`, `393`, `412`, or `430`.

The preferred surrounding `#F6F8FB` page canvas remains host-owned because GTB still has no separately authenticated page-level seam that would justify taking over `html`, `body`, generic site containers, page IDs, or GeneratePress internals. GeneratePress Full Width remains a proven host configuration example, not a GTB dependency.

### Historical authority/provenance repair in 0.1.18

Theme `0.1.18` remains the PR #28 authority/provenance repair. It removed an unsupported self-authored later desktop-shell supersession, restored the then-admitted no-depth shell, and added the deterministic provenance guard.

That guard remains active in `0.1.19`: a later-dated direct Owner supersession is accepted only when it resolves to a separately registered/admitted Owner authority handle. The new desktop-shell decision passes because `OWNER:SRWF-2026-09-20-DESKTOP-SHELL` is now separately recorded and registered; unknown handles and fabricated implementation prose still fail qualification.

### Host full-width prerequisite

Owner runtime at `390 CSS px` established the intended width chain after the dedicated Registration page was configured through its host theme's native full-width content option. GeneratePress is the currently proven host example; it is not a dependency of GTB.

The product/framework-neutral requirement is:

> The page hosting the SRWF Registration surface must provide the required full-width content area. GTB then owns its canonical `16px` mobile inline gutter.

In the proven Owner runtime, the host/content chain was `390px`, the SRWF wrapper was `390px` with `16px` inline padding, and the form/ordinary controls/Submit were `358px`; `document.clientWidth` and `scrollWidth` were both `390px`, with no visible overflow among the sampled consumers.

### Radio full-cell repair retained from 0.1.17

After the host width was corrected, Owner runtime isolated a separate repeatable Radio defect: paired `.gchoice` cells measured `173px` while their visible labels measured `161px`; full-row choices measured `358px` while labels measured `346px`. The deficit was exactly `12px` in both cases.

Gravity Forms publishes `--gf-label-space-x-secondary` for the horizontal reserve between a choice input and its secondary inline label, with a `12px` default in the qualified Theme Framework. SRWF deliberately moves the authentic Radio input out of flow and renders its visible circular cue inside the associated label. The normal input-to-label reserve is therefore no longer needed for this presentation.

The retained repair sets:

```css
.gform-theme--framework.srwf-registration-theme_wrapper .gfield.gfield--type-radio .gfield_radio {
    --gf-label-space-x-secondary: 0;
    display: flex;
    flex-flow: row wrap;
    gap: 12px;
}
```

This is not a `+12px` width compensation. The explicit `12px` group gap remains the option-to-option spacing authority; `.gchoice` keeps its `9.5rem` intrinsic basis; labels remain content-height driven; the authentic Radio input/label/checked/focus relationship remains intact; selected border/background/cue values are unchanged.

### Add-on presentation boundaries

- **GP File Upload Pro — initial state only**: all GPFUP presentation rules remain limited to `:not(.gpfup--has-files)`. Report Card specialization remains explicit, while Student Photo uses the authentic `gpfup--images-only` initial-state seam.
- Student Photo post-upload/crop/re-crop/delete structure remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN**.
- Upload/progress/validation/preview/delete/crop/storage remain GPFUP-owned.
- GP Advanced Select / Tom Select retains its existing visual adapter only; open/close/search/value behavior remains add-on-owned.
- Submit remains full available content width with the current `56px` minimum and action styling.

### Diagnostic / Owner requalification

Diagnostic package **0.3.6** remains current. No diagnostic bump is needed because diagnostic source/schema is unchanged.

Static tests and exact-head CI can prove scoping, source contracts, package closure, visual-reference identity, version coherence, authority provenance, shell declarations, and absence of host-layout takeover. They do **not** prove real browser rendering.

The required Owner runtime pass remains desktop `960`, `1024`, approximately `1366/1440`, and a wide desktop where practical, plus responsive `320 / 360 / 390 / 393 / 412 / 430 CSS px`. Also recheck authentic keyboard focus, invalid submission, GPAS open state, GPFUP post-upload state where available, and conditional reveal.

Until exact theme `0.1.19` + diagnostic `0.3.6` are exercised in the Owner browser, `OWNER_RUNTIME_REQUALIFICATION: NOT_PROVEN`.

Student Photo post-upload/crop/re-crop/delete composition remains **OWNER_RUNTIME_REQUIRED / NOT_PROVEN** and GPFUP-owned. PersianGravity/Jalali presentation remains runtime-dependent until an authentic consumer is captured.

### Reuse boundary

The scoped desktop-shell implementation, provenance guard, and retained Radio repair remain theme-local. The host full-width prerequisite does not create a GeneratePress adapter or page-layout subsystem inside GTB.
