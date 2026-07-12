#!/usr/bin/env python3
"""Convert approved netdiscover_scan JSON into SpiderFeet nugget graph JSON.

Input schema: ``.seed/06A_Updates_to_NetDiscover_Cli_App_Profiling copy.md``
Graph contract: provisional ``SYSTEM`` nuggets with ``NETWORKS`` / ``MAC_VENDOR``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from graph_builder import GraphBuilder, nugget_node, validate_graph
from core.ip_classify import ip_nugget_node

REPO_ROOT = Path(__file__).resolve().parents[3]


def describe_graph(graph: dict[str, Any], scenario_key: str) -> str:
    from narrative_report import build_netdiscover_narrative_report

    return build_netdiscover_narrative_report(graph, scenario_key)


def description_path_for(graph_path: Path) -> Path:
    return graph_path.with_name(
        graph_path.name.replace(
            "_proposed_nuggets_edges.json", "_proposed_nuggets_edges_description.md"
        )
    )


def write_graph_artifacts(
    json_path: Path, graph_path: Path, scenario_key: str
) -> dict[str, Any]:
    graph = graph_from_json_file(json_path)
    validate_graph(graph)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    description_path_for(graph_path).write_text(
        describe_graph(graph, scenario_key), encoding="utf-8"
    )
    return graph


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

    builder = GraphBuilder()

    scan = builder.add_node(nugget_node("SCAN_RECORD", args_label))
    scan_args = builder.add_node(nugget_node("SCAN_ARGS", args_label, nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], scan_args["id"], "had")

    if start_time:
        ts = builder.add_node(
            nugget_node("SCAN_TIMESTAMP", start_time, nugget_type="DESCRIPTOR", description="Scan Start Time")
        )
        builder.add_edge(scan["id"], ts["id"], "had")

    end_time = finished.get("end_time")
    if end_time:
        end_node = builder.add_node(
            nugget_node("SCAN_END_TIME", end_time, nugget_type="DESCRIPTOR", description="Scan End Time")
        )
        builder.add_edge(scan["id"], end_node["id"], "had")

    summary = finished.get("summary")
    if summary:
        summary_node = builder.add_node(nugget_node("SCAN_SUMMARY", summary, nugget_type="DESCRIPTOR"))
        builder.add_edge(scan["id"], summary_node["id"], "had")

    exit_status = scan_data.get("exit_status") or finished.get("exit_status")
    if exit_status:
        status_node = builder.add_node(
            nugget_node("SCAN_EXIT_STATUS", exit_status, nugget_type="DESCRIPTOR", description="Scan Exit Status")
        )
        builder.add_edge(scan["id"], status_node["id"], "had")

    scan_tries = systems_stats.get("scan_tries")
    if scan_tries is not None:
        tries_node = builder.add_node(
            nugget_node("SCAN_TRIES", str(scan_tries), nugget_type="DESCRIPTOR", description="Scan Tries")
        )
        builder.add_edge(scan["id"], tries_node["id"], "had")

    empty_scans = systems_stats.get("empty_scans")
    if empty_scans is not None:
        empty_node = builder.add_node(
            nugget_node("SCAN_EMPTY_SCANS", str(empty_scans), nugget_type="DESCRIPTOR", description="Empty Scans")
        )
        builder.add_edge(scan["id"], empty_node["id"], "had")

    discovered = systems_stats.get("discovered")
    if discovered is not None:
        discovered_node = builder.add_node(
            nugget_node("SCAN_DISCOVERED", str(discovered), nugget_type="DESCRIPTOR", description="Systems Discovered")
        )
        builder.add_edge(scan["id"], discovered_node["id"], "had")

    for system in systems:
        ipv4 = system.get("ipv4", "")
        mac = str(system.get("mac", "")).lower()
        vendor = str(system.get("mac_vendor", "")).strip() or "Unknown"
        if not ipv4:
            continue

        system_n = builder.add_node(nugget_node("SYSTEM", ipv4, description="System"))
        networks = builder.add_node(nugget_node("NETWORKS", f"networks:{ipv4}"))
        ip_n = builder.add_node(ip_nugget_node(ipv4, description="IP Address"))
        builder.add_edge(scan["id"], system_n["id"], "contains")
        builder.add_edge(system_n["id"], networks["id"], "contains")
        builder.add_edge(networks["id"], ip_n["id"], "contains")

        if mac:
            mac_n = builder.add_node(nugget_node("MAC_ADDRESS", mac, description="MAC Address"))
            builder.add_edge(networks["id"], mac_n["id"], "contains")
            vend = builder.add_node(
                nugget_node("MAC_VENDOR", vendor, nugget_type="DESCRIPTOR", description="MAC Vendor")
            )
            builder.add_edge(mac_n["id"], vend["id"], "had")

    return builder.build()


def graph_from_json_text(raw: str) -> dict[str, Any]:
    doc = json.loads(raw)
    return netdiscover_scan_to_graph(doc)


def graph_from_json_file(path: Path) -> dict[str, Any]:
    return graph_from_json_text(path.read_text(encoding="utf-8"))


def write_graph_file(json_path: Path, graph_path: Path) -> dict[str, Any]:
    graph = graph_from_json_file(json_path)
    validate_graph(graph)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    return graph
