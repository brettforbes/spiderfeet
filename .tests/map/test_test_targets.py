"""Unit tests for module seed metadata helpers."""

from spiderfeet.map.test_targets import (
    fixture_kind_for_entry,
    seed_coverage_complete,
    seed_metadata_for_module,
    seed_research_complete,
    seed_upstream_blocked,
)


def test_fixture_kind_defaults_positive():
    assert fixture_kind_for_entry({}) == "positive"
    assert fixture_kind_for_entry({"fixture_kind": "negative"}) == "negative"


def test_seed_coverage_positive():
    assert seed_coverage_complete("sfp_duckduckgo", "DOMAIN_NAME") is True


def test_seed_coverage_negative():
    assert seed_coverage_complete("sfp_spamcop", "IP_ADDRESS") is True
    meta = seed_metadata_for_module("sfp_spamcop", "IP_ADDRESS")
    assert meta["fixture_kind"] == "negative"
    assert meta["seed_validated"] is True


def test_seed_upstream_blocked_counts_as_research_complete():
    assert seed_upstream_blocked("sfp_dnsdumpster", "DOMAIN_NAME") is True
    assert seed_coverage_complete("sfp_dnsdumpster", "DOMAIN_NAME") is False
    assert seed_research_complete("sfp_dnsdumpster", "DOMAIN_NAME") is True
