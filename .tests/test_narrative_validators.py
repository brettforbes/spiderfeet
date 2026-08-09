"""SPEC-014 BE1 — narrative validators (R14-08)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / ".seed" / "scripts" / "cli_corpus"
if str(CORPUS) not in sys.path:
    sys.path.insert(0, str(CORPUS))

from core.narrative_engine import render_narrative  # noqa: E402
from core.narrative_validators import (  # noqa: E402
    validate_appendix_dedupe,
    validate_example_cap_and_table,
    validate_meta_concept_coverage,
    validate_mermaid_overview_type_only,
    validate_mermaid_shape_cap,
    validate_narrative_report,
)

SAMPLE_GRAPH = {
    "nodes": [
        {"id": "s1", "nugget_id": "SCAN_RECORD", "nugget_data": "scan:demo"},
        {"id": "cli", "nugget_id": "SCAN_CLI", "nugget_data": "demo --json"},
        {"id": "h1", "nugget_id": "HOST", "nugget_data": "scanme.nmap.org"},
        {"id": "net", "nugget_id": "NETWORKS", "nugget_data": "networks:scanme"},
        {"id": "ip1", "nugget_id": "IP_ADDRESS", "nugget_data": "45.33.32.156"},
    ],
    "edges": [
        {"source": "s1", "target": "cli", "relation": "had"},
        {"source": "s1", "target": "h1", "relation": "contains"},
        {"source": "h1", "target": "net", "relation": "contains"},
        {"source": "net", "target": "ip1", "relation": "contains"},
    ],
}


def test_validate_narrative_report_passes_on_engine_output():
    md = render_narrative(SAMPLE_GRAPH, tool="httpx", scenario_key="demo")
    assert validate_narrative_report(SAMPLE_GRAPH, md) == []


def test_validate_meta_concept_coverage_pass_and_fail():
    md = render_narrative(SAMPLE_GRAPH, tool="httpx", scenario_key="demo")
    assert validate_meta_concept_coverage(SAMPLE_GRAPH, md) == []
    broken = md.replace("## Host", "## HostsBroken")
    problems = validate_meta_concept_coverage(SAMPLE_GRAPH, broken)
    assert any("host" in p for p in problems)


def test_validate_mermaid_shape_cap_pass_and_fail():
    good = "```mermaid\nflowchart TD\n  a[\"A\"]\n  b[\"B\"]\n  a -->|r| b\n```\n"
    assert validate_mermaid_shape_cap(good, max_shapes=12) == []
    lines = ["```mermaid", "flowchart TD"]
    for i in range(15):
        lines.append(f'  n{i}["T{i}"]')
    lines.append("```")
    bad = "\n".join(lines)
    problems = validate_mermaid_shape_cap(bad, max_shapes=12)
    assert problems and "15" in problems[0]


def test_validate_mermaid_overview_type_only_pass_and_fail():
    good = (
        "## Host\n\n### Structure overview\n\n"
        "```mermaid\nflowchart TD\n  host[\"HOST\"]\n  net[\"NETWORKS\"]\n  host -->|contains| net\n```\n"
    )
    assert validate_mermaid_overview_type_only(good) == []
    bad = (
        "## Host\n\n### Structure overview\n\n"
        "```mermaid\nflowchart TD\n  host[\"HOST\"]\n  ip[\"45.33.32.156\"]\n  host -->|contains| ip\n```\n"
    )
    assert validate_mermaid_overview_type_only(bad)


def test_validate_example_cap_and_table_pass_and_fail():
    good = (
        "### `NETWORKS`\n\n"
        "```mermaid\nflowchart TD\n  n[\"NETWORKS\"]\n"
        '  a["IP_ADDRESS: 1.1.1.1"]\n  b["IP_ADDRESS: 2.2.2.2"]\n'
        '  c["IP_ADDRESS: 3.3.3.3"]\n  m["+2 more"]\n'
        "  n -->|contains| a\n  n -->|contains| b\n  n -->|contains| c\n  n -->|contains| m\n```\n\n"
        "| Nugget | Value |\n| --- | --- |\n| `IP_ADDRESS` | `1.1.1.1` |\n"
    )
    assert validate_example_cap_and_table(SAMPLE_GRAPH, good, example_cap=3) == []
    bad = (
        "### `NETWORKS`\n\n"
        "```mermaid\nflowchart TD\n  n[\"NETWORKS\"]\n"
        '  a["IP_ADDRESS: 1.1.1.1"]\n  b["IP_ADDRESS: 2.2.2.2"]\n'
        '  c["IP_ADDRESS: 3.3.3.3"]\n  d["IP_ADDRESS: 4.4.4.4"]\n'
        "  n -->|contains| a\n  n -->|contains| b\n  n -->|contains| c\n  n -->|contains| d\n```\n\n"
        "| Nugget | Value |\n| --- | --- |\n| `IP_ADDRESS` | `1.1.1.1` |\n"
    )
    problems = validate_example_cap_and_table(SAMPLE_GRAPH, bad, example_cap=3)
    assert any("without +N more" in p for p in problems)


def test_validate_appendix_dedupe_pass_and_fail():
    good = (
        "## Appendix\n\n### Nodes\n\n| Nugget | Value |\n| --- | --- |\n| `A` | `1` |\n\n"
        "### Edges\n\n| Source | Relation | Target |\n| --- | --- | --- |\n| `A` | `had` | `B` |\n"
    )
    assert validate_appendix_dedupe(good) == []
    bad = good + "\n### Edges\n\n| Source | Relation | Target |\n| --- | --- | --- |\n| `A` | `had` | `B` |\n"
    assert any("repeated" in p for p in validate_appendix_dedupe(bad))
    dup_rows = (
        "## Appendix\n\n### Edges\n\n| Source | Relation | Target |\n| --- | --- | --- |\n"
        "| `A` | `had` | `B` |\n| `A` | `had` | `B` |\n"
    )
    assert any("duplicate" in p for p in validate_appendix_dedupe(dup_rows))


def test_validate_narrative_report_on_live_nmap_fixture():
    path = (
        REPO
        / ".docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_permissive_proposed_nuggets_edges.json"
    )
    if not path.is_file():
        pytest.skip("nmap fixture missing")
    graph = json.loads(path.read_text(encoding="utf-8"))
    md = render_narrative(graph, tool="nmap", scenario_key="tcp_top_ports_permissive")
    assert validate_narrative_report(graph, md) == []
