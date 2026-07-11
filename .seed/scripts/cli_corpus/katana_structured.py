#!/usr/bin/env python3
"""Katana structured JSON helpers and structured→text conversion."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

KATANA_STRUCTURED_SCHEMA = "katana_crawl_v1"

CAPTURE_HEADER_RE = re.compile(
    r"^# SpiderFeet CLI examination capture\n(?:# .+\n)*\n",
    re.MULTILINE,
)


def parse_jsonl(raw: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def parse_katana_structured(raw: str) -> dict[str, Any]:
    stripped = raw.strip()
    if not stripped:
        return {"schema": KATANA_STRUCTURED_SCHEMA, "records": []}
    if stripped.startswith("{"):
        try:
            doc = json.loads(stripped)
        except json.JSONDecodeError:
            return {"schema": KATANA_STRUCTURED_SCHEMA, "records": parse_jsonl(stripped)}
        if isinstance(doc, list):
            return {"schema": KATANA_STRUCTURED_SCHEMA, "records": doc}
        records = doc.get("records") or []
        return {"schema": doc.get("schema", KATANA_STRUCTURED_SCHEMA), "records": records}
    return {"schema": KATANA_STRUCTURED_SCHEMA, "records": parse_jsonl(stripped)}


def records_only(raw: str) -> list[dict[str, Any]]:
    return parse_katana_structured(raw)["records"]


def _host_from_record(rec: dict[str, Any]) -> str:
    url = str(rec.get("url") or rec.get("request", {}).get("endpoint") or "").strip()
    if url:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        host = parsed.hostname or ""
        if host:
            return host.lower().rstrip(".")
    endpoint = rec.get("request", {}).get("endpoint")
    if endpoint:
        parsed = urlparse(str(endpoint))
        if parsed.hostname:
            return parsed.hostname.lower().rstrip(".")
    return ""


def record_to_text_line(rec: dict[str, Any]) -> str:
    url = str(rec.get("url") or rec.get("request", {}).get("endpoint") or "").strip()
    if not url:
        return ""
    host = _host_from_record(rec)
    method = rec.get("request", {}).get("method") or rec.get("method") or "GET"
    status = rec.get("response", {}).get("status_code") or rec.get("status_code")
    parts = [url]
    if host:
        parts.append(f"host={host}")
    parts.append(f"method={method}")
    if status is not None:
        parts.append(f"status={status}")
    return " ".join(parts)


def structured_to_text(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    lines = [line for rec in records if (line := record_to_text_line(rec))]
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def build_katana_bundle(records: list[dict[str, Any]], scan: dict[str, Any] | None = None) -> dict[str, Any]:
    if scan:
        return {
            "schema": KATANA_STRUCTURED_SCHEMA,
            **scan,
            "endpoint_summary_lines": len(records),
            "records": records,
        }
    return {"schema": KATANA_STRUCTURED_SCHEMA, "records": records}


def katana_scan_context(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    target: str | None,
    httpx_scenario: str | None,
    crawl_profile: str,
    url_input_count: int,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
    stderr_banner: str | None = None,
) -> dict[str, Any]:
    ctx: dict[str, Any] = {
        "tool": "katana",
        "scenario": scenario_name,
        "scenario_id": scenario_id,
        "target": target,
        "httpx_scenario": httpx_scenario,
        "crawl_profile": crawl_profile,
        "url_input_count": url_input_count,
        "command": command,
        "runtime": runtime,
        "started_at": captured_at.astimezone(timezone.utc).isoformat(),
        "duration_s": round(duration_s, 3),
        "exit_code": exit_code,
        "endpoint_summary_lines": record_count,
        "text_role": "one line per endpoint: url host=… method=… status=…",
        "structured_role": "full katana JSONL crawl objects in records[]",
    }
    if stderr_banner and stderr_banner.strip():
        ctx["stderr_banner"] = stderr_banner.strip()
    return ctx


def dumps_katana_bundle(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, indent=2) + "\n"


def strip_capture_header(text: str) -> str:
    return CAPTURE_HEADER_RE.sub("", text, count=1)


def katana_text_capture_header(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    target: str | None,
    httpx_scenario: str | None,
    crawl_profile: str,
    url_input_count: int,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
) -> str:
    scan = katana_scan_context(
        command=command,
        scenario_name=scenario_name,
        scenario_id=scenario_id,
        target=target,
        httpx_scenario=httpx_scenario,
        crawl_profile=crawl_profile,
        url_input_count=url_input_count,
        captured_at=captured_at,
        runtime=runtime,
        exit_code=exit_code,
        duration_s=duration_s,
        record_count=record_count,
    )
    target_line = scan["target"] or "—"
    httpx_line = scan["httpx_scenario"] or "—"
    return (
        "# SpiderFeet CLI examination capture\n"
        f"# tool: {scan['tool']}\n"
        f"# scenario: {scan['scenario']} ({scan['scenario_id']})\n"
        f"# target: {target_line}\n"
        f"# httpx_scenario: {httpx_line}\n"
        f"# crawl_profile: {scan['crawl_profile']}\n"
        f"# url_input_count: {scan['url_input_count']}\n"
        f"# command: {scan['command']}\n"
        f"# runtime: {scan['runtime']}\n"
        f"# started_at: {scan['started_at']}\n"
        f"# duration_s: {scan['duration_s']:.3f}\n"
        f"# exit_code: {scan['exit_code']}\n"
        f"# endpoint_summary_lines: {scan['endpoint_summary_lines']}\n"
        f"# text_role: {scan['text_role']}\n"
        f"# structured_role: {scan['structured_role']}\n"
        "\n"
    )
