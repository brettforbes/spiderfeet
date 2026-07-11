#!/usr/bin/env python3
"""Build proposed nugget graphs from httpx structured JSON bundles."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlparse

from graph_builder import GraphBuilder, nugget_node
from httpx_structured import records_only


def _host_from_record(rec: dict[str, Any]) -> str:
    url = str(rec.get("url") or rec.get("input") or "").strip()
    host = rec.get("host")
    if host:
        return str(host).lower().rstrip(".")
    if url:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        return (parsed.hostname or "").lower().rstrip(".")
    return ""


def httpx_to_graph(raw: str, target: str, command: str) -> dict[str, Any]:
    records = records_only(raw)
    g = GraphBuilder()
    apex = target.lower().rstrip(".")

    scan = g.add_node(nugget_node("SCAN_RECORD", apex, description="httpx probe scan"))
    scan_cli = g.add_node(nugget_node("SCAN_CLI", command if command else apex, nugget_type="DESCRIPTOR"))
    g.add_edge(scan["id"], scan_cli["id"], "had")

    domain = g.add_node(nugget_node("DOMAIN_NAME", apex))
    g.add_edge(scan["id"], domain["id"], "contains")

    seen_urls: set[str] = set()
    for rec in records:
        if rec.get("failed"):
            continue
        url = str(rec.get("url") or "").strip()
        if not url:
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)

        url_node = g.add_node(nugget_node("LINKED_URL_INTERNAL", url))
        g.add_edge(scan["id"], url_node["id"], "contains")

        host = _host_from_record(rec)
        if host:
            host_node = g.add_node(nugget_node("INTERNET_NAME", host))
            g.add_edge(domain["id"], host_node["id"], "contains")
            g.add_edge(url_node["id"], host_node["id"], "contains")

        ip = rec.get("ip")
        if ip:
            ip_node = g.add_node(nugget_node("IP_ADDRESS", str(ip)))
            if host:
                g.add_edge(host_node["id"], ip_node["id"], "contains")

        status = rec.get("status_code")
        if status is not None:
            code_node = g.add_node(nugget_node("HTTP_CODE", str(status)))
            g.add_edge(url_node["id"], code_node["id"], "had")

        webserver = rec.get("webserver")
        if webserver:
            banner = g.add_node(nugget_node("WEBSERVER_BANNER", str(webserver)))
            g.add_edge(url_node["id"], banner["id"], "had")

        tech_list = rec.get("tech") or []
        if isinstance(tech_list, list):
            for tech in tech_list:
                tech_name = str(tech).strip()
                if not tech_name:
                    continue
                tech_node = g.add_node(nugget_node("WEBSERVER_TECHNOLOGY", tech_name))
                g.add_edge(url_node["id"], tech_node["id"], "had")

        cdn = rec.get("cdn_name") or rec.get("cdn")
        if cdn:
            cdn_node = g.add_node(nugget_node("PROVIDER_HOSTING", str(cdn)))
            g.add_edge(url_node["id"], cdn_node["id"], "had")

    return g.build()


def write_graph_artifacts(structured_path, graph_path, scenario_id: str, target: str, command: str) -> None:
    del scenario_id
    raw = structured_path.read_text(encoding="utf-8", errors="replace")
    graph = httpx_to_graph(raw, target, command)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
