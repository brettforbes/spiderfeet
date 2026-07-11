"""Tests for the SPEC-004 YAML rule engine."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
SHARED_RULES = CLI_CORPUS / "rules" / "_shared"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.rule_engine import RuleEngine, RulePackError, load_rule_pack


def test_invalid_rule_pack_fails(tmp_path):
    mapping = tmp_path / "mapping.yaml"
    mapping.write_text(
        """
tool: broken
capture_family: structured_native
mappings:
  - path: target
    nugget_id: LINKED_URL_INTERNAL
    relation: redirects-to
""".lstrip(),
        encoding="utf-8",
    )

    with pytest.raises(RulePackError, match="unsupported relation"):
        load_rule_pack(mapping, shared_dir=SHARED_RULES)


def test_minimal_rule_pack_loads_shared_rules_and_creates_scan_record(tmp_path):
    mapping = tmp_path / "mapping.yaml"
    mapping.write_text(
        """
tool: minimal
capture_family: structured_native
scan_head:
  data_path: meta.command
  fallback: minimal scan
mappings:
  - path: meta.target
    nugget_id: SCAN_TARGET
    relation: had
""".lstrip(),
        encoding="utf-8",
    )

    rule_pack = load_rule_pack(mapping, shared_dir=SHARED_RULES)
    graph = RuleEngine(rule_pack).build_graph(
        {
            "command": "minimal --json",
            "meta": {
                "command": "minimal scan",
                "target": "example.com",
            },
        }
    )

    assert {"relations", "scan_head", "categories", "identity", "validation", "four_outputs"} <= (
        set(rule_pack.shared)
    )
    nodes = graph["nodes"]
    edges = graph["edges"]
    assert any(
        node["nugget_id"] == "SCAN_RECORD" and node["nugget_data"] == "minimal scan"
        for node in nodes
    )
    assert any(
        node["nugget_id"] == "SCAN_TARGET" and node["nugget_data"] == "example.com"
        for node in nodes
    )
    assert edges
