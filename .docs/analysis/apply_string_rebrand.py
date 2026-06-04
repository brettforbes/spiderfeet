#!/usr/bin/env python3
"""Stage 1 #17: replace SpiderFoot/spiderfoot branding strings (preserve code identifiers)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SKIP_DIRS = {
    ".git", ".venv", "__pycache__", "node_modules", ".cursor",
    ".governance/project/bootstrap/history",
}

SKIP_FILES = {
    ".docs/analysis/spiderfeet_reference_inventory.json",
    ".docs/analysis/apply_path_renames.py",
    ".docs/analysis/apply_string_rebrand.py",
    ".seed/planning/github_issues_manifest.json",
    ".seed/planning/create_first_four_github_issues.py",
    ".seed/planning/consolidate_to_module_issues.py",
}

TEXT_EXTENSIONS = {
    ".py", ".js", ".css", ".html", ".tmpl", ".md", ".rst", ".yml", ".yaml",
    ".cfg", ".ini", ".txt", ".gitignore", ".dockerignore", ".mdc", ".json",
    ".toml", ".sh", ".ps1", ".sql",
}

IDENTIFIER_RESTORE = [
    ("TestSpiderfeetWebUiRoutes", "TestSpiderFootWebUiRoutes"),
    ("TestSpiderfeetScanner", "TestSpiderFootScanner"),
    ("TestSpiderfeetCli", "TestSpiderFootCli"),
    ("TestSpiderfeetWebUi", "TestSpiderFootWebUi"),
    ("TestSpiderfeet", "TestSpiderFoot"),
    ("SpiderfeetScanner", "SpiderFootScanner"),
    ("SpiderfeetPluginLogger", "SpiderFootPluginLogger"),
    ("SpiderfeetSqliteLogHandler", "SpiderFootSqliteLogHandler"),
    ("SpiderfeetThreadPool", "SpiderFootThreadPool"),
    ("SpiderfeetCorrelator", "SpiderFootCorrelator"),
    ("SpiderfeetHelpers", "SpiderFootHelpers"),
    ("SpiderfeetPlugin", "SpiderFootPlugin"),
    ("SpiderfeetTarget", "SpiderFootTarget"),
    ("SpiderfeetWebUi", "SpiderFootWebUi"),
    ("SpiderfeetEvent", "SpiderFootEvent"),
    ("SpiderfeetCli", "SpiderFootCli"),
    ("SpiderfeetDb", "SpiderFootDb"),
    ("startSpiderfeetScanner", "startSpiderFootScanner"),
]

CODE_IDENTIFIER_RX = [
    (re.compile(r"\bfrom sflib import Spiderfeet\b"), "from sflib import SpiderFoot"),
    (re.compile(r"\bfrom sfscan import SpiderfeetScanner\b"), "from sfscan import SpiderFootScanner"),
    (re.compile(r"\bclass Spiderfeet\b"), "class SpiderFoot"),
    (re.compile(r"\bSpiderfeet\s*\("), "SpiderFoot("),
]

LITERAL_KEEP = [
    "greynoise-spiderfoot-community",
    "greynoise-spiderfoot",
    "linkedin.com/in/spiderfoot",
    "github.com/smicallef/spiderfoot",
    "asciinema.org/~spiderfoot",
    "spiderfoot-wide.png",
    "spiderfoot-icon.png",
    "spiderfoot-header",
    "twgr%5Espiderfoot",
]

URL_RX = re.compile(r"https?://[^\s\"'<>]+", re.I)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in SKIP_FILES:
        return True
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    if path.suffix.lower() in {".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".pyc"}:
        return True
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return False
    return path.name not in {"Dockerfile", "Dockerfile.full", "LICENSE", "VERSION", "AGENTS.md"}


def protect_literals(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    for keep in sorted(LITERAL_KEEP, key=len, reverse=True):
        while keep in text:
            idx = len(saved)
            saved.append(keep)
            text = text.replace(keep, f"__KEEP_{idx}__", 1)

    for match in URL_RX.finditer(text):
        url = match.group(0)
        if "spiderfoot" in url.lower():
            idx = len(saved)
            saved.append(url)
            text = text.replace(url, f"__KEEP_{idx}__", 1)

    return text, saved


def restore_literals(text: str, saved: list[str]) -> str:
    for idx in range(len(saved) - 1, -1, -1):
        text = text.replace(f"__KEEP_{idx}__", saved[idx])
    return text


def restore_code_identifiers(text: str) -> str:
    for wrong, right in IDENTIFIER_RESTORE:
        text = re.sub(rf"\b{re.escape(wrong)}\b", right, text)
    for rx, repl in CODE_IDENTIFIER_RX:
        text = rx.sub(repl, text)
    return text


def rebrand_text(text: str) -> str:
    text, saved = protect_literals(text)
    text = text.replace("SPIDERFOOT", "SPIDERFEET")
    text = text.replace("SpiderFoot", "Spiderfeet")
    text = text.replace("Spiderfoot", "Spiderfeet")
    text = text.replace("spiderfoot", "spiderfeet")
    text = restore_code_identifiers(text)
    return restore_literals(text, saved)


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
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if rebrand_file(path):
            changed += 1
            print(path.relative_to(ROOT))
    print(f"Rebranded {changed} files")


if __name__ == "__main__":
    main()
