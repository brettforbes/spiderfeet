"""Shared narrative profile loading and appendix rendering (SPEC-004 R4-01-05)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_narrative_profile(path: Path) -> dict[str, Any]:
    """Load _rules/<tool>/narrative.yaml when present."""
    import yaml

    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def append_standard_appendix(lines: list[str], graph: dict[str, Any]) -> None:
    """Append §4.3 node/edge appendix covering every graph value."""
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}
    lines.extend(["", "## Appendix", "", "### Nodes", ""])
    for node in sorted(nodes, key=lambda n: (n.get("nugget_id", ""), n.get("nugget_data", ""))):
        lines.append(f"- `{node.get('nugget_id')}`: {node.get('nugget_data')}")
    lines.extend(["", "### Edges", ""])
    for edge in edges:
        src = by_id.get(edge.get("source"), {})
        tgt = by_id.get(edge.get("target"), {})
        lines.append(
            f"- `{src.get('nugget_id')}` `{edge.get('relation')}` `{tgt.get('nugget_id')}`"
        )
