# Gravity Forms Theme Framework — Canonical Validation Report

**Validation date:** 2026-09-17  
**Baseline:** latest supplied `Gravity Forms Theme Framework — Canonical Engineering Reference`  
**Sources:** current official Gravity Forms-owned documentation only  
**Candidate current `--gf-*` identifiers checked:** 748

## A. Changes made

| Location | Old issue | Verified official evidence | Repair |
|---|---|---|---|
| YAML front matter | The baseline used a broad `authority: "Official Gravity Forms Documentation"` field that could misstate the local snapshot's authority domain and represented only one source root. | The local file is project-owned; current Gravity Forms implementation facts remain governed by the official documentation roots used throughout the reference. | Replaced with `authority_domain: "implementation-fact-evidence"`, `authority_source`, both `source_roots`, valid `---` delimiters, and evidence-based status. |
| §3.1 / §16.11 — Gravity Forms 2.5 wrapper | The preferred table used `.gravity-theme` but the live upstream contradiction with `.gform_theme` was no longer explicit. | Quick Start, Core Concepts, and CSS Element Naming Structure publish `.gravity-theme`; the current Theme Framework FAQ still publishes `.gform_theme`. | Kept `.gravity-theme` as the preferred wrapper supported by the wrapper-specific/current structure sources, restored `DOCUMENTATION AMBIGUOUS`, identified both source sides, and prohibited treating the spellings as interchangeable without runtime/source verification. |
| §5.2 / §12.4 / §16.12 — focus styling | The current Colors page contains a `Used by` reference that could be mistaken for a current control API identifier. | Colors references `--gf-ctrl-shadow-color-focus`; the dedicated current Controls — Base API does not define it and instead defines current border/outline focus properties. | Added explicit ambiguity; excluded the disputed name from the current usable API set and retained the dedicated Controls — Base inventory for new code. |
| §11.1 — `gform_default_styles` | Needed revalidation that the complete key list is a style-setting contract rather than raw CSS custom properties. | Dedicated hook documentation lists `theme`, input/label/description/button keys and Image Choice keys as accepted properties. | Revalidated the full list and preserved the explicit “style-setting keys ≠ arbitrary raw `--gf-*` names” boundary. |
| §6.3 — Choice Controls | Previously high-risk area; current candidate already contained repaired names. | Current Choice Controls API defines `--gf-ctrl-checkbox-check-*`, `--gf-ctrl-radio-check-*`, and `--gf-ctrl-choice-*` base sizing/color properties. | Revalidated exact current identifiers/defaults; retained only explicitly labeled negative aliases. No new identifier repair was required in this pass. |
| §7.2 — Date Field | Previously high-risk area; current candidate already contained repaired names. | Current Date Field API defines `--gf-field-date-ctrl-padding-x-end`, `--gf-field-date-icon-*`, and `--gf-field-date-custom-icon-*`. | Revalidated exact current identifiers/defaults; retained only explicitly labeled rejected aliases. No new identifier repair was required in this pass. |
| §15.5 — Gravity Forms 3.0 | Required current-version revalidation. | Current submit-selector/upgrade/changelog docs confirm `<button>` submit controls, spinner inside button with `.gform-has-spinner` / `.gform-loader`, removed legacy spinner hooks, and WhatSock replacing jQuery UI for datepicker. | Preserved current guidance and source boundaries. |
| §11.2 — custom-theme registration | Required revalidation against possible confusion with Theme Layers. | Current Theme Framework FAQ states: “You cannot currently register a form theme.” | Preserved the limitation; Theme Layers are not treated as evidence of a first-class public form-theme registration API. |
| §20.1 — validation evidence | Gates existed only as maintenance rules; no execution record accompanied the baseline. | Candidate was audited against all current official CSS API branches and the relevant dedicated official docs. | Added `Canonical Validation Record` with actual gate results, counts, repairs, and unresolved upstream ambiguities. |

### Primary official evidence used for repairs

- Choice Controls API: https://docs.css.gravity.com/framework.controls.choice._api-global.html
- Date Field API: https://docs.css.gravity.com/framework.fields.date._api-global.html
- Controls — Base API: https://docs.css.gravity.com/framework.controls.default._api-global.html
- Colors API: https://docs.css.gravity.com/framework.api._colors.html
- `gform_default_styles`: https://docs.gravityforms.com/gform_default_styles/
- Quick Start Guide: https://docs.gravityforms.com/quick-start-guide/
- Core Concepts: https://docs.gravityforms.com/theme-framework/
- CSS Element Naming Structure: https://docs.gravityforms.com/basic-structure/
- Theme Framework FAQ: https://docs.gravityforms.com/theme-framework-faq/
- Submit Button CSS Selectors: https://docs.gravityforms.com/submit-button-css-selectors/
- Gravity Forms 3.0 upgrade checks: https://docs.gravityforms.com/checks-before-upgrading-to-gravity-forms-3-0/
- Gravity Forms changelog: https://docs.gravityforms.com/gravityforms-change-log/

