"""Unit tests for OSINT subscription tier and API-key detection."""

from spiderfeet.map.subscriptions import (
    has_configured_api_key,
    is_secret_module_opt,
    mask_secret,
    requires_api_key,
    secret_opt_names,
    subscription_status,
    subscription_tier_for_service,
)


def test_is_secret_module_opt_rejects_hostname():
    assert is_secret_module_opt("api_hostname") is False
    assert is_secret_module_opt("api_host") is False
    assert is_secret_module_opt("api_key") is True
    assert is_secret_module_opt("token") is True


def test_is_secret_module_opt_rejects_passwordpages_toggle():
    assert is_secret_module_opt("passwordpages") is False
    assert is_secret_module_opt("api_key_password") is True
    assert is_secret_module_opt("password") is True


def test_archiveorg_free_no_auth_not_key_gated():
    from spiderfeet.map.routes_catalog import service_by_module_id

    service = service_by_module_id("sfp_archiveorg")
    assert service is not None
    assert requires_api_key(service) is False
    assert subscription_tier_for_service(service) == "none"


def test_threatjammer_requires_key_without_hostname_false_positive():
    service = {
        "module_id": "sfp_threatjammer",
        "access_tier": "free_auth",
        "flags": ["apikey"],
        "data_source": {"api_key_instructions": ["get a key"]},
        "module_opts": [
            {"name": "api_hostname", "value": "dublin.api.threatjammer.com"},
            {"name": "api_key", "value": ""},
        ],
    }
    assert secret_opt_names(service) == ["api_key"]
    assert requires_api_key(service) is True
    assert has_configured_api_key(service, {}) is False
    tier, needs, has_key, skip = subscription_status(service, {})
    assert tier == "free_auth"
    assert needs is True
    assert has_key is False
    assert skip == "missing-api-key"


def test_threatjammer_with_runtime_key():
    service = {
        "module_id": "sfp_threatjammer",
        "access_tier": "free_auth",
        "flags": ["apikey"],
        "module_opts": [
            {"name": "api_hostname", "value": "dublin.api.threatjammer.com"},
            {"name": "api_key", "value": ""},
        ],
    }
    configured = {"sfp_threatjammer": {"opts": {"api_key": "abc123", "api_hostname": "x"}}}
    assert has_configured_api_key(service, configured) is True
    _, _, has_key, skip = subscription_status(service, configured)
    assert has_key is True
    assert skip is None


def test_duckduckgo_none_tier():
    service = {
        "module_id": "sfp_duckduckgo",
        "access_tier": "free_no_auth",
        "flags": [],
        "data_source": {"model": "FREE_NOAUTH_UNLIMITED"},
        "module_opts": [{"name": "affiliatedomains", "value": True}],
    }
    assert requires_api_key(service) is False
    assert subscription_tier_for_service(service) == "none"
    assert has_configured_api_key(service, {}) is True


def test_abstractapi_free_auth_despite_free_no_auth_label():
    service = {
        "module_id": "sfp_abstractapi",
        "access_tier": "free_no_auth",
        "flags": ["apikey"],
        "data_source": {"api_key_instructions": ["sign up"]},
        "module_opts": [{"name": "api_key", "value": ""}],
    }
    assert subscription_tier_for_service(service) == "free_auth"
    assert requires_api_key(service) is True


def test_paid_tier():
    service = {
        "module_id": "sfp_shodan",
        "access_tier": "paid",
        "module_opts": [{"name": "api_key", "value": ""}],
    }
    assert subscription_tier_for_service(service) == "paid_auth"


def test_mask_secret():
    assert mask_secret("") is None
    assert mask_secret("abc") == "••••"
    assert mask_secret("test-emailrep-key-1234").endswith("1234")
