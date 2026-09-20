from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from types import ModuleType

VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
NOTES_VERSION_RE = re.compile(r"^Release-Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", re.M)
FORBIDDEN_ARCHIVE_SEGMENTS = {"tests", "reference", "diagnostic"}
PROTECTED_HISTORICAL_RELEASES = {
    "0.1.19": {
        "tag": "srwf-registration-v0.1.19",
        "source_sha": "4e5727ec3573bc08395c43a99312f157f062a347",
        "zip_sha256": "e31c11dfb75131e1cc99cab0f4f0da484ee9c238eaa36443766570ad508728ef",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def plugin_versions(plugin_file: Path) -> tuple[str, str]:
    source = plugin_file.read_text(encoding="utf-8")
    header = re.search(r"^ \* Version: ([0-9]+\.[0-9]+\.[0-9]+)$", source, re.M)
    constant = re.search(r"const SRWF_REGISTRATION_THEME_VERSION = '([^']+)';", source)
    if not header or not constant:
        raise RuntimeError(f"unable to read SRWF version from {plugin_file}")
    return header.group(1), constant.group(1)


def validate_version(theme_root: Path, requested_version: str) -> str:
    if not VERSION_RE.fullmatch(requested_version):
        raise RuntimeError("requested version must use x.y.z numeric format")

    plugin_file = theme_root / "src" / "srwf-registration-theme.php"
    header_version, constant_version = plugin_versions(plugin_file)
    if header_version != constant_version:
        raise RuntimeError(
            f"source version is internally inconsistent: header={header_version}, constant={constant_version}"
        )
    if requested_version != header_version:
        raise RuntimeError(
            f"requested version {requested_version} does not match source version {header_version}"
        )
    return header_version


def validate_notes(notes_path: Path, requested_version: str) -> None:
    if not notes_path.is_file():
        raise RuntimeError(f"release notes are missing from exact source: {notes_path}")

    source = notes_path.read_text(encoding="utf-8")
    match = NOTES_VERSION_RE.search(source)
    if not match:
        raise RuntimeError("release notes must contain an exact 'Release-Version: x.y.z' line")
    if match.group(1) != requested_version:
        raise RuntimeError(
            f"release notes version {match.group(1)} does not match requested version {requested_version}"
        )
    if len(source.strip().splitlines()) < 4:
        raise RuntimeError("release notes are unexpectedly empty")


def read_json_object(path: Path, error_code: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{error_code}: unable to read valid GitHub JSON from {path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{error_code}: GitHub response must be a JSON object")
    return payload


def validate_immutable_releases_policy(http_status: int, response_path: Path) -> dict[str, object]:
    if http_status == 404:
        raise RuntimeError(
            "IMMUTABLE_RELEASES_POLICY_DISABLED: GitHub reports immutable releases are not enabled for this repository"
        )
    if http_status in {401, 403}:
        raise RuntimeError(
            "IMMUTABLE_RELEASES_POLICY_UNAUTHORIZED: policy-read credential cannot read repository immutable-release status"
        )
    if http_status != 200:
        raise RuntimeError(
            f"IMMUTABLE_RELEASES_POLICY_UNAVAILABLE: GitHub policy-status API returned HTTP {http_status}"
        )

    payload = read_json_object(response_path, "IMMUTABLE_RELEASES_POLICY_MALFORMED")
    enabled = payload.get("enabled")
    if enabled is False:
        raise RuntimeError(
            "IMMUTABLE_RELEASES_POLICY_DISABLED: GitHub policy response reports enabled=false"
        )
    if enabled is not True:
        raise RuntimeError(
            "IMMUTABLE_RELEASES_POLICY_MALFORMED: GitHub policy response does not contain enabled=true"
        )
    if payload.get("enforced_by_owner") not in {True, False}:
        raise RuntimeError(
            "IMMUTABLE_RELEASES_POLICY_MALFORMED: GitHub policy response has no boolean enforced_by_owner state"
        )
    return payload


def validate_published_release_immutable(release_json: Path) -> dict[str, object]:
    payload = read_json_object(release_json, "POST_PUBLISH_RELEASE_STATE_MALFORMED")
    if payload.get("immutable") is not True:
        raise RuntimeError(
            "POST_PUBLISH_NOT_IMMUTABLE: published GitHub Release does not report immutable=true"
        )
    return payload


def load_source_builder(theme_root: Path) -> ModuleType:
    builder_path = theme_root / "tests" / "build_owner_test_packages.py"
    if not builder_path.is_file():
        raise RuntimeError(f"deterministic builder is missing: {builder_path}")

    spec = importlib.util.spec_from_file_location("srwf_source_builder", builder_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load deterministic builder: {builder_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def archive_files(archive: Path, install_root: str) -> list[str]:
    root_prefix = f"{install_root}/"
    with zipfile.ZipFile(archive) as bundle:
        names = [name for name in bundle.namelist() if not name.endswith("/")]

    if not names:
        raise RuntimeError("production archive is empty")
    for name in names:
        if not name.startswith(root_prefix):
            raise RuntimeError(f"unexpected archive root: {name}")
    return sorted(name[len(root_prefix) :] for name in names)


def assert_no_forbidden_content(relative_files: list[str]) -> None:
    for relative in relative_files:
        parts = set(Path(relative).parts)
        forbidden = sorted(parts & FORBIDDEN_ARCHIVE_SEGMENTS)
        if forbidden:
            raise RuntimeError(f"production archive contains forbidden content: {relative}: {forbidden}")


def archive_plugin_versions(archive: Path, install_root: str) -> tuple[str, str]:
    member = f"{install_root}/srwf-registration-theme.php"
    with zipfile.ZipFile(archive) as bundle:
        try:
            source = bundle.read(member).decode("utf-8")
        except KeyError as exc:
            raise RuntimeError(f"production archive is missing {member}") from exc

    header = re.search(r"^ \* Version: ([0-9]+\.[0-9]+\.[0-9]+)$", source, re.M)
    constant = re.search(r"const SRWF_REGISTRATION_THEME_VERSION = '([^']+)';", source)
    if not header or not constant:
        raise RuntimeError("unable to read version from packaged SRWF plugin")
    return header.group(1), constant.group(1)


def prepare_release_assets(
    theme_root: Path,
    builder_output: Path,
    release_dir: Path,
    requested_version: str,
) -> dict[str, str]:
    validate_version(theme_root, requested_version)
    builder = load_source_builder(theme_root)

    source_zip = builder_output / f"gtb-srwf-registration-owner-test-{requested_version}.zip"
    if not source_zip.is_file():
        raise RuntimeError(f"deterministic production package is missing: {source_zip}")

    release_dir.mkdir(parents=True, exist_ok=True)
    public_zip = release_dir / f"gtb-srwf-registration-{requested_version}.zip"
    checksum_file = release_dir / f"GTB_SRWF_REGISTRATION_{requested_version}_SHA256.txt"

    shutil.copyfile(source_zip, public_zip)
    source_hash = sha256(source_zip)
    public_hash = sha256(public_zip)
    if source_hash != public_hash:
        raise RuntimeError("public ZIP is not byte-identical to deterministic builder output")

    install_root = "gtb-srwf-registration"
    builder.smoke_archive(
        public_zip,
        builder.PRODUCTION_FILES,
        install_root,
        check_css=True,
    )

    actual_files = archive_files(public_zip, install_root)
    expected_files = sorted(builder.PRODUCTION_FILES)
    if actual_files != expected_files:
        raise RuntimeError(
            f"release package file set differs from deterministic builder contract: {actual_files}"
        )
    assert_no_forbidden_content(actual_files)

    header_version, constant_version = archive_plugin_versions(public_zip, install_root)
    if header_version != requested_version or constant_version != requested_version:
        raise RuntimeError(
            "packaged version does not match requested release version: "
            f"header={header_version}, constant={constant_version}, requested={requested_version}"
        )

    checksum_file.write_text(f"{public_hash}  {public_zip.name}\n", encoding="utf-8")

    return {
        "version": requested_version,
        "source_zip": str(source_zip),
        "public_zip": str(public_zip),
        "checksum_file": str(checksum_file),
        "sha256": public_hash,
        "tag": f"srwf-registration-v{requested_version}",
    }


def command_validate_version(args: argparse.Namespace) -> int:
    version = validate_version(args.theme_root.resolve(), args.version)
    print(version)
    return 0


def command_validate_notes(args: argparse.Namespace) -> int:
    validate_notes(args.notes.resolve(), args.version)
    print(args.notes)
    return 0


def command_validate_immutable_policy(args: argparse.Namespace) -> int:
    payload = validate_immutable_releases_policy(args.http_status, args.response.resolve())
    print(json.dumps(payload, sort_keys=True))
    return 0


def command_validate_published_immutability(args: argparse.Namespace) -> int:
    payload = validate_published_release_immutable(args.release_json.resolve())
    print(json.dumps({"immutable": payload["immutable"]}, sort_keys=True))
    return 0


def command_prepare_assets(args: argparse.Namespace) -> int:
    result = prepare_release_assets(
        args.theme_root.resolve(),
        args.builder_output.resolve(),
        args.release_dir.resolve(),
        args.version,
    )
    if args.summary_file:
        args.summary_file.parent.mkdir(parents=True, exist_ok=True)
        args.summary_file.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SRWF Registration release-local safety helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    version_parser = subparsers.add_parser("validate-version")
    version_parser.add_argument("--theme-root", type=Path, required=True)
    version_parser.add_argument("--version", required=True)
    version_parser.set_defaults(func=command_validate_version)

    notes_parser = subparsers.add_parser("validate-notes")
    notes_parser.add_argument("--notes", type=Path, required=True)
    notes_parser.add_argument("--version", required=True)
    notes_parser.set_defaults(func=command_validate_notes)

    policy_parser = subparsers.add_parser("validate-immutable-policy")
    policy_parser.add_argument("--http-status", type=int, required=True)
    policy_parser.add_argument("--response", type=Path, required=True)
    policy_parser.set_defaults(func=command_validate_immutable_policy)

    published_parser = subparsers.add_parser("validate-published-immutability")
    published_parser.add_argument("--release-json", type=Path, required=True)
    published_parser.set_defaults(func=command_validate_published_immutability)

    package_parser = subparsers.add_parser("prepare-assets")
    package_parser.add_argument("--theme-root", type=Path, required=True)
    package_parser.add_argument("--builder-output", type=Path, required=True)
    package_parser.add_argument("--release-dir", type=Path, required=True)
    package_parser.add_argument("--summary-file", type=Path)
    package_parser.add_argument("--version", required=True)
    package_parser.set_defaults(func=command_prepare_assets)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except RuntimeError as exc:
        print(f"release gate failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
