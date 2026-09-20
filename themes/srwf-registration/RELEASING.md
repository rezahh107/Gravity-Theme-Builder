# Releasing SRWF Registration

SRWF Registration releases are created deliberately from a specific commit that is already merged into `main`. The release workflow never bumps the version and never publishes the diagnostic package.

## GitHub-native immutability prerequisite

Future SRWF publications require GitHub **Immutable Releases** to be enabled for this repository (or enforced for it by the repository owner/organization) before the workflow may report a new candidate as ready for publication.

Repository-setting enablement is an Owner/repository-administration action outside this workflow and outside the release PR. The workflow does not enable, disable, or synchronize that setting itself.

For a repository-level setting, an Owner/admin can use GitHub **Settings → Releases → Enable release immutability**. Organization policy may also enforce immutable releases for this repository. GitHub applies immutability to future releases; an older release is not made retrospectively immutable merely because the setting is enabled later.

The workflow also requires the Actions secret:

`SRWF_IMMUTABLE_RELEASES_POLICY_READ_TOKEN`

Provision that secret with a dedicated credential restricted to this repository and the minimum GitHub repository permission needed by the official policy-status endpoint: **Administration: read**. A fine-grained PAT or another GitHub-supported credential type may be used. Do not grant Administration write merely for this workflow.

This policy-read credential is separate from publication. Actual tag/Release publication continues to use the workflow's normal `GITHUB_TOKEN` with only `contents: write` in the conditional publish job.

The workflow proves native policy state through GitHub's repository immutable-releases status API. A missing credential, denied/unavailable request, disabled policy, or malformed/unknown response fails closed. No workflow input, environment variable, documentation statement, or operator confirmation can substitute for that API evidence.

## Before releasing

A release candidate is ready when the intended code is merged to `main`, the production plugin header and `SRWF_REGISTRATION_THEME_VERSION` already contain the intended version, `RELEASE_NOTES.md` has been reviewed and contains the same `Release-Version`, and the GitHub-native immutability prerequisite above is configured.

In GitHub, open **Actions → SRWF Registration Release → Run workflow** and keep the workflow branch set to `main`.

Enter:

- **version** — the version already present in the code, for example `0.1.20`.
- **source_sha** — the full 40-character commit ID of the exact merged commit you intend to release. Think of this as the immutable fingerprint of the source, not just “latest main”.
- **publish** — leave this **false** first.

## First run: `publish=false`

The dry-run checks the exact source SHA, confirms it belongs to current `main`, validates the source version and release notes, runs the full deterministic SRWF qualification, builds the production package, smoke-checks its contents, creates the SHA-256 file, and inspects tag/release conflicts.

For a clean new candidate, the dry-run also reads GitHub's native Immutable Releases status using the dedicated Administration-read credential. It cannot end with **READY TO PUBLISH** unless GitHub reports native immutability enabled.

It does **not** create or change a tag or GitHub Release. The production ZIP and checksum are uploaded only as temporary GitHub Actions artifacts for inspection.

A clean new candidate ends with **READY TO PUBLISH** only after every gate, including the GitHub-native policy proof, succeeds. A failed gate means release publication is intentionally blocked; fix that exact issue in source or repository prerequisites and use the appropriate merged SHA rather than bypassing the gate.

The historical `0.1.19` release predates this automation and predates any requirement that it become immutable retrospectively. A dry-run against its original SHA may report **ALREADY RELEASED — NO MUTATION** after verifying the existing tag/release read-only. That read-only path does not require the historical release to report immutable state. `0.1.19` remains explicitly protected from publication or mutation by this workflow.

## Publication: `publish=true`

After a successful dry-run, run the workflow again with the same `version` and `source_sha`, then set **publish=true**.

Immediately before the publication mutation, the publish job rechecks the GitHub-native Immutable Releases policy with the separate Administration-read credential. If the setting was disabled, the credential became unavailable/unauthorized, or the API response is not trustworthy, publication stops before `gh release create`.

Only after all gates pass, GitHub creates the exact `srwf-registration-v<version>` tag and Release, then uploads exactly two assets:

- `gtb-srwf-registration-<version>.zip`
- `GTB_SRWF_REGISTRATION_<version>_SHA256.txt`

The workflow then reads the remote GitHub state back and verifies the tag target, non-draft/non-prerelease state, native `immutable == true` state, exact asset set, and uploaded ZIP digest. **PUBLISHED AND VERIFIED** is emitted only after all of those checks succeed.

The final installable ZIP appears on the GitHub **Releases** page. Its internal install directory remains `gtb-srwf-registration/`.

The runtime diagnostic is a separate evidence tool. It is **not** included inside the production ZIP and is **not** uploaded as a normal production Release asset.
