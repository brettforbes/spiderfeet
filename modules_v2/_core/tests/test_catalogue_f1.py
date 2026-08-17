"""SPEC-019 R19-15 — COMPANY/SUBDOMAIN catalogue entries."""

from __future__ import annotations

from modules_v2._core.graph_builder import load_nugget_templates


def test_company_and_subdomain_catalogue_entries() -> None:
    templates = load_nugget_templates()
    company = templates["COMPANY"]
    subdomain = templates["SUBDOMAIN"]
    company_name = templates["COMPANY_NAME"]

    assert company["nugget_type"] == "ENTITY"
    assert company["nugget_icon"] == "icon_company_name.svg"
    assert subdomain["nugget_type"] == "ENTITY"
    assert subdomain["nugget_icon"] == "icon_domain_name.svg"
    assert company_name["nugget_type"] == "DESCRIPTOR"
