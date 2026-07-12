"""Unit tests for SPEC-006 structure_doc_engine."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.structure_doc_engine import (  # noqa: E402
    ADAPTER_TOOLS,
    load_shared_structure_patterns,
    load_tool_structure_pack,
    render_mermaid_from_pattern,
    render_ontology_doc,
    render_tool_structure_doc,
    validate_mermaid_purity,
)

REQUIRED_PATTERN_IDS = (
    "scan_head",
    "system_l2",
    "host_networks_port_service",
    "trace_hop_chain",
    "host_status",
    "os_environment",
    "ssh_host_keys",
    "domain_apex",
    "org_company_tree",
    "web_url_probe",
    "crawl_url_tree",
    "vuln_findings",
)


def test_structure_v1_loads_required_patterns():
    patterns = load_shared_structure_patterns()
    for pattern_id in REQUIRED_PATTERN_IDS:
        assert pattern_id in patterns, f"missing shared pattern {pattern_id}"
        edges = patterns[pattern_id].get("edges") or []
        assert edges, f"pattern {pattern_id} has no edges"


def test_structure_v1_yaml_file_exists():
    path = CLI_CORPUS / "rules" / "_shared" / "structure_v1.yaml"
    assert path.is_file()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert "patterns" in data


@pytest.mark.parametrize("tool_id", ADAPTER_TOOLS)
def test_tool_structure_pack_loads(tool_id: str):
    pack = load_tool_structure_pack(tool_id)
    assert pack.get("tool") == tool_id
    assert pack.get("display_name")
    assert pack.get("patterns")
    assert pack.get("scenarios")
    assert pack.get("field_mapping")


@pytest.mark.parametrize("tool_id", ADAPTER_TOOLS)
def test_render_tool_structure_doc_sections(tool_id: str):
    md = render_tool_structure_doc(tool_id)
    assert f"# {load_tool_structure_pack(tool_id)['display_name']} — proposed nugget graph structure" in md
    assert "## Scan head" in md
    assert "## Scenario coverage" in md
    assert "Field mapping" in md
    assert "## Review notes" in md
    assert "```mermaid" in md
    assert "../_Current_Ontology.md" in md


@pytest.mark.parametrize("tool_id", ADAPTER_TOOLS)
def test_rendered_mermaid_has_no_value_literals(tool_id: str):
    violations = validate_mermaid_purity(render_tool_structure_doc(tool_id))
    assert not violations, f"{tool_id} mermaid violations: {violations[:3]}"


def test_render_mermaid_from_pattern_rejects_value_labels():
    pattern = {
        "edges": [
            {"source": "HOST", "relation": "contains", "target": "IP_ADDRESS", "target_label": "192.168.1.1"},
        ]
    }
    with pytest.raises(ValueError, match="type-only"):
        render_mermaid_from_pattern(pattern)


def test_render_ontology_doc_lists_all_tools():
    md = render_ontology_doc()
    assert "# Current CLI Profiling Ontology" in md
    for tool_id in ADAPTER_TOOLS:
        assert f"{tool_id}_nugget_graph_structure.md" in md
    assert "## Sub-graph:" in md
    violations = validate_mermaid_purity(md)
    assert not violations
