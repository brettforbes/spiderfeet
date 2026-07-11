#!/usr/bin/env python3
"""Build proposed nugget graphs from katana structured JSON bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from graph_builder import GraphBuilder, nugget_node
from katana_structured import _host_from_record, records_only


def _url_from_record(rec: dict[str, Any]) -> str:
    return str(rec.get("url") or rec.get("request", {}).get("endpoint") or "").strip()


def katana_to_graph(raw: str, target: str, command: str) -> dict[str, Any]:
    records = records_only(raw)
    g = GraphBuilder()
    apex = target.lower().rstrip(".")

    scan = g.add_node(nugget_node("SCAN_RECORD", apex, description="Katana crawl scan"))
    scan_cli = g.add_node(nugget_node("SCAN_CLI", command if command else apex, nugget_type="DESCRIPTOR"))
    g.add_edge(scan["id"], scan_cli["id"], "had")

    domain = g.add_node(nugget_node("DOMAIN_NAME", apex))
    g.add_edge(scan["id"], domain["id"], "contains")

    seen_urls: set[str] = set()
    seen_hosts: set[str] = set()

    for rec in records:
        url = _url_from_record(rec)
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        url_node = g.add_node(nugget_node("LINKED_URL_INTERNAL", url))
        g.add_edge(scan["id"], url_node["id"], "contains")

        host = _host_from_record(rec)
        if host:
            if host not in seen_hosts:
                seen_hosts.add(host)
                host_node = g.add_node(nugget_node("INTERNET_NAME", host))
                g.add_edge(domain["id"], host_node["id"], "contains")
            else:
                host_node = g.add_node(nugget_node("INTERNET_NAME", host))
            g.add_edge(host_node["id"], url_node["id"], "contains")

        status = rec.get("response", {}).get("status_code") or rec.get("status_code")
        if status is not None:
            code_node = g.add_node(nugget_node("HTTP_CODE", str(status)))
            g.add_edge(url_node["id"], code_node["id"], "had")

    return g.build()


def write_graph_artifacts(structured_path, graph_path, scenario_id: str, target: str, command: str) -> None:
    del scenario_id
    raw = structured_path.read_text(encoding="utf-8", errors="replace")
    graph = katana_to_graph(raw, target, command)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
