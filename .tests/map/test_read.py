"""Unit tests for map read/export helpers."""

from unittest.mock import MagicMock, patch

from spiderfeet.map.read import _fav_icons_from_catalog, export_force_graph


class _DocIter:
    def __init__(self, rows):
        self._rows = rows

    def __iter__(self):
        return iter(self._rows)


def test_export_force_graph_deduplicates():
    consumed_row = {
        "module_id": "sfp_a",
        "service_name": "A",
        "service_state": "in-test",
        "nugget_id": "N1",
        "nugget_description": "Nugget 1",
        "nugget_colour": "#111",
    }

    def fake_fetch(driver, database, query):
        if "consumed" in query:
            return [consumed_row]
        if "produced" in query:
            return [consumed_row]
        if "fav_icon" in query:
            return []
        return []

    driver = MagicMock()
    with patch("spiderfeet.map.read._fetch_documents", side_effect=fake_fetch):
        graph = export_force_graph(driver, "spiderfeet-map")

    assert len(graph.nodes) == 2
    assert len(graph.links) == 2
    roles = {link.role for link in graph.links}
    assert roles == {"consumed", "produced"}


def test_fav_icons_from_catalog_has_abstractapi():
    icons = _fav_icons_from_catalog()
    assert "sfp_abstractapi" in icons
    assert icons["sfp_abstractapi"].startswith("http")


def test_export_force_graph_enriches_service_fav_icon():
    consumed_row = {
        "module_id": "sfp_abstractapi",
        "service_name": "AbstractAPI",
        "service_state": "in-test",
        "nugget_id": "DOMAIN_NAME",
        "nugget_description": "Domain Name",
        "nugget_colour": "#3B82F6",
        "nugget_icon": "icon_domain_name.svg",
    }

    def fake_fetch(driver, database, query):
        if "consumed" in query:
            return [consumed_row]
        if "produced" in query:
            return []
        if "fav_icon" in query:
            return []
        return []

    driver = MagicMock()
    with patch("spiderfeet.map.read._fetch_documents", side_effect=fake_fetch):
        graph = export_force_graph(driver, "spiderfeet-map")

    service = next(n for n in graph.nodes if n.kind == "osint-service")
    assert service.fav_icon
    assert service.fav_icon.startswith("http")
