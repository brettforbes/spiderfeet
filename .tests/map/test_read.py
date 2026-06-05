"""Unit tests for map read/export helpers."""

from unittest.mock import MagicMock, patch

from spiderfeet.map.read import export_force_graph


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
        return []

    driver = MagicMock()
    with patch("spiderfeet.map.read._fetch_documents", side_effect=fake_fetch):
        graph = export_force_graph(driver, "spiderfeet-map")

    assert len(graph.nodes) == 2
    assert len(graph.links) == 2
    roles = {link.role for link in graph.links}
    assert roles == {"consumed", "produced"}
