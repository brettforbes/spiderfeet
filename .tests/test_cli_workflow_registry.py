"""T1 — tool registry tests."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".seed" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import pytest

from cli_workflow.tools.registry import FixtureDriver, get, parse_uses, register  # noqa: E402


def test_registry_roundtrip():
    register(FixtureDriver(tool_id="nmap", scan_graph={"nodes": [], "edges": []}))
    assert get("nmap").run([])["scan_graph"]["nodes"] == []
    assert parse_uses("tool.httpx") == "httpx"


def test_unknown_tool_raises():
    with pytest.raises(KeyError):
        get("not_registered_tool_xyz")
