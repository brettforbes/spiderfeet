"""v2 CLI module contract — four-output ``run()`` (SPEC-010 R10-14).

Every ``modules_v2/sfp_cli_<tool>.py`` module implements ``run(scan_step_spec)``
returning Text, Structured, Graph, and Narrative plus execution metadata.

CLI execution is **argv-only** (``subprocess`` list form). Never pass a shell
string or ``shell=True``.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

_REPO_ROOT = Path(__file__).resolve().parents[1]
_TOOLS_BIN = _REPO_ROOT / ".tools" / "bin"
_TOOLS_ROOT = _REPO_ROOT / ".tools"


STATUS_SUCCESS = "SUCCESS"
STATUS_ERROR = "ERROR"
STATUS_TIMEOUT = "TIMEOUT"
STATUS_MISSING_TOOL = "MISSING_TOOL"

RESULT_KEYS = (
    "command",
    "text",
    "structured",
    "structured_type",
    "graph",
    "narrative",
    "status",
    "counts",
    "duration",
    "timestamp",
)


@dataclass
class ModuleResult:
    """Canonical four-output result for one scan-step invocation."""

    command: list[str]
    text: str
    structured: Any
    structured_type: str
    graph: dict[str, Any]
    narrative: str
    status: str
    counts: dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0
    timestamp: str = ""
    error: str | None = None
    exit_code: int | None = None
    stderr: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        # Keep the R10-14 contract keys first; extras (error/exit_code/stderr) trail.
        ordered = {key: payload[key] for key in RESULT_KEYS}
        for key in ("error", "exit_code", "stderr"):
            if payload.get(key) not in (None, ""):
                ordered[key] = payload[key]
        return ordered


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def empty_graph() -> dict[str, Any]:
    return {"nodes": [], "edges": []}


def graph_counts(graph: Mapping[str, Any] | None) -> dict[str, int]:
    if not graph:
        return {"nodes": 0, "edges": 0, "hosts": 0}
    nodes = list(graph.get("nodes") or [])
    edges = list(graph.get("edges") or [])
    hosts = sum(1 for n in nodes if n.get("nugget_id") == "HOST")
    return {"nodes": len(nodes), "edges": len(edges), "hosts": hosts}


def _repo_tool_candidates(name: str) -> list[Path]:
    """Known SpiderFeet install layouts under ``.tools/`` (Windows + portable)."""
    bare = name
    exe = f"{name}.exe"
    return [
        _TOOLS_BIN / exe,
        _TOOLS_BIN / bare,
        _TOOLS_ROOT / bare,  # e.g. .tools/pius
        _TOOLS_ROOT / bare / exe,  # e.g. .tools/dnsx/dnsx.exe
        _TOOLS_ROOT / bare / bare,
    ]


def _env_tool_path(name: str) -> str | None:
    """Optional operator overrides: SPIDERFEET_<NAME> or <NAME>_BIN."""
    key = name.upper().replace("-", "_")
    for env_key in (f"SPIDERFEET_{key}", f"{key}_BIN"):
        raw = (os.environ.get(env_key) or "").strip()
        if raw and Path(raw).is_file():
            return raw
    return None


def resolve_executable(
    name: str,
    *,
    prefer_wsl: bool = True,
) -> tuple[list[str], str | None]:
    """Resolve a CLI tool to an argv prefix.

    Order: env override → native PATH → repo ``.tools/`` layouts → WSL ``which``.

    Returns ``(prefix_argv, error)``. On success ``error`` is ``None`` and
    ``prefix_argv`` is either ``[path]`` (native) or ``["wsl", name]``.
    """
    env_path = _env_tool_path(name)
    if env_path:
        return [env_path], None

    native = shutil.which(name)
    if native:
        return [native], None

    for candidate in _repo_tool_candidates(name):
        if candidate.is_file():
            return [str(candidate)], None

    if prefer_wsl and shutil.which("wsl"):
        try:
            probe = subprocess.run(
                ["wsl", "which", name],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            probe = None
        if probe is not None and probe.returncode == 0 and (probe.stdout or "").strip():
            return ["wsl", name], None

    return [], f"{name} not found on PATH, .tools/, or WSL"


def run_argv(
    argv: Sequence[str],
    *,
    timeout: float | None = 300.0,
    cwd: str | None = None,
    env: Mapping[str, str] | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command as an argv list only — never ``shell=True``."""
    if not argv:
        raise ValueError("argv must be a non-empty sequence")
    if isinstance(argv, str):
        raise TypeError("argv must be a sequence of strings, not a shell string")
    cmd = [str(part) for part in argv]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd,
        env=dict(env) if env is not None else None,
        input=input_text,
        shell=False,
        check=False,
    )


def error_result(
    *,
    command: Sequence[str],
    status: str,
    error: str,
    duration: float = 0.0,
    exit_code: int | None = None,
    stderr: str = "",
    structured_type: str = "json",
) -> dict[str, Any]:
    return ModuleResult(
        command=list(command),
        text="",
        structured={"error": error, "exit_code": exit_code, "stderr": stderr},
        structured_type=structured_type,
        graph=empty_graph(),
        narrative="",
        status=status,
        counts=graph_counts(None),
        duration=duration,
        timestamp=utc_now_iso(),
        error=error,
        exit_code=exit_code,
        stderr=stderr,
    ).to_dict()


class CliModuleBase:
    """Base class for v2 four-output CLI modules."""

    module_id: str = ""
    tool_name: str = ""
    structured_type: str = "json"
    consumed_inputs: list[str] = []
    produced_nugget_types: list[str] = []

    def build_argv(self, scan_step_spec: Mapping[str, Any]) -> list[str]:
        raise NotImplementedError

    def run(self, scan_step_spec: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """Execute the tool and return the R10-14 four-output result dict."""
        raise NotImplementedError

    def _merge_spec(self, scan_step_spec: Mapping[str, Any] | None) -> dict[str, Any]:
        return dict(scan_step_spec or {})

    def _timed_run_argv(
        self,
        argv: Sequence[str],
        *,
        timeout: float | None = 300.0,
    ) -> tuple[subprocess.CompletedProcess[str] | None, float, str | None]:
        started = time.perf_counter()
        try:
            completed = run_argv(argv, timeout=timeout)
            return completed, time.perf_counter() - started, None
        except subprocess.TimeoutExpired as exc:
            return None, time.perf_counter() - started, f"timeout after {exc.timeout}s"
        except OSError as exc:
            return None, time.perf_counter() - started, str(exc)


def ensure_no_shell_string(argv: Sequence[str]) -> list[str]:
    """Validate and normalize an argv list (rejects bare shell strings)."""
    if isinstance(argv, str):
        raise TypeError("command must be an argv list, not a shell string")
    parts = [str(p) for p in argv]
    if not parts:
        raise ValueError("command argv is empty")
    return parts


def annotate_counts(
    result: MutableMapping[str, Any],
    graph: Mapping[str, Any] | None = None,
    **extra: Any,
) -> None:
    counts = graph_counts(graph if graph is not None else result.get("graph"))
    counts.update({k: v for k, v in extra.items() if v is not None})
    result["counts"] = counts
