# -*- coding: utf-8 -*-
"""v2 Nerva CLI module — four-output Text / Structured / Graph / Narrative (R10-15)."""

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
from modules_v2.adapters.nerva import build_outputs
from modules_v2.adapters.nerva.structured import (
    NERVA_STRUCTURED_SCHEMA,
    build_nerva_bundle,
    nerva_scan_context,
    parse_jsonl,
)

MODULE_ID = "sfp_cli_nerva"
TOOL_NAME = "nerva"

CONSUMED_INPUTS = [
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "INTERNET_NAME",
    "DOMAIN_NAME",
    "TCP_PORT_OPEN",
    "UDP_PORT_OPEN",
    "PORT",
]

PRODUCED_NUGGET_TYPES = [
    "APPLICATIONS",
    "CDN",
    "CDN_POP_CODE",
    "CDN_VENDOR",
    "CPE_URL",
    "DOMAIN_NAME",
    "HOST",
    "HOST_CLASSIFICATION",
    "HTTP_STATUS_CODE",
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "NETWORKS",
    "PORT",
    "SCAN_CLI",
    "SCAN_ELAPSED",
    "SCAN_EXIT_STATUS",
    "SCAN_RECORD",
    "SCAN_START",
    "SCAN_TARGET",
    "SCAN_TOOL",
    "SERVICE",
    "SERVICE_BANNER",
    "SERVICE_VERSION",
    "SOFTWARE_USED",
    "TLS_ENABLED",
    "TRANSPORT",
]

# Structured-first: --json is mandatory; short wait for smoke.
DEFAULT_SMOKE_ARGS = ["--json", "-w", "5000"]


