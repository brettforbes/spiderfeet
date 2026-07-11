#!/usr/bin/env python3
"""Build proposed nugget graphs from subfinder structured JSON bundles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from adapters import subfinder as subfinder_adapter


def subfinder_to_graph(raw: str, target: str, command: str) -> dict[str, Any]:
    structured = subfinder_adapter.to_structured(raw, target=target, command=command)
    return subfinder_adapter.to_graph(structured, target=target)


def write_graph_artifacts(structured_path: Path, graph_path: Path, scenario_id: str, target: str, command: str) -> None:
    del scenario_id
    raw = structured_path.read_text(encoding="utf-8", errors="replace")
    graph = subfinder_to_graph(raw, target, command)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
