# Owner Visual Recheck — Radio Choice Presentation — 2026-09-18

Evidence class: **Owner runtime visual feedback**

This record supplements `OWNER_RUNTIME_GTB_CONFIGURATION_2026-09-18.md`.
It does not replace the admitted visual authority under `reference/` and it does not
promote screenshots or Owner feedback into a new design specification.

## Tested build

Owner-tested Registration package: **0.1.6**.

The earlier runtime configuration proof remains valid for the per-form GTB settings,
Save/persistence, eight semantic mappings, activation token projection, and Registration
admission. This visual recheck narrows only the presentation claims.

## Owner-observed result

The Owner reported after viewing the real Registration surface:

- Gender presentation is only partially correct (approximately “50 percent” visually);
- Gender sizing/layout is not correct;
- the other radio menus are not presented correctly;
- responsive behavior has **not** been tested.

Therefore none of the following may be represented as Owner-runtime-qualified from the
0.1.6 pass:

- final Gender binary-card geometry;
- final Graduation Status binary-card geometry;
- ordinary radio-card presentation;
- 320/360/390/430 responsive acceptance;
- final desktop/mobile visual equivalence.

## Root-cause inspection against the admitted artifact

The exact admitted artifact was re-materialized under the repository hash lock before
repair work. It contains two different radio presentation families:

1. **Binary `choice-row` / `choice-btn`** — Gender and conditional Graduation Status only.
   The approved composition is a flex row with `12px` gap, two equal flexible cards,
   `48px` minimum card height, `12px 16px` card padding, and the approved selected surface.
2. **Ordinary `vertical-choices` / `vertical-choice`** — used by the ordinary radio family
   represented by Education Level. The approved composition is a vertical stack with
   `10px` gap, full-width cards, `48px` minimum card height, `14px 16px` padding, a
   `20px` radio control and `10px` checked mark, plus the approved selected surface.

The 0.1.6 production CSS implemented only the first family and did not explicitly
neutralize the authentic Gravity Forms `gfield--choice-align-vertical` direction on the
binary field. On the Owner runtime this allowed the binary choices to remain vertically
oriented/narrow instead of becoming the approved two equal cards. Ordinary radio fields
had no implementation of the admitted vertical-card family at all.

## 0.1.7 repair disposition

The 0.1.7 candidate:

- explicitly sets the semantic binary role's authentic `.gfield_radio` to a row;
- gives its two authentic `.gchoice` children equal flexible tracks and full-width labels;
- keeps the native GF radio as the selection/focus/keyboard authority;
- styles ordinary opted-in radio fields as the admitted vertical-card family while
  explicitly excluding `srwf-role-binary-choice`;
- uses the documented Gravity Forms choice size (`20px`) and radio check size (`10px`)
  from the canonical Theme Framework API source;
- does **not** introduce a new responsive breakpoint or claim responsive qualification.

The 0.1.7 repair is **STATICALLY_PROVEN / OWNER_RUNTIME_RECHECK_REQUIRED** until the Owner
installs that exact package and rechecks the real surface.

## Still not proven

Responsive acceptance remains open. In particular, the repository's hard 320 CSS px
acceptance condition has not been Owner-tested in this pass. The exact production
breakpoint remains `NOT_PROVEN` under the existing visual contract, so this repair does
not invent one merely to manufacture a responsive result.
