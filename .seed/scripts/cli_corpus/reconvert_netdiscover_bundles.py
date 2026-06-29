#!/usr/bin/env python3
"""Reconvert NetDiscover examination text bundles to approved JSON + graph artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

from netdiscover_json_to_graph import write_graph_file
from netdiscover_text_to_json import (
    convert_text_to_netdiscover_scan,
    dumps_netdiscover_scan,
    output_mode_for_scenario,
    strip_capture_header,
    validate_netdiscover_scan,
)

REPO_ROOT = CORPUS_DIR.parents[2]
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs" / "netdiscover"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
MANIFEST_PATH = CORPUS_DIR / "manifests" / "netdiscover.yaml"


def load_scenarios() -> dict[str, dict]:
    import yaml

    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {s["id"]: s for s in manifest.get("scenarios", [])}


def reconvert_exam(exam_id: int, scenarios: dict[str, dict], write_graph: bool) -> None:
    manifest_path = EXAM_ROOT / f"{exam_id}_manifest.json"
    if not manifest_path.is_file():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    scenario_id = manifest["scenario_id"]
    scenario = scenarios[scenario_id]
    text_path = EXAM_ROOT / f"{exam_id}_output_text.txt"
    json_path = EXAM_ROOT / f"{exam_id}_output_structured.json"
    command_path = EXAM_ROOT / f"{exam_id}_command.txt"

    raw = text_path.read_text(encoding="utf-8", errors="replace")
    body = strip_capture_header(raw)
    command = command_path.read_text(encoding="utf-8").strip() if command_path.is_file() else ""
    captured_at = datetime.fromisoformat(manifest["captured_at"])
    duration_s = float(manifest.get("duration_s", 0.0))
    start_time = captured_at - timedelta(seconds=duration_s)

    doc = convert_text_to_netdiscover_scan(
        body,
        scenario_name=scenario.get("name", scenario_id),
        output_mode=output_mode_for_scenario(scenario, command),
        start_time=start_time,
        duration_s=duration_s,
        exit_code=int(manifest.get("exit_code", 0)),
    )
    errors = validate_netdiscover_scan(doc)
    if errors:
        raise SystemExit(f"exam {exam_id} validation failed: {errors}")

    json_path.write_text(dumps_netdiscover_scan(doc), encoding="utf-8")
    manifest["structured_kind"] = "json"
    manifest["structured_path"] = str(json_path.relative_to(REPO_ROOT))
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if write_graph:
        graph_path = NUGGET_ROOT / f"netdiscover_{scenario_id}_proposed_nuggets_edges.json"
        write_graph_file(json_path, graph_path)

    print(f"exam {exam_id} ({scenario_id}) -> {json_path.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exam", type=int, action="append", dest="exams")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--graph", action="store_true", help="Also refresh proposed nugget graphs")
    args = parser.parse_args()

    scenarios = load_scenarios()
    if args.all:
        exam_ids = sorted(
            int(p.name.split("_", 1)[0])
            for p in EXAM_ROOT.glob("*_manifest.json")
        )
    elif args.exams:
        exam_ids = args.exams
    else:
        raise SystemExit("Specify --all or --exam <id>")

    for exam_id in exam_ids:
        reconvert_exam(exam_id, scenarios, write_graph=args.graph)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
