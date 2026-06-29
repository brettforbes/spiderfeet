"""Tests for NetDiscover text→JSON and JSON→graph converters."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

CORPUS_DIR = Path(__file__).resolve().parents[1] / ".seed" / "scripts" / "cli_corpus"
import sys

sys.path.insert(0, str(CORPUS_DIR))

from graph_builder import validate_graph_connectivity
from netdiscover_json_to_graph import netdiscover_scan_to_graph
from netdiscover_text_to_json import (
    convert_text_to_netdiscover_scan,
    dumps_netdiscover_scan,
    parse_interactive_body,
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
    assert scan["exit_status"] == "success"
    assert scan["runstats"]["finished_time"]["exit_status"] == "success"
    payload = dumps_netdiscover_scan(doc)
    assert payload.lstrip().startswith("{")
    assert "HUAWEI TECHNOLOGIES CO.,LTD" in payload


def test_interactive_tui_frame_counts():
    """Issue 4 from 06A: 5 TUI frames, 3 empty, first populated table kept."""
    raw = """
Currently scanning: Starting.   |   Screen View: Unique Hosts
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0
 -----------------------------------------------------------------------------
Currently scanning: Starting.   |   Screen View: Unique Hosts
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0
 -----------------------------------------------------------------------------
Currently scanning: 192.168.1.0/24   |   Screen View: Unique Hosts
 0 Captured ARP Req/Rep packets, from 0 hosts.   Total size: 0
 -----------------------------------------------------------------------------
Currently scanning: 192.168.1.0/24   |   Screen View: Unique Hosts
 12 Captured ARP Req/Rep packets, from 8 hosts.   Total size: 504
 192.168.1.1     14:5f:94:d8:7a:5f      1      42  HUAWEI TECHNOLOGIES CO.,LTD
 192.168.1.2     a8:51:ab:23:c6:49      1      42  Apple, Inc.
Currently scanning: 192.168.1.0/24   |   Screen View: Unique Hosts
 18 Captured ARP Req/Rep packets, from 9 hosts.   Total size: 756
 192.168.1.1     14:5f:94:d8:7a:5f      1      42  HUAWEI TECHNOLOGIES CO.,LTD
