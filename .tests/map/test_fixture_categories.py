"""fixture_category classification."""

from spiderfeet.map.fixture_categories import fixture_category_for_service


def test_reputation_module_is_negative():
    svc = {
        "module_id": "sfp_spamcop",
        "categories": ["Reputation Systems"],
    }
    assert fixture_category_for_service(svc) == "negative"


def test_search_module_defaults_positive():
    svc = {
        "module_id": "sfp_dnsresolve",
        "categories": ["DNS"],
    }
    assert fixture_category_for_service(svc) == "positive"


def test_explicit_fixture_category_wins():
    svc = {
        "module_id": "sfp_spamcop",
        "fixture_category": "positive",
        "categories": ["Reputation Systems"],
    }
    assert fixture_category_for_service(svc) == "positive"
