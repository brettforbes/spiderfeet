"""scan_ui endpoint validation and mapping (SF-02)."""

from fastapi.testclient import TestClient

from spiderfeet.api.schemas import ScanResultItem
from spiderfeet.api.services.scan_ui import result_to_nugget


def test_scan_ui_requires_consumed_nugget(api_client: TestClient):
    response = api_client.post(
        "/api/v1/scan_ui",
        json={"module_id": "sfp_dnsresolve"},
    )
    assert response.status_code == 422


def test_scan_ui_unknown_module(api_client: TestClient):
    response = api_client.post(
        "/api/v1/scan_ui",
        json={
            "module_id": "sfp_not_a_real_module",
            "consumed": {
                "nugget_id": "INTERNET_NAME",
                "nugget_data": "sbs.com.au",
            },
            "wait": False,
        },
    )
    assert response.status_code == 400
    assert "Unknown module_id" in response.json()["detail"]


def test_scan_ui_unknown_nugget_id(api_client: TestClient):
    response = api_client.post(
        "/api/v1/scan_ui",
        json={
            "module_id": "sfp_dnsresolve",
            "consumed": {
                "nugget_id": "NOT_IN_CATALOGUE",
                "nugget_data": "sbs.com.au",
            },
            "wait": False,
        },
    )
    assert response.status_code == 400
    assert "Unknown catalogue nugget_id" in response.json()["detail"]


def test_scan_ui_catalogue_company_name(api_client: TestClient):
    response = api_client.post(
        "/api/v1/scan_ui",
        json={
            "module_id": "sfp_gleif",
            "consumed": {
                "nugget_id": "COMPANY_NAME",
                "nugget_data": "Google LLC",
            },
            "wait": False,
        },
    )
    assert response.status_code != 400 or "not a valid SpiderFeet target" not in (
        response.json().get("detail") or ""
    )


def test_scan_ui_invalid_target(api_client: TestClient):
    response = api_client.post(
        "/api/v1/scan_ui",
        json={
            "module_id": "sfp_dnsresolve",
            "consumed": {
                "nugget_id": "INTERNET_NAME",
                "nugget_data": "!!!not-a-target!!!",
            },
            "wait": False,
        },
    )
    assert response.status_code == 400


def test_result_to_nugget_maps_catalogue_fields():
    item = ScanResultItem(
        generated=1710000000,
        data="203.0.113.1",
        source_data="sbs.com.au",
        module="sfp_dnsresolve",
        type="IP_ADDRESS",
        confidence=100,
        visibility=100,
        risk=0,
        event_description="IP resolved",
        false_positive=False,
    )
    nugget = result_to_nugget(item)
    assert nugget.nugget_id == "IP_ADDRESS"
    assert nugget.entity_type == "ip-address"
    assert nugget.nugget_data == "203.0.113.1"
    assert nugget.nugget_module == "sfp_dnsresolve"
    assert nugget.nugget_icon is not None
    assert nugget.nugget_colour is not None
    assert nugget.nugget_instance_id.startswith("IP_ADDRESS--")
