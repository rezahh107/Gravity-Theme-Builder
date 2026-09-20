# Releasing SRWF Registration

SRWF Registration releases are created deliberately from a specific commit that is already merged into `main`. The release workflow never bumps the version and never publishes the diagnostic package.

## Before releasing

A release candidate is ready when the intended code is merged to `main`, the production plugin header and `SRWF_REGISTRATION_THEME_VERSION` already contain the intended version, and `RELEASE_NOTES.md` has been reviewed and contains the same `Release-Version`.

In GitHub, open **Actions → SRWF Registration Release → Run workflow** and keep the workflow branch set to `main`.

Enter:

- **version** — the version already present in the code, for example `0.1.20`.
- **source_sha** — the full 40-character commit ID of the exact merged commit you intend to release. Think of this as the immutable fingerprint of the source, not just “latest main”.
- **publish** — leave this **false** first.

## First run: `publish=false`

The dry-run checks the exact source SHA, confirms it belongs to current `main`, validates the source version and release notes, runs the full deterministic SRWF qualification, builds the production package, smoke-checks its contents, creates the SHA-256 file, and inspects tag/release conflicts.

It does **not** create or change a tag or GitHub Release. The production ZIP and checksum are uploaded only as temporary GitHub Actions artifacts for inspection.

A clean new candidate ends with **READY TO PUBLISH**. A failed gate means release publication is intentionally blocked; fix that exact issue in source and use the new merged SHA rather than bypassing the gate.

The historical `0.1.19` release predates this automation. A dry-run against its original SHA may report **ALREADY RELEASED — NO MUTATION** after verifying the existing tag/release read-only. `0.1.19` is explicitly protected from publication by this workflow.

## Publication: `publish=true`

After a successful dry-run, run the workflow again with the same `version` and `source_sha`, then set **publish=true**.

Only after all gates pass, GitHub creates the exact `srwf-registration-v<version>` tag and Release, then uploads exactly two assets:

- `gtb-srwf-registration-<version>.zip`
- `GTB_SRWF_REGISTRATION_<version>_SHA256.txt`

The workflow then reads the remote GitHub state back and verifies the tag target, release state, exact asset set, and uploaded ZIP digest.

The final installable ZIP appears on the GitHub **Releases** page. Its internal install directory remains `gtb-srwf-registration/`.

The runtime diagnostic is a separate evidence tool. It is **not** included inside the production ZIP and is **not** uploaded as a normal production Release asset.
