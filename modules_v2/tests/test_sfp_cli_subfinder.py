"""AK4 / R10-15 — sfp_cli_subfinder four-output contract (fixture JSON path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_subfinder import sfp_cli_subfinder

FIXTURE_JSON = Path(__file__).resolve().parent / "fixtures" / "subfinder_vcof_sparse.json"


def test_import_clean() -> None:
    import modules_v2.sfp_cli_subfinder as mod

    assert mod.MODULE_ID == "sfp_cli_subfinder"
    assert callable(mod.run)


def test_run_from_fixture_json_four_forms() -> None:
    raw = FIXTURE_JSON.read_text(encoding="utf-8")
    result = sfp_cli_subfinder().run(
        {
            "json_text": raw,
            "scenario_key": "corporate_vcof_sparse_passive",
            "domain": "venturecapitalopportunitiesfund.com.au",
        }
    )

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "json"
    assert isinstance(result["structured"], dict)
    assert result["structured"].get("schema") == "subfinder_host_v1"
    records = result["structured"].get("records") or []
    assert len(records) == 1

    assert isinstance(result["text"], str) and result["text"].strip()
    assert "www.venturecapitalopportunitiesfund.com.au" in result["text"]
    assert "crtsh" in result["text"]
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

    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_oj_flag() -> None:
    mod = sfp_cli_subfinder()
    argv = mod.build_argv(
        {
            "domain": "example.com",
            "args": ["-silent"],
            "executable_prefix": ["subfinder"],
        }
    )
    assert argv[:1] == ["subfinder"]
    assert "-oJ" in argv
    assert "-d" in argv
    assert argv[argv.index("-d") + 1] == "example.com"


def test_build_argv_active_injects_flags() -> None:
    mod = sfp_cli_subfinder()
    argv = mod.build_argv(
        {
            "domain": "example.com",
            "active": True,
            "executable_prefix": ["subfinder"],
        }
    )
    assert "-active" in argv
    assert "-oI" in argv
    assert "-oJ" in argv


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("subfinder -d example.com -oJ")  # type: ignore[arg-type]


def test_no_cli_corpus_imports() -> None:
    import modules_v2.adapters.subfinder as adapter
    import modules_v2.adapters.subfinder.hooks as hooks
    import modules_v2.adapters.subfinder.structured as structured
    import modules_v2.sfp_cli_subfinder as mod

    for module in (mod, adapter, hooks, structured):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert "cli_corpus" not in src
        assert "seed.scripts" not in src
