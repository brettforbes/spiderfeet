"""Unit tests for module seed metadata helpers."""

from spiderfeet.map.test_targets import (
    fixture_kind_for_entry,
    seed_coverage_complete,
    seed_metadata_for_module,
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
