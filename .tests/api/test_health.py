"""API health endpoint (SF-02-02 / R2-02-01)."""

from fastapi.testclient import TestClient

from spiderfeet import __version__


def test_health_returns_version(api_client: TestClient):
    response = api_client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == __version__
    assert body["service"] == "spiderfeet-api"
