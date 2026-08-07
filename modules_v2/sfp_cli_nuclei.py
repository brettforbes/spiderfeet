# -*- coding: utf-8 -*-
"""v2 Nuclei CLI module — four-output Text / Structured / Graph / Narrative (R10-15)."""

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
from modules_v2.adapters.nuclei import build_outputs
from modules_v2.adapters.nuclei.structured import (
    NUCLEI_STRUCTURED_SCHEMA,
    build_nuclei_bundle,
    nuclei_scan_context,
    parse_jsonl,
)

MODULE_ID = "sfp_cli_nuclei"
TOOL_NAME = "nuclei"

CONSUMED_INPUTS = [
    "DOMAIN_NAME",
    "INTERNET_NAME",
    "IPV4_ADDRESS",
    "IPV6_ADDRESS",
    "LINKED_URL_INTERNAL",
    "LINKED_URL_EXTERNAL",
]

PRODUCED_NUGGET_TYPES = [
    "FINDINGS",
    "HOST",
    "NUCLEI_EXTRACTED_RESULTS",
    "NUCLEI_FINDING",
    "NUCLEI_FINDING_HOST",
    "NUCLEI_FINDING_IP",
    "NUCLEI_FINDING_PORT",
    "NUCLEI_FINDING_PROTOCOL",
    "NUCLEI_FINDING_TIMESTAMP",
    "NUCLEI_FINDING_URL",
    "NUCLEI_MATCHED_AT",
    "NUCLEI_MATCHER_NAME",
    "NUCLEI_MATCHER_STATUS",
    "NUCLEI_SEVERITY_CRITICAL",
    "NUCLEI_SEVERITY_HIGH",
    "NUCLEI_SEVERITY_INFO",
    "NUCLEI_SEVERITY_LOW",
    "NUCLEI_SEVERITY_MEDIUM",
    "NUCLEI_TEMPLATE",
    "NUCLEI_TEMPLATE_AUTHOR",
    "NUCLEI_TEMPLATE_ID",
    "NUCLEI_TEMPLATE_NAME",
    "NUCLEI_TEMPLATE_PATH",
    "NUCLEI_TEMPLATE_PROTOCOL",
    "NUCLEI_TEMPLATE_TAGS",
    "NUCLEI_VULNERABILITY",
    "NUCLEI_VULN_CPE",
    "NUCLEI_VULN_CVSS_METRICS",
    "NUCLEI_VULN_CVSS_SCORE",
    "NUCLEI_VULN_CWE",
    "NUCLEI_VULN_DESCRIPTION",
    "NUCLEI_VULN_EPSS_PERCENTILE",
    "NUCLEI_VULN_EPSS_SCORE",
    "NUCLEI_VULN_IMPACT",
    "NUCLEI_VULN_PRODUCT",
    "NUCLEI_VULN_REMEDIATION",
    "NUCLEI_VULN_SEVERITY",
    "NUCLEI_VULN_TAGS",
    "NUCLEI_VULN_VENDOR",
    "SCAN_CLI",
    "SCAN_ELAPSED",
    "SCAN_EXIT_STATUS",
    "SCAN_FINDING_COUNT",
    "SCAN_RECORD",
    "SCAN_START",
    "SCAN_TARGET",
    "SCAN_TOOL",
    "SECURITY",
    "SERVICE",
    "TEMPLATES_USED",
    "VULNERABILITY_CVE_CRITICAL",
    "VULNERABILITY_CVE_HIGH",
    "VULNERABILITY_CVE_LOW",
    "VULNERABILITY_CVE_MEDIUM",
    "VULNERABILITY_GENERAL",
]

# Structured-first tech fingerprint smoke (nuclei_strategy Phase A).
DEFAULT_SMOKE_ARGS = [
    "-silent",
    "-jsonl",
    "-no-interactsh",
    "-etags",
    "dos,fuzz,misc",
    "-duc",
    "-retries",
    "1",
    "-tags",
    "tech",
    "-severity",
    "info",
    "-c",
    "25",
    "-timeout",
    "10",
]


