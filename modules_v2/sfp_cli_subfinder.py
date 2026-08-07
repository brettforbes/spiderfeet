# -*- coding: utf-8 -*-
"""v2 Subfinder CLI module — four-output Text / Structured / Graph / Narrative (R10-15)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from modules_v2._base import (
    STATUS_ERROR,
    STATUS_MISSING_TOOL,
    STATUS_SUCCESS,
    STATUS_TIMEOUT,
    CliModuleBase,
    ModuleResult,
    annotate_counts,
    ensure_no_shell_string,
    error_result,
    graph_counts,
    resolve_executable,
    utc_now_iso,
)
from modules_v2.adapters.subfinder import build_outputs
from modules_v2.adapters.subfinder.structured import (
    SUBFINDER_STRUCTURED_SCHEMA,
    build_subfinder_bundle,
    normalize_record,
    parse_jsonl,
    subfinder_scan_context,
)

MODULE_ID = "sfp_cli_subfinder"
TOOL_NAME = "subfinder"

CONSUMED_INPUTS = [
    "DOMAIN_NAME",
    "DOMAIN_NAME_PARENT",
    "INTERNET_NAME",
]

PRODUCED_NUGGET_TYPES = [
    "CDN_REVIEW_NEEDED",
    "DISCOVERY_MODE",
    "DISCOVERY_SOURCE",
    "DOMAIN_NAME",
    "DOMAIN_NAME_PARENT",
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "LIVENESS_STATUS",
    "RAW_VALUE",
    "SCAN_CLI",
    "SCAN_ELAPSED",
    "SCAN_EXIT_STATUS",
    "SCAN_MODE",
    "SCAN_RECORD",
    "SCAN_START",
    "SCAN_TARGET",
    "SCAN_TOOL",
]

# Structured-first: -oJ (JSONL) is mandatory; -cs collects sources; stdout (no -o file).
DEFAULT_SMOKE_ARGS = ["-oJ", "-cs", "-silent"]


class sfp_cli_subfinder(CliModuleBase):
    """Subfinder v2 module: argv-only CLI → JSONL → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "json"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "Subfinder CLI App",
        "summary": "Run Subfinder and produce Text, Structured (JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Subdomain enumeration"],
        "dataSource": {
            "website": "https://github.com/projectdiscovery/subfinder",
            "license": "MIT",
            "repository": "https://github.com/projectdiscovery/subfinder",
            "references": ["https://docs.projectdiscovery.io/tools/subfinder"],
            "description": (
                "Subfinder discovers subdomains via passive OSINT sources and optional "
                "active DNS validation, emitting structured JSONL host records."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build subfinder argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``domain`` / ``target`` — ``-d`` value (required unless ``argv``)
        - ``args`` — extra flags (list[str]); ``-oJ`` injected if missing
        - ``argv`` — full tool argv *after* the executable (overrides args/domain)
        - ``executable_prefix`` — optional override for resolved exe prefix
        - ``active`` — when true, inject ``-active`` and ``-oI`` if missing
        """
        if scan_step_spec.get("argv") is not None:
            tool_argv = ensure_no_shell_string(scan_step_spec["argv"])
        else:
            args = scan_step_spec.get("args")
            if args is None:
                tool_argv = list(DEFAULT_SMOKE_ARGS)
            else:
                tool_argv = ensure_no_shell_string(args)

            if not _has_json_flag(tool_argv):
                tool_argv = ["-oJ"] + list(tool_argv)

            if scan_step_spec.get("active"):
                if not _has_flag(tool_argv, "-active") and not _has_flag(tool_argv, "-nW"):
                    tool_argv = list(tool_argv) + ["-active"]
                if not _has_flag(tool_argv, "-oI") and not _has_flag(tool_argv, "-ip"):
                    tool_argv = list(tool_argv) + ["-oI"]

            domain = scan_step_spec.get("domain") or scan_step_spec.get("target")
            if not domain:
                raise ValueError("scan_step_spec requires domain/target or argv")
            if not _has_flag(tool_argv, "-d") and not _has_flag(tool_argv, "-domain"):
                tool_argv = list(tool_argv) + ["-d", str(domain)]

        prefix = scan_step_spec.get("executable_prefix")
        if prefix is not None:
            exe_prefix = ensure_no_shell_string(prefix)
        else:
            exe_prefix, err = resolve_executable(TOOL_NAME)
            if err:
                raise FileNotFoundError(err)

        return ensure_no_shell_string(list(exe_prefix) + list(tool_argv))

    def run_from_structured(
        self,
        raw: str | dict[str, Any],
        *,
        command: Sequence[str] | None = None,
        scenario_key: str = "subfinder",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
        target: str | None = None,
        enumeration_mode: str | None = None,
        started_at: datetime | None = None,
    ) -> dict[str, Any]:
        """Produce four outputs from a Subfinder bundle / JSONL capture (fixture / offline)."""
        cmd_list = list(command or ["subfinder", "-oJ", "<fixture>"])
        cmd_str = " ".join(str(p) for p in cmd_list)
        mode = enumeration_mode or _mode_from_argv(cmd_list) or "passive"
        doc = _normalize_capture(
            raw,
            command=cmd_str,
            scenario_key=scenario_key,
            target=target,
            enumeration_mode=mode,
            duration=duration,
            exit_code=exit_code,
            stderr=stderr,
            started_at=started_at,
        )
        outputs = build_outputs(
            doc,
            scenario_key=scenario_key,
            target=target or doc.get("target"),
            command=cmd_str,
        )
        graph = outputs["graph"]
        records = (outputs["structured"] or {}).get("records") or []
        result = ModuleResult(
            command=cmd_list,
            text=outputs["text"],
            structured=outputs["structured"],
            structured_type="json",
            graph=graph,
            narrative=outputs["markdown_report"],
            status=STATUS_SUCCESS,
            counts=graph_counts(graph),
            duration=duration,
            timestamp=utc_now_iso(),
            exit_code=exit_code,
            stderr=stderr,
        ).to_dict()
        annotate_counts(
            result,
            graph,
            records=len(records),
            hosts=result["counts"].get("hosts", 0),
        )
        result["structured_json"] = outputs["structured_json"]
        return result

    def run(self, scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """Live (or fixture) four-output subfinder run.

        Special keys:
        - ``structured`` / ``json_text`` — skip CLI; build four forms from bundle/JSONL
        - ``structured_path`` / ``json_path`` — load fixture from disk
        - ``timeout`` — seconds (default 120)
        - ``scenario_key`` — narrative scenario label
        - ``enumeration_mode`` — ``passive`` / ``active`` (inferred from argv when omitted)
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "subfinder")
        target = _first_domain(spec)
        enumeration_mode = (
            str(spec["enumeration_mode"])
            if spec.get("enumeration_mode")
            else ("active" if spec.get("active") else None)
        )

        if spec.get("structured") is not None:
            return self.run_from_structured(
                spec["structured"],
                command=spec.get("command") or ["subfinder", "-oJ", "<structured>"],
                scenario_key=scenario_key,
                target=target,
                enumeration_mode=enumeration_mode,
            )
        if spec.get("json_text") is not None:
            return self.run_from_structured(
                str(spec["json_text"]),
                command=spec.get("command") or ["subfinder", "-oJ", "<json_text>"],
                scenario_key=scenario_key,
                target=target,
                enumeration_mode=enumeration_mode,
            )
        path_key = spec.get("structured_path") or spec.get("json_path")
        if path_key:
            raw_text = Path(path_key).read_text(encoding="utf-8")
            return self.run_from_structured(
                raw_text,
                command=spec.get("command") or ["subfinder", "-oJ", str(path_key)],
                scenario_key=scenario_key,
                target=target,
                enumeration_mode=enumeration_mode,
            )

        try:
            argv = self.build_argv(spec)
        except FileNotFoundError as exc:
            return error_result(
                command=[TOOL_NAME],
                status=STATUS_MISSING_TOOL,
                error=str(exc),
                structured_type="json",
            )
        except (TypeError, ValueError) as exc:
            return error_result(
                command=[TOOL_NAME],
                status=STATUS_ERROR,
                error=str(exc),
                structured_type="json",
            )

        timeout = float(spec.get("timeout") or 120.0)
        started_at = datetime.now(timezone.utc)
        completed, duration, err = self._timed_run_argv(argv, timeout=timeout)
        if err and completed is None:
            status = STATUS_TIMEOUT if err.startswith("timeout") else STATUS_ERROR
            return error_result(
                command=argv,
                status=status,
                error=err,
                duration=duration,
                structured_type="json",
            )

        assert completed is not None
        raw_out = completed.stdout or ""
        # When -o writes to a file, hydrate stdout from that path.
        out_path = _output_file_from_argv(argv)
        if out_path and Path(out_path).is_file():
            file_body = Path(out_path).read_text(encoding="utf-8", errors="replace")
            if file_body.strip():
                raw_out = file_body

        if completed.returncode != 0 and not raw_out.strip():
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"subfinder exited {completed.returncode}",
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                structured_type="json",
            )

        try:
            result = self.run_from_structured(
                raw_out,
                command=argv,
                scenario_key=scenario_key,
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                target=target or _domain_from_argv(argv),
                enumeration_mode=enumeration_mode or _mode_from_argv(argv),
                started_at=started_at,
            )
        except Exception as exc:  # noqa: BLE001 — surface parse/graph failures as ERROR
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"four-output conversion failed: {exc}",
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                structured_type="json",
            )

        if completed.returncode != 0:
            result["status"] = STATUS_ERROR
            result["error"] = f"subfinder exited {completed.returncode}"
        return result


