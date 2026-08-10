"""Shared helpers for resolving local CLI tool binaries (Stage 5 — #733).

Canonical lookup used by legacy ``sfp_tool_*`` wrappers and v2
``modules_v2._base.resolve_executable`` (SPEC-010 twin-fork CLIs).

Order: env override → PATH → repo ``.tools/`` layouts.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from shutil import which
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_BIN = REPO_ROOT / ".tools" / "bin"
TOOLS_ROOT = REPO_ROOT / ".tools"
NUCLEI_TEMPLATES = REPO_ROOT / ".tools" / "nuclei-templates"


def _env_tool_path(name: str) -> Optional[str]:
    """Optional operator overrides: ``SPIDERFEET_<NAME>`` or ``<NAME>_BIN``."""
    key = name.upper().replace("-", "_")
    for env_key in (f"SPIDERFEET_{key}", f"{key}_BIN"):
        raw = (os.environ.get(env_key) or "").strip()
        if raw and Path(raw).is_file():
            return raw
    return None


def _repo_tool_candidates(name: str) -> list[Path]:
    """Known SpiderFeet install layouts under ``.tools/`` (Windows + portable)."""
    bare = name
    exe = f"{name}.exe"
    candidates = [
        TOOLS_BIN / exe,
        TOOLS_BIN / bare,
        TOOLS_ROOT / bare,  # e.g. .tools/pius
        TOOLS_ROOT / bare / exe,  # e.g. .tools/dnsx/dnsx.exe
        TOOLS_ROOT / bare / bare,
    ]
    if sys.platform == "win32":
        candidates.insert(1, TOOLS_BIN / f"{name}.cmd")
    return candidates


def resolve_cli_binary(name: str, *, extra_paths: Optional[list[Path]] = None) -> Optional[str]:
    """Resolve a CLI binary path (native file path only — not a WSL wrapper)."""
    env_path = _env_tool_path(name)
    if env_path:
        return env_path

    found = which(name) or (which(f"{name}.exe") if sys.platform == "win32" else None)
    if found and os.path.isfile(found):
        return found

    for folder in os.environ.get("PATH", "").split(os.pathsep):
        for candidate_name in (name, f"{name}.exe", f"{name}.cmd"):
            candidate = os.path.join(folder, candidate_name)
            if os.path.isfile(candidate):
                return candidate

    for candidate in _repo_tool_candidates(name):
        if candidate.is_file():
            return str(candidate)

    if extra_paths:
        for candidate in extra_paths:
            if candidate.is_file():
                return str(candidate)

    return None


def resolve_nuclei_templates() -> Optional[str]:
    if NUCLEI_TEMPLATES.is_dir() and any(NUCLEI_TEMPLATES.rglob("*.yaml")):
        return str(NUCLEI_TEMPLATES)
    home = Path.home() / "nuclei-templates"
    if home.is_dir() and any(home.rglob("*.yaml")):
        return str(home)
    return None


def _wsl_cli_root() -> Path:
    return Path(os.environ.get("SPIDERFEET_CLI_ROOT", Path.home() / ".local" / "spiderfeet-cli"))


def load_wsl_cli_manifest() -> bool:
    """Source ~/.local/spiderfeet-cli/manifest.env into os.environ when present."""
    manifest = _wsl_cli_root() / "manifest.env"
    if not manifest.is_file():
        return False
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value:
            os.environ.setdefault(key, value)
    return True


def _env_or_file(path_key: str, *candidates: Path) -> Optional[str]:
    raw = os.environ.get(path_key, "").strip()
    if raw and Path(raw).is_file():
        return raw
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


def quarantine_cli_module_opts() -> dict[str, dict[str, str]]:
    """Module opts for the six quarantine CLI wrappers (WSL/apt layout)."""
    root = _wsl_cli_root()
    node = os.environ.get("SPIDERFEET_NODE_PATH") or resolve_cli_binary("node") or "/usr/bin/node"
    wapp_candidates = [
        Path(os.environ.get("SPIDERFEET_WAPPALYZER_PATH", "")),
        root / "wappalyzer" / "src" / "drivers" / "npm" / "cli.js",
        root / "wappalyzer" / "src" / "drivers" / "webextension" / "cli.js",
    ]
    wapp = _env_or_file("SPIDERFEET_WAPPALYZER_PATH", *wapp_candidates)

    cmseek = _env_or_file(
        "SPIDERFEET_CMSEEK_PATH",
        root / "CMSeeK" / "cmseek.py",
    )
    testssl = _env_or_file(
        "SPIDERFEET_TESTSSL_PATH",
        root / "testssl.sh" / "testssl.sh",
    )
    whatweb = _env_or_file(
        "SPIDERFEET_WHATWEB_PATH",
        root / "WhatWeb" / "whatweb",
    )
    nbtscan = os.environ.get("SPIDERFEET_NBTSCAN_PATH") or resolve_cli_binary("nbtscan")
    onesixtyone = os.environ.get("SPIDERFEET_ONESIXTYONE_PATH") or resolve_cli_binary(
        "onesixtyone"
    )

    opts: dict[str, dict[str, str]] = {}
    if cmseek:
        opts["sfp_tool_cmseek"] = {"cmseekpath": cmseek, "pythonpath": "python3"}
    if testssl:
        opts["sfp_tool_testsslsh"] = {"testsslsh_path": testssl}
    if whatweb:
        opts["sfp_tool_whatweb"] = {"whatweb_path": whatweb, "ruby_path": "ruby"}
    if nbtscan:
        opts["sfp_tool_nbtscan"] = {"nbtscan_path": nbtscan}
    if onesixtyone:
        opts["sfp_tool_onesixtyone"] = {"onesixtyone_path": onesixtyone}
    if wapp:
        opts["sfp_tool_wappalyzer"] = {"wappalyzer_path": wapp, "node_path": node}
    return opts
