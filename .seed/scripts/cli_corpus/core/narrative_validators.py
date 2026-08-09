"""SPEC-014 narrative validators (R14-08)."""

from __future__ import annotations

import re
from typing import Any

from core.meta_concept_registry import mermaid_settings
from core.meta_narrative import count_mermaid_shapes, detect_meta_concepts
from narrative_report import validate_narrative_coverage

_H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
_MERMAID = re.compile(r"```mermaid\n(.*?)```", re.S)
_VALUE_LITERAL = re.compile(
    r"(?:\b\d{1,3}(?:\.\d{1,3}){3}\b|https?://|www\.|CVE-\d{4}-\d+)",
    re.IGNORECASE,
)
_MORE = re.compile(r"\+\d+\s+more", re.IGNORECASE)


def validate_meta_concept_coverage(graph: dict[str, Any], markdown: str) -> list[str]:
    """Every present meta-concept needs a heading + overview Mermaid when roots exist."""
    problems: list[str] = []
    concepts = detect_meta_concepts(graph)
    headings = {h.strip().lower() for h in _H2.findall(markdown)}
    for concept in concepts:
        heading = str(concept.get("heading") or concept.get("id") or "").strip()
        if heading.lower() not in headings:
            problems.append(f"missing section heading for meta-concept {concept.get('id')!r} ({heading})")
            continue
        # Slice section body until next H2
        pattern = re.compile(
            rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s|\Z)",
            re.M,
        )
        match = pattern.search(markdown)
        body = match.group(1) if match else ""
        if "```mermaid" not in body and concept.get("id") != "scan":
            # Scan may be descriptor-only; still prefer overview when present in engine
            if any(n.get("nugget_id") in (concept.get("root_nugget_ids") or []) for n in graph.get("nodes") or []):
                problems.append(f"meta-concept {concept.get('id')!r} missing overview Mermaid")
        elif "```mermaid" not in body and concept.get("id") == "scan":
            if "### Structure overview" not in body and "```mermaid" not in body:
                problems.append("scan section missing overview Mermaid")
    return problems


def validate_mermaid_shape_cap(markdown: str, *, max_shapes: int | None = None) -> list[str]:
    """Fail when any Mermaid block exceeds the registry shape cap."""
    cap = int(max_shapes or mermaid_settings().get("shape_cap") or 12)
    problems: list[str] = []
    for idx, block in enumerate(_MERMAID.findall(markdown), start=1):
        shapes = count_mermaid_shapes("```mermaid\n" + block + "\n```")
        if shapes > cap:
            problems.append(f"mermaid#{idx} has {shapes} shapes (cap {cap})")
    return problems


def validate_mermaid_overview_type_only(markdown: str) -> list[str]:
    """Overview diagrams (no value labels with ':') must stay type-only."""
    problems: list[str] = []
    pre = markdown.split("## Appendix")[0] if "## Appendix" in markdown else markdown
    # Structure overview blocks sit under ### Structure overview
    sections = re.split(r"^###\s+Structure overview\s*$", pre, flags=re.M)
    for chunk in sections[1:]:
        blocks = _MERMAID.findall(chunk.split("###", 1)[0])
        for block in blocks:
            if _VALUE_LITERAL.search(block):
                problems.append("overview Mermaid contains value literal (must be type-only)")
    return problems


def validate_example_cap_and_table(
    graph: dict[str, Any],
    markdown: str,
    *,
    example_cap: int | None = None,
) -> list[str]:
    """Category example diagrams must not exceed example_cap without +N more; tables list values."""
    settings = mermaid_settings()
    default_cap = int(example_cap or settings.get("example_cap_default") or 3)
    problems: list[str] = []
    # Heuristic: count value-labelled nodes (contain ':') per example Mermaid under ### `CAT`
    for match in re.finditer(r"^###\s+`([^`]+)`\s*$([\s\S]*?)(?=^###\s|^##\s|\Z)", markdown, re.M):
        cat = match.group(1)
        body = match.group(2)
        blocks = _MERMAID.findall(body)
        if not blocks:
            # Category subsection without diagram is ok when table empty
            continue
        for block in blocks:
            value_labels = re.findall(r'\["([^"]+:\s*[^"]+)"\]', block)
            if len(value_labels) > default_cap and not _MORE.search(block):
                problems.append(
                    f"category {cat}: {len(value_labels)} example values without +N more (cap {default_cap})"
                )
        if "| Nugget | Value |" not in body and "| Nugget | Value |" not in body.replace(" ", ""):
            if "| Nugget |" not in body:
                problems.append(f"category {cat}: missing value table")
    del graph  # reserved for stricter instance counting later
    return problems


def validate_appendix_dedupe(markdown: str) -> list[str]:
    """Appendix edge inventory must appear once; no duplicate edge rows."""
    problems: list[str] = []
    edge_headers = markdown.count("### Edges")
    if edge_headers == 0 and "## Appendix" in markdown:
        problems.append("appendix missing ### Edges")
    elif edge_headers > 1:
        problems.append(f"appendix ### Edges repeated {edge_headers} times")
    if "## Appendix" not in markdown:
        return problems
    appendix = markdown.split("## Appendix", 1)[1]
    edge_section = appendix.split("### Edges", 1)[-1] if "### Edges" in appendix else ""
    rows = [
        line.strip()
        for line in edge_section.splitlines()
        if line.strip().startswith("|") and "---" not in line and "Source" not in line
    ]
    if len(rows) != len(set(rows)):
        problems.append("appendix contains duplicate edge rows")
    return problems


def validate_narrative_report(graph: dict[str, Any], markdown: str) -> list[str]:
    """Run the full SPEC-014 narrative validator suite."""
    problems: list[str] = []
    ok, missing = validate_narrative_coverage(graph, markdown)
    if not ok:
        problems.append(f"coverage missing: {missing[:8]}")
    problems.extend(validate_meta_concept_coverage(graph, markdown))
    problems.extend(validate_mermaid_shape_cap(markdown))
    problems.extend(validate_mermaid_overview_type_only(markdown))
    problems.extend(validate_example_cap_and_table(graph, markdown))
    problems.extend(validate_appendix_dedupe(markdown))
    return problems
