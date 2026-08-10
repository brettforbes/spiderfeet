# -*- coding: utf-8 -*-
"""v2 Nmap CLI module — four-output Text / Structured / Graph / Narrative (R10-14)."""

from __future__ import annotations

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
from modules_v2.adapters.nmap import build_outputs

MODULE_ID = "sfp_cli_nmap"
TOOL_NAME = "nmap"

CONSUMED_INPUTS = [
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "INTERNET_NAME",
    "DOMAIN_NAME",
    "NETBLOCK_OWNER",
    "NETBLOCK_MEMBER",
    "AFFILIATE_IPV4_ADDRESS",
    "AFFILIATE_IPV6_ADDRESS",
    "AFFILIATE_INTERNET_NAME",
    "CO_HOSTED_SITE",
    "PORT",
]

PRODUCED_NUGGET_TYPES = [
    "ACCURACY",
    "APPLICATIONS",
    "CPE_URL",
    "DSA",
    "ECDSA",
    "EDDSA",
    "ENVIRONMENT",
    "HOP_ORDER",
    "HOP_RTT",
    "HOP_TTL",
    "HOST",
    "HOST_STATUS",
    "HOST_STATUS_REASON",
    "HTTP_TITLE",
    "INTERNET_NAME",
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "NETWORKS",
    "OPERATING_SYSTEM",
    "OS_FAMILY",
    "OS_GEN",
    "OS_TYPE",
    "OS_VENDOR",
    "PORT",
    "PORT_PROTOCOL",
    "PORT_SOURCE",
    "PORT_STATE",
    "PORT_STATE_REASON",
    "RSA",
    "SCAN_CLI",
    "SCAN_ELAPSED",
    "SCAN_RECORD",
    "SCAN_START",
    "SCAN_SUMMARY",
    "SCAN_TARGET",
    "SCAN_TOOL",
    "SCAN_VERSION",
    "SERVICE",
    "SERVICE_EXTRAINFO",
    "SERVICE_FINGERPRINT",
    "SERVICE_VERSION",
    "SSH_KEY_BITS",
    "SSH_KEY_KEY",
    "SSH_KEY_TYPE",
    "TRACE",
    "TRACE_HOP",
    "TRACE_PROTOCOL",
    "TRANSPORT",
]

# Short smoke defaults honour structured-first (-oX -) and stay lightweight.
DEFAULT_SMOKE_ARGS = ["-sn", "-T4", "-oX", "-"]


