# -*- coding: utf-8 -*-
"""httpx structured JSON helpers and structured→text conversion (modules_v2 port)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

HTTPX_STRUCTURED_SCHEMA = "httpx_probe_v1"

CAPTURE_HEADER_RE = re.compile(
    r"^# SpiderFeet CLI examination capture\n(?:# .+\n)*\n",
    re.MULTILINE,
)


def parse_jsonl(raw: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def parse_httpx_structured(raw: str) -> dict[str, Any]:
    """Parse httpx bundle JSON or legacy JSONL into {schema, records, …}."""
    stripped = raw.strip()
    if not stripped:
        return {"schema": HTTPX_STRUCTURED_SCHEMA, "records": []}
    if stripped.startswith("{"):
        try:
            doc = json.loads(stripped)
        except json.JSONDecodeError:
            return {"schema": HTTPX_STRUCTURED_SCHEMA, "records": parse_jsonl(stripped)}
        if isinstance(doc, list):
            return {"schema": HTTPX_STRUCTURED_SCHEMA, "records": doc}
        records = doc.get("records") or []
        return {
            "schema": doc.get("schema", HTTPX_STRUCTURED_SCHEMA),
            "records": records,
            **{k: v for k, v in doc.items() if k not in {"schema", "records"}},
        }
    return {"schema": HTTPX_STRUCTURED_SCHEMA, "records": parse_jsonl(stripped)}


def records_only(raw: str) -> list[dict[str, Any]]:
    return parse_httpx_structured(raw)["records"]


def record_to_text_line(rec: dict[str, Any]) -> str:
    url = rec.get("url") or rec.get("input") or ""
    status = rec.get("status_code")
    title = rec.get("title") or ""
    webserver = rec.get("webserver") or ""
    tech = rec.get("tech") or []
    if isinstance(tech, list) and tech:
        tech_part = f" tech=[{', '.join(str(t) for t in tech)}]"
    else:
        tech_part = ""
    status_part = f" [{status}]" if status is not None else ""
    title_part = f" [{title}]" if title else ""
    server_part = f" server={webserver}" if webserver else ""
    if rec.get("failed"):
        return f"{url} [FAILED]{server_part}"
    return f"{url}{status_part}{title_part}{server_part}{tech_part}"


def structured_to_text(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    return "\n".join(record_to_text_line(rec) for rec in records) + "\n"


def build_httpx_bundle(
    records: list[dict[str, Any]],
    scan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if scan:
        return {
            "schema": HTTPX_STRUCTURED_SCHEMA,
            **scan,
            "probe_summary_lines": len(records),
            "records": records,
        }
    return {"schema": HTTPX_STRUCTURED_SCHEMA, "records": records}


def httpx_scan_context(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    target: str | None,
    subfinder_scenario: str | None,
    probe_profile: str,
    host_input_count: int,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
    stderr_banner: str | None = None,
) -> dict[str, Any]:
    ctx: dict[str, Any] = {
        "tool": "httpx",
        "scenario": scenario_name,
        "scenario_id": scenario_id,
        "target": target,
        "subfinder_scenario": subfinder_scenario,
        "probe_profile": probe_profile,
        "host_input_count": host_input_count,
        "command": command,
        "runtime": runtime,
        "started_at": captured_at.astimezone(timezone.utc).isoformat(),
        "duration_s": round(duration_s, 3),
        "exit_code": exit_code,
        "probe_summary_lines": record_count,
        "text_role": "one line per live URL: url [status] [title] server=… tech=[…]",
        "structured_role": "full httpx JSONL probe objects in records[]",
    }
    if stderr_banner and stderr_banner.strip():
        ctx["stderr_banner"] = stderr_banner.strip()
    return ctx


def dumps_httpx_bundle(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, indent=2) + "\n"


def strip_capture_header(text: str) -> str:
    return CAPTURE_HEADER_RE.sub("", text, count=1)


def httpx_text_capture_header(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    target: str | None,
    subfinder_scenario: str | None,
    probe_profile: str,
    host_input_count: int,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
) -> str:
    scan = httpx_scan_context(
        command=command,
        scenario_name=scenario_name,
        scenario_id=scenario_id,
        target=target,
        subfinder_scenario=subfinder_scenario,
        probe_profile=probe_profile,
        host_input_count=host_input_count,
        captured_at=captured_at,
        runtime=runtime,
        exit_code=exit_code,
        duration_s=duration_s,
        record_count=record_count,
    )
    target_line = scan["target"] or "—"
    subfinder_line = scan["subfinder_scenario"] or "—"
    return (
        "# SpiderFeet CLI examination capture\n"
        f"# tool: {scan['tool']}\n"
        f"# scenario: {scan['scenario']} ({scan['scenario_id']})\n"
        f"# target: {target_line}\n"
        f"# subfinder_scenario: {subfinder_line}\n"
        f"# probe_profile: {scan['probe_profile']}\n"
        f"# host_input_count: {scan['host_input_count']}\n"
        f"# command: {scan['command']}\n"
        f"# runtime: {scan['runtime']}\n"
        f"# started_at: {scan['started_at']}\n"
        f"# duration_s: {scan['duration_s']:.3f}\n"
        f"# exit_code: {scan['exit_code']}\n"
        f"# probe_summary_lines: {scan['probe_summary_lines']}\n"
        f"# text_role: {scan['text_role']}\n"
        f"# structured_role: {scan['structured_role']}\n"
        "\n"
    )
