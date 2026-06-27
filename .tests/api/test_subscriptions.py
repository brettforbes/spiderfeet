"""Unit tests for Subscriptions API."""


def test_subscriptions_modules_list(api_client):
    r = api_client.get("/api/v1/subscriptions/modules", params={"limit": 10})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 10
    assert rows[0]["requires_api_key"] is True
    assert "secret_opts" in rows[0]
    assert "subscription_tier" in rows[0]
    assert "signup_url" in rows[0]
    assert "signup_bucket" in rows[0]
    assert "provider_kind" in rows[0]
    assert "service_labels" in rows[0]
    assert "group" in rows[0]


def test_subscriptions_filter_cli_pius(api_client):
    r = api_client.get(
        "/api/v1/subscriptions/modules",
        params={"cli_app": "pius", "limit": 500},
    )
    assert r.status_code == 200
    rows = r.json()
    assert rows
    assert all("pius" in (row.get("cli_apps") or []) for row in rows)


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
    assert body["signup_bucket"] == "manual"
    assert body["signup_url"]
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


def test_subscriptions_never_leaks_plaintext_secret(api_client):
    import json

    module_id = "sfp_emailrep"
    secret = "redteam-emailrep-secret-xyzzy"
    try:
        put = api_client.put(
            f"/api/v1/subscriptions/modules/{module_id}",
            json={"secrets": {"api_key": secret}},
        )
        assert put.status_code == 200
        assert secret not in json.dumps(put.json())
    finally:
        api_client.put(
            f"/api/v1/subscriptions/modules/{module_id}",
            json={"secrets": {"api_key": ""}},
        )


def test_subscriptions_db_encrypts_module_secret(api_client):
    from spiderfeet import SpiderFeetDb
    from spiderfeet.api.bootstrap import get_runtime
    from spiderfeet.credentials.vault import is_encrypted

    module_id = "sfp_emailrep"
    secret = "redteam-db-encryption-check"
    runtime = get_runtime()
    try:
        api_client.put(
            f"/api/v1/subscriptions/modules/{module_id}",
            json={"secrets": {"api_key": secret}},
        )
        raw = SpiderFeetDb(runtime.config).configGet().get(f"{module_id}:api_key", "")
        assert secret not in str(raw)
        assert is_encrypted(str(raw))
    finally:
        api_client.put(
            f"/api/v1/subscriptions/modules/{module_id}",
            json={"secrets": {"api_key": ""}},
        )


def test_subscriptions_cli_only_providers(api_client):
    r = api_client.get("/api/v1/subscriptions/modules", params={"group": "cli", "limit": 500})
    assert r.status_code == 200
    ids = {row["module_id"] for row in r.json()}
    for expected in ("cli_pius_apollo", "cli_pius_viewdns", "cli_pius_fofa", "cli_pius_github"):
        assert expected in ids


def test_subscriptions_save_syncs_pius_env(api_client):
    from spiderfeet.credentials.registry import REPO_ROOT

    secret = "redteam-shodan-for-pius-sync"
    try:
        put = api_client.put(
            "/api/v1/subscriptions/modules/sfp_shodan",
            json={"secrets": {"api_key": secret}},
        )
        assert put.status_code == 200
        env_path = REPO_ROOT / ".tools" / "pius.env"
        assert env_path.is_file()
        assert secret in env_path.read_text(encoding="utf-8")
    finally:
        api_client.put(
            "/api/v1/subscriptions/modules/sfp_shodan",
            json={"secrets": {"api_key": ""}},
        )
