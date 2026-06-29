"""Tests for Netdiscover §4.3 narrative reports."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
GRAPH_PATH = (
    REPO_ROOT
    / ".docs/docs-for-cli-tools/nugget_structure/netdiscover_local_subnet_fast_parsable_proposed_nuggets_edges.json"
)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.path.insert(0, str(CORPUS_DIR))
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_netdiscover_narrative_sections_and_mermaid():
    narrative = _load("narrative_report", CORPUS_DIR / "narrative_report.py")
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    report = narrative.build_netdiscover_narrative_report(graph, "local_subnet_fast_parsable")

    for heading in (
        "## Introduction",
        "## Scan",
        "## System ",
        "### Networks",
        "## Conclusion",
        "## Appendix",
        "OS-Intel Scan",
        "```mermaid",
        "flowchart TD",
        "MAC_VENDOR",
    ):
        assert heading in report


def test_netdiscover_narrative_covers_every_nugget_value():
    narrative = _load("narrative_report", CORPUS_DIR / "narrative_report.py")
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    report = narrative.build_netdiscover_narrative_report(graph, "local_subnet_fast_parsable")
    ok, missing = narrative.validate_narrative_coverage(graph, report)
    assert ok, f"missing values: {missing[:10]}"
