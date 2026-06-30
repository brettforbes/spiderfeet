#!/usr/bin/env python3
"""Validate nerva structured→text conversion."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parents[1] / ".seed" / "scripts" / "cli_corpus"
REPO_ROOT = CORPUS_DIR.parents[2]
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

from nerva_structured import (
    LINE_RE,
    parse_nerva_structured,
    record_to_text_line,
    reference_lines_match_records,
    strip_capture_header,
    structured_to_text,
)

REFERENCE = CORPUS_DIR / "fixtures" / "nerva_text_reference"
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs" / "nerva"


def test_record_to_text_line_format() -> None:
    rec = {
        "host": "example.com",
        "ip": "93.184.216.34",
        "port": 443,
        "protocol": "https",
        "tls": True,
    }
    line = record_to_text_line(rec)
    assert LINE_RE.match(line)
    assert line.endswith("(tls)")


def test_reference_fixtures_match_record_multiset() -> None:
    """One-time native text captures: same fingerprints as structured, order may differ."""
    for ref in sorted(REFERENCE.glob("*.txt")):
        sid = ref.stem
        exam = None
        for manifest_path in EXAM_ROOT.glob("*_manifest.json"):
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("scenario_id") == sid:
                structured_rel = manifest.get("structured_path")
                if structured_rel:
                    exam = REPO_ROOT / structured_rel
                break
        if exam is None or not exam.is_file():
            continue
        records = parse_nerva_structured(exam.read_text(encoding="utf-8"))["records"]
        assert reference_lines_match_records(records, ref.read_text(encoding="utf-8")), sid


def test_harvested_text_derived_from_structured_only() -> None:
    for manifest_path in sorted(EXAM_ROOT.glob("*_manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        structured_rel = manifest.get("structured_path")
        text_rel = manifest.get("text_path")
        if not structured_rel or not text_rel:
            continue
        records = parse_nerva_structured((REPO_ROOT / structured_rel).read_text(encoding="utf-8"))["records"]
        derived = structured_to_text(records)
        saved = strip_capture_header(
            (REPO_ROOT / text_rel).read_text(encoding="utf-8")
        ).replace("\r\n", "\n")
        if saved and not saved.endswith("\n"):
            saved += "\n"
        assert derived == saved, manifest.get("scenario_id")


def test_nerva_text_capture_header_includes_scan_context() -> None:
    from datetime import datetime, timezone

    from nerva_structured import nerva_text_capture_header

    header = nerva_text_capture_header(
        command="nerva -t scanme.nmap.org:80 --json -w 5000",
        scenario_name="TCP HTTP rich metadata (scanme:80)",
        scenario_id="tcp_http_rich_json",
        target="scanme.nmap.org:80",
        captured_at=datetime(2026, 6, 30, 12, 0, 0, tzinfo=timezone.utc),
        runtime="windows",
        exit_code=0,
        duration_s=15.734,
        record_count=2,
    )
    assert "# SpiderFeet CLI examination capture" in header
    assert "nerva -t scanme.nmap.org:80 --json -w 5000" in header
    assert "fingerprint_summary_lines: 2" in header
    assert "text_role:" in header
    assert "structured_role:" in header


def test_harvested_structured_includes_scan_context() -> None:
    for manifest_path in sorted(EXAM_ROOT.glob("*_manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        structured_rel = manifest.get("structured_path")
        if not structured_rel:
            continue
        doc = json.loads((REPO_ROOT / structured_rel).read_text(encoding="utf-8"))
        assert doc.get("tool") == "nerva", manifest.get("scenario_id")
        assert doc.get("schema") == "nerva_fingerprint_v1"
        assert "command" in doc
        assert "started_at" in doc
        assert "duration_s" in doc
        assert "exit_code" in doc
        assert "records" in doc
        assert doc["fingerprint_summary_lines"] == len(doc["records"])


if __name__ == "__main__":
    test_record_to_text_line_format()
    test_nerva_text_capture_header_includes_scan_context()
    test_reference_fixtures_match_record_multiset()
    test_harvested_text_derived_from_structured_only()
    test_harvested_structured_includes_scan_context()
    print("ok")
