"""Tool driver registry (T1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Protocol


class ToolDriver(Protocol):
    tool_id: str

    def run(
        self,
        argv: List[str],
        *,
        input_path: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return {exit_code, structured_path}."""


@dataclass
class FixtureDriver:
    """Dry-run driver: returns a preloaded scan graph (no CLI)."""

    tool_id: str
    scan_graph: Dict[str, Any]
    structured_path: Optional[str] = None

    def run(
        self,
        argv: List[str],
        *,
        input_path: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "exit_code": 0,
            "structured_path": self.structured_path or "",
            "scan_graph": self.scan_graph,
        }


_REGISTRY: Dict[str, ToolDriver] = {}


def register(driver: ToolDriver) -> None:
    _REGISTRY[driver.tool_id] = driver


def get(tool_id: str) -> ToolDriver:
    if tool_id not in _REGISTRY:
        raise KeyError(f"unknown tool driver: {tool_id}")
    return _REGISTRY[tool_id]


def parse_uses(uses: str) -> str:
    if not uses.startswith("tool."):
        raise ValueError(f"invalid uses: {uses}")
    return uses.split(".", 1)[1]
