#!/usr/bin/env python3
"""Build proposed nugget graphs from subfinder structured JSON bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from graph_builder import GraphBuilder, nugget_node
from subfinder_structured import records_only


def _apex_from_records(records: list[dict[str, Any]], fallback: str) -> str:
    for rec in records:
        inp = rec.get("input")
        if inp:
            return str(inp).lower().rstrip(".")
    return fallback.lower().rstrip(".")


def _host_is_apex(host: str, apex: str) -> bool:
    return host.lower().rstrip(".") == apex.lower().rstrip(".")


def subfinder_to_graph(raw: str, target: str, command: str) -> dict[str, Any]:
    records = records_only(raw)
    apex = _apex_from_records(records, target)
    g = GraphBuilder()

    scan = g.add_node(nugget_node("SCAN_RECORD", apex, description="Subfinder scan"))
    scan_cli = g.add_node(nugget_node("SCAN_CLI", command if command else apex, nugget_type="DESCRIPTOR"))
    g.add_edge(scan["id"], scan_cli["id"], "had")

    domain = g.add_node(nugget_node("DOMAIN_NAME", apex))
    g.add_edge(scan["id"], domain["id"], "contains")

    seen_hosts: set[str] = set()
    for rec in records:
        host = str(rec.get("host", "")).lower().rstrip(".")
        if not host or host in seen_hosts:
            continue
        seen_hosts.add(host)
        if _host_is_apex(host, apex):
            continue

        ip = rec.get("ip")
        mode = rec.get("mode") or rec.get("enumeration_mode") or ("active" if ip else "passive")
        nugget_id = "INTERNET_NAME" if ip or mode == "active" else "INTERNET_NAME_UNRESOLVED"
        host_node = g.add_node(nugget_node(nugget_id, host))
        g.add_edge(scan["id"], host_node["id"], "contains")
        g.add_edge(domain["id"], host_node["id"], "contains")

        sources = rec.get("sources") or []
        if sources:
            src_data = ",".join(sources)
            src_node = g.add_node(
                nugget_node("RAW_DNS_RECORDS", src_data, nugget_type="DESCRIPTOR", description="Passive sources")
            )
            g.add_edge(host_node["id"], src_node["id"], "had")

        if ip:
            ip_node = g.add_node(nugget_node("IP_ADDRESS", str(ip)))
            g.add_edge(host_node["id"], ip_node["id"], "contains")

    return g.build()


def write_graph_artifacts(structured_path: Path, graph_path: Path, scenario_id: str, target: str, command: str) -> None:
    raw = structured_path.read_text(encoding="utf-8", errors="replace")
    graph = subfinder_to_graph(raw, target, command)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
