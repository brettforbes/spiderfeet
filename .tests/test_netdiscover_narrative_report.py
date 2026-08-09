"""Tests for Netdiscover §4.3 narrative reports via shared engine (SPEC-014)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
GRAPH_PATH = (
    REPO_ROOT
    / ".docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_fast_parsable_proposed_nuggets_edges.json"
)

if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

from core.narrative_engine import render_narrative  # noqa: E402
from narrative_report import validate_narrative_coverage  # noqa: E402


def test_netdiscover_narrative_sections_and_mermaid():
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    report = render_narrative(graph, tool="netdiscover", scenario_key="local_subnet_fast_parsable")

    for heading in (
        "## Introduction",
        "## Scan",
        "## System",
        "### `NETWORKS`",
        "## Conclusion",
        "## Appendix",
        "OS-Intel Scan",
        "```mermaid",
        "flowchart TD",
        "MAC_VENDOR",
    ):
        assert heading in report


def test_netdiscover_narrative_covers_every_nugget_value():
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    report = render_narrative(graph, tool="netdiscover", scenario_key="local_subnet_fast_parsable")
    ok, missing = validate_narrative_coverage(graph, report)
    assert ok, f"missing values: {missing[:10]}"
