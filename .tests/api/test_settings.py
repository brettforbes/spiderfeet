"""Settings API tests."""

def test_settings_cli_apps_list(api_client):
    r = api_client.get("/api/v1/settings/cli-apps")
    assert r.status_code == 200
    apps = r.json()
    assert any(row["tool_id"] == "pius" for row in apps)


def test_settings_ai_agents_crud(api_client):
    create = api_client.post(
        "/api/v1/settings/ai-agents",
        json={"label": "Test OpenAI", "provider": "openai", "model": "gpt-4o", "api_key": "sk-test-redteam"},
    )
    assert create.status_code == 200
    body = create.json()
    assert body["has_api_key"] is True
    assert "sk-test-redteam" not in str(body)
    agent_id = body["id"]

    listed = api_client.get("/api/v1/settings/ai-agents")
    assert any(row["id"] == agent_id for row in listed.json())

    api_client.delete(f"/api/v1/settings/ai-agents/{agent_id}")
