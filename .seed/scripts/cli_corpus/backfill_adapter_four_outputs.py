#!/usr/bin/env python3
"""Regenerate graph JSON + narrative Markdown from existing examination structured files.

Use when SPEC-004 adapters landed but on-disk corpora predate harvest four-output wiring.
Does not re-run CLI tools; reads manifests + structured artifacts only.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
CORPUS_DIR = Path(__file__).resolve().parent
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"

ADAPTER_TOOLS = frozenset(
    {"netdiscover", "nmap", "nerva", "pius", "subfinder", "httpx", "katana", "nuclei"}
)

_STRUCTURED_EXTS = (".json", ".xml", ".jsonl")


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _resolve_path(manifest: dict[str, Any], key: str, tool_dir: Path, exam_id: int) -> Path | None:
    rel = manifest.get(key)
    if rel:
        candidate = (REPO_ROOT / str(rel).replace("\\", "/")).resolve()
        if candidate.is_file():
            return candidate
    return None


def _structured_path(tool_dir: Path, exam_id: int, manifest: dict[str, Any]) -> Path | None:
    resolved = _resolve_path(manifest, "structured_path", tool_dir, exam_id)
    if resolved:
        return resolved
    for ext in _STRUCTURED_EXTS:
        candidate = tool_dir / f"{exam_id}_output_structured{ext}"
        if candidate.is_file():
            return candidate
    return None


def _text_path(tool_dir: Path, exam_id: int, manifest: dict[str, Any]) -> Path | None:
    resolved = _resolve_path(manifest, "text_path", tool_dir, exam_id)
    if resolved:
        return resolved
    candidate = tool_dir / f"{exam_id}_output_text.txt"
    return candidate if candidate.is_file() else None


def _write_graph_and_markdown(
    tool: str,
    scenario_key: str,
    graph: dict[str, Any],
    markdown: str,
    *,
    dry_run: bool,
) -> tuple[Path, Path]:
    graph_path = NUGGET_ROOT / f"{tool}_{scenario_key}_proposed_nuggets_edges.json"
    markdown_path = NUGGET_ROOT / f"{tool}_{scenario_key}_proposed_nuggets_edges_description.md"
    if not dry_run:
        graph_path.parent.mkdir(parents=True, exist_ok=True)
        graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
        markdown_path.write_text(markdown, encoding="utf-8")
    return graph_path, markdown_path


def _build_from_manifest(tool: str, manifest: dict[str, Any], tool_dir: Path, exam_id: int) -> dict[str, Any] | None:
    adapter = importlib.import_module(f"adapters.{tool}")
    scenario_key = manifest.get("scenario_id") or manifest.get("scenario_key")
    if not scenario_key:
        return None

    structured_path = _structured_path(tool_dir, exam_id, manifest)
    if not structured_path:
        return None

    if tool == "nmap":
        if structured_path.suffix.lower() == ".xml":
            return adapter.build_outputs(
                structured_path.read_text(encoding="utf-8", errors="replace"),
                scenario_key=scenario_key,
            )
        doc = _read_json(structured_path)
        graph = adapter.to_graph(doc)
        return {
            "graph": graph,
            "markdown_report": adapter.to_narrative(graph, scenario_key=scenario_key),
        }

    if tool == "netdiscover":
        text_path = _text_path(tool_dir, exam_id, manifest)
        if not text_path:
            return None
        raw_text = text_path.read_text(encoding="utf-8", errors="replace")
        mode = manifest.get("output_mode") or "parsable"
        return adapter.build_outputs(
            raw_text,
            scenario_name=manifest.get("scenario_name") or scenario_key,
            scenario_key=scenario_key,
            output_mode=mode,
            start_time=None,
            duration_s=manifest.get("duration_s"),
            exit_code=manifest.get("exit_code", 0),
        )

    if structured_path.suffix.lower() == ".xml":
        payload: str | dict[str, Any] = structured_path.read_text(encoding="utf-8", errors="replace")
    else:
        payload = _read_json(structured_path)

    kwargs: dict[str, Any] = {"scenario_key": scenario_key}
    if tool == "pius":
        kwargs["org"] = manifest.get("org")
    if manifest.get("command_path"):
        cmd_path = _resolve_path(manifest, "command_path", tool_dir, exam_id)
        if cmd_path:
            kwargs["command"] = cmd_path.read_text(encoding="utf-8", errors="replace").strip()
    elif (tool_dir / f"{exam_id}_command.txt").is_file():
        kwargs["command"] = (tool_dir / f"{exam_id}_command.txt").read_text(encoding="utf-8").strip()
    if tool in {"subfinder", "httpx", "katana", "nuclei"}:
        kwargs["target"] = manifest.get("target")
    if tool == "nerva" and "command" not in kwargs:
        kwargs["command"] = manifest.get("command") or "nerva"

    return adapter.build_outputs(payload, **kwargs)


def backfill_tool(tool: str, *, dry_run: bool = False, force: bool = False) -> list[str]:
    if tool not in ADAPTER_TOOLS:
        raise SystemExit(f"unsupported tool: {tool}")

    tool_dir = EXAM_ROOT / tool
    if not tool_dir.is_dir():
        raise SystemExit(f"missing examination dir: {tool_dir}")

    written: list[str] = []
    for manifest_path in sorted(tool_dir.glob("*_manifest.json")):
        exam_id = int(manifest_path.name.split("_", 1)[0])
        manifest = _read_json(manifest_path)
        scenario_key = manifest.get("scenario_id") or manifest.get("scenario_key")
        if not scenario_key:
            continue

        graph_path = NUGGET_ROOT / f"{tool}_{scenario_key}_proposed_nuggets_edges.json"
        md_path = NUGGET_ROOT / f"{tool}_{scenario_key}_proposed_nuggets_edges_description.md"
        if not force and graph_path.is_file() and md_path.is_file():
            continue

        try:
            outputs = _build_from_manifest(tool, manifest, tool_dir, exam_id)
        except Exception as exc:  # noqa: BLE001 — batch backfill should continue
            print(f"SKIP {tool}/{scenario_key}: {exc}")
            continue
        if not outputs:
            print(f"SKIP {tool}/{scenario_key}: no structured artifact")
            continue

        g_path, m_path = _write_graph_and_markdown(
            tool,
            scenario_key,
            outputs["graph"],
            outputs["markdown_report"],
            dry_run=dry_run,
        )
        action = "would write" if dry_run else "wrote"
        print(f"{action} {g_path.name} + {m_path.name}")
        written.append(scenario_key)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", action="append", help="Limit to one or more tools (repeatable)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing graph+markdown pairs")
    args = parser.parse_args()

    tools = args.tool or sorted(ADAPTER_TOOLS)
    total = 0
    for tool in tools:
        keys = backfill_tool(tool, dry_run=args.dry_run, force=args.force)
        total += len(keys)
        print(f"{tool}: {len(keys)} scenario(s)")
    print(f"done — {total} scenario(s) {'planned' if args.dry_run else 'updated'}")


if __name__ == "__main__":
    main()
