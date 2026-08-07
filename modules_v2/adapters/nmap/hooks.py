"""06B-cited graph hooks for Nmap structured-native adapter."""

from __future__ import annotations

from typing import Any

from modules_v2._core.graph_builder import GraphBuilder, nugget_node
from modules_v2._core.ip_classify import ip_nugget_node


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


def _ssh_key_nugget_id(key_type: str) -> str | None:
    key_type = key_type.lower()
    if "ed25519" in key_type or "eddsa" in key_type:
        return "EDDSA"
    if "ecdsa" in key_type:
        return "ECDSA"
    if "rsa" in key_type:
        return "RSA"
    if "dss" in key_type or "dsa" in key_type:
        return "DSA"
    return None


def apply_host_scan_head(
    builder: GraphBuilder,
    scan_id: str,
    host: dict[str, Any],
) -> dict[str, Any]:
    """Create HOST / NETWORKS / IPV4_ADDRESS scaffold for one host row."""
    host_key = host["host_key"]
    host_node = builder.add_node(nugget_node("HOST", host_key, description="Host"))
    builder.add_edge(scan_id, host_node["id"], "contains")

    status = host.get("status") or {}
    _add_descriptor(builder, host_node["id"], "HOST_STATUS", status.get("state"))
    _add_descriptor(builder, host_node["id"], "HOST_STATUS_REASON", status.get("reason"))
    for name in host.get("hostnames") or []:
        _add_descriptor(builder, host_node["id"], "INTERNET_NAME", name)

    networks = builder.add_node(nugget_node("NETWORKS", f"networks:{host_key}"))
    ip_node = builder.add_node(ip_nugget_node(host_key, description="IP Address"))
    builder.add_edge(host_node["id"], networks["id"], "contains")
    builder.add_edge(networks["id"], ip_node["id"], "contains")

    return {"host": host_node, "networks": networks, "ip_address": ip_node}


def apply_ports_and_services(
    builder: GraphBuilder,
    host_nodes: dict[str, Any],
    host: dict[str, Any],
) -> dict[tuple[str, str], str]:
    """
    06B P1 — TRANSPORT contains PORT; service listens-to port.

    Returns a map of (protocol, portid) -> PORT node id for P2/P3 reconciliation.
    """
    host_key = host["host_key"]
    host_id = host_nodes["host"]["id"]
    ip_id = host_nodes["ip_address"]["id"]

    apps = builder.add_node(nugget_node("APPLICATIONS", f"applications:{host_key}"))
    builder.add_edge(host_id, apps["id"], "contains")

    port_index: dict[tuple[str, str], str] = {}
    for port in host.get("ports") or []:
        proto = port.get("protocol", "tcp")
        portid = str(port.get("portid", ""))
        if not portid:
            continue

        transport = builder.add_node(nugget_node("TRANSPORT", proto, description="Transport Protocol"))
        builder.add_edge(ip_id, transport["id"], "contains")

        port_node = builder.add_node(
            nugget_node("PORT", portid, nugget_type="SUBENTITY", description="Network Port")
        )
        builder.add_edge(transport["id"], port_node["id"], "contains")
        port_index[(proto, portid)] = port_node["id"]

        _add_descriptor(builder, port_node["id"], "PORT_STATE", port.get("state"))
        _add_descriptor(builder, port_node["id"], "PORT_STATE_REASON", port.get("state_reason"))
        _add_descriptor(builder, port_node["id"], "PORT_PROTOCOL", proto)
        if port.get("source") == "os_probe":
            _add_descriptor(builder, port_node["id"], "PORT_SOURCE", "os_probe")

        service_info = port.get("service") or {}
        svc_name = service_info.get("name") or "unknown"
        service_node = builder.add_node(nugget_node("SERVICE", svc_name, description="Network Service"))
        builder.add_edge(apps["id"], service_node["id"], "contains")
        builder.add_edge(service_node["id"], port_node["id"], "listens-to")

        product = service_info.get("product")
        version = service_info.get("version")
        if product or version:
            _add_descriptor(
                builder,
                service_node["id"],
                "SERVICE_VERSION",
                " ".join(x for x in (product, version) if x),
            )
        _add_descriptor(builder, service_node["id"], "SERVICE_FINGERPRINT", service_info.get("servicefp"))
        _add_descriptor(builder, service_node["id"], "SERVICE_EXTRAINFO", service_info.get("extrainfo"))
        for cpe in service_info.get("cpes") or []:
            cpe_node = builder.add_node(nugget_node("CPE_URL", cpe))
            builder.add_edge(service_node["id"], cpe_node["id"], "contains")

        scripts = port.get("scripts") or {}
        for key_data in scripts.get("ssh_hostkeys") or []:
            nugget_id = _ssh_key_nugget_id(str(key_data.get("type", "")))
            fingerprint = key_data.get("fingerprint")
            if not nugget_id or not fingerprint:
                continue
            key_node = builder.add_node(nugget_node(nugget_id, fingerprint, nugget_type="SUBENTITY"))
            builder.add_edge(service_node["id"], key_node["id"], "contains")
            _add_descriptor(builder, key_node["id"], "SSH_KEY_BITS", key_data.get("bits"))
            _add_descriptor(builder, key_node["id"], "SSH_KEY_TYPE", key_data.get("type"))
            _add_descriptor(builder, key_node["id"], "SSH_KEY_KEY", key_data.get("key"))

        http_title = scripts.get("http_title")
        if http_title:
            _add_descriptor(builder, service_node["id"], "HTTP_TITLE", http_title)

    return port_index


