# -*- coding: utf-8 -*-
"""10-cited graph hooks for Httpx structured-native adapter (modules_v2 port)."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from core.graph_builder import GraphBuilder, nugget_node
from core.ip_classify import classify_ip, ip_nugget_node
from core.topology import add_company_domain_tree, resolve_website_root
from adapters.pius.classify import normalize_value


def _add_descriptor(builder: GraphBuilder, parent_id: str, nugget_id: str, value: Any) -> None:
    if value is None or value == "":
        return
    node = builder.add_node(nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR"))
    builder.add_edge(parent_id, node["id"], "had")


def _hostname(value: str) -> str:
    normalized = normalize_value(value.strip()).candidate_value
    parsed = urlparse(normalized if "://" in normalized else f"https://{normalized}")
    return (parsed.hostname or normalized).lower().rstrip(".")


def _host_from_record(record: dict[str, Any]) -> str:
    source = record.get("input") or record.get("url") or record.get("host") or ""
    return _hostname(str(source))


def _service_name(record: dict[str, Any]) -> str:
    scheme = record.get("scheme")
    if scheme:
        return str(scheme)
    url = str(record.get("url") or record.get("input") or "")
    parsed = urlparse(url)
    return parsed.scheme or "http"


def _split_tech(value: str) -> tuple[str, str | None]:
    if ":" not in value:
        return value, None
    name, version = value.rsplit(":", 1)
    if not name.strip() or not version.strip() or " " in version.strip():
        return value, None
    return name.strip(), version.strip()


def _system_key(record: dict[str, Any], domain: str) -> str:
    return str(record.get("host") or record.get("ip") or domain).strip()


def _port_value(record: dict[str, Any]) -> str:
    port = record.get("port")
    if port:
        return str(port)
    scheme = _service_name(record)
    return "443" if scheme == "https" else "80"


def _probe_url(record: dict[str, Any]) -> str:
    return str(record.get("url") or record.get("input") or "").strip()


def _add_network_chain(
    builder: GraphBuilder,
    system_id: str,
    ip_value: str,
    port_value: str,
) -> dict[str, Any]:
    networks = builder.add_node(nugget_node("NETWORKS", "NETWORKS", nugget_type="CATEGORY"))
    builder.add_edge(system_id, networks["id"], "contains")
    transport_parent = networks["id"]
    if ip_value and classify_ip(ip_value):
        ip_node = builder.add_node(ip_nugget_node(ip_value))
        builder.add_edge(networks["id"], ip_node["id"], "contains")
        transport_parent = ip_node["id"]
    transport = builder.add_node(nugget_node("TRANSPORT", "tcp"))
    builder.add_edge(transport_parent, transport["id"], "contains")
    _add_descriptor(builder, transport["id"], "TRANSPORT_PROTOCOL", "tcp")
    port = builder.add_node(nugget_node("PORT", port_value, nugget_type="SUBENTITY"))
    builder.add_edge(transport["id"], port["id"], "contains")
    _add_descriptor(builder, port["id"], "PORT_STATE", "open")
    return port


def _add_service_chain(
    builder: GraphBuilder,
    system_id: str,
    port_id: str,
    record: dict[str, Any],
) -> None:
    applications = builder.add_node(nugget_node("APPLICATIONS", "APPLICATIONS", nugget_type="CATEGORY"))
    builder.add_edge(system_id, applications["id"], "contains")
    service = builder.add_node(nugget_node("SERVICE", _service_name(record)))
    builder.add_edge(applications["id"], service["id"], "contains")
    builder.add_edge(service["id"], port_id, "listens-to")

    webserver = record.get("webserver")
    if webserver:
        software = builder.add_node(nugget_node("SOFTWARE_USED", str(webserver), nugget_type="SUBENTITY"))
        builder.add_edge(service["id"], software["id"], "contains")

    tech = record.get("tech") or []
    if isinstance(tech, list):
        for entry in tech:
            name, version = _split_tech(str(entry).strip())
            if not name:
                continue
            software = builder.add_node(nugget_node("SOFTWARE_USED", name, nugget_type="SUBENTITY"))
            builder.add_edge(service["id"], software["id"], "contains")
            _add_descriptor(builder, software["id"], "SOFTWARE_VERSION", version)


def _attach_website_http_facts(
    builder: GraphBuilder,
    website_root_id: str,
    record: dict[str, Any],
) -> None:
    for field, nugget_id in (
        ("status_code", "HTTP_STATUS_CODE"),
        ("title", "HTTP_TITLE"),
        ("content_type", "CONTENT_TYPE"),
        ("content_length", "CONTENT_LENGTH"),
        ("method", "HTTP_METHOD"),
        ("path", "HTTP_PATH"),
        ("time", "RESPONSE_TIME_MS"),
        ("words", "WORD_COUNT"),
        ("lines", "LINE_COUNT"),
        ("failed", "PROBE_FAILED"),
        ("timestamp", "PROBE_TIMESTAMP"),
    ):
        _add_descriptor(builder, website_root_id, nugget_id, record.get(field))

    knowledgebase = record.get("knowledgebase") or {}
    if isinstance(knowledgebase, dict):
        page_type = knowledgebase.get("PageType")
        _add_descriptor(builder, website_root_id, "PAGE_TYPE", page_type)
        _add_descriptor(builder, website_root_id, "PAGE_HASH", knowledgebase.get("pHash"))
        if str(page_type).lower() == "error":
            _add_descriptor(builder, website_root_id, "IS_ERROR_PAGE", "true")


def apply_httpx_records(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Apply SPEC-019 website roots plus 10 H0-H7 host/CDN chains."""
    target = str(doc.get("target") or "").lower().rstrip(".")
    tree = add_company_domain_tree(builder, scan_id, target) if target else None

    if doc.get("probe_profile"):
        _add_descriptor(builder, scan_id, "SCAN_PROBE_PROFILE", doc.get("probe_profile"))
    if doc.get("host_input_count") is not None:
        _add_descriptor(builder, scan_id, "SCAN_HOST_INPUT_COUNT", doc.get("host_input_count"))
    if doc.get("subfinder_scenario"):
        _add_descriptor(builder, scan_id, "UPSTREAM_SCENARIO_ID", doc.get("subfinder_scenario"))

    confirmed_roots: set[str] = set()
    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        domain_value = _host_from_record(record)
        if not domain_value:
            continue
        if tree is not None:
            website_root = resolve_website_root(builder, tree, domain_value)
        else:
            website_root = builder.add_node(nugget_node("DOMAIN_NAME", domain_value))
        _add_descriptor(builder, website_root["id"], "HTTP_LIVENESS_STATUS", "confirmed")
        confirmed_roots.add(domain_value)

        system_nugget = "CDN" if record.get("cdn") is True else "HOST"
        system = builder.add_node(nugget_node(system_nugget, _system_key(record, domain_value)))
        builder.add_edge(scan_id, system["id"], "contains")
        builder.add_edge(website_root["id"], system["id"], "had")
        if system_nugget == "CDN":
            _add_descriptor(builder, system["id"], "CDN_NAME", record.get("cdn_name"))
            _add_descriptor(builder, system["id"], "CDN_TYPE", record.get("cdn_type"))

        ip_value = str(record.get("ip") or "").strip()
        if not ip_value:
            a_records = record.get("a") or []
            if a_records:
                ip_value = str(a_records[0]).strip()
        port = _add_network_chain(builder, system["id"], ip_value, _port_value(record))
        _add_service_chain(builder, system["id"], port["id"], record)
        _attach_website_http_facts(builder, website_root["id"], record)

        probe_url = _probe_url(record)
        if probe_url:
            url_node = builder.add_node(nugget_node("LINKED_URL_INTERNAL", probe_url))
            builder.add_edge(website_root["id"], url_node["id"], "contains")

        for cname in record.get("cname") or []:
            cname_value = _hostname(str(cname))
            cname_node = builder.add_node(nugget_node("DOMAIN_NAME", cname_value))
            builder.add_edge(website_root["id"], cname_node["id"], "had")
            _add_descriptor(builder, website_root["id"], "CNAME_TARGET", cname_value)

        for ip in record.get("a") or []:
            ip_node = builder.add_node(ip_nugget_node(str(ip)))
            builder.add_edge(website_root["id"], ip_node["id"], "had")
            _add_descriptor(
                builder,
                ip_node["id"],
                "PROBE_CONNECTED",
                "true" if str(ip) == str(record.get("host")) else "false",
            )

    if target and tree is not None and target not in confirmed_roots:
        _add_descriptor(builder, tree["domain"]["id"], "HTTP_LIVENESS_STATUS", "unconfirmed")
