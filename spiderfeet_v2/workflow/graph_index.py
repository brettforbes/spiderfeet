"""Adjacency index for SpiderFeet scan graphs."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Dict, List, Set


Relation = str


class GraphIndex:
    def __init__(self, graph: Dict[str, Any]):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.out: Dict[str, Dict[Relation, List[str]]] = defaultdict(lambda: defaultdict(list))
        self.inn: Dict[str, Dict[Relation, List[str]]] = defaultdict(lambda: defaultdict(list))
        for node in graph.get("nodes") or []:
            nid = node.get("id") or node.get("nugget_instance_id")
            if not nid:
                continue
            self.nodes[nid] = node
        for edge in graph.get("edges") or []:
            src, tgt, rel = edge.get("source"), edge.get("target"), edge.get("relation")
            if not src or not tgt or not rel:
                continue
            self.out[src][rel].append(tgt)
            self.inn[tgt][rel].append(src)

    def neighbors(self, node_id: str, relation: Relation, direction: str = "out") -> List[str]:
        table = self.out if direction == "out" else self.inn
        return list(table.get(node_id, {}).get(relation, []))

    def reachable(
        self,
        start_id: str,
        relation: Relation,
        *,
        transitive: bool = False,
        direction: str = "out",
    ) -> Set[str]:
        direct = self.neighbors(start_id, relation, direction)
        if not transitive:
            return set(direct)
        seen: Set[str] = set()
        q: deque[str] = deque(direct)
        while q:
            cur = q.popleft()
            if cur in seen:
                continue
            seen.add(cur)
            for nxt in self.neighbors(cur, relation, direction):
                if nxt not in seen:
                    q.append(nxt)
        return seen


def empty_graph() -> Dict[str, List[Any]]:
    return {"nodes": [], "edges": []}
