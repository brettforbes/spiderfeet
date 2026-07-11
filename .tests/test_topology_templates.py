"""Tests for SPEC-004 shared topology templates."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.graph_builder import GraphBuilder
from core.topology import (
    add_host_networks_port_service,
    add_scan_head,
    add_system_l2,
    add_trace_hop_chain,
)

ALLOWED_RELATIONS = {"contains", "had", "listens-to"}


def _edge_pairs(graph):
    nodes = {node["id"]: node for node in graph["nodes"]}
    return {
        (
            nodes[edge["source"]]["nugget_id"],
            edge["relation"],
            nodes[edge["target"]]["nugget_id"],
        )
        for edge in graph["edges"]
    }


def test_system_l2_template_edges():
    builder = GraphBuilder()
    scan = add_scan_head(builder, "netdiscover test", command="netdiscover -P")
    add_system_l2(
        builder,
        scan["id"],
        system="172.18.0.1",
        ip_address="172.18.0.1",
        mac_address="00:15:5d:c1:a8:4a",
        mac_vendor="Microsoft Corporation",
    )

    graph = builder.build()
    pairs = _edge_pairs(graph)

    assert ("SCAN_RECORD", "contains", "SYSTEM") in pairs
    assert ("SYSTEM", "contains", "NETWORKS") in pairs
    assert ("NETWORKS", "contains", "IP_ADDRESS") in pairs
    assert ("NETWORKS", "contains", "MAC_ADDRESS") in pairs
    assert ("MAC_ADDRESS", "had", "MAC_VENDOR") in pairs
    assert {edge["relation"] for edge in graph["edges"]} <= ALLOWED_RELATIONS


def test_host_networks_port_service_template_edges():
    builder = GraphBuilder()
    scan = add_scan_head(builder, "nerva test", command="nerva --json")
    add_host_networks_port_service(
        builder,
        scan["id"],
        host="scanme.nmap.org",
        ip_address="45.33.32.156",
        transport="tcp",
        port=80,
        service="http",
    )

    graph = builder.build()
    pairs = _edge_pairs(graph)

    assert ("SCAN_RECORD", "contains", "HOST") in pairs
    assert ("HOST", "contains", "NETWORKS") in pairs
    assert ("NETWORKS", "contains", "IP_ADDRESS") in pairs
    assert ("NETWORKS", "contains", "TRANSPORT") in pairs
    assert ("TRANSPORT", "contains", "PORT") in pairs
    assert ("PORT", "had", "PORT_PROTOCOL") in pairs
    assert ("HOST", "contains", "APPLICATIONS") in pairs
    assert ("APPLICATIONS", "contains", "SERVICE") in pairs
    assert ("SERVICE", "listens-to", "PORT") in pairs
    assert {edge["relation"] for edge in graph["edges"]} <= ALLOWED_RELATIONS


def test_trace_hop_chain_template_edges():
    builder = GraphBuilder()
    scan = add_scan_head(builder, "nmap trace", command="nmap -A -oX -")
    add_trace_hop_chain(
        builder,
        scan["id"],
        trace="trace:scanme.nmap.org",
        hops=[
            {"order": 1, "ttl": 1, "rtt": "1.23", "ip": "192.0.2.1"},
            {"order": 2, "ttl": 2, "rtt": "8.90", "ip": "45.33.32.156"},
        ],
    )

    graph = builder.build()
    pairs = _edge_pairs(graph)

    assert ("SCAN_RECORD", "contains", "TRACE") in pairs
    assert ("TRACE", "contains", "TRACE_HOP") in pairs
    assert ("TRACE_HOP", "had", "HOP_ORDER") in pairs
    assert ("TRACE_HOP", "had", "HOP_TTL") in pairs
    assert ("TRACE_HOP", "had", "HOP_RTT") in pairs
    assert {edge["relation"] for edge in graph["edges"]} <= ALLOWED_RELATIONS
