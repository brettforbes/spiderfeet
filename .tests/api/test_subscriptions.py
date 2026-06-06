"""Unit tests for Subscriptions API."""


def test_subscriptions_modules_list(api_client):
    r = api_client.get("/api/v1/subscriptions/modules", params={"limit": 10})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 10
    assert rows[0]["requires_api_key"] is True
    assert "secret_opts" in rows[0]
    assert "subscription_tier" in rows[0]


def test_subscriptions_modules_search(api_client):
    r = api_client.get(
        "/api/v1/subscriptions/modules",
        params={"search": "emailrep", "limit": 5},
    )
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) >= 1
    assert rows[0]["module_id"] == "sfp_emailrep"
    assert rows[0]["has_api_key"] is False


def test_subscriptions_module_detail(api_client):
    r = api_client.get("/api/v1/subscriptions/modules/sfp_emailrep")
    assert r.status_code == 200
    body = r.json()
    assert body["module_id"] == "sfp_emailrep"
    assert body["requires_api_key"] is True
    assert "EMAILADDR" in body["consumed_nuggets"]
    assert any(opt["name"] == "api_key" for opt in body["secret_opts"])


def test_subscriptions_module_not_found(api_client):
    r = api_client.get("/api/v1/subscriptions/modules/sfp_not_a_real_module")
    assert r.status_code == 404


def test_subscriptions_set_key_updates_plan(api_client):
    module_id = "sfp_emailrep"
    test_key = "test-emailrep-key-1234"

    try:
        put = api_client.put(
            f"/api/v1/subscriptions/modules/{module_id}",
            json={"secrets": {"api_key": test_key}},
        )
        assert put.status_code == 200
        detail = put.json()
        assert detail["has_api_key"] is True
        masked = detail["secret_opts"][0]["masked_value"]
        assert masked.endswith("1234")
        assert test_key not in str(detail)

        plan = api_client.get(
            "/api/v1/tests/plan",
            params={"search": "emailrep", "limit": 20},
        )
        assert plan.status_code == 200
        items = plan.json()["items"]
        assert items
        for item in items:
            assert item["has_api_key"] is True
            assert item["skip_reason"] is None
    finally:
        api_client.put(
            f"/api/v1/subscriptions/modules/{module_id}",
            json={"secrets": {"api_key": ""}},
        )


def test_subscriptions_rejects_non_secret_opt(api_client):
    r = api_client.put(
        "/api/v1/subscriptions/modules/sfp_threatjammer",
        json={"secrets": {"api_hostname": "evil.example"}},
    )
    assert r.status_code == 422


def test_subscriptions_clear_key(api_client):
    module_id = "sfp_emailrep"
    api_client.put(
        f"/api/v1/subscriptions/modules/{module_id}",
        json={"secrets": {"api_key": "temporary-key-9999"}},
    )
    cleared = api_client.put(
        f"/api/v1/subscriptions/modules/{module_id}",
        json={"secrets": {"api_key": ""}},
    )
    assert cleared.status_code == 200
    assert cleared.json()["has_api_key"] is False
    assert cleared.json()["secret_opts"][0]["configured"] is False
