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
    header = re.search(r"^ \* Version:\s*([^\s]+)\s*$", source, re.M)
    constant = re.search(r"const SRWF_REGISTRATION_THEME_VERSION = '([^']+)';", source)
    if not header or not constant:
        raise RuntimeError(f"unable to read SRWF version from {plugin_file}")
    return header.group(1), constant.group(1)


def resolve_version(theme_root: Path) -> str:
    plugin_file = theme_root / "src" / "srwf-registration-theme.php"
    header_version, constant_version = plugin_versions(plugin_file)
    if not VERSION_RE.fullmatch(header_version) or not VERSION_RE.fullmatch(constant_version):
        raise RuntimeError(
            "source version must use x.y.z numeric format: "
            f"header={header_version}, constant={constant_version}"
        )
    if header_version != constant_version:
        raise RuntimeError(
            f"source version is internally inconsistent: header={header_version}, constant={constant_version}"
        )
    return header_version


def validate_notes(notes_path: Path, source_version: str) -> None:
    if not VERSION_RE.fullmatch(source_version):
        raise RuntimeError("derived source version must use x.y.z numeric format")
    if not notes_path.is_file():
        raise RuntimeError(f"release notes are missing from exact source: {notes_path}")

    source = notes_path.read_text(encoding="utf-8")
    match = NOTES_VERSION_RE.search(source)
    if not match:
        raise RuntimeError("release notes must contain an exact 'Release-Version: x.y.z' line")
    if match.group(1) != source_version:
        raise RuntimeError(
            f"release notes version {match.group(1)} does not match derived source version {source_version}"
        )
    if len(source.strip().splitlines()) < 4:
        raise RuntimeError("release notes are unexpectedly empty")


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
) -> dict[str, str]:
    version = resolve_version(theme_root)
    builder = load_source_builder(theme_root)

    source_zip = builder_output / f"gtb-srwf-registration-owner-test-{version}.zip"
    if not source_zip.is_file():
        raise RuntimeError(f"deterministic production package is missing: {source_zip}")

    release_dir.mkdir(parents=True, exist_ok=True)
    public_zip = release_dir / f"gtb-srwf-registration-{version}.zip"
    checksum_file = release_dir / f"GTB_SRWF_REGISTRATION_{version}_SHA256.txt"

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
    if header_version != version or constant_version != version:
        raise RuntimeError(
            "packaged version does not match derived source version: "
            f"header={header_version}, constant={constant_version}, source={version}"
        )

    checksum_file.write_text(f"{public_hash}  {public_zip.name}\n", encoding="utf-8")

    return {
        "version": version,
        "source_zip": str(source_zip),
        "public_zip": str(public_zip),
        "checksum_file": str(checksum_file),
        "sha256": public_hash,
        "tag": f"srwf-registration-v{version}",
    }


def command_resolve_version(args: argparse.Namespace) -> int:
    print(resolve_version(args.theme_root.resolve()))
    return 0


def command_validate_notes(args: argparse.Namespace) -> int:
    validate_notes(args.notes.resolve(), args.version)
    print(args.notes)
    return 0


def command_prepare_assets(args: argparse.Namespace) -> int:
    result = prepare_release_assets(
        args.theme_root.resolve(),
        args.builder_output.resolve(),
        args.release_dir.resolve(),
    )
    if args.summary_file:
        args.summary_file.parent.mkdir(parents=True, exist_ok=True)
        args.summary_file.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SRWF Registration release-local safety helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    version_parser = subparsers.add_parser("resolve-version")
    version_parser.add_argument("--theme-root", type=Path, required=True)
    version_parser.set_defaults(func=command_resolve_version)

    notes_parser = subparsers.add_parser("validate-notes")
    notes_parser.add_argument("--notes", type=Path, required=True)
    notes_parser.add_argument("--version", required=True)
    notes_parser.set_defaults(func=command_validate_notes)

    package_parser = subparsers.add_parser("prepare-assets")
    package_parser.add_argument("--theme-root", type=Path, required=True)
    package_parser.add_argument("--builder-output", type=Path, required=True)
    package_parser.add_argument("--release-dir", type=Path, required=True)
    package_parser.add_argument("--summary-file", type=Path)
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
