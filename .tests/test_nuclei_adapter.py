"""Tests for the SPEC-004 Nuclei structured-native adapter (D5)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"
FIXTURES = CLI_CORPUS / "fixtures"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import nuclei
from core.graph_builder import validate_graph
from core.rule_engine import load_rule_pack
from nuclei_structured import build_nuclei_bundle, parse_ndjson


def _load_fixture(name: str) -> list[dict]:
    raw = (FIXTURES / name).read_text(encoding="utf-8")
    return parse_ndjson(raw)


def _nuclei_bundle(records: list[dict], *, target: str = "example.com") -> dict:
    return build_nuclei_bundle(
        records,
        {
            "tool": "nuclei",
            "target": target,
            "command": "nuclei -u https://example.com -silent -jsonl",
            "started_at": "2026-06-15T10:00:00+00:00",
            "duration_s": 2.5,
            "exit_code": 0,
            "scan_data": f"nuclei:{target}:nuclei -u https://example.com -silent -jsonl",
        },
    )


def test_nuclei_rule_pack_loads_as_structured_native():
    rule_pack = load_rule_pack(RULES / "nuclei" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "nuclei"
    assert rule_pack.capture_family == "structured_native"


def test_nuclei_adapter_builds_four_outputs():
    bundle = _nuclei_bundle(_load_fixture("nuclei_cve_critical_sample.jsonl"))
    outputs = nuclei.build_outputs(bundle, scenario_key="cve_critical_sample")

    assert "CVE-2021-44228" in outputs["text"]
    assert outputs["structured"]["schema"] == "nuclei_finding_v1"
    validate_graph(outputs["graph"])
    assert "## Appendix" in outputs["markdown_report"]


def test_nuclei_adapter_preserves_security_finding_hierarchy():
    records = _load_fixture("nuclei_cve_critical_sample.jsonl") + _load_fixture(
        "nuclei_vuln_medium_sample.jsonl"
    )
    graph = nuclei.to_graph(_nuclei_bundle(records))
    nodes = graph["nodes"]

    assert any(n["nugget_id"] == "HOST" and n["nugget_data"] == "app.example.com" for n in nodes)
    assert any(n["nugget_id"] == "HOST" and n["nugget_data"] == "admin.example.com" for n in nodes)
    assert any(n["nugget_id"] == "SECURITY" for n in nodes)
    assert any(n["nugget_id"] == "FINDINGS" for n in nodes)
    assert any(n["nugget_id"] == "TEMPLATES_USED" for n in nodes)
    assert any(n["nugget_id"] == "NUCLEI_SEVERITY_CRITICAL" for n in nodes)
    assert any(n["nugget_id"] == "NUCLEI_SEVERITY_MEDIUM" for n in nodes)
    assert any(n["nugget_id"] == "NUCLEI_TEMPLATE" and n["nugget_data"] == "CVE-2021-44228" for n in nodes)
    assert any(n["nugget_id"] == "NUCLEI_TEMPLATE" and n["nugget_data"] == "exposed-panel" for n in nodes)
    assert any(n["nugget_id"] == "NUCLEI_FINDING" for n in nodes)
    assert any(n["nugget_id"] == "NUCLEI_VULNERABILITY" for n in nodes)
    assert any(n["nugget_id"] == "VULNERABILITY_CVE_CRITICAL" and "CVE-2021-44228" in n["nugget_data"] for n in nodes)


def test_nuclei_converter_delegates_to_adapter():
    from nuclei_json_to_graph import nuclei_to_graph

    raw = json.dumps(_nuclei_bundle(_load_fixture("nuclei_vuln_medium_sample.jsonl")))
    graph = nuclei_to_graph(raw, "admin.example.com", "nuclei -u https://admin.example.com -silent -jsonl")

    assert any(n["nugget_id"] == "NUCLEI_FINDING" for n in graph["nodes"])
    validate_graph(graph)
