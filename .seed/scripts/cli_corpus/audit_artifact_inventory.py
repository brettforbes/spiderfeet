#!/usr/bin/env python3
"""Audit CLI corpus examination artifacts for SPEC-005 G0 inventory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"

ADAPTER_TOOLS = (
    "netdiscover",
    "nmap",
    "nerva",
    "pius",
    "subfinder",
    "httpx",
    "katana",
    "nuclei",
)

_SUFFIXES = ("_text", "_jsonl", "_json", "_xml", "_yaml", "_yml", "_csv")


def scenario_key_from_id(scenario_id: str) -> str:
    for suffix in _SUFFIXES:
        if scenario_id.endswith(suffix):
            return scenario_id[: -len(suffix)]
    return scenario_id


def _resolve_graph(tool: str, scenario_key: str, scenario_id: str) -> tuple[Path | None, list[str]]:
    tried: list[str] = []
    for sid in (scenario_id, scenario_key):
        path = NUGGET_ROOT / f"{tool}_{sid}_proposed_nuggets_edges.json"
        tried.append(str(path.relative_to(REPO_ROOT)).replace("\\", "/"))
        if path.is_file():
            return path, tried
    return None, tried


def _resolve_markdown(tool: str, scenario_key: str, scenario_id: str) -> tuple[Path | None, list[str]]:
    tried: list[str] = []
    for sid in (scenario_id, scenario_key):
        path = NUGGET_ROOT / f"{tool}_{sid}_proposed_nuggets_edges_description.md"
        tried.append(str(path.relative_to(REPO_ROOT)).replace("\\", "/"))
        if path.is_file():
            return path, tried
    return None, tried


def _has_structured(tool_dir: Path, exam_id: int, manifest: dict) -> bool:
    rel = manifest.get("structured_path")
    if rel:
        p = (REPO_ROOT / str(rel).replace("\\", "/")).resolve()
        if p.is_file():
            return True
    for ext in (".json", ".xml", ".jsonl"):
        if (tool_dir / f"{exam_id}_output_structured{ext}").is_file():
            return True
    return False


def _has_text(tool_dir: Path, exam_id: int, manifest: dict) -> bool:
    rel = manifest.get("text_path")
    if rel:
        p = (REPO_ROOT / str(rel).replace("\\", "/")).resolve()
        if p.is_file():
            return True
    return (tool_dir / f"{exam_id}_output_text.txt").is_file()


def audit_tool(tool: str) -> list[dict]:
    tool_dir = EXAM_ROOT / tool
    if not tool_dir.is_dir():
        return []
    rows: list[dict] = []
    for manifest_path in sorted(tool_dir.glob("*_manifest.json")):
        exam_id = int(manifest_path.name.split("_", 1)[0])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        scenario_id = manifest.get("scenario_id") or f"exam_{exam_id}"
        scenario_key = scenario_key_from_id(scenario_id)
        has_structured = _has_structured(tool_dir, exam_id, manifest)
        has_text = _has_text(tool_dir, exam_id, manifest)
        graph_path, graph_tried = _resolve_graph(tool, scenario_key, scenario_id)
        md_path, md_tried = _resolve_markdown(tool, scenario_key, scenario_id)
        deferred = bool(manifest.get("graph_deferred"))
        if not graph_path or not md_path:
            if has_structured:
                classification = "missing-both" if not graph_path and not md_path else (
                    "missing-markdown" if graph_path and not md_path else "missing-graph"
                )
            elif has_text:
                classification = "missing-both"
            else:
                classification = "partial"
        elif graph_path and md_path:
            classification = "ok"
        else:
            classification = "partial"
        rows.append(
            {
                "tool": tool,
                "exam_id": exam_id,
                "scenario_id": scenario_id,
                "scenario_key": scenario_key,
                "has_structured": has_structured,
                "has_text": has_text,
                "has_graph": graph_path is not None,
                "has_markdown": md_path is not None,
                "graph_deferred": deferred,
                "classification": classification,
                "graph_resolved": str(graph_path.relative_to(REPO_ROOT)).replace("\\", "/")
                if graph_path
                else "",
                "markdown_resolved": str(md_path.relative_to(REPO_ROOT)).replace("\\", "/")
                if md_path
                else "",
            }
        )
    return rows


def main() -> None:
    all_rows: list[dict] = []
    for tool in ADAPTER_TOOLS:
        all_rows.extend(audit_tool(tool))
    out = REPO_ROOT / ".governance" / "project" / "SPEC005_ARTIFACT_INVENTORY.json"
    out.write_text(json.dumps(all_rows, indent=2) + "\n", encoding="utf-8")
    counts: dict[str, int] = {}
    for row in all_rows:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    print(f"Wrote {len(all_rows)} rows to {out}")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
