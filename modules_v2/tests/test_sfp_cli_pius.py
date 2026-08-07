"""AK3 / R10-15 — sfp_cli_pius four-output contract (fixture JSON path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_pius import sfp_cli_pius

FIXTURE_JSON = Path(__file__).resolve().parent / "fixtures" / "pius_squarepeg.json"


def test_import_clean() -> None:
    import modules_v2.sfp_cli_pius as mod

    assert mod.MODULE_ID == "sfp_cli_pius"
    assert callable(mod.run)


def test_run_from_fixture_json_four_forms() -> None:
    raw = FIXTURE_JSON.read_text(encoding="utf-8")
    result = sfp_cli_pius().run(
        {
            "json_text": raw,
            "scenario_key": "corporate_squarepeg_ndjson",
            "org": "Square Peg Capital Pty Ltd",
            "domain": "squarepeg.vc",
        }
    )

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "json"
    assert isinstance(result["structured"], dict)
    assert result["structured"].get("schema") == "pius_finding_v1"
    records = result["structured"].get("records") or []
    assert len(records) == 6

    assert isinstance(result["text"], str) and result["text"].strip()
    assert "[domain] squarepeg.vc (crt-sh)" in result["text"]
    assert isinstance(result["narrative"], str) and result["narrative"].strip()
    assert isinstance(result["graph"], dict)
    assert isinstance(result["graph"].get("nodes"), list)
    assert isinstance(result["graph"].get("edges"), list)
    assert result["counts"]["nodes"] >= 1
    assert result["duration"] >= 0
    assert result["timestamp"]

    for node in result["graph"]["nodes"]:
        assert node.get("nugget_id") != "IP_ADDRESS"

    companies = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "COMPANY_NAME"]
    domains = [n for n in result["graph"]["nodes"] if n.get("nugget_id") == "DOMAIN_NAME"]
    assert any(n["nugget_data"] == "Square Peg Capital Pty Ltd" for n in companies)
    assert any(n["nugget_data"] == "squarepeg.vc" for n in domains)

    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_ndjson_output() -> None:
    mod = sfp_cli_pius()
    argv = mod.build_argv(
        {
            "org": "Square Peg Capital Pty Ltd",
            "domain": "squarepeg.vc",
            "args": ["--plugins", "crt-sh"],
            "executable_prefix": ["pius"],
        }
    )
    assert argv[:1] == ["pius"]
    assert argv[1] == "run"
    assert "--output" in argv
    assert argv[argv.index("--output") + 1] == "ndjson"
    assert "--org" in argv
    assert argv[argv.index("--org") + 1] == "Square Peg Capital Pty Ltd"
    assert "--domain" in argv
    assert argv[argv.index("--domain") + 1] == "squarepeg.vc"


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("pius run --org Acme --output ndjson")  # type: ignore[arg-type]


def test_no_cli_corpus_imports() -> None:
    import modules_v2.adapters.pius as adapter
    import modules_v2.adapters.pius.classify as classify
    import modules_v2.adapters.pius.hooks as hooks
    import modules_v2.adapters.pius.structured as structured
    import modules_v2.sfp_cli_pius as mod

    for module in (mod, adapter, classify, hooks, structured):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert "cli_corpus" not in src
        assert "seed.scripts" not in src
