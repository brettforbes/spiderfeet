"""Tests for generate_options_schema.py (SPEC-008 V1)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GEN = REPO_ROOT / ".seed" / "scripts" / "cli_corpus" / "generate_options_schema.py"


def _run(tool: str, output_dir: Path) -> dict:
    subprocess.run(
        [sys.executable, str(GEN), "--tool", tool, "--output-dir", str(output_dir)],
        check=True,
    )
    return json.loads((output_dir / "options_schema.json").read_text(encoding="utf-8"))


def test_generate_nmap_schema_has_flags(tmp_path):
    schema = _run("nmap", tmp_path / "nmap")
    assert schema["tool_id"] == "nmap"
    assert schema["groups"]
    assert len(schema["flags"]) >= 10
    target = next(f for f in schema["flags"] if f["id"] == "target")
    assert target["required"] is True
    assert target["type"] == "string"
    for flag in schema["flags"]:
        assert flag.get("description")
        if flag["type"] == "select":
            assert flag["choices"]


def test_generate_httpx_schema_has_double_dash_flags(tmp_path):
    schema = _run("httpx", tmp_path / "httpx")
    assert schema["tool_id"] == "httpx"
    assert len(schema["flags"]) >= 5
    flag_names = {f["flag"] for f in schema["flags"] if f.get("flag")}
    assert any(str(f).startswith("--") or str(f).startswith("-") for f in flag_names)
    for flag in schema["flags"]:
        assert flag.get("description")
        assert flag.get("group") in schema["groups"]
