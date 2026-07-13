"""S2 — context merge tests."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".seed" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.context_export import merge_graph  # noqa: E402


def test_merge_graph_deduplicates_nodes_and_edges():
    ctx: dict = {"nodes": [], "edges": []}
    g = {
        "nodes": [{"id": "A", "nugget_id": "HOST", "nugget_data": "h"}],
        "edges": [{"source": "A", "target": "B", "relation": "contains"}],
    }
    merge_graph(ctx, g)
    merge_graph(ctx, g)
    assert len(ctx["nodes"]) == 1
    assert len(ctx["edges"]) == 1
