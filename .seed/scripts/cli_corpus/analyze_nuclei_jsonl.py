#!/usr/bin/env python3
"""Summarize semantic variety in a Nuclei JSONL export."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}")


def iter_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("{"):
            records.append(json.loads(line))
    return records


def shape_key(rec: dict[str, Any]) -> str:
    info = rec.get("info") or {}
    severity = info.get("severity", "unknown")
    proto = rec.get("type", "unknown")
    has_matcher = "matcher-name" in rec
    has_extracted = bool(rec.get("extracted-results"))
    has_cve = bool(CVE_RE.search(json.dumps(rec)))
    classification = info.get("classification") or {}
    has_class_cve = bool(classification.get("cve-id"))
    tags = tuple(sorted((info.get("tags") or [])[:3]))
    return (
        f"severity={severity}|type={proto}|matcher={has_matcher}|extracted={has_extracted}"
        f"|cve_line={has_cve}|cve_class={has_class_cve}|tags_sample={tags}"
    )


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {"record_count": 0, "shapes": {}, "severities": {}, "types": {}, "template_ids": []}

    shapes: Counter[str] = Counter()
    severities: Counter[str] = Counter()
    types: Counter[str] = Counter()
    template_ids: Counter[str] = Counter()

    for rec in records:
        info = rec.get("info") or {}
        shapes[shape_key(rec)] += 1
        severities[str(info.get("severity", "unknown"))] += 1
        types[str(rec.get("type", "unknown"))] += 1
        template_ids[str(rec.get("template-id", "unknown"))] += 1

    return {
        "record_count": len(records),
        "unique_templates_matched": len(template_ids),
        "severities": dict(severities.most_common()),
        "types": dict(types.most_common()),
        "shapes": dict(shapes.most_common(50)),
        "top_templates": template_ids.most_common(30),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Nuclei JSONL semantic variety")
    parser.add_argument("jsonl", type=Path, help="Path to JSONL export")
    parser.add_argument("-o", "--output", type=Path, help="Write JSON summary here")
    args = parser.parse_args()

    if not args.jsonl.is_file():
        print(f"Missing file: {args.jsonl}", file=sys.stderr)
        return 1

    records = iter_records(args.jsonl)
    report = {"source": str(args.jsonl), **summarize(records)}
    text = json.dumps(report, indent=2) + "\n"

    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
