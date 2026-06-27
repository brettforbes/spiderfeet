"""CLI corpus API endpoints (profiling review UI)."""

import pytest
from fastapi.testclient import TestClient


def test_cli_corpus_config(api_client: TestClient):
    response = api_client.get("/api/v1/cli-corpus/config")
    assert response.status_code == 200
    body = response.json()
    assert "data_viewer_url" in body
    assert body["data_viewer_url"].endswith("/widget")


def test_cli_corpus_tools_lists_indexed_tools(api_client: TestClient):
    response = api_client.get("/api/v1/cli-corpus/tools")
    assert response.status_code == 200
    tools = response.json()
    ids = {t["id"] for t in tools}
    assert "nmap" in ids
    nmap = next(t for t in tools if t["id"] == "nmap")
    assert nmap["phase"] == "complete"
    assert nmap["exam_count"] >= 15
    assert nmap["has_graph_structure"] is True


def test_cli_corpus_scenarios_lists_nmap_archetypes(api_client: TestClient):
    response = api_client.get("/api/v1/cli-corpus/tools/nmap/scenarios")
    assert response.status_code == 200
    scenarios = response.json()
    assert len(scenarios) >= 15
    keys = {s["scenario_key"] for s in scenarios}
    assert "host_discovery_permissive" in keys
    assert "capstone_permissive" in keys
    for row in scenarios:
        assert row.get("has_text") or row.get("has_structured")


def test_cli_corpus_nmap_scenarios_operator_approved(api_client: TestClient):
    response = api_client.get("/api/v1/cli-corpus/tools/nmap/scenarios")
    assert response.status_code == 200
    scenarios = response.json()
    assert len(scenarios) >= 15
    assert all(row["review_status"] == "approved" for row in scenarios)
    assert all(row["complete"] for row in scenarios)


def test_cli_corpus_scenario_detail_missing_returns_404(api_client: TestClient):
    response = api_client.get("/api/v1/cli-corpus/tools/nmap/scenarios/nonexistent_scenario_key")
    assert response.status_code == 404


def test_cli_corpus_scenario_detail_host_discovery(api_client: TestClient):
    response = api_client.get("/api/v1/cli-corpus/tools/nmap/scenarios/host_discovery_permissive")
    assert response.status_code == 200
    body = response.json()
    assert body["tool_id"] == "nmap"
    assert body["scenario_key"] == "host_discovery_permissive"
    assert body.get("output_text") or body.get("structured")
    assert "graph_description_markdown" in body


def test_cli_corpus_tool_graph_structure(api_client: TestClient):
    response = api_client.get("/api/v1/cli-corpus/tools/nmap/graph-structure")
    assert response.status_code == 200
    body = response.json()
    assert body["tool_id"] == "nmap"
    assert body["filename"] == "nmap_nugget_graph_structure.md"
    assert "markdown" in body


@pytest.mark.skip(reason="Optional: review roundtrip mutates review.status.json on disk")
def test_cli_corpus_scenario_detail_and_review_roundtrip(api_client: TestClient):
    list_resp = api_client.get("/api/v1/cli-corpus/tools/nmap/scenarios")
    assert list_resp.status_code == 200
    scenarios = list_resp.json()
    assert scenarios
    scenario_key = scenarios[0]["scenario_key"]

    response = api_client.get(f"/api/v1/cli-corpus/tools/nmap/scenarios/{scenario_key}")
    assert response.status_code == 200
    body = response.json()
    assert body["tool_id"] == "nmap"
    assert body["scenario_key"] == scenario_key
    assert isinstance(body.get("output_text"), str)
    assert body.get("structured") is not None or body.get("output_text")
    assert "artifacts" in body

    get_resp = api_client.get(f"/api/v1/cli-corpus/tools/nmap/scenarios/{scenario_key}")
    original = get_resp.json()["review_status"]

    post_resp = api_client.post(
        f"/api/v1/cli-corpus/tools/nmap/scenarios/{scenario_key}/review",
        json={"status": "pending"},
    )
    assert post_resp.status_code == 200
    assert post_resp.json()["status"] == "pending"

    if original != "pending":
        api_client.post(
            f"/api/v1/cli-corpus/tools/nmap/scenarios/{scenario_key}/review",
            json={"status": original},
        )
