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
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFESTS_DIR = Path(__file__).resolve().parent / "manifests"
EXAM_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "app_examination_docs"
NUGGET_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"


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


def run_command(command: str, runtime: str, cwd: Path | None, timeout: int) -> RunResult:
    started = time.monotonic()
    if runtime in ("wsl", "wsl-root"):
        inner = command
        if cwd:
            inner = f"cd {cwd} && {command}"
        wsl_args = ["wsl", "-e", "bash", "-lc", inner]
        if runtime == "wsl-root":
            wsl_args = ["wsl", "-u", "root", "bash", "-lc", inner]
        shell_cmd = wsl_args
        use_shell = False
        run_cwd = None
    else:
        shell_cmd = command if sys.platform == "win32" else command
        use_shell = sys.platform == "win32"
        run_cwd = str(cwd) if cwd else None
    proc = subprocess.run(
        shell_cmd,
        capture_output=True,
        text=True,
        cwd=run_cwd,
        timeout=timeout,
        shell=use_shell,
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


def write_bundle(
    tool: str,
    scenario: dict[str, Any],
    result: RunResult,
    manifest_meta: dict[str, Any],
) -> Path:
    tool_dir = EXAM_ROOT / tool
    tool_dir.mkdir(parents=True, exist_ok=True)
    exam_id = next_exam_id(tool_dir)
    prefix = f"{exam_id}"

    structured_kind = scenario.get("structured_kind")
    structured_ext = scenario.get("structured_ext")
    structured_path: Path | None = None
    if structured_ext:
        structured_path = tool_dir / f"{prefix}_output_structured.{structured_ext}"
        # Structured output may be in stdout or a file path from scenario
        out_file = scenario.get("structured_output_file")
        if out_file and Path(out_file).is_file():
            structured_path.write_text(Path(out_file).read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = structured_kind
        elif result.stdout.strip():
            structured_path.write_text(result.stdout, encoding="utf-8")
            result.structured_path = str(structured_path.relative_to(REPO_ROOT))
            result.structured_kind = structured_kind

    text_path = tool_dir / f"{prefix}_output_text.txt"
    text_content = result.stderr if scenario.get("text_from") == "stderr" else result.stdout
    if scenario.get("text_output_file") and Path(scenario["text_output_file"]).is_file():
        text_content = Path(scenario["text_output_file"]).read_text(encoding="utf-8", errors="replace")
    text_path.write_text(text_content, encoding="utf-8")

    command_path = tool_dir / f"{prefix}_command.txt"
    command_path.write_text(result.command + "\n", encoding="utf-8")

    bundle_manifest = {
        "tool": tool,
        "exam_id": exam_id,
        "scenario_id": scenario["id"],
        "scenario_name": scenario.get("name", scenario["id"]),
        "target": scenario.get("target"),
        "runtime": result.runtime,
        "exit_code": result.exit_code,
        "duration_s": result.duration_s,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "structured_kind": structured_kind,
        "structured_path": result.structured_path,
        "text_path": str(text_path.relative_to(REPO_ROOT)),
        "command_path": str(command_path.relative_to(REPO_ROOT)),
        "tool_manifest_version": manifest_meta.get("version"),
        "review_status": "pending",
    }
    manifest_path = tool_dir / f"{prefix}_manifest.json"
    manifest_path.write_text(json.dumps(bundle_manifest, indent=2) + "\n", encoding="utf-8")

    review_path = tool_dir / f"{prefix}_review.status.json"
    review_path.write_text(
        json.dumps({"status": "pending", "exam_id": exam_id, "scenario_id": scenario["id"]}, indent=2) + "\n",
        encoding="utf-8",
    )
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
    timeout = int(scenario.get("timeout", manifest.get("default_timeout", 300)))
    cwd = scenario.get("cwd")
    cwd_path = Path(cwd) if cwd else None

    if dry_run:
        print(json.dumps({"tool": tool, "scenario": scenario_id, "command": command, "runtime": runtime}, indent=2))
        return

    print(f"[harvest] {tool}/{scenario_id} ({runtime}) …")
    result = run_command(command, runtime, cwd_path, timeout)
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
    write_bundle(tool, scenario, result, manifest)
    print(f"[harvest] exit={result.exit_code} duration={result.duration_s}s")


def run_all(tool: str, dry_run: bool = False) -> None:
    manifest = load_manifest(tool)
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
