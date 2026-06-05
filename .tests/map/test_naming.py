"""Unit tests for map naming helpers."""

from spiderfeet.map.naming import (
    entity_type_for_nugget_id,
    kebab_case,
    relation_type_for_module_id,
)


def test_kebab_case():
    assert kebab_case("INTERNET_NAME") == "internet-name"
    assert kebab_case("sfp_dnsresolve") == "sfp-dnsresolve"


def test_entity_type_for_nugget_id():
    assert entity_type_for_nugget_id("DOMAIN_NAME") == "domain-name"


def test_relation_type_for_module_id():
    assert relation_type_for_module_id("sfp_virustotal") == "sfp-virustotal"
