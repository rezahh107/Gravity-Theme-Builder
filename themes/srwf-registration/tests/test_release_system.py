from __future__ import annotations

import importlib.util
import json
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

    def test_publish_defaults_false_and_exact_sha_is_required(self) -> None:
        self.assertRegex(
            self.workflow,
            r"source_sha:\n\s+description:.*\n\s+required: true\n\s+type: string",
        )
        self.assertRegex(
            self.workflow,
            r"publish:\n\s+description:.*\n\s+required: true\n\s+default: false\n\s+type: boolean",
        )
        self.assertIn("^[0-9a-f]{40}$", self.workflow)

    def test_source_must_be_reachable_from_current_main(self) -> None:
        self.assertIn("merge-base --is-ancestor", self.workflow)
        self.assertIn("SOURCE_NOT_MERGED_TO_MAIN", self.workflow)
        self.assertIn("refs/remotes/origin/main", self.workflow)

    def test_version_and_tag_identity_are_srwf_scoped(self) -> None:
        self.assertIn("validate-version", self.workflow)
        self.assertIn('tag="srwf-registration-v${VERSION}"', self.workflow)
        self.assertEqual(
            release.PROTECTED_HISTORICAL_RELEASES["0.1.19"]["tag"],
            "srwf-registration-v0.1.19",
        )

    def test_conflicting_or_already_published_tags_fail_closed(self) -> None:
        self.assertIn("TAG_SHA_MISMATCH", self.workflow)
        self.assertIn("ALREADY_RELEASED", self.workflow)
        self.assertIn("EXISTING_TAG_REQUIRES_OWNER_REVIEW", self.workflow)
        self.assertIn("PROTECTED_HISTORICAL_RELEASE", self.workflow)

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
        self.assertNotIn("diagnostic", body.lower())

    def test_native_policy_proof_precedes_ready_and_publish_boundaries(self) -> None:
        readiness_policy = self.workflow.index(
            "- name: Prove GitHub-native Immutable Releases policy for readiness"
        )
        readiness = self.workflow.index("- name: Evaluate publication readiness")
        publish_policy = self.workflow.index(
            "- name: Reprove GitHub-native Immutable Releases policy immediately before mutation"
        )
        publication = self.workflow.index("- name: Publish exact tag and GitHub Release")
        self.assertLess(readiness_policy, readiness)
        self.assertLess(publish_policy, publication)
        self.assertIn("repos/${GITHUB_REPOSITORY}/immutable-releases", self.workflow)
        self.assertIn("X-GitHub-Api-Version: 2026-03-10", self.workflow)

    def test_policy_evidence_failures_cannot_become_readiness_success(self) -> None:
        policy = re.search(
            r"- name: Prove GitHub-native Immutable Releases policy for readiness\n(?P<body>.*?)(?=\n      - name: Evaluate publication readiness)",
            self.workflow,
            re.S,
        )
        self.assertIsNotNone(policy)
        body = policy.group("body")
        self.assertIn("IMMUTABLE_RELEASES_POLICY_CREDENTIAL_MISSING", body)
        self.assertIn("IMMUTABLE_RELEASES_POLICY_UNAVAILABLE", body)
        self.assertIn("validate-immutable-policy", body)
        self.assertNotIn("READY TO PUBLISH", body)
        self.assertNotIn("PUBLISHED AND VERIFIED", body)

    def test_policy_credential_is_separate_from_publication_token(self) -> None:
        self.assertIn(
            "SRWF_IMMUTABLE_RELEASES_POLICY_READ_TOKEN: ${{ secrets.SRWF_IMMUTABLE_RELEASES_POLICY_READ_TOKEN }}",
            self.workflow,
        )
        publication = re.search(
            r"- name: Publish exact tag and GitHub Release\n(?P<body>.*?)(?=\n      - name:)",
            self.workflow,
            re.S,
        )
        self.assertIsNotNone(publication)
        self.assertNotIn("SRWF_IMMUTABLE_RELEASES_POLICY_READ_TOKEN", publication.group("body"))
        self.assertIn("GH_TOKEN: ${{ github.token }}", self.workflow)
        self.assertNotRegex(self.workflow, r"(?m)^\s+administration:\s")

    def test_caller_cannot_assert_immutability(self) -> None:
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
        self.assertIn("gtb-srwf-registration-${{ inputs.version }}.zip", body)
        self.assertIn("GTB_SRWF_REGISTRATION_${{ inputs.version }}_SHA256.txt", body)
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

    def test_post_publication_verifies_remote_tag_release_assets_digest_and_immutability(self) -> None:
        for required in (
            "POST_PUBLISH_TAG_MISMATCH",
            "POST_PUBLISH_DRAFT",
            "POST_PUBLISH_PRERELEASE",
            "POST_PUBLISH_NOT_IMMUTABLE",
            "POST_PUBLISH_ASSET_SET_MISMATCH",
            "POST_PUBLISH_ZIP_DIGEST_MISMATCH",
        ):
            self.assertIn(required, self.workflow)

    def test_historical_read_only_path_remains_without_retroactive_immutability_requirement(self) -> None:
        self.assertIn("ALREADY RELEASED — NO MUTATION", self.workflow)
        self.assertIn("Historical dry-run exception", self.workflow)
        policy = re.search(
            r"- name: Prove GitHub-native Immutable Releases policy for readiness\n(?P<body>.*?)(?=\n      - name: Evaluate publication readiness)",
            self.workflow,
            re.S,
        )
        self.assertIsNotNone(policy)
        self.assertIn('if [[ "$TAG_EXISTS" == true || "$RELEASE_EXISTS" == true ]]; then', policy.group("body"))
        self.assertIn('if [[ "$PUBLISH" == true && "$VERSION" == "0.1.19" ]]; then', self.workflow)


