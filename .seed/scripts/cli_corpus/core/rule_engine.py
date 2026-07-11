"""Minimal SPEC-004 YAML rule-pack loader and graph emitter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .graph_builder import GraphBuilder, nugget_node
from .types import CaptureFamily, RulePack

ALLOWED_CAPTURE_FAMILIES: set[CaptureFamily] = {"structured_native", "text_native"}
DEFAULT_ALLOWED_RELATIONS = {"contains", "had", "listens-to"}


class RulePackError(ValueError):
    """Raised when a SPEC-004 rule pack is missing required contract fields."""


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RulePackError(f"{path} must contain a YAML mapping")
    return data


def load_shared_rules(shared_dir: Path) -> dict[str, Any]:
    """Load optional shared YAML contracts from `rules/_shared/`."""
    shared: dict[str, Any] = {}
    if not shared_dir.is_dir():
        return shared
    for path in sorted(shared_dir.glob("*.yaml")):
        shared[path.stem] = _load_yaml(path)
    return shared


def load_rule_pack(mapping_path: Path, *, shared_dir: Path | None = None) -> RulePack:
    """Load and validate one tool mapping pack."""
    data = _load_yaml(mapping_path)
    tool = data.get("tool")
    if not isinstance(tool, str) or not tool.strip() or tool == "REPLACE_ME":
        raise RulePackError("rule pack requires a concrete `tool`")

    capture_family = data.get("capture_family")
    if capture_family not in ALLOWED_CAPTURE_FAMILIES:
        allowed = ", ".join(sorted(ALLOWED_CAPTURE_FAMILIES))
        raise RulePackError(f"`capture_family` must be one of: {allowed}")

    mappings = data.get("mappings") or []
    if not isinstance(mappings, list):
        raise RulePackError("`mappings` must be a list when present")

    for mapping in mappings:
        if not isinstance(mapping, dict):
            raise RulePackError("each mapping entry must be a YAML mapping")
        relation = mapping.get("relation", "had")
        if relation not in DEFAULT_ALLOWED_RELATIONS:
            raise RulePackError(f"unsupported relation `{relation}`")
        if "path" not in mapping or "nugget_id" not in mapping:
            raise RulePackError("each mapping requires `path` and `nugget_id`")

    shared = load_shared_rules(shared_dir) if shared_dir is not None else {}
    return RulePack(
        tool=tool,
        capture_family=capture_family,
        scan_head=data.get("scan_head") or {},
        mappings=mappings,
        narrative=data.get("narrative") or {},
        shared=shared,
    )


def resolve_path(source: dict[str, Any], path: str) -> Any:
    """Resolve a simple dotted path from structured scan data."""
    current: Any = source
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


class RuleEngine:
    """Build a graph from a loaded rule pack and one structured document."""

    def __init__(self, rule_pack: RulePack) -> None:
        self.rule_pack = rule_pack

    def build_graph(self, source: dict[str, Any]) -> dict[str, Any]:
        builder = GraphBuilder()
        scan = self._add_scan_head(builder, source)
        self._add_mapped_descriptors(builder, source, scan["id"])
        return builder.build()

    def _add_scan_head(self, builder: GraphBuilder, source: dict[str, Any]) -> dict[str, Any]:
        scan_head = self.rule_pack.scan_head
        data_path = scan_head.get("data_path", "command")
        fallback = scan_head.get("fallback") or self.rule_pack.tool
        scan_data = resolve_path(source, data_path) or fallback
        scan = builder.add_node(
            nugget_node(
                scan_head.get("nugget_id", "SCAN_RECORD"),
                str(scan_data),
                description=scan_head.get("description", "Scan Record"),
            )
        )

        cli_data = source.get("command") or scan_data
        scan_cli = builder.add_node(nugget_node("SCAN_CLI", str(cli_data), nugget_type="DESCRIPTOR"))
        builder.add_edge(scan["id"], scan_cli["id"], "had")
        return scan

    def _add_mapped_descriptors(
        self,
        builder: GraphBuilder,
        source: dict[str, Any],
        scan_id: str,
    ) -> None:
        for mapping in self.rule_pack.mappings:
            value = resolve_path(source, str(mapping["path"]))
            if value is None or value == "":
                continue
            node = builder.add_node(
                nugget_node(
                    str(mapping["nugget_id"]),
                    str(value),
                    nugget_type=str(mapping.get("nugget_type", "DESCRIPTOR")),
                    description=mapping.get("description"),
                )
            )
            builder.add_edge(scan_id, node["id"], str(mapping.get("relation", "had")))
