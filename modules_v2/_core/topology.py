"""Reusable graph topology templates for SPEC-004 rule packs."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .graph_builder import GraphBuilder, nugget_node
from .ip_classify import ip_nugget_node


def add_scan_head(
    builder: GraphBuilder,
    scan_data: str,
    *,
    command: str | None = None,
) -> dict[str, Any]:
    """Create the common scan head and CLI descriptor."""
    scan = builder.add_node(nugget_node("SCAN_RECORD", scan_data, description="Scan Record"))
    cli = builder.add_node(
        nugget_node("SCAN_CLI", command or scan_data, nugget_type="DESCRIPTOR", description="Scan CLI"),
        parent_id=scan["id"],
    )
    builder.add_edge(scan["id"], cli["id"], "had")
    return scan


def add_system_l2(
    builder: GraphBuilder,
    scan_id: str,
    *,
    system: str,
    ip_address: str,
    mac_address: str | None = None,
    mac_vendor: str | None = None,
) -> dict[str, Any]:
    """Create the Netdiscover-style SYSTEM -> NETWORKS -> IP/MAC shape."""
    system_node = builder.add_node(
        nugget_node("SYSTEM", system, description="System"),
        parent_id=scan_id,
    )
    networks = builder.add_node(
        nugget_node("NETWORKS", f"networks:{system}"),
        parent_id=system_node["id"],
    )
    ip_node = builder.add_node(
        ip_nugget_node(ip_address, description="IP Address"),
        parent_id=networks["id"],
    )

    builder.add_edge(scan_id, system_node["id"], "contains")
    builder.add_edge(system_node["id"], networks["id"], "contains")
    builder.add_edge(networks["id"], ip_node["id"], "contains")

    result = {"system": system_node, "networks": networks, "ip_address": ip_node}
    if mac_address:
        mac_node = builder.add_node(
            nugget_node("MAC_ADDRESS", mac_address.lower(), description="MAC Address"),
            parent_id=networks["id"],
        )
        builder.add_edge(networks["id"], mac_node["id"], "contains")
        result["mac_address"] = mac_node
        if mac_vendor:
            vendor_node = builder.add_node(
                nugget_node("MAC_VENDOR", mac_vendor, nugget_type="DESCRIPTOR", description="MAC Vendor"),
                parent_id=mac_node["id"],
            )
            builder.add_edge(mac_node["id"], vendor_node["id"], "had")
            result["mac_vendor"] = vendor_node
    return result


def add_host_networks_port_service(
    builder: GraphBuilder,
    scan_id: str,
    *,
    host: str,
    ip_address: str,
    transport: str,
    port: str | int,
    service: str,
) -> dict[str, Any]:
    """Create HOST -> NETWORKS/APPLICATIONS -> transport/port/service shape."""
    host_node = builder.add_node(
        nugget_node("HOST", host, description="Host"),
        parent_id=scan_id,
    )
    networks = builder.add_node(
        nugget_node("NETWORKS", f"networks:{host}"),
        parent_id=host_node["id"],
    )
    ip_node = builder.add_node(
        ip_nugget_node(ip_address, description="IP Address"),
        parent_id=networks["id"],
    )
    transport_node = builder.add_node(
        nugget_node("TRANSPORT", transport, description="Transport Protocol"),
        parent_id=networks["id"],
    )
    port_node = builder.add_node(
        nugget_node("PORT", str(port), nugget_type="SUBENTITY", description="Network Port"),
        parent_id=transport_node["id"],
    )
    protocol_node = builder.add_node(
        nugget_node("PORT_PROTOCOL", transport, nugget_type="DESCRIPTOR", description="Port Protocol"),
        parent_id=port_node["id"],
    )
    applications = builder.add_node(
        nugget_node("APPLICATIONS", f"applications:{host}"),
        parent_id=host_node["id"],
    )
    service_node = builder.add_node(
        nugget_node("SERVICE", service, description="Network Service"),
        parent_id=applications["id"],
    )

    builder.add_edge(scan_id, host_node["id"], "contains")
    builder.add_edge(host_node["id"], networks["id"], "contains")
    builder.add_edge(networks["id"], ip_node["id"], "contains")
    builder.add_edge(networks["id"], transport_node["id"], "contains")
    builder.add_edge(transport_node["id"], port_node["id"], "contains")
    builder.add_edge(port_node["id"], protocol_node["id"], "had")
    builder.add_edge(host_node["id"], applications["id"], "contains")
    builder.add_edge(applications["id"], service_node["id"], "contains")
    builder.add_edge(service_node["id"], port_node["id"], "listens-to")

    return {
        "host": host_node,
        "networks": networks,
        "ip_address": ip_node,
        "transport": transport_node,
        "port": port_node,
        "port_protocol": protocol_node,
        "applications": applications,
        "service": service_node,
    }


def add_trace_hop_chain(
    builder: GraphBuilder,
    scan_id: str,
    *,
    trace: str,
    hops: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Create TRACE -> TRACE_HOP nodes with hop descriptors."""
    trace_node = builder.add_node(
        nugget_node("TRACE", trace, description="Trace"),
        parent_id=scan_id,
    )
    builder.add_edge(scan_id, trace_node["id"], "contains")

    hop_nodes = []
    for index, hop in enumerate(hops, start=1):
        hop_label = str(hop.get("host") or hop.get("ip") or f"{trace}:hop:{index}")
        hop_node = builder.add_node(
            nugget_node("TRACE_HOP", hop_label, nugget_type="SUBENTITY"),
            parent_id=trace_node["id"],
        )
        builder.add_edge(trace_node["id"], hop_node["id"], "contains")
        hop_nodes.append(hop_node)

        order = builder.add_node(
            nugget_node("HOP_ORDER", str(hop.get("order", index)), nugget_type="DESCRIPTOR"),
            parent_id=hop_node["id"],
        )
        builder.add_edge(hop_node["id"], order["id"], "had")
        for field, nugget_id in (("ttl", "HOP_TTL"), ("rtt", "HOP_RTT")):
            value = hop.get(field)
            if value is None or value == "":
                continue
            descriptor = builder.add_node(
                nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR"),
                parent_id=hop_node["id"],
            )
            builder.add_edge(hop_node["id"], descriptor["id"], "had")

    return {"trace": trace_node, "hops": hop_nodes}
def add_company_domain_tree(
    builder: GraphBuilder,
    scan_id: str,
    apex: str,
    company_name: str | None = None,
) -> dict[str, Any]:
    """Create SCAN -> COMPANY -> DOMAIN_NAME(apex) with optional COMPANY_NAME."""
    company_data = f"company:{apex}"
    company_node = builder.add_node(
        nugget_node("COMPANY", company_data, description="Company"),
        parent_id=scan_id,
    )
    builder.add_edge(scan_id, company_node["id"], "contains")

    domain_node = builder.add_node(
        nugget_node("DOMAIN_NAME", apex, description="Domain Name"),
        parent_id=company_node["id"],
    )
    builder.add_edge(company_node["id"], domain_node["id"], "contains")

    result: dict[str, Any] = {"company": company_node, "domain": domain_node}
    if company_name:
        name_node = builder.add_node(
            nugget_node(
                "COMPANY_NAME",
                company_name,
                nugget_type="DESCRIPTOR",
                description="Company Name",
            ),
            parent_id=company_node["id"],
        )
        builder.add_edge(company_node["id"], name_node["id"], "had")
        result["company_name"] = name_node
    return result
