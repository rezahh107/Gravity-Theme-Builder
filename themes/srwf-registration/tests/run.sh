#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)"
REFERENCE_OUT="${TMPDIR:-/tmp}/gtb-srwf-owner-reference.html"

bash "$ROOT/themes/srwf-registration/reference/materialize_reference.sh" "$REFERENCE_OUT"
php -l "$ROOT/themes/srwf-registration/srwf-registration.php"
php "$ROOT/themes/srwf-registration/tests/test_bootstrap.php"
python3 "$ROOT/themes/srwf-registration/tests/test_static_contract.py"