class sfp_cli_nuclei(CliModuleBase):
    """Nuclei v2 module: argv-only CLI → JSONL → four outputs via adapters + _core."""

    module_id = MODULE_ID
    tool_name = TOOL_NAME
    structured_type = "json"
    consumed_inputs = list(CONSUMED_INPUTS)
    produced_nugget_types = list(PRODUCED_NUGGET_TYPES)

    meta = {
        "name": "Nuclei CLI App",
        "summary": "Run Nuclei and produce Text, Structured (JSON), Graph, and Narrative.",
        "types": ["cli"],
        "useCases": ["Footprint", "Investigate"],
        "categories": ["Vulnerability scanning"],
        "dataSource": {
            "website": "https://github.com/projectdiscovery/nuclei",
            "license": "MIT",
            "repository": "https://github.com/projectdiscovery/nuclei",
            "references": ["https://docs.projectdiscovery.io/tools/nuclei"],
            "description": (
                "Nuclei runs template-driven vulnerability and technology checks "
                "and emits structured JSONL findings."
            ),
        },
    }

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        """Build nuclei argv from a scan-step spec (never a shell string).

        Accepted keys:
        - ``url`` / ``target`` / ``urls`` / ``hosts`` — ``-u`` value(s)
        - ``host_list`` — path for ``-l``
        - ``templates`` / ``template_path`` — ``-t`` value
        - ``tags`` / ``severity`` — optional template filters
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
            if not _has_flag(tool_argv, "-no-interactsh"):
                tool_argv = list(tool_argv) + ["-no-interactsh"]
            if not _has_flag(tool_argv, "-duc"):
                tool_argv = list(tool_argv) + ["-duc"]
            if not _has_flag(tool_argv, "-etags"):
                tool_argv = list(tool_argv) + ["-etags", "dos,fuzz,misc"]

            tags = scan_step_spec.get("tags")
            if tags and not _has_flag(tool_argv, "-tags"):
                tool_argv = list(tool_argv) + ["-tags", str(tags)]

            severity = scan_step_spec.get("severity")
            if severity and not _has_flag(tool_argv, "-severity"):
                # Nuclei accepts repeated -severity; also accept comma-joined.
                parts = [p.strip() for p in str(severity).split(",") if p.strip()]
                for part in parts:
                    tool_argv = list(tool_argv) + ["-severity", part]

            templates = (
                scan_step_spec.get("templates")
                or scan_step_spec.get("template_path")
                or _default_templates_path()
            )
            if templates and not _has_flag(tool_argv, "-t") and not _has_flag(tool_argv, "-templates"):
                tool_argv = list(tool_argv) + ["-t", str(templates)]

            host_list = scan_step_spec.get("host_list")
            urls = _collect_urls(scan_step_spec)
            has_u = _has_flag(tool_argv, "-u") or _has_flag(tool_argv, "-target")
            has_l = _has_flag(tool_argv, "-l") or _has_flag(tool_argv, "-list")

            if host_list and not has_l:
                tool_argv = list(tool_argv) + ["-l", str(host_list)]
            elif urls and not has_u and not has_l:
                # Nuclei accepts repeated -u; join with comma for single -u when one value.
                if len(urls) == 1:
                    tool_argv = list(tool_argv) + ["-u", urls[0]]
                else:
                    for url in urls:
                        tool_argv = list(tool_argv) + ["-u", url]
            elif not host_list and not urls and not has_u and not has_l:
                raise ValueError(
                    "scan_step_spec requires url/target/urls/hosts/host_list or argv"
                )

        prefix = scan_step_spec.get("executable_prefix")
        if prefix is not None:
            exe_prefix = ensure_no_shell_string(prefix)
        else:
            exe_prefix, err = _resolve_nuclei_executable()
            if err:
                raise FileNotFoundError(err)

        return ensure_no_shell_string(list(exe_prefix) + list(tool_argv))

    def run_from_structured(
        self,
        raw: str | dict[str, Any],
        *,
        command: Sequence[str] | None = None,
        scenario_key: str = "nuclei",
        duration: float = 0.0,
        exit_code: int = 0,
        stderr: str = "",
        target: str | None = None,
        tags: str | None = None,
        severity: str | None = None,
        started_at: datetime | None = None,
    ) -> dict[str, Any]:
        """Produce four outputs from a Nuclei bundle / JSONL capture (fixture / offline)."""
        cmd_list = list(command or ["nuclei", "-jsonl", "<fixture>"])
        cmd_str = " ".join(str(p) for p in cmd_list)
        doc = _normalize_capture(
            raw,
            command=cmd_str,
            scenario_key=scenario_key,
            target=target,
            tags=tags or _tags_from_argv(cmd_list),
            severity=severity or _severity_from_argv(cmd_list),
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
        """Live (or fixture) four-output nuclei run.

        Special keys:
        - ``structured`` / ``json_text`` — skip CLI; build four forms from bundle/JSONL
        - ``structured_path`` / ``json_path`` — load fixture from disk
        - ``timeout`` — seconds (default 180)
        - ``scenario_key`` — narrative scenario label
        - ``tags`` / ``severity`` — template filters (also inferred from argv)
        """
        spec = self._merge_spec(scan_step_spec)
        scenario_key = str(spec.get("scenario_key") or "nuclei")
        target = _first_target(spec)
        tags = str(spec["tags"]) if spec.get("tags") else None
        severity = str(spec["severity"]) if spec.get("severity") else None

        if spec.get("structured") is not None:
            return self.run_from_structured(
                spec["structured"],
                command=spec.get("command") or ["nuclei", "-jsonl", "<structured>"],
                scenario_key=scenario_key,
                target=target,
                tags=tags,
                severity=severity,
            )
        if spec.get("json_text") is not None:
            return self.run_from_structured(
                str(spec["json_text"]),
                command=spec.get("command") or ["nuclei", "-jsonl", "<json_text>"],
                scenario_key=scenario_key,
                target=target,
                tags=tags,
                severity=severity,
            )
        path_key = spec.get("structured_path") or spec.get("json_path")
        if path_key:
            raw_text = Path(path_key).read_text(encoding="utf-8")
            return self.run_from_structured(
                raw_text,
                command=spec.get("command") or ["nuclei", "-jsonl", str(path_key)],
                scenario_key=scenario_key,
                target=target,
                tags=tags,
                severity=severity,
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
        out_path = _output_file_from_argv(argv)
        if out_path and Path(out_path).is_file():
            file_body = Path(out_path).read_text(encoding="utf-8", errors="replace")
            if file_body.strip():
                raw_out = file_body

        if completed.returncode != 0 and not raw_out.strip():
            return error_result(
                command=argv,
                status=STATUS_ERROR,
                error=f"nuclei exited {completed.returncode}",
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
                tags=tags or _tags_from_argv(argv),
                severity=severity or _severity_from_argv(argv),
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
            result["error"] = f"nuclei exited {completed.returncode}"
        return result


def _has_flag(argv: Sequence[str], flag: str) -> bool:
    return flag in argv


def _has_jsonl_flag(argv: Sequence[str]) -> bool:
    return "-jsonl" in argv or "-json-l" in argv or "-j" in argv


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _repo_tools_nuclei() -> Path | None:
    root = _repo_root()
    for name in ("nuclei.exe", "nuclei"):
        candidate = root / ".tools" / "bin" / name
        if candidate.is_file():
            return candidate
    return None


def _default_templates_path() -> str | None:
    env = os.environ.get("SPIDERFEET_NUCLEI_TEMPLATES") or os.environ.get("NUCLEI_TEMPLATES")
    if env and Path(env).exists():
        return env
    candidate = _repo_root() / ".tools" / "nuclei-templates"
    if candidate.is_dir():
        return str(candidate)
    return None


def _resolve_nuclei_executable() -> tuple[list[str], str | None]:
    env_path = os.environ.get("SPIDERFEET_NUCLEI") or os.environ.get("NUCLEI_BIN")
    if env_path:
        return [env_path], None
    tools = _repo_tools_nuclei()
    if tools is not None:
        return [str(tools)], None
    native = shutil.which("nuclei")
    if native:
        return [native], None
    prefix, err = resolve_executable(TOOL_NAME, prefer_wsl=True)
    if prefix:
        return list(prefix), None
    return [], err or "nuclei executable not found (SPIDERFEET_NUCLEI / .tools/bin / PATH / WSL)"


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
    # Preserve host:port labels used by nuclei network scans.
    if "://" not in text and "/" not in text and text.count(":") == 1:
        host, port = text.rsplit(":", 1)
        if port.isdigit():
            return f"{host.lower().rstrip('.')}:{port}"
    if "://" in text or "/" in text:
        parsed = urlparse(text if "://" in text else f"https://{text}")
        if parsed.hostname:
            if parsed.port:
                return f"{parsed.hostname.lower().rstrip('.')}:{parsed.port}"
            return parsed.hostname.lower().rstrip(".")
    return text.lower().rstrip(".")


def _target_from_argv(argv: Sequence[str]) -> str | None:
    for flag in ("-u", "-target"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return _hostname_like(str(argv[idx + 1]))
    for flag in ("-l", "-list"):
        if flag in argv:
            idx = list(argv).index(flag)
            if idx + 1 < len(argv):
                return Path(str(argv[idx + 1])).stem
    return None


def _flag_values(argv: Sequence[str], flag: str) -> list[str]:
    values: list[str] = []
    items = list(argv)
    i = 0
    while i < len(items):
        if items[i] == flag and i + 1 < len(items):
            values.append(str(items[i + 1]))
            i += 2
            continue
        i += 1
    return values


def _tags_from_argv(argv: Sequence[str]) -> str | None:
    values = _flag_values(argv, "-tags")
    return ",".join(values) if values else None


def _severity_from_argv(argv: Sequence[str]) -> str | None:
    values = _flag_values(argv, "-severity")
    return ",".join(values) if values else None


def _output_file_from_argv(argv: Sequence[str]) -> str | None:
    for flag in ("-jle", "-jsonl-export", "-o", "-output"):
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
    tags: str | None,
    severity: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    """Ensure a full nuclei_finding_v1 bundle (JSONL stdout → bundle with scan meta)."""
    if isinstance(raw, dict):
        doc = dict(raw)
        if "records" not in doc:
            raise ValueError("structured dict requires records[]")
        doc.setdefault("schema", NUCLEI_STRUCTURED_SCHEMA)
        if not doc.get("command") or doc.get("command") == "nuclei":
            doc["command"] = command
        if target and not doc.get("target"):
            doc["target"] = target
        if tags and not doc.get("tags"):
            doc["tags"] = tags
        if severity and not doc.get("severity"):
            doc["severity"] = severity
        return doc

    text = str(raw).strip()
    if not text:
        return _bundle_with_scan(
            [],
            command=command,
            scenario_key=scenario_key,
            target=target,
            tags=tags,
            severity=severity,
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
        maybe.setdefault("schema", NUCLEI_STRUCTURED_SCHEMA)
        if not maybe.get("command") or maybe.get("command") == "nuclei":
            maybe["command"] = command
        if target and not maybe.get("target"):
            maybe["target"] = target
        if tags and not maybe.get("tags"):
            maybe["tags"] = tags
        if severity and not maybe.get("severity"):
            maybe["severity"] = severity
        return maybe
    if isinstance(maybe, list):
        records = [row for row in maybe if isinstance(row, dict)]
        return _bundle_with_scan(
            records,
            command=command,
            scenario_key=scenario_key,
            target=target,
            tags=tags,
            severity=severity,
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
        tags=tags,
        severity=severity,
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
    tags: str | None,
    severity: str | None,
    duration: float,
    exit_code: int,
    stderr: str,
    started_at: datetime | None,
) -> dict[str, Any]:
    scan = nuclei_scan_context(
        command=command,
        scenario_name=scenario_key,
        scenario_id=scenario_key,
        target=target,
        captured_at=started_at or datetime.now(timezone.utc),
        runtime="modules_v2",
        exit_code=exit_code,
        duration_s=duration,
        record_count=len(records),
        stderr_banner=stderr or None,
        tags=tags,
        severity=severity,
    )
    return build_nuclei_bundle(records, scan)


def run(scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Module-level entrypoint matching the R10-14 ``run()`` contract."""
    return sfp_cli_nuclei().run(scan_step_spec)


# End of sfp_cli_nuclei
