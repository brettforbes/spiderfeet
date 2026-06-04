"""API health endpoint (SF-02-02 / R2-02-01)."""

from fastapi.testclient import TestClient

from spiderfeet.api.app import create_app
from spiderfeet import __version__


def test_health_returns_version():
    client = TestClient(create_app())
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == __version__
    assert body["service"] == "spiderfeet-api"
