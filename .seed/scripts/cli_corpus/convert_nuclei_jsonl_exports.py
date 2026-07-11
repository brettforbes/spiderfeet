#!/usr/bin/env python3
"""Convert Nuclei JSONL exports to structured JSON bundles (records[] list of dicts)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent
REPO_ROOT = CORPUS_DIR.parents[2]
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

from nuclei_structured import NUCLEI_STRUCTURED_SCHEMA, dumps_nuclei_bundle, ndjson_to_bundle, parse_ndjson

DEFAULT_DIR = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "exploration_scratch" / "nuclei"


def jsonl_to_bundle_path(jsonl_path: Path, output: Path | None = None) -> Path:
    out = output or jsonl_path.with_suffix(".json")
    raw = jsonl_path.read_text(encoding="utf-8", errors="replace")
    records = parse_ndjson(raw)
    bundle = ndjson_to_bundle(
        raw,
        scan={
            "tool": "nuclei",
            "scenario_id": jsonl_path.stem,
            "source_jsonl": str(jsonl_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "started_at": datetime.fromtimestamp(jsonl_path.stat().st_mtime, tz=timezone.utc).isoformat(),
            "finding_summary_lines": len(records),
            "text_role": "one line per JSONL finding: [severity] template-id @ matched-at",
            "structured_role": "full JSONL finding objects in records[]",
        },
    )
    out.write_text(dumps_nuclei_bundle(bundle), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Nuclei JSONL exports to JSON bundles with records[] (list of dicts)"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="JSONL file(s); default: all *.jsonl in exploration_scratch/nuclei",
    )
    parser.add_argument("-o", "--output", type=Path, help="Output .json path (single input only)")
    args = parser.parse_args()

    inputs = list(args.paths) or sorted(DEFAULT_DIR.glob("*.jsonl"))
    if not inputs:
        print("No JSONL files found.", file=sys.stderr)
        return 1

    for jsonl_path in inputs:
        if not jsonl_path.is_file():
            print(f"Missing: {jsonl_path}", file=sys.stderr)
            return 1
        if args.output and len(inputs) > 1:
            print("Use --output with a single input file only.", file=sys.stderr)
            return 1
        out = jsonl_to_bundle_path(jsonl_path, args.output)
        records = parse_ndjson(jsonl_path.read_text(encoding="utf-8", errors="replace"))
        print(f"Wrote {out} ({len(records)} records, schema={NUCLEI_STRUCTURED_SCHEMA})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
