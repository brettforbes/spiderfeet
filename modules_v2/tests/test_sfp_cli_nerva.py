"""AK2 / R10-15 — sfp_cli_nerva four-output contract (fixture JSON path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_nerva import sfp_cli_nerva

FIXTURE_JSON = Path(__file__).resolve().parent / "fixtures" / "nerva_scanme_80.json"


def test_import_clean() -> None:
    import modules_v2.sfp_cli_nerva as mod

    assert mod.MODULE_ID == "sfp_cli_nerva"
    assert callable(mod.run)


def test_run_from_fixture_json_four_forms() -> None:
    raw = FIXTURE_JSON.read_text(encoding="utf-8")
    result = sfp_cli_nerva().run(
        {"json_text": raw, "scenario_key": "tcp_http_rich_json", "target": "scanme.nmap.org:80"}
    )

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "json"
    assert isinstance(result["structured"], dict)
    assert result["structured"].get("schema") == "nerva_fingerprint_v1"
    records = result["structured"].get("records") or []
    assert len(records) == 2

    assert isinstance(result["text"], str) and result["text"].strip()
    assert "http://scanme.nmap.org:80" in result["text"]
    assert isinstance(result["narrative"], str) and result["narrative"].strip()
    assert isinstance(result["graph"], dict)
    assert isinstance(result["graph"].get("nodes"), list)
    assert isinstance(result["graph"].get("edges"), list)
    assert result["counts"]["nodes"] >= 1
    assert result["duration"] >= 0
    assert result["timestamp"]

    for node in result["graph"]["nodes"]:
        assert node.get("nugget_id") != "IP_ADDRESS"

    ipv4 = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "IPV4_ADDRESS"]
    ipv6 = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "IPV6_ADDRESS"]
    assert any(n["nugget_data"] == "45.33.32.156" for n in ipv4)
    assert any(":" in n["nugget_data"] for n in ipv6)

    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_json_flag() -> None:
    mod = sfp_cli_nerva()
    argv = mod.build_argv(
        {
            "target": "scanme.nmap.org:80",
            "args": ["-w", "5000"],
            "executable_prefix": ["nerva"],
        }
    )
    assert argv[:1] == ["nerva"]
    assert "--json" in argv
    assert "-t" in argv
    assert argv[argv.index("-t") + 1] == "scanme.nmap.org:80"


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("nerva -t scanme.nmap.org:80 --json")  # type: ignore[arg-type]



def test_output_file_from_argv() -> None:
    from modules_v2.sfp_cli_nerva import _output_file_from_argv

    assert _output_file_from_argv(["nerva", "--json", "-o", "out.jsonl", "-t", "h:80"]) == "out.jsonl"
    assert _output_file_from_argv(["nerva", "--json", "--output", "out.jsonl"]) == "out.jsonl"
    assert _output_file_from_argv(["nerva", "--json", "-t", "h:80"]) is None

def test_run_hydrates_jsonl_from_output_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Workflow ``--output`` must not treat empty stdout as a clean-miss SUCCESS."""
    from types import SimpleNamespace

    import json

    from modules_v2._base import STATUS_SUCCESS

    record = {
        "host": "scanme.nmap.org",
        "ip": "45.33.32.156",
        "port": 80,
        "protocol": "http",
        "tls": False,
        "transport": "tcp",
    }
    out_path = tmp_path / "nerva_out.jsonl"
    out_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    argv = ["nerva", "--json", "-t", "scanme.nmap.org:80", "-o", str(out_path)]

    completed = SimpleNamespace(stdout="", stderr="", returncode=0)

    mod = sfp_cli_nerva()
    monkeypatch.setattr(
        mod,
        "_timed_run_argv",
        lambda _argv, timeout=120.0: (completed, 0.5, None),
    )
    monkeypatch.setattr(mod, "build_argv", lambda _spec: list(argv))

    result = mod.run({"argv": argv, "timeout": 30})
    assert result["status"] == STATUS_SUCCESS
    assert result["graph"]["nodes"]
    assert result["structured"].get("records")

def test_run_errors_when_stdout_and_output_file_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from types import SimpleNamespace

    from modules_v2._base import STATUS_ERROR

    out_path = tmp_path / "empty.jsonl"
    out_path.write_text("", encoding="utf-8")
    argv = ["nerva", "--json", "-t", "scanme.nmap.org:80", "-o", str(out_path)]

    completed = SimpleNamespace(stdout="", stderr="", returncode=0)

    mod = sfp_cli_nerva()
    monkeypatch.setattr(
        mod,
        "_timed_run_argv",
        lambda _argv, timeout=120.0: (completed, 0.5, None),
    )
    monkeypatch.setattr(mod, "build_argv", lambda _spec: list(argv))

    result = mod.run({"argv": argv, "timeout": 30})
    assert result["status"] == STATUS_ERROR
    assert "no output" in (result.get("error") or "").lower()

def test_no_cli_corpus_imports() -> None:
    import modules_v2.adapters.nerva as adapter
    import modules_v2.adapters.nerva.hooks as hooks
    import modules_v2.adapters.nerva.structured as structured
    import modules_v2.sfp_cli_nerva as mod

    for module in (mod, adapter, hooks, structured):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert "cli_corpus" not in src
        assert "seed.scripts" not in src
