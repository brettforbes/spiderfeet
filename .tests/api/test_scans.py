"""Scan API validation and read paths (SF-02-04, SF-02-07)."""

from fastapi.testclient import TestClient


def test_create_scan_requires_module_selection(api_client: TestClient):
    response = api_client.post(
        "/api/v1/scans",
        json={"target": "example.com"},
    )
    assert response.status_code == 422


def test_create_scan_invalid_target(api_client: TestClient):
    response = api_client.post(
        "/api/v1/scans",
        json={
            "target": "not-a-valid-target-@@@",
            "use_case": "passive",
        },
    )
    assert response.status_code == 400


def test_get_scan_not_found(api_client: TestClient):
    response = api_client.get("/api/v1/scans/nonexistent-scan-id")
    assert response.status_code == 404


def test_list_scans_returns_array(api_client: TestClient):
    response = api_client.get("/api/v1/scans")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
