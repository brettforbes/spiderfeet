"""07B-cited graph hooks for Nerva structured-native adapter."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from core.correlation_engine import RecordCorrelationResult, correlate_nerva_records
from core.graph_builder import GraphBuilder, nugget_node

_CDN_LAYER_MARKERS = frozenset(
    {
        "cloudflare",
        "cloudflare browser insights",
        "fastly",
        "akamai",
        "hsts",
        "http/3",
        "http/2",
    }
)


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


def _header_value(headers: dict[str, Any], name: str) -> str:
    for key, values in (headers or {}).items():
        if str(key).lower() != name.lower():
            continue
        if isinstance(values, list) and values:
            return str(values[0])
        if values is not None:
            return str(values)
    return ""


def _header_list(headers: dict[str, Any], name: str) -> list[str]:
    for key, values in (headers or {}).items():
        if str(key).lower() != name.lower():
            continue
        if isinstance(values, list):
            return [str(item) for item in values if item is not None]
        if values is not None:
            return [str(values)]
    return []


def _pop_code(cf_ray: str) -> str | None:
    if "-" not in cf_ray:
        return None
    suffix = cf_ray.rsplit("-", 1)[-1].strip()
    return suffix or None


def _parse_server_timing(value: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for part in value.split(","):
        part = part.strip()
        if "cfEdge;dur=" in part:
            found["edge"] = part.split("dur=", 1)[-1].strip()
        if "cfOrigin;dur=" in part:
            found["origin"] = part.split("dur=", 1)[-1].strip()
    return found


def _parse_hsts(value: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    match = re.search(r"max-age=(\d+)", value, re.I)
    if match:
        result["max_age"] = match.group(1)
    result["preload"] = "preload" in value.lower()
    result["include_subdomains"] = "includesubdomains" in value.lower()
    return result


def _csp_third_parties(csp: str, own_host: str) -> list[str]:
    domains: set[str] = set()
    for token in re.findall(r"(?:\*\.)?([a-z0-9.-]+\.[a-z]{2,})", csp, re.I):
        host = token.lower().lstrip(".")
        if host.endswith(own_host.lower()) or host == own_host.lower():
            continue
        if host in {"self", "blob", "data", "https", "http"}:
            continue
        domains.add(host)
    return sorted(domains)


def _is_cdn_layer_software(name: str) -> bool:
    return name.strip().lower() in _CDN_LAYER_MARKERS


def _correlation_by_record(
    records: list[dict[str, Any]],
) -> dict[str, RecordCorrelationResult]:
    results = correlate_nerva_records(records)
    by_id = {row.record_id: row for row in results}
    mapped: dict[str, RecordCorrelationResult] = {}
    for index, record in enumerate(records):
        record_id = f"{record.get('host', 'unknown')}:{record.get('ip', '?')}:{record.get('port', 0)}:{index}"
        mapped[record_id] = by_id[record_id]
    return mapped


def _system_key(corr: RecordCorrelationResult) -> tuple[str, str]:
    if corr.host_classification == "fronted_unknown":
        return ("CDN", corr.hostname)
    if corr.same_system_group_id:
        return ("HOST", corr.same_system_group_id)
    return ("HOST", corr.ip_address)


def apply_nerva_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """
    07B N0–N5 — expand nerva records into SYSTEM/HOST/CDN topology.

    N1 runs correlation_engine before any HOST/CDN node is created.
    """
    records = list(doc.get("records") or [])
    if not records:
        return

    correlation = _correlation_by_record(records)
    systems: dict[tuple[str, str], dict[str, Any]] = {}

    for index, record in enumerate(records):
        record_id = f"{record.get('host', 'unknown')}:{record.get('ip', '?')}:{record.get('port', 0)}:{index}"
        corr = correlation[record_id]
        key = _system_key(corr)
        if key not in systems:
            systems[key] = _ensure_system(builder, scan_id, key, corr)
        _attach_record(builder, systems[key], record, corr)


def _ensure_system(
    builder: GraphBuilder,
    scan_id: str,
    key: tuple[str, str],
    corr: RecordCorrelationResult,
) -> dict[str, Any]:
    kind, data = key
    if kind == "CDN":
        # 07B N1 — one CDN node keyed on hostname when Ruleset C fires.
        system = builder.add_node(nugget_node("CDN", data, description="CDN"))
    else:
        system = builder.add_node(nugget_node("HOST", data, description="Host"))
    builder.add_edge(scan_id, system["id"], "contains")

    _add_descriptor(builder, system["id"], "HOST_CLASSIFICATION", corr.host_classification)
    if corr.classification_rule_fired:
        _add_descriptor(builder, system["id"], "CLASSIFICATION_RULE_FIRED", corr.classification_rule_fired)
    if corr.cdn_vendor:
        _add_descriptor(builder, system["id"], "CDN_VENDOR", corr.cdn_vendor)
    if corr.origin_host_count is None and corr.host_classification == "fronted_unknown":
        # Explicit null contract from Ruleset C / 07B N1 — omit numeric count.
        _add_descriptor(builder, system["id"], "ORIGIN_HOST_COUNT", "indeterminate")

    networks = builder.add_node(nugget_node("NETWORKS", f"networks:{data}"))
    applications = builder.add_node(nugget_node("APPLICATIONS", f"applications:{data}"))
    builder.add_edge(system["id"], networks["id"], "contains")
    builder.add_edge(system["id"], applications["id"], "contains")
    return {
        "kind": kind,
        "system": system,
        "networks": networks,
        "applications": applications,
        "ips": set(),
        "fronted": corr.host_classification == "fronted_unknown",
        "cdn_vendor": corr.cdn_vendor,
    }


def _attach_record(
    builder: GraphBuilder,
    system_ctx: dict[str, Any],
    record: dict[str, Any],
    corr: RecordCorrelationResult,
) -> None:
    ip = str(record.get("ip") or "")
    if ip and ip not in system_ctx["ips"]:
        ip_node = builder.add_node(nugget_node("IP_ADDRESS", ip, description="IP Address"))
        builder.add_edge(system_ctx["networks"]["id"], ip_node["id"], "contains")
        system_ctx["ips"].add(ip)

    metadata = record.get("metadata") or {}
    headers = metadata.get("response_headers") or {}
    protocol = str(record.get("protocol") or "unknown")
    port = str(record.get("port") or "")
    transport = str(record.get("transport") or "tcp")
    service_name = protocol

    service = builder.add_node(nugget_node("SERVICE", service_name, description="Network Service"))
    builder.add_edge(system_ctx["applications"]["id"], service["id"], "contains")

    if port:
        port_node = builder.add_node(
            nugget_node("PORT", port, nugget_type="SUBENTITY", description="Network Port")
        )
        if ip:
            # Keep port under the IP networks branch when available.
            transport_node = builder.add_node(
                nugget_node("TRANSPORT", transport, description="Transport Protocol")
            )
            ip_id = builder.add_node(nugget_node("IP_ADDRESS", ip))["id"]
            builder.add_edge(ip_id, transport_node["id"], "contains")
            builder.add_edge(transport_node["id"], port_node["id"], "contains")
        builder.add_edge(service["id"], port_node["id"], "listens-to")

    version = record.get("version")
    if version:
        _add_descriptor(builder, service["id"], "SERVICE_VERSION", version)

    status_code = metadata.get("status_code")
    if status_code is not None:
        _add_descriptor(builder, service["id"], "HTTP_STATUS_CODE", status_code)

    if record.get("tls") is not None:
        _add_descriptor(builder, service["id"], "TLS_ENABLED", bool(record.get("tls")))

    banner = metadata.get("banner")
    if banner:
        _add_descriptor(builder, service["id"], "SERVICE_BANNER", str(banner).strip())

    # 07B N2 — CDN operational descriptors.
    if system_ctx["fronted"]:
        cf_ray = _header_value(headers, "Cf-Ray")
        if cf_ray:
            _add_descriptor(builder, system_ctx["system"]["id"], "EDGE_NODE_ID", cf_ray)
            pop = _pop_code(cf_ray)
            if pop:
                _add_descriptor(builder, system_ctx["system"]["id"], "CDN_POP_CODE", pop)

        cache = _header_value(headers, "Cf-Cache-Status")
        if cache:
            _add_descriptor(builder, service["id"], "CACHE_STATUS", cache)

        timing_parts = []
        for item in _header_list(headers, "Server-Timing"):
            timing_parts.append(item)
        timing = _parse_server_timing(",".join(timing_parts))
        if timing.get("edge") is not None:
            _add_descriptor(builder, service["id"], "EDGE_DURATION_MS", timing["edge"])
        if timing.get("origin") is not None:
            _add_descriptor(builder, service["id"], "ORIGIN_DURATION_MS", timing["origin"])

        alt_svc = _header_value(headers, "Alt-Svc")
        if "h3" in alt_svc.lower():
            _add_descriptor(builder, service["id"], "PROTOCOLS_OFFERED", "h3")

        hsts = _parse_hsts(_header_value(headers, "Strict-Transport-Security"))
        if hsts.get("max_age"):
            _add_descriptor(builder, service["id"], "HSTS_MAX_AGE", hsts["max_age"])
        if hsts.get("preload"):
            _add_descriptor(builder, service["id"], "HSTS_PRELOAD", True)
        if hsts.get("include_subdomains"):
            _add_descriptor(builder, service["id"], "HSTS_INCLUDE_SUBDOMAINS", True)

        csp = _header_value(headers, "Content-Security-Policy")
        for domain in _csp_third_parties(csp, str(record.get("host") or "")):
            _add_descriptor(builder, service["id"], "CSP_THIRD_PARTY_DOMAIN", domain)

        if _header_value(headers, "Nel") or _header_value(headers, "Report-To"):
            _add_descriptor(builder, service["id"], "NEL_ACTIVE", True)

    # 07B N3 — technologies / CPEs / fingerprint metadata.
    fingerprint = metadata.get("fingerprint_metadata") or {}
    for technology in metadata.get("technologies") or []:
        tech_name = str(technology)
        software = builder.add_node(nugget_node("SOFTWARE_USED", tech_name))
        builder.add_edge(service["id"], software["id"], "contains")

        # 07B N4 — suppress origin-looking fingerprints under CDN.
        if system_ctx["fronted"] and not _is_cdn_layer_software(tech_name):
            _add_descriptor(builder, software["id"], "ORIGIN_FINGERPRINT_SUPPRESSED", True)

        meta_key = _match_fingerprint_key(tech_name, fingerprint)
        if meta_key:
            meta = fingerprint[meta_key] or {}
            _add_descriptor(builder, software["id"], "SOFTWARE_VENDOR", meta.get("vendor"))
            _add_descriptor(builder, software["id"], "SOFTWARE_PRODUCT", meta.get("product"))
            _add_descriptor(builder, software["id"], "DETECTION_METHOD", meta.get("detection_method"))

    for cpe in metadata.get("cpes") or []:
        cpe_node = builder.add_node(nugget_node("CPE_URL", str(cpe)))
        builder.add_edge(service["id"], cpe_node["id"], "contains")

    # 07B N5 — redirect location via allowed `had` relation only
    # (`redirects-to` requires SPEC update before use).
    try:
        status = int(metadata.get("status_code") or 0)
    except (TypeError, ValueError):
        status = 0
    location = _header_value(headers, "Location")
    if 300 <= status < 400 and location:
        _add_descriptor(builder, service["id"], "HTTP_REDIRECT_LOCATION", location)
        parsed = urlparse(location)
        if parsed.hostname:
            domain = builder.add_node(nugget_node("DOMAIN_NAME", parsed.hostname.lower()))
            builder.add_edge(service["id"], domain["id"], "contains")


def _match_fingerprint_key(tech_name: str, fingerprint: dict[str, Any]) -> str | None:
    normalized = re.sub(r"[^a-z0-9]+", "", tech_name.lower())
    for key in fingerprint:
        key_norm = re.sub(r"[^a-z0-9]+", "", str(key).lower())
        if key_norm == normalized or key_norm in normalized or normalized in key_norm:
            return str(key)
    return None
