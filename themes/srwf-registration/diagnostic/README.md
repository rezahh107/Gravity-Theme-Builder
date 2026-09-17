# SRWF Runtime Diagnostic v0.2

This is the first repository-managed copy of the Owner runtime diagnostic. The earlier v0.1 used in Owner testing was not present in the required repository base, so v0.2 preserves the intended diagnostic role while replacing the proven generic traversal failure with bounded semantic collectors.

## Activation

Install the diagnostic as a separate WordPress plugin. It loads only when all three conditions are true:

- the current user has `manage_options`;
- the rendered form explicitly has the SRWF `srwf-registration-theme` class;
- the page request includes `?gtb_srwf_diag=v0.2`.

The diagnostic has no server endpoint and no remote transport. Results are exposed in the browser as `window.GTB_SRWF_RUNTIME_DIAGNOSTIC_V02` and logged to the developer console.

## Privacy boundary

The collector records structural classes/approved structural IDs, bounding rectangles, state attributes, selected computed presentation properties, canonical SRWF custom properties, and stylesheet paths/order. It does not collect form/control content, option content, submission payloads, cookies, authentication data, or arbitrary displayed text.

Selects are captured as a structural source plus aggregate `optionCount`; option descendants are never traversed. Tom Select discovery is a separate bounded collector and therefore cannot be starved by a large option collection. Generic Gravity Forms upload structure is captured structurally; GP File Upload Pro and PersianGravity remain `NOT_PROVEN` unless a later real runtime supplies identifying evidence.

Static/unit PASS for this diagnostic proves only bounded/privacy-safe behavior against repository fixtures. It does not prove that the next Owner site's Tom Select, upload, PersianGravity, validation, focus, or narrow-layout runtime has been captured successfully.
