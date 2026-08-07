"""P2 / Q1 — graph_index unit tests."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".seed" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.graph_index import GraphIndex  # noqa: E402


def _five_node_graph():
    return {
        "nodes": [
            {"id": "H1", "nugget_id": "HOST", "nugget_data": "host1"},
            {"id": "N1", "nugget_id": "NETWORKS", "nugget_data": "net"},
            {"id": "IP1", "nugget_id": "IP_ADDRESS", "nugget_data": "10.0.0.1"},
            {"id": "T1", "nugget_id": "TRANSPORT", "nugget_data": "tcp"},
            {"id": "P1", "nugget_id": "PORT", "nugget_data": "443"},
        ],
        "edges": [
            {"source": "H1", "target": "N1", "relation": "contains"},
            {"source": "N1", "target": "IP1", "relation": "contains"},
            {"source": "H1", "target": "T1", "relation": "contains"},
            {"source": "T1", "target": "P1", "relation": "contains"},
        ],
    }


def test_reachable_non_transitive_only_direct():
    idx = GraphIndex(_five_node_graph())
    direct = idx.reachable("H1", "contains", transitive=False)
    assert direct == {"N1", "T1"}


def test_reachable_transitive_includes_ip_and_port():
    idx = GraphIndex(_five_node_graph())
    all_reach = idx.reachable("H1", "contains", transitive=True)
    assert {"N1", "IP1", "T1", "P1"}.issubset(all_reach)


def test_neighbors_out_and_in():
    idx = GraphIndex(_five_node_graph())
    assert idx.neighbors("H1", "contains", "out") == ["N1", "T1"]
    assert idx.neighbors("IP1", "contains", "in") == ["N1"]
