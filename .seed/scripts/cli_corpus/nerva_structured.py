#!/usr/bin/env python3
"""Nerva structured JSON helpers and structured→text conversion."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

NERVA_STRUCTURED_SCHEMA = "nerva_fingerprint_v1"

LINE_RE = re.compile(
    r"^(?P<proto>[a-z][a-z0-9+.-]*)://(?P<host>[^:]+):(?P<port>\d+) \((?P<ip>[^)]+)\)(?: \(tls\))?$"
)


def parse_jsonl(raw: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def parse_nerva_structured(raw: str) -> dict[str, Any]:
    """Parse nerva bundle JSON or legacy JSONL into {schema, records}."""
    stripped = raw.strip()
    if not stripped:
        return {"schema": NERVA_STRUCTURED_SCHEMA, "records": []}
    if stripped.startswith("{"):
        doc = json.loads(stripped)
        if isinstance(doc, list):
            return {"schema": NERVA_STRUCTURED_SCHEMA, "records": doc}
        records = doc.get("records") or []
        return {
            "schema": doc.get("schema", NERVA_STRUCTURED_SCHEMA),
            "records": records,
        }
    records = parse_jsonl(stripped)
    return {"schema": NERVA_STRUCTURED_SCHEMA, "records": records}


def records_only(raw: str) -> list[dict[str, Any]]:
    return parse_nerva_structured(raw)["records"]


def record_to_text_line(rec: dict[str, Any]) -> str:
    proto = rec["protocol"]
    host = rec["host"]
    port = rec["port"]
    ip = rec["ip"]
    line = f"{proto}://{host}:{port} ({ip})"
    if rec.get("tls"):
        line += " (tls)"
    return line


def parse_text_line(line: str) -> dict[str, Any]:
    m = LINE_RE.match(line.strip())
    if not m:
        raise ValueError(f"Unrecognized nerva text line: {line!r}")
    return {
        "protocol": m.group("proto"),
        "host": m.group("host"),
        "port": int(m.group("port")),
        "ip": m.group("ip"),
        "tls": line.strip().endswith("(tls)"),
    }


def record_matches_line(rec: dict[str, Any], parsed: dict[str, Any]) -> bool:
    return (
        rec.get("protocol") == parsed["protocol"]
        and rec.get("host") == parsed["host"]
        and int(rec.get("port", 0)) == parsed["port"]
        and rec.get("ip") == parsed["ip"]
        and bool(rec.get("tls")) == parsed["tls"]
    )


def compute_text_line_order(records: list[dict[str, Any]]) -> list[int]:
    """Text order for a single --json run: JSON emission / records array order."""
    return list(range(len(records)))


def derive_text_line_order(records: list[dict[str, Any]], reference_text: str) -> list[int]:
    """Map saved native text lines onto record indices (validation / fixture analysis)."""
    lines = [ln for ln in reference_text.replace("\r\n", "\n").split("\n") if ln.strip()]
    if not lines and not records:
        return []
    if len(lines) != len(records):
        raise ValueError(f"Line count {len(lines)} != record count {len(records)}")
    used: set[int] = set()
    order: list[int] = []
    for line in lines:
        parsed = parse_text_line(line)
        match_idx = None
        for idx, rec in enumerate(records):
            if idx in used:
                continue
            if record_matches_line(rec, parsed):
                match_idx = idx
                break
        if match_idx is None:
            raise ValueError(f"No structured record matches nerva text line: {line!r}")
        used.add(match_idx)
        order.append(match_idx)
    return order


def structured_to_text(
    records: list[dict[str, Any]],
    text_line_order: list[int] | None = None,
) -> str:
    if not records:
        return ""
    order = text_line_order if text_line_order is not None else compute_text_line_order(records)
    if len(order) != len(records):
        raise ValueError("text_line_order length must match records length")
    lines = [record_to_text_line(records[i]) for i in order]
    return "\n".join(lines) + "\n"


def build_nerva_bundle(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": NERVA_STRUCTURED_SCHEMA,
        "records": records,
    }


def jsonl_to_bundle(jsonl: str) -> dict[str, Any]:
    return build_nerva_bundle(parse_jsonl(jsonl))


def dumps_nerva_bundle(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, indent=2) + "\n"


def reference_lines_match_records(records: list[dict[str, Any]], reference_text: str) -> bool:
    """True when reference text lines are a permutation of record_to_text_line outputs."""
    lines = [ln for ln in reference_text.replace("\r\n", "\n").split("\n") if ln.strip()]
    if len(lines) != len(records):
        return False
    expected = sorted(record_to_text_line(r) for r in records)
    return sorted(lines) == expected


CAPTURE_HEADER_RE = re.compile(
    r"^# SpiderFeet CLI examination capture\n(?:# .+\n)*\n",
    re.MULTILINE,
)


def strip_capture_header(text: str) -> str:
    return CAPTURE_HEADER_RE.sub("", text, count=1)


def nerva_text_capture_header(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    target: str | None,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
) -> str:
    started = captured_at.astimezone(timezone.utc).isoformat()
    target_line = target or "—"
    return (
        "# SpiderFeet CLI examination capture\n"
        "# tool: nerva\n"
        f"# scenario: {scenario_name} ({scenario_id})\n"
        f"# target: {target_line}\n"
        f"# command: {command}\n"
        f"# runtime: {runtime}\n"
        f"# started_at: {started}\n"
        f"# duration_s: {duration_s:.3f}\n"
        f"# exit_code: {exit_code}\n"
        f"# fingerprint_summary_lines: {record_count}\n"
        "# text_role: one line per discovered service/IP (pipe-friendly summary)\n"
        "# structured_role: full JSON metadata per record (headers, findings, etc.)\n"
        "\n"
    )
