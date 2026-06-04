#!/usr/bin/env python3
"""Normalize package import paths to spiderfeet/ (PEP 8) while keeping SpiderFeet branding."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".cursor"}

# Filesystem / import package uses lowercase spiderfeet on all platforms.
PATH_REPLACEMENTS = [
    ("from spiderFeet.", "from spiderfeet."),
    ("from spiderFeet import", "from spiderfeet import"),
    ("import spiderFeet.", "import spiderfeet."),
    ("spiderFeet/templates/", "spiderfeet/templates/"),
    ("spiderFeet/static/", "spiderfeet/static/"),
    ("'spiderFeet/", "'spiderfeet/"),
    ('"spiderFeet/', '"spiderfeet/'),
    ("/spiderFeet/", "/spiderfeet/"),
    ("]/spiderFeet", "]/spiderfeet"),
    ("{docroot}/static", "{docroot}/static"),  # no-op anchor
]

# Real public site uses spiderfeet.net (lowercase) — fix mistaken host strings.
URL_FIXES = [
    ("www.spiderFeet.net", "www.spiderfeet.net"),
    ("spiderFeet.net", "spiderfeet.net"),
]

# Remaining legacy tokens → SpiderFeet branding.
LEGACY_REPLACEMENTS = [
    ("SpiderFoot", "SpiderFeet"),
    ("Spiderfeet", "SpiderFeet"),
    ("spiderfoot", "spiderFeet"),
]

SKIP_FILES = {
    ".docs/analysis/apply_path_renames.py",
    ".docs/analysis/apply_string_rebrand.py",
    ".docs/analysis/apply_spiderFeet_unified_rename.py",
    ".docs/analysis/fix_spiderFeet_import_paths.py",
}


def transform(text: str) -> str:
    for old, new in PATH_REPLACEMENTS:
        text = text.replace(old, new)
    for old, new in URL_FIXES:
        text = text.replace(old, new)
    for old, new in LEGACY_REPLACEMENTS:
        text = text.replace(old, new)
    # staticdir root in sf.py
    text = text.replace(
        ')/spiderFeet"',
        ')/spiderfeet"',
    )
    text = text.replace(
        ")/spiderFeet'",
        ")/spiderfeet'",
    )
    return text


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(p in SKIP_DIRS for p in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".gif", ".pyc"}:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = transform(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Fixed {changed} files")


if __name__ == "__main__":
    main()
