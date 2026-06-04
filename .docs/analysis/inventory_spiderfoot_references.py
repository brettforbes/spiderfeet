#!/usr/bin/env python3
"""Inventory SpiderFoot/spiderfoot references for Stage 1 rebrand (issue #14)."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_MD = ROOT / ".docs/analysis/spiderfoot_reference_inventory.md"
OUT_JSON = ROOT / ".docs/analysis/spiderfoot_reference_inventory.json"

SKIP_DIRS = {
    ".git", ".venv", "__pycache__", "node_modules", ".cursor", "dist",
    ".governance/project/bootstrap/history",
}
SKIP_FILES_SUFFIX = {".pyc", ".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".eot"}

PATTERNS = [
    ("spiderfoot", re.compile(r"spiderfoot", re.I)),
    ("SpiderFoot", re.compile(r"SpiderFoot")),
    ("Spiderfoot", re.compile(r"Spiderfoot")),
    ("SPIDERFOOT", re.compile(r"SPIDERFOOT")),
]

PATH_PATTERNS = [
    re.compile(r"spiderfoot", re.I),
]


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return True
    if path.suffix.lower() in SKIP_FILES_SUFFIX:
        return True
    if path.name == "spiderfoot_reference_inventory.json":
        return True
    return False


def main() -> None:
    text_hits: dict[str, list[dict]] = defaultdict(list)
    path_hits: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if any(p.search(rel) for p in PATH_PATTERNS):
            path_hits.append(rel)
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, rx in PATTERNS:
            count = len(rx.findall(content))
            if count:
                text_hits[label].append({"path": rel, "count": count})

    summary = {
        label: {"files": len(items), "occurrences": sum(i["count"] for i in items)}
        for label, items in text_hits.items()
    }

    OUT_JSON.write_text(
        json.dumps(
            {"summary": summary, "path_hits": sorted(path_hits), "text_hits": text_hits},
            indent=2,
        ),
        encoding="utf-8",
    )

    lines = [
        "# SpiderFoot Reference Inventory",
        "",
        "**Issue:** #14 (SF-01-01) | **Spec:** SPEC-002 R2-01-01",
        f"**Generated:** from `{ROOT.name}` repo root",
        "",
        "## Summary",
        "",
        "| Pattern | Files | Occurrences |",
        "|---------|------:|------------:|",
    ]
    for label in ["SpiderFoot", "spiderfoot", "Spiderfoot", "SPIDERFOOT"]:
        s = summary.get(label, {"files": 0, "occurrences": 0})
        lines.append(f"| `{label}` | {s['files']} | {s['occurrences']} |")

    lines += [
        "",
        f"**Paths containing `spiderfoot` in filename/directory:** {len(path_hits)}",
        "",
        "## Path renames required",
        "",
    ]
    for p in sorted(path_hits)[:80]:
        lines.append(f"- `{p}`")
    if len(path_hits) > 80:
        lines.append(f"- … and {len(path_hits) - 80} more (see JSON)")

    lines += [
        "",
        "## Top files by occurrence (any pattern)",
        "",
    ]
    merged: dict[str, int] = defaultdict(int)
    for items in text_hits.values():
        for item in items:
            merged[item["path"]] += item["count"]
    for path, count in sorted(merged.items(), key=lambda x: -x[1])[:40]:
        lines.append(f"- `{path}` — {count}")

    lines += [
        "",
        "## Allowlist candidates (review before rename)",
        "",
        "- Upstream fork attribution in README if retained temporarily",
        "- `.docs/analysis/` historical exports",
        "- Git remote URLs until repo rename confirmed",
        "",
        "## Next issue",
        "",
        "#15 — Rename files and directories (SF-01-02)",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD} and {OUT_JSON}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
