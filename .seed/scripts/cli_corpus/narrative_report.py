#!/usr/bin/env python3
"""Shared graph helpers + narrative coverage validation (SPEC-014 BD2).

Bespoke ``NarrativeReportBuilder`` / ``NetdiscoverNarrativeReportBuilder`` were
retired in favour of ``core.narrative_engine.render_narrative`` (R14-06).
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple

Relation = str
Node = Dict[str, Any]
Edge = Dict[str, str]
Graph = Dict[str, Any]


def node_label(node: Node) -> str:
    return str(node.get("nugget_description") or node.get("nugget_id") or "nugget")


def node_value(node: Node) -> str:
    return str(node.get("nugget_data") or node.get("data") or "")


class SemanticGraph:
    """Index nodes and edges for ontology-aware traversal (non-narrative helpers)."""

    def __init__(self, graph: Graph) -> None:
        self.nodes: Dict[str, Node] = {
            str(n["id"]): n for n in graph.get("nodes", []) if n.get("id")
        }
        self.out_edges: Dict[str, List[Tuple[Relation, str]]] = {}
        self.in_edges: Dict[str, List[Tuple[Relation, str]]] = {}
        for edge in graph.get("edges", []):
            source = edge.get("source", "")
            target = edge.get("target", "")
            relation = edge.get("relation", "")
            if not source or not target:
                continue
            self.out_edges.setdefault(source, []).append((relation, target))
            self.in_edges.setdefault(target, []).append((relation, source))

    def get(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def outgoing(
        self,
        node_id: str,
        relation: Optional[Relation] = None,
        nugget_id: Optional[str] = None,
    ) -> List[Node]:
        results: List[Node] = []
        for rel, target in self.out_edges.get(node_id, []):
            if relation and rel != relation:
                continue
            node = self.get(target)
            if not node:
                continue
            if nugget_id and node.get("nugget_id") != nugget_id:
                continue
            results.append(node)
        return self._sort_nodes(results)

    def incoming(
        self,
        node_id: str,
        relation: Optional[Relation] = None,
        nugget_id: Optional[str] = None,
    ) -> List[Node]:
        results: List[Node] = []
        for rel, source in self.in_edges.get(node_id, []):
            if relation and rel != relation:
                continue
            node = self.get(source)
            if not node:
                continue
            if nugget_id and node.get("nugget_id") != nugget_id:
                continue
            results.append(node)
        return self._sort_nodes(results)

    def descriptors(self, entity_id: str) -> List[Node]:
        return self.outgoing(entity_id, relation="had")

    def contained(self, entity_id: str, nugget_id: Optional[str] = None) -> List[Node]:
        return self.outgoing(entity_id, relation="contains", nugget_id=nugget_id)

    def contained_ip_addresses(self, entity_id: str) -> List[Node]:
        nodes: List[Node] = []
        for nugget_id in ("IPV4_ADDRESS", "IPV6_ADDRESS", "IP_ADDRESS"):
            nodes.extend(self.contained(entity_id, nugget_id=nugget_id))
        return self._sort_nodes({n["id"]: n for n in nodes}.values())

    def find_by_nugget_id(self, nugget_id: str) -> List[Node]:
        return self._sort_nodes(
            [node for node in self.nodes.values() if node.get("nugget_id") == nugget_id]
        )

    def find_scan(self, scan_nugget_id: str = "SCAN_RECORD") -> Optional[Node]:
        scans = self.find_by_nugget_id(scan_nugget_id)
        return scans[0] if scans else None

    def find_trace(self, trace_nugget_id: str = "TRACE") -> Optional[Node]:
        traces = self.find_by_nugget_id(trace_nugget_id)
        return traces[0] if traces else None

    def scan_hosts(
        self,
        scan_nugget_id: str = "SCAN_RECORD",
        host_nugget_id: str = "HOST",
    ) -> List[Node]:
        scan = self.find_scan(scan_nugget_id)
        if not scan:
            return self.find_by_nugget_id(host_nugget_id)
        return self.contained(scan["id"], nugget_id=host_nugget_id)

    def all_nodes(self) -> List[Node]:
        return self._sort_nodes(list(self.nodes.values()))

    @staticmethod
    def _sort_nodes(nodes: Iterable[Node]) -> List[Node]:
        return sorted(
            nodes,
            key=lambda n: (
                str(n.get("nugget_type", "")),
                str(n.get("nugget_id", "")),
                node_value(n),
                str(n.get("id", "")),
            ),
        )


def validate_narrative_coverage(
    graph: Graph,
    markdown: str,
    *,
    require_appendix: bool = True,
) -> Tuple[bool, List[str]]:
    """Return (ok, missing_values) — every node nugget_data must appear in markdown."""
    missing: List[str] = []
    for node in graph.get("nodes", []):
        value = node_value(node)
        if not value:
            continue
        # Appendix tables escape `|` as `\|` for Markdown cell safety (R14-03).
        escaped = value.replace("|", "\\|").replace("\n", " ")
        if value not in markdown and escaped not in markdown:
            missing.append(value)
    ok = not missing
    if require_appendix and "## Appendix" not in markdown:
        ok = False
        missing.append("(appendix section missing)")
    return ok, missing
