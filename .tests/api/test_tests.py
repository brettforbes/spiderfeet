"""Unit tests for tests catalog API."""

from unittest.mock import patch


def test_tests_summary(api_client):
    r = api_client.get("/api/v1/tests/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["module_count"] >= 170
    assert body["test_count"] > 0
    assert body["route_count"] >= body["test_count"]
    assert "test_states" in body
    assert body["test_states"]["not_started"] >= 0


def test_tests_modules_list(api_client):
    r = api_client.get("/api/v1/tests/modules", params={"limit": 5, "offset": 0})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 5
    assert rows[0]["module_id"].startswith("sfp_")
    assert rows[0]["test_count"] >= 1


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
    assert detail.test_count == len(detail.tests)
    assert detail.test_count < detail.route_count
    assert detail.tests[0].test_state == "not-started"


def test_tests_plan(api_client):
    r = api_client.get("/api/v1/tests/plan", params={"limit": 200, "offset": 0})
    assert r.status_code == 200
    body = r.json()
    assert body["test_count"] == len(body["items"])
    assert body["test_count"] > 0
    assert body["items"][0]["module_id"].startswith("sfp_")
    assert "consumed_nugget_id" in body["items"][0]
    assert "input_value" in body["items"][0]
    assert "requires_api_key" in body["items"][0]
    assert "has_api_key" in body["items"][0]
    assert "skip_reason" in body["items"][0]


def test_tests_plan_search(api_client):
    r = api_client.get("/api/v1/tests/plan", params={"search": "abstractapi", "limit": 50})
    assert r.status_code == 200
    body = r.json()
    assert body["test_count"] >= 4
    assert all("abstractapi" in row["module_id"] for row in body["items"])


def test_tests_plan_marks_missing_keys(api_client):
    r = api_client.get("/api/v1/tests/plan", params={"search": "emailrep", "limit": 20})
    assert r.status_code == 200
    body = r.json()
    assert body["items"]
    for item in body["items"]:
        assert item["requires_api_key"] is True
        assert item["has_api_key"] is False
        assert item["skip_reason"] == "missing-api-key"
        assert item["subscription_tier"] in ("free_auth", "paid_auth")


def test_tests_plan_threatjammer_not_runnable_without_key(api_client):
    r = api_client.get("/api/v1/tests/plan", params={"search": "threatjammer", "limit": 20})
    assert r.status_code == 200
    body = r.json()
    assert body["items"]
    for item in body["items"]:
        assert item["requires_api_key"] is True
        assert item["has_api_key"] is False
        assert item["skip_reason"] == "missing-api-key"
        assert item["subscription_tier"] == "free_auth"


def test_tests_plan_duckduckgo_open_tier(api_client):
    r = api_client.get("/api/v1/tests/plan", params={"search": "duckduckgo", "limit": 20})
    assert r.status_code == 200
    body = r.json()
    assert body["items"]
    for item in body["items"]:
        assert item["subscription_tier"] == "none"
        assert item["requires_api_key"] is False
        assert item["skip_reason"] is None


def test_tests_modules_subscription_fields(api_client):
    r = api_client.get("/api/v1/tests/modules", params={"search": "duckduckgo", "limit": 5})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) >= 1
    assert rows[0]["subscription_tier"] == "none"
    assert rows[0]["requires_api_key"] is False
    assert rows[0]["has_api_key"] is True


def test_tests_nugget_samples(api_client):
    r = api_client.get("/api/v1/tests/nugget-samples")
    assert r.status_code == 200
    body = r.json()
    assert "INTERNET_NAME" in body["samples"]
    assert body["samples"]["INTERNET_NAME"] == "sbs.com.au"


def test_tests_module_detail_includes_input_value(api_client):
    r = api_client.get("/api/v1/tests/modules/sfp_abstractapi")
    assert r.status_code == 200
    detail = r.json()
    assert detail["tests"]
    domain_tests = [
        row for row in detail["tests"] if row["consumed_nugget_id"] == "DOMAIN_NAME"
    ]
    assert len(domain_tests) == 1
    assert domain_tests[0]["input_value"] == "sbs.com.au"
    assert "expected_produced" not in domain_tests[0]


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
    assert body["test_states"]["in_test"] >= 1