class ReleaseHelperTests(unittest.TestCase):
    def write_json(self, directory: str, name: str, payload: object) -> Path:
        path = Path(directory) / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_version_mismatch_fails(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "does not match source version"):
            release.validate_version(THEME, "9.9.9")

    def test_release_notes_must_identify_requested_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "RELEASE_NOTES.md"
            notes.write_text("# Notes\n\nRelease-Version: 1.2.3\n\nBody.\n", encoding="utf-8")
            release.validate_notes(notes, "1.2.3")
            with self.assertRaisesRegex(RuntimeError, "does not match requested version"):
                release.validate_notes(notes, "1.2.4")

    def test_current_source_release_notes_match_current_source_version(self) -> None:
        current_version = release.plugin_versions(THEME / "src" / "srwf-registration-theme.php")[0]
        release.validate_notes(THEME / "RELEASE_NOTES.md", current_version)

    def test_enabled_native_policy_is_accepted_only_from_api_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            response = self.write_json(tmp, "policy.json", {"enabled": True, "enforced_by_owner": False})
            payload = release.validate_immutable_releases_policy(200, response)
            self.assertIs(payload["enabled"], True)

    def test_disabled_native_policy_fails_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            response = self.write_json(tmp, "policy.json", {})
            with self.assertRaisesRegex(RuntimeError, "IMMUTABLE_RELEASES_POLICY_DISABLED"):
                release.validate_immutable_releases_policy(404, response)
            disabled = self.write_json(tmp, "disabled.json", {"enabled": False, "enforced_by_owner": False})
            with self.assertRaisesRegex(RuntimeError, "IMMUTABLE_RELEASES_POLICY_DISABLED"):
                release.validate_immutable_releases_policy(200, disabled)

    def test_missing_authorization_or_unavailable_policy_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            response = self.write_json(tmp, "policy.json", {})
            for status in (401, 403):
                with self.subTest(status=status):
                    with self.assertRaisesRegex(RuntimeError, "IMMUTABLE_RELEASES_POLICY_UNAUTHORIZED"):
                        release.validate_immutable_releases_policy(status, response)
            with self.assertRaisesRegex(RuntimeError, "IMMUTABLE_RELEASES_POLICY_UNAVAILABLE"):
                release.validate_immutable_releases_policy(500, response)

    def test_malformed_policy_payload_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_enabled = self.write_json(tmp, "missing.json", {"enforced_by_owner": False})
            with self.assertRaisesRegex(RuntimeError, "IMMUTABLE_RELEASES_POLICY_MALFORMED"):
                release.validate_immutable_releases_policy(200, missing_enabled)
            wrong_owner_state = self.write_json(tmp, "owner.json", {"enabled": True})
            with self.assertRaisesRegex(RuntimeError, "IMMUTABLE_RELEASES_POLICY_MALFORMED"):
                release.validate_immutable_releases_policy(200, wrong_owner_state)

    def test_post_publish_release_requires_immutable_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            immutable = self.write_json(tmp, "immutable.json", {"immutable": True})
            payload = release.validate_published_release_immutable(immutable)
            self.assertIs(payload["immutable"], True)

            mutable = self.write_json(tmp, "mutable.json", {"immutable": False})
            with self.assertRaisesRegex(RuntimeError, "POST_PUBLISH_NOT_IMMUTABLE"):
                release.validate_published_release_immutable(mutable)

            unknown = self.write_json(tmp, "unknown.json", {})
            with self.assertRaisesRegex(RuntimeError, "POST_PUBLISH_NOT_IMMUTABLE"):
                release.validate_published_release_immutable(unknown)

    def test_public_zip_is_byte_identical_and_checksum_is_final_bytes(self) -> None:
        version = release.validate_version(
            THEME,
            release.plugin_versions(THEME / "src" / "srwf-registration-theme.php")[0],
        )
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            builder_output = tmp_path / "builder"
            release_output = tmp_path / "release"
            production_zip, diagnostic_zip, _ = builder.build(builder_output)
            result = release.prepare_release_assets(THEME, builder_output, release_output, version)

            public_zip = Path(result["public_zip"])
            checksum_file = Path(result["checksum_file"])
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
        version = release.validate_version(
            THEME,
            release.plugin_versions(THEME / "src" / "srwf-registration-theme.php")[0],
        )
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            builder_output = tmp_path / "builder"
            release_output = tmp_path / "release"
            builder.build(builder_output)
            result = release.prepare_release_assets(THEME, builder_output, release_output, version)
            public_zip = Path(result["public_zip"])

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
