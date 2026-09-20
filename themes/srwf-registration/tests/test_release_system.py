from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
import zipfile
from pathlib import Path

TESTS = Path(__file__).resolve().parent
THEME = TESTS.parent
REPO = THEME.parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "srwf-registration-release.yml"
HELPER = TESTS / "release_srwf_registration.py"
BUILDER = TESTS / "build_owner_test_packages.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_version_fixture(
    theme_root: Path,
    *,
    header: str | None = "1.2.3",
    constant: str | None = "1.2.3",
) -> None:
    src = theme_root / "src"
    src.mkdir(parents=True, exist_ok=True)
    lines = ["<?php", "/**", " * Plugin Name: Fixture"]
    if header is not None:
        lines.append(f" * Version: {header}")
    lines.append(" */")
    if constant is not None:
        lines.append(f"const SRWF_REGISTRATION_THEME_VERSION = '{constant}';")
    (src / "srwf-registration-theme.php").write_text("\n".join(lines) + "\n", encoding="utf-8")


release = load_module(HELPER, "srwf_release_helper")
builder = load_module(BUILDER, "srwf_owner_package_builder")


class ReleaseWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_manual_dispatch_is_the_only_release_trigger(self) -> None:
        self.assertRegex(self.workflow, r"(?m)^on:\n  workflow_dispatch:\n")
        trigger_block = self.workflow.split("permissions:", 1)[0]
        self.assertNotRegex(trigger_block, r"(?m)^  push:")
        self.assertNotRegex(trigger_block, r"(?m)^  pull_request:")

    def test_manual_version_channel_is_closed_and_exact_sha_is_required(self) -> None:
        trigger_block = self.workflow.split("permissions:", 1)[0]
        self.assertRegex(
            trigger_block,
            r"source_sha:\n\s+description:.*\n\s+required: true\n\s+type: string",
        )
        self.assertRegex(
            trigger_block,
            r"publish:\n\s+description:.*\n\s+required: true\n\s+default: false\n\s+type: boolean",
        )
        self.assertNotRegex(trigger_block, r"(?m)^\s{6}version:\s*$")
        self.assertNotIn("inputs.version", self.workflow)
        self.assertNotIn("${{ inputs.version }}", self.workflow)
        self.assertIn("^[0-9a-f]{40}$", self.workflow)

    def test_source_must_be_reachable_from_current_main(self) -> None:
        self.assertIn("merge-base --is-ancestor", self.workflow)
        self.assertIn("SOURCE_NOT_MERGED_TO_MAIN", self.workflow)
        self.assertIn("refs/remotes/origin/main", self.workflow)

    def test_version_is_resolved_only_after_exact_source_identity_check(self) -> None:
        identity = self.workflow.index("- name: Verify exact source identity and merged-main ancestry")
        resolution = self.workflow.index("- name: Resolve release version from exact source")
        self.assertLess(identity, resolution)
        resolve_block = re.search(
            r"- name: Resolve release version from exact source\n(?P<body>.*?)(?=\n      - name:)",
            self.workflow,
            re.S,
        )
        self.assertIsNotNone(resolve_block)
        body = resolve_block.group("body")
        self.assertIn("resolve-version", body)
        self.assertIn('--theme-root "$SOURCE_DIR/themes/srwf-registration"', body)
        self.assertIn('echo "version=$version"', body)
        self.assertIn('echo "VERSION=$version"', body)
        self.assertIn("candidate_artifact=\"gtb-srwf-registration-release-candidate-${version}-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}\"", body)
        self.assertIn("version: ${{ steps.resolve_version.outputs.version }}", self.workflow)
        self.assertIn("candidate_artifact: ${{ steps.resolve_version.outputs.candidate_artifact }}", self.workflow)

    def test_version_and_tag_identity_are_srwf_scoped(self) -> None:
        self.assertIn("resolve-version", self.workflow)
        self.assertIn('tag="srwf-registration-v${VERSION}"', self.workflow)
        self.assertEqual(
            release.PROTECTED_HISTORICAL_RELEASES["0.1.19"]["tag"],
            "srwf-registration-v0.1.19",
        )

    def test_all_versioned_release_consumers_use_derived_version(self) -> None:
        self.assertNotIn("inputs.version", self.workflow)
        self.assertIn("name: ${{ steps.resolve_version.outputs.candidate_artifact }}", self.workflow)
        self.assertIn(
            "gtb-srwf-registration-${{ steps.resolve_version.outputs.version }}.zip",
            self.workflow,
        )
        self.assertIn(
            "GTB_SRWF_REGISTRATION_${{ steps.resolve_version.outputs.version }}_SHA256.txt",
            self.workflow,
        )
        self.assertIn("VERIFY_VERSION: ${{ needs['verify-and-build'].outputs.version }}", self.workflow)
        self.assertIn(
            "CANDIDATE_ARTIFACT: ${{ needs['verify-and-build'].outputs.candidate_artifact }}",
            self.workflow,
        )
        self.assertIn('--title "SRWF Registration ${VERSION}"', self.workflow)
        self.assertIn('checksum="$RUNNER_TEMP/gtb-srwf-release-assets/GTB_SRWF_REGISTRATION_${VERSION}_SHA256.txt"', self.workflow)
        self.assertIn('zip="$RUNNER_TEMP/gtb-srwf-release-assets/gtb-srwf-registration-${VERSION}.zip"', self.workflow)

    def test_conflicting_or_already_published_tags_fail_closed(self) -> None:
        self.assertIn("TAG_SHA_MISMATCH", self.workflow)
        self.assertIn("ORPHANED_RELEASE_CONFLICT", self.workflow)
        self.assertIn("ALREADY_RELEASED", self.workflow)
        self.assertIn("EXISTING_TAG_REQUIRES_OWNER_REVIEW", self.workflow)
        self.assertIn("PROTECTED_HISTORICAL_RELEASE", self.workflow)
        self.assertIn("TAG_APPEARED_BEFORE_PUBLISH", self.workflow)
        self.assertIn("RELEASE_APPEARED_BEFORE_PUBLISH", self.workflow)

    def test_publish_job_is_write_scoped_and_conditionally_gated(self) -> None:
        self.assertRegex(
            self.workflow,
            r"(?ms)^permissions:\n  contents: read.*?^  publish:\n.*?    if: \$\{\{ inputs\.publish \}\}.*?    permissions:\n      contents: write",
        )
        publication = re.search(
            r"- name: Publish exact tag and GitHub Release\n(?P<body>.*?)(?=\n      - name:)",
            self.workflow,
            re.S,
        )
        self.assertIsNotNone(publication)
        body = publication.group("body")
        self.assertIn("gh release create", body)
        self.assertIn('--target "$SOURCE_SHA"', body)
        self.assertNotIn("diagnostic", body.lower())

    def test_publish_boundary_rederives_version_and_fails_handoff_mismatch_before_mutation(self) -> None:
        recheck = re.search(
            r"- name: Reconfirm exact source, derived version, notes and candidate checksum\n(?P<body>.*?)(?=\n      - name:)",
            self.workflow,
            re.S,
        )
        self.assertIsNotNone(recheck)
        body = recheck.group("body")
        self.assertIn("resolve-version", body)
        self.assertIn('if [[ "$resolved_version" != "$VERIFY_VERSION" ]]; then', body)
        self.assertIn("VERIFY_PUBLISH_VERSION_HANDOFF_MISMATCH", body)
        self.assertIn('echo "VERSION=$VERSION" >> "$GITHUB_ENV"', body)
        self.assertIn("validate-notes", body)
        self.assertLess(
            self.workflow.index("VERIFY_PUBLISH_VERSION_HANDOFF_MISMATCH"),
            self.workflow.index("gh release create"),
        )
        self.assertLess(
            self.workflow.index("SOURCE_SHA_MISMATCH_BEFORE_PUBLISH"),
            self.workflow.index("gh release create"),
        )
        self.assertLess(
            self.workflow.index("SOURCE_NOT_MERGED_TO_MAIN_BEFORE_PUBLISH"),
            self.workflow.index("gh release create"),
        )

    def test_no_native_immutable_policy_prerequisite_or_special_credential(self) -> None:
        for forbidden in (
            "SRWF_IMMUTABLE_RELEASES_POLICY_READ_TOKEN",
            "repos/${GITHUB_REPOSITORY}/immutable-releases",
            "validate-immutable-policy",
            "IMMUTABLE_RELEASES_POLICY_CREDENTIAL_MISSING",
            "IMMUTABLE_RELEASES_POLICY_DISABLED",
            "IMMUTABLE_RELEASES_POLICY_UNAVAILABLE",
            "Administration: read",
        ):
            self.assertNotIn(forbidden, self.workflow)
        self.assertNotRegex(self.workflow, r"(?m)^\s+administration:\s")

    def test_no_replacement_policy_assertion_is_exposed(self) -> None:
        trigger_block = self.workflow.split("permissions:", 1)[0]
        self.assertNotRegex(
            trigger_block,
            r"(?mi)^\s+(?:immutable|immutability|immutable_releases|immutable_releases_enabled):\s*$",
        )
        self.assertNotIn("inputs.immutable", self.workflow.lower())
        self.assertNotIn("IMMUTABLE_RELEASES_ENABLED", self.workflow)

    def test_verified_candidate_contains_only_production_zip_and_checksum(self) -> None:
        candidate = re.search(
            r"- name: Upload verified production candidate artifact\n(?P<body>.*?)(?=\n      - name:)",
            self.workflow,
            re.S,
        )
        self.assertIsNotNone(candidate)
        body = candidate.group("body")
        self.assertIn("gtb-srwf-registration-${{ steps.resolve_version.outputs.version }}.zip", body)
        self.assertIn("GTB_SRWF_REGISTRATION_${{ steps.resolve_version.outputs.version }}_SHA256.txt", body)
        self.assertNotIn("runtime-diagnostic", body)
        self.assertNotIn("owner-test", body)

    def test_dry_run_has_no_write_scoped_job(self) -> None:
        verify_job = re.search(
            r"(?ms)^  verify-and-build:\n(?P<body>.*?)(?=^  publish:)",
            self.workflow,
        )
        self.assertIsNotNone(verify_job)
        self.assertIn("permissions:\n      contents: read", verify_job.group("body"))
        self.assertNotIn("contents: write", verify_job.group("body"))
        self.assertIn("if: ${{ inputs.publish }}", self.workflow)

    def test_post_publication_verifies_exact_remote_state_without_immutability_gate(self) -> None:
        for required in (
            "POST_PUBLISH_TAG_MISMATCH",
            "POST_PUBLISH_DRAFT",
            "POST_PUBLISH_PRERELEASE",
            "POST_PUBLISH_ASSET_SET_MISMATCH",
            "POST_PUBLISH_ZIP_DIGEST_MISMATCH",
        ):
            self.assertIn(required, self.workflow)
        self.assertIn('gh api "repos/$GITHUB_REPOSITORY/releases/tags/$TAG_NAME"', self.workflow)
        self.assertNotIn("POST_PUBLISH_NOT_IMMUTABLE", self.workflow)
        self.assertNotIn("validate-published-immutability", self.workflow)
        self.assertNotRegex(self.workflow, r"jq -r ['\"]\.immutable")

    def test_historical_read_only_path_remains_protected_and_non_mutating(self) -> None:
        self.assertIn("ALREADY RELEASED — NO MUTATION", self.workflow)
        self.assertIn("Historical dry-run exception", self.workflow)
        self.assertIn('if [[ "$PUBLISH" == true && "$VERSION" == "0.1.19" ]]; then', self.workflow)
        self.assertIn('if [[ "$VERSION" == "0.1.19" ]]; then', self.workflow)
        self.assertIn("PROTECTED_HISTORICAL_RELEASE", self.workflow)
        self.assertNotIn("immutable-releases", self.workflow)


