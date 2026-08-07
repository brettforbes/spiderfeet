"""Convert Netdiscover CLI text to approved ``netdiscover_scan`` JSON.

Self-contained port for ``modules_v2`` (TextFSM / regex parse → structured).
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
PLATFORM = "spiderfeet_netdiscover"
COMMAND_PARSABLE = "netdiscover -P"
COMMAND_INTERACTIVE = "netdiscover interactive"

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
CAPTURE_HEADER_RE = re.compile(
    r"^# SpiderFeet CLI examination capture\n(?:# .+\n)*\n",
    re.MULTILINE,
)
HOST_ROW_RE = re.compile(
    r"^(\d{1,3}(?:\.\d{1,3}){3})\s+"
    r"([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})\s+"
    r"(\d+)\s+(\d+)\s+([^\r\n]+)$",
)
MAC_ADDRESS_RE = re.compile(r"[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}")
FOOTER_ACTIVE_RE = re.compile(r"-- Active scan completed, (\d+) Hosts found\.?", re.IGNORECASE)
FOOTER_PASSIVE_RE = re.compile(r"-- Passive capture ended, (\d+) Hosts observed\.?", re.IGNORECASE)

OutputMode = Literal["parsable", "interactive"]


def detect_output_mode_from_text(raw: str) -> OutputMode | None:
    cleaned = strip_ansi(strip_capture_header(raw))
    if "Currently scanning:" in cleaned:
        return "interactive"
    if FOOTER_ACTIVE_RE.search(cleaned) or FOOTER_PASSIVE_RE.search(cleaned):
        return "parsable"
    if HOST_ROW_RE.search(cleaned, re.MULTILINE):
        return "parsable"
    return None


def resolve_output_mode(raw: str, declared: OutputMode) -> OutputMode:
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

    if not MAC_ADDRESS_RE.search(cleaned):
        return []

    try:
        import textfsm
    except ImportError as exc:
        raise RuntimeError("textfsm or ntc-templates required for Netdiscover parsing") from exc

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


def _missing_fields(mapping: dict[str, Any], fields: tuple[str, ...], prefix: str) -> list[str]:
    return [f"missing {prefix}.{field}" for field in fields if field not in mapping]


def _validate_runstats(runstats: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(runstats, dict):
        return ["missing netdiscover_scan.runstats"]

    finished = runstats.get("finished_time")
    if not isinstance(finished, dict):
        errors.append("missing runstats.finished_time")
    else:
        errors.extend(
            _missing_fields(
                finished,
                ("end_time", "elapsed", "summary", "exit_status"),
                "runstats.finished_time",
            )
        )

    systems_stats = runstats.get("systems")
    if not isinstance(systems_stats, dict):
        errors.append("missing runstats.systems")
    else:
        errors.extend(
            _missing_fields(
                systems_stats,
                ("discovered", "scan_tries", "empty_scans"),
                "runstats.systems",
            )
        )
    return errors


def validate_netdiscover_scan(doc: dict[str, Any]) -> list[str]:
    scan = doc.get("netdiscover_scan")
    if not isinstance(scan, dict):
        return ["missing netdiscover_scan root object"]

    errors = [
        f"missing netdiscover_scan.{field}"
        for field in ("scanner", "args", "start_time", "exit_status")
        if not scan.get(field)
    ]
    if "systems" not in scan or not isinstance(scan["systems"], list):
        errors.append("missing netdiscover_scan.systems array")
    errors.extend(_validate_runstats(scan.get("runstats")))
    return errors


def dumps_netdiscover_scan(doc: dict[str, Any]) -> str:
    errors = validate_netdiscover_scan(doc)
    if errors:
        raise ValueError(f"invalid netdiscover_scan JSON: {errors}")
    return json.dumps(doc, indent=4) + "\n"
