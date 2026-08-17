"""SPEC-019 R19-02 — topology parent_id wiring."""

from __future__ import annotations

from modules_v2._core.graph_builder import GraphBuilder, nugget_node
from modules_v2._core.topology import add_host_networks_port_service, add_scan_head


def test_two_hosts_distinct_transport_per_host() -> None:
    builder = GraphBuilder()
    scan = add_scan_head(builder, "nmap:two-hosts")
    scan_id = scan["id"]

    first = add_host_networks_port_service(
        builder,
        scan_id,
        host="10.0.0.1",
        ip_address="10.0.0.1",
        transport="tcp",
        port=22,
        service="ssh",
    )
    second = add_host_networks_port_service(
        builder,
        scan_id,
        host="10.0.0.2",
        ip_address="10.0.0.2",
        transport="tcp",
        port=22,
        service="ssh",
    )

    assert first["transport"]["id"] != second["transport"]["id"]
    assert first["port"]["id"] != second["port"]["id"]


def test_same_host_reuses_transport_and_port() -> None:
    builder = GraphBuilder()
    scan = add_scan_head(builder, "nmap:reuse")
    scan_id = scan["id"]

    first = add_host_networks_port_service(
        builder,
        scan_id,
        host="10.0.0.1",
        ip_address="10.0.0.1",
        transport="tcp",
        port=22,
        service="ssh",
    )
    transport_again = builder.add_node(
        nugget_node("TRANSPORT", "tcp", description="Transport Protocol"),
        parent_id=first["networks"]["id"],
    )
    port_again = builder.add_node(
        nugget_node("PORT", "22", nugget_type="SUBENTITY", description="Network Port"),
        parent_id=first["transport"]["id"],
    )

    assert transport_again["id"] == first["transport"]["id"]
    assert port_again["id"] == first["port"]["id"]
