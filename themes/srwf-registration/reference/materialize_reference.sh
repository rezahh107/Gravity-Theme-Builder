#!/usr/bin/env bash
set -euo pipefail

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
TMP_GZ="${TMPDIR:-/tmp}/OWNER_REFERENCE_new_7.html.gz"
OUT="${1:-${TMPDIR:-/tmp}/OWNER_REFERENCE_new_7.html}"

cat \
  "$HERE/OWNER_REFERENCE_new_7.html.gz.b64.part01" \
  "$HERE/OWNER_REFERENCE_new_7.html.gz.b64.part02" \
  "$HERE/OWNER_REFERENCE_new_7.html.gz.b64.part03" \
  | base64 -d > "$TMP_GZ"

printf '%s  %s\n' \
  '696bc8466aa9503e782fee48f484a34c1a85d4c30210bcc645ecc7e8171c9340' \
  "$TMP_GZ" | sha256sum -c -

gzip -dc "$TMP_GZ" > "$OUT"

printf '%s  %s\n' \
  '436307d4cd6d896e0f280e502901269240dc310ec2e5927e30e1c29643483000' \
  "$OUT" | sha256sum -c -

printf '%s\n' "$OUT"
