#!/usr/bin/env python3
"""Build proposed nugget graphs from katana structured JSON bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from adapters import katana as katana_adapter


def katana_to_graph(raw: str, target: str, command: str) -> dict[str, Any]:
    structured = katana_adapter.to_structured(raw, target=target, command=command)
    return katana_adapter.to_graph(structured, target=target)


def write_graph_artifacts(structured_path, graph_path, scenario_id: str, target: str, command: str) -> None:
    del scenario_id
    raw = structured_path.read_text(encoding="utf-8", errors="replace")
    graph = katana_to_graph(raw, target, command)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
