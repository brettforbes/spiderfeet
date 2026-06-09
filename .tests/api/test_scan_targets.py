"""scan_ui target resolution for catalogue nugget types."""

import pytest

from spiderfeet.api.services.scan_targets import resolve_scan_ui_target


def test_resolve_company_name():
    value, kind = resolve_scan_ui_target("COMPANY_NAME", "Google LLC")
    assert value == "Google LLC"
    assert kind == "COMPANY_NAME"


def test_resolve_physical_address():
    value, kind = resolve_scan_ui_target(
        "PHYSICAL_ADDRESS",
        "1600 Amphitheatre Parkway, Mountain View, CA",
    )
    assert kind == "PHYSICAL_ADDRESS"
    assert "Mountain View" in value


def test_resolve_username_quotes_bare_handle():
    value, kind = resolve_scan_ui_target("USERNAME", "keybase")
    assert value == "keybase"
    assert kind == "USERNAME"


def test_resolve_web_analytics_id():
    value, kind = resolve_scan_ui_target("WEB_ANALYTICS_ID", "GTM-5K8Q5L")
    assert value == "GTM-5K8Q5L"
    assert kind == "WEB_ANALYTICS_ID"


def test_resolve_domain_via_internet_name():
    value, kind = resolve_scan_ui_target("DOMAIN_NAME", "example.com")
    assert value == "example.com"
    assert kind == "INTERNET_NAME"


def test_resolve_rejects_blank():
    with pytest.raises(ValueError):
        resolve_scan_ui_target("COMPANY_NAME", "   ")
