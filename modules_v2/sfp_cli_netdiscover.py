# -*- coding: utf-8 -*-
"""v2 Netdiscover CLI module — four-output Text / Structured / Graph / Narrative (R10-15)."""

from __future__ import annotations

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
from modules_v2.adapters.netdiscover import build_outputs

MODULE_ID = "sfp_cli_netdiscover"
TOOL_NAME = "netdiscover"

CONSUMED_INPUTS = [
    "NETBLOCK_OWNER",
    "NETBLOCK_MEMBER",
    "IPV4_ADDRESS",
]

PRODUCED_NUGGET_TYPES = [
    "IPV4_ADDRESS",
    "MAC_ADDRESS",
    "MAC_VENDOR",
    "NETWORKS",
    "SCAN_CLI",
    "SCAN_DISCOVERED",
    "SCAN_EMPTY_SCANS",
    "SCAN_END_TIME",
    "SCAN_EXIT_STATUS",
    "SCAN_RECORD",
    "SCAN_SUMMARY",
    "SCAN_TIMESTAMP",
    "SCAN_TRIES",
    "SYSTEM",
]

# Parsable (-P) is mandatory for automation; -N suppresses the banner when available.
DEFAULT_SMOKE_ARGS = ["-P", "-N", "-f"]


class sfp_cli_netdiscover(CliModuleBase):
    """Netdiscover v2 module: argv-only CLI → text → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "json"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "Netdiscover CLI App",
        "summary": "Run Netdiscover and produce Text, Structured (JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Network discovery"],
        "dataSource": {
            "website": "https://github.com/netdiscover-scanner/netdiscover",
            "license": "GPL-3.0",
            "repository": "https://github.com/netdiscover-scanner/netdiscover",
            "references": ["https://github.com/netdiscover-scanner/netdiscover"],
            "description": (
                "Netdiscover is an active/passive ARP reconnaissance tool for "
                "local Layer-2 network discovery."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build netdiscover argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``range`` / ``target`` — CIDR/range for ``-r`` (optional if ``argv`` given)
        - ``args`` — extra flags (list[str]); ``-P`` injected if missing
        - ``argv`` — full tool argv *after* the executable (overrides args/range)
        - ``executable_prefix`` — optional override for resolved exe prefix
        - ``prefer_sudo`` — when True (default), prefix with ``sudo`` / ``wsl sudo`` when present
        """
        if scan_step_spec.get("argv") is not None:
            tool_argv = ensure_no_shell_string(scan_step_spec["argv"])
        else:
            args = scan_step_spec.get("args")
            if args is None:
                tool_argv = list(DEFAULT_SMOKE_ARGS)
            else:
                tool_argv = ensure_no_shell_string(args)

            if not _has_flag(tool_argv, "-P"):
                tool_argv = ["-P"] + list(tool_argv)

            range_val = scan_step_spec.get("range") or scan_step_spec.get("target")
            if range_val and not _has_flag(tool_argv, "-r"):
                tool_argv = list(tool_argv) + ["-r", str(range_val)]

        prefix = scan_step_spec.get("executable_prefix")
        if prefix is not None:
            exe_prefix = ensure_no_shell_string(prefix)
        else:
            prefer_sudo = bool(scan_step_spec.get("prefer_sudo", True))
            exe_prefix, err = _resolve_netdiscover(prefer_sudo=prefer_sudo)
            if err:
                raise FileNotFoundError(err)

        return ensure_no_shell_string(list(exe_prefix) + list(tool_argv))

    def run_from_text(
        self,
        raw_text: str,
        *,
        command: Sequence[str] | None = None,
        scenario_key: str = "netdiscover",
        scenario_name: str | None = None,
        output_mode: str = "parsable",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
        start_time: datetime | None = None,
    ) -> dict[str, Any]:
        """Produce four outputs from captured Netdiscover text (fixture / offline path)."""
        outputs = build_outputs(
            raw_text,
            scenario_name=scenario_name or scenario_key,
            scenario_key=scenario_key,
            output_mode=output_mode if output_mode in ("parsable", "interactive") else "parsable",
            start_time=start_time or datetime.now(timezone.utc),
            duration_s=duration,
            exit_code=exit_code,
        )
        graph = outputs["graph"]
        systems = (outputs["structured"] or {}).get("netdiscover_scan", {}).get("systems") or []
        result = ModuleResult(
            command=list(command or ["netdiscover", "-P", "<fixture>"]),
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
        annotate_counts(result, graph, systems=len(systems), hosts=len(systems))
        result["structured_json"] = outputs["structured_json"]
        return result

    def run(self, scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """Live (or fixture) four-output netdiscover run.

        Special keys:
        - ``text`` / ``text_path`` — skip CLI; build four forms from fixture text
        - ``timeout`` — seconds (default 90)
        - ``scenario_key`` / ``scenario_name`` — narrative / args labels
        - ``output_mode`` — ``parsable`` (default) or ``interactive``
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "netdiscover")
        scenario_name = str(spec.get("scenario_name") or scenario_key)
        output_mode = str(spec.get("output_mode") or "parsable")

        if spec.get("text") is not None:
            return self.run_from_text(
                str(spec["text"]),
                command=spec.get("command") or ["netdiscover", "-P", "<text>"],
                scenario_key=scenario_key,
                scenario_name=scenario_name,
                output_mode=output_mode,
            )
        if spec.get("text_path"):
            raw_text = Path(spec["text_path"]).read_text(encoding="utf-8")
            return self.run_from_text(
                raw_text,
                command=spec.get("command") or ["netdiscover", "-P", str(spec["text_path"])],
                scenario_key=scenario_key,
                scenario_name=scenario_name,
                output_mode=output_mode,
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

        timeout = float(spec.get("timeout") or 90.0)
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
        raw_text = completed.stdout or ""
        if completed.returncode != 0 and not raw_text.strip():
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"netdiscover exited {completed.returncode}",
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                structured_type="json",
            )

        try:
            result = self.run_from_text(
                raw_text,
                command=argv,
                scenario_key=scenario_key,
                scenario_name=scenario_name or " ".join(argv),
                output_mode=output_mode,
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                start_time=started_at,
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
            result["error"] = f"netdiscover exited {completed.returncode}"
        return result


def _has_flag(argv: Sequence[str], flag: str) -> bool:
    return flag in argv


def _resolve_netdiscover(*, prefer_sudo: bool = True) -> tuple[list[str], str | None]:
    """Resolve netdiscover, optionally wrapping with sudo for CAP_NET_RAW."""
    import shutil

    prefix, err = resolve_executable(TOOL_NAME)
    if err:
        return [], err

    if not prefer_sudo:
        return prefix, None

    # Native: sudo netdiscover …
    if len(prefix) == 1 and shutil.which("sudo"):
        return ["sudo", "-n", prefix[0]], None

    # WSL: wsl sudo -n netdiscover …
    if prefix[:1] == ["wsl"] and len(prefix) == 2:
        return ["wsl", "sudo", "-n", prefix[1]], None

    return prefix, None


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_netdiscover().run(scan_step_spec)


# End of sfp_cli_netdiscover