"""
    doc = convert_text_to_netdiscover_scan(
        raw,
        scenario_name="A — active ARP scan 192.168.1.0/24 (parseable)",
        output_mode="parsable",
        start_time=datetime(2026, 6, 23, 19, 6, 27, tzinfo=timezone.utc),
        duration_s=0.42,
        exit_code=0,
    )
    stats = doc["netdiscover_scan"]["runstats"]["systems"]
    assert stats["scan_tries"] == 5
    assert stats["empty_scans"] == 3
    assert stats["discovered"] == 2
    assert len(doc["netdiscover_scan"]["systems"]) == 2


def test_networks_nodes_are_category():
    doc = convert_text_to_netdiscover_scan(
        PARSABLE_SAMPLE,
        scenario_name="parsable",
        output_mode="parsable",
        start_time=datetime.now(timezone.utc),
        duration_s=1.0,
        exit_code=0,
    )
    graph = netdiscover_scan_to_graph(doc)
    networks = [n for n in graph["nodes"] if n["nugget_id"] == "NETWORKS"]
    assert networks
    assert all(n["nugget_type"] == "CATEGORY" for n in networks)
    assert all(n.get("nugget_colour") == "#14B8A6" for n in networks)


def test_shared_mac_vendor_singleton():
    """Same vendor data → one MAC_VENDOR node; each MAC links via had."""
    doc = {
        "netdiscover_scan": {
            "args": "netdiscover test",
            "systems": [
                {"ipv4": "10.0.0.1", "mac": "aa:bb:cc:dd:ee:01", "mac_vendor": "Unknown"},
                {"ipv4": "10.0.0.2", "mac": "aa:bb:cc:dd:ee:02", "mac_vendor": "Unknown"},
                {"ipv4": "10.0.0.3", "mac": "aa:bb:cc:dd:ee:03", "mac_vendor": "Apple, Inc."},
            ],
        }
    }
    graph = netdiscover_scan_to_graph(doc)
    vendors = [n for n in graph["nodes"] if n["nugget_id"] == "MAC_VENDOR"]
    unknown = [n for n in vendors if n["nugget_data"] == "Unknown"]
    assert len(unknown) == 1
    had_to_unknown = [
        e for e in graph["edges"] if e["relation"] == "had" and e["target"] == unknown[0]["id"]
    ]
    assert len(had_to_unknown) == 2


def test_mac_vendor_descriptor_in_graph():
    doc = convert_text_to_netdiscover_scan(
        PARSABLE_SAMPLE,
        scenario_name="parsable",
        output_mode="parsable",
        start_time=datetime.now(timezone.utc),
        duration_s=1.0,
        exit_code=0,
    )
    graph = netdiscover_scan_to_graph(doc)
    vendors = [n for n in graph["nodes"] if n["nugget_id"] == "MAC_VENDOR"]
    assert len(vendors) == 3
    mac_ids = [n["id"] for n in graph["nodes"] if n["nugget_id"] == "MAC_ADDRESS"]
    assert len(mac_ids) == 3
    for mac_id in mac_ids:
        had_edges = [
            e
            for e in graph["edges"]
            if e["source"] == mac_id and e["relation"] == "had"
        ]
        assert len(had_edges) == 1
        target = had_edges[0]["target"]
        assert any(v["id"] == target and v["nugget_id"] == "MAC_VENDOR" for v in vendors)


def test_graph_has_no_duplicate_nodes_or_orphans():
    doc = convert_text_to_netdiscover_scan(
        PARSABLE_SAMPLE,
        scenario_name="parsable",
        output_mode="parsable",
        start_time=datetime.now(timezone.utc),
        duration_s=1.0,
        exit_code=0,
    )
    graph = netdiscover_scan_to_graph(doc)
    assert len(graph["nodes"]) == len({n["id"] for n in graph["nodes"]})
    assert validate_graph_connectivity(graph) == []


def test_six_frames_two_tables_four_empty():
    """User rule: 6 scan frames, 2 with host tables → empty_scans=4."""
    frames = []
    for _ in range(4):
        frames.append(
            "Currently scanning: Starting.\n"
            " 0 Captured ARP Req/Rep packets, from 0 hosts.\n"
            " -----------------------------------------------------------------------------\n"
        )
    frames.append(
        "Currently scanning: 192.168.1.0/24\n"
        " 10 Captured ARP Req/Rep packets, from 2 hosts.\n"
        " 192.168.1.1     14:5f:94:d8:7a:5f      1      42  Apple, Inc.\n"
        " 192.168.1.2     a8:51:ab:23:c6:49      1      42  Texas Instruments\n"
    )
    frames.append(
        "Currently scanning: 192.168.1.0/24\n"
        " 12 Captured ARP Req/Rep packets, from 2 hosts.\n"
        " 192.168.1.1     14:5f:94:d8:7a:5f      1      42  Apple, Inc.\n"
    )
    raw = "\n".join(frames)
    _, scan_tries, empty_scans, _ = parse_interactive_body(raw)
    assert scan_tries == 6
    assert empty_scans == 4


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
    assert doc["netdiscover_scan"]["exit_status"] == "error"
    graph = netdiscover_scan_to_graph(doc)
    assert any(node["nugget_id"] == "SCAN_RECORD" for node in graph["nodes"])
    exit_nodes = [n for n in graph["nodes"] if n["nugget_id"] == "SCAN_EXIT_STATUS"]
    assert len(exit_nodes) == 1
    assert exit_nodes[0]["nugget_data"] == "error"
    scan_id = next(n["id"] for n in graph["nodes"] if n["nugget_id"] == "SCAN_RECORD")
    assert any(
        e["source"] == scan_id and e["target"] == exit_nodes[0]["id"] and e["relation"] == "had"
        for e in graph["edges"]
    )
