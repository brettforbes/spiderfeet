"""Integration test for POST /api/v1/scan_ui (real scan)."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.slow
def test_scan_ui_dns_resolve_finishes(api_client: TestClient):
    """Runs sfp_dnsresolve against sbs.com.au; requires working DNS/modules."""
    response = api_client.post(
        "/api/v1/scan_ui",
        json={
            "module_id": "sfp_dnsresolve",
            "consumed": {
                "nugget_id": "INTERNET_NAME",
                "nugget_data": "sbs.com.au",
            },
            "wait": True,
            "timeout_seconds": 120,
        },
        timeout=130,
    )
    assert response.status_code == 200, response.text
    body = response.json()
    record = body["scan_record"]
    assert record["status"] == "FINISHED"
    assert record["scan_event_count"] >= 1
    assert record["scan_results"]["event_count"] >= 1
    assert record["service"]["module_id"] == "sfp_dnsresolve"
    assert len(body["produced"]) >= 1
    assert len(body["consumed"]) == 1
    assert body["consumed"][0]["nugget_id"] == "INTERNET_NAME"
