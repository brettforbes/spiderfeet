"""Catalogue endpoints (SF-02-05, SF-02-06)."""

from fastapi.testclient import TestClient


def test_modules_list(api_client: TestClient):
    response = api_client.get("/api/v1/modules")
    assert response.status_code == 200
    body = response.json()
    assert len(body) > 10
    assert "name" in body[0]
    assert "description" in body[0]
    names = {m["name"] for m in body}
    assert "sfp_dnsresolve" in names or any(n.startswith("sfp_") for n in names)


def test_event_types_list(api_client: TestClient):
    response = api_client.get("/api/v1/event-types")
    assert response.status_code == 200
    body = response.json()
    assert len(body) > 5
    assert "name" in body[0]
    assert "description" in body[0]
