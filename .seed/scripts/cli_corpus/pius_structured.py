#!/usr/bin/env python3
"""Pius structured JSON helpers and structured→text conversion."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

PIUS_STRUCTURED_SCHEMA = "pius_finding_v1"

LINE_RE = re.compile(
    r"^\[(?P<type>[a-z][a-z0-9_-]*)\]\s+(?P<value>.+?)\s+\((?P<source>[^)]+)\)"
    r"(?:\s+⚠\s+needs-review(?:\s+\[confidence:(?P<confidence>[0-9.]+)\])?)?\s*$",
    re.IGNORECASE,
)

CAPTURE_HEADER_RE = re.compile(
    r"^# SpiderFeet CLI examination capture\n(?:# .+\n)*\n",
    re.MULTILINE,
)


def parse_ndjson(raw: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{"):
            records.append(json.loads(line))
    return records


def parse_pius_structured(raw: str) -> dict[str, Any]:
    """Parse pius bundle JSON or legacy NDJSON into {schema, records}."""
    stripped = raw.strip()
    if not stripped:
        return {"schema": PIUS_STRUCTURED_SCHEMA, "records": []}
    if stripped.startswith("{"):
        try:
            doc = json.loads(stripped)
        except json.JSONDecodeError:
            return {"schema": PIUS_STRUCTURED_SCHEMA, "records": parse_ndjson(stripped)}
        if isinstance(doc, list):
            return {"schema": PIUS_STRUCTURED_SCHEMA, "records": doc}
        records = doc.get("records") or []
        return {
            "schema": doc.get("schema", PIUS_STRUCTURED_SCHEMA),
            "records": records,
        }
    return {"schema": PIUS_STRUCTURED_SCHEMA, "records": parse_ndjson(stripped)}


def records_only(raw: str) -> list[dict[str, Any]]:
    return parse_pius_structured(raw)["records"]


def record_to_text_line(rec: dict[str, Any]) -> str:
    ftype = str(rec.get("Type", "")).lower()
    value = str(rec.get("Value", "")).strip()
    source = str(rec.get("Source", "")).strip()
    line = f"[{ftype}] {value} ({source})"
    data = rec.get("Data") or {}
    if isinstance(data, dict):
        if data.get("needs_review"):
            line += " ⚠ needs-review"
            confidence = data.get("confidence")
            if confidence is not None:
                line += f" [confidence:{confidence}]"
    return line


def structured_to_text(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    lines = [record_to_text_line(rec) for rec in records]
    return "\n".join(lines) + "\n"


def build_pius_bundle(
    records: list[dict[str, Any]],
    scan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if scan:
        return {
            "schema": PIUS_STRUCTURED_SCHEMA,
            **scan,
            "finding_summary_lines": len(records),
            "records": records,
        }
    return {
        "schema": PIUS_STRUCTURED_SCHEMA,
        "records": records,
    }


def pius_scan_context(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    org: str | None,
    target: str | None,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
    stderr_banner: str | None = None,
) -> dict[str, Any]:
    ctx: dict[str, Any] = {
        "tool": "pius",
        "scenario": scenario_name,
        "scenario_id": scenario_id,
        "org": org,
        "target": target,
        "command": command,
        "runtime": runtime,
        "started_at": captured_at.astimezone(timezone.utc).isoformat(),
        "duration_s": round(duration_s, 3),
        "exit_code": exit_code,
        "finding_summary_lines": record_count,
        "text_role": "one line per finding: [type] value (source)",
        "structured_role": "full NDJSON finding objects in records[]",
    }
    if stderr_banner and stderr_banner.strip():
        ctx["stderr_banner"] = stderr_banner.strip()
    return ctx


def dumps_pius_bundle(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, indent=2) + "\n"


def strip_capture_header(text: str) -> str:
    return CAPTURE_HEADER_RE.sub("", text, count=1)


def pius_text_capture_header(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    org: str | None,
    target: str | None,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
) -> str:
    scan = pius_scan_context(
        command=command,
        scenario_name=scenario_name,
        scenario_id=scenario_id,
        org=org,
        target=target,
        captured_at=captured_at,
        runtime=runtime,
        exit_code=exit_code,
        duration_s=duration_s,
        record_count=record_count,
    )
    org_line = scan["org"] or "—"
    target_line = scan["target"] or "—"
    return (
        "# SpiderFeet CLI examination capture\n"
        f"# tool: {scan['tool']}\n"
        f"# scenario: {scan['scenario']} ({scan['scenario_id']})\n"
        f"# org: {org_line}\n"
        f"# target: {target_line}\n"
        f"# command: {scan['command']}\n"
        f"# runtime: {scan['runtime']}\n"
        f"# started_at: {scan['started_at']}\n"
        f"# duration_s: {scan['duration_s']:.3f}\n"
        f"# exit_code: {scan['exit_code']}\n"
        f"# finding_summary_lines: {scan['finding_summary_lines']}\n"
        f"# text_role: {scan['text_role']}\n"
        f"# structured_role: {scan['structured_role']}\n"
        "\n"
    )


def ndjson_to_bundle(ndjson: str, scan: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_pius_bundle(parse_ndjson(ndjson), scan)
