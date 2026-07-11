"""Netdiscover SPEC-004 adapter (`text_native`)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Literal

from core.graph_builder import GraphBuilder, nugget_node
from core.topology import add_scan_head, add_system_l2
from narrative_report import build_netdiscover_narrative_report
from netdiscover_text_to_json import (
    OutputMode,
    convert_text_to_netdiscover_scan,
    dumps_netdiscover_scan,
    validate_netdiscover_scan,
)

CAPTURE_FAMILY: Literal["text_native"] = "text_native"


def to_structured(
    raw_text: str,
    *,
    scenario_name: str = "netdiscover scan",
    output_mode: OutputMode = "parsable",
    start_time: datetime | None = None,
    duration_s: float = 0.0,
    exit_code: int = 0,
) -> dict[str, Any]:
    """Convert native Netdiscover text into the approved `netdiscover_scan` document."""
    doc = convert_text_to_netdiscover_scan(
        raw_text,
        scenario_name=scenario_name,
        output_mode=output_mode,
        start_time=start_time or datetime.now(timezone.utc),
        duration_s=duration_s,
        exit_code=exit_code,
    )
    errors = validate_netdiscover_scan(doc)
    if errors:
        raise ValueError(f"invalid netdiscover structured output: {errors}")
    return doc


def to_text(raw_text: str, **_kwargs: Any) -> str:
    """Netdiscover is text-native; preserve the captured text pane content."""
    return raw_text


def _structured_doc(structured: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = json.loads(structured)
    else:
        doc = structured
    errors = validate_netdiscover_scan(doc)
    if errors:
        raise ValueError(f"invalid netdiscover structured output: {errors}")
    return doc


def _add_descriptor(
    builder: GraphBuilder,
    parent_id: str,
    nugget_id: str,
    value: Any,
    *,
    description: str | None = None,
) -> None:
    if value is None or value == "":
        return
    descriptor = builder.add_node(
        nugget_node(nugget_id, str(value), nugget_type="DESCRIPTOR", description=description)
    )
    builder.add_edge(parent_id, descriptor["id"], "had")


def to_graph(structured: dict[str, Any] | str) -> dict[str, Any]:
    """Build Netdiscover graph output using shared SPEC-004 topology helpers."""
    doc = _structured_doc(structured)
    scan_data = doc["netdiscover_scan"]
    args_label = scan_data.get("args", "netdiscover scan")
    runstats = scan_data.get("runstats") or {}
    finished = runstats.get("finished_time") or {}
    systems_stats = runstats.get("systems") or {}

    builder = GraphBuilder()
    scan = add_scan_head(builder, args_label, command=args_label)
    scan_id = scan["id"]

    _add_descriptor(builder, scan_id, "SCAN_TIMESTAMP", scan_data.get("start_time"), description="Scan Start Time")
    _add_descriptor(builder, scan_id, "SCAN_END_TIME", finished.get("end_time"), description="Scan End Time")
    _add_descriptor(builder, scan_id, "SCAN_SUMMARY", finished.get("summary"))
    _add_descriptor(
        builder,
        scan_id,
        "SCAN_EXIT_STATUS",
        scan_data.get("exit_status") or finished.get("exit_status"),
        description="Scan Exit Status",
    )
    _add_descriptor(builder, scan_id, "SCAN_TRIES", systems_stats.get("scan_tries"), description="Scan Tries")
    _add_descriptor(
        builder,
        scan_id,
        "SCAN_EMPTY_SCANS",
        systems_stats.get("empty_scans"),
        description="Empty Scans",
    )
    _add_descriptor(
        builder,
        scan_id,
        "SCAN_DISCOVERED",
        systems_stats.get("discovered"),
        description="Systems Discovered",
    )

    for system in scan_data.get("systems") or []:
        ipv4 = system.get("ipv4")
        if not ipv4:
            continue
        add_system_l2(
            builder,
            scan_id,
            system=ipv4,
            ip_address=ipv4,
            mac_address=system.get("mac"),
            mac_vendor=(str(system.get("mac_vendor") or "").strip() or "Unknown"),
        )

    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "netdiscover") -> str:
    """Build the Markdown report pane for a Netdiscover graph."""
    return build_netdiscover_narrative_report(graph, scenario_key)


def build_outputs(
    raw_text: str,
    *,
    scenario_name: str = "netdiscover scan",
    scenario_key: str = "netdiscover",
    output_mode: OutputMode = "parsable",
    start_time: datetime | None = None,
    duration_s: float = 0.0,
    exit_code: int = 0,
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Netdiscover capture."""
    structured = to_structured(
        raw_text,
        scenario_name=scenario_name,
        output_mode=output_mode,
        start_time=start_time,
        duration_s=duration_s,
        exit_code=exit_code,
    )
    graph = to_graph(structured)
    return {
        "text": to_text(raw_text),
        "structured": structured,
        "structured_json": dumps_netdiscover_scan(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
