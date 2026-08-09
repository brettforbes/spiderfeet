"""SPEC-005/014 narrative engine — centralized §4.3 report generation (modules_v2 mirror)."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

import yaml

from .meta_concept_registry import load_narrative_v2 as _load_registry
from .meta_narrative import (
    append_appendix,
    category_example_mermaid,
    category_table,
    concept_overview_mermaid,
    concept_prose,
    detect_meta_concepts,
    present_categories_under_roots,
)
from .narrative_profile import load_narrative_profile
from .narrative_report import (  # noqa: F401 — re-export coverage helpers
    Graph,
    SemanticGraph,
    node_value,
    validate_narrative_coverage,
)
from .paths import RULES_DIR, SHARED_RULES_DIR

_SHARED_RULES = SHARED_RULES_DIR
_TOOL_RULES = RULES_DIR

_MERMAID_SAFE = re.compile(r"[^A-Za-z0-9_]")


@lru_cache(maxsize=1)
def _load_narrative_v2() -> dict[str, Any]:
    try:
        return _load_registry()
    except Exception:  # noqa: BLE001
        path = _SHARED_RULES / "narrative_v2.yaml"
        if not path.is_file():
            return {}
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}


def _mermaid_id(nugget_id: str) -> str:
    return _MERMAID_SAFE.sub("_", nugget_id or "UNKNOWN")


def type_relation_mermaid(graph: dict[str, Any], *, root_ids: list[str] | None = None) -> str:
    nodes = {n["id"]: n for n in graph.get("nodes", []) if n.get("id")}
    seen: set[tuple[str, str, str]] = set()
    lines = ["```mermaid", "flowchart LR"]
    for edge in graph.get("edges", []):
        if root_ids and edge.get("source") not in nodes:
            continue
        src = nodes.get(edge.get("source", ""), {})
        tgt = nodes.get(edge.get("target", ""), {})
        src_type = _mermaid_id(str(src.get("nugget_id", "UNKNOWN")))
        rel = str(edge.get("relation", "rel")).replace(" ", "-")
        tgt_type = _mermaid_id(str(tgt.get("nugget_id", "UNKNOWN")))
        key = (src_type, rel, tgt_type)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"  {src_type} -->|{rel}| {tgt_type}")
    lines.extend(["```", ""])
    return "\n".join(lines)


def build_factual_intro(
    *,
    tool: str,
    profile: dict[str, Any] | None = None,
) -> str:
    v2 = _load_narrative_v2()
    tool_name = (profile or {}).get("tool_name") or tool.replace("_", " ").title()
    categories = ", ".join(
        v2.get("category_order")
        or ["ENVIRONMENT", "NETWORKS", "APPLICATIONS", "VULNERABILITIES"]
    )
    template = (profile or {}).get("intro_facts") or (v2.get("intro_facts") or {}).get("default") or (
        "The scan used {tool_name}. Findings are organised under category sections ({categories})."
    )
    blurb = v2.get("intro", {}).get("hierarchy_blurb", "")
    body = template.format(tool_name=tool_name, categories=categories).strip()
    return f"{body} {blurb}".strip()


def _profile_concept_allowlist(profile: dict[str, Any]) -> set[str] | None:
    raw = profile.get("meta_concepts")
    if not raw:
        return None
    return {str(item) for item in raw}


def _render_concept_section(lines: list[str], graph: dict[str, Any], concept: dict[str, Any]) -> None:
    heading = str(concept.get("heading") or concept.get("id") or "Concept")
    lines.extend([f"## {heading}", "", concept_prose(graph, concept), ""])

    overview = concept_overview_mermaid(graph, concept)
    if overview:
        lines.extend(["### Structure overview", "", overview, ""])

    render_ids = present_categories_under_roots(graph, concept)
    if concept.get("id") == "scan" and not render_ids:
        lines.extend(["### Scan descriptors", "", category_table(graph, concept, None), ""])
        return

    if not render_ids:
        lines.extend(["### Values", "", category_table(graph, concept, None), ""])
        return

    for cat in render_ids:
        table = category_table(graph, concept, cat)
        if table.strip() == "_No values._":
            continue
        lines.extend([f"### `{cat}`", ""])
        example = category_example_mermaid(graph, concept, cat)
        if example:
            lines.extend([example, ""])
        lines.extend([table, ""])


def render_narrative(
    graph: dict[str, Any],
    *,
    tool: str,
    scenario_key: str,
    profile: dict[str, Any] | None = None,
) -> str:
    tool_profile = profile or load_narrative_profile(_TOOL_RULES / tool / "narrative.yaml")
    merged = {**tool_profile, "tool_name": tool_profile.get("tool_name") or tool.title()}

    intro = (merged.get("phrasing") or {}).get("introduction") or build_factual_intro(
        tool=tool, profile=merged
    )
    lines = [
        f"# {merged.get('tool_name', tool.title())} scan narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        intro.strip(),
        "",
    ]

    allow = _profile_concept_allowlist(merged)
    concepts = detect_meta_concepts(graph)
    if allow is not None:
        concepts = [c for c in concepts if c.get("id") in allow]

    for concept in concepts:
        if concept.get("id") == "trace" and not merged.get("include_trace", True):
            continue
        _render_concept_section(lines, graph, concept)

    if not concepts:
        lines.extend(
            [
                "## Graph structure (types)",
                "",
                type_relation_mermaid(graph),
                "",
            ]
        )

    lines.extend(["## Conclusion", "", "See the appendix for the full node and edge inventory.", ""])

    if merged.get("include_appendix", True):
        append_appendix(lines, graph)

    footer = (
        merged.get("footer_brand")
        or _load_narrative_v2().get("footer", {}).get("brand", "OS-Intel Scan")
    )
    lines.extend(["---", "", f"*{footer}*", ""])
    return "\n".join(lines).strip() + "\n"
