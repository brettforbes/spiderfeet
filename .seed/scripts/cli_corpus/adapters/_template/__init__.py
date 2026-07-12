"""Adapter template — copy to adapters/<tool>/ and implement.

Public contract (SPEC-004 / SPEC-005 / proj-07):
- CAPTURE_FAMILY: \"structured_native\" | \"text_native\"
- to_structured / to_text / to_graph / to_narrative / build_outputs

Onboarding: .seed/scripts/cli_corpus/ONBOARDING.md
Rules: .cursor/rules/proj-07-cli-graph-rules-engine.mdc

Guidelines:
- Put field→nugget maps in rules/<tool>/mapping.yaml (not here).
- Cite seed rule ids in hooks.py docstrings.
- Create IP nodes via core.ip_classify.classify_ip (never hardcode IPv4-only).
- to_narrative should call the shared narrative engine + rules/<tool>/narrative.yaml
  (do not ship bullet-list stubs).
"""

from __future__ import annotations

from typing import Any, Literal

CAPTURE_FAMILY: Literal["structured_native", "text_native"] = "structured_native"


def to_structured(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    raise NotImplementedError


def to_text(*_args: Any, **_kwargs: Any) -> str:
    raise NotImplementedError


def to_graph(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    raise NotImplementedError


def to_narrative(*_args: Any, **_kwargs: Any) -> str:
    raise NotImplementedError


def build_outputs(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    """Return text, structured, structured_json, graph, markdown_report."""
    raise NotImplementedError
