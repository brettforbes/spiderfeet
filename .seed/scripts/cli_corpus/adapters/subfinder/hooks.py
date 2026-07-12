"""09-cited graph hooks for Subfinder structured-native adapter."""

from __future__ import annotations

from collections import Counter
from typing import Any

from adapters.pius.classify import normalize_value
from core.graph_builder import GraphBuilder, nugget_node
from core.ip_classify import ip_nugget_node


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


def _ensure_domain(builder: GraphBuilder, scan_id: str, value: str) -> dict[str, Any]:
    node = builder.add_node(nugget_node("DOMAIN_NAME", value.lower().rstrip(".")))
    builder.add_edge(scan_id, node["id"], "contains")
    return node


def _add_parent_descriptor(builder: GraphBuilder, domain_id: str, value: str) -> None:
    """09 S6 — reuse pius R3 parent-domain descriptor derivation."""
    labels = value.split(".")
    if len(labels) <= 2:
        return
    parent = ".".join(labels[1:])
    _add_descriptor(builder, domain_id, "DOMAIN_NAME_PARENT", parent)


def _record_mode(record: dict[str, Any], doc: dict[str, Any]) -> str:
    return str(record.get("mode") or doc.get("enumeration_mode") or ("active" if record.get("ip") else "passive"))


def apply_subfinder_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Apply 09 S0-S6; S4 uses allowed `had` until `dns-resolves-to` is SPEC-approved."""
    target = str(doc.get("target") or "").strip().lower().rstrip(".")
    if target:
        root = _ensure_domain(builder, scan_id, target)
        _add_parent_descriptor(builder, root["id"], target)

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
        domain = _ensure_domain(builder, scan_id, host)
        if raw_value:
            _add_descriptor(builder, domain["id"], "RAW_VALUE", raw_value)
        _add_parent_descriptor(builder, domain["id"], host)

        mode = _record_mode(record, doc)
        _add_descriptor(builder, domain["id"], "DISCOVERY_MODE", mode)

        sources = record.get("sources") or []
        if isinstance(sources, list):
            for source in sorted({str(item).strip() for item in sources if str(item).strip()}):
                _add_descriptor(builder, domain["id"], "DISCOVERY_SOURCE", source)

        ip = str(record.get("ip") or "").strip()
        if ip:
            ip_node = builder.add_node(ip_nugget_node(ip))
            builder.add_edge(domain["id"], ip_node["id"], "had")
            _add_descriptor(builder, domain["id"], "LIVENESS_STATUS", "confirmed")
            if ip_fan_in[ip] >= 2:
                _add_descriptor(builder, ip_node["id"], "CDN_REVIEW_NEEDED", "true")
        else:
            _add_descriptor(builder, domain["id"], "LIVENESS_STATUS", "unconfirmed")
        seen_hosts.add(host)

    # 09 S1 requires the root even when no records are emitted; if records include
    # the target, GraphBuilder deduplicates the node and edges.
    if target and target not in seen_hosts:
        root = _ensure_domain(builder, scan_id, target)
        _add_descriptor(builder, root["id"], "LIVENESS_STATUS", "unconfirmed")
