#!/usr/bin/env python3
"""Convert NetDiscover CLI text output to approved netdiscover_scan JSON.

Uses NTC Templates (parse_output) with project-local TextFSM templates under
``.docs/docs-for-cli-tools/textfsm_templates/``.

Approved schema: ``.seed/06A_Updates_to_NetDiscover_Cli_App_Profiling copy.md``
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_DIR = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "textfsm_templates"
PLATFORM = "spiderfeet_netdiscover"
COMMAND_PARSABLE = "netdiscover -P"
COMMAND_INTERACTIVE = "netdiscover interactive"

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[0-9;]*[a-zA-Z]")
CAPTURE_HEADER_RE = re.compile(
    r"^# SpiderFeet CLI examination capture\n(?:# .+\n)*\n",
    re.MULTILINE,
)
HOST_ROW_RE = re.compile(
    r"^(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:]{17})\s+(\d+)\s+(\d+)\s+(.+)$",
)
FOOTER_ACTIVE_RE = re.compile(r"-- Active scan completed, (\d+) Hosts found\.?", re.IGNORECASE)
FOOTER_PASSIVE_RE = re.compile(r"-- Passive capture ended, (\d+) Hosts observed\.?", re.IGNORECASE)
TRUNCATION_PATTERNS = ("| head", "| tail", "head -", "tail -")

OutputMode = Literal["parsable", "interactive"]


def assert_no_truncation(command: str, scenario_id: str = "") -> None:
    lowered = command.lower()
    for pattern in TRUNCATION_PATTERNS:
        if pattern in lowered:
            label = f"scenario '{scenario_id}'" if scenario_id else "command"
            raise SystemExit(
                f"Truncation forbidden in {label}: contains '{pattern.strip()}' — {command}"
            )


def detect_output_mode_from_text(raw: str) -> OutputMode | None:
    """Infer interactive TUI vs flat parsable output from captured text."""
    cleaned = strip_ansi(strip_capture_header(raw))
    if "Currently scanning:" in cleaned:
        return "interactive"
    if FOOTER_ACTIVE_RE.search(cleaned) or FOOTER_PASSIVE_RE.search(cleaned):
        return "parsable"
    if HOST_ROW_RE.search(cleaned, re.MULTILINE):
        return "parsable"
    return None


def resolve_output_mode(raw: str, declared: OutputMode) -> OutputMode:
    """Prefer text-shape detection over manifest declaration when they disagree."""
    detected = detect_output_mode_from_text(raw)
    if detected is not None:
        return detected
    return declared


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def strip_capture_header(text: str) -> str:
    return CAPTURE_HEADER_RE.sub("", text, count=1)


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%a %b %d %H:%M:%S %Y")


def parse_host_rows_ntc(raw: str, *, command: str = COMMAND_PARSABLE) -> list[dict[str, str]]:
    """Parse host table rows via NTC Templates, with regex/TextFSM fallback."""
    cleaned = strip_ansi(strip_capture_header(raw))
    try:
        from ntc_templates.parse import parse_output

        rows = parse_output(
            platform=PLATFORM,
            command=command,
            data=cleaned,
            template_dir=str(TEMPLATE_DIR),
        )
        if rows:
            return [_normalize_row(row) for row in rows]
    except ImportError:
        pass
    except Exception:
        pass

    rows: list[dict[str, str]] = []
    for line in cleaned.splitlines():
        match = HOST_ROW_RE.match(line.strip())
        if match:
            rows.append(
                {
                    "IP": match.group(1),
                    "MAC": match.group(2),
                    "COUNT": match.group(3),
                    "LEN": match.group(4),
                    "VENDOR": match.group(5).strip(),
                }
            )
    if rows:
        return [_normalize_row(row) for row in rows]

    try:
        import textfsm
    except ImportError as exc:
        raise RuntimeError(
            "textfsm or ntc-templates required for NetDiscover parsing"
        ) from exc

    template_path = TEMPLATE_DIR / "spiderfeet_netdiscover_host_row.textfsm"
    with template_path.open(encoding="utf-8") as fh:
        fsm = textfsm.TextFSM(fh)
    return [_normalize_row(row) for row in fsm.ParseTextToDicts(cleaned)]


def _normalize_row(row: dict[str, Any]) -> dict[str, str]:
    ip = row.get("IP") or row.get("ip") or ""
    mac = row.get("MAC") or row.get("mac") or ""
    count = str(row.get("COUNT") or row.get("count") or "0")
    length = str(row.get("LEN") or row.get("len") or "0")
    vendor = str(row.get("VENDOR") or row.get("vendor") or row.get("mac_vendor") or "").strip()
    return {"IP": ip, "MAC": mac, "COUNT": count, "LEN": length, "VENDOR": vendor}


def rows_to_systems(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    systems: list[dict[str, Any]] = []
    for row in rows:
        if not row.get("IP") or not row.get("MAC"):
            continue
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
    cleaned = strip_ansi(strip_capture_header(raw))
    if "Currently scanning:" not in cleaned:
        return [cleaned] if cleaned.strip() else []
    parts = re.split(r"(?=Currently scanning:)", cleaned)
    return [part for part in parts if part.strip()]


def frame_host_count(frame: str) -> int:
    match = re.search(r"from (\d+) hosts", frame, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def parse_parsable_body(raw: str) -> tuple[list[dict[str, Any]], int, int, int]:
    rows = parse_host_rows_ntc(raw, command=COMMAND_PARSABLE)
    systems = rows_to_systems(rows)
    footer = FOOTER_ACTIVE_RE.search(raw) or FOOTER_PASSIVE_RE.search(raw)
    discovered = int(footer.group(1)) if footer else len(systems)
    return systems, 1, 0, discovered


def parse_interactive_body(raw: str) -> tuple[list[dict[str, Any]], int, int, int]:
    frames = split_tui_frames(raw)
    if not frames:
        return [], 1, 1, 0

    scan_tries = len(frames)
    empty_scans = 0
    systems: list[dict[str, Any]] = []
    discovered = 0

    for frame in frames:
        rows = parse_host_rows_ntc(frame, command=COMMAND_INTERACTIVE)
        if rows:
            if not systems:
                systems = rows_to_systems(rows)
                discovered = len(systems)
        else:
            empty_scans += 1

    if not systems and frames:
        footer = FOOTER_ACTIVE_RE.search(raw) or FOOTER_PASSIVE_RE.search(raw)
        if footer:
            discovered = int(footer.group(1))

    return systems, scan_tries, empty_scans, discovered


def stats_from_text(raw_text: str, *, output_mode: OutputMode) -> tuple[int, int, int, int]:
    """Return (discovered, scan_tries, empty_scans, system_count) derived from text only."""
    effective_mode = resolve_output_mode(raw_text, output_mode)
    if effective_mode == "parsable":
        systems, scan_tries, empty_scans, discovered = parse_parsable_body(raw_text)
    else:
        systems, scan_tries, empty_scans, discovered = parse_interactive_body(raw_text)
    return discovered, scan_tries, empty_scans, len(systems)


def verify_text_structured_alignment(
    raw_text: str,
    doc: dict[str, Any],
    *,
    output_mode: OutputMode,
) -> list[str]:
    """Ensure structured runstats match what the captured text actually contains."""
    errors: list[str] = []
    scan = doc.get("netdiscover_scan", {})
    stats = (scan.get("runstats") or {}).get("systems") or {}
    discovered, scan_tries, empty_scans, system_count = stats_from_text(
        raw_text, output_mode=output_mode
    )

    for field, expected in (
        ("discovered", discovered),
        ("scan_tries", scan_tries),
        ("empty_scans", empty_scans),
    ):
        actual = stats.get(field)
        if actual != expected:
            errors.append(
                f"runstats.systems.{field}={actual!r} but text implies {expected!r}"
            )

    systems = scan.get("systems") or []
    if len(systems) != system_count:
        errors.append(
            f"netdiscover_scan.systems has {len(systems)} rows but text implies {system_count}"
        )
    return errors


def build_args_label(scenario_name: str) -> str:
    name = scenario_name.strip()
    if name.lower().startswith("netdiscover"):
        return name
    return f"netdiscover — {name}"


def convert_text_to_netdiscover_scan(
    raw_text: str,
    *,
    scenario_name: str,
    output_mode: OutputMode,
    start_time: datetime,
    duration_s: float,
    exit_code: int,
) -> dict[str, Any]:
    """Return ``{"netdiscover_scan": {...}}`` matching the approved prompt schema."""
    effective_mode = resolve_output_mode(raw_text, output_mode)
    if effective_mode == "parsable":
        systems, scan_tries, empty_scans, discovered = parse_parsable_body(raw_text)
    else:
        systems, scan_tries, empty_scans, discovered = parse_interactive_body(raw_text)

    if scan_tries < 1:
        scan_tries = 1
    if empty_scans < 0:
        empty_scans = 0

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
            "args": build_args_label(scenario_name),
            "start_time": format_timestamp(start_time),
            "exit_status": exit_status,
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


def validate_netdiscover_scan(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scan = doc.get("netdiscover_scan")
    if not isinstance(scan, dict):
        return ["missing netdiscover_scan root object"]

    for field in ("scanner", "args", "start_time", "exit_status"):
        if not scan.get(field):
            errors.append(f"missing netdiscover_scan.{field}")

    if "systems" not in scan or not isinstance(scan["systems"], list):
        errors.append("missing netdiscover_scan.systems array")

    runstats = scan.get("runstats")
    if not isinstance(runstats, dict):
        errors.append("missing netdiscover_scan.runstats")
        return errors

    finished = runstats.get("finished_time")
    if not isinstance(finished, dict):
        errors.append("missing runstats.finished_time")
    else:
        for field in ("end_time", "elapsed", "summary", "exit_status"):
            if field not in finished:
                errors.append(f"missing runstats.finished_time.{field}")

    systems_stats = runstats.get("systems")
    if not isinstance(systems_stats, dict):
        errors.append("missing runstats.systems")
    else:
        for field in ("discovered", "scan_tries", "empty_scans"):
            if field not in systems_stats:
                errors.append(f"missing runstats.systems.{field}")

    return errors


def dumps_netdiscover_scan(doc: dict[str, Any]) -> str:
    errors = validate_netdiscover_scan(doc)
    if errors:
        raise ValueError(f"invalid netdiscover_scan JSON: {errors}")
    return json.dumps(doc, indent=4) + "\n"


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


def output_mode_for_scenario(scenario: dict[str, Any], command: str) -> OutputMode:
    if scenario.get("output_mode") in ("parsable", "interactive"):
        return scenario["output_mode"]
    if "-P" in command.split():
        return "parsable"
    return "interactive"


def convert_file(text_path: Path, json_path: Path, **kwargs: Any) -> dict[str, Any]:
    raw = text_path.read_text(encoding="utf-8", errors="replace")
    doc = convert_text_to_netdiscover_scan(raw, **kwargs)
    json_path.write_text(dumps_netdiscover_scan(doc), encoding="utf-8")
    return doc
