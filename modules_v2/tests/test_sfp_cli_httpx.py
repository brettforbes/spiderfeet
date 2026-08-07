"""AK5 / R10-15 — sfp_cli_httpx four-output contract (fixture JSON path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_httpx import sfp_cli_httpx

FIXTURE_JSON = Path(__file__).resolve().parent / "fixtures" / "httpx_vcof_sparse.json"


def test_import_clean() -> None:
    import modules_v2.sfp_cli_httpx as mod

    assert mod.MODULE_ID == "sfp_cli_httpx"
    assert callable(mod.run)


def test_run_from_fixture_json_four_forms() -> None:
    raw = FIXTURE_JSON.read_text(encoding="utf-8")
    result = sfp_cli_httpx().run(
        {
            "json_text": raw,
            "scenario_key": "from_subfinder_vcof_sparse",
            "target": "venturecapitalopportunitiesfund.com.au",
        }
    )

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "json"
    assert isinstance(result["structured"], dict)
    assert result["structured"].get("schema") == "httpx_probe_v1"
    records = result["structured"].get("records") or []
    assert len(records) == 1

    assert isinstance(result["text"], str) and result["text"].strip()
    assert "www.venturecapitalopportunitiesfund.com.au" in result["text"]
    assert "200" in result["text"]
    assert isinstance(result["narrative"], str) and result["narrative"].strip()
    assert isinstance(result["graph"], dict)
    assert isinstance(result["graph"].get("nodes"), list)
    assert isinstance(result["graph"].get("edges"), list)
    assert result["counts"]["nodes"] >= 1
    assert result["duration"] >= 0
    assert result["timestamp"]

    for node in result["graph"]["nodes"]:
        assert node.get("nugget_id") != "IP_ADDRESS"

    domains = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "DOMAIN_NAME"]
    assert any(n["nugget_data"] == "venturecapitalopportunitiesfund.com.au" for n in domains)
    assert any(
        n["nugget_data"] == "www.venturecapitalopportunitiesfund.com.au" for n in domains
    )

    ipv4 = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "IPV4_ADDRESS"]
    assert ipv4, "expected IPV4_ADDRESS nodes from A records"

    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_json_flag() -> None:
    mod = sfp_cli_httpx()
    argv = mod.build_argv(
        {
            "url": "https://scanme.nmap.org",
            "args": ["-silent", "-status-code"],
            "executable_prefix": ["httpx"],
        }
    )
    assert argv[:1] == ["httpx"]
    assert "-json" in argv
    assert "-no-stdin" in argv
    assert "-u" in argv
    assert argv[argv.index("-u") + 1] == "https://scanme.nmap.org"


def test_build_argv_host_list() -> None:
    mod = sfp_cli_httpx()
    argv = mod.build_argv(
        {
            "host_list": "hosts.txt",
            "executable_prefix": ["httpx"],
        }
    )
    assert "-json" in argv
    assert "-l" in argv
    assert argv[argv.index("-l") + 1] == "hosts.txt"


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("httpx -u example.com -json")  # type: ignore[arg-type]


def test_no_cli_corpus_imports() -> None:
    import modules_v2.adapters.httpx as adapter
    import modules_v2.adapters.httpx.hooks as hooks
    import modules_v2.adapters.httpx.structured as structured
    import modules_v2.sfp_cli_httpx as mod

    for module in (mod, adapter, hooks, structured):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert "cli_corpus" not in src
        assert "seed.scripts" not in src
