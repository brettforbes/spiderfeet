"""AK1 / R10-15 — sfp_cli_netdiscover four-output contract (fixture text path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_netdiscover import sfp_cli_netdiscover

FIXTURE_TEXT = Path(__file__).resolve().parent / "fixtures" / "netdiscover_local_subnet_fast.txt"


def test_import_clean() -> None:
    import modules_v2.sfp_cli_netdiscover as mod

    assert mod.MODULE_ID == "sfp_cli_netdiscover"
    assert callable(mod.run)


def test_run_from_fixture_text_four_forms() -> None:
    raw_text = FIXTURE_TEXT.read_text(encoding="utf-8")
    result = sfp_cli_netdiscover().run(
        {"text": raw_text, "scenario_key": "local_subnet_fast_parsable"}
    )

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "json"
    assert isinstance(result["structured"], dict)
    assert "netdiscover_scan" in result["structured"]
    systems = result["structured"]["netdiscover_scan"]["systems"]
    assert len(systems) == 1
    assert systems[0]["ipv4"] == "192.168.1.1"

    assert isinstance(result["text"], str) and result["text"].strip()
    assert isinstance(result["narrative"], str) and result["narrative"].strip()
    assert isinstance(result["graph"], dict)
    assert isinstance(result["graph"].get("nodes"), list)
    assert isinstance(result["graph"].get("edges"), list)
    assert result["counts"]["nodes"] >= 1
    assert result["duration"] >= 0
    assert result["timestamp"]

    for node in result["graph"]["nodes"]:
        assert node.get("nugget_id") != "IP_ADDRESS"
        if node.get("nugget_id") in {"IPV4_ADDRESS", "IPV6_ADDRESS"}:
            assert ":" not in node["nugget_data"] or node["nugget_id"] == "IPV6_ADDRESS"

    ipv4_nodes = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "IPV4_ADDRESS"]
    assert any(n["nugget_data"] == "192.168.1.1" for n in ipv4_nodes)

    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_parsable_flag() -> None:
    mod = sfp_cli_netdiscover()
    argv = mod.build_argv(
        {
            "range": "192.168.1.0/24",
            "args": ["-N", "-f"],
            "executable_prefix": ["netdiscover"],
        }
    )
    assert argv[:1] == ["netdiscover"]
    assert "-P" in argv
    assert "-r" in argv
    assert argv[argv.index("-r") + 1] == "192.168.1.0/24"


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("netdiscover -P -r 192.168.1.0/24")  # type: ignore[arg-type]


def test_no_cli_corpus_imports() -> None:
    import modules_v2.adapters.netdiscover as adapter
    import modules_v2.adapters.netdiscover.text_to_json as text_to_json
    import modules_v2.sfp_cli_netdiscover as mod

    for module in (mod, adapter, text_to_json):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert "cli_corpus" not in src
        assert "seed.scripts" not in src
