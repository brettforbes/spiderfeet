# -*- coding: utf-8 -*-
"""v2 Katana CLI module — four-output Text / Structured / Graph / Narrative (R10-15)."""

from __future__ import annotations

import json
import os
import shutil
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
from modules_v2.adapters.katana import build_outputs
from modules_v2.adapters.katana.structured import (
    KATANA_STRUCTURED_SCHEMA,
    build_katana_bundle,
    katana_scan_context,
    parse_jsonl,
)

MODULE_ID = "sfp_cli_katana"
TOOL_NAME = "katana"

CONSUMED_INPUTS = [
    "DOMAIN_NAME",
    "INTERNET_NAME",
    "LINKED_URL_INTERNAL",
    "LINKED_URL_EXTERNAL",
]

PRODUCED_NUGGET_TYPES = [
    "DOMAIN_NAME",
    "HTTP_METHOD",
    "HTTP_STATUS_CODE",
    "LINKED_URL_INTERNAL",
    "SCAN_CLI",
    "SCAN_CRAWL_PROFILE",
    "SCAN_ELAPSED",
    "SCAN_EXIT_STATUS",
    "SCAN_RECORD",
    "SCAN_START",
    "SCAN_TARGET",
    "SCAN_TOOL",
    "SCAN_URL_INPUT_COUNT",
    "UPSTREAM_SCENARIO_ID",
]

# Structured-first: -jsonl is mandatory; bounded crawl for smoke.
DEFAULT_SMOKE_ARGS = [
    "-silent",
    "-jsonl",
    "-depth",
    "2",
    "-c",
    "5",
    "-timeout",
    "10",
    "-fs",
    "fqdn",
    "-ct",
    "30s",
]

DEFAULT_CRAWL_PROFILE = "depth-2,fqdn-scope,concurrency-5,timeout-10,crawl-duration-30s"


