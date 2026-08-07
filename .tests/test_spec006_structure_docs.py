"""SPEC-006 governance tests — Structure docs for all ADAPTER_TOOLS."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
STRUCTURE_DIR = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
ONTOLOGY_PATH = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "_Current_Ontology.md"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.structure_doc_engine import (  # noqa: E402
    ADAPTER_TOOLS,
    required_headings_present,
    validate_mermaid_purity,
)

REQUIRED_TOOLS = ADAPTER_TOOLS


@pytest.mark.parametrize("tool_id", REQUIRED_TOOLS)
def test_structure_md_exists_on_disk(tool_id: str):
    path = STRUCTURE_DIR / f"{tool_id}_nugget_graph_structure.md"
    assert path.is_file(), f"missing structure doc for {tool_id}"


@pytest.mark.parametrize("tool_id", REQUIRED_TOOLS)
def test_structure_yaml_exists(tool_id: str):
    path = CLI_CORPUS / "rules" / tool_id / "structure.yaml"
    assert path.is_file(), f"missing rules/{tool_id}/structure.yaml"


@pytest.mark.parametrize("tool_id", REQUIRED_TOOLS)
def test_structure_md_required_headings(tool_id: str):
    md = (STRUCTURE_DIR / f"{tool_id}_nugget_graph_structure.md").read_text(encoding="utf-8")
    missing = required_headings_present(md)
    assert not missing, f"{tool_id} missing headings: {missing}"


@pytest.mark.parametrize("tool_id", REQUIRED_TOOLS)
def test_structure_md_has_mermaid_fence(tool_id: str):
    md = (STRUCTURE_DIR / f"{tool_id}_nugget_graph_structure.md").read_text(encoding="utf-8")
    assert "```mermaid" in md


@pytest.mark.parametrize("tool_id", REQUIRED_TOOLS)
def test_structure_md_mermaid_purity(tool_id: str):
    md = (STRUCTURE_DIR / f"{tool_id}_nugget_graph_structure.md").read_text(encoding="utf-8")
    violations = validate_mermaid_purity(md)
    assert not violations, f"{tool_id}: {violations[:5]}"


def test_katana_and_nuclei_structure_docs_present():
    for tool_id in ("katana", "nuclei"):
        assert (STRUCTURE_DIR / f"{tool_id}_nugget_graph_structure.md").is_file()


def test_current_ontology_doc_exists():
    assert ONTOLOGY_PATH.is_file()


def test_current_ontology_lists_eight_tools():
    md = ONTOLOGY_PATH.read_text(encoding="utf-8")
    for tool_id in REQUIRED_TOOLS:
        assert f"{tool_id}_nugget_graph_structure.md" in md
