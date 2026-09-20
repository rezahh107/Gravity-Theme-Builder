# Releasing SRWF Registration

SRWF Registration releases are created deliberately from a specific commit that is already merged into `main`. The exact source commit owns the release version: the workflow derives it from the production plugin header and `SRWF_REGISTRATION_THEME_VERSION`, requires those two source representations to match, never bumps the version, never republishes an existing release identity, and never publishes the diagnostic package.

## Before releasing

A release candidate is ready when the intended code is merged to `main`, the production plugin header and `SRWF_REGISTRATION_THEME_VERSION` already contain the intended matching version, and `RELEASE_NOTES.md` has been reviewed and contains the same `Release-Version`.

In GitHub, open **Actions → SRWF Registration Release → Run workflow** and keep the workflow branch set to `main`.

Enter:

- **source_sha** — the full 40-character commit ID of the exact merged commit you intend to release. Think of this as the source fingerprint, not just “latest main”.
- **publish** — leave this **false** first.

There is no manual release-version field. After the exact source is checked out and its SHA / current-`main` ancestry are verified, the workflow resolves the version from that exact source. A missing, malformed, or internally inconsistent source version fails closed.

No separate repository Administration credential or Immutable Releases policy setup is required by this workflow.

## First run: `publish=false`

The dry-run checks the exact source SHA, confirms it belongs to current `main`, derives and validates the source version, validates release notes against that derived version, runs the full deterministic SRWF qualification, builds the production package, smoke-checks its contents, creates the SHA-256 file, and inspects tag/release conflicts.

It does **not** create or change a tag or GitHub Release. The production ZIP and checksum are uploaded only as temporary GitHub Actions artifacts for inspection.

A clean new candidate ends with **READY TO PUBLISH** only after every repository-owned release gate succeeds. A failed gate means release publication is intentionally blocked; fix that exact issue in source or release state and use the appropriate merged SHA rather than bypassing the gate.

The historical `0.1.19` release predates this automation. A dry-run against its original SHA may report **ALREADY RELEASED — NO MUTATION** after verifying the existing tag/release read-only. `0.1.19` remains explicitly protected from publication or mutation by this workflow.

## Publication: `publish=true`

After a successful dry-run, run the workflow again with the same **source_sha**, then set **publish=true**.

The verify/build job hands its derived version and candidate-artifact identity to the publish job. Before any publication mutation, the publish job independently checks out the exact source SHA, rechecks its current-`main` ancestry, re-derives the version from that exact source, requires it to match the verify/build handoff, validates `RELEASE_NOTES.md` against that re-derived version, verifies the candidate checksum, and rechecks that neither the intended tag nor Release appeared since verification. Existing tag/release identities are never reused or edited by this workflow.

Only after all gates pass, GitHub creates the exact `srwf-registration-v<version>` tag and Release, then uploads exactly two assets:

- `gtb-srwf-registration-<version>.zip`
- `GTB_SRWF_REGISTRATION_<version>_SHA256.txt`

The workflow then reads the remote GitHub state back and verifies the tag target, non-draft/non-prerelease state, exact asset set, and uploaded ZIP digest. **PUBLISHED AND VERIFIED** is emitted only after those checks succeed.

The final installable ZIP appears on the GitHub **Releases** page. Its internal install directory remains `gtb-srwf-registration/`.

The runtime diagnostic is a separate evidence tool. It is **not** included inside the production ZIP and is **not** uploaded as a normal production Release asset.

## Optional GitHub-side hardening

GitHub Immutable Releases may be enabled independently as additional repository/organization hardening. The SRWF release workflow does not require, query, enable, disable, or verify that policy, and normal SRWF publication does not require an Administration-read token for it.
