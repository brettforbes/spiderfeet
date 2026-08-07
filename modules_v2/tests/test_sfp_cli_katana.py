"""AK6 / R10-15 — sfp_cli_katana four-output contract (fixture JSON path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_katana import sfp_cli_katana

FIXTURE_JSON = Path(__file__).resolve().parent / "fixtures" / "katana_upside_sample.json"


def test_import_clean() -> None:
    import modules_v2.sfp_cli_katana as mod

    assert mod.MODULE_ID == "sfp_cli_katana"
    assert callable(mod.run)


def test_run_from_fixture_json_four_forms() -> None:
    raw = FIXTURE_JSON.read_text(encoding="utf-8")
    result = sfp_cli_katana().run(
        {
            "json_text": raw,
            "scenario_key": "from_httpx_upside_com_sample",
            "target": "theupside.com",
        }
    )

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "json"
    assert isinstance(result["structured"], dict)
    assert result["structured"].get("schema") == "katana_crawl_v1"
    records = result["structured"].get("records") or []
    assert len(records) == 3

    assert isinstance(result["text"], str) and result["text"].strip()
    assert "https://uat.theupside.com" in result["text"]
    assert "method=GET" in result["text"]
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
    assert any(n["nugget_data"] == "theupside.com" for n in domains)
    assert any(n["nugget_data"] == "uat.theupside.com" for n in domains)

    urls = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "LINKED_URL_INTERNAL"]
    assert any(n["nugget_data"] == "https://uat.theupside.com" for n in urls)

    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_jsonl_flag() -> None:
    mod = sfp_cli_katana()
    argv = mod.build_argv(
        {
            "url": "https://example.com",
            "args": ["-depth", "1", "-ct", "10s"],
            "executable_prefix": ["katana"],
        }
    )
    assert argv[:1] == ["katana"]
    assert "-jsonl" in argv
    assert "-silent" in argv
    assert "-u" in argv
    assert argv[argv.index("-u") + 1] == "https://example.com"


def test_build_argv_url_list() -> None:
    mod = sfp_cli_katana()
    argv = mod.build_argv(
        {
            "url_list": "urls.txt",
            "executable_prefix": ["katana"],
        }
    )
    assert "-jsonl" in argv
    assert "-list" in argv
    assert argv[argv.index("-list") + 1] == "urls.txt"


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("katana -u https://example.com -jsonl")  # type: ignore[arg-type]


def test_no_cli_corpus_imports() -> None:
    import modules_v2.adapters.katana as adapter
    import modules_v2.adapters.katana.hooks as hooks
    import modules_v2.adapters.katana.structured as structured
    import modules_v2.sfp_cli_katana as mod

    for module in (mod, adapter, hooks, structured):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert "cli_corpus" not in src
        assert "seed.scripts" not in src
