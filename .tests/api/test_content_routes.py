"""Content platform API routes (SPEC-008 W1/W2)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from spiderfeet.api.bootstrap import REPO_ROOT
from spiderfeet.api.services import content as content_service


@pytest.fixture(autouse=True)
def _clear_content_cache():
    content_service.invalidate_cache()
    yield
    content_service.invalidate_cache()


def test_content_tools_lists_adapter_tools(api_client: TestClient):
    response = api_client.get("/api/v1/content/tools")
    assert response.status_code == 200
    body = response.json()
    assert "tools" in body
    ids = {t["tool_id"] for t in body["tools"]}
    assert "nmap" in ids
    assert "httpx" in ids
    assert body["total"] >= 8


def test_content_tools_pagination(api_client: TestClient, tmp_path, monkeypatch):
    root = tmp_path / "content"
    for i in range(3):
        bundle = root / f"tool{i}"
        bundle.mkdir(parents=True)
        (bundle / "manifest.json").write_text(
            json.dumps(
                {
                    "tool_id": f"tool{i}",
                    "display_name": f"Tool {i}",
                    "kind": "cli",
                    "category": "test",
                    "executable": f"tool{i}",
                    "content_version": 1,
                }
            ),
            encoding="utf-8",
        )
    monkeypatch.setattr(content_service, "_CONTENT_ROOT", root)
    content_service.invalidate_cache()
    response = api_client.get("/api/v1/content/tools?limit=2&offset=1")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert len(body["tools"]) == 2
    assert body["offset"] == 1


def test_content_nmap_manifest(api_client: TestClient):
    response = api_client.get("/api/v1/content/tools/nmap")
    assert response.status_code == 200
    body = response.json()
    assert body["tool_id"] == "nmap"
    assert body["executable"] == "nmap"


def test_content_nmap_options_schema(api_client: TestClient):
    response = api_client.get("/api/v1/content/tools/nmap/options-schema")
    assert response.status_code == 200
    schema = response.json()
    assert schema["tool_id"] == "nmap"
    assert len(schema["flags"]) >= 10


def test_content_nmap_markdown_docs(api_client: TestClient):
    for path in ("options", "zero-to-hero", "graph-structure"):
        response = api_client.get(f"/api/v1/content/tools/nmap/{path}")
        assert response.status_code == 200
        body = response.json()
        assert body["markdown"].strip()


def test_content_unknown_tool_404(api_client: TestClient):
    response = api_client.get("/api/v1/content/tools/not-a-real-tool-xyz/options-schema")
    assert response.status_code == 404


def test_content_bundles_exist_on_disk():
    root = REPO_ROOT / "modules_v2" / "content"
    for tool_id in ("nmap", "netdiscover", "nerva", "pius", "subfinder", "httpx", "katana", "nuclei"):
        bundle = root / tool_id
        for name in (
            "manifest.json",
            "options.md",
            "options_schema.json",
            "zero_to_hero.md",
            "graph_structure.md",
        ):
            assert (bundle / name).is_file(), f"{tool_id}/{name} missing"
