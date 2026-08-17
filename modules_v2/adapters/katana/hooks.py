# -*- coding: utf-8 -*-
"""Graph hooks for Katana structured-native adapter (modules_v2 port)."""

from __future__ import annotations

from typing import Any

from modules_v2._core.graph_builder import GraphBuilder, nugget_node
from modules_v2._core.topology import add_company_domain_tree, host_matches_apex, resolve_website_root
from modules_v2.adapters.katana.structured import host_from_record


def _add_descriptor(builder: GraphBuilder, parent_id: str, nugget_id: str, value: Any) -> None:
    if value is None or value == "":
        return
    node = builder.add_node(nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR"))
    builder.add_edge(parent_id, node["id"], "had")


def _url_from_record(record: dict[str, Any]) -> str:
    return str(record.get("url") or record.get("request", {}).get("endpoint") or "").strip()


def apply_katana_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Apply SPEC-019 hostname URL ownership for Katana crawl records."""
    target = str(doc.get("target") or "").lower().rstrip(".")
    tree = add_company_domain_tree(builder, scan_id, target) if target else None

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

        host = host_from_record(record)
        url_kind = "LINKED_URL_EXTERNAL"
        owner_id: str | None = None
        if host and tree is not None:
            if host_matches_apex(host, target) in {"apex", "subdomain"}:
                root = resolve_website_root(builder, tree, host)
                owner_id = root["id"]
                url_kind = "LINKED_URL_INTERNAL"

        url_node = builder.add_node(nugget_node(url_kind, url))
        if owner_id is not None:
            builder.add_edge(owner_id, url_node["id"], "contains")
        else:
            builder.add_edge(scan_id, url_node["id"], "contains")

        request = record.get("request") or {}
        response = record.get("response") or {}
        _add_descriptor(
            builder,
            url_node["id"],
            "HTTP_METHOD",
            request.get("method") or record.get("method"),
        )
        status = response.get("status_code") or record.get("status_code")
        _add_descriptor(builder, url_node["id"], "HTTP_STATUS_CODE", status)

