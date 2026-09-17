#!/usr/bin/env python3
"""Deterministic repository checks for claims this batch can prove statically."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
THEME = ROOT / "themes" / "srwf-registration"
CSS = THEME / "src" / "srwf-registration.css"
BOOTSTRAP = THEME / "srwf-registration.php"
MAP = THEME / "IMPLEMENTATION_MAP.md"

errors = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


css = CSS.read_text(encoding="utf-8")
php = BOOTSTRAP.read_text(encoding="utf-8")
implementation_map = MAP.read_text(encoding="utf-8")

# Activation and ownership boundary.
require("gform_enqueue_scripts" in php, "bootstrap must use documented Gravity Forms enqueue lifecycle")
require("cssClass" in php and "srwf-registration" in php, "bootstrap must require explicit form opt-in")
require("gform_default_styles" not in php, "theme must not apply global Gravity Forms default styles")
require("srwf-registration" in css, "all theme CSS must have an explicit activation boundary")
require(not re.search(r"(?m)^\s*(html|body|:root)\b", css), "CSS must not own html/body/:root")
require("!important" not in css, "unproven specificity escalation is forbidden")

# Unresolved visual decisions must remain unresolved.
for forbidden in ("@media", "box-shadow", "grid-template-columns"):
    require(forbidden not in css, f"unresolved responsive/optical decision leaked into CSS: {forbidden}")
for forbidden_value in ("13.5px", "24px", "26px", "rgba(29, 78, 216", "rgba(29,78,216"):
    require(forbidden_value not in css, f"non-normative reference value leaked into CSS: {forbidden_value}")

# Canonical values that this implementation claims to map must be present.
for canonical in (
    "#F6F8FB",  # map keeps page background host-owned, so it must be traceable there
    "#FFFFFF", "#172033", "#667085", "#1D4ED8", "#1E40AF", "#B42318",
    "#E4E7EC", "#8690A1", "10px", "52px", "56px", "16px", "840px", "18px", "15px",
    "Vazirmatn",
):
    require(canonical in css or canonical in implementation_map, f"canonical value missing from implementation/map: {canonical}")

# The map must preserve unresolved states rather than silently upgrading them.
for unresolved in (
    "focus_ring_exact_geometry",
    "focus_ring_exact_alpha",
    "desktop_short_field_pairings",
    "desktop_shadow_exact_value",
    "production breakpoint",
    "NON_NORMATIVE_REFERENCE",
    "RUNTIME_REQUIRED",
):
    normalized = implementation_map.replace("-", "_").lower()
    require(unresolved.replace("-", "_").lower() in normalized, f"implementation map does not preserve: {unresolved}")

# No mockup behavior JavaScript or premature shared implementation was added.
js_files = list(THEME.rglob("*.js"))
require(not js_files, f"mockup/runtime JavaScript is not authorized: {js_files}")
shared_src = ROOT / "src"
if shared_src.exists():
    shared_files = [p for p in shared_src.rglob("*") if p.is_file() and p.name != "README.md"]
    require(not shared_files, f"premature top-level shared implementation detected: {shared_files}")

# Keep selector leakage check intentionally narrow: static scope evidence only.
selector_blocks = re.findall(r"([^{}]+)\{", re.sub(r"/\*.*?\*/", "", css, flags=re.S))
for selector_block in selector_blocks:
    block = selector_block.strip()
    if block.startswith("--") or block.startswith("@"):
        continue
    require("srwf-registration" in block, f"selector block is outside activation boundary: {block}")

if errors:
    print("STATIC CONTRACT CHECK: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("STATIC CONTRACT CHECK: PASS")
print("Proves: repository scope/traceability/unresolved-value guards only; does NOT prove Gravity Forms runtime behavior or visual fidelity.")
