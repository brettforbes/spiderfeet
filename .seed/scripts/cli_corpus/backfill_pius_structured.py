#!/usr/bin/env python3
"""Backfill pius NDJSON examination bundles to structured JSON + derived text."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

CORPUS_DIR = Path(__file__).resolve().parent
REPO_ROOT = CORPUS_DIR.parents[2]
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

from cli_tool_to_graph import pius_to_graph
from pius_structured import (
    build_pius_bundle,
    dumps_pius_bundle,
    parse_pius_structured,
    pius_scan_context,
    pius_text_capture_header,
    structured_to_text,
)

EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs" / "pius"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
MANIFEST_YAML = CORPUS_DIR / "manifests" / "pius.yaml"


def _scenario_org(scenario_id: str) -> str | None:
    if not MANIFEST_YAML.is_file():
        return None
    data = yaml.safe_load(MANIFEST_YAML.read_text(encoding="utf-8"))
    for scenario in data.get("scenarios", []):
        if scenario.get("id") == scenario_id:
            return scenario.get("org")
    return None


def _structured_source(exam_id: int, manifest: dict) -> Path | None:
    rel = manifest.get("structured_path")
    if rel:
        path = REPO_ROOT / rel
        if path.is_file():
            return path
    for ext in (".jsonl", ".json"):
        candidate = EXAM_ROOT / f"{exam_id}_output_structured{ext}"
        if candidate.is_file():
            return candidate
    return None


def main() -> int:
    updated = 0
    for manifest_path in sorted(EXAM_ROOT.glob("*_manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not manifest.get("scenario_id", "").endswith("_ndjson"):
            continue
        exam_id = int(manifest_path.name.split("_", 1)[0])
        structured_path = _structured_source(exam_id, manifest)
        if structured_path is None:
            print(f"skip {manifest['scenario_id']}: no structured file", file=sys.stderr)
            continue

        raw = structured_path.read_text(encoding="utf-8", errors="replace")
        records = parse_pius_structured(raw)["records"]
        command_path = REPO_ROOT / manifest["command_path"]
        command = command_path.read_text(encoding="utf-8").strip()
        captured_at = datetime.fromisoformat(manifest["captured_at"])

        stderr_banner = None
        text_path = REPO_ROOT / manifest["text_path"]
        if text_path.is_file():
            old_text = text_path.read_text(encoding="utf-8", errors="replace").strip()
            if old_text and not old_text.startswith("#") and not old_text.startswith("["):
                stderr_banner = old_text

        org = manifest.get("org") or _scenario_org(manifest["scenario_id"])
        scan = pius_scan_context(
            command=command,
            scenario_name=manifest.get("scenario_name", manifest["scenario_id"]),
            scenario_id=manifest["scenario_id"],
            org=org,
            target=manifest.get("target"),
            captured_at=captured_at,
            runtime=manifest["runtime"],
            exit_code=int(manifest["exit_code"]),
            duration_s=float(manifest["duration_s"]),
            record_count=len(records),
            stderr_banner=stderr_banner,
        )
        bundle = build_pius_bundle(records, scan)
        json_path = EXAM_ROOT / f"{exam_id}_output_structured.json"
        json_path.write_text(dumps_pius_bundle(bundle), encoding="utf-8")
        if structured_path != json_path and structured_path.suffix == ".jsonl":
            structured_path.unlink()

        text_body = structured_to_text(records)
        header = pius_text_capture_header(
            command=command,
            scenario_name=manifest.get("scenario_name", manifest["scenario_id"]),
            scenario_id=manifest["scenario_id"],
            org=org,
            target=manifest.get("target"),
            captured_at=captured_at,
            runtime=manifest["runtime"],
            exit_code=int(manifest["exit_code"]),
            duration_s=float(manifest["duration_s"]),
            record_count=len(records),
        )
        text_path.write_text(header + text_body, encoding="utf-8")

        org = manifest.get("org") or _scenario_org(manifest["scenario_id"])
        graph = pius_to_graph(json_path.read_text(encoding="utf-8"), org or manifest.get("target") or manifest["scenario_id"], command)
        graph_path = NUGGET_ROOT / f"pius_{manifest['scenario_id']}_proposed_nuggets_edges.json"
        graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")

        manifest["structured_kind"] = "json"
        manifest["structured_path"] = str(json_path.relative_to(REPO_ROOT))
        if org:
            manifest["org"] = org
        manifest["tool_manifest_version"] = 3
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        print(f"updated {manifest['scenario_id']}: {len(records)} records -> {json_path.name}")
        updated += 1

    print(f"done ({updated} bundles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
