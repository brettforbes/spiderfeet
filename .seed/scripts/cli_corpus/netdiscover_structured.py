#!/usr/bin/env python3
"""Build netdiscover_scan JSON from -P parseable or interactive TUI output."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = Path(__file__).resolve().parent / "templates" / "netdiscover_parsable.textfsm"

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[0-9;]*[a-zA-Z]")
HOST_ROW_RE = re.compile(
    r"^(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:]{17})\s+(\d+)\s+(\d+)\s+(.+)$",
    re.MULTILINE,
)
TRUNCATION_PATTERNS = (r"| head", r"| tail", r"head -", r"tail -")

REQUIRED_SCAN_FIELDS = ("scanner", "args", "command", "start_time")


def assert_no_truncation(command: str, scenario_id: str) -> None:
    lowered = command.lower()
    for pattern in TRUNCATION_PATTERNS:
        if pattern in lowered:
            raise SystemExit(
                f"Truncation forbidden in scenario '{scenario_id}': "
                f"command contains '{pattern.strip()}' — {command}"
            )


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def parse_host_rows(raw: str) -> list[dict[str, str]]:
    try:
        import textfsm
    except ImportError:
        rows: list[dict[str, str]] = []
        for line in strip_ansi(raw).splitlines():
            m = HOST_ROW_RE.match(line.strip())
            if m:
                rows.append(
                    {
                        "IP": m.group(1),
                        "MAC": m.group(2),
                        "COUNT": m.group(3),
                        "LEN": m.group(4),
                        "VENDOR": m.group(5).strip(),
                    }
                )
        return rows
    with TEMPLATE.open(encoding="utf-8") as fh:
        fsm = textfsm.TextFSM(fh)
    return fsm.ParseTextToDicts(strip_ansi(raw))


def rows_to_systems(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    systems: list[dict[str, Any]] = []
    for row in rows:
        systems.append(
            {
                "ipv4": row["IP"],
                "mac": row["MAC"].lower(),
                "mac_vendor": row.get("VENDOR", "").strip(),
                "count": int(row.get("COUNT", 0) or 0),
                "len": int(row.get("LEN", 0) or 0),
            }
        )
    return systems


def split_tui_frames(raw: str) -> list[str]:
    cleaned = strip_ansi(raw)
    if "Currently scanning:" not in cleaned:
        return [cleaned] if cleaned.strip() else []
    parts = re.split(r"(?=Currently scanning:)", cleaned)
    return [part for part in parts if part.strip()]


def frame_host_count(frame: str) -> int:
    match = re.search(r"from (\d+) hosts", frame)
    return int(match.group(1)) if match else 0


def parse_interactive(raw: str) -> tuple[list[dict[str, Any]], int, int, int]:
    frames = split_tui_frames(raw)
    scan_tries = len(frames)
    empty_scans = 0
    systems: list[dict[str, Any]] = []
    discovered = 0
    for frame in frames:
        host_count = frame_host_count(frame)
        rows = parse_host_rows(frame)
        if host_count == 0 and not rows:
            empty_scans += 1
        elif rows and not systems:
            systems = rows_to_systems(rows)
            discovered = len(systems)
    return systems, scan_tries, empty_scans, discovered


def parse_parsable(raw: str) -> tuple[list[dict[str, Any]], int, int, int]:
    rows = parse_host_rows(raw)
    systems = rows_to_systems(rows)
    footer = re.search(r"-- Active scan completed, (\d+) Hosts found", raw)
    discovered = int(footer.group(1)) if footer else len(systems)
    return systems, 1, 0, discovered


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%a %b %d %H:%M:%S %Y")


def output_mode_for_command(command: str, scenario: dict[str, Any]) -> str:
    if scenario.get("output_mode"):
        return str(scenario["output_mode"])
    if "-P" in command.split():
        return "parsable"
    return "interactive"


def build_netdiscover_scan(
    *,
    command: str,
    scenario_name: str,
    target: str,
    raw_text: str,
    output_mode: str,
    start_time: datetime,
    duration_s: float,
    exit_code: int,
) -> dict[str, Any]:
    if output_mode == "parsable":
        systems, scan_tries, empty_scans, discovered = parse_parsable(raw_text)
    else:
        systems, scan_tries, empty_scans, discovered = parse_interactive(raw_text)

    end_time = start_time + timedelta(seconds=duration_s)
    exit_status = "success" if exit_code == 0 else "error"
    summary = (
        f"NetDiscover done at {format_timestamp(end_time)}; "
        f"{discovered} Systems Discovered, {scan_tries} Scan Tries, "
        f"{empty_scans} Empty Scans, scanned in {duration_s:.2f} seconds"
    )
    return {
        "netdiscover_scan": {
            "scanner": "netdiscover",
            "args": scenario_name,
            "command": command,
            "target": target,
            "start_time": format_timestamp(start_time),
            "systems": systems,
            "runstats": {
                "finished_time": {
                    "end_time": format_timestamp(end_time),
                    "elapsed": round(duration_s, 2),
                    "summary": summary,
                    "exit_status": exit_status,
                },
                "systems": {
                    "discovered": discovered,
                    "scan_tries": scan_tries,
                    "empty_scans": empty_scans,
                },
            },
        }
    }


def validate_structured(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scan = doc.get("netdiscover_scan")
    if not isinstance(scan, dict):
        return ["missing netdiscover_scan object"]
    for field in REQUIRED_SCAN_FIELDS:
        if not scan.get(field):
            errors.append(f"missing netdiscover_scan.{field}")
    runstats = scan.get("runstats", {})
    systems_stats = runstats.get("systems", {})
    if "scan_tries" not in systems_stats:
        errors.append("missing runstats.systems.scan_tries")
    if "systems" not in scan:
        errors.append("missing netdiscover_scan.systems")
    return errors


def text_capture_header(
    *,
    command: str,
    scenario_name: str,
    captured_at: datetime,
) -> str:
    return (
        "# SpiderFeet CLI examination capture\n"
        f"# command: {command}\n"
        f"# scenario: {scenario_name}\n"
        f"# captured_at: {captured_at.astimezone(timezone.utc).isoformat()}\n"
        "\n"
    )


def dumps_structured(doc: dict[str, Any]) -> str:
    return json.dumps(doc, indent=2) + "\n"