class ReleaseHelperTests(unittest.TestCase):
    def test_source_version_positive_control(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            theme_root = Path(tmp)
            write_version_fixture(theme_root, header="1.2.3", constant="1.2.3")
            self.assertEqual(release.resolve_version(theme_root), "1.2.3")

    def test_source_version_header_constant_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            theme_root = Path(tmp)
            write_version_fixture(theme_root, header="1.2.3", constant="1.2.4")
            with self.assertRaisesRegex(RuntimeError, "internally inconsistent"):
                release.resolve_version(theme_root)

    def test_missing_or_malformed_source_versions_fail_closed(self) -> None:
        cases = (
            (None, "1.2.3", "unable to read SRWF version"),
            ("1.2.3", None, "unable to read SRWF version"),
            ("1.2", "1.2", "must use x.y.z numeric format"),
            ("1.2.3", "not-a-version", "must use x.y.z numeric format"),
        )
        for header, constant, expected_error in cases:
            with self.subTest(header=header, constant=constant):
                with tempfile.TemporaryDirectory() as tmp:
                    theme_root = Path(tmp)
                    write_version_fixture(theme_root, header=header, constant=constant)
                    with self.assertRaisesRegex(RuntimeError, expected_error):
                        release.resolve_version(theme_root)

    def test_release_notes_must_match_derived_source_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "RELEASE_NOTES.md"
            notes.write_text("# Notes\n\nRelease-Version: 1.2.3\n\nBody.\n", encoding="utf-8")
            release.validate_notes(notes, "1.2.3")
            with self.assertRaisesRegex(RuntimeError, "does not match derived source version"):
                release.validate_notes(notes, "1.2.4")

    def test_current_source_release_notes_match_current_source_version(self) -> None:
        current_version = release.resolve_version(THEME)
        release.validate_notes(THEME / "RELEASE_NOTES.md", current_version)

    def test_release_helper_commands_match_source_derived_contract(self) -> None:
        commands = release.build_parser()._subparsers._group_actions[0].choices
        self.assertNotIn("validate-version", commands)
        self.assertNotIn("validate-immutable-policy", commands)
        self.assertNotIn("validate-published-immutability", commands)
        self.assertEqual(set(commands), {"resolve-version", "validate-notes", "prepare-assets"})

    def test_public_zip_is_byte_identical_and_checksum_is_final_bytes(self) -> None:
        version = release.resolve_version(THEME)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            builder_output = tmp_path / "builder"
            release_output = tmp_path / "release"
            production_zip, diagnostic_zip, _ = builder.build(builder_output)
            result = release.prepare_release_assets(THEME, builder_output, release_output)

            public_zip = Path(result["public_zip"])
            checksum_file = Path(result["checksum_file"])
            self.assertEqual(result["version"], version)
            self.assertEqual(production_zip.read_bytes(), public_zip.read_bytes())
            self.assertEqual(release.sha256(public_zip), result["sha256"])
            self.assertEqual(
                checksum_file.read_text(encoding="utf-8"),
                f"{result['sha256']}  {public_zip.name}\n",
            )
            self.assertNotEqual(public_zip, diagnostic_zip)
            self.assertNotIn(diagnostic_zip.name, checksum_file.read_text(encoding="utf-8"))
            if version == "0.1.19":
                self.assertEqual(
                    result["sha256"],
                    release.PROTECTED_HISTORICAL_RELEASES["0.1.19"]["zip_sha256"],
                )

    def test_production_package_has_exact_install_root_and_no_forbidden_content(self) -> None:
        version = release.resolve_version(THEME)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            builder_output = tmp_path / "builder"
            release_output = tmp_path / "release"
            builder.build(builder_output)
            result = release.prepare_release_assets(THEME, builder_output, release_output)
            public_zip = Path(result["public_zip"])

            self.assertEqual(result["version"], version)
            with zipfile.ZipFile(public_zip) as bundle:
                names = [name for name in bundle.namelist() if not name.endswith("/")]
            self.assertTrue(names)
            self.assertTrue(all(name.startswith("gtb-srwf-registration/") for name in names))
            lowered = "\n".join(names).lower()
            self.assertNotIn("/tests/", lowered)
            self.assertNotIn("/reference/", lowered)
            self.assertNotIn("/diagnostic/", lowered)

    def test_historical_0119_release_identity_is_locked(self) -> None:
        protected = release.PROTECTED_HISTORICAL_RELEASES["0.1.19"]
        self.assertEqual(protected["source_sha"], "4e5727ec3573bc08395c43a99312f157f062a347")
        self.assertEqual(
            protected["zip_sha256"],
            "e31c11dfb75131e1cc99cab0f4f0da484ee9c238eaa36443766570ad508728ef",
        )


if __name__ == "__main__":
    unittest.main()
