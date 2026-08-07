"""Configurable roots for modules_v2 rule packs and catalogues.

Override with env ``MODULES_V2_ROOT`` (absolute path to the ``modules_v2`` package root).
"""

from __future__ import annotations

import os
from pathlib import Path

_DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def modules_v2_root() -> Path:
    """Return modules_v2 root (env override or package parent of ``_core``)."""
    override = os.environ.get("MODULES_V2_ROOT", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return _DEFAULT_ROOT


MODULES_V2_ROOT = modules_v2_root()
RULES_DIR = MODULES_V2_ROOT / "_rules"
SHARED_RULES_DIR = RULES_DIR / "_shared"
CATALOGUES_DIR = MODULES_V2_ROOT / "_catalogues"
NUGGETS_PATH = CATALOGUES_DIR / "nuggets.json"
NUGGETS_EXTENSION_PATH = CATALOGUES_DIR / "nuggets_extension.json"


def tool_rules_dir(tool_id: str) -> Path:
    """Return ``modules_v2/_rules/<tool_id>/``."""
    return RULES_DIR / tool_id


def mapping_path(tool_id: str) -> Path:
    """Default mapping pack path for a tool."""
    return tool_rules_dir(tool_id) / "mapping.yaml"
