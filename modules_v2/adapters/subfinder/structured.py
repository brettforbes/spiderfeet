# -*- coding: utf-8 -*-
"""Subfinder structured JSON helpers and structured→text conversion (modules_v2 port)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

SUBFINDER_STRUCTURED_SCHEMA = "subfinder_host_v1"

CAPTURE_HEADER_RE = re.compile(
    r"^# SpiderFeet CLI examination capture\n(?:# .+\n)*\n",
    re.MULTILINE,
)


def parse_jsonl(raw: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{"):
            records.append(json.loads(line))
    return records


def normalize_record(rec: dict[str, Any], *, mode: str = "passive") -> dict[str, Any]:
    """Normalize passive sources[] vs active source + ip shapes."""
    host = str(rec.get("host", "")).strip().lower().rstrip(".")
    out: dict[str, Any] = {
        "host": host,
        "input": str(rec.get("input", "")).strip().lower().rstrip(".") or None,
        "mode": mode,
    }
    if rec.get("ip"):
        out["ip"] = str(rec["ip"]).strip()
    sources = rec.get("sources")
    if isinstance(sources, list) and sources:
        out["sources"] = sorted({str(s).strip() for s in sources if str(s).strip()})
    elif rec.get("source"):
        out["sources"] = [str(rec["source"]).strip()]
    return out


def parse_subfinder_structured(raw: str) -> dict[str, Any]:
    """Parse subfinder bundle JSON or legacy JSONL into {schema, records}."""
    stripped = raw.strip()
    if not stripped:
        return {"schema": SUBFINDER_STRUCTURED_SCHEMA, "records": []}
    if stripped.startswith("{"):
        try:
            doc = json.loads(stripped)
        except json.JSONDecodeError:
            return {"schema": SUBFINDER_STRUCTURED_SCHEMA, "records": parse_jsonl(stripped)}
        if isinstance(doc, list):
            return {"schema": SUBFINDER_STRUCTURED_SCHEMA, "records": doc}
        records = doc.get("records") or []
        return {
            "schema": doc.get("schema", SUBFINDER_STRUCTURED_SCHEMA),
            "records": records,
            **{k: v for k, v in doc.items() if k not in {"schema", "records"}},
        }
    return {"schema": SUBFINDER_STRUCTURED_SCHEMA, "records": parse_jsonl(stripped)}


def records_only(raw: str) -> list[dict[str, Any]]:
    return parse_subfinder_structured(raw)["records"]


def record_to_text_line(rec: dict[str, Any]) -> str:
    host = rec.get("host", "")
    ip = rec.get("ip")
    sources = rec.get("sources") or []
    if ip:
        src = sources[0] if len(sources) == 1 else ",".join(sources)
        suffix = f" (source: {src})" if src else ""
        return f"{host} -> {ip}{suffix}"
    if sources:
        return f"{host} (sources: {', '.join(sources)})"
    return str(host)


def structured_to_text(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    lines = [record_to_text_line(rec) for rec in records]
    return "\n".join(lines) + "\n"


def build_subfinder_bundle(
    records: list[dict[str, Any]],
    scan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if scan:
        return {
            "schema": SUBFINDER_STRUCTURED_SCHEMA,
            **scan,
            "host_summary_lines": len(records),
            "records": records,
        }
    return {
        "schema": SUBFINDER_STRUCTURED_SCHEMA,
        "records": records,
    }


def subfinder_scan_context(
    *,
    command: str,
    scenario_name: str,
    scenario_id: str,
    target: str | None,
    enumeration_mode: str,
    captured_at: datetime,
    runtime: str,
    exit_code: int,
    duration_s: float,
    record_count: int,
    stderr_banner: str | None = None,
) -> dict[str, Any]:
    ctx: dict[str, Any] = {
        "tool": "subfinder",
        "scenario": scenario_name,
        "scenario_id": scenario_id,
        "target": target,
        "enumeration_mode": enumeration_mode,
        "command": command,
        "runtime": runtime,
        "started_at": captured_at.astimezone(timezone.utc).isoformat(),
        "duration_s": round(duration_s, 3),
        "exit_code": exit_code,
        "host_summary_lines": record_count,
        "text_role": "one line per host: fqdn (sources: …) or fqdn -> ip",
        "structured_role": "normalized host records in records[]",
    }
    if stderr_banner and stderr_banner.strip():
        ctx["stderr_banner"] = stderr_banner.strip()
    return ctx


def dumps_subfinder_bundle(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, indent=2) + "\n"


def strip_capture_header(text: str) -> str:
    return CAPTURE_HEADER_RE.sub("", text, count=1)


__all__ = [
    "SUBFINDER_STRUCTURED_SCHEMA",
    "build_subfinder_bundle",
    "dumps_subfinder_bundle",
    "normalize_record",
    "parse_jsonl",
    "parse_subfinder_structured",
    "records_only",
    "record_to_text_line",
    "strip_capture_header",
    "structured_to_text",
    "subfinder_scan_context",
]
