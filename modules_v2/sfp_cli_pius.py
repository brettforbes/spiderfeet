# -*- coding: utf-8 -*-
"""v2 Pius CLI module — four-output Text / Structured / Graph / Narrative (R10-15)."""

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
from modules_v2.adapters.pius import build_outputs
from modules_v2.adapters.pius.structured import (
    PIUS_STRUCTURED_SCHEMA,
    build_pius_bundle,
    parse_ndjson,
    pius_scan_context,
)

MODULE_ID = "sfp_cli_pius"
TOOL_NAME = "pius"

CONSUMED_INPUTS = [
    "COMPANY_NAME",
    "DOMAIN_NAME",
    "INTERNET_NAME",
]

PRODUCED_NUGGET_TYPES = [
    "AFFILIATE_COMPANY_NAME",
    "AFFILIATES",
    "CANDIDATE_ENTITY",
    "COMPANY_NAME",
    "DOMAIN_NAME",
    "DOMAIN_NAME_PARENT",
    "DOMAIN_REGISTRAR",
    "DOMAINS",
    "LEADS",
    "NETBLOCK_OWNER",
    "PAGE",
    "PAGES",
    "SCAN_CLI",
    "SCAN_ELAPSED",
    "SCAN_EXIT_STATUS",
    "SCAN_RECORD",
    "SCAN_START",
    "SCAN_TARGET",
    "SCAN_TOOL",
]

# Structured-first: --output ndjson is mandatory for automation.
DEFAULT_SMOKE_ARGS = ["run", "--output", "ndjson", "--mode", "passive"]