def apply_os_matches(
    builder: GraphBuilder,
    host_nodes: dict[str, Any],
    host: dict[str, Any],
) -> str | None:
    """
    06B G1, N0, N1, N2, N3, N4 — ENVIRONMENT contains OPERATING_SYSTEM subgraphs.

    Returns the node id of the highest-accuracy OPERATING_SYSTEM candidate for P3.
    """
    os_block = host.get("os")
    if not os_block:
        return None

    host_key = host["host_key"]
    host_id = host_nodes["host"]["id"]
    environment = builder.add_node(nugget_node("ENVIRONMENT", f"environment:{host_key}"))
    builder.add_edge(host_id, environment["id"], "contains")

    top_os_id: str | None = None
    top_accuracy = -1

    for match in os_block.get("matches") or []:
        os_name = match.get("name") or "unknown"
        for osclass in match.get("classes") or [{}]:
            os_node = builder.add_node(
                nugget_node("OPERATING_SYSTEM", os_name, description="Operating System")
            )
            builder.add_edge(environment["id"], os_node["id"], "contains")

            accuracy = osclass.get("accuracy") or match.get("accuracy")
            _add_descriptor(builder, os_node["id"], "OS_TYPE", osclass.get("type"))
            _add_descriptor(builder, os_node["id"], "OS_VENDOR", osclass.get("vendor"))
            _add_descriptor(builder, os_node["id"], "OS_FAMILY", osclass.get("osfamily"))
            _add_descriptor(builder, os_node["id"], "ACCURACY", accuracy)
            _add_descriptor(builder, os_node["id"], "OS_GEN", osclass.get("osgen"))

            for cpe in osclass.get("cpes") or []:
                cpe_node = builder.add_node(nugget_node("CPE_URL", cpe))
                builder.add_edge(os_node["id"], cpe_node["id"], "contains")

            try:
                acc_value = int(str(accuracy or "0"))
            except ValueError:
                acc_value = 0
            if acc_value > top_accuracy:
                top_accuracy = acc_value
                top_os_id = os_node["id"]

    return top_os_id


