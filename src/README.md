# Shared Source

This directory is reserved for **proven reusable implementation code** shared across themes.

It is intentionally empty of framework code at project start.

Do not move theme-local code here merely because it appears generic. Promotion requires either:

- a second real theme that needs materially the same mechanism; or
- a clearly project-wide invariant that is safer when centralized.

Any promoted code should have cross-theme tests and an explicit contract independent of SRWF-specific visual values.
