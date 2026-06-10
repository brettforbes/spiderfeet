"""Shared helpers for resolving local CLI tool binaries (Stage 5 — #733)."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from shutil import which
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_BIN = REPO_ROOT / ".tools" / "bin"
NUCLEI_TEMPLATES = REPO_ROOT / ".tools" / "nuclei-templates"


def _path_candidates(name: str) -> list[Path]:
    names = [name]
    if sys.platform == "win32":
        names.extend([f"{name}.exe", f"{name}.cmd"])
    return [TOOLS_BIN / n for n in names]


def resolve_cli_binary(name: str, *, extra_paths: Optional[list[Path]] = None) -> Optional[str]:
    found = which(name) or (which(f"{name}.exe") if sys.platform == "win32" else None)
    if found and os.path.isfile(found):
        return found

    for folder in os.environ.get("PATH", "").split(os.pathsep):
        for candidate_name in (name, f"{name}.exe", f"{name}.cmd"):
            candidate = os.path.join(folder, candidate_name)
            if os.path.isfile(candidate):
                return candidate

    for candidate in _path_candidates(name):
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
