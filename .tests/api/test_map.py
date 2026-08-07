"""Unit tests for map API routes (mocked TypeDB)."""

from unittest.mock import MagicMock, patch

import pytest

from spiderfeet.map.read import ForceGraphExport, ForceGraphLink, ForceGraphNode, MapInventory


@pytest.fixture
def mock_config():
    cfg = MagicMock()
    cfg.database = "spiderfeet-map"
    cfg.addresses = ["127.0.0.1:1729"]
    cfg.username = "admin"
    cfg.password = "secret"
    cfg.tls_enabled = False
    return cfg


def test_map_connection_requires_config(api_client):
    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        side_effect=__import__(
            "spiderfeet.map.config", fromlist=["TypeDBConfigError"]
        ).TypeDBConfigError("missing"),
    ):
        r = api_client.get("/api/v1/map/connection")
    assert r.status_code == 503


def test_map_connection_redacted(api_client, mock_config):
    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=mock_config,
    ):
        r = api_client.get("/api/v1/map/connection")
    assert r.status_code == 200
    body = r.json()
    assert body["database"] == "spiderfeet-map"
    assert "password" not in body


def test_map_status_with_inventory(api_client, mock_config):
    inv = MapInventory(nugget_count=172, service_count=177, link_count=1443)

    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=mock_config,
    ), patch("spiderfeet.api.services.map.ping", return_value=True), patch(
        "spiderfeet.api.services.map.database_exists", return_value=True
    ), patch("spiderfeet.api.services.map.driver_session") as session, patch(
        "spiderfeet.api.services.map.get_inventory",
        return_value=inv,
    ):
        session.return_value.__enter__ = MagicMock(return_value=MagicMock())
        session.return_value.__exit__ = MagicMock(return_value=False)
        r = api_client.get("/api/v1/map/status")

    assert r.status_code == 200
    body = r.json()
    assert body["reachable"] is True
    assert body["server_reachable"] is True
    assert body["database_ready"] is True
    assert body["inventory"]["service_count"] == 177


def test_map_status_server_up_bootstraps_when_not_ready(api_client, mock_config):
    inv = MapInventory(nugget_count=172, service_count=177, link_count=1443)

    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=mock_config,
    ), patch("spiderfeet.api.services.map.ping", return_value=True), patch(
        "spiderfeet.api.services.map.ensure_map_ready", return_value=True
    ) as ensure, patch(
        "spiderfeet.api.services.map.database_exists", return_value=True
    ), patch("spiderfeet.api.services.map.driver_session") as session, patch(
        "spiderfeet.api.services.map.get_inventory",
        return_value=inv,
    ):
        session.return_value.__enter__ = MagicMock(return_value=MagicMock())
        session.return_value.__exit__ = MagicMock(return_value=False)
        r = api_client.get("/api/v1/map/status")

    assert r.status_code == 200
    body = r.json()
    ensure.assert_called_once()
    assert body["bootstrapped"] is True
    assert body["server_reachable"] is True
    assert body["database_ready"] is True


def test_map_status_empty_catalogue_not_ready(api_client, mock_config):
    inv = MapInventory(nugget_count=0, service_count=0, link_count=0)

    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=mock_config,
    ), patch("spiderfeet.api.services.map.ping", return_value=True), patch(
        "spiderfeet.api.services.map.ensure_map_ready", return_value=True
    ), patch(
        "spiderfeet.api.services.map.database_exists", return_value=True
    ), patch("spiderfeet.api.services.map.driver_session") as session, patch(
        "spiderfeet.api.services.map.get_inventory",
        return_value=inv,
    ):
        session.return_value.__enter__ = MagicMock(return_value=MagicMock())
        session.return_value.__exit__ = MagicMock(return_value=False)
        r = api_client.get("/api/v1/map/status")

    assert r.status_code == 200
    body = r.json()
    assert body["bootstrapped"] is True
    assert body["database_ready"] is False


def test_map_status_server_down(api_client, mock_config):
    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=mock_config,
    ), patch("spiderfeet.api.services.map.ping", return_value=False):
        r = api_client.get("/api/v1/map/status")

    assert r.status_code == 200
    body = r.json()
    assert body["reachable"] is False
    assert body["database_ready"] is False


def test_map_graph_export(api_client, mock_config):
    graph = ForceGraphExport(
        nodes=[
            ForceGraphNode(
                id="sfp_abstractapi",
                kind="osint-service",
                label="AbstractAPI",
                service_state="in-test",
            ),
            ForceGraphNode(
                id="INTERNET_NAME",
                kind="nugget",
                label="Internet Name",
                colour="#3B82F6",
            ),
        ],
        links=[
            ForceGraphLink(
                source="sfp_abstractapi",
                target="INTERNET_NAME",
                role="consumed",
            )
        ],
    )

    with patch(
        "spiderfeet.api.services.map.load_connection_config",
        return_value=mock_config,
    ), patch("spiderfeet.api.services.map.ping", return_value=True), patch(
        "spiderfeet.api.services.map.driver_session"
    ) as session, patch(
        "spiderfeet.api.services.map.export_force_graph",
        return_value=graph,
    ):
        session.return_value.__enter__ = MagicMock(return_value=MagicMock())
        session.return_value.__exit__ = MagicMock(return_value=False)
        r = api_client.get("/api/v1/map/graph")

    assert r.status_code == 200
    body = r.json()
    assert len(body["nodes"]) == 2
    assert body["links"][0]["role"] == "consumed"
