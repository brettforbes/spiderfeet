#!/usr/bin/env python3
"""Generate proposed nugget graph JSON from CLI examination structured output."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
TEMPLATE = REPO_ROOT / ".seed" / "scripts" / "cli_corpus" / "templates" / "netdiscover_parsable.textfsm"


def _uid(nugget_id: str, data: str) -> str:
    return f"{nugget_id}--{uuid.uuid5(uuid.NAMESPACE_DNS, f'{nugget_id}:{data}')}"


def _node(nugget_id: str, nugget_type: str, data: str, description: str) -> Dict[str, Any]:
    iid = _uid(nugget_id, data)
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


def parse_netdiscover_p(raw: str) -> List[Dict[str, str]]:
    try:
        import textfsm
    except ImportError:
        rows: List[Dict[str, str]] = []
        for line in raw.splitlines():
            m = re.match(
                r"^(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:]{17})\s+(\d+)\s+(\d+)\s+(.+)$",
                line.strip(),
            )
            if m:
                rows.append(
                    {
                        "IP": m.group(1),
                        "MAC": m.group(2),
                        "COUNT": m.group(3),
                        "LEN": m.group(4),
                        "VENDOR": m.group(5).strip(),
                    }
                )
        return rows
    with TEMPLATE.open(encoding="utf-8") as fh:
        fsm = textfsm.TextFSM(fh)
    return fsm.ParseTextToDicts(raw)


def netdiscover_to_graph(raw: str, target: str, command: str) -> Dict[str, Any]:
    scan = _node("SCAN_RECORD", "ENTITY", command, "Scan Record")
    scan_cli = _node("SCAN_CLI", "DESCRIPTOR", command, "Scan CLI")
    scan_target = _node("SCAN_TARGET", "DESCRIPTOR", target, "Scan Target")
    nodes = [scan, scan_cli, scan_target]
    edges = [
        _edge(scan["id"], scan_cli["id"], "had"),
        _edge(scan["id"], scan_target["id"], "had"),
    ]
    for row in parse_netdiscover_p(raw):
        ip = row["IP"]
        mac = row["MAC"].lower()
        vendor = row.get("VENDOR", "").strip()
        host = _node("HOST", "ENTITY", ip, "Host")
        ip_n = _node("IP_ADDRESS", "ENTITY", ip, "IP Address")
        mac_n = _node("MAC_ADDRESS", "ENTITY", mac, "MAC Address")
        nodes.extend([host, ip_n, mac_n])
        edges.extend(
            [
                _edge(scan["id"], host["id"], "contains"),
                _edge(host["id"], ip_n["id"], "contains"),
                _edge(host["id"], mac_n["id"], "had"),
            ]
        )
        if vendor and vendor.lower() != "unknown vendor":
            vend = _node("RAW_RIR_DATA", "DESCRIPTOR", vendor, "Vendor")
            nodes.append(vend)
            edges.append(_edge(mac_n["id"], vend["id"], "had"))
    return {"nodes": nodes, "edges": edges}


def parse_nerva_jsonl(raw: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def nerva_to_graph(raw: str, target: str, command: str) -> Dict[str, Any]:
    scan = _node("SCAN_RECORD", "ENTITY", command, "Scan Record")
    scan_cli = _node("SCAN_CLI", "DESCRIPTOR", command, "Scan CLI")
    nodes = [scan, scan_cli]
    edges = [_edge(scan["id"], scan_cli["id"], "had")]
    for rec in parse_nerva_jsonl(raw):
        ip = rec.get("ip") or rec.get("host", "")
        port = rec["port"]
        protocol = rec.get("protocol", "unknown")
        transport = rec.get("transport", "tcp")
        port_data = f"{ip}:{port}"
        host = _node("HOST", "ENTITY", ip, "Host")
        port_n = _node("PORT", "ENTITY", str(port), "Port")
        proto = _node("PORT_PROTOCOL", "DESCRIPTOR", transport, "Port Protocol")
        svc = _node("SERVICE", "ENTITY", protocol, "Service")
        nodes.extend([host, port_n, proto, svc])
        edges.extend(
            [
                _edge(scan["id"], host["id"], "contains"),
                _edge(host["id"], port_n["id"], "contains"),
                _edge(port_n["id"], proto["id"], "had"),
                _edge(port_n["id"], svc["id"], "listens-to"),
            ]
        )
        version = rec.get("version")
        if version:
            ver = _node("SERVICE_VERSION", "DESCRIPTOR", version, "Service Version")
            nodes.append(ver)
            edges.append(_edge(svc["id"], ver["id"], "had"))
    return {"nodes": nodes, "edges": edges}


def parse_pius_ndjson(raw: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


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


def latest_exam_for_scenario(tool: str, scenario_key: str) -> Optional[Tuple[int, Path, Path]]:
    tool_dir = EXAM_ROOT / tool
    best: Optional[Tuple[int, Path, Path, Path]] = None
    for manifest_path in tool_dir.glob("*_manifest.json"):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        sid = manifest.get("scenario_id", "")
        key = sid.replace("_text", "").replace("_jsonl", "")
        if key != scenario_key and not sid.startswith(scenario_key):
            continue
        exam_id = int(manifest_path.name.split("_", 1)[0])
        struct_ext = manifest.get("structured_kind")
        for ext in ("jsonl", "json", "xml", "txt"):
            sp = tool_dir / f"{exam_id}_output_structured.{ext}"
            if sp.is_file():
                if best is None or exam_id > best[0]:
                    best = (exam_id, sp, tool_dir / f"{exam_id}_command.txt", manifest)
                break
    if not best:
        return None
    return best[0], best[1], best[2]


def generate_tool_graphs(tool: str, scenario_keys: List[str]) -> None:
    generators = {
        "netdiscover": ("local_subnet_active_parsable", netdiscover_to_graph),
        "nerva": ("tcp_scanme_http_json", nerva_to_graph),
        "pius": ("passive_bbc_corporate_ndjson", pius_to_graph),
    }
    if tool not in generators:
        raise SystemExit(f"Unsupported tool: {tool}")
    default_key, fn = generators[tool]
    keys = scenario_keys or [default_key]
    for key in keys:
        found = latest_exam_for_scenario(tool, key)
        if not found:
            print(f"skip {key}: no structured output", file=sys.stderr)
            continue
        _exam_id, struct_path, cmd_path = found
        raw = struct_path.read_text(encoding="utf-8", errors="replace")
        command = cmd_path.read_text(encoding="utf-8").strip() if cmd_path.is_file() else key
        target = key
        if tool == "pius":
            graph = fn(raw, "British Broadcasting Corporation", command)
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
    if args.all_defaults or not keys:
        generate_tool_graphs(args.tool, keys)
    else:
        generate_tool_graphs(args.tool, keys)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
