from __future__ import annotations

import argparse
import hashlib
import re
import tempfile
import zipfile
from pathlib import Path

THEME = Path(__file__).resolve().parents[1]
PRODUCTION = THEME / 'src'
DIAGNOSTIC = THEME / 'diagnostic'

PRODUCTION_FILES = (
    'srwf-registration-theme.php',
    'srwf-registration-settings.php',
    'srwf-registration.css',
    'icons/report-card-file.svg',
    'icons/section-contact.svg',
    'icons/section-education.svg',
    'icons/section-identity.svg',
    'icons/section-school-documents.svg',
    'icons/section-student-photo.svg',
)
DIAGNOSTIC_FILES = (
    'srwf-runtime-diagnostic.php',
    'assets/runtime-diagnostic.js',
    'assets/admission-diagnostic.js',
)


def read_version(path: Path, constant: str) -> str:
    source = path.read_text(encoding='utf-8')
    header = re.search(r'^ \* Version: ([0-9]+\.[0-9]+\.[0-9]+)$', source, re.M)
    const = re.search(rf"const {re.escape(constant)} = '([^']+)';", source)
    if not header or not const or header.group(1) != const.group(1):
        raise RuntimeError(f'unsynchronized package version in {path}')
    return const.group(1)


def local_css_urls(css_source: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)", css_source):
        value = match.group(2).strip()
        if not value or value.startswith(('data:', 'http://', 'https://', '//', '#')):
            continue
        values.append(value.split('?', 1)[0].split('#', 1)[0])
    return values


def deterministic_zip(source_root: Path, files: tuple[str, ...], archive: Path, install_root: str) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for relative in sorted(files):
            path = source_root / relative
            if not path.is_file():
                raise RuntimeError(f'missing runtime dependency: {path}')
            info = zipfile.ZipInfo(f'{install_root}/{relative}')
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())


def smoke_archive(archive: Path, expected_files: tuple[str, ...], install_root: str, check_css: bool = False) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        destination = Path(tmp)
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(destination)
        root = destination / install_root
        actual = sorted(str(path.relative_to(root)).replace('\\', '/') for path in root.rglob('*') if path.is_file())
        if actual != sorted(expected_files):
            raise RuntimeError(f'archive runtime file set mismatch: {archive.name}: {actual}')
        if check_css:
            css = root / 'srwf-registration.css'
            for relative in local_css_urls(css.read_text(encoding='utf-8')):
                candidate = (css.parent / relative).resolve()
                if root.resolve() not in candidate.parents or not candidate.is_file():
                    raise RuntimeError(f'unresolved extracted CSS dependency: {relative}')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(output_dir: Path) -> tuple[Path, Path, Path]:
    production_version = read_version(PRODUCTION / 'srwf-registration-theme.php', 'SRWF_REGISTRATION_THEME_VERSION')
    diagnostic_version = read_version(DIAGNOSTIC / 'srwf-runtime-diagnostic.php', 'GTB_SRWF_RUNTIME_DIAGNOSTIC_VERSION')

    production_zip = output_dir / f'gtb-srwf-registration-owner-test-{production_version}.zip'
    diagnostic_zip = output_dir / f'gtb-srwf-runtime-diagnostic-v{diagnostic_version}.zip'
    manifest = output_dir / 'GTB_SRWF_OWNER_TEST_PACKAGES_SHA256.txt'

    deterministic_zip(PRODUCTION, PRODUCTION_FILES, production_zip, 'gtb-srwf-registration')
    deterministic_zip(DIAGNOSTIC, DIAGNOSTIC_FILES, diagnostic_zip, 'gtb-srwf-runtime-diagnostic')

    smoke_archive(production_zip, PRODUCTION_FILES, 'gtb-srwf-registration', check_css=True)
    smoke_archive(diagnostic_zip, DIAGNOSTIC_FILES, 'gtb-srwf-runtime-diagnostic')

    manifest.write_text(
        f'{sha256(production_zip)}  {production_zip.name}\n'
        f'{sha256(diagnostic_zip)}  {diagnostic_zip.name}\n',
        encoding='utf-8',
    )
    return production_zip, diagnostic_zip, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    production_zip, diagnostic_zip, manifest = build(args.output_dir)
    print(production_zip)
    print(diagnostic_zip)
    print(manifest)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