## B. Integrity gates

| Gate | Result | Validation outcome |
|---|---|---|
| GATE A — ZERO-INVENTION | **PASS** | Extracted 748 unique exact current usable `--gf-*` identifiers. Every one was matched by exact spelling to its current official owning CSS API page or explicit current official CSS API documentation. Explicit historical/incorrect/conflict/wildcard literals were excluded only where unambiguously labeled as such. |
| GATE B — API-FIDELITY | **PASS** | Exhaustively checked the API records represented in §§4–8 against the owning current official pages. Copied defaults, dependencies, states, and owner/category claims are consistent with current official evidence. Upstream self-conflicts/incomplete defaults are preserved as ambiguity rather than silently repaired. |
| GATE C — SOURCE-DOMAIN AUTHORITY | **PASS** | Exact CSS identifiers/defaults use dedicated CSS API pages; hook contract uses dedicated hook docs; architecture uses Theme Framework docs; markup/version transitions use dedicated selector/upgrade/current docs. |
| GATE D — INTERNAL TOKEN BOUNDARY | **PASS** | All `--gform-theme-*` occurrences are explicitly internal/implementation-detail dependencies and are not promoted into the public `--gf-*` contract. |
| GATE E — HISTORICAL API BOUNDARY | **PASS** | Historical/pre-2.8/conflicting identifiers are clearly labeled and cannot be mistaken for recommended current API. |
| GATE F — QUICK LOOKUP FIDELITY | **PASS** | Every exact property in Quick Lookup resolves to a current verified API entry; wildcard forms are explicitly navigation shorthand and not literal identifiers. |

## C. Identifier validation

```text
current identifiers checked: 748
unverified identifiers: 0
repaired identifiers: 0
```

`repaired identifiers: 0` is intentional: the supplied baseline already contained the earlier Choice and Date identifier repairs. This pass **revalidated** those high-risk families rather than claiming to repair them again.

Explicit negative/historical/conflict examples were not counted as current usable identifiers. In particular:

- Choice aliases such as `--gf-ctrl-choice-checkbox-radius` remain labeled nonexistent.
- Date aliases such as `--gf-field-date-ctrl-icon-color` remain labeled nonexistent.
- `--gf-ctrl-shadow-color-focus` remains documentation-conflict evidence, not current usable API.
- Design Overview/historical examples such as `--gf-ctrl-border-size`, `--gf-ctrl-padding-inline`, `--gf-control-bg-color-focus`, and `--gf-ctrl-color-invalid` remain non-current/conflict evidence.
- Wildcard strings such as `--gf-ctrl-date-picker-*` are navigation shorthand only.

## D. Remaining upstream ambiguities

1. **Gravity Forms 2.5 wrapper conflict** — Quick Start, Core Concepts, and CSS Element Naming Structure publish `.gravity-theme`; Theme Framework FAQ still publishes `.gform_theme`.
2. **Focus-shadow reference conflict** — Colors lists `--gf-ctrl-shadow-color-focus` in `Used by`; dedicated Controls — Base does not define it.
3. **Design Overview stale/conflicting names** — high-level examples include names such as `--gf-ctrl-border-size` / `--gf-ctrl-padding-inline` while dedicated current Controls API uses `--gf-ctrl-border-width` / `--gf-ctrl-padding-x`.
4. **Historical CSS API naming examples** — architecture/upgrade material can contain pre-2.8 property forms.
5. **Simple-button self-reference** — current Button API publishes `--gf-ctrl-btn-icon-color-focus-simple` with a self-referential default.
6. **Enhanced-select missing default** — current Select API defines `--gf-ctrl-select-dropdown-option-shadow-hover` but leaves its default cell empty.
7. **Internal dependencies in public defaults** — some public API defaults reference internal-looking `--gform-theme-*` values.
8. **Modifier dash rendering** — some Core Concepts utility modifier names are rendered with ambiguous dash characters.

These ambiguities are explicitly preserved in the revised reference and therefore do not become invented current API.

## E. Canonical conclusion

```text
CANONICAL_READY
```

All six gates completed with `PASS`. The revised front matter therefore uses:

```yaml
status: "canonical-project-reference"
```
