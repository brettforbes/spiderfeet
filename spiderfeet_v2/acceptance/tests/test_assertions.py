"""Unit checks for R10-30 acceptance assertion helpers."""

from __future__ import annotations

import pytest

from spiderfeet_v2.acceptance.assertions import (
    AcceptanceError,
    assert_graph_invariants,
    assert_no_ip_address_nodes,
    assert_no_orphan_nodes,
    assert_scan_step_artifacts,
)


def test_rejects_ip_address_nugget() -> None:
    graph = {
        "nodes": [{"id": "n1", "nugget_id": "IP_ADDRESS", "nugget_data": "1.2.3.4"}],
        "edges": [],
    }
    with pytest.raises(AcceptanceError, match="IP_ADDRESS"):
        assert_no_ip_address_nodes(graph)


def test_rejects_orphans_when_edges_exist() -> None:
    graph = {
        "nodes": [
            {"id": "a", "nugget_id": "DOMAIN_NAME", "nugget_data": "a.example"},
            {"id": "b", "nugget_id": "DOMAIN_NAME", "nugget_data": "b.example"},
        ],
        "edges": [{"source": "a", "target": "a", "reln": "self"}],
    }
    with pytest.raises(AcceptanceError, match="orphan"):
        assert_no_orphan_nodes(graph)


def test_empty_graph_ok() -> None:
    assert_graph_invariants({"nodes": [], "edges": []})


def test_four_forms_and_graph() -> None:
    step = {
        "scan_instance_id": "scan_step--t",
        "text_form": "host\n",
        "structured_form": "{}",
        "graph_form": '{"nodes":[{"id":"a","nugget_id":"DOMAIN_NAME"}],"edges":[]}',
        "markdown_narrative_form": "# Report\n",
    }
    assert_scan_step_artifacts(step)
