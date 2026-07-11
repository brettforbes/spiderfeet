"""Tests for SPEC-004 harvest adapter dispatch (B5)."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
NMAP_XML = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap/17_output_structured.xml"
NETDISCOVER_TEXT = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/netdiscover/1_output_text.txt"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))


def _load_harvest():
    spec = importlib.util.spec_from_file_location("harvest", CLI_CORPUS / "harvest.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["harvest"] = module
    spec.loader.exec_module(module)
    return module


def _strip_capture_header(text: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    body: list[str] = []
    for line in lines:
        if line.startswith("#"):
            continue
        body.append(line)
    return "\n".join(body).lstrip("\n")


def test_harvest_adapter_tools_include_spec004_adapters():
    harvest = _load_harvest()
    assert harvest.ADAPTER_TOOLS == frozenset(
        {"netdiscover", "nmap", "nerva", "pius", "subfinder", "httpx", "katana", "nuclei"}
    )


def test_harvest_adapter_dispatch_writes_four_netdiscover_artifacts(tmp_path, monkeypatch):
    harvest = _load_harvest()
    monkeypatch.setattr(harvest, "NUGGET_ROOT", tmp_path / "nugget_structure")
    raw_text = _strip_capture_header(NETDISCOVER_TEXT.read_text(encoding="utf-8"))
    scenario = {
        "id": "local_subnet_active_parsable",
        "name": "A — active ARP scan 192.168.1.0/24 (parseable)",
        "output_mode": "parsable",
    }
    result = harvest.RunResult(
        command="netdiscover -r 192.168.1.0/24 -P",
        runtime="windows-lan",
        exit_code=0,
        duration_s=1.0,
        stdout=raw_text,
        stderr="",
    )
    captured_at = datetime(2026, 6, 29, 14, 34, 37, tzinfo=timezone.utc)

    structured_path, text_content, graph_path, markdown_path = harvest._write_adapter_four_outputs(
        "netdiscover",
        scenario,
        raw_input=raw_text,
        captured_at=captured_at,
        result=result,
        prefix="99",
        tool_dir=tmp_path,
    )

    assert structured_path.name == "99_output_structured.json"
    assert json.loads(structured_path.read_text(encoding="utf-8"))["netdiscover_scan"]["systems"]
    assert text_content.startswith("# SpiderFeet CLI examination capture")
    assert graph_path.is_file()
    assert markdown_path.is_file()
    assert json.loads(graph_path.read_text(encoding="utf-8"))["nodes"]
    assert "## Appendix" in markdown_path.read_text(encoding="utf-8")


def test_harvest_adapter_dispatch_writes_four_nmap_artifacts(tmp_path, monkeypatch):
    harvest = _load_harvest()
    monkeypatch.setattr(harvest, "NUGGET_ROOT", tmp_path / "nugget_structure")
    xml_text = NMAP_XML.read_text(encoding="utf-8")
    scenario = {"id": "nse_default_permissive", "name": "NSE default permissive"}
    result = harvest.RunResult(
        command="nmap -sT -A -T3 -p 22,80,443 -oX - scanme.nmap.org",
        runtime="windows",
        exit_code=0,
        duration_s=12.0,
        stdout=xml_text,
        stderr="",
    )
    captured_at = datetime(2026, 6, 23, 12, 0, 0, tzinfo=timezone.utc)

    structured_path, text_content, graph_path, markdown_path = harvest._write_adapter_four_outputs(
        "nmap",
        scenario,
        raw_input=xml_text,
        captured_at=captured_at,
        result=result,
        prefix="17",
        tool_dir=tmp_path,
    )

    structured = json.loads(structured_path.read_text(encoding="utf-8"))
    assert structured["schema"] == "nmap_scan_v1"
    assert text_content.startswith("Nmap scan report")
    assert graph_path.is_file()
    assert markdown_path.is_file()
    assert any(node["nugget_id"] == "HOST" for node in json.loads(graph_path.read_text())["nodes"])


def test_write_tool_graph_skips_adapter_tools():
    harvest = _load_harvest()
    harvest._write_tool_graph(
        "netdiscover",
        {"id": "local_subnet_active_parsable"},
        Path("missing.json"),
        "netdiscover",
    )
    harvest._write_tool_graph(
        "nmap",
        {"id": "host_discovery_permissive_xml"},
        Path("missing.json"),
        "nmap",
    )
    harvest._write_tool_graph(
        "nerva",
        {"id": "tcp_http_rich_json"},
        Path("missing.json"),
        "nerva",
    )
    harvest._write_tool_graph(
        "pius",
        {"id": "crt_linode_ndjson", "org": "Linode"},
        Path("missing.json"),
        "pius",
    )
    harvest._write_tool_graph(
        "nuclei",
        {"id": "pg_dvwa_tech_fingerprint"},
        Path("missing.json"),
        "nuclei",
    )


def test_harvest_adapter_dispatch_writes_four_pius_artifacts(tmp_path, monkeypatch):
    harvest = _load_harvest()
    monkeypatch.setattr(harvest, "NUGGET_ROOT", tmp_path / "nugget_structure")
    raw = (CLI_CORPUS / "fixtures" / "pius_linode_crt_sample.jsonl").read_text(encoding="utf-8")
    scenario = {
        "id": "crt_linode_ndjson",
        "name": "CRT Linode sample",
        "org": "Linode",
        "target": "linode.com",
    }
    result = harvest.RunResult(
        command="pius run --org Linode --domain linode.com --output ndjson",
        runtime="windows",
        exit_code=0,
        duration_s=1.0,
        stdout=raw,
        stderr="",
    )
    captured_at = datetime(2026, 6, 15, 10, 0, 0, tzinfo=timezone.utc)

    structured_path, text_content, graph_path, markdown_path = harvest._write_adapter_four_outputs(
        "pius",
        scenario,
        raw_input=raw,
        captured_at=captured_at,
        result=result,
        prefix="12",
        tool_dir=tmp_path,
    )

    assert structured_path.name == "12_output_structured.json"
    assert text_content.startswith("# SpiderFeet CLI examination capture")
    assert graph_path.is_file()
    assert markdown_path.is_file()
    assert "## Organization" in markdown_path.read_text(encoding="utf-8")
    assert "## Appendix" in markdown_path.read_text(encoding="utf-8")


def test_harvest_adapter_dispatch_writes_four_nerva_artifacts(tmp_path, monkeypatch):
    harvest = _load_harvest()
    monkeypatch.setattr(harvest, "NUGGET_ROOT", tmp_path / "nugget_structure")
    fixture = CLI_CORPUS / "fixtures" / "nerva_correlation_seed07.json"
    raw = fixture.read_text(encoding="utf-8")
    # Convert bundle records into JSONL stdout shape harvest expects.
    records = json.loads(raw)["records"]
    stdout = "\n".join(json.dumps(record) for record in records) + "\n"
    scenario = {
        "id": "tcp_list_file_json",
        "name": "Multi-target list file",
        "target": "scanme.nmap.org + praetorian.com",
    }
    result = harvest.RunResult(
        command="nerva -l targets --json -w 8000",
        runtime="windows",
        exit_code=0,
        duration_s=2.0,
        stdout=stdout,
        stderr="",
    )
    captured_at = datetime(2026, 6, 30, 7, 40, 7, tzinfo=timezone.utc)

    structured_path, text_content, graph_path, markdown_path = harvest._write_adapter_four_outputs(
        "nerva",
        scenario,
        raw_input=stdout,
        captured_at=captured_at,
        result=result,
        prefix="42",
        tool_dir=tmp_path,
    )

    structured = json.loads(structured_path.read_text(encoding="utf-8"))
    assert structured["schema"] == "nerva_fingerprint_v1"
    assert text_content.startswith("# SpiderFeet CLI examination capture")
    assert graph_path.is_file()
    assert markdown_path.is_file()
    assert "indeterminate" in markdown_path.read_text(encoding="utf-8").lower()
    assert any(node["nugget_id"] == "CDN" for node in json.loads(graph_path.read_text())["nodes"])

