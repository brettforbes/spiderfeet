"""Typed workflow document shapes (R1)."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class WorkflowInputSpec(TypedDict, total=False):
    type: str
    description: str
    default: List[str]


class WorkflowDocument(TypedDict):
    apiVersion: str
    kind: str
    id: str
    info: Dict[str, Any]
    inputs: Dict[str, WorkflowInputSpec]
    steps: List[Dict[str, Any]]