class sfp_cli_nerva(CliModuleBase):
    """Nerva v2 module: argv-only CLI → JSON/JSONL → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "json"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "Nerva CLI App",
        "summary": "Run Nerva and produce Text, Structured (JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Service fingerprinting"],
        "dataSource": {
            "website": "https://github.com/praetorian-inc/nerva",
            "license": "Apache-2.0",
            "repository": "https://github.com/praetorian-inc/nerva",
            "references": ["https://github.com/praetorian-inc/nerva"],
            "description": (
                "Nerva fingerprints open TCP/UDP/SCTP services and emits "
                "structured JSON-lines for protocol identification."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build nerva argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``target`` / ``targets`` — ``host:port`` value(s) for ``-t`` (required unless ``argv``)
        - ``args`` — extra flags (list[str]); ``--json`` injected if missing
        - ``argv`` — full tool argv *after* the executable (overrides args/target)
        - ``executable_prefix`` — optional override for resolved exe prefix
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
                tool_argv = ["--json"] + list(tool_argv)

            targets = scan_step_spec.get("targets")
            if targets is None:
                target = scan_step_spec.get("target")
                targets = [target] if target else []
            if isinstance(targets, str):
                targets = [targets]
            targets = [str(t) for t in targets if t]
            if not targets:
                raise ValueError("scan_step_spec requires target/targets (host:port) or argv")
            if not _has_flag(tool_argv, "-t") and not _has_flag(tool_argv, "--targets"):
                # Comma-joined -t list is the nerva multi-target form.
                tool_argv = list(tool_argv) + ["-t", ",".join(targets)]

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
        scenario_key: str = "nerva",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
        target: str | None = None,
        started_at: datetime | None = None,
    ) -> dict[str, Any]:
        """Produce four outputs from a Nerva bundle / JSONL capture (fixture / offline)."""
        cmd_list = list(command or ["nerva", "--json", "<fixture>"])
        cmd_str = " ".join(str(p) for p in cmd_list)
        doc = _normalize_capture(
            raw,
            command=cmd_str,
            scenario_key=scenario_key,
            target=target,
            duration=duration,
            exit_code=exit_code,
            started_at=started_at,
        )
        outputs = build_outputs(doc, scenario_key=scenario_key, command=cmd_str)
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
        """Live (or fixture) four-output nerva run.

        Special keys:
        - ``structured`` / ``json_text`` — skip CLI; build four forms from bundle/JSONL
        - ``structured_path`` / ``json_path`` — load fixture from disk
        - ``timeout`` — seconds (default 120)
        - ``scenario_key`` — narrative scenario label
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "nerva")
        target = _first_target(spec)

        if spec.get("structured") is not None:
            return self.run_from_structured(
                spec["structured"],
                command=spec.get("command") or ["nerva", "--json", "<structured>"],
                scenario_key=scenario_key,
                target=target,
            )
        if spec.get("json_text") is not None:
            return self.run_from_structured(
                str(spec["json_text"]),
                command=spec.get("command") or ["nerva", "--json", "<json_text>"],
                scenario_key=scenario_key,
                target=target,
            )
        path_key = spec.get("structured_path") or spec.get("json_path")
        if path_key:
            raw_text = Path(path_key).read_text(encoding="utf-8")
            return self.run_from_structured(
                raw_text,
                command=spec.get("command") or ["nerva", "--json", str(path_key)],
                scenario_key=scenario_key,
                target=target,
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
        if completed.returncode != 0 and not raw_out.strip():
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"nerva exited {completed.returncode}",
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
                target=target or _target_from_argv(argv),
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
            result["error"] = f"nerva exited {completed.returncode}"
        return result


def _has_flag(argv: Sequence[str], flag: str) -> bool:
    return flag in argv


def _has_json_flag(argv: Sequence[str]) -> bool:
    return "--json" in argv or "-j" in argv


def _first_target(spec: Mapping[str, Any]) -> str | None:
    targets = spec.get("targets")
    if isinstance(targets, (list, tuple)) and targets:
        return str(targets[0])
    if isinstance(targets, str) and targets:
        return targets
    target = spec.get("target")
    return str(target) if target else None


def _target_from_argv(argv: Sequence[str]) -> str | None:
    for flag in ("-t", "--targets"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return str(argv[idx + 1]).split(",", 1)[0]
    return None


def _normalize_capture(
    raw: str | dict[str, Any],
    *,
    command: str,
    scenario_key: str,
    target: str | None,
    duration: float,
    exit_code: int,
    started_at: datetime | None,
) -> dict[str, Any]:
    """Ensure a full nerva_fingerprint_v1 bundle (JSONL stdout → bundle with scan meta)."""
    if isinstance(raw, dict):
        doc = dict(raw)
        if "records" not in doc:
            raise ValueError("structured dict requires records[]")
        doc.setdefault("schema", NERVA_STRUCTURED_SCHEMA)
        if not doc.get("command") or doc.get("command") == "nerva":
            doc["command"] = command
        if target and not doc.get("target"):
            doc["target"] = target
        return doc

    text = str(raw).strip()
    if not text:
        return _bundle_with_scan(
            [],
            command=command,
            scenario_key=scenario_key,
            target=target,
            duration=duration,
            exit_code=exit_code,
            started_at=started_at,
        )

    # Full bundle JSON (single object with records[]) — keep metadata.
    try:
        maybe = json.loads(text)
    except json.JSONDecodeError:
        maybe = None
    if isinstance(maybe, dict) and "records" in maybe:
        maybe.setdefault("schema", NERVA_STRUCTURED_SCHEMA)
        if not maybe.get("command") or maybe.get("command") == "nerva":
            maybe["command"] = command
        if target and not maybe.get("target"):
            maybe["target"] = target
        return maybe
    if isinstance(maybe, list):
        records = [row for row in maybe if isinstance(row, dict)]
        return _bundle_with_scan(
            records,
            command=command,
            scenario_key=scenario_key,
            target=target,
            duration=duration,
            exit_code=exit_code,
            started_at=started_at,
        )

    # Live tool stdout is JSONL (one object per line).
    records = parse_jsonl(text)
    return _bundle_with_scan(
        records,
        command=command,
        scenario_key=scenario_key,
        target=target,
        duration=duration,
        exit_code=exit_code,
        started_at=started_at,
    )


def _bundle_with_scan(
    records: list[dict[str, Any]],
    *,
    command: str,
    scenario_key: str,
    target: str | None,
    duration: float,
    exit_code: int,
    started_at: datetime | None,
) -> dict[str, Any]:
    scan = nerva_scan_context(
        command=command,
        scenario_name=scenario_key,
        scenario_id=scenario_key,
        target=target,
        captured_at=started_at or datetime.now(timezone.utc),
        runtime="modules_v2",
        exit_code=exit_code,
        duration_s=duration,
        record_count=len(records),
    )
    return build_nerva_bundle(records, scan)


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_nerva().run(scan_step_spec)


# End of sfp_cli_nerva
