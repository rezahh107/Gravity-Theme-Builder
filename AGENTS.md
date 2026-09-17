# AGENTS.md

Repository instructions for coding agents working on **Gravity Theme Builder**.

## 0. Mandatory canonical-source preflight

The repository has a canonical local Gravity Forms Theme Framework implementation-fact source at this exact path:

`PROJECT_SOURCES/00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_REFERENCE.md`

Before beginning **any code change, technical design, implementation planning, debugging, refactoring, technical review, or Theme Framework implementation-fact analysis** for the current task, read that source **first**.

Do not begin that technical work until the canonical source has actually been retrieved and read for the current task. Do not claim or imply that this preflight occurred if it did not.

Then read:

`PROJECT_SOURCES/SOURCE_REGISTRY.md`

for the source's current admission/canonical status, snapshot metadata, update rules, and recorded supplemental ambiguity.

### Canonical-source preflight gate

The preflight is satisfied only when all of the following are true:

1. `PROJECT_SOURCES/00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_REFERENCE.md` exists and is readable.
2. It has been read for the current task before technical implementation/review decisions are made.
3. `PROJECT_SOURCES/SOURCE_REGISTRY.md` has been checked for the source's current status and maintenance notes.
4. Any relevant ambiguity, staleness warning, or source limitation is carried into the task rather than silently ignored.

If the canonical source is missing or unreadable, stop Theme Framework technical work and report:

`CANONICAL_SOURCE_UNAVAILABLE`

Do not substitute model memory, naming-pattern inference, an older copied snapshot, or guessed Gravity Forms behavior for the missing source.

If the registry marks the source as suspended, stale, candidate-only, or otherwise non-canonical, still use it as the required first local lookup, but do not treat it as current factual authority; revalidate the relevant implementation facts against current official Gravity Forms documentation/source and supported-runtime evidence before relying on them.

The existence and path of the canonical source are repository invariants for normal work. Do not bypass, rename, replace, remove, or relocate it as part of unrelated implementation work. Any intentional source replacement, path migration, or canonical-status change must be an explicit source-maintenance change with corresponding registry reconciliation.

This is a **mandatory read-order/preflight rule**, not a flat cross-domain authority ranking.

For Theme Framework implementation facts:

- use the canonical local reference as the first lookup;
- never invent a `--gf-*` property, wrapper class, selector, framework layer, or host behavior from naming patterns;
- if required information is absent, classify it as `UNKNOWN_FROM_LOCAL_REFERENCE` and consult current official Gravity Forms documentation/source;
- if current official Gravity Forms documentation/source or inspected supported-runtime behavior conflicts with the local snapshot, the current evidence wins for that factual question and the local source must be reconciled/updated;
- do not let this source override owner decisions, approved visual intent, Charter non-goals, or other normative repository boundaries outside the implementation-fact domain.

## 1. Read governing and theme documents

After the mandatory source preflight, read:

1. `docs/PROJECT_CHARTER.md`
2. `docs/THEME_AUTHORING_CONTRACT.md`
3. `docs/ARCHITECTURE.md`
4. The target theme's own README and approved reference artifacts

Do **not** interpret this reading order as one flat authority ranking across every kind of question.

For **normative repository instructions**, use this precedence:

1. `docs/PROJECT_CHARTER.md`
2. `docs/THEME_AUTHORING_CONTRACT.md`
3. `docs/ARCHITECTURE.md`
4. Theme-specific implementation documentation

For **visual intent / WHAT**, use the approved visual/UX contract and approved reference artifacts for the target theme. Visual authority controls presentation only; it does not authorize takeover of Gravity Forms behavior or override repository non-goals and engineering boundaries.

For **implementation facts / HOW**, consult `PROJECT_SOURCES/00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_REFERENCE.md` first, then use current official Gravity Forms documentation/source plus inspected behavior in the supported runtime where the local snapshot is absent, ambiguous, version-sensitive, or contradictory. Theme-local or repository documentation may record implementation facts, but a stale local factual claim must not override contradictory current official documentation or inspected runtime evidence. Surface and reconcile the contradiction instead.

Explicit current owner decisions govern authorized project/design decisions, subject to any Charter change-control requirement that requires the Charter itself to be amended.

