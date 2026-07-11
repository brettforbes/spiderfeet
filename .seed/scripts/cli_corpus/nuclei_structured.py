#!/usr/bin/env python3
"""Nuclei structured JSON helpers and structured→text conversion."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

NUCLEI_STRUCTURED_SCHEMA = "nuclei_finding_v1"

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}")

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


def parse_nuclei_structured(raw: str) -> dict[str, Any]:
    """Parse nuclei bundle JSON or legacy NDJSON into {schema, records}."""
    stripped = raw.strip()
    if not stripped:
        return {"schema": NUCLEI_STRUCTURED_SCHEMA, "records": []}
    if stripped.startswith("{"):
        try:
            doc = json.loads(stripped)
        except json.JSONDecodeError:
            return {"schema": NUCLEI_STRUCTURED_SCHEMA, "records": parse_ndjson(stripped)}
        if isinstance(doc, list):
            return {"schema": NUCLEI_STRUCTURED_SCHEMA, "records": doc}
        records = doc.get("records") or []
        return {
            "schema": doc.get("schema", NUCLEI_STRUCTURED_SCHEMA),
            "records": records,
        }
    return {"schema": NUCLEI_STRUCTURED_SCHEMA, "records": parse_ndjson(stripped)}


def records_only(raw: str) -> list[dict[str, Any]]:
    return parse_nuclei_structured(raw)["records"]


def record_to_text_line(rec: dict[str, Any]) -> str:
    info = rec.get("info") or {}
    severity = str(info.get("severity", "unknown"))
    template_id = str(rec.get("template-id", "unknown"))
    matched = str(rec.get("matched-at", ""))
    line = f"[{severity}] {template_id} @ {matched}"
    matcher = rec.get("matcher-name")
    if matcher:
        line += f" (matcher: {matcher})"
    extracted = rec.get("extracted-results")
    if extracted and isinstance(extracted, list):
        line += f" (extracted: {', '.join(str(x) for x in extracted)})"
    cves = CVE_RE.findall(json.dumps(rec))
    if cves:
        line += f" [CVE: {', '.join(sorted(set(cves)))}]"
    return line


def structured_to_text(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    lines = [record_to_text_line(rec) for rec in records]
    return "\n".join(lines) + "\n"


def build_nuclei_bundle(
    records: list[dict[str, Any]],
    scan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if scan:
        return {
            "schema": NUCLEI_STRUCTURED_SCHEMA,
            **scan,
            "finding_summary_lines": len(records),
            "records": records,
        }
    return {
        "schema": NUCLEI_STRUCTURED_SCHEMA,
        "records": records,
    }


def nuclei_scan_context(
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
    stderr_banner: str | None = None,
) -> dict[str, Any]:
    ctx: dict[str, Any] = {
        "tool": "nuclei",
        "scenario": scenario_name,
        "scenario_id": scenario_id,
        "target": target,
        "command": command,
        "runtime": runtime,
        "started_at": captured_at.astimezone(timezone.utc).isoformat(),
        "duration_s": round(duration_s, 3),
        "exit_code": exit_code,
        "finding_summary_lines": record_count,
        "text_role": "one line per JSONL finding: [severity] template-id @ matched-at",
        "structured_role": "full JSONL finding objects in records[]",
    }
    if stderr_banner and stderr_banner.strip():
        ctx["stderr_banner"] = stderr_banner.strip()
    return ctx


def dumps_nuclei_bundle(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, indent=2) + "\n"


def strip_capture_header(text: str) -> str:
    return CAPTURE_HEADER_RE.sub("", text, count=1)


def nuclei_text_capture_header(
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
    scan = nuclei_scan_context(
        command=command,
        scenario_name=scenario_name,
        scenario_id=scenario_id,
        target=target,
        captured_at=captured_at,
        runtime=runtime,
        exit_code=exit_code,
        duration_s=duration_s,
        record_count=record_count,
    )
    target_line = scan["target"] or "—"
    return (
        "# SpiderFeet CLI examination capture\n"
        f"# tool: {scan['tool']}\n"
        f"# scenario: {scan['scenario']} ({scan['scenario_id']})\n"
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
    return build_nuclei_bundle(parse_ndjson(ndjson), scan)
