"""Tests for the SPEC-004 Netdiscover adapter."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import netdiscover
from core.graph_builder import validate_graph
from core.rule_engine import load_rule_pack

PARSABLE_SAMPLE = """ 192.168.1.1     14:5f:94:d8:7a:5f      1      42  HUAWEI TECHNOLOGIES CO.,LTD
 192.168.1.16    88:f4:da:1a:b7:65      1      42  Unknown vendor
 192.168.1.2     a8:51:ab:23:c6:49      1      42  Apple, Inc.

-- Active scan completed, 3 Hosts found.
"""


def test_netdiscover_rule_pack_loads_as_text_native():
    rule_pack = load_rule_pack(RULES / "netdiscover" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "netdiscover"
    assert rule_pack.capture_family == "text_native"
    assert "system_l2" in rule_pack.scan_head.get("topology_templates", []) or (
        "topology_templates" in rule_pack.shared
    )


def test_netdiscover_adapter_builds_four_outputs():
    outputs = netdiscover.build_outputs(
        PARSABLE_SAMPLE,
        scenario_name="A - active ARP scan 192.168.1.0/24 (parseable)",
        scenario_key="adapter_parsable",
        output_mode="parsable",
        start_time=datetime(2026, 6, 23, 19, 6, 27, tzinfo=timezone.utc),
        duration_s=0.42,
        exit_code=0,
    )

    assert outputs["text"] == PARSABLE_SAMPLE
    assert outputs["structured"]["netdiscover_scan"]["systems"]
    assert outputs["structured_json"].lstrip().startswith("{")
    validate_graph(outputs["graph"])
    assert any(node["nugget_id"] == "SYSTEM" for node in outputs["graph"]["nodes"])
    assert any(edge["relation"] == "contains" for edge in outputs["graph"]["edges"])
    assert "## Appendix" in outputs["markdown_report"]
