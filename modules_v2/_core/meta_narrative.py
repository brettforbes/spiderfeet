"""SPEC-014 meta-concept progressive-disclosure narrative primitives (R14-02/04/05)."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from .meta_concept_registry import (
    get_meta_concept,
    list_meta_concepts,
    mermaid_settings,
)

_MERMAID_SAFE = re.compile(r"[^A-Za-z0-9_]")
_VALUE_LITERAL = re.compile(
    r"(?:\b\d{1,3}(?:\.\d{1,3}){3}\b|https?://|www\.|CVE-\d{4}-\d+)",
    re.IGNORECASE,
)


def _safe_id(text: str, *, index: int | None = None) -> str:
    base = _MERMAID_SAFE.sub("_", text or "NODE").strip("_") or "NODE"
    if index is None:
        return base.lower()
    return f"{base.lower()}_{index}"


def _nodes_by_id(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(n["id"]): n for n in graph.get("nodes") or [] if n.get("id")}


def _index_edges(
    graph: dict[str, Any],
) -> tuple[dict[str, list[tuple[str, str]]], dict[str, list[tuple[str, str]]]]:
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    inbound: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for edge in graph.get("edges") or []:
        src = str(edge.get("source") or "")
        tgt = str(edge.get("target") or "")
        rel = str(edge.get("relation") or "rel")
        if not src or not tgt:
            continue
        out[src].append((rel, tgt))
        inbound[tgt].append((rel, src))
    return out, inbound


def _nodes_of_types(graph: dict[str, Any], nugget_ids: list[str]) -> list[dict[str, Any]]:
    wanted = set(nugget_ids)
    return [
        n
        for n in graph.get("nodes") or []
        if n.get("nugget_id") in wanted
    ]


def detect_meta_concepts(graph: dict[str, Any]) -> list[dict[str, Any]]:
    """Return registry concepts present in the graph, ordered by registry order."""
    present_types = {str(n.get("nugget_id")) for n in graph.get("nodes") or []}
    found: list[dict[str, Any]] = []
    for concept in list_meta_concepts():
        roots = [str(x) for x in concept.get("root_nugget_ids") or []]
        if any(root in present_types for root in roots):
            found.append(concept)
    return found


def present_categories_under_roots(
    graph: dict[str, Any],
    concept: dict[str, Any],
) -> list[str]:
    nodes = _nodes_by_id(graph)
    out_edges, _ = _index_edges(graph)
    root_ids = {
        nid
        for nid, node in nodes.items()
        if node.get("nugget_id") in set(concept.get("root_nugget_ids") or [])
    }
    category_ids = [str(c) for c in concept.get("category_nugget_ids") or []]
    child_ids = [str(c) for c in concept.get("child_nugget_ids") or []]
    present: list[str] = []
    seen: set[str] = set()

    for root_id in root_ids:
        for rel, tgt in out_edges.get(root_id, []):
            tgt_node = nodes.get(tgt) or {}
            tgt_type = str(tgt_node.get("nugget_id") or "")
            if tgt_type in category_ids and tgt_type not in seen:
                seen.add(tgt_type)
                present.append(tgt_type)
            if tgt_type in child_ids and f"child:{tgt_type}" not in seen:
                seen.add(f"child:{tgt_type}")
                present.append(tgt_type)

    # Scan: expose descriptor types linked via had when no categories.
    if not present and concept.get("id") == "scan":
        for root_id in root_ids:
            for rel, tgt in out_edges.get(root_id, []):
                if rel != "had":
                    continue
                tgt_type = str((nodes.get(tgt) or {}).get("nugget_id") or "")
                if tgt_type and tgt_type not in seen:
                    seen.add(tgt_type)
                    present.append(tgt_type)

    # Fallback: categories that exist anywhere in the graph for this concept.
    if not present:
        for cat in category_ids:
            if any(n.get("nugget_id") == cat for n in graph.get("nodes") or []):
                present.append(cat)
    return present


def concept_overview_mermaid(
    graph: dict[str, Any],
    concept: dict[str, Any],
    *,
    shape_cap: int | None = None,
) -> str:
    """Type-only overview: root type -> present categories/children."""
    settings = mermaid_settings()
    cap = int(shape_cap or settings.get("shape_cap") or 12)
    roots = [str(r) for r in concept.get("root_nugget_ids") or []]
    if not roots:
        return ""
    root_type = roots[0]
    categories = present_categories_under_roots(graph, concept)
    lines = ["```mermaid", "flowchart TD"]
    node_index = 0
    declared: dict[str, str] = {}

    def declare(nugget_id: str, label: str | None = None) -> str:
        nonlocal node_index
        key = f"{nugget_id}|{label or nugget_id}"
        if key in declared:
            return declared[key]
        node_index += 1
        mid = _safe_id(nugget_id, index=node_index)
        text = label or nugget_id
        if _VALUE_LITERAL.search(text):
            raise ValueError(f"overview Mermaid must be type-only: {text!r}")
        lines.append(f'  {mid}["{text}"]')
        declared[key] = mid
        return mid

    root_mid = declare(root_type)
    shapes = 1
    for cat in categories:
        if shapes >= cap:
            more = declare("MORE", f"+{len(categories) - (shapes - 1)} more")
            lines.append(f"  {root_mid} -->|contains| {more}")
            break
        label = cat
        if concept.get("id") == "domain" and cat == "DOMAIN_NAME":
            label = "DOMAIN_NAME subdomain"
        cat_mid = declare(cat, label)
        rel = "had" if concept.get("id") == "scan" else "contains"
        lines.append(f"  {root_mid} -->|{rel}| {cat_mid}")
        shapes += 1
    if shapes == 1:
        # Root-only overview still useful.
        pass
    lines.append("```")
    return "\n".join(lines)


def _children_of_type(
    graph: dict[str, Any],
    parent_ids: set[str],
    child_nugget_id: str,
) -> list[dict[str, Any]]:
    nodes = _nodes_by_id(graph)
    out_edges, _ = _index_edges(graph)
    found: list[dict[str, Any]] = []
    seen: set[str] = set()
    for parent_id in parent_ids:
        for _rel, tgt in out_edges.get(parent_id, []):
            node = nodes.get(tgt)
            if not node or node.get("nugget_id") != child_nugget_id:
                continue
            if tgt in seen:
                continue
            seen.add(tgt)
            found.append(node)
    if not found:
        # Fallback: all nodes of that type.
        found = _nodes_of_types(graph, [child_nugget_id])
    return sorted(found, key=lambda n: str(n.get("nugget_data") or ""))


def category_example_mermaid(
    graph: dict[str, Any],
    concept: dict[str, Any],
    category_nugget_id: str,
    *,
    example_cap: int | None = None,
    shape_cap: int | None = None,
) -> str:
    """Category diagram with capped example values and a +N more affordance."""
    settings = mermaid_settings()
    cap = int(example_cap or concept.get("example_cap") or settings.get("example_cap_default") or 3)
    max_shapes = int(shape_cap or settings.get("shape_cap") or 12)

    nodes = _nodes_by_id(graph)
    root_ids = {
        nid
        for nid, node in nodes.items()
        if node.get("nugget_id") in set(concept.get("root_nugget_ids") or [])
    }
    # Instances: for category buckets, children under the category; for domain children, the children themselves.
    if category_nugget_id in set(concept.get("category_nugget_ids") or []):
        category_node_ids = {
            nid for nid, node in nodes.items() if node.get("nugget_id") == category_nugget_id
        }
        # Prefer children of category nodes; else children of roots that are not categories.
        out_edges, _ = _index_edges(graph)
        instances: list[dict[str, Any]] = []
        seen: set[str] = set()
        parents = category_node_ids or root_ids
        for parent_id in parents:
            for _rel, tgt in out_edges.get(parent_id, []):
                node = nodes.get(tgt)
                if not node:
                    continue
                if node.get("nugget_id") == category_nugget_id:
                    continue
                if tgt in seen:
                    continue
                # Keep entity/descriptor instances under the category.
                seen.add(tgt)
                instances.append(node)
        instances = sorted(instances, key=lambda n: (str(n.get("nugget_id")), str(n.get("nugget_data"))))
        parent_label = category_nugget_id
    else:
        instances = _children_of_type(graph, root_ids, category_nugget_id)
        parent_label = str((concept.get("root_nugget_ids") or ["ROOT"])[0])

    total = len(instances)
    shown = instances[:cap]
    remaining = max(0, total - len(shown))

    lines = ["```mermaid", "flowchart TD"]
    node_index = 0
    parent_mid = _safe_id(parent_label, index=1)
    node_index = 1
    lines.append(f'  {parent_mid}["{parent_label}"]')
    shapes = 1

    for inst in shown:
        if shapes >= max_shapes:
            break
        node_index += 1
        shapes += 1
        nugget_id = str(inst.get("nugget_id") or "NODE")
        value = str(inst.get("nugget_data") or "")
        # Progressive disclosure: show type + short example value.
        label = f"{nugget_id}: {_short_label(value)}"
        mid = _safe_id(nugget_id, index=node_index)
        lines.append(f'  {mid}["{label}"]')
        lines.append(f"  {parent_mid} -->|contains| {mid}")

    if remaining > 0 and shapes < max_shapes:
        node_index += 1
        more_mid = _safe_id("MORE", index=node_index)
        lines.append(f'  {more_mid}["+{remaining} more"]')
        lines.append(f"  {parent_mid} -->|contains| {more_mid}")

    lines.append("```")
    return "\n".join(lines)


def _short_label(value: str, *, limit: int = 40) -> str:
    text = value.replace('"', "'").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def category_table(
    graph: dict[str, Any],
    concept: dict[str, Any],
    category_nugget_id: str | None = None,
) -> str:
    """Markdown table of values for a category (or whole concept roots)."""
    nodes = _nodes_by_id(graph)
    if category_nugget_id:
        # Collect instances similarly to category_example_mermaid.
        root_ids = {
            nid
            for nid, node in nodes.items()
            if node.get("nugget_id") in set(concept.get("root_nugget_ids") or [])
        }
        if category_nugget_id in set(concept.get("category_nugget_ids") or []):
            category_node_ids = {
                nid for nid, node in nodes.items() if node.get("nugget_id") == category_nugget_id
            }
            out_edges, _ = _index_edges(graph)
            instances: list[dict[str, Any]] = []
            seen: set[str] = set()
            for parent_id in category_node_ids or root_ids:
                for _rel, tgt in out_edges.get(parent_id, []):
                    node = nodes.get(tgt)
                    if not node or tgt in seen:
                        continue
                    if node.get("nugget_id") == category_nugget_id:
                        continue
                    seen.add(tgt)
                    instances.append(node)
        else:
            instances = _children_of_type(graph, root_ids, category_nugget_id)
    else:
        instances = _nodes_of_types(graph, [str(r) for r in concept.get("root_nugget_ids") or []])

    instances = sorted(instances, key=lambda n: (str(n.get("nugget_id")), str(n.get("nugget_data"))))
    if not instances:
        return "_No values._"

    lines = [
        "| Nugget | Value |",
        "| --- | --- |",
    ]
    for node in instances:
        lines.append(
            f"| `{node.get('nugget_id')}` | `{_escape_cell(str(node.get('nugget_data') or ''))}` |"
        )
    return "\n".join(lines)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def concept_prose(graph: dict[str, Any], concept: dict[str, Any]) -> str:
    """Short story with counts and representative values."""
    roots = _nodes_of_types(graph, [str(r) for r in concept.get("root_nugget_ids") or []])
    root_count = len(roots)
    sample = ", ".join(f"`{n.get('nugget_data')}`" for n in roots[:3])
    base = str(concept.get("prose") or "").strip()
    categories = present_categories_under_roots(graph, concept)
    cat_text = ", ".join(f"`{c}`" for c in categories[:6]) or "no child categories"
    parts = [base] if base else []
    heading = concept.get("heading") or concept.get("id")
    if root_count:
        parts.append(f"This scan includes **{root_count}** {heading} root node(s)")
        if sample:
            parts[-1] += f" (e.g. {sample})"
        parts[-1] += "."
    else:
        parts.append(f"No {heading} root nodes were present.")
    parts.append(f"Linked structures: {cat_text}.")
    return " ".join(p for p in parts if p)


def append_appendix(lines: list[str], graph: dict[str, Any]) -> None:
    """Append deduped node + edge inventory (fixes duplicate-edge recital)."""
    nodes = list(graph.get("nodes") or [])
    edges = list(graph.get("edges") or [])
    by_id = {str(n["id"]): n for n in nodes if n.get("id")}

    lines.extend(["", "## Appendix", "", "### Nodes", ""])
    lines.extend(
        [
            "| Nugget | Value |",
            "| --- | --- |",
        ]
    )
    seen_nodes: set[tuple[str, str]] = set()
    for node in sorted(nodes, key=lambda n: (str(n.get("nugget_id")), str(n.get("nugget_data")))):
        key = (str(node.get("nugget_id")), str(node.get("nugget_data")))
        if key in seen_nodes:
            continue
        seen_nodes.add(key)
        lines.append(
            f"| `{key[0]}` | `{_escape_cell(key[1])}` |"
        )

    lines.extend(["", "### Edges", ""])
    lines.extend(
        [
            "| Source | Relation | Target |",
            "| --- | --- | --- |",
        ]
    )
    seen_edges: set[tuple[str, str, str]] = set()
    for edge in edges:
        src = by_id.get(str(edge.get("source")), {})
        tgt = by_id.get(str(edge.get("target")), {})
        key = (
            str(src.get("nugget_id") or ""),
            str(edge.get("relation") or ""),
            str(tgt.get("nugget_id") or ""),
        )
        if not key[0] or not key[2] or key in seen_edges:
            continue
        seen_edges.add(key)
        lines.append(f"| `{key[0]}` | `{key[1]}` | `{key[2]}` |")


def count_mermaid_shapes(mermaid_block: str) -> int:
    """Count declared node lines inside a mermaid fence."""
    body = mermaid_block
    if "```" in body:
        parts = body.split("```")
        body = parts[1] if len(parts) > 1 else body
        if body.lstrip().startswith("mermaid"):
            body = body.lstrip()[len("mermaid") :]
    return sum(1 for line in body.splitlines() if re.search(r'^\s+\w+\["', line))