class sfp_cli_nmap(CliModuleBase):
    """Nmap v2 module: argv-only CLI → XML → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "xml"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "NMAP CLI App",
        "summary": "Run Nmap and produce Text, Structured (XML→JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Network discovery"],
        "dataSource": {
            "website": "https://nmap.org/",
            "license": "Nmap Public Source License Version 0.95",
            "repository": "https://github.com/nmap/nmap",
            "references": ["https://nmap.org/book/toc.html"],
            "description": (
                "Nmap ('Network Mapper') is a free and open source utility for "
                "network discovery and security auditing."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build nmap argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``target`` / ``targets`` — host(s) to scan (required unless ``argv`` given)
        - ``args`` — extra nmap flags (list[str]); ``-oX -`` injected if missing
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

            if not _has_ox_stdout(tool_argv):
                tool_argv = list(tool_argv) + ["-oX", "-"]

            targets = scan_step_spec.get("targets")
            if targets is None:
                target = scan_step_spec.get("target")
                targets = [target] if target else []
            if isinstance(targets, str):
                targets = [targets]
            targets = [str(t) for t in targets if t]
            if not targets:
                raise ValueError("scan_step_spec requires target/targets or argv")
            tool_argv = list(tool_argv) + targets

        prefix = scan_step_spec.get("executable_prefix")
        if prefix is not None:
            exe_prefix = ensure_no_shell_string(prefix)
        else:
            exe_prefix, err = resolve_executable(TOOL_NAME)
            if err:
                raise FileNotFoundError(err)

        return ensure_no_shell_string(list(exe_prefix) + list(tool_argv))

    def run_from_xml(
        self,
        xml_text: str,
        *,
        command: Sequence[str] | None = None,
        scenario_key: str = "nmap",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
    ) -> dict[str, Any]:
        """Produce four outputs from captured Nmap XML (fixture / offline path)."""
        outputs = build_outputs(xml_text, scenario_key=scenario_key)
        graph = outputs["graph"]
        result = ModuleResult(
            command=list(command or ["nmap", "-oX", "-", "<fixture>"]),
            text=outputs["text"],
            structured=xml_text,
            structured_type="xml",
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
            hosts=len((outputs["structured"] or {}).get("hosts") or []),
        )
        # Expose intermediate JSON for callers that want the parsed form.
        result["structured_json"] = outputs["structured"]
        return result

    def run(self, scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """Live (or fixture) four-output nmap run.

        Special keys:
        - ``xml_text`` / ``xml_path`` — skip CLI; build four forms from fixture XML
        - ``timeout`` — seconds (default 900)
        - ``scenario_key`` — narrative scenario label
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "nmap")

        if spec.get("xml_text"):
            return self.run_from_xml(
                str(spec["xml_text"]),
                command=spec.get("command") or ["nmap", "-oX", "-", "<xml_text>"],
                scenario_key=scenario_key,
            )
        if spec.get("xml_path"):
            xml_text = Path(spec["xml_path"]).read_text(encoding="utf-8")
            return self.run_from_xml(
                xml_text,
                command=spec.get("command") or ["nmap", "-oX", "-", str(spec["xml_path"])],
                scenario_key=scenario_key,
            )

        try:
            argv = self.build_argv(spec)
        except FileNotFoundError as exc:
            return error_result(
                command=[TOOL_NAME],
                status=STATUS_MISSING_TOOL,
                error=str(exc),
                structured_type="xml",
            )
        except (TypeError, ValueError) as exc:
            return error_result(
                command=[TOOL_NAME],
                status=STATUS_ERROR,
                error=str(exc),
                structured_type="xml",
            )

        timeout = float(spec.get("timeout") or 900.0)
        completed, duration, err = self._timed_run_argv(argv, timeout=timeout)
        if err and completed is None:
            status = STATUS_TIMEOUT if err.startswith("timeout") else STATUS_ERROR
            return error_result(
                command=argv,
                status=status,
                error=err,
                duration=duration,
                structured_type="xml",
            )

        assert completed is not None
        # Workflow argv uses `-oX $step.files.output` (file path). Nmap then
        # writes XML to that file and leaves stdout empty/non-XML — same hydrate
        # pattern as subfinder/httpx `-o` capture (step_runner comment).
        xml_text = completed.stdout or ""
        out_path = _ox_output_file_from_argv(argv)
        if out_path and Path(out_path).is_file():
            file_body = Path(out_path).read_text(encoding="utf-8", errors="replace")
            if file_body.strip():
                xml_text = file_body
        if completed.returncode != 0 and not xml_text.strip():
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"nmap exited {completed.returncode}",
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                structured_type="xml",
            )
        if not xml_text.strip():
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=(
                    "nmap produced empty XML "
                    f"({'file ' + out_path if out_path else 'stdout'})"
                ),
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                structured_type="xml",
            )

        try:
            result = self.run_from_xml(
                xml_text,
                command=argv,
                scenario_key=scenario_key,
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
            )
        except Exception as exc:  # noqa: BLE001 — surface parse/graph failures as ERROR
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"four-output conversion failed: {exc}",
                duration=duration,
                exit_code=completed.returncode,
                stderr=completed.stderr or "",
                structured_type="xml",
            )

        if completed.returncode != 0:
            result["status"] = STATUS_ERROR
            result["error"] = f"nmap exited {completed.returncode}"
        return result


def _has_ox_stdout(argv: Sequence[str]) -> bool:
    for i, part in enumerate(argv):
        if part == "-oX" and i + 1 < len(argv) and argv[i + 1] == "-":
            return True
        if part.startswith("-oX") and part != "-oX":
            # e.g. unusual glued form; treat as present
            return True
    return False


def _ox_output_file_from_argv(argv: Sequence[str]) -> str | None:
    """Return the path after ``-oX`` when it is a real file (not ``-`` / stdout)."""
    for i, part in enumerate(argv):
        if part == "-oX" and i + 1 < len(argv):
            candidate = str(argv[i + 1])
            if candidate == "-" or candidate.startswith("-"):
                return None
            return candidate
        if part.startswith("-oX") and part != "-oX":
            # glued form `-oXfile.xml` (rare)
            glued = part[3:]
            if glued and glued != "-":
                return glued
    return None


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_nmap().run(scan_step_spec)


# End of sfp_cli_nmap
