#!/usr/bin/env python3
"""Unified SpiderFeet rebrand: paths, filenames, identifiers, and all string variants."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".cursor"}

SKIP_FILES = {
    ".docs/analysis/apply_spiderFeet_unified_rename.py",
    ".docs/analysis/apply_path_renames.py",
    ".docs/analysis/apply_string_rebrand.py",
}

DIR_RENAMES = [
    ("spiderfeet", "spiderFeet"),
    ("test/unit/spiderfeet", "test/unit/spiderFeet"),
]

FILE_RENAMES = [
    ("docs/spiderfeet.rst", "docs/spiderFeet.rst"),
    ("test/unit/test_spiderfeet.py", "test/unit/test_spiderFeet.py"),
    ("test/unit/test_spiderfeetcli.py", "test/unit/test_spiderFeetcli.py"),
    ("test/unit/test_spiderfeetscanner.py", "test/unit/test_spiderFeetscanner.py"),
    ("test/unit/test_spiderfeetwebui.py", "test/unit/test_spiderFeetwebui.py"),
    ("spiderFeet/static/css/spiderfeet.css", "spiderFeet/static/css/spiderFeet.css"),
    ("spiderFeet/static/js/spiderfeet.js", "spiderFeet/static/js/spiderFeet.js"),
    ("spiderFeet/static/js/spiderfeet.newscan.js", "spiderFeet/static/js/spiderFeet.newscan.js"),
    ("spiderFeet/static/js/spiderfeet.opts.js", "spiderFeet/static/js/spiderFeet.opts.js"),
    ("spiderFeet/static/js/spiderfeet.scanlist.js", "spiderFeet/static/js/spiderFeet.scanlist.js"),
    ("spiderFeet/static/img/spiderfeet-header.png", "spiderFeet/static/img/spiderFeet-header.png"),
    ("spiderFeet/static/img/spiderfeet-header-dark.png", "spiderFeet/static/img/spiderFeet-header-dark.png"),
    ("spiderFeet/static/img/spiderfeet-icon.png", "spiderFeet/static/img/spiderFeet-icon.png"),
    (".docs/analysis/inventory_spiderfeet_references.py", ".docs/analysis/inventory_spiderFeet_references.py"),
    (".docs/analysis/spiderfeet_reference_inventory.md", ".docs/analysis/spiderFeet_reference_inventory.md"),
    (".docs/analysis/spiderfeet_reference_inventory.json", ".docs/analysis/spiderFeet_reference_inventory.json"),
    (".docs/analysis/spiderfoot_string_allowlist.md", ".docs/analysis/spiderFeet_string_allowlist.md"),
]

TEST_FILE_RENAMES = [
    ("test_spiderfeetcorrelator.py", "test_spiderFeetcorrelator.py"),
    ("test_spiderfeetdb.py", "test_spiderFeetdb.py"),
    ("test_spiderfeetevent.py", "test_spiderFeetevent.py"),
    ("test_spiderfeethelpers.py", "test_spiderFeethelpers.py"),
    ("test_spiderfeetplugin.py", "test_spiderFeetplugin.py"),
    ("test_spiderfeettarget.py", "test_spiderFeettarget.py"),
    ("test_spiderfeetthreadpool.py", "test_spiderFeetthreadpool.py"),
]

TEXT_REPLACEMENTS = [
    ("SPIDERFOOT", "SPIDERFEET"),
    ("SpiderFoot", "SpiderFeet"),
    ("Spiderfeet", "SpiderFeet"),
    ("Spiderfoot", "SpiderFeet"),
    ("spiderfoot", "spiderFeet"),
    ("spiderfeet", "spiderFeet"),
]

TEXT_EXTENSIONS = {
    ".py", ".js", ".css", ".html", ".tmpl", ".md", ".rst", ".yml", ".yaml",
    ".cfg", ".ini", ".txt", ".gitignore", ".dockerignore", ".mdc", ".json",
    ".toml", ".sh", ".ps1", ".sql", ".tql",
}


def git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print(f"SKIP missing: {src}")
        return
    if src.resolve() == dst.resolve():
        return
    if dst.exists():
        print(f"SKIP exists: {dst}")
        return
    subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)
    print(f"git mv {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def rebrand_text(text: str) -> str:
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def rebrand_file(path: Path) -> bool:
    try:
        original = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    updated = rebrand_text(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    for old, new in DIR_RENAMES:
        git_mv(ROOT / old, ROOT / new)

    for old, new in FILE_RENAMES:
        git_mv(ROOT / old, ROOT / new)

    for old, new in TEST_FILE_RENAMES:
        git_mv(ROOT / "test/unit/spiderFeet" / old, ROOT / "test/unit/spiderFeet" / new)

    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".pyc"}:
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {
            "Dockerfile", "Dockerfile.full", "LICENSE", "VERSION", "AGENTS.md",
        }:
            continue
        if rebrand_file(path):
            changed += 1
    print(f"Updated text in {changed} files")


if __name__ == "__main__":
    main()
