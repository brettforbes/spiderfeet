"""Tests for SPEC-004 correlation engine (C2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
FIXTURE = CLI_CORPUS / "fixtures" / "nerva_correlation_seed07.json"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.correlation_engine import correlate_nerva_records, correlate_records, normalize_nerva_record


def _load_fixture_records():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["records"]


def test_scanme_dual_stack_ssh_records_same_system_via_a1():
    records = [
        normalize_nerva_record(item, index)
        for index, item in enumerate(_load_fixture_records())
        if item["host"] == "scanme.nmap.org" and item["port"] == 22
    ]
    results = correlate_records(records)

    assert len(results) == 2
    assert all(result.same_system_confidence == "high" for result in results)
    assert all("A1:" in result.same_system_evidence for result in results)
    assert results[0].same_system_group_id == results[1].same_system_group_id
    assert results[0].host_classification == "standard_host"
    assert results[0].classification_rule_fired.startswith("B1")


def test_praetorian_records_classified_as_cloudflare_fronted():
    records = [
        normalize_nerva_record(item, index)
        for index, item in enumerate(_load_fixture_records())
        if item["host"] == "praetorian.com"
    ]
    results = correlate_records(records)

    assert len(results) == 4
    assert all(result.host_classification == "fronted_unknown" for result in results)
    assert all(result.classification_confidence == "high" for result in results)
    assert all(result.classification_rule_fired.startswith("C1:") for result in results)
    assert all(result.cdn_vendor == "Cloudflare" for result in results)
    assert all(result.origin_host_count is None for result in results)


def test_correlate_nerva_records_groups_by_hostname():
    results = correlate_nerva_records(_load_fixture_records())
    scanme = [row for row in results if row.hostname == "scanme.nmap.org"]
    praetorian = [row for row in results if row.hostname == "praetorian.com"]

    assert len(scanme) == 2
    assert len(praetorian) == 4
    assert all(row.cdn_vendor == "Cloudflare" for row in praetorian)
