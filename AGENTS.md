# AGENTS.md

Repository instructions for coding agents working on **Gravity Theme Builder**.

## 1. Read this first

Before changing code or documentation, read:

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

For **implementation facts / HOW**, use current official Gravity Forms documentation/source plus inspected behavior in the supported runtime. Theme-local or repository documentation may record implementation facts, but a stale local factual claim must not override contradictory current official documentation or inspected runtime evidence. Surface and reconcile the contradiction instead.

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
3. Search the official Theme Framework/CSS API for the narrowest supported mechanism.
4. If an official mechanism exists, use it.
5. If it does not, add the smallest scoped adapter and record the gap.
6. Validate the result in real runtime conditions.
7. Record only proven reusable patterns as candidates for promotion into `src/`.

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
