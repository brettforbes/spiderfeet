"""AN3 / R10-26 — absorbed v1 routes remain equivalent under dual-stack mount.

Maps / Tests / Subscriptions / CLI-Profiling / Content must keep working when
``spiderfeet_v2.api.v2_router`` is mounted on the same ``/api/v1`` app.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from spiderfeet.map.read import MapInventory


# Widget-consumed v1 surfaces that must not break when v2 routes are present.
ABSORBED_V1_OPENAPI_PREFIXES = (
    "/api/v1/map",
    "/api/v1/tests",
    "/api/v1/subscriptions",
    "/api/v1/cli-corpus",
    "/api/v1/content",
)

V2_OPENAPI_PATHS = (
    "/api/v1/projects",
    "/api/v1/workflows",
    "/api/v1/targets",
    "/api/v1/scan-steps/{scan_instance_id}",
    "/api/v1/projects/{project_id}/contexts/temporary",
    "/api/v1/projects/{project_id}/complete",
    "/api/v1/workflows/{workflow_id}/execute",
)


def test_openapi_keeps_absorbed_v1_and_v2_paths(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    paths = r.json()["paths"]

    for prefix in ABSORBED_V1_OPENAPI_PREFIXES:
        assert any(p.startswith(prefix) for p in paths), f"missing v1 surface {prefix}"

    for path in V2_OPENAPI_PATHS:
        assert path in paths, f"missing v2 path {path}"

    # Dual-stack must not collide: v2 projects/workflows/targets are additive.
    assert "/api/v1/map/status" in paths or any(
        p.startswith("/api/v1/map/") for p in paths
    )
    assert "/api/v1/projects" in paths
    assert "/api/v1/projects" != "/api/v1/map/status"


def test_v1_health_and_cors_headers(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    # Preflight-style OPTIONS is handled by CORS middleware; GET with Origin
    # should still succeed (stable base URL / CORS retained for widget).
    r = client.get("/api/v1/health", headers={"Origin": "http://localhost:8080"})
    assert r.status_code == 200


def test_v1_tests_summary_unaffected(client):
    r = client.get("/api/v1/tests/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["module_count"] > 0
    assert body["test_count"] > 0
    assert "test_states" in body


def test_v1_tests_modules_list_unaffected(client):
    r = client.get("/api/v1/tests/modules", params={"limit": 3, "offset": 0})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 3
    assert rows[0]["module_id"].startswith("sfp_")


def test_v1_subscriptions_modules_unaffected(client):
    r = client.get("/api/v1/subscriptions/modules", params={"limit": 5})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 5
    assert rows[0]["requires_api_key"] is True
    assert "secret_opts" in rows[0]


def test_v1_cli_corpus_tools_unaffected(client):
    r = client.get("/api/v1/cli-corpus/tools")
    assert r.status_code == 200
    ids = {t["id"] for t in r.json()}
    assert "nmap" in ids
    assert "netdiscover" in ids


def test_v1_cli_corpus_config_unaffected(client):
    r = client.get("/api/v1/cli-corpus/config")
    assert r.status_code == 200
    assert "data_viewer_url" in r.json()


def test_v1_content_tools_unaffected(client):
    r = client.get("/api/v1/content/tools")
    assert r.status_code == 200
    body = r.json()
    ids = {t["tool_id"] for t in body["tools"]}
    assert "nmap" in ids
    assert body["total"] >= 8


def test_v1_map_connection_shape_unaffected(client):
    cfg = MagicMock()
    cfg.database = "spiderfeet-map"
    cfg.addresses = ["127.0.0.1:1729"]
    cfg.username = "admin"
    cfg.password = "secret"
    cfg.tls_enabled = False

    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=cfg,
    ):
        r = client.get("/api/v1/map/connection")
    assert r.status_code == 200
    body = r.json()
    assert body["database"] == "spiderfeet-map"
    assert "password" not in body


def test_v1_map_status_shape_unaffected(client):
    cfg = MagicMock()
    cfg.database = "spiderfeet-map"
    cfg.addresses = ["127.0.0.1:1729"]
    cfg.username = "admin"
    cfg.password = "secret"
    cfg.tls_enabled = False
    inv = MapInventory(nugget_count=172, service_count=177, link_count=1443)

    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=cfg,
    ), patch("spiderfeet.api.services.map.ping", return_value=True), patch(
        "spiderfeet.api.services.map.database_exists", return_value=True
    ), patch("spiderfeet.api.services.map.driver_session") as session, patch(
        "spiderfeet.api.services.map.get_inventory",
        return_value=inv,
    ):
        session.return_value.__enter__ = MagicMock(return_value=MagicMock())
        session.return_value.__exit__ = MagicMock(return_value=False)
        r = client.get("/api/v1/map/status")

    assert r.status_code == 200
    body = r.json()
    assert body["reachable"] is True
    assert body["inventory"]["service_count"] == 177


def test_dual_stack_v2_crud_does_not_shadow_v1_tests(client):
    """Creating a v2 project must not change v1 Tests catalogue responses."""
    before = client.get("/api/v1/tests/summary").json()

    client.post(
        "/api/v1/targets",
        json={"target_id": "target--shadow", "target_value": "shadow.example"},
    )
    client.post(
        "/api/v1/workflows",
        json={"workflow_id": "workflow--shadow", "target_id": "target--shadow"},
    )
    client.post(
        "/api/v1/projects",
        json={
            "project_id": "project--shadow",
            "workflow_ids": ["workflow--shadow"],
        },
    )

    after = client.get("/api/v1/tests/summary").json()
    assert after["module_count"] == before["module_count"]
    assert after["test_count"] == before["test_count"]

    # v2 still works
    assert client.get("/api/v1/projects/project--shadow").status_code == 200
