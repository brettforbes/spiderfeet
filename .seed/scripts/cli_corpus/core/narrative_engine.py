"""SPEC-005 narrative engine v2 — centralized §4.3 report generation."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from core.narrative_profile import append_standard_appendix, load_narrative_profile
from narrative_report import (  # noqa: F401 — re-export compat shim source
    Graph,
    NarrativeConfig,
    NarrativeReportBuilder,
    NetdiscoverNarrativeReportBuilder,
    SemanticGraph,
    build_narrative_report,
    build_netdiscover_narrative_report,
    build_nmap_narrative_report,
    node_value,
    validate_narrative_coverage,
)

_CORPUS_DIR = Path(__file__).resolve().parents[1]
_SHARED_RULES = _CORPUS_DIR / "rules" / "_shared"
_TOOL_RULES = _CORPUS_DIR / "rules"

_MERMAID_SAFE = re.compile(r"[^A-Za-z0-9_]")


@lru_cache(maxsize=1)
def _load_narrative_v2() -> dict[str, Any]:
    path = _SHARED_RULES / "narrative_v2.yaml"
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _mermaid_id(nugget_id: str) -> str:
    return _MERMAID_SAFE.sub("_", nugget_id or "UNKNOWN")


def type_relation_mermaid(graph: dict[str, Any], *, root_ids: list[str] | None = None) -> str:
    """Project unique ontology edges as type→relation→type (no literal values)."""
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
    """Build a factual introduction from shared v2 YAML and tool profile."""
    v2 = _load_narrative_v2()
    tool_name = (profile or {}).get("tool_name") or tool.replace("_", " ").title()
    categories = ", ".join(v2.get("category_order") or ["ENVIRONMENT", "NETWORKS", "APPLICATIONS", "VULNERABILITIES"])
    template = (profile or {}).get("intro_facts") or (v2.get("intro_facts") or {}).get("default") or (
        "The scan used {tool_name}. Findings are organised under category sections ({categories})."
    )
    blurb = v2.get("intro", {}).get("hierarchy_blurb", "")
    body = template.format(tool_name=tool_name, categories=categories).strip()
    return f"{body} {blurb}".strip()


def _config_from_profile(tool: str, profile: dict[str, Any]) -> NarrativeConfig:
    v2 = _load_narrative_v2()
    footer = (v2.get("footer") or {}).get("brand", "OS-Intel Scan")
    host_id = profile.get("host_nugget_id") or profile.get("host_entity") or "HOST"
    return NarrativeConfig(
        tool_name=profile.get("tool_name") or tool.title(),
        scan_nugget_id=profile.get("scan_nugget_id", "SCAN_RECORD"),
        host_nugget_id=host_id,
        trace_nugget_id=profile.get("trace_nugget_id", "TRACE"),
        environment_category=profile.get("environment_category", "ENVIRONMENT"),
        networks_category=profile.get("networks_category", "NETWORKS"),
        applications_category=profile.get("applications_category", "APPLICATIONS"),
        vulnerabilities_category=profile.get("vulnerabilities_category", "VULNERABILITIES"),
        footer_brand=profile.get("footer_brand", footer),
    )


def _section_heading(section: str) -> str:
    return {
        "hosts": "Hosts",
        "systems": "Systems",
        "findings": "Findings",
        "organization": "Organization",
        "domains": "Domains",
        "urls": "URLs",
        "cdn_fronting": "CDN / edge fronting",
        "services": "Services",
    }.get(section, section.replace("_", " ").title())


def _render_profile_section(
    lines: list[str],
    section: str,
    graph: dict[str, Any],
    profile: dict[str, Any],
) -> None:
    nodes = graph.get("nodes") or []
    phrasing = profile.get("phrasing") or {}
    if section in {"introduction", "appendix"}:
        return
    heading = _section_heading(section)
    lines.extend([f"## {heading}", ""])
    if section == "systems":
        for node in sorted(
            (n for n in nodes if n.get("nugget_id") in {"HOST", "CDN", "SYSTEM"}),
            key=lambda n: (n.get("nugget_id", ""), n.get("nugget_data", "")),
        ):
            lines.append(f"- `{node.get('nugget_id')}` `{node.get('nugget_data')}`")
        if not any(n.get("nugget_id") in {"HOST", "CDN", "SYSTEM"} for n in nodes):
            lines.append("- (none)")
    elif section == "cdn_fronting":
        if any(n.get("nugget_id") == "CDN" for n in nodes):
            lines.append((phrasing.get("fronted_unknown") or "").strip())
            lines.append("")
            lines.append(
                f"Origin host count is **{phrasing.get('indeterminate_origin_count', 'indeterminate')}**."
            )
        else:
            lines.append((phrasing.get("standard_host") or "No CDN fronting detected.").strip())
    elif section == "services":
        services = [n for n in nodes if n.get("nugget_id") == "SERVICE"]
        for service in services:
            lines.append(f"- `{service.get('nugget_data')}`")
        if not services:
            lines.append("- (none)")
    elif section == "organization":
        companies = [n for n in nodes if n.get("nugget_id") == "COMPANY_NAME"]
        for company in companies:
            lines.append(f"- `{company.get('nugget_data')}`")
        if not companies:
            lines.append("- (no head company node)")
    elif section == "domains":
        domains = [n for n in nodes if n.get("nugget_id") == "DOMAIN_NAME"]
        for domain in sorted(domains, key=lambda n: str(n.get("nugget_data"))):
            lines.append(f"- `{domain.get('nugget_data')}`")
        if not domains:
            lines.append("- (none)")
    elif section == "hosts":
        hosts = [n for n in nodes if n.get("nugget_id") == "HOST"]
        for host in sorted(hosts, key=lambda n: str(n.get("nugget_data"))):
            lines.append(f"- `{host.get('nugget_data')}`")
        if not hosts:
            lines.append("- (none)")
    elif section == "findings":
        findings = [n for n in nodes if n.get("nugget_id") in {"NUCLEI_FINDING", "VULNERABILITY_GENERAL"}]
        for finding in sorted(findings, key=lambda n: str(n.get("nugget_data"))):
            lines.append(f"- `{finding.get('nugget_data')}`")
        if not findings:
            lines.append("- (none)")
    elif section == "urls":
        urls = [n for n in nodes if n.get("nugget_id") == "LINKED_URL_INTERNAL"]
        for url in sorted(urls, key=lambda n: str(n.get("nugget_data"))):
            lines.append(f"- `{url.get('nugget_data')}`")
        if not urls:
            lines.append("- (none)")
    else:
        lines.append(f"_Section `{section}` — see appendix for values._")
    lines.append("")


def render_narrative(
    graph: dict[str, Any],
    *,
    tool: str,
    scenario_key: str,
    profile: dict[str, Any] | None = None,
) -> str:
    """Render Markdown narrative using tool YAML profile + shared v2 engine."""
    tool_profile = profile or load_narrative_profile(_TOOL_RULES / tool / "narrative.yaml")
    merged = {**tool_profile, "tool_name": tool_profile.get("tool_name") or tool.title()}

    if tool == "nmap":
        return build_nmap_narrative_report(graph, scenario_key)
    if tool == "netdiscover":
        return build_netdiscover_narrative_report(graph, scenario_key)

    # Generic v2 path: factual intro + YAML sections + type mermaid + appendix
    intro = (merged.get("phrasing") or {}).get("introduction") or build_factual_intro(tool=tool, profile=merged)
    lines = [
        f"# {merged.get('tool_name', tool.title())} scan narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        intro.strip(),
        "",
    ]
    for section in merged.get("sections") or ["systems"]:
        _render_profile_section(lines, str(section), graph, merged)
    lines.extend(["## Graph structure (types)", "", type_relation_mermaid(graph)])
    if merged.get("include_trace", True):
        lines.extend(["## Trace", "", "_Trace section omitted when no TRACE nodes present._", ""])
    if merged.get("include_appendix", True):
        append_standard_appendix(lines, graph)
    footer = (merged.get("footer_brand") or _load_narrative_v2().get("footer", {}).get("brand", "OS-Intel Scan"))
    lines.extend(["---", "", f"*{footer}*", ""])
    return "\n".join(lines).strip() + "\n"
