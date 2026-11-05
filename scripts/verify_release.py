#!/usr/bin/env python3
"""Make and verify SHA-256 release inventory, including built site and source.

Usage:
    python3 scripts/verify_release.py --write  # package maintainer, after build
    python3 scripts/verify_release.py          # verify downloaded package

Python standard library only; errors cause nonzero exit codes.
"""
from __future__ import annotations
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'MANIFEST.sha256'
IGNORE_DIRS = {'.git', '.venv', '.pytest_cache', '__pycache__', '.mypy_cache', '.DS_Store'}
IGNORE_NAMES = {'.DS_Store', 'MANIFEST.sha256'}


def files_in_release():
    return sorted((p for p in ROOT.rglob('*') if p.is_file()
                   and not any(part in IGNORE_DIRS for part in p.relative_to(ROOT).parts)
                   and p.name not in IGNORE_NAMES),
                  key=lambda p: p.relative_to(ROOT).as_posix())


def sha256(path: Path):
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(part)
    return digest.hexdigest()


def write():
    files = files_in_release()
    MANIFEST.write_text(''.join(f'{sha256(p)}  {p.relative_to(ROOT).as_posix()}\n'
                                for p in files), encoding='utf-8')
    print(f'Wrote {len(files)} SHA-256 entries to {MANIFEST.relative_to(ROOT)}')
    return 0


def check():
    if not MANIFEST.is_file():
        print('Missing MANIFEST.sha256: use --write when building a release', file=sys.stderr)
        return 2
    expected = {}
    for line_num, line in enumerate(MANIFEST.read_text(encoding='utf-8').splitlines(), 1):
        if not line:
            continue
        try:
            digest, rel = line.split('  ', 1)
        except ValueError:
            print(f'Invalid manifest line {line_num}', file=sys.stderr)
            return 2
        relpath = Path(rel)
        if (len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest)
                or relpath.is_absolute() or '..' in relpath.parts or rel in expected):
            print(f'Invalid manifest entry {line_num}', file=sys.stderr)
            return 2
        expected[rel] = digest
    actual = {p.relative_to(ROOT).as_posix(): p for p in files_in_release()}
    missing, added, changed = sorted(expected.keys() - actual.keys()), sorted(actual.keys() - expected.keys()), []
    for rel in sorted(actual.keys() & expected.keys()):
        if sha256(actual[rel]) != expected[rel]:
            changed.append(rel)
    if missing or added or changed:
        for what, names in [('Missing', missing), ('Extra', added), ('Changed', changed)]:
            for name in names[:12]:
                print(f'{what}: {name}', file=sys.stderr)
            if len(names) > 12:
                print(f'... plus {len(names)-12} more {what.lower()} files', file=sys.stderr)
        return 1
    print(f'PASS: all {len(expected)} release files match SHA-256 manifest')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check package file integrity against release SHA-256 manifest')
    parser.add_argument('--write', action='store_true', help='Recreate manifest after successful build and tests')
    args = parser.parse_args()
    sys.exit(write() if args.write else check())
