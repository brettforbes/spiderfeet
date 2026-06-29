"""Tests for NetDiscover text→JSON and JSON→graph converters."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

CORPUS_DIR = Path(__file__).resolve().parents[1] / ".seed" / "scripts" / "cli_corpus"
import sys

sys.path.insert(0, str(CORPUS_DIR))

from netdiscover_json_to_graph import netdiscover_scan_to_graph
from netdiscover_text_to_json import (
    convert_text_to_netdiscover_scan,
    dumps_netdiscover_scan,
    validate_netdiscover_scan,
)

PARSABLE_SAMPLE = """ 192.168.1.1     14:5f:94:d8:7a:5f      1      42  HUAWEI TECHNOLOGIES CO.,LTD
 192.168.1.16    88:f4:da:1a:b7:65      1      42  Unknown vendor
 192.168.1.2     a8:51:ab:23:c6:49      1      42  Apple, Inc.

-- Active scan completed, 3 Hosts found.
"""


def test_parsable_text_becomes_valid_json():
    doc = convert_text_to_netdiscover_scan(
        PARSABLE_SAMPLE,
        scenario_name="A — active ARP scan 192.168.1.0/24 (parseable)",
        output_mode="parsable",
        start_time=datetime(2026, 6, 23, 19, 6, 27, tzinfo=timezone.utc),
        duration_s=0.42,
        exit_code=0,
    )
    assert validate_netdiscover_scan(doc) == []
    scan = doc["netdiscover_scan"]
    assert scan["scanner"] == "netdiscover"
    assert scan["args"].startswith("netdiscover")
    assert len(scan["systems"]) == 3
    assert scan["runstats"]["systems"]["discovered"] == 3
    payload = dumps_netdiscover_scan(doc)
    assert payload.lstrip().startswith("{")
    assert "HUAWEI TECHNOLOGIES CO.,LTD" in payload


def test_empty_scan_still_has_scan_record():
    doc = convert_text_to_netdiscover_scan(
        "pcap_open_live(): eth1: No such device exists",
        scenario_name="A — active ARP scan 192.168.1.0/24 (parseable)",
        output_mode="parsable",
        start_time=datetime.now(timezone.utc),
        duration_s=1.0,
        exit_code=1,
    )
    assert doc["netdiscover_scan"]["systems"] == []
    graph = netdiscover_scan_to_graph(doc)
    assert any(node["nugget_id"] == "SCAN_RECORD" for node in graph["nodes"])