If a conflict crosses authority domains, classify the question first and apply the authority for that domain rather than forcing a cross-domain precedence comparison.

## 2. Core mission

Implement approved visual designs on the Gravity Forms Theme Framework with the smallest safe amount of custom code.

The job is **not** to redesign the approved visual reference, replace Gravity Forms behavior, or rebuild Orbital/Foundation.

## 3. Mandatory engineering rules

- Treat the approved theme reference/contract as visual authority.
- Preserve Gravity Forms markup, lifecycle, validation, accessibility semantics, and persistence unless an explicit requirement proves otherwise.
- Prefer official Gravity Forms Theme Framework / CSS API properties over direct DOM styling when they provide the needed capability.
- Do not assume that an available `--gf-*` property authorizes a visual value. Values come from the approved design contract.
- Use direct CSS only for a demonstrated API gap or a proven runtime-consumer requirement.
- Keep selectors scoped to the target theme/runtime surface. Avoid global `html`, `body`, broad `.gform_wrapper`, or site-wide ownership unless explicitly authorized.
- Avoid `!important`. When unavoidable because of proven host cascade behavior, document why and test the exact consumer.
- Do not fork or copy Orbital wholesale.
- Do not recreate native controls, validation UI, focus lifecycle, or layout engines without a named requirement and evidence that the host cannot satisfy it.
- Do not create generic abstractions before at least one real implementation proves the need. Prefer local theme code first; promote to `src/` only after reuse is demonstrated.

## 4. Evidence discipline

Distinguish clearly between:

- `DOCUMENTED` — supported by current official Gravity Forms documentation/source.
- `RUNTIME_PROVEN` — observed in the real supported runtime.
- `REFERENCE_ONLY` — present only in a visual/mockup reference.
- `ASSUMED` — not yet verified.

A CSS custom property appearing in documentation does not prove where it is consumed in every add-on or custom field. Inspect computed styles/runtime when consumer identity matters.

Before relying on version-sensitive APIs, verify them against the actual supported Gravity Forms version and current official documentation.

Repository documentation does not become factual runtime authority merely because it is normative for repository behavior. When local factual documentation conflicts with current official Gravity Forms documentation/source or inspected supported-runtime behavior, mark the local claim stale or `NOT_PROVEN` until reconciled.

## 5. Theme implementation workflow

For each visual requirement:

1. Identify the visual authority and exact requirement.
2. Classify responsibility: typography, spacing, control, layout, optical detail, responsive behavior, media, state, or host behavior.
3. Search `PROJECT_SOURCES/00_GRAVITY_FORMS_THEME_FRAMEWORK_CANONICAL_REFERENCE.md` for the narrowest documented mechanism.
4. If the local source is absent, ambiguous, or contradicted, check the current official Theme Framework/CSS API documentation and supported runtime.
5. If an official mechanism exists, use it.
6. If it does not, add the smallest scoped adapter and record the gap.
7. Validate the result in real runtime conditions.
8. Record only proven reusable patterns as candidates for promotion into `src/`.

## 6. Validation expectations

A theme is not complete merely because it visually matches a static screenshot. Validate, where applicable:

- desktop and mobile/reference widths;
- RTL and Persian content;
- long labels/values;
- validation and error states;
- keyboard focus and focus-visible behavior;
- text enlargement and narrow reflow;
- host/theme isolation;
- supported Gravity Forms runtime;
- required add-ons/custom fields;
- no behavior regression in submission or validation.

Theme-specific tests belong with the theme. Cross-theme invariant tests belong in top-level `tests/`.

## 7. Pull request behavior

- Keep PRs bounded to one coherent work unit.
- State what was proven versus what remains unverified.
- Do not silently broaden the project scope.
- Do not merge without explicit owner authorization.
- If a runtime dependency is unavailable, leave the result `NOT_PROVEN`; do not infer success from static CSS alone.

## 8. First reference implementation

`themes/srwf-registration/` is the first reference theme. It should remain independently understandable and should not be prematurely decomposed into a universal generator.

The repository may become a reusable theme-building system over time, but reuse must emerge from real themes rather than speculative framework design.
