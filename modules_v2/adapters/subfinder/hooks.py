# -*- coding: utf-8 -*-
"""09-cited graph hooks for Subfinder structured-native adapter (modules_v2 port)."""

from __future__ import annotations

from collections import Counter
from typing import Any

from modules_v2._core.graph_builder import GraphBuilder, nugget_node
from modules_v2._core.ip_classify import ip_nugget_node
from modules_v2._core.topology import add_company_domain_tree, ensure_subdomain, host_matches_apex
from modules_v2.adapters.pius.classify import normalize_value


def _add_descriptor(
    builder: GraphBuilder,
    parent_id: str,
    nugget_id: str,
    value: Any,
    *,
    description: str | None = None,
) -> None:
    if value is None or value == "":
        return
    node = builder.add_node(
        nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR", description=description)
    )
    builder.add_edge(parent_id, node["id"], "had")


def _domain_value(raw: str) -> tuple[str, str | None]:
    normalized = normalize_value(raw)
    candidate = normalized.candidate_value.lower().rstrip(".")
    raw_value = normalized.raw_value if normalized.raw_value != candidate else None
    return candidate, raw_value


def _record_mode(record: dict[str, Any], doc: dict[str, Any]) -> str:
    return str(
        record.get("mode")
        or doc.get("enumeration_mode")
        or ("active" if record.get("ip") else "passive")
    )


def _ensure_host_node(
    builder: GraphBuilder,
    tree: dict[str, Any] | None,
    host: str,
) -> dict[str, Any]:
    if tree is None:
        return builder.add_node(nugget_node("DOMAIN_NAME", host))
    kind = host_matches_apex(host, str(tree["domain"]["nugget_data"]))
    if kind == "apex":
        return tree["domain"]
    if kind == "subdomain":
        return ensure_subdomain(builder, tree["domain"], host)
    return builder.add_node(nugget_node("DOMAIN_NAME", host))


def apply_subfinder_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Apply SPEC-019 company/domain/subdomain tree plus 09 discovery descriptors."""
    target = str(doc.get("target") or "").strip().lower().rstrip(".")
    tree: dict[str, Any] | None = None
    if target:
        tree = add_company_domain_tree(builder, scan_id, target)

    enumeration_mode = doc.get("enumeration_mode")
    if enumeration_mode:
        _add_descriptor(builder, scan_id, "SCAN_MODE", enumeration_mode)

    ip_fan_in = Counter(
        str(record.get("ip")).strip()
        for record in doc.get("records") or []
        if isinstance(record, dict) and record.get("ip")
    )

    seen_hosts: set[str] = set()
    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        host_raw = str(record.get("host") or "").strip()
        if not host_raw:
            continue

        host, raw_value = _domain_value(host_raw)
        if not host:
            continue
        host_node = _ensure_host_node(builder, tree, host)
        if raw_value:
            _add_descriptor(builder, host_node["id"], "RAW_VALUE", raw_value)

        mode = _record_mode(record, doc)
        _add_descriptor(builder, host_node["id"], "DISCOVERY_MODE", mode)

        sources = record.get("sources") or []
        if isinstance(sources, list):
            for source in sorted({str(item).strip() for item in sources if str(item).strip()}):
                _add_descriptor(builder, host_node["id"], "DISCOVERY_SOURCE", source)

        ip = str(record.get("ip") or "").strip()
        if ip:
            ip_node = builder.add_node(ip_nugget_node(ip))
            builder.add_edge(host_node["id"], ip_node["id"], "had")
            _add_descriptor(builder, host_node["id"], "LIVENESS_STATUS", "confirmed")
            if ip_fan_in[ip] >= 2:
                _add_descriptor(builder, ip_node["id"], "CDN_REVIEW_NEEDED", "true")
        else:
            _add_descriptor(builder, host_node["id"], "LIVENESS_STATUS", "unconfirmed")
        seen_hosts.add(host)

    if target and target not in seen_hosts and tree is not None:
        _add_descriptor(builder, tree["domain"]["id"], "LIVENESS_STATUS", "unconfirmed")
