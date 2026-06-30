#!/usr/bin/env python3
"""Backfill nerva structured JSON bundles with root-level scan metadata."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent
REPO_ROOT = CORPUS_DIR.parents[2]
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

from nerva_structured import build_nerva_bundle, dumps_nerva_bundle, nerva_scan_context, parse_nerva_structured

EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs" / "nerva"


def main() -> int:
    updated = 0
    for manifest_path in sorted(EXAM_ROOT.glob("*_manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        structured_rel = manifest.get("structured_path")
        if not structured_rel:
            continue
        structured_path = REPO_ROOT / structured_rel
        if not structured_path.is_file():
            continue
        records = parse_nerva_structured(structured_path.read_text(encoding="utf-8"))["records"]
        command_path = REPO_ROOT / manifest["command_path"]
        command = command_path.read_text(encoding="utf-8").strip()
        captured_at = datetime.fromisoformat(manifest["captured_at"])
        scan = nerva_scan_context(
            command=command,
            scenario_name=manifest.get("scenario_name", manifest["scenario_id"]),
            scenario_id=manifest["scenario_id"],
            target=manifest.get("target"),
            captured_at=captured_at,
            runtime=manifest["runtime"],
            exit_code=int(manifest["exit_code"]),
            duration_s=float(manifest["duration_s"]),
            record_count=len(records),
        )
        bundle = build_nerva_bundle(records, scan)
        structured_path.write_text(dumps_nerva_bundle(bundle), encoding="utf-8")
        print(f"updated {manifest['scenario_id']} -> {structured_path.name}")
        updated += 1
    print(f"done ({updated} bundles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
