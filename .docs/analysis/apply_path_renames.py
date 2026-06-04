#!/usr/bin/env python3
"""Stage 1 #15: rename spiderfoot paths to spiderfeet (files, dirs, import paths)."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (old relative path, new relative path) — directories first via git mv
DIR_RENAMES = [
    ("spiderfoot", "spiderfeet"),
    ("test/unit/spiderfoot", "test/unit/spiderfeet"),
]

FILE_RENAMES = [
    ("docs/spiderfeet.rst", "docs/spiderfeet.rst"),
    ("test/unit/test_spiderfeet.py", "test/unit/test_spiderfeet.py"),
    ("test/unit/test_spiderfeetcli.py", "test/unit/test_spiderfeetcli.py"),
    ("test/unit/test_spiderfeetscanner.py", "test/unit/test_spiderfeetscanner.py"),
    ("test/unit/test_spiderfeetwebui.py", "test/unit/test_spiderfeetwebui.py"),
    ("spiderfeet/static/css/spiderfeet.css", "spiderfeet/static/css/spiderfeet.css"),
    ("spiderfeet/static/js/spiderfeet.js", "spiderfeet/static/js/spiderfeet.js"),
    ("spiderfeet/static/js/spiderfeet.newscan.js", "spiderfeet/static/js/spiderfeet.newscan.js"),
    ("spiderfeet/static/js/spiderfeet.opts.js", "spiderfeet/static/js/spiderfeet.opts.js"),
    ("spiderfeet/static/js/spiderfeet.scanlist.js", "spiderfeet/static/js/spiderfeet.scanlist.js"),
    (".docs/analysis/inventory_spiderfeet_references.py", ".docs/analysis/inventory_spiderfeet_references.py"),
    (".docs/analysis/spiderfeet_reference_inventory.md", ".docs/analysis/spiderfeet_reference_inventory.md"),
    (".docs/analysis/spiderfeet_reference_inventory.json", ".docs/analysis/spiderfeet_reference_inventory.json"),
]

# After test dir rename, rename test module files
TEST_FILE_GLOBS = [
    ("test_spiderfeetcorrelator.py", "test_spiderfeetcorrelator.py"),
    ("test_spiderfeetdb.py", "test_spiderfeetdb.py"),
    ("test_spiderfeetevent.py", "test_spiderfeetevent.py"),
    ("test_spiderfeethelpers.py", "test_spiderfeethelpers.py"),
    ("test_spiderfeetplugin.py", "test_spiderfeetplugin.py"),
    ("test_spiderfeettarget.py", "test_spiderfeettarget.py"),
    ("test_spiderfeetthreadpool.py", "test_spiderfeetthreadpool.py"),
]

SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".cursor"}

TEXT_EXTENSIONS = {
    ".py", ".js", ".css", ".html", ".tmpl", ".md", ".rst", ".yml", ".yaml",
    ".cfg", ".ini", ".txt", ".gitignore", ".dockerignore", ".mdc", ".json",
    ".toml", ".sh", ".ps1", ".tmpl", ".sql",
}


def git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print(f"SKIP missing: {src}")
        return
    if dst.exists():
        print(f"SKIP exists: {dst}")
        return
    subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)
    print(f"git mv {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def replace_in_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    orig = text
    # Path segments and import paths (not class names SpiderFoot*)
    text = text.replace("spiderfeet/", "spiderfeet/")
    text = text.replace("spiderfeet.", "spiderfeet.")
    text = re.sub(r"\bfrom spiderfoot\b", "from spiderfeet", text)
    text = re.sub(r"\bimport spiderfoot\b", "import spiderfeet", text)
    # Renamed static assets
    for old, new in [
        ("spiderfeet.css", "spiderfeet.css"),
        ("spiderfeet.js", "spiderfeet.js"),
        ("spiderfeet.newscan.js", "spiderfeet.newscan.js"),
        ("spiderfeet.opts.js", "spiderfeet.opts.js"),
        ("spiderfeet.scanlist.js", "spiderfeet.scanlist.js"),
        ("docs/spiderfeet.rst", "docs/spiderfeet.rst"),
        ("test/unit/spiderfeet/", "test/unit/spiderfeet/"),
        ("inventory_spiderfeet_references", "inventory_spiderfeet_references"),
        ("spiderfeet_reference_inventory", "spiderfeet_reference_inventory"),
    ]:
        text = text.replace(old, new)
    # Test file renames in strings
    for old, new in TEST_FILE_GLOBS:
        text = text.replace(f"test/unit/spiderfeet/{old}", f"test/unit/spiderfeet/{new}")
        text = text.replace(old, new)
    for old, new in [
        ("test_spiderfeet.py", "test_spiderfeet.py"),
        ("test_spiderfeetcli.py", "test_spiderfeetcli.py"),
        ("test_spiderfeetscanner.py", "test_spiderfeetscanner.py"),
        ("test_spiderfeetwebui.py", "test_spiderfeetwebui.py"),
    ]:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    # 1) Directory renames
    for old, new in DIR_RENAMES:
        git_mv(ROOT / old, ROOT / new)

    # 2) File renames (spiderfeet package must exist first)
    for old, new in FILE_RENAMES:
        git_mv(ROOT / old, ROOT / new)

    for old, new in TEST_FILE_GLOBS:
        git_mv(ROOT / "test/unit/spiderfeet" / old, ROOT / "test/unit/spiderfeet" / new)

    # 3) Text updates for path/import references
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in (
            "Dockerfile", "Dockerfile.full", ".gitignore", ".dockerignore", "LICENSE", "VERSION"
        ):
            continue
        if replace_in_file(path):
            changed += 1
    print(f"Updated {changed} files with path/import references")


if __name__ == "__main__":
    main()
