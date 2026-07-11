"""Tests for SPEC-004 shared correlation lists (C1)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
SHARED = CLI_CORPUS / "rules" / "_shared"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.correlation_lists import (
    cdn_provider_signatures,
    edge_asn_entries,
    load_cdn_signatures,
    load_edge_asns,
    match_edge_asn,
    match_server_header,
)


def test_cdn_signatures_yaml_loads_with_seed_traceability():
    data = load_cdn_signatures(SHARED / "cdn_signatures.yaml")

    assert data["schema"] == "cdn_signatures_v1"
    assert data["ruleset"] == "C1"
    assert "07_Nerva_Scan_Record_Host_Correlation_Rulesets.md" in data["source_seed"]
    assert any(row["vendor"] == "Cloudflare" for row in data["providers"])


def test_edge_asns_yaml_loads_with_seed_traceability():
    data = load_edge_asns(SHARED / "edge_asns.yaml")

    assert data["schema"] == "edge_asns_v1"
    assert data["ruleset"] == "C2"
    assert any(row["asn"] == 13335 and row["vendor"] == "Cloudflare" for row in data["asns"])


def test_praetorian_cloudflare_server_header_matches_c1():
    vendor = match_server_header("cloudflare", cdn_provider_signatures())

    assert vendor == "Cloudflare"


def test_cloudflare_asn_matches_c2():
    vendor = match_edge_asn(13335, edge_asn_entries())

    assert vendor == "Cloudflare"
