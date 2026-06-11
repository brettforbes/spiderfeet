"""service_origin classification (external-api | cli | local)."""

from spiderfeet.map.service_classification import (
    SERVICE_ORIGIN_CLI,
    SERVICE_ORIGIN_EXTERNAL_API,
    SERVICE_ORIGIN_LOCAL,
    normalize_service_origin,
    service_origin_for_module_id,
)


def test_external_api_module():
    assert (
        service_origin_for_module_id("sfp_shodan", external_api=True)
        == SERVICE_ORIGIN_EXTERNAL_API
    )


def test_local_quarantine_module():
    assert (
        service_origin_for_module_id("sfp_dnsresolve", external_api=False)
        == SERVICE_ORIGIN_LOCAL
    )


def test_cli_tool_module():
    assert (
        service_origin_for_module_id("sfp_tool_nmap", external_api=False)
        == SERVICE_ORIGIN_CLI
    )


def test_normalize_legacy_quarantine_origin():
    assert (
        normalize_service_origin(
            "quarantine",
            module_id="sfp_tool_nuclei",
            external_api=False,
        )
        == SERVICE_ORIGIN_CLI
    )
    assert (
        normalize_service_origin(
            "quarantine",
            module_id="sfp_accounts",
            external_api=False,
        )
        == SERVICE_ORIGIN_LOCAL
    )


def test_normalize_legacy_external():
    assert (
        normalize_service_origin("external", module_id="sfp_shodan", external_api=True)
        == SERVICE_ORIGIN_EXTERNAL_API
    )


def test_normalize_legacy_external_cli_tool():
    assert (
        normalize_service_origin(
            "external",
            module_id="sfp_tool_nuclei",
            external_api=False,
        )
        == SERVICE_ORIGIN_CLI
    )
