"""Graph hooks for Katana structured-native adapter (SPEC-004 D4)."""

from __future__ import annotations

from typing import Any

from core.graph_builder import GraphBuilder, nugget_node
from katana_structured import _host_from_record


def _add_descriptor(builder: GraphBuilder, parent_id: str, nugget_id: str, value: Any) -> None:
    if value is None or value == "":
        return
    node = builder.add_node(nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR"))
    builder.add_edge(parent_id, node["id"], "had")


def _url_from_record(record: dict[str, Any]) -> str:
    return str(record.get("url") or record.get("request", {}).get("endpoint") or "").strip()


def apply_katana_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Apply Katana crawl hierarchy (doc 14 / legacy katana_json_to_graph migration)."""
    target = str(doc.get("target") or "").lower().rstrip(".")
    if target:
        root = builder.add_node(nugget_node("DOMAIN_NAME", target))
        builder.add_edge(scan_id, root["id"], "contains")

    if doc.get("crawl_profile"):
        _add_descriptor(builder, scan_id, "SCAN_CRAWL_PROFILE", doc.get("crawl_profile"))
    if doc.get("url_input_count") is not None:
        _add_descriptor(builder, scan_id, "SCAN_URL_INPUT_COUNT", doc.get("url_input_count"))
    if doc.get("httpx_scenario"):
        _add_descriptor(builder, scan_id, "UPSTREAM_SCENARIO_ID", doc.get("httpx_scenario"))

    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        url = _url_from_record(record)
        if not url:
            continue
        url_node = builder.add_node(nugget_node("LINKED_URL_INTERNAL", url))
        builder.add_edge(scan_id, url_node["id"], "contains")

        host = _host_from_record(record)
        if host:
            host_node = builder.add_node(nugget_node("DOMAIN_NAME", host))
            if target:
                root = builder.add_node(nugget_node("DOMAIN_NAME", target))
                builder.add_edge(root["id"], host_node["id"], "contains")
            builder.add_edge(host_node["id"], url_node["id"], "contains")

        request = record.get("request") or {}
        response = record.get("response") or {}
        _add_descriptor(builder, url_node["id"], "HTTP_METHOD", request.get("method") or record.get("method"))
        status = response.get("status_code") or record.get("status_code")
        _add_descriptor(builder, url_node["id"], "HTTP_STATUS_CODE", status)
