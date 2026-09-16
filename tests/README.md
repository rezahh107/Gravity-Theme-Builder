# Cross-Theme Tests

Top-level `tests/` is for **project-wide invariants and reusable validation tooling**.

Theme-specific tests should live with the theme until the assertion is demonstrably shared.

Good candidates for top-level tests later may include:

- theme scope/isolation checks;
- forbidden global-selector checks;
- shared mapping/schema validation;
- reusable runtime harnesses;
- compatibility checks that apply to every theme.

Do not create a cross-theme test abstraction before at least one real theme exposes the requirement clearly.
