# Owner Runtime Evidence — SRWF Binary Choice Layout Repair

Date: 2026-09-18

Status: **REPAIR IMPLEMENTED / STATIC QUALIFICATION REQUIRED / OWNER RUNTIME RECHECK REQUIRED**

## Observed runtime failure

On the admitted SRWF Registration surface, the semantic `srwf-role-binary-choice` selector is proven to match: its native Gravity Forms radio inputs receive the existing visually-hidden input treatment. However, the two visible choice cards remain vertically stacked.

The authentic Gender and Graduation Status fields carry Gravity Forms' `gfield--choice-align-vertical` modifier. The approved visual target requires these two semantic consumers to present exactly two equal-width cards in one row while retaining native radio semantics.

Numeric form/field IDs observed during runtime inspection are evidence only and are not production selector identity.

## Root cause

The production role rule set `display: flex` and the approved gap on `.gfield_radio`, but did not set `flex-direction`. Gravity Forms' authentic vertical-choice alignment therefore remained authoritative for the choice-list direction. The existing child-card rules were active, which explains why the cards looked partially correct while the list remained vertical.

Current Gravity Forms documentation identifies `gfield--choice-align-vertical` / `gfield--choice-align-horizontal` as the Multiple Choice alignment hooks and confirms the authentic structure `ginput_container_radio → gfield_radio → gchoice`.

## Repair

Only inside:

`SRWF admitted Registration wrapper + .gfield.srwf-role-binary-choice`

GTB now establishes:

- `.gfield_radio { display:flex; flex-direction:row; gap:12px; inline-size:100%; }`
- each authentic `.gchoice` remains `flex:1 1 0; min-inline-size:0;`
- each associated label fills its choice cell with `inline-size:100%`;
- native radio inputs, checked state, label association, focusability, keyboard navigation, required state, validation and conditional visibility remain Gravity Forms-owned.

No generic `.gfield--type-radio`, `.gfield--choice-align-vertical`, `.gfield_radio` or `.gchoice` rule was added. Ordinary radio groups remain host-owned.

## Version reality

Canonical `main` at the start of this repair is `0.1.5`, while the Owner runtime evidence under repair comes from an already-installed `0.1.6` candidate. The repair package therefore uses `0.1.7` to avoid producing a second, behaviorally different `0.1.6` artifact.

## Qualification boundary

Static tests and exact-Head CI can prove selector scope, authentic fixture structure, native association, checked-state styling, package closure and regression safety. They cannot prove the final geometry in the Owner's real Gravity Forms runtime.

Required closure evidence is an Owner runtime recheck showing Gender and visible Graduation Status with two equal-width choices on one row, plus the bounded binary-choice geometry diagnostic.