class sfp_cli_pius(CliModuleBase):
    """Pius v2 module: argv-only CLI → NDJSON → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "json"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "Pius CLI App",
        "summary": "Run Pius and produce Text, Structured (JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Organization discovery"],
        "dataSource": {
            "website": "https://github.com/praetorian-inc/pius",
            "license": "Apache-2.0",
            "repository": "https://github.com/praetorian-inc/pius",
            "references": ["https://github.com/praetorian-inc/pius"],
            "description": (
                "Pius maps an organization's external assets (domains, subdomains, "
                "CIDRs) from an org name and emits structured NDJSON findings."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build pius argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``org`` — required ``--org`` value (unless ``argv``)
        - ``domain`` / ``target`` — optional ``--domain`` hint
        - ``args`` — extra flags (list[str]); ``run`` + ``--output ndjson`` injected
        - ``argv`` — full tool argv *after* the executable (overrides args/org)
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

            tool_argv = _ensure_run_subcommand(tool_argv)
            if not _has_output_ndjson(tool_argv):
                tool_argv = list(tool_argv) + ["--output", "ndjson"]

            org = scan_step_spec.get("org")
            if not org:
                raise ValueError("scan_step_spec requires org or argv")
            if not _has_flag(tool_argv, "--org"):
                tool_argv = list(tool_argv) + ["--org", str(org)]

            domain = scan_step_spec.get("domain") or scan_step_spec.get("target")
            if domain and not _has_flag(tool_argv, "--domain"):
                tool_argv = list(tool_argv) + ["--domain", str(domain)]

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
        scenario_key: str = "pius",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
        org: str | None = None,
        target: str | None = None,
        started_at: datetime | None = None,
    ) -> dict[str, Any]:
        """Produce four outputs from a Pius bundle / NDJSON capture (fixture / offline)."""
        cmd_list = list(command or ["pius", "run", "--output", "ndjson", "<fixture>"])
        cmd_str = " ".join(str(p) for p in cmd_list)
        doc = _normalize_capture(
            raw,
            command=cmd_str,
            scenario_key=scenario_key,
            org=org,
            target=target,
            duration=duration,
            exit_code=exit_code,
            stderr=stderr,
            started_at=started_at,
        )
        outputs = build_outputs(
            doc,
            scenario_key=scenario_key,
            org=org or doc.get("org"),
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
        """Live (or fixture) four-output pius run.

        Special keys:
        - ``structured`` / ``json_text`` — skip CLI; build four forms from bundle/NDJSON
        - ``structured_path`` / ``json_path`` — load fixture from disk
        - ``timeout`` — seconds (default 180)
        - ``scenario_key`` — narrative scenario label
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "pius")
        org = str(spec["org"]) if spec.get("org") else None
        target = _first_domain(spec)

        if spec.get("structured") is not None:
            return self.run_from_structured(
                spec["structured"],
                command=spec.get("command") or ["pius", "run", "--output", "ndjson", "<structured>"],
                scenario_key=scenario_key,
                org=org,
                target=target,
            )
        if spec.get("json_text") is not None:
            return self.run_from_structured(
                str(spec["json_text"]),
                command=spec.get("command") or ["pius", "run", "--output", "ndjson", "<json_text>"],
                scenario_key=scenario_key,
                org=org,
                target=target,
            )
        path_key = spec.get("structured_path") or spec.get("json_path")
        if path_key:
            raw_text = Path(path_key).read_text(encoding="utf-8")
            return self.run_from_structured(
                raw_text,
                command=spec.get("command") or ["pius", "run", "--output", "ndjson", str(path_key)],
                scenario_key=scenario_key,
                org=org,
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

        timeout = float(spec.get("timeout") or 180.0)
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
                error=f"pius exited {completed.returncode}",
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
                org=org or _org_from_argv(argv),
                target=target or _domain_from_argv(argv),
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
            result["error"] = f"pius exited {completed.returncode}"
        return result


def _has_flag(argv: Sequence[str], flag: str) -> bool:
    return flag in argv


def _has_output_ndjson(argv: Sequence[str]) -> bool:
    if "--output" in argv:
        idx = list(argv).index("--output")
        if idx + 1 < len(argv) and str(argv[idx + 1]).lower() == "ndjson":
            return True
    if "-o" in argv:
        idx = list(argv).index("-o")
        if idx + 1 < len(argv) and str(argv[idx + 1]).lower() == "ndjson":
            return True
    return False


def _ensure_run_subcommand(argv: Sequence[str]) -> list[str]:
    parts = list(argv)
    if not parts or parts[0] != "run":
        return ["run"] + parts
    return parts


def _first_domain(spec: Mapping[str, Any]) -> str | None:
    for key in ("domain", "target"):
        value = spec.get(key)
        if value:
            return str(value)
    return None


def _org_from_argv(argv: Sequence[str]) -> str | None:
    if "--org" in argv:
        idx = list(argv).index("--org")
        if idx + 1 < len(argv):
            return str(argv[idx + 1])
    return None


def _domain_from_argv(argv: Sequence[str]) -> str | None:
    if "--domain" in argv:
        idx = list(argv).index("--domain")
        if idx + 1 < len(argv):
            return str(argv[idx + 1])
    return None


def _normalize_capture(
    raw: str | dict[str, Any],
    *,
    command: str,
    scenario_key: str,
    org: str | None,
    target: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    """Ensure a full pius_finding_v1 bundle (NDJSON stdout → bundle with scan meta)."""
    if isinstance(raw, dict):
        doc = dict(raw)
        if "records" not in doc:
            raise ValueError("structured dict requires records[]")
        doc.setdefault("schema", PIUS_STRUCTURED_SCHEMA)
        if not doc.get("command") or doc.get("command") == "pius":
            doc["command"] = command
        if org and not doc.get("org"):
            doc["org"] = org
        if target and not doc.get("target"):
            doc["target"] = target
        return doc

    text = str(raw).strip()
    if not text:
        return _bundle_with_scan(
            [],
            command=command,
            scenario_key=scenario_key,
            org=org,
            target=target,
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
        maybe.setdefault("schema", PIUS_STRUCTURED_SCHEMA)
        if not maybe.get("command") or maybe.get("command") == "pius":
            maybe["command"] = command
        if org and not maybe.get("org"):
            maybe["org"] = org
        if target and not maybe.get("target"):
            maybe["target"] = target
        return maybe
    if isinstance(maybe, list):
        records = [row for row in maybe if isinstance(row, dict)]
        return _bundle_with_scan(
            records,
            command=command,
            scenario_key=scenario_key,
            org=org,
            target=target,
            duration=duration,
            exit_code=exit_code,
            stderr=stderr,
            started_at=started_at,
        )

    records = parse_ndjson(text)
    return _bundle_with_scan(
        records,
        command=command,
        scenario_key=scenario_key,
        org=org,
        target=target,
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
    org: str | None,
    target: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    scan = pius_scan_context(
        command=command,
        scenario_name=scenario_key,
        scenario_id=scenario_key,
        org=org,
        target=target,
        captured_at=started_at or datetime.now(timezone.utc),
        runtime="modules_v2",
        exit_code=exit_code,
        duration_s=duration,
        record_count=len(records),
        stderr_banner=stderr or None,
    )
    return build_pius_bundle(records, scan)


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_pius().run(scan_step_spec)


# End of sfp_cli_pius
