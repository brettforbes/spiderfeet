"""Shared SPEC-004 type contracts for adapter and rule-pack work."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

CaptureFamily = Literal["structured_native", "text_native"]


@dataclass(frozen=True)
class RulePack:
    """Minimal rule-pack descriptor; mapping execution is introduced in later stories."""

    tool: str
    capture_family: CaptureFamily
    scan_head: dict[str, Any] = field(default_factory=dict)
    mappings: list[dict[str, Any]] = field(default_factory=list)
    narrative: dict[str, Any] = field(default_factory=dict)
    shared: dict[str, Any] = field(default_factory=dict)
