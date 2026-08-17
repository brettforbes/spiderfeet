"""SPEC-019 R19-01 — uuid4 occurrence identity and parent-scoped cache."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from modules_v2._core.graph_builder import (
    GraphBuilder,
    nugget_instance_id,
    nugget_node,
    uses_uuid4_identity,
    validate_graph,
)
from spiderfeet_v2.engine.persist import _persist_scan_result_graph


def test_uuid4_types_use_occurrence_identity() -> None:
    assert uses_uuid4_identity("ENTITY")
    assert uses_uuid4_identity("SUBENTITY")
    assert not uses_uuid4_identity("DESCRIPTOR")

    a = nugget_instance_id("HOST", "10.0.0.1", nugget_type="ENTITY")
    b = nugget_instance_id("HOST", "10.0.0.1", nugget_type="ENTITY")
    assert a != b
    assert a.startswith("HOST--")
    assert b.startswith("HOST--")


def test_descriptor_stays_uuid5_unique_by_value() -> None:
    a = nugget_instance_id("PORT_STATE", "open", nugget_type="DESCRIPTOR")
    b = nugget_instance_id("PORT_STATE", "open", nugget_type="DESCRIPTOR")
    assert a == b


def test_two_hosts_two_ports_same_value() -> None:
    builder = GraphBuilder()
    scan = builder.add_node(nugget_node("SCAN_RECORD", "scan:test"))
    builder.add_edge(scan["id"], scan["id"], "had")  # connect scan (self-loop for validate)

    host_a = builder.add_node(nugget_node("HOST", "10.0.0.1"), parent_id=scan["id"])
    host_b = builder.add_node(nugget_node("HOST", "10.0.0.2"), parent_id=scan["id"])
    builder.add_edge(scan["id"], host_a["id"], "contains")
    builder.add_edge(scan["id"], host_b["id"], "contains")

    port_a = builder.add_node(
        nugget_node("PORT", "22", nugget_type="SUBENTITY"),
        parent_id=host_a["id"],
    )
    port_b = builder.add_node(
        nugget_node("PORT", "22", nugget_type="SUBENTITY"),
        parent_id=host_b["id"],
    )
    builder.add_edge(host_a["id"], port_a["id"], "contains")
    builder.add_edge(host_b["id"], port_b["id"], "contains")

    state = builder.add_node(nugget_node("PORT_STATE", "open", nugget_type="DESCRIPTOR"))
    builder.add_edge(port_a["id"], state["id"], "had")
    builder.add_edge(port_b["id"], state["id"], "had")

    graph = builder.build()
    ports = [n for n in graph["nodes"] if n["nugget_id"] == "PORT"]
    states = [n for n in graph["nodes"] if n["nugget_id"] == "PORT_STATE"]
    assert len(ports) == 2
    assert ports[0]["id"] != ports[1]["id"]
    assert len(states) == 1


def test_parent_cache_reuses_same_parent_value() -> None:
    builder = GraphBuilder()
    scan = builder.add_node(nugget_node("SCAN_RECORD", "scan:cache"))
    builder.add_edge(scan["id"], scan["id"], "had")
    host = builder.add_node(nugget_node("HOST", "10.0.0.1"), parent_id=scan["id"])
    builder.add_edge(scan["id"], host["id"], "contains")

    transport_a = builder.add_node(
        nugget_node("TRANSPORT", "tcp"),
        parent_id=host["id"],
    )
    transport_b = builder.add_node(
        nugget_node("TRANSPORT", "tcp"),
        parent_id=host["id"],
    )
    builder.add_edge(host["id"], transport_a["id"], "contains")

    assert transport_a["id"] == transport_b["id"]


def test_validate_graph_allows_duplicate_uuid4_pairs() -> None:
    graph = {
        "nodes": [
            {
                "id": "TRANSPORT--11111111-1111-4111-8111-111111111111",
                "nugget_id": "TRANSPORT",
                "nugget_type": "ENTITY",
                "nugget_data": "tcp",
            },
            {
                "id": "TRANSPORT--22222222-2222-4222-8222-222222222222",
                "nugget_id": "TRANSPORT",
                "nugget_type": "ENTITY",
                "nugget_data": "tcp",
            },
            {
                "id": "HOST--33333333-3333-4333-8333-333333333333",
                "nugget_id": "HOST",
                "nugget_type": "ENTITY",
                "nugget_data": "h1",
            },
        ],
        "edges": [
            {
                "source": "HOST--33333333-3333-4333-8333-333333333333",
                "target": "TRANSPORT--11111111-1111-4111-8111-111111111111",
                "relation": "contains",
            },
            {
                "source": "HOST--33333333-3333-4333-8333-333333333333",
                "target": "TRANSPORT--22222222-2222-4222-8222-222222222222",
                "relation": "contains",
            },
        ],
    }
    validate_graph(graph)


def test_validate_graph_rejects_duplicate_descriptor_pairs() -> None:
    graph = {
        "nodes": [
            {
                "id": "PORT_STATE--aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "nugget_id": "PORT_STATE",
                "nugget_type": "DESCRIPTOR",
                "nugget_data": "open",
            },
            {
                "id": "PORT_STATE--ffffffff-ffff-ffff-ffff-ffffffffffff",
                "nugget_id": "PORT_STATE",
                "nugget_type": "DESCRIPTOR",
                "nugget_data": "open",
            },
            {
                "id": "PORT--11111111-1111-4111-8111-111111111111",
                "nugget_id": "PORT",
                "nugget_type": "SUBENTITY",
                "nugget_data": "22",
            },
        ],
        "edges": [
            {
                "source": "PORT--11111111-1111-4111-8111-111111111111",
                "target": "PORT_STATE--aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "relation": "had",
            },
            {
                "source": "PORT--11111111-1111-4111-8111-111111111111",
                "target": "PORT_STATE--ffffffff-ffff-ffff-ffff-ffffffffffff",
                "relation": "had",
            },
        ],
    }
    with pytest.raises(ValueError, match="duplicate nugget_id\\+data"):
        validate_graph(graph)


def test_persist_stores_graph_as_emitted() -> None:
    """R19-01: persist must not re-collapse uuid4 nodes by value."""
    store = MagicMock()
    store.get_subgraph.return_value = None
    graph = {
        "nodes": [
            {"id": "PORT--a", "nugget_id": "PORT", "nugget_type": "SUBENTITY", "nugget_data": "22"},
            {"id": "PORT--b", "nugget_id": "PORT", "nugget_type": "SUBENTITY", "nugget_data": "22"},
        ],
        "edges": [],
    }
    _persist_scan_result_graph(
        store,
        scan_instance_id="scan-1",
        scan_result_id="result-1",
        graph=graph,
    )
    store.create_subgraph.assert_called_once()
    stored = store.create_subgraph.call_args[0][0]["graph"]
    assert stored == graph
    assert len(stored["nodes"]) == 2