class sfp_cli_katana(CliModuleBase):
    """Katana v2 module: argv-only CLI → JSONL → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "json"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "Katana CLI App",
        "summary": "Run Katana and produce Text, Structured (JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Web crawling"],
        "dataSource": {
            "website": "https://github.com/projectdiscovery/katana",
            "license": "MIT",
            "repository": "https://github.com/projectdiscovery/katana",
            "references": ["https://docs.projectdiscovery.io/tools/katana"],
            "description": (
                "Katana crawls web targets for endpoints and assets, emitting "
                "structured JSONL crawl records for attack-surface mapping."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build katana argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``url`` / ``target`` / ``urls`` — ``-u`` value(s)
        - ``url_list`` / ``list`` — path for ``-list``
        - ``args`` — extra flags (list[str]); ``-jsonl`` injected if missing
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

            if not _has_jsonl_flag(tool_argv):
                tool_argv = ["-jsonl"] + list(tool_argv)
            if not _has_flag(tool_argv, "-silent"):
                tool_argv = list(tool_argv) + ["-silent"]

            url_list = scan_step_spec.get("url_list") or scan_step_spec.get("list")
            urls = _collect_urls(scan_step_spec)
            has_u = _has_flag(tool_argv, "-u") or _has_flag(tool_argv, "-url")
            has_list = _has_flag(tool_argv, "-list") or _has_flag(tool_argv, "-l")

            if url_list and not has_list:
                tool_argv = list(tool_argv) + ["-list", str(url_list)]
            elif urls and not has_u and not has_list:
                tool_argv = list(tool_argv) + ["-u", ",".join(urls)]
            elif not url_list and not urls and not has_u and not has_list:
                raise ValueError(
                    "scan_step_spec requires url/target/urls/url_list/list or argv"
                )

        prefix = scan_step_spec.get("executable_prefix")
        if prefix is not None:
            exe_prefix = ensure_no_shell_string(prefix)
        else:
            exe_prefix, err = _resolve_katana_executable()
            if err:
                raise FileNotFoundError(err)

        return ensure_no_shell_string(list(exe_prefix) + list(tool_argv))

    def run_from_structured(
        self,
        raw: str | dict[str, Any],
        *,
        command: Sequence[str] | None = None,
        scenario_key: str = "katana",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
        target: str | None = None,
        crawl_profile: str | None = None,
        url_input_count: int | None = None,
        httpx_scenario: str | None = None,
        started_at: datetime | None = None,
    ) -> dict[str, Any]:
        """Produce four outputs from a Katana bundle / JSONL capture (fixture / offline)."""
        cmd_list = list(command or ["katana", "-jsonl", "<fixture>"])
        cmd_str = " ".join(str(p) for p in cmd_list)
        profile = crawl_profile or _crawl_profile_from_argv(cmd_list) or DEFAULT_CRAWL_PROFILE
        doc = _normalize_capture(
            raw,
            command=cmd_str,
            scenario_key=scenario_key,
            target=target,
            crawl_profile=profile,
            url_input_count=url_input_count,
            httpx_scenario=httpx_scenario,
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
        """Live (or fixture) four-output katana run.

        Special keys:
        - ``structured`` / ``json_text`` — skip CLI; build four forms from bundle/JSONL
        - ``structured_path`` / ``json_path`` — load fixture from disk
        - ``timeout`` — seconds (default 90)
        - ``scenario_key`` — narrative scenario label
        - ``crawl_profile`` — scan metadata label (inferred from argv when omitted)
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "katana")
        target = _first_target(spec)
        crawl_profile = str(spec["crawl_profile"]) if spec.get("crawl_profile") else None
        url_input_count = spec.get("url_input_count")
        if url_input_count is None:
            urls = _collect_urls(spec)
            url_input_count = len(urls) if urls else None
        httpx_scenario = str(spec["httpx_scenario"]) if spec.get("httpx_scenario") else None

        if spec.get("structured") is not None:
            return self.run_from_structured(
                spec["structured"],
                command=spec.get("command") or ["katana", "-jsonl", "<structured>"],
                scenario_key=scenario_key,
                target=target,
                crawl_profile=crawl_profile,
                url_input_count=url_input_count,
                httpx_scenario=httpx_scenario,
            )
        if spec.get("json_text") is not None:
            return self.run_from_structured(
                str(spec["json_text"]),
                command=spec.get("command") or ["katana", "-jsonl", "<json_text>"],
                scenario_key=scenario_key,
                target=target,
                crawl_profile=crawl_profile,
                url_input_count=url_input_count,
                httpx_scenario=httpx_scenario,
            )
        path_key = spec.get("structured_path") or spec.get("json_path")
        if path_key:
            raw_text = Path(path_key).read_text(encoding="utf-8")
            return self.run_from_structured(
                raw_text,
                command=spec.get("command") or ["katana", "-jsonl", str(path_key)],
                scenario_key=scenario_key,
                target=target,
                crawl_profile=crawl_profile,
                url_input_count=url_input_count,
                httpx_scenario=httpx_scenario,
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
                error=f"katana exited {completed.returncode}",
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
                crawl_profile=crawl_profile or _crawl_profile_from_argv(argv),
                url_input_count=url_input_count or _url_input_count_from_argv(argv),
                httpx_scenario=httpx_scenario,
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
            result["error"] = f"katana exited {completed.returncode}"
        return result


def _has_flag(argv: Sequence[str], flag: str) -> bool:
    return flag in argv


def _has_jsonl_flag(argv: Sequence[str]) -> bool:
    return "-jsonl" in argv or "-j" in argv or "-json" in argv


def _repo_tools_katana() -> Path | None:
    root = Path(__file__).resolve().parents[1]
    for name in ("katana.exe", "katana"):
        candidate = root / ".tools" / "bin" / name
        if candidate.is_file():
            return candidate
    return None


def _resolve_katana_executable() -> tuple[list[str], str | None]:
    """Resolve ProjectDiscovery katana (repo tools, env, PATH, WSL)."""
    env_path = os.environ.get("SPIDERFEET_KATANA") or os.environ.get("KATANA_BIN")
    if env_path:
        return [env_path], None
    tools = _repo_tools_katana()
    if tools is not None:
        return [str(tools)], None
    native = shutil.which("katana")
    if native:
        return [native], None
    return resolve_executable(TOOL_NAME, prefer_wsl=True)


def _collect_urls(spec: Mapping[str, Any]) -> list[str]:
    urls: list[str] = []
    for key in ("urls",):
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
            text = str(value).strip()
            # Allow bare hostnames — normalize to https URL for katana -u.
            if "://" not in text and "/" not in text and "." in text:
                text = f"https://{text}"
            urls.append(text)
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
    url_list = spec.get("url_list") or spec.get("list")
    if url_list:
        return Path(str(url_list)).stem
    return None


def _hostname_like(value: str) -> str:
    text = value.strip()
    if "://" in text or "/" in text:
        parsed = urlparse(text if "://" in text else f"https://{text}")
        if parsed.hostname:
            return parsed.hostname.lower().rstrip(".")
    return text.lower().rstrip(".")


def _target_from_argv(argv: Sequence[str]) -> str | None:
    for flag in ("-u", "-url"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                first = str(argv[idx + 1]).split(",", 1)[0]
                return _hostname_like(first)
    for flag in ("-list", "-l"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return Path(str(argv[idx + 1])).stem
    return None


def _crawl_profile_from_argv(argv: Sequence[str]) -> str:
    parts: list[str] = []
    if "-depth" in argv:
        idx = list(argv).index("-depth")
        if idx + 1 < len(argv):
            parts.append(f"depth-{argv[idx + 1]}")
    if "-fs" in argv:
        idx = list(argv).index("-fs")
        if idx + 1 < len(argv):
            parts.append(f"{argv[idx + 1]}-scope")
    if "-c" in argv:
        idx = list(argv).index("-c")
        if idx + 1 < len(argv):
            parts.append(f"concurrency-{argv[idx + 1]}")
    if "-timeout" in argv:
        idx = list(argv).index("-timeout")
        if idx + 1 < len(argv):
            parts.append(f"timeout-{argv[idx + 1]}")
    if "-ct" in argv:
        idx = list(argv).index("-ct")
        if idx + 1 < len(argv):
            parts.append(f"crawl-duration-{argv[idx + 1]}")
    return ",".join(parts) if parts else DEFAULT_CRAWL_PROFILE


def _url_input_count_from_argv(argv: Sequence[str]) -> int | None:
    for flag in ("-u", "-url"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return len([p for p in str(argv[idx + 1]).split(",") if p.strip()])
    for flag in ("-list", "-l"):
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
    crawl_profile: str,
    url_input_count: int | None,
    httpx_scenario: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    """Ensure a full katana_crawl_v1 bundle (JSONL stdout → bundle with scan meta)."""
    if isinstance(raw, dict):
        doc = dict(raw)
        if "records" not in doc:
            raise ValueError("structured dict requires records[]")
        doc.setdefault("schema", KATANA_STRUCTURED_SCHEMA)
        if not doc.get("command") or doc.get("command") == "katana":
            doc["command"] = command
        if target and not doc.get("target"):
            doc["target"] = target
        if not doc.get("crawl_profile"):
            doc["crawl_profile"] = crawl_profile
        if url_input_count is not None and doc.get("url_input_count") is None:
            doc["url_input_count"] = url_input_count
        if httpx_scenario and not doc.get("httpx_scenario"):
            doc["httpx_scenario"] = httpx_scenario
        return doc

    text = str(raw).strip()
    if not text:
        return _bundle_with_scan(
            [],
            command=command,
            scenario_key=scenario_key,
            target=target,
            crawl_profile=crawl_profile,
            url_input_count=url_input_count or 0,
            httpx_scenario=httpx_scenario,
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
        maybe.setdefault("schema", KATANA_STRUCTURED_SCHEMA)
        if not maybe.get("command") or maybe.get("command") == "katana":
            maybe["command"] = command
        if target and not maybe.get("target"):
            maybe["target"] = target
        if not maybe.get("crawl_profile"):
            maybe["crawl_profile"] = crawl_profile
        if url_input_count is not None and maybe.get("url_input_count") is None:
            maybe["url_input_count"] = url_input_count
        if httpx_scenario and not maybe.get("httpx_scenario"):
            maybe["httpx_scenario"] = httpx_scenario
        return maybe
    if isinstance(maybe, list):
        records = [row for row in maybe if isinstance(row, dict)]
        return _bundle_with_scan(
            records,
            command=command,
            scenario_key=scenario_key,
            target=target,
            crawl_profile=crawl_profile,
            url_input_count=url_input_count if url_input_count is not None else len(records),
            httpx_scenario=httpx_scenario,
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
        crawl_profile=crawl_profile,
        url_input_count=url_input_count if url_input_count is not None else len(records),
        httpx_scenario=httpx_scenario,
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
    crawl_profile: str,
    url_input_count: int,
    httpx_scenario: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    scan = katana_scan_context(
        command=command,
        scenario_name=scenario_key,
        scenario_id=scenario_key,
        target=target,
        httpx_scenario=httpx_scenario,
        crawl_profile=crawl_profile,
        url_input_count=url_input_count,
        captured_at=started_at or datetime.now(timezone.utc),
        runtime="modules_v2",
        exit_code=exit_code,
        duration_s=duration,
        record_count=len(records),
        stderr_banner=stderr or None,
    )
    return build_katana_bundle(records, scan)


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_katana().run(scan_step_spec)


# End of sfp_cli_katana
