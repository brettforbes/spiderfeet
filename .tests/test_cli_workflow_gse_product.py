"""Q3 — GSE for_each product ip:port on nmap corpus."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".seed" / "scripts"
NUGGET = ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.gse_eval import eval_select  # noqa: E402


def test_nmap_ip_port_product():
    path = NUGGET / "nmap_tcp_top_ports_permissive_proposed_nuggets_edges.json"
    if not path.is_file():
        pytest.skip("fixture missing")
    graph = json.loads(path.read_text(encoding="utf-8"))
    values = eval_select(
        {
            "source": "$step.scan_graph",
            "for_each": {
                "as": "endpoint",
                "nodes": {"nugget_id_in": ["HOST", "SYSTEM", "DEVICE", "CDN", "SERVER"]},
                "collect": [
                    {
                        "as": "ip",
                        "reachable_from": "endpoint",
                        "along": {"relation": "contains", "transitive": True},
                        "nodes": {"nugget_id_in": ["IPV4_ADDRESS", "IPV6_ADDRESS"]},
                        "project": "nugget_data",
                    },
                    {
                        "as": "port",
                        "reachable_from": "endpoint",
                        "along": {"relation": "contains", "transitive": True},
                        "nodes": {"nugget_id": "PORT"},
                        "project": "nugget_data",
                    },
                ],
                "emit": {"product": ["ip", "port"], "join": ":"},
            },
            "distinct": True,
        },
        graph,
    )
    assert values
    assert all(v.count(":") == 1 for v in values)
