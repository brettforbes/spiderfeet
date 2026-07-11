#!/usr/bin/env python3
"""Generate proposed nugget graph JSON from CLI examination structured output."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
CORPUS_DIR = Path(__file__).resolve().parent
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"

from netdiscover_json_to_graph import graph_from_json_text, netdiscover_scan_to_graph
from nerva_structured import records_only as nerva_records_only
from pius_structured import records_only as pius_records_only
from graph_builder import nugget_instance_id


def _node(nugget_id: str, nugget_type: str, data: str, description: str) -> Dict[str, Any]:
    iid = nugget_instance_id(nugget_id, data)
    return {
        "id": iid,
        "nugget_instance_id": iid,
        "nugget_id": nugget_id,
        "nugget_type": nugget_type,
        "nugget_description": description,
        "nugget_data": data,
    }


def _edge(source: str, target: str, relation: str) -> Dict[str, str]:
    return {"source": source, "target": target, "relation": relation}


def netdiscover_to_graph(raw: str, target: str, command: str) -> Dict[str, Any]:
    """Build nugget graph from approved netdiscover_scan JSON only."""
    del target, command
    if not raw.lstrip().startswith("{"):
        raise ValueError(
            "netdiscover structured artifact must be netdiscover_scan JSON, not raw CLI text"
        )
    return graph_from_json_text(raw)


def parse_nerva_jsonl(raw: str) -> List[Dict[str, Any]]:
    return nerva_records_only(raw)


def nerva_to_graph(raw: str, target: str, command: str) -> Dict[str, Any]:
    """Delegate to SPEC-004 Nerva adapter (07B + correlation_engine)."""
    from adapters import nerva as nerva_adapter

    del target
    return nerva_adapter.to_graph(nerva_adapter.to_structured(raw, command=command))


def parse_pius_ndjson(raw: str) -> List[Dict[str, Any]]:
    return pius_records_only(raw)


def pius_to_graph(raw: str, org: str, command: str) -> Dict[str, Any]:
    scan = _node("SCAN_RECORD", "ENTITY", org, "Scan Record")
    scan_cli = _node("SCAN_CLI", "DESCRIPTOR", command, "Scan CLI")
    org_n = _node("COMPANY_NAME", "DESCRIPTOR", org, "Organization")
    nodes = [scan, scan_cli, org_n]
    edges = [_edge(scan["id"], scan_cli["id"], "had"), _edge(scan["id"], org_n["id"], "had")]
    for finding in parse_pius_ndjson(raw):
        ftype = finding.get("Type", "")
        value = str(finding.get("Value", "")).strip()
        if not value or ftype in ("preseed",):
            continue
        if ftype == "domain" and " " not in value and "." in value:
            dom = _node("INTERNET_NAME", "ENTITY", value.lower(), "Internet Name")
            src = _node("PIUS_SOURCE", "DESCRIPTOR", finding.get("Source", ""), "PIUS Source")
            nodes.extend([dom, src])
            edges.extend([_edge(scan["id"], dom["id"], "contains"), _edge(dom["id"], src["id"], "had")])
        elif ftype == "cidr" and "/" in value:
            nb = _node("NETBLOCK_OWNER", "ENTITY", value, "Netblock Owner")
            src = _node("PIUS_SOURCE", "DESCRIPTOR", finding.get("Source", ""), "PIUS Source")
            nodes.extend([nb, src])
            edges.extend([_edge(scan["id"], nb["id"], "contains"), _edge(nb["id"], src["id"], "had")])
    return {"nodes": nodes, "edges": edges}


def latest_exam_for_scenario(tool: str, scenario_key: str) -> Optional[Tuple[int, Path, Path, Dict[str, Any]]]:
    tool_dir = EXAM_ROOT / tool
    best: Optional[Tuple[int, Path, Path, Dict[str, Any]]] = None
    for manifest_path in tool_dir.glob("*_manifest.json"):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        sid = manifest.get("scenario_id", "")
        key = sid.replace("_text", "").replace("_jsonl", "")
        if key != scenario_key and not sid.startswith(scenario_key):
            continue
        exam_id = int(manifest_path.name.split("_", 1)[0])
        for ext in ("jsonl", "json", "xml", "txt"):
            sp = tool_dir / f"{exam_id}_output_structured.{ext}"
            if sp.is_file():
                if best is None or exam_id > best[0]:
                    best = (exam_id, sp, tool_dir / f"{exam_id}_command.txt", manifest)
                break
    if not best:
        return None
    return best[0], best[1], best[2], best[3]


def generate_tool_graphs(tool: str, scenario_keys: List[str]) -> None:
    generators = {
        "netdiscover": netdiscover_to_graph,
        "nerva": nerva_to_graph,
        "pius": pius_to_graph,
    }
    default_keys = {
        "netdiscover": [
            "local_subnet_active_parsable",
            "local_subnet_active_text",
            "local_subnet_fast_parsable",
            "passive_snippet_text",
            "sparse_subnet_parsable",
        ],
        "nerva": [
            "tcp_http_rich_json",
            "tcp_ssh_misconfigs_json",
            "tcp_https_praetorian_json",
            "tcp_list_file_json",
            "tcp_fast_praetorian_json",
            "tcp_closed_clean_miss",
        ],
        "pius": [
            "crt_praetorian_ndjson",
            "crt_linode_ndjson",
            "corporate_bbc_gleif_ndjson",
            "rir_cidr_ndjson",
            "sparse_scanme_ndjson",
        ],
    }
    if tool not in generators:
        raise SystemExit(f"Unsupported tool: {tool}")
    fn = generators[tool]
    keys = scenario_keys or default_keys[tool]
    for key in keys:
        found = latest_exam_for_scenario(tool, key)
        if not found:
            print(f"skip {key}: no structured output", file=sys.stderr)
            continue
        _exam_id, struct_path, cmd_path, manifest = found
        raw = struct_path.read_text(encoding="utf-8", errors="replace")
        command = cmd_path.read_text(encoding="utf-8").strip() if cmd_path.is_file() else key
        target = manifest.get("target") or key
        if tool == "pius":
            org = manifest.get("org") or target
            graph = fn(raw, org, command)
        else:
            graph = fn(raw, target, command)
        out = NUGGET_ROOT / f"{tool}_{key}_proposed_nuggets_edges.json"
        out.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
        print(f"{key}: {len(graph['nodes'])} nodes -> {out.relative_to(REPO_ROOT)}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, choices=["netdiscover", "nerva", "pius"])
    parser.add_argument("--scenario", action="append", dest="scenarios")
    parser.add_argument("--all-defaults", action="store_true")
    args = parser.parse_args(argv)
    keys = args.scenarios or []
    generate_tool_graphs(args.tool, keys)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
