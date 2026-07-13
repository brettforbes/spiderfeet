"""Q2 — GSE select + where on subfinder corpus."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".seed" / "scripts"
NUGGET = ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.gse_eval import eval_binding, eval_select  # noqa: E402


@pytest.fixture
def subfinder_graph():
    path = NUGGET / "subfinder_corporate_upside_au_passive_cs_proposed_nuggets_edges.json"
    if not path.is_file():
        pytest.skip("fixture missing")
    return json.loads(path.read_text(encoding="utf-8"))


def test_apex_and_subdomains_disjoint(subfinder_graph):
    apex = eval_select(
        {
            "source": "$step.scan_graph",
            "nodes": {
                "nugget_id": "DOMAIN_NAME",
                "where": [
                    {
                        "not": {
                            "related": {
                                "direction": "out",
                                "relation": "had",
                                "nugget_id": "DOMAIN_NAME_PARENT",
                            }
                        }
                    }
                ],
            },
            "project": "nugget_data",
            "distinct": True,
        },
        subfinder_graph,
    )
    subs = eval_select(
        {
            "source": "$step.scan_graph",
            "nodes": {
                "nugget_id": "DOMAIN_NAME",
                "where": [
                    {
                        "related": {
                            "direction": "out",
                            "relation": "had",
                            "nugget_id": "DOMAIN_NAME_PARENT",
                        }
                    }
                ],
            },
            "project": "nugget_data",
            "distinct": True,
        },
        subfinder_graph,
    )
    assert subs
    assert set(apex).isdisjoint(subs)
    merged = eval_binding(
        {"type": "string_list", "union": ["a", "b"], "distinct": True},
        env_lists={"a": apex, "b": subs},
    )
    assert set(merged) == set(apex) | set(subs)
