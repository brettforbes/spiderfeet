"""Unit tests for tests catalog API."""

from unittest.mock import patch


def test_tests_summary(api_client):
    r = api_client.get("/api/v1/tests/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["module_count"] >= 170
    assert body["route_count"] > 0
    assert "route_states" in body
    assert body["route_states"]["not_started"] >= 0


def test_tests_modules_list(api_client):
    r = api_client.get("/api/v1/tests/modules", params={"limit": 5, "offset": 0})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 5
    assert rows[0]["module_id"].startswith("sfp_")


def test_tests_modules_search(api_client):
    r = api_client.get("/api/v1/tests/modules", params={"search": "abstractapi", "limit": 10})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) >= 1
    assert all("abstractapi" in row["module_id"] for row in rows)


def test_tests_module_detail(api_client):
    r = api_client.get("/api/v1/tests/modules/sfp_abstractapi")
    assert r.status_code == 200
    from spiderfeet.api.schemas import TestsModuleDetail as ModuleDetailModel

    detail = ModuleDetailModel.model_validate(r.json())
    assert detail.module_id == "sfp_abstractapi"
    assert detail.route_count == len(detail.routes)
    assert detail.routes[0].route_state == "not-started"


def test_tests_module_not_found(api_client):
    r = api_client.get("/api/v1/tests/modules/sfp_not_a_real_module")
    assert r.status_code == 404


def test_tests_summary_with_typedb_states(api_client):
    states = {
        "DOMAIN_NAME-to-IP_ADDRESS-via-sfp_dnsdb": "in-test",
    }
    with patch(
        "spiderfeet.api.services.tests._typedb_route_states",
        return_value=states,
    ):
        r = api_client.get("/api/v1/tests/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["typedb_connected"] is True
    assert body["route_states"]["in_test"] >= 1