def reconcile_os_probe_ports(
    builder: GraphBuilder,
    host_nodes: dict[str, Any],
    host: dict[str, Any],
    port_index: dict[tuple[str, str], str],
) -> dict[tuple[str, str], str]:
    """06B P2 — create missing PORT nodes referenced by `<portused>` entries."""
    os_block = host.get("os") or {}
    ip_id = host_nodes["ip_address"]["id"]

    for entry in os_block.get("portused") or []:
        proto = entry.get("proto") or "tcp"
        portid = str(entry.get("portid") or "")
        if not portid:
            continue
        key = (proto, portid)
        if key in port_index:
            continue

        transport = builder.add_node(nugget_node("TRANSPORT", proto, description="Transport Protocol"))
        builder.add_edge(ip_id, transport["id"], "contains")
        port_node = builder.add_node(
            nugget_node("PORT", portid, nugget_type="SUBENTITY", description="Network Port")
        )
        builder.add_edge(transport["id"], port_node["id"], "contains")
        _add_descriptor(builder, port_node["id"], "PORT_STATE", entry.get("state"))
        _add_descriptor(builder, port_node["id"], "PORT_PROTOCOL", proto)
        _add_descriptor(builder, port_node["id"], "PORT_SOURCE", "os_probe")
        port_index[key] = port_node["id"]

    return port_index


def apply_os_listens_to(
    builder: GraphBuilder,
    top_os_id: str | None,
    host: dict[str, Any],
    port_index: dict[tuple[str, str], str],
) -> None:
    """06B P3 — top-accuracy OPERATING_SYSTEM listens-to every portused port number."""
    if not top_os_id:
        return
    os_block = host.get("os") or {}
    for entry in os_block.get("portused") or []:
        proto = entry.get("proto") or "tcp"
        portid = str(entry.get("portid") or "")
        port_id = port_index.get((proto, portid))
        if port_id:
            builder.add_edge(top_os_id, port_id, "listens-to")


def apply_trace(
    builder: GraphBuilder,
    scan_id: str,
    host_nodes: dict[str, Any],
    host: dict[str, Any],
) -> None:
    """Trace hop chain under SCAN_RECORD (legacy trace topology)."""
    trace = host.get("trace")
    if not trace:
        return

    host_key = host["host_key"]
    host_id = host_nodes["host"]["id"]
    proto = trace.get("proto", "unknown")
    trace_node = builder.add_node(nugget_node("TRACE", f"{host_key}:{proto}", description="Trace"))
    builder.add_edge(scan_id, trace_node["id"], "contains")
    _add_descriptor(builder, trace_node["id"], "TRACE_PROTOCOL", proto)

    for order, hop in enumerate(trace.get("hops") or [], start=1):
        ipaddr = hop.get("ipaddr")
        if not ipaddr:
            continue
        hop_node = builder.add_node(nugget_node("TRACE_HOP", ipaddr, nugget_type="SUBENTITY"))
        builder.add_edge(trace_node["id"], hop_node["id"], "contains")
        _add_descriptor(builder, hop_node["id"], "HOP_TTL", hop.get("ttl"))
        _add_descriptor(builder, hop_node["id"], "HOP_RTT", hop.get("rtt"))
        _add_descriptor(builder, hop_node["id"], "HOP_ORDER", str(order))

        if ipaddr == host_key:
            hop_host_id = host_id
        else:
            hop_host = apply_host_scan_head(builder, scan_id, {"host_key": ipaddr, "hostnames": [hop["host"]] if hop.get("host") else []})
            hop_host_id = hop_host["host"]["id"]
        builder.add_edge(hop_node["id"], hop_host_id, "contains")


def apply_host_graph(
    builder: GraphBuilder,
    scan_id: str,
    host: dict[str, Any],
) -> None:
    """Apply all 06B host-level hooks for one intermediate host document."""
    host_nodes = apply_host_scan_head(builder, scan_id, host)
    port_index = apply_ports_and_services(builder, host_nodes, host)
    top_os_id = apply_os_matches(builder, host_nodes, host)
    port_index = reconcile_os_probe_ports(builder, host_nodes, host, port_index)
    apply_os_listens_to(builder, top_os_id, host, port_index)
    apply_trace(builder, scan_id, host_nodes, host)


def apply_nmap_hosts(builder: GraphBuilder, scan_id: str, doc: dict[str, Any]) -> None:
    """Entry hook: expand all hosts from one `nmap_scan_v1` document."""
    for host in doc.get("hosts") or []:
        apply_host_graph(builder, scan_id, host)
