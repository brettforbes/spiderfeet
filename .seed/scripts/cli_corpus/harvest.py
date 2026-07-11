#!/usr/bin/env python3
"""Run CLI app examination scenarios and write evidence bundles.

Evidence layout per .seed/04_Driving and Integrating_CLI_Apps.md section 2.1.2.D.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

from netdiscover_text_to_json import (
    assert_no_truncation,
    output_mode_for_scenario,
    text_capture_header,
    verify_text_structured_alignment,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
CORPUS_DIR = Path(__file__).resolve().parent
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))
MANIFESTS_DIR = CORPUS_DIR / "manifests"
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
ADAPTER_TOOLS = frozenset({"netdiscover", "nmap"})


@dataclass
class RunResult:
    command: str
    runtime: str
    exit_code: int
    duration_s: float
    stdout: str
    stderr: str
    structured_path: str | None = None
    structured_kind: str | None = None
    structured_fixture_used: str | None = None


def ensure_dev_paths() -> None:
    prefixes: list[str] = []
    tools_bin = REPO_ROOT / ".tools" / "bin"
    if tools_bin.is_dir():
        prefixes.append(str(tools_bin))
    if sys.platform == "win32":
        for candidate in (
            r"C:\Program Files (x86)\Nmap",
            r"C:\Program Files\Nmap",
            r"C:\cli_apps",
        ):
            if os.path.isdir(candidate):
                prefixes.append(candidate)
    current = os.environ.get("PATH", "")
    merged = os.pathsep.join(p for p in prefixes if p and p not in current.split(os.pathsep))
    if merged:
        os.environ["PATH"] = merged + os.pathsep + current


def load_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.is_file():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def _bash_env_prefix(env: dict[str, str]) -> str:
    if not env:
        return ""
    parts = [f'export {k}="{v.replace(chr(34), chr(92)+chr(34))}"' for k, v in env.items()]
    return " && ".join(parts) + " && "


def isolate_text_capture_command(command: str, runtime: str, tool: str) -> str:
    """Clear the terminal before text-only CLI captures so output is never mixed."""
    if tool != "netdiscover":
        return command
    if runtime == "windows-lan":
        return f"Clear-Host; {command}"
    if runtime in ("wsl", "wsl-root"):
        return f"clear; {command}"
    if sys.platform == "win32":
        return f"cls; {command}"
    return f"clear; {command}"


def run_command(
    command: str,
    runtime: str,
    cwd: Path | None,
    timeout: int,
    env: dict[str, str] | None = None,
) -> RunResult:
    started = time.monotonic()
    env = env or {}
    if runtime in ("wsl", "wsl-root"):
        inner = command
        if cwd:
            inner = f"cd {cwd} && {command}"
        inner = _bash_env_prefix(env) + inner
        wsl_args = ["wsl", "bash", "-lc", inner]
        if runtime == "wsl-root":
            wsl_args = ["wsl", "-u", "root", "bash", "-lc", inner]
        shell_cmd = wsl_args
        use_shell = False
        run_cwd = None
        proc_env = None
    elif runtime == "windows-lan":
        shell_cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            command,
        ]
        use_shell = False
        run_cwd = str(cwd) if cwd else str(REPO_ROOT)
        proc_env = {**os.environ, **env} if env else None
    else:
        shell_cmd = command if sys.platform == "win32" else command
        use_shell = sys.platform == "win32"
        run_cwd = str(cwd) if cwd else None
        proc_env = {**os.environ, **env} if env else None
    try:
        proc = subprocess.run(
            shell_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=run_cwd,
            timeout=timeout,
            shell=use_shell,
            env=proc_env,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired as exc:
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/IM", "katana.exe"],
                capture_output=True,
                timeout=15,
            )
        partial_out = exc.output
        if isinstance(partial_out, tuple):
            stdout_text = (partial_out[0] or "") if partial_out[0] else ""
            stderr_text = (partial_out[1] or "") if len(partial_out) > 1 and partial_out[1] else ""
        else:
            stdout_text = partial_out or ""
            stderr_text = ""
        duration = time.monotonic() - started
        return RunResult(
            command=command,
            runtime=runtime,
            exit_code=124,
            duration_s=round(duration, 3),
            stdout=stdout_text,
            stderr=(stderr_text + "\n[harvest] command timed out").strip(),
        )
    duration = time.monotonic() - started
    return RunResult(
        command=command,
        runtime=runtime,
        exit_code=proc.returncode,
        duration_s=round(duration, 3),
        stdout=proc.stdout or "",
        stderr=proc.stderr or "",
    )


def load_manifest(tool: str) -> dict[str, Any]:
    path = MANIFESTS_DIR / f"{tool}.yaml"
    if not path.is_file():
        raise SystemExit(f"Manifest not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def next_exam_id(tool_dir: Path) -> int:
    existing = []
    for p in tool_dir.glob("*_manifest.json"):
        try:
            existing.append(int(p.name.split("_", 1)[0]))
        except ValueError:
            continue
    return max(existing, default=0) + 1


def exam_id_for_scenario(manifest_meta: dict[str, Any], scenario_id: str, tool_dir: Path) -> int:
    for idx, scenario in enumerate(manifest_meta.get("scenarios", []), start=1):
        if scenario.get("id") == scenario_id:
            return idx
    return next_exam_id(tool_dir)


def remove_exam_bundle(tool_dir: Path, exam_id: int) -> None:
    prefix = f"{exam_id}_"
    for path in tool_dir.glob(f"{prefix}*"):
        if path.is_file():
            path.unlink()


def _import_adapter(tool: str):
    import importlib

    return importlib.import_module(f"adapters.{tool}")


def _nmap_xml_payload(text_content: str, scenario: dict[str, Any]) -> str:
    out_file = scenario.get("structured_output_file")
    if out_file and Path(out_file).is_file():
        return Path(out_file).read_text(encoding="utf-8", errors="replace")
    return text_content


def _write_adapter_four_outputs(
    tool: str,
    scenario: dict[str, Any],
    *,
    raw_input: str,
    captured_at: datetime,
    result: RunResult,
    prefix: str,
    tool_dir: Path,
) -> tuple[Path, str, Path, Path]:
    """Build and persist Text/Structured/Graph/Markdown via adapters.<tool>."""
    adapter = _import_adapter(tool)
    scenario_key = scenario["id"]
    scenario_name = scenario.get("name", scenario_key)

    if tool == "netdiscover":
        mode = output_mode_for_scenario(scenario, result.command)
        start_time = captured_at - timedelta(seconds=result.duration_s)
        outputs = adapter.build_outputs(
            raw_input,
            scenario_name=scenario_name,
            scenario_key=scenario_key,
            output_mode=mode,
            start_time=start_time,
            duration_s=result.duration_s,
            exit_code=result.exit_code,
        )
        alignment = verify_text_structured_alignment(
            raw_input,
            outputs["structured"],
            output_mode=mode,
        )
        if alignment:
            raise SystemExit(
                f"netdiscover structured/text mismatch for {scenario_key}: {alignment}"
            )
        header = text_capture_header(
            command=result.command,
            scenario_name=scenario_name,
            captured_at=captured_at,
        )
        text_content = header + outputs["text"]
    elif tool == "nmap":
        outputs = adapter.build_outputs(raw_input, scenario_key=scenario_key)
        text_content = outputs["text"]
    else:
        raise ValueError(f"unsupported adapter tool: {tool}")

    structured_path = tool_dir / f"{prefix}_output_structured.json"
    structured_path.write_text(outputs["structured_json"], encoding="utf-8")

    graph_path = NUGGET_ROOT / f"{tool}_{scenario_key}_proposed_nuggets_edges.json"
    markdown_path = NUGGET_ROOT / f"{tool}_{scenario_key}_proposed_nuggets_edges_description.md"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(outputs["graph"], indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(outputs["markdown_report"], encoding="utf-8")
    return structured_path, text_content, graph_path, markdown_path


def _jsonl_lines_from_stdout(stdout: str) -> str:
    lines = [ln for ln in stdout.splitlines() if ln.strip().startswith("{")]
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def _nerva_structured_payload(
    scenario: dict[str, Any],
    result: RunResult,
    captured_at: datetime,
) -> tuple[dict[str, Any], str]:
    from nerva_structured import build_nerva_bundle, nerva_scan_context, parse_jsonl, structured_to_text

    jsonl = _jsonl_lines_from_stdout(result.stdout)
    records = parse_jsonl(jsonl)
    scan = nerva_scan_context(
        command=result.command,
        scenario_name=scenario.get("name", scenario["id"]),
        scenario_id=scenario["id"],
        target=scenario.get("target"),
        captured_at=captured_at,
        runtime=result.runtime,
        exit_code=result.exit_code,
        duration_s=result.duration_s,
        record_count=len(records),
    )
    bundle = build_nerva_bundle(records, scan)
    text_content = structured_to_text(bundle["records"])
    return bundle, text_content


def _pius_ndjson_payload(result: RunResult, scenario: dict[str, Any]) -> str:
    payload = _jsonl_lines_from_stdout(result.stdout)
    fixture_rel = scenario.get("structured_fixture")
    if not payload.strip() and fixture_rel:
        fixture_path = REPO_ROOT / fixture_rel
        if fixture_path.is_file():
            payload = fixture_path.read_text(encoding="utf-8", errors="replace")
            result.structured_fixture_used = str(fixture_path.relative_to(REPO_ROOT))
    return payload


def _pius_structured_payload(
    scenario: dict[str, Any],
    result: RunResult,
    captured_at: datetime,
) -> tuple[dict[str, Any], str]:
    from pius_structured import (
        build_pius_bundle,
        parse_ndjson,
        pius_scan_context,
        structured_to_text,
    )

    ndjson = _pius_ndjson_payload(result, scenario)
    records = parse_ndjson(ndjson)
    stderr_banner = result.stderr.strip() or None
    scan = pius_scan_context(
        command=result.command,
        scenario_name=scenario.get("name", scenario["id"]),
        scenario_id=scenario["id"],
        org=scenario.get("org"),
        target=scenario.get("target"),
        captured_at=captured_at,
        runtime=result.runtime,
        exit_code=result.exit_code,
        duration_s=result.duration_s,
        record_count=len(records),
        stderr_banner=stderr_banner,
    )
    bundle = build_pius_bundle(records, scan)
    text_content = structured_to_text(bundle["records"])
    return bundle, text_content


def _nuclei_ndjson_payload(result: RunResult, scenario: dict[str, Any]) -> str:
    export_rel = scenario.get("jsonl_export")
    if export_rel:
        export_path = REPO_ROOT / export_rel
        if export_path.is_file():
            payload = export_path.read_text(encoding="utf-8", errors="replace")
            result.structured_fixture_used = str(export_path.relative_to(REPO_ROOT))
            return payload
    payload = _jsonl_lines_from_stdout(result.stdout)
    fixture_rel = scenario.get("structured_fixture")
    if not payload.strip() and fixture_rel:
        fixture_path = REPO_ROOT / fixture_rel
        if fixture_path.is_file():
            payload = fixture_path.read_text(encoding="utf-8", errors="replace")
            result.structured_fixture_used = str(fixture_path.relative_to(REPO_ROOT))
    return payload


def _subfinder_jsonl_payload(result: RunResult, scenario: dict[str, Any]) -> str:
    export_rel = scenario.get("jsonl_export")
    if export_rel:
        export_path = REPO_ROOT / export_rel
        if export_path.is_file():
            payload = export_path.read_text(encoding="utf-8", errors="replace")
            result.structured_fixture_used = str(export_path.relative_to(REPO_ROOT))
            return payload
    return _jsonl_lines_from_stdout(result.stdout)


def _subfinder_structured_payload(
    scenario: dict[str, Any],
    result: RunResult,
    captured_at: datetime,
) -> tuple[dict[str, Any], str]:
    from subfinder_structured import (
        build_subfinder_bundle,
        normalize_record,
        parse_jsonl,
        structured_to_text,
        subfinder_scan_context,
    )

    jsonl = _subfinder_jsonl_payload(result, scenario)
    mode = scenario.get("enumeration_mode", "passive")
    records = [normalize_record(rec, mode=mode) for rec in parse_jsonl(jsonl)]
    stderr_banner = result.stderr.strip() or None
    scan = subfinder_scan_context(
        command=result.command,
        scenario_name=scenario.get("name", scenario["id"]),
        scenario_id=scenario["id"],
        target=scenario.get("target"),
        enumeration_mode=mode,
        captured_at=captured_at,
        runtime=result.runtime,
        exit_code=result.exit_code,
        duration_s=result.duration_s,
        record_count=len(records),
        stderr_banner=stderr_banner,
    )
    bundle = build_subfinder_bundle(records, scan)
    text_content = structured_to_text(bundle["records"])
    return bundle, text_content


def _httpx_jsonl_payload(result: RunResult, scenario: dict[str, Any]) -> str:
    export_rel = scenario.get("jsonl_export")
    if export_rel:
        export_path = REPO_ROOT / export_rel
        if export_path.is_file():
            payload = export_path.read_text(encoding="utf-8", errors="replace")
            result.structured_fixture_used = str(export_path.relative_to(REPO_ROOT))
            return payload
    return _jsonl_lines_from_stdout(result.stdout)


def _host_input_count(scenario: dict[str, Any]) -> int:
    host_rel = scenario.get("host_list")
    if not host_rel:
        return 0
    host_path = REPO_ROOT / host_rel
    if not host_path.is_file():
        return 0
    return sum(1 for ln in host_path.read_text(encoding="utf-8").splitlines() if ln.strip())


def _url_input_count(scenario: dict[str, Any]) -> int:
    url_rel = scenario.get("url_list")
    if not url_rel:
        return 0
    url_path = REPO_ROOT / url_rel
    if not url_path.is_file():
        return 0
    return sum(1 for ln in url_path.read_text(encoding="utf-8").splitlines() if ln.strip())


def _httpx_structured_payload(
    scenario: dict[str, Any],
    result: RunResult,
    captured_at: datetime,
) -> tuple[dict[str, Any], str]:
    from httpx_structured import (
        build_httpx_bundle,
        httpx_scan_context,
        parse_jsonl,
        structured_to_text,
    )

    jsonl = _httpx_jsonl_payload(result, scenario)
    records = parse_jsonl(jsonl)
    stderr_banner = result.stderr.strip() or None
    scan = httpx_scan_context(
        command=result.command,
        scenario_name=scenario.get("name", scenario["id"]),
        scenario_id=scenario["id"],
        target=scenario.get("target"),
        subfinder_scenario=scenario.get("subfinder_scenario"),
        probe_profile=scenario.get("probe_profile", ""),
        host_input_count=_host_input_count(scenario),
        captured_at=captured_at,
        runtime=result.runtime,
        exit_code=result.exit_code,
        duration_s=result.duration_s,
        record_count=len(records),
        stderr_banner=stderr_banner,
    )
    bundle = build_httpx_bundle(records, scan)
    text_content = structured_to_text(bundle["records"])
    return bundle, text_content


def _katana_jsonl_payload(result: RunResult, scenario: dict[str, Any]) -> str:
    export_rel = scenario.get("jsonl_export")
    if export_rel:
        export_path = REPO_ROOT / export_rel
        if export_path.is_file():
            payload = export_path.read_text(encoding="utf-8", errors="replace")
            result.structured_fixture_used = str(export_path.relative_to(REPO_ROOT))
            return payload
    return _jsonl_lines_from_stdout(result.stdout)


def _katana_structured_payload(
    scenario: dict[str, Any],
    result: RunResult,
    captured_at: datetime,
) -> tuple[dict[str, Any], str]:
    from katana_structured import (
        build_katana_bundle,
        katana_scan_context,
        parse_jsonl,
        structured_to_text,
    )

    jsonl = _katana_jsonl_payload(result, scenario)
    records = parse_jsonl(jsonl)
    stderr_banner = result.stderr.strip() or None
    scan = katana_scan_context(
        command=result.command,
        scenario_name=scenario.get("name", scenario["id"]),
        scenario_id=scenario["id"],
        target=scenario.get("target"),
        httpx_scenario=scenario.get("httpx_scenario"),
        crawl_profile=scenario.get("crawl_profile", ""),
        url_input_count=_url_input_count(scenario),
        captured_at=captured_at,
        runtime=result.runtime,
        exit_code=result.exit_code,
        duration_s=result.duration_s,
        record_count=len(records),
        stderr_banner=stderr_banner,
    )
    bundle = build_katana_bundle(records, scan)
    text_content = structured_to_text(bundle["records"])
    return bundle, text_content


def _nuclei_structured_payload(
    scenario: dict[str, Any],
    result: RunResult,
    captured_at: datetime,
) -> tuple[dict[str, Any], str]:
    from nuclei_structured import (
        build_nuclei_bundle,
        parse_ndjson,
        nuclei_scan_context,
        structured_to_text,
    )

    ndjson = _nuclei_ndjson_payload(result, scenario)
    records = parse_ndjson(ndjson)
    stderr_banner = result.stderr.strip() or None
    scan = nuclei_scan_context(
        command=result.command,
        scenario_name=scenario.get("name", scenario["id"]),
        scenario_id=scenario["id"],
        target=scenario.get("target"),
        captured_at=captured_at,
        runtime=result.runtime,
        exit_code=result.exit_code,
        duration_s=result.duration_s,
        record_count=len(records),
        stderr_banner=stderr_banner,
    )
    bundle = build_nuclei_bundle(records, scan)
    text_content = structured_to_text(bundle["records"])
    return bundle, text_content


def _write_tool_graph(
    tool: str,
    scenario: dict[str, Any],
    structured_path: Path | None,
    command: str,
) -> None:
    if tool in ADAPTER_TOOLS:
        return
    if tool not in ("nerva", "pius", "subfinder", "httpx", "katana") or structured_path is None or not structured_path.is_file():
        return
    raw = structured_path.read_text(encoding="utf-8", errors="replace")
    if not raw.strip() and tool in ("nerva", "subfinder", "httpx", "katana"):
        graph = {"nodes": [], "edges": []}
    elif not raw.strip():
        return
    else:
        from cli_tool_to_graph import nerva_to_graph, pius_to_graph
        from httpx_json_to_graph import httpx_to_graph
        from katana_json_to_graph import katana_to_graph
        from subfinder_json_to_graph import subfinder_to_graph

        target = scenario.get("target") or scenario["id"]
        if tool == "nerva":
            graph = nerva_to_graph(raw, target, command)
        elif tool == "subfinder":
            graph = subfinder_to_graph(raw, target, command)
        elif tool == "httpx":
            graph = httpx_to_graph(raw, target, command)
        elif tool == "katana":
            graph = katana_to_graph(raw, target, command)
        else:
            org = scenario.get("org") or target
            graph = pius_to_graph(raw, org, command)
    graph_path = NUGGET_ROOT / f"{tool}_{scenario['id']}_proposed_nuggets_edges.json"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")


def write_bundle(
    tool: str,
    scenario: dict[str, Any],
    result: RunResult,
    manifest_meta: dict[str, Any],
    captured_at: datetime | None = None,
) -> Path:
    tool_dir = EXAM_ROOT / tool
    tool_dir.mkdir(parents=True, exist_ok=True)
    exam_id = exam_id_for_scenario(manifest_meta, scenario["id"], tool_dir)
    remove_exam_bundle(tool_dir, exam_id)
    prefix = f"{exam_id}"
    captured_at = captured_at or datetime.now(timezone.utc)

    structured_kind = scenario.get("structured_kind")
    structured_ext = scenario.get("structured_ext")
    structured_path: Path | None = None

    text_content = result.stderr if scenario.get("text_from") == "stderr" else result.stdout
    if scenario.get("text_output_file") and Path(scenario["text_output_file"]).is_file():
        text_content = Path(scenario["text_output_file"]).read_text(encoding="utf-8", errors="replace")

    adapter_text_content: str | None = None
    adapter_graph_path: Path | None = None
    adapter_markdown_path: Path | None = None

    if tool == "netdiscover" and structured_ext:
        structured_path, adapter_text_content, adapter_graph_path, adapter_markdown_path = _write_adapter_four_outputs(
            tool,
            scenario,
            raw_input=text_content,
            captured_at=captured_at,
            result=result,
            prefix=prefix,
            tool_dir=tool_dir,
        )
        result.structured_path = str(structured_path.relative_to(REPO_ROOT))
        result.structured_kind = "json"
        structured_kind = "json"
        structured_ext = "json"
    elif tool == "nmap" and structured_ext == "xml":
        raw_xml = _nmap_xml_payload(text_content, scenario)
        if not raw_xml.strip():
            raise SystemExit(f"nmap XML scenario {scenario['id']} produced empty structured output")
        structured_path, adapter_text_content, adapter_graph_path, adapter_markdown_path = _write_adapter_four_outputs(
            tool,
            scenario,
            raw_input=raw_xml,
            captured_at=captured_at,
            result=result,
            prefix=prefix,
            tool_dir=tool_dir,
        )
        result.structured_path = str(structured_path.relative_to(REPO_ROOT))
        result.structured_kind = "json"
        structured_kind = "json"
        structured_ext = "json"
    elif structured_ext:
        if tool == "nerva" and structured_ext in ("json", "jsonl"):
            bundle, text_content = _nerva_structured_payload(scenario, result, captured_at)
            from nerva_structured import dumps_nerva_bundle

            structured_path = tool_dir / f"{prefix}_output_structured.json"
            structured_path.write_text(dumps_nerva_bundle(bundle), encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = "json"
            structured_kind = "json"
            structured_ext = "json"
        elif tool == "pius" and structured_ext in ("json", "jsonl"):
            bundle, text_content = _pius_structured_payload(scenario, result, captured_at)
            from pius_structured import dumps_pius_bundle

            structured_path = tool_dir / f"{prefix}_output_structured.json"
            structured_path.write_text(dumps_pius_bundle(bundle), encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = "json"
            structured_kind = "json"
            structured_ext = "json"
        elif tool == "nuclei" and structured_ext in ("json", "jsonl"):
            bundle, text_content = _nuclei_structured_payload(scenario, result, captured_at)
            from nuclei_structured import dumps_nuclei_bundle

            structured_path = tool_dir / f"{prefix}_output_structured.json"
            structured_path.write_text(dumps_nuclei_bundle(bundle), encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = "json"
            structured_kind = "json"
            structured_ext = "json"
        elif tool == "subfinder" and structured_ext in ("json", "jsonl"):
            bundle, text_content = _subfinder_structured_payload(scenario, result, captured_at)
            from subfinder_structured import dumps_subfinder_bundle

            structured_path = tool_dir / f"{prefix}_output_structured.json"
            structured_path.write_text(dumps_subfinder_bundle(bundle), encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = "json"
            structured_kind = "json"
            structured_ext = "json"
        elif tool == "httpx" and structured_ext in ("json", "jsonl"):
            bundle, text_content = _httpx_structured_payload(scenario, result, captured_at)
            from httpx_structured import dumps_httpx_bundle

            structured_path = tool_dir / f"{prefix}_output_structured.json"
            structured_path.write_text(dumps_httpx_bundle(bundle), encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = "json"
            structured_kind = "json"
            structured_ext = "json"
        elif tool == "katana" and structured_ext in ("json", "jsonl"):
            bundle, text_content = _katana_structured_payload(scenario, result, captured_at)
            from katana_structured import dumps_katana_bundle

            structured_path = tool_dir / f"{prefix}_output_structured.json"
            structured_path.write_text(dumps_katana_bundle(bundle), encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = "json"
            structured_kind = "json"
            structured_ext = "json"
        else:
            structured_path = tool_dir / f"{prefix}_output_structured.{structured_ext}"
            out_file = scenario.get("structured_output_file")
            if out_file and Path(out_file).is_file():
                structured_path.write_text(Path(out_file).read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
                result.structured_path = str(structured_path.relative_to(REPO_ROOT))
                result.structured_kind = structured_kind
            elif result.stdout.strip() or tool in ("nerva", "pius", "nuclei", "subfinder", "httpx", "katana"):
                if tool in ("nerva", "pius", "nuclei", "subfinder", "httpx", "katana") and structured_ext == "jsonl":
                    payload = _jsonl_lines_from_stdout(result.stdout)
                else:
                    payload = result.stdout
                fixture_rel = scenario.get("structured_fixture")
                if tool in ("pius", "nuclei") and not payload.strip() and fixture_rel:
                    fixture_path = REPO_ROOT / fixture_rel
                    if fixture_path.is_file():
                        payload = fixture_path.read_text(encoding="utf-8", errors="replace")
                        result.structured_fixture_used = str(fixture_path.relative_to(REPO_ROOT))
                structured_path.write_text(payload, encoding="utf-8")
                result.structured_path = str(structured_path.relative_to(REPO_ROOT))
                result.structured_kind = structured_kind

    text_path = tool_dir / f"{prefix}_output_text.txt"
    header = ""
    if adapter_text_content is not None:
        text_content = adapter_text_content
    elif tool == "netdiscover":
        header = text_capture_header(
            command=result.command,
            scenario_name=scenario.get("name", scenario["id"]),
            captured_at=captured_at,
        )
    elif tool == "nerva":
        from nerva_structured import nerva_text_capture_header, strip_capture_header

        body_lines = [
            ln
            for ln in strip_capture_header(text_content).replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.startswith("#")
        ]
        header = nerva_text_capture_header(
            command=result.command,
            scenario_name=scenario.get("name", scenario["id"]),
            scenario_id=scenario["id"],
            target=scenario.get("target"),
            captured_at=captured_at,
            runtime=result.runtime,
            exit_code=result.exit_code,
            duration_s=result.duration_s,
            record_count=len(body_lines),
        )
    elif tool == "pius" and structured_ext == "json" and structured_path is not None:
        from pius_structured import pius_text_capture_header, strip_capture_header

        body_lines = [
            ln
            for ln in strip_capture_header(text_content).replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.startswith("#")
        ]
        header = pius_text_capture_header(
            command=result.command,
            scenario_name=scenario.get("name", scenario["id"]),
            scenario_id=scenario["id"],
            org=scenario.get("org"),
            target=scenario.get("target"),
            captured_at=captured_at,
            runtime=result.runtime,
            exit_code=result.exit_code,
            duration_s=result.duration_s,
            record_count=len(body_lines),
        )
    elif tool == "nuclei" and structured_ext == "json" and structured_path is not None:
        from nuclei_structured import nuclei_text_capture_header, strip_capture_header

        body_lines = [
            ln
            for ln in strip_capture_header(text_content).replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.startswith("#")
        ]
        header = nuclei_text_capture_header(
            command=result.command,
            scenario_name=scenario.get("name", scenario["id"]),
            scenario_id=scenario["id"],
            target=scenario.get("target"),
            captured_at=captured_at,
            runtime=result.runtime,
            exit_code=result.exit_code,
            duration_s=result.duration_s,
            record_count=len(body_lines),
        )
    elif tool == "subfinder" and structured_ext == "json" and structured_path is not None:
        from subfinder_structured import subfinder_text_capture_header, strip_capture_header

        body_lines = [
            ln
            for ln in strip_capture_header(text_content).replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.startswith("#")
        ]
        header = subfinder_text_capture_header(
            command=result.command,
            scenario_name=scenario.get("name", scenario["id"]),
            scenario_id=scenario["id"],
            target=scenario.get("target"),
            enumeration_mode=scenario.get("enumeration_mode", "passive"),
            captured_at=captured_at,
            runtime=result.runtime,
            exit_code=result.exit_code,
            duration_s=result.duration_s,
            record_count=len(body_lines),
        )
    elif tool == "httpx" and structured_ext == "json" and structured_path is not None:
        from httpx_structured import httpx_text_capture_header, strip_capture_header

        body_lines = [
            ln
            for ln in strip_capture_header(text_content).replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.startswith("#")
        ]
        header = httpx_text_capture_header(
            command=result.command,
            scenario_name=scenario.get("name", scenario["id"]),
            scenario_id=scenario["id"],
            target=scenario.get("target"),
            subfinder_scenario=scenario.get("subfinder_scenario"),
            probe_profile=scenario.get("probe_profile", ""),
            host_input_count=_host_input_count(scenario),
            captured_at=captured_at,
            runtime=result.runtime,
            exit_code=result.exit_code,
            duration_s=result.duration_s,
            record_count=len(body_lines),
        )
    elif tool == "katana" and structured_ext == "json" and structured_path is not None:
        from katana_structured import katana_text_capture_header, strip_capture_header

        body_lines = [
            ln
            for ln in strip_capture_header(text_content).replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.startswith("#")
        ]
        header = katana_text_capture_header(
            command=result.command,
            scenario_name=scenario.get("name", scenario["id"]),
            scenario_id=scenario["id"],
            target=scenario.get("target"),
            httpx_scenario=scenario.get("httpx_scenario"),
            crawl_profile=scenario.get("crawl_profile", ""),
            url_input_count=_url_input_count(scenario),
            captured_at=captured_at,
            runtime=result.runtime,
            exit_code=result.exit_code,
            duration_s=result.duration_s,
            record_count=len(body_lines),
        )
    text_path.write_text(header + text_content, encoding="utf-8")

    command_path = tool_dir / f"{prefix}_command.txt"
    command_path.write_text(result.command + "\n", encoding="utf-8")

    bundle_manifest = {
        "tool": tool,
        "exam_id": exam_id,
        "scenario_id": scenario["id"],
        "scenario_name": scenario.get("name", scenario["id"]),
        "target": scenario.get("target"),
        "org": scenario.get("org"),
        "runtime": result.runtime,
        "exit_code": result.exit_code,
        "duration_s": result.duration_s,
        "captured_at": captured_at.isoformat(),
        "structured_kind": structured_kind,
        "structured_path": result.structured_path,
        "text_path": str(text_path.relative_to(REPO_ROOT)),
        "command_path": str(command_path.relative_to(REPO_ROOT)),
        "tool_manifest_version": manifest_meta.get("version"),
        "review_status": "pending",
    }
    if result.structured_fixture_used:
        bundle_manifest["structured_fixture_used"] = result.structured_fixture_used
    if adapter_graph_path is not None:
        bundle_manifest["graph_path"] = str(adapter_graph_path.relative_to(REPO_ROOT))
    if adapter_markdown_path is not None:
        bundle_manifest["markdown_report_path"] = str(adapter_markdown_path.relative_to(REPO_ROOT))
    manifest_path = tool_dir / f"{prefix}_manifest.json"
    manifest_path.write_text(json.dumps(bundle_manifest, indent=2) + "\n", encoding="utf-8")

    review_path = tool_dir / f"{prefix}_review.status.json"
    review_path.write_text(
        json.dumps({"status": "pending", "exam_id": exam_id, "scenario_id": scenario["id"]}, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_tool_graph(tool, scenario, structured_path, result.command)
    return tool_dir


def run_scenario(tool: str, scenario_id: str, dry_run: bool = False) -> None:
    ensure_dev_paths()
    manifest = load_manifest(tool)
    scenarios = {s["id"]: s for s in manifest.get("scenarios", [])}
    if scenario_id not in scenarios:
        raise SystemExit(f"Unknown scenario '{scenario_id}' for tool '{tool}'")
    scenario = scenarios[scenario_id]
    runtime = scenario.get("runtime", manifest.get("default_runtime", "windows"))
    command = scenario["command"]
    if tool == "netdiscover":
        assert_no_truncation(command, scenario_id)
    timeout = int(scenario.get("timeout", manifest.get("default_timeout", 300)))
    cwd = scenario.get("cwd")
    cwd_path = Path(cwd) if cwd else None
    if cwd_path is None and runtime in ("windows", "windows-lan"):
        cwd_path = REPO_ROOT

    env: dict[str, str] = {}
    default_env_file = manifest.get("env_file")
    if default_env_file:
        env.update(load_env_file(REPO_ROOT / default_env_file))
    scenario_env_file = scenario.get("env_file")
    if scenario_env_file:
        env.update(load_env_file(REPO_ROOT / scenario_env_file))
    env.update(scenario.get("env") or {})

    if dry_run:
        print(json.dumps({"tool": tool, "scenario": scenario_id, "command": command, "runtime": runtime}, indent=2))
        return

    if scenario.get("harvest_deferred"):
        print(f"[harvest] {tool}/{scenario_id}: deferred — {scenario.get('harvest_deferred_reason', 'not run')}")
        return

    print(f"[harvest] {tool}/{scenario_id} ({runtime}) …")
    captured_at = datetime.now(timezone.utc)
    isolated_command = isolate_text_capture_command(command, runtime, tool)
    export_rel = scenario.get("jsonl_export")
    export_path = (REPO_ROOT / export_rel) if export_rel else None
    if export_path is not None:
        export_path.parent.mkdir(parents=True, exist_ok=True)
    reuse_export = bool(scenario.get("reuse_export") and export_path and export_path.is_file())
    if reuse_export:
        stderr_text = ""
        if export_path and export_path.name.endswith(".jsonl"):
            stderr_candidate = export_path.parent / f"{export_path.stem}.stderr.txt"
            if stderr_candidate.is_file():
                text = stderr_candidate.read_text(encoding="utf-8", errors="replace")
                first = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
                if first and not first.startswith("{"):
                    stderr_text = text
        result = RunResult(
            command=command,
            runtime=runtime,
            exit_code=0,
            duration_s=0.0,
            stdout="",
            stderr=stderr_text,
        )
        print(f"[harvest] reusing export {export_rel}")
    else:
        # Do not wsl --shutdown before pius: breaks DNS on the next wsl bash -lc invocation.
        if tool != "pius":
            pass
        result = run_command(isolated_command, runtime, cwd_path, timeout, env=env)
        if tool == "pius" and runtime in ("wsl", "wsl-root") and not result.stdout.strip():
            subprocess.run(["wsl", "--shutdown"], capture_output=True, timeout=30)
            time.sleep(3)
            result = run_command(isolated_command, runtime, cwd_path, timeout, env=env)
    result.command = command
    # JSONL tools write to -o export; hydrate stdout from file when present.
    if tool in ("nuclei", "subfinder", "httpx", "katana"):
        export_rel = scenario.get("jsonl_export")
        if export_rel:
            export_path = REPO_ROOT / export_rel
            export_path.parent.mkdir(parents=True, exist_ok=True)
            if export_path.is_file() and export_path.stat().st_size > 0:
                result.stdout = export_path.read_text(encoding="utf-8", errors="replace")
    # Post-run structured file pickup (e.g. CMSeeK cms.json)
    src = scenario.get("structured_source_path")
    if src:
        src_path = Path(src)
        if not src_path.is_absolute() and cwd_path:
            src_path = cwd_path / src
        if not src_path.is_file() and runtime in ("wsl", "wsl-root"):
            # Read structured artifact from WSL filesystem
            wsl_cat = ["wsl", "bash", "-lc", f"cat {src_path}"]
            if runtime == "wsl-root":
                wsl_cat = ["wsl", "-u", "root", "bash", "-lc", f"cat {src_path}"]
            cat_proc = subprocess.run(wsl_cat, capture_output=True, text=True, timeout=30)
            if cat_proc.returncode == 0 and cat_proc.stdout.strip():
                tmp = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs" / tool / "_tmp_structured.json"
                tmp.parent.mkdir(parents=True, exist_ok=True)
                tmp.write_text(cat_proc.stdout, encoding="utf-8")
                scenario = {**scenario, "structured_output_file": str(tmp)}
        elif src_path.is_file():
            scenario = {**scenario, "structured_output_file": str(src_path.resolve())}
    write_bundle(tool, scenario, result, manifest, captured_at=captured_at)
    print(f"[harvest] exit={result.exit_code} duration={result.duration_s}s")


def run_all(tool: str, dry_run: bool = False) -> None:
    manifest = load_manifest(tool)
    if tool == "httpx" and not dry_run:
        prep = CORPUS_DIR / "prepare_httpx_hosts_from_subfinder.py"
        print("[harvest] preparing httpx host lists from subfinder examinations …")
        subprocess.run([sys.executable, str(prep)], cwd=str(REPO_ROOT), check=True)
    if tool == "katana" and not dry_run:
        prep = CORPUS_DIR / "prepare_katana_urls_from_httpx.py"
        print("[harvest] preparing katana seed URL lists from httpx examinations …")
        subprocess.run([sys.executable, str(prep)], cwd=str(REPO_ROOT), check=True)
    for scenario in manifest.get("scenarios", []):
        run_scenario(tool, scenario["id"], dry_run=dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description="CLI corpus harvest runner")
    parser.add_argument("--tool", required=True, help="Tool manifest name (e.g. nmap)")
    parser.add_argument("--scenario", help="Scenario id; omit to run all scenarios in manifest")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.scenario:
        run_scenario(args.tool, args.scenario, dry_run=args.dry_run)
    else:
        run_all(args.tool, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
