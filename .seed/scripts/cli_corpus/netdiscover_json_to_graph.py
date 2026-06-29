#!/usr/bin/env python3
"""Convert approved netdiscover_scan JSON into SpiderFeet nugget graph JSON.

Input schema: ``.seed/06A_Updates_to_NetDiscover_Cli_App_Profiling copy.md``
Graph contract: provisional ``SYSTEM`` nuggets with ``NETWORKS`` / ``MAC_VENDOR``.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]


def _uid(nugget_id: str, data: str) -> str:
    return f"{nugget_id}--{uuid.uuid5(uuid.NAMESPACE_DNS, f'{nugget_id}:{data}')}"


def _node(nugget_id: str, nugget_type: str, data: str, description: str) -> dict[str, Any]:
    iid = _uid(nugget_id, data)
    return {
        "id": iid,
        "nugget_instance_id": iid,
        "nugget_id": nugget_id,
        "nugget_type": nugget_type,
        "nugget_description": description,
        "nugget_data": data,
    }


def _edge(source: str, target: str, relation: str) -> dict[str, str]:
    return {"source": source, "target": target, "relation": relation}


def netdiscover_scan_to_graph(doc: dict[str, Any]) -> dict[str, Any]:
    """Build nodes/edges from a validated netdiscover_scan document."""
    scan_data = doc.get("netdiscover_scan")
    if not isinstance(scan_data, dict):
        raise ValueError("missing netdiscover_scan root object")

    args_label = scan_data.get("args", "netdiscover scan")
    start_time = scan_data.get("start_time", "")
    systems = scan_data.get("systems") or []
    runstats = scan_data.get("runstats", {})
    finished = runstats.get("finished_time", {})
    systems_stats = runstats.get("systems", {})

    scan = _node("SCAN_RECORD", "ENTITY", args_label, "Scan Record")
    scan_args = _node("SCAN_ARGS", "DESCRIPTOR", args_label, "Scan Args")
    nodes: list[dict[str, Any]] = [scan, scan_args]
    edges: list[dict[str, str]] = [_edge(scan["id"], scan_args["id"], "had")]

    if start_time:
        ts = _node("SCAN_TIMESTAMP", "DESCRIPTOR", start_time, "Scan Start Time")
        nodes.append(ts)
        edges.append(_edge(scan["id"], ts["id"], "had"))

    end_time = finished.get("end_time")
    if end_time:
        end_node = _node("SCAN_END_TIME", "DESCRIPTOR", end_time, "Scan End Time")
        nodes.append(end_node)
        edges.append(_edge(scan["id"], end_node["id"], "had"))

    summary = finished.get("summary")
    if summary:
        summary_node = _node("SCAN_SUMMARY", "DESCRIPTOR", summary, "Scan Summary")
        nodes.append(summary_node)
        edges.append(_edge(scan["id"], summary_node["id"], "had"))

    exit_status = finished.get("exit_status")
    if exit_status:
        status_node = _node("SCAN_EXIT_STATUS", "DESCRIPTOR", exit_status, "Scan Exit Status")
        nodes.append(status_node)
        edges.append(_edge(scan["id"], status_node["id"], "had"))

    scan_tries = systems_stats.get("scan_tries")
    if scan_tries is not None:
        tries_node = _node("SCAN_TRIES", "DESCRIPTOR", str(scan_tries), "Scan Tries")
        nodes.append(tries_node)
        edges.append(_edge(scan["id"], tries_node["id"], "had"))

    empty_scans = systems_stats.get("empty_scans")
    if empty_scans is not None:
        empty_node = _node("SCAN_EMPTY_SCANS", "DESCRIPTOR", str(empty_scans), "Empty Scans")
        nodes.append(empty_node)
        edges.append(_edge(scan["id"], empty_node["id"], "had"))

    discovered = systems_stats.get("discovered")
    if discovered is not None:
        discovered_node = _node("SCAN_DISCOVERED", "DESCRIPTOR", str(discovered), "Systems Discovered")
        nodes.append(discovered_node)
        edges.append(_edge(scan["id"], discovered_node["id"], "had"))

    for system in systems:
        ipv4 = system.get("ipv4", "")
        mac = str(system.get("mac", "")).lower()
        vendor = str(system.get("mac_vendor", "")).strip()
        if not ipv4:
            continue

        system_n = _node("SYSTEM", "ENTITY", ipv4, "System")
        networks = _node("NETWORKS", "ENTITY", f"networks:{ipv4}", "Networks")
        ip_n = _node("IP_ADDRESS", "ENTITY", ipv4, "IP Address")
        nodes.extend([system_n, networks, ip_n])
        edges.extend(
            [
                _edge(scan["id"], system_n["id"], "contains"),
                _edge(system_n["id"], networks["id"], "contains"),
                _edge(networks["id"], ip_n["id"], "contains"),
            ]
        )

        if mac:
            mac_n = _node("MAC_ADDRESS", "ENTITY", mac, "MAC Address")
            nodes.append(mac_n)
            edges.append(_edge(networks["id"], mac_n["id"], "contains"))
            if vendor:
                vend = _node("MAC_VENDOR", "DESCRIPTOR", vendor, "MAC Vendor")
                nodes.append(vend)
                edges.append(_edge(mac_n["id"], vend["id"], "had"))

    return {"nodes": nodes, "edges": edges}


def graph_from_json_text(raw: str) -> dict[str, Any]:
    doc = json.loads(raw)
    return netdiscover_scan_to_graph(doc)


def graph_from_json_file(path: Path) -> dict[str, Any]:
    return graph_from_json_text(path.read_text(encoding="utf-8"))


def write_graph_file(json_path: Path, graph_path: Path) -> dict[str, Any]:
    graph = graph_from_json_file(json_path)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    return graph
