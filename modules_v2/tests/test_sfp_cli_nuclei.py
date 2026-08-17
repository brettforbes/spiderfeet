"""AK7 / R10-15 — sfp_cli_nuclei four-output contract (fixture JSON path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_nuclei import sfp_cli_nuclei

FIXTURE_JSON = (
    Path(__file__).resolve().parent / "fixtures" / "nuclei_cipherheart_redis_lab.json"
)


def test_import_clean() -> None:
    import modules_v2.sfp_cli_nuclei as mod

    assert mod.MODULE_ID == "sfp_cli_nuclei"
    assert callable(mod.run)


def test_run_from_fixture_json_four_forms() -> None:
    raw = FIXTURE_JSON.read_text(encoding="utf-8")
    result = sfp_cli_nuclei().run(
        {
            "json_text": raw,
            "scenario_key": "cipherheart_redis_lab",
            "target": "pentest-ground.com:6379",
        }
    )

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "json"
    assert isinstance(result["structured"], dict)
    assert result["structured"].get("schema") == "nuclei_finding_v1"
    records = result["structured"].get("records") or []
    assert len(records) == 2

    assert isinstance(result["text"], str) and result["text"].strip()
    assert "CVE-2022-0543" in result["text"]
    assert "exposed-redis" in result["text"]
    assert isinstance(result["narrative"], str) and result["narrative"].strip()
    assert isinstance(result["graph"], dict)
    assert isinstance(result["graph"].get("nodes"), list)
    assert isinstance(result["graph"].get("edges"), list)
    assert result["counts"]["nodes"] >= 1
    assert result["duration"] >= 0
    assert result["timestamp"]

    for node in result["graph"]["nodes"]:
        assert node.get("nugget_id") != "IP_ADDRESS"

    hosts = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "HOST"]
    assert any(n["nugget_data"] == "pentest-ground.com" for n in hosts)
    assert any(
        n["nugget_id"] == "VULNERABILITY_CVE_CRITICAL"
        and "CVE-2022-0543" in str(n.get("nugget_data", "")).upper()
        for n in result["graph"]["nodes"]
    )

    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_jsonl_and_safe_defaults() -> None:
    mod = sfp_cli_nuclei()
    argv = mod.build_argv(
        {
            "url": "https://scanme.nmap.org",
            "args": ["-tags", "tech"],
            "executable_prefix": ["nuclei"],
            "templates": "C:\\templates",
        }
    )
    assert argv[:1] == ["nuclei"]
    assert "-jsonl" in argv
    assert "-silent" in argv
    assert "-no-interactsh" in argv
    assert "-etags" in argv
    assert "-u" in argv
    assert argv[argv.index("-u") + 1] == "https://scanme.nmap.org"
    assert "-t" in argv
    assert argv[argv.index("-t") + 1] == "C:\\templates"


def test_build_argv_host_list() -> None:
    mod = sfp_cli_nuclei()
    argv = mod.build_argv(
        {
            "host_list": "hosts.txt",
            "executable_prefix": ["nuclei"],
            "templates": "C:\\templates",
        }
    )
    assert "-jsonl" in argv
    assert "-l" in argv
    assert argv[argv.index("-l") + 1] == "hosts.txt"


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("nuclei -u example.com -jsonl")  # type: ignore[arg-type]


def test_no_cli_corpus_imports() -> None:
    import modules_v2.adapters.nuclei as adapter
    import modules_v2.adapters.nuclei.hooks as hooks
    import modules_v2.adapters.nuclei.structured as structured
    import modules_v2.sfp_cli_nuclei as mod

    for module in (mod, adapter, hooks, structured):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert "cli_corpus" not in src
        assert "seed.scripts" not in src


def test_collect_urls_and_batch_planning_forty_five_r19_07() -> None:
    """R19-07: 45 URLs in spec yields 3 target chunks (batch size 20)."""
    from modules_v2.sfp_cli_nuclei import (
        DEFAULT_BATCH_SIZE,
        _collect_urls,
        chunk_targets,
        plan_batch_jobs,
    )

    urls = [f"https://host{i}.example" for i in range(45)]
    spec = {"urls": urls, "target": urls[0], "domain": urls[0]}
    collected = _collect_urls(spec)
    assert collected == urls
    chunks = chunk_targets(collected, batch_size=DEFAULT_BATCH_SIZE)
    assert len(chunks) == 3
    assert sum(len(c) for c in chunks) == 45
    jobs = plan_batch_jobs(collected, batch_size=DEFAULT_BATCH_SIZE)
    assert len(jobs) == 3
