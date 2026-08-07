"""AK0 / R10-14 — sfp_cli_nmap four-output contract (fixture XML path)."""

from __future__ import annotations

from pathlib import Path

import pytest

from modules_v2._base import RESULT_KEYS, STATUS_SUCCESS, run_argv
from modules_v2.sfp_cli_nmap import sfp_cli_nmap

FIXTURE_XML = Path(__file__).resolve().parent / "fixtures" / "nmap_scanme_sn.xml"


def test_import_clean() -> None:
    import modules_v2.sfp_cli_nmap as mod

    assert mod.MODULE_ID == "sfp_cli_nmap"
    assert callable(mod.run)


def test_run_from_fixture_xml_four_forms() -> None:
    xml_text = FIXTURE_XML.read_text(encoding="utf-8")
    result = sfp_cli_nmap().run({"xml_text": xml_text, "scenario_key": "scanme_sn"})

    for key in RESULT_KEYS:
        assert key in result, f"missing contract key {key}"

    assert result["status"] == STATUS_SUCCESS
    assert result["structured_type"] == "xml"
    assert "nmaprun" in result["structured"] or "nmap" in result["structured"]
    assert isinstance(result["text"], str) and result["text"].strip()
    assert isinstance(result["narrative"], str) and result["narrative"].strip()
    assert isinstance(result["graph"], dict)
    assert isinstance(result["graph"].get("nodes"), list)
    assert isinstance(result["graph"].get("edges"), list)
    assert result["counts"]["nodes"] >= 1
    assert result["duration"] >= 0
    assert result["timestamp"]

    # No ambiguous IP_ADDRESS after Epic AH
    for node in result["graph"]["nodes"]:
        assert node.get("nugget_id") != "IP_ADDRESS"

    # Every node appears in at least one edge (no orphans) when edges exist
    if result["graph"]["edges"]:
        seen = set()
        for edge in result["graph"]["edges"]:
            seen.add(edge["source"])
            seen.add(edge["target"])
        for node in result["graph"]["nodes"]:
            assert node["id"] in seen, f"orphan node {node['id']}"


def test_build_argv_injects_ox_stdout() -> None:
    mod = sfp_cli_nmap()
    argv = mod.build_argv(
        {
            "target": "scanme.nmap.org",
            "args": ["-sn", "-T4"],
            "executable_prefix": ["nmap"],
        }
    )
    assert argv[:1] == ["nmap"]
    assert "-oX" in argv
    assert argv[argv.index("-oX") + 1] == "-"
    assert argv[-1] == "scanme.nmap.org"


def test_run_argv_rejects_shell_string() -> None:
    with pytest.raises(TypeError):
        run_argv("nmap -sn scanme.nmap.org")  # type: ignore[arg-type]
