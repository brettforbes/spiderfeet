# -*- coding: utf-8 -*-
"""v2 Httpx CLI module — four-output Text / Structured / Graph / Narrative (R10-15)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

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
from modules_v2.adapters.httpx import build_outputs
from modules_v2.adapters.httpx.structured import (
    HTTPX_STRUCTURED_SCHEMA,
    build_httpx_bundle,
    httpx_scan_context,
    parse_jsonl,
)

MODULE_ID = "sfp_cli_httpx"
TOOL_NAME = "httpx"

CONSUMED_INPUTS = [
    "DOMAIN_NAME",
    "INTERNET_NAME",
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "LINKED_URL_INTERNAL",
    "LINKED_URL_EXTERNAL",
]

PRODUCED_NUGGET_TYPES = [
    "APPLICATIONS",
    "CDN",
    "CDN_NAME",
    "CDN_TYPE",
    "CONTENT_LENGTH",
    "CONTENT_TYPE",
    "DOMAIN_NAME",
    "HOST",
    "HTTP_LIVENESS_STATUS",
    "HTTP_METHOD",
    "HTTP_PATH",
    "HTTP_STATUS_CODE",
    "HTTP_TITLE",
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "NETWORKS",
    "PORT",
    "PROBE_CONNECTED",
    "PROBE_FAILED",
    "PROBE_TIMESTAMP",
    "RESPONSE_TIME_MS",
    "SCAN_CLI",
    "SCAN_ELAPSED",
    "SCAN_EXIT_STATUS",
    "SCAN_HOST_INPUT_COUNT",
    "SCAN_PROBE_PROFILE",
    "SCAN_RECORD",
    "SCAN_START",
    "SCAN_TARGET",
    "SCAN_TOOL",
    "SERVICE",
    "SOFTWARE_USED",
    "SOFTWARE_VERSION",
    "TRANSPORT",
    "UPSTREAM_SCENARIO_ID",
]

# Structured-first: -json is mandatory; rich probe profile for smoke.
DEFAULT_SMOKE_ARGS = [
    "-json",
    "-status-code",
    "-title",
    "-tech-detect",
    "-server",
    "-cdn",
    "-ip",
    "-silent",
    "-no-stdin",
]

DEFAULT_PROBE_PROFILE = "status-code,title,tech-detect,server,cdn,ip"


class sfp_cli_httpx(CliModuleBase):
    """Httpx v2 module: argv-only CLI → JSONL → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "json"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "Httpx CLI App",
        "summary": "Run Httpx and produce Text, Structured (JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["HTTP probing"],
        "dataSource": {
            "website": "https://github.com/projectdiscovery/httpx",
            "license": "MIT",
            "repository": "https://github.com/projectdiscovery/httpx",
            "references": ["https://docs.projectdiscovery.io/tools/httpx"],
            "description": (
                "Httpx probes HTTP/HTTPS surfaces for liveness, status, title, "
                "tech stack, CDN, and IP metadata via structured JSONL."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build httpx argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``url`` / ``target`` / ``urls`` / ``hosts`` — ``-u`` value(s)
        - ``host_list`` — path for ``-l``
        - ``args`` — extra flags (list[str]); ``-json`` injected if missing
        - ``argv`` — full tool argv *after* the executable (overrides args/url)
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
                tool_argv = ["-json"] + list(tool_argv)
            if not _has_flag(tool_argv, "-no-stdin") and not _has_flag(tool_argv, "-no-stdin=false"):
                # Avoid stdin hang when launching without a pipe (esp. Windows/WSL).
                tool_argv = list(tool_argv) + ["-no-stdin"]

            host_list = scan_step_spec.get("host_list")
            urls = _collect_urls(scan_step_spec)
            has_u = _has_flag(tool_argv, "-u") or _has_flag(tool_argv, "-target")
            has_l = _has_flag(tool_argv, "-l") or _has_flag(tool_argv, "-list")

            if host_list and not has_l:
                tool_argv = list(tool_argv) + ["-l", str(host_list)]
            elif urls and not has_u and not has_l:
                tool_argv = list(tool_argv) + ["-u", ",".join(urls)]
            elif not host_list and not urls and not has_u and not has_l:
                raise ValueError(
                    "scan_step_spec requires url/target/urls/hosts/host_list or argv"
                )

        prefix = scan_step_spec.get("executable_prefix")
        if prefix is not None:
            exe_prefix = ensure_no_shell_string(prefix)
        else:
            exe_prefix, err = _resolve_httpx_executable()
            if err:
                raise FileNotFoundError(err)

        return ensure_no_shell_string(list(exe_prefix) + list(tool_argv))

    def run_from_structured(
        self,
        raw: str | dict[str, Any],
        *,
        command: Sequence[str] | None = None,
        scenario_key: str = "httpx",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
        target: str | None = None,
        probe_profile: str | None = None,
        host_input_count: int | None = None,
        subfinder_scenario: str | None = None,
        started_at: datetime | None = None,
    ) -> dict[str, Any]:
        """Produce four outputs from an Httpx bundle / JSONL capture (fixture / offline)."""
        cmd_list = list(command or ["httpx", "-json", "<fixture>"])
        cmd_str = " ".join(str(p) for p in cmd_list)
        profile = probe_profile or _probe_profile_from_argv(cmd_list) or DEFAULT_PROBE_PROFILE
        doc = _normalize_capture(
            raw,
            command=cmd_str,
            scenario_key=scenario_key,
            target=target,
            probe_profile=profile,
            host_input_count=host_input_count,
            subfinder_scenario=subfinder_scenario,
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
        """Live (or fixture) four-output httpx run.

        Special keys:
        - ``structured`` / ``json_text`` — skip CLI; build four forms from bundle/JSONL
        - ``structured_path`` / ``json_path`` — load fixture from disk
        - ``timeout`` — seconds (default 120)
        - ``scenario_key`` — narrative scenario label
        - ``probe_profile`` — scan metadata label (inferred from argv when omitted)
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "httpx")
        target = _first_target(spec)
        probe_profile = (
            str(spec["probe_profile"]) if spec.get("probe_profile") else None
        )
        host_input_count = spec.get("host_input_count")
        if host_input_count is None:
            urls = _collect_urls(spec)
            host_input_count = len(urls) if urls else None
        subfinder_scenario = (
            str(spec["subfinder_scenario"]) if spec.get("subfinder_scenario") else None
        )

        if spec.get("structured") is not None:
            return self.run_from_structured(
                spec["structured"],
                command=spec.get("command") or ["httpx", "-json", "<structured>"],
                scenario_key=scenario_key,
                target=target,
                probe_profile=probe_profile,
                host_input_count=host_input_count,
                subfinder_scenario=subfinder_scenario,
            )
        if spec.get("json_text") is not None:
            return self.run_from_structured(
                str(spec["json_text"]),
                command=spec.get("command") or ["httpx", "-json", "<json_text>"],
                scenario_key=scenario_key,
                target=target,
                probe_profile=probe_profile,
                host_input_count=host_input_count,
                subfinder_scenario=subfinder_scenario,
            )
        path_key = spec.get("structured_path") or spec.get("json_path")
        if path_key:
            raw_text = Path(path_key).read_text(encoding="utf-8")
            return self.run_from_structured(
                raw_text,
                command=spec.get("command") or ["httpx", "-json", str(path_key)],
                scenario_key=scenario_key,
                target=target,
                probe_profile=probe_profile,
                host_input_count=host_input_count,
                subfinder_scenario=subfinder_scenario,
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
        out_path = _output_file_from_argv(argv)
        if out_path and Path(out_path).is_file():
            file_body = Path(out_path).read_text(encoding="utf-8", errors="replace")
            if file_body.strip():
                raw_out = file_body

        if completed.returncode != 0 and not raw_out.strip():
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"httpx exited {completed.returncode}",
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
                probe_profile=probe_profile or _probe_profile_from_argv(argv),
                host_input_count=host_input_count or _host_input_count_from_argv(argv),
                subfinder_scenario=subfinder_scenario,
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
            result["error"] = f"httpx exited {completed.returncode}"
        return result


def _has_flag(argv: Sequence[str], flag: str) -> bool:
    return flag in argv


def _has_json_flag(argv: Sequence[str]) -> bool:
    return "-json" in argv or "-j" in argv


def _repo_tools_httpx() -> Path | None:
    """Prefer repo-local ProjectDiscovery binary over the Python httpx package."""
    root = Path(__file__).resolve().parents[1]
    for name in ("httpx.exe", "httpx"):
        candidate = root / ".tools" / "bin" / name
        if candidate.is_file():
            return candidate
    return None


def _is_projectdiscovery_httpx(prefix: Sequence[str]) -> bool:
    """Reject the Python ``httpx`` CLI; accept ProjectDiscovery ``httpx -version``."""
    try:
        probe = subprocess.run(
            list(prefix) + ["-version"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    blob = f"{probe.stdout or ''}\n{probe.stderr or ''}".lower()
    if "required dependencies were not installed" in blob:
        return False
    if "pip install" in blob and "httpx[cli]" in blob:
        return False
    # ProjectDiscovery prints an ASCII banner and/or version line.
    return "projectdiscovery" in blob or "__    __" in (probe.stdout or probe.stderr or "")


def _resolve_httpx_executable() -> tuple[list[str], str | None]:
    """Resolve ProjectDiscovery httpx (never the Python package shim)."""
    env_path = os.environ.get("SPIDERFEET_HTTPX") or os.environ.get("HTTPX_BIN")
    candidates: list[list[str]] = []
    if env_path:
        candidates.append([env_path])
    tools = _repo_tools_httpx()
    if tools is not None:
        candidates.append([str(tools)])

    # Native PATH may point at the Python package; probe and skip impostors.
    native = shutil.which("httpx")
    if native:
        candidates.append([native])

    prefix, err = resolve_executable(TOOL_NAME, prefer_wsl=True)
    if prefix:
        candidates.append(list(prefix))

    seen: set[tuple[str, ...]] = set()
    for candidate in candidates:
        key = tuple(candidate)
        if key in seen:
            continue
        seen.add(key)
        if _is_projectdiscovery_httpx(candidate):
            return candidate, None

    return [], (
        "ProjectDiscovery httpx not found "
        "(looked at SPIDERFEET_HTTPX/HTTPX_BIN, .tools/bin/httpx, PATH, WSL); "
        "refusing Python httpx package"
    )


def _collect_urls(spec: Mapping[str, Any]) -> list[str]:
    urls: list[str] = []
    for key in ("urls", "hosts"):
        value = spec.get(key)
        if value is None:
            continue
        if isinstance(value, str):
            urls.extend([part.strip() for part in value.split(",") if part.strip()])
        else:
            urls.extend([str(part).strip() for part in value if str(part).strip()])
    for key in ("url", "target"):
        value = spec.get(key)
        if value:
            urls.append(str(value).strip())
    # Preserve order, drop duplicates.
    seen: set[str] = set()
    ordered: list[str] = []
    for item in urls:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _first_target(spec: Mapping[str, Any]) -> str | None:
    for key in ("target", "url", "domain"):
        value = spec.get(key)
        if value:
            return _hostname_like(str(value))
    urls = _collect_urls(spec)
    if urls:
        return _hostname_like(urls[0])
    host_list = spec.get("host_list")
    if host_list:
        return Path(str(host_list)).stem
    return None


def _hostname_like(value: str) -> str:
    text = value.strip()
    if "://" in text or "/" in text:
        parsed = urlparse(text if "://" in text else f"https://{text}")
        if parsed.hostname:
            return parsed.hostname.lower().rstrip(".")
    return text.lower().rstrip(".")


def _target_from_argv(argv: Sequence[str]) -> str | None:
    for flag in ("-u", "-target"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                first = str(argv[idx + 1]).split(",", 1)[0]
                return _hostname_like(first)
    for flag in ("-l", "-list"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return Path(str(argv[idx + 1])).stem
    return None


def _probe_profile_from_argv(argv: Sequence[str]) -> str:
    flags = []
    for flag in (
        "-status-code",
        "-title",
        "-tech-detect",
        "-server",
        "-cdn",
        "-ip",
        "-include-chain",
        "-irh",
        "-body",
    ):
        if flag in argv:
            flags.append(flag.lstrip("-"))
    return ",".join(flags) if flags else DEFAULT_PROBE_PROFILE


def _host_input_count_from_argv(argv: Sequence[str]) -> int | None:
    for flag in ("-u", "-target"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return len([p for p in str(argv[idx + 1]).split(",") if p.strip()])
    for flag in ("-l", "-list"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                path = Path(str(argv[idx + 1]))
                if path.is_file():
                    lines = [
                        line.strip()
                        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
                        if line.strip() and not line.strip().startswith("#")
                    ]
                    return len(lines)
    return None


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
    probe_profile: str,
    host_input_count: int | None,
    subfinder_scenario: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    """Ensure a full httpx_probe_v1 bundle (JSONL stdout → bundle with scan meta)."""
    if isinstance(raw, dict):
        doc = dict(raw)
        if "records" not in doc:
            raise ValueError("structured dict requires records[]")
        doc.setdefault("schema", HTTPX_STRUCTURED_SCHEMA)
        if not doc.get("command") or doc.get("command") == "httpx":
            doc["command"] = command
        if target and not doc.get("target"):
            doc["target"] = target
        if not doc.get("probe_profile"):
            doc["probe_profile"] = probe_profile
        if host_input_count is not None and doc.get("host_input_count") is None:
            doc["host_input_count"] = host_input_count
        if subfinder_scenario and not doc.get("subfinder_scenario"):
            doc["subfinder_scenario"] = subfinder_scenario
        return doc

    text = str(raw).strip()
    if not text:
        return _bundle_with_scan(
            [],
            command=command,
            scenario_key=scenario_key,
            target=target,
            probe_profile=probe_profile,
            host_input_count=host_input_count or 0,
            subfinder_scenario=subfinder_scenario,
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
        maybe.setdefault("schema", HTTPX_STRUCTURED_SCHEMA)
        if not maybe.get("command") or maybe.get("command") == "httpx":
            maybe["command"] = command
        if target and not maybe.get("target"):
            maybe["target"] = target
        if not maybe.get("probe_profile"):
            maybe["probe_profile"] = probe_profile
        if host_input_count is not None and maybe.get("host_input_count") is None:
            maybe["host_input_count"] = host_input_count
        if subfinder_scenario and not maybe.get("subfinder_scenario"):
            maybe["subfinder_scenario"] = subfinder_scenario
        return maybe
    if isinstance(maybe, list):
        records = [row for row in maybe if isinstance(row, dict)]
        return _bundle_with_scan(
            records,
            command=command,
            scenario_key=scenario_key,
            target=target,
            probe_profile=probe_profile,
            host_input_count=host_input_count if host_input_count is not None else len(records),
            subfinder_scenario=subfinder_scenario,
            duration=duration,
            exit_code=exit_code,
            stderr=stderr,
            started_at=started_at,
        )

    records = parse_jsonl(text)
    return _bundle_with_scan(
        records,
        command=command,
        scenario_key=scenario_key,
        target=target,
        probe_profile=probe_profile,
        host_input_count=host_input_count if host_input_count is not None else len(records),
        subfinder_scenario=subfinder_scenario,
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
    probe_profile: str,
    host_input_count: int,
    subfinder_scenario: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    scan = httpx_scan_context(
        command=command,
        scenario_name=scenario_key,
        scenario_id=scenario_key,
        target=target,
        subfinder_scenario=subfinder_scenario,
        probe_profile=probe_profile,
        host_input_count=host_input_count,
        captured_at=started_at or datetime.now(timezone.utc),
        runtime="modules_v2",
        exit_code=exit_code,
        duration_s=duration,
        record_count=len(records),
        stderr_banner=stderr or None,
    )
    return build_httpx_bundle(records, scan)


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_httpx().run(scan_step_spec)


# End of sfp_cli_httpx