def _has_flag(argv: Sequence[str], flag: str) -> bool:
    return flag in argv


def _has_json_flag(argv: Sequence[str]) -> bool:
    return "-oJ" in argv or "-json" in argv


def _first_domain(spec: Mapping[str, Any]) -> str | None:
    for key in ("domain", "target"):
        value = spec.get(key)
        if value:
            return str(value)
    return None


def _domain_from_argv(argv: Sequence[str]) -> str | None:
    for flag in ("-d", "-domain"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return str(argv[idx + 1]).split(",", 1)[0]
    return None


def _mode_from_argv(argv: Sequence[str]) -> str:
    if "-active" in argv or "-nW" in argv:
        return "active"
    return "passive"


def _output_file_from_argv(argv: Sequence[str]) -> str | None:
    for flag in ("-o", "-output"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                candidate = str(argv[idx + 1])
                if candidate.startswith("-"):
                    return None
                return candidate
    return None


def _normalize_capture(
    raw: str | dict[str, Any],
    *,
    command: str,
    scenario_key: str,
    target: str | None,
    enumeration_mode: str,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    """Ensure a full subfinder_host_v1 bundle (JSONL stdout → bundle with scan meta)."""
    if isinstance(raw, dict):
        doc = dict(raw)
        if "records" not in doc:
            raise ValueError("structured dict requires records[]")
        doc.setdefault("schema", SUBFINDER_STRUCTURED_SCHEMA)
        if not doc.get("command") or doc.get("command") == "subfinder":
            doc["command"] = command
        if target and not doc.get("target"):
            doc["target"] = target
        if not doc.get("enumeration_mode"):
            doc["enumeration_mode"] = enumeration_mode
        return doc

    text = str(raw).strip()
    if not text:
        return _bundle_with_scan(
            [],
            command=command,
            scenario_key=scenario_key,
            target=target,
            enumeration_mode=enumeration_mode,
            duration=duration,
            exit_code=exit_code,
            stderr=stderr,
            started_at=started_at,
        )

    try:
        maybe = json.loads(text)
    except json.JSONDecodeError:
        maybe = None
    if isinstance(maybe, dict) and "records" in maybe:
        maybe.setdefault("schema", SUBFINDER_STRUCTURED_SCHEMA)
        if not maybe.get("command") or maybe.get("command") == "subfinder":
            maybe["command"] = command
        if target and not maybe.get("target"):
            maybe["target"] = target
        if not maybe.get("enumeration_mode"):
            maybe["enumeration_mode"] = enumeration_mode
        return maybe
    if isinstance(maybe, list):
        records = [
            normalize_record(row, mode=enumeration_mode)
            for row in maybe
            if isinstance(row, dict)
        ]
        return _bundle_with_scan(
            records,
            command=command,
            scenario_key=scenario_key,
            target=target,
            enumeration_mode=enumeration_mode,
            duration=duration,
            exit_code=exit_code,
            stderr=stderr,
            started_at=started_at,
        )

    records = [
        normalize_record(row, mode=enumeration_mode) for row in parse_jsonl(text)
    ]
    return _bundle_with_scan(
        records,
        command=command,
        scenario_key=scenario_key,
        target=target,
        enumeration_mode=enumeration_mode,
        duration=duration,
        exit_code=exit_code,
        stderr=stderr,
        started_at=started_at,
    )


def _bundle_with_scan(
    records: list[dict[str, Any]],
    *,
    command: str,
    scenario_key: str,
    target: str | None,
    enumeration_mode: str,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    scan = subfinder_scan_context(
        command=command,
        scenario_name=scenario_key,
        scenario_id=scenario_key,
        target=target,
        enumeration_mode=enumeration_mode,
        captured_at=started_at or datetime.now(timezone.utc),
        runtime="modules_v2",
        exit_code=exit_code,
        duration_s=duration,
        record_count=len(records),
        stderr_banner=stderr or None,
    )
    return build_subfinder_bundle(records, scan)


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_subfinder().run(scan_step_spec)


# End of sfp_cli_subfinder
