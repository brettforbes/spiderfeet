"""SPEC-006 structure documentation engine — YAML packs to Nmap-quality Markdown."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_CORPUS_DIR = Path(__file__).resolve().parents[1]
_REPO_ROOT = _CORPUS_DIR.parents[2]
_SHARED_STRUCTURE = _CORPUS_DIR / "rules" / "_shared" / "structure_v1.yaml"
_RULES_DIR = _CORPUS_DIR / "rules"
_STRUCTURE_OUTPUT_DIR = _REPO_ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
_ONTOLOGY_PATH = _REPO_ROOT / ".docs" / "docs-for-cli-tools" / "_Current_Ontology.md"

ADAPTER_TOOLS: tuple[str, ...] = (
    "nmap",
    "netdiscover",
    "nerva",
    "pius",
    "subfinder",
    "httpx",
    "katana",
    "nuclei",
)

_MERMAID_SAFE = re.compile(r"[^A-Za-z0-9_]")
_VALUE_LITERAL = re.compile(
    r"(?:\b\d{1,3}(?:\.\d{1,3}){3}\b|https?://|www\.|CVE-\d{4}-\d+)",
    re.IGNORECASE,
)

_REQUIRED_HEADINGS = (
    "Scan head",
    "Scenario coverage",
    "Field mapping",
    "Review notes",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


@lru_cache(maxsize=1)
def load_shared_structure_patterns() -> dict[str, Any]:
    data = _load_yaml(_SHARED_STRUCTURE)
    patterns = data.get("patterns") or {}
    return patterns if isinstance(patterns, dict) else {}


def load_tool_structure_pack(tool_id: str) -> dict[str, Any]:
    path = _RULES_DIR / tool_id / "structure.yaml"
    pack = _load_yaml(path)
    if pack.get("tool") and pack["tool"] != tool_id:
        raise ValueError(f"structure.yaml tool={pack['tool']!r} does not match {tool_id!r}")
    return pack


def _mermaid_node_id(nugget_id: str, *, index: int) -> str:
    base = _MERMAID_SAFE.sub("_", nugget_id or "UNKNOWN").strip("_") or "NODE"
    return f"{base.lower()}_{index}"


def _node_label(nugget_id: str, override: str | None = None) -> str:
    return override or nugget_id


def render_mermaid_from_pattern(pattern: dict[str, Any]) -> str:
    """Render a type-only flowchart TD from a structure_v1 pattern."""
    edges = pattern.get("edges") or []
    if not edges:
        return ""

    node_by_key: dict[tuple[str, str | None], str] = {}
    mermaid_edges: list[str] = []
    node_index = 0

    def ensure_node(nugget_id: str, label_override: str | None = None) -> str:
        nonlocal node_index
        key = (nugget_id, label_override)
        existing = node_by_key.get(key)
        if existing:
            return existing
        node_index += 1
        node_id = _mermaid_node_id(nugget_id, index=node_index)
        label = _node_label(nugget_id, label_override)
        if _VALUE_LITERAL.search(label):
            raise ValueError(f"Mermaid label must be type-only: {label!r}")
        node_by_key[key] = node_id
        return node_id

    lines = ["```mermaid", "flowchart TD"]
    for edge in edges:
        source_id = str(edge.get("source", ""))
        target_id = str(edge.get("target", ""))
        relation = str(edge.get("relation", "rel"))
        src = ensure_node(source_id, edge.get("source_label"))
        tgt = ensure_node(target_id, edge.get("target_label"))
        mermaid_edges.append((src, relation, tgt, source_id, target_id, edge.get("source_label"), edge.get("target_label")))

    declared: set[str] = set()
    for src, relation, tgt, source_id, target_id, src_label, tgt_label in mermaid_edges:
        for node_id, nugget_id, label_override in (
            (src, source_id, src_label),
            (tgt, target_id, tgt_label),
        ):
            if node_id in declared:
                continue
            declared.add(node_id)
            label = _node_label(nugget_id, label_override)
            lines.append(f'  {node_id}["{label}"]')
    for src, relation, tgt, *_ in mermaid_edges:
        lines.append(f"  {src} -->|{relation}| {tgt}")
    lines.append("```")
    return "\n".join(lines)


def _render_header(pack: dict[str, Any]) -> str:
    display = pack.get("display_name") or pack.get("tool", "Tool").title()
    lines = [
        f"# {display} — proposed nugget graph structure",
        "",
    ]
    seed_docs = pack.get("seed_docs") or []
    if seed_docs:
        seed_text = " · ".join(f"`{doc}`" for doc in seed_docs)
        lines.append(f"Ontology source: {seed_text}.")
    generator = pack.get("generator")
    if generator:
        lines.append(f"Generator: `{generator}`")
    artifacts = pack.get("artifacts") or {}
    if artifacts:
        graph_pat = artifacts.get("graph", "<tool>_<scenario_id>_proposed_nuggets_edges.json")
        narrative_pat = artifacts.get("narrative", "<tool>_<scenario_id>_proposed_nuggets_edges_description.md")
        out_dir = artifacts.get("output_dir", ".docs/docs-for-cli-tools/nugget_structure")
        lines.append(
            f"Artifacts: `{graph_pat}` and narrative `{narrative_pat}` in `{out_dir}`."
        )
    lines.append("")
    narrative = pack.get("narrative")
    if narrative:
        lines.extend(
            [
                "## Narrative reports (§4.3)",
                "",
                (
                    "Graph JSON is converted to readable OSINT Markdown by "
                    f"`{narrative.get('engine', 'core/narrative_engine.py')}` "
                    f"via `{narrative.get('method', 'render_narrative')}()`. "
                    "Reports follow scan → endpoint categories → appendix; "
                    "`validate_narrative_coverage()` enforces full value inventory in tests."
                ),
                "",
            ]
        )
    return "\n".join(lines)


def _render_pattern_section(
    section: dict[str, Any],
    shared_patterns: dict[str, Any],
) -> str:
    pattern_id = section.get("id") or section.get("pattern")
    if not pattern_id:
        return ""
    pattern = dict(shared_patterns.get(pattern_id) or {})
    title = section.get("title") or pattern.get("title") or pattern_id.replace("_", " ").title()
    prose = section.get("prose") or pattern.get("prose") or ""
    bullets = section.get("bullets") or []

    lines = [f"## {title}", ""]
    if prose:
        lines.append(str(prose).strip())
        lines.append("")
    mermaid = render_mermaid_from_pattern(pattern)
    if mermaid:
        lines.append(mermaid)
        lines.append("")
    for bullet in bullets:
        lines.append(f"- {bullet}")
    if bullets:
        lines.append("")
    return "\n".join(lines)


def _render_specialty_sections(
    sections: list[dict[str, Any]] | None,
    shared_patterns: dict[str, Any],
) -> str:
    if not sections:
        return ""
    chunks: list[str] = []
    for section in sections:
        chunk = _render_pattern_section(section, shared_patterns)
        if chunk:
            chunks.append(chunk)
    return "\n".join(chunks)


def _render_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return ""
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _render_scenarios(pack: dict[str, Any]) -> str:
    scenarios = pack.get("scenarios") or []
    if not scenarios:
        return ""
    headers = ["Scenario key", "Primary structures"]
    if any(s.get("notes") for s in scenarios):
        headers.append("Notes")
    rows: list[list[str]] = []
    for scenario in scenarios:
        row = [
            str(scenario.get("id", "")),
            str(scenario.get("structures", "")),
        ]
        if len(headers) == 3:
            row.append(str(scenario.get("notes", "")))
        rows.append(row)
    lines = [
        "## Scenario coverage",
        "",
        _render_table(headers, rows),
        "",
    ]
    return "\n".join(lines)


def _render_field_mapping(pack: dict[str, Any]) -> str:
    mappings = pack.get("field_mapping") or []
    if not mappings:
        return ""
    headers = ["Structured path", "Nugget"]
    if any(m.get("notes") for m in mappings):
        headers.append("Notes")
    rows: list[list[str]] = []
    for mapping in mappings:
        row = [
            str(mapping.get("path", "")),
            str(mapping.get("nugget_id", "")),
        ]
        if len(headers) == 3:
            row.append(str(mapping.get("notes", "")))
        rows.append(row)
    lines = [
        "## Field mapping (structured → nugget)",
        "",
        _render_table(headers, rows),
        "",
    ]
    return "\n".join(lines)


def _render_proposed_nuggets(pack: dict[str, Any]) -> str:
    nuggets = pack.get("proposed_nuggets") or []
    if not nuggets:
        return ""
    rows = [
        [
            str(item.get("nugget_id", "")),
            str(item.get("type", "")),
            str(item.get("parent", "")),
            str(item.get("source", "")),
            str(item.get("relation", "")),
        ]
        for item in nuggets
    ]
    lines = [
        "## Proposed nuggets",
        "",
        _render_table(["Nugget", "Type", "Parent", "Source", "Relation"], rows),
        "",
        "Canonical vocabulary: `.docs/analysis/nuggets.json` and `.docs/analysis/nuggets_extension.json`. "
        f"Combined cross-tool view: [{pack.get('cross_link', '../_Current_Ontology.md')}]({pack.get('cross_link', '../_Current_Ontology.md')}).",
        "",
    ]
    return "\n".join(lines)


def _render_review_notes(pack: dict[str, Any]) -> str:
    notes = pack.get("review_notes") or []
    if not notes:
        notes = ["Relations use ontology vocabulary: `contains`, `had`, `listens-to`."]
    lines = ["## Review notes", ""]
    for note in notes:
        lines.append(f"- {note}")
    cross = pack.get("cross_link", "../_Current_Ontology.md")
    lines.extend(["", f"Combined cross-tool view: [{cross}]({cross}).", ""])
    return "\n".join(lines)


def render_tool_structure_doc(tool_id: str) -> str:
    """Render a tool Structure Markdown document from YAML packs."""
    pack = load_tool_structure_pack(tool_id)
    shared_patterns = load_shared_structure_patterns()
    parts = [_render_header(pack)]

    for section in pack.get("patterns") or []:
        parts.append(_render_pattern_section(section, shared_patterns))

    parts.append(_render_specialty_sections(pack.get("specialty_sections"), shared_patterns))
    parts.append(_render_scenarios(pack))
    parts.append(_render_proposed_nuggets(pack))
    parts.append(_render_field_mapping(pack))
    parts.append(_render_review_notes(pack))

    return "\n".join(part for part in parts if part).rstrip() + "\n"


def structure_doc_path(tool_id: str) -> Path:
    return _STRUCTURE_OUTPUT_DIR / f"{tool_id}_nugget_graph_structure.md"


def write_tool_structure_doc(tool_id: str, *, dry_run: bool = False) -> Path:
    content = render_tool_structure_doc(tool_id)
    path = structure_doc_path(tool_id)
    if dry_run:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _tool_subgraph_table_row(tool_id: str, pack: dict[str, Any]) -> str:
    display = pack.get("display_name") or tool_id.title()
    generator = pack.get("generator", f"adapters/{tool_id}")
    doc_name = f"{tool_id}_nugget_graph_structure.md"
    return (
        f"| **{display}** | implemented | "
        f"[{doc_name}](nugget_structure/{doc_name}) | `{generator}` |"
    )


def _render_tool_subgraph_section(tool_id: str, pack: dict[str, Any], shared_patterns: dict[str, Any]) -> str:
    display = pack.get("display_name") or tool_id.title()
    lines = [
        f"## Sub-graph: {display}",
        "",
        f"*{display} contributes validated nodes and edges via `{pack.get('generator', f'adapters/{tool_id}')}`. "
        "See the per-tool Structure doc for field tables and scenario coverage.*",
        "",
    ]
    pattern_ids: list[str] = []
    for section in pack.get("patterns") or []:
        pid = section.get("id") or section.get("pattern")
        if pid and pid != "scan_head":
            pattern_ids.append(pid)
    for section in pack.get("specialty_sections") or []:
        pid = section.get("pattern")
        if pid and pid not in pattern_ids:
            pattern_ids.append(pid)

    for pid in pattern_ids[:3]:
        pattern = shared_patterns.get(pid) or {}
        title = pattern.get("title") or pid.replace("_", " ").title()
        lines.append(f"### {title}")
        lines.append("")
        prose = pattern.get("prose")
        if prose:
            lines.append(str(prose).strip())
            lines.append("")
        mermaid = render_mermaid_from_pattern(pattern)
        if mermaid:
            lines.append(mermaid)
            lines.append("")

    cross = pack.get("cross_link", f"nugget_structure/{tool_id}_nugget_graph_structure.md")
    if cross.startswith("../"):
        cross = cross.removeprefix("../")
    lines.append(f"Full Structure doc: [{tool_id}_nugget_graph_structure.md]({cross}).")
    lines.append("")
    return "\n".join(lines)


def _ontology_unified_prefix() -> str:
    return """# Current CLI Profiling Ontology

Living summary of the **unified** nugget graph model built incrementally from CLI application profiling. Individual tools each contribute **sub-graphs** — validated slices of the same ontology — that **compose** into one semantic investigation graph. Start here for the full-extent vocabulary; drill into per-tool structure docs and generators when implementing parsers.

"""


def _ontology_unified_intro() -> str:
    return """Canonical seed: `.seed/05_Onotology_for_Nuggets.md` · Vocabulary: `.docs/analysis/nuggets.json` + `.docs/analysis/nuggets_extension.json` · Correlation: `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md`

---

## Unified model (full extent)

Every profiled CLI app emits a graph that **plugs into** the same top-level shape:

```mermaid
flowchart TD
  scan["SCAN_RECORD"]
  endpoint["Endpoint entity"]
  cat["Category nuggets"]
  desc["Descriptor nuggets"]
  scan -->|contains| endpoint
  scan -->|had| desc
  endpoint -->|contains| cat
  endpoint -->|had| desc
  cat -->|contains| desc
```

| Layer | Role | Shared across tools |
|-------|------|---------------------|
| **Scan head** | One `SCAN_RECORD` per examination run; tool-specific metadata as `had` descriptors | Always |
| **Endpoint** | `SYSTEM`, `HOST`, `DEVICE`, `MOBILE`, `SERVER`, `CDN`, `DOMAIN_NAME`, `COMPANY_NAME`, … | Variant per evidence |
| **Categories** | `NETWORKS`, `APPLICATIONS`, `ENVIRONMENT`, `VULNERABILITIES`, `SECURITY`, … | As evidence allows |
| **Facts** | Descriptor nuggets linked via `had` or nested `contains` | As evidence allows |

**Composition rule:** later scans **add** nodes and edges to the same investigation; they do not define a parallel ontology.

---

## Relations (global)

| Relation | Direction | Meaning |
|----------|-----------|---------|
| `contains` | parent → child | Structural ownership |
| `had` | entity → descriptor | Attribute fact on a node |
| `listens-to` | service → port | Application service associated with a transport port |

Instance ids use `nugget_id--uuid5(ontology_seed, nugget_data)` — see `core/graph_builder.py`.

---

## System qualification hierarchy

Endpoint subclass is a qualification decision within the unified model. ARP-level scans emit **`SYSTEM`**; port/service scans justify **`HOST`** or **`CDN`**; org tools emit **`COMPANY_NAME`** and **`DOMAIN_NAME`** trees.

```mermaid
flowchart TB
  system["SYSTEM"]
  host["HOST"]
  cdn["CDN"]
  company["COMPANY_NAME"]
  domain["DOMAIN_NAME"]
  system --> host
  system --> cdn
```

| Depth | Typical tools | Endpoint | Categories typically present |
|-------|---------------|----------|------------------------------|
| L2 / ARP | Netdiscover | `SYSTEM` | `NETWORKS` → IP/MAC |
| L3 + ports | Nmap, Nerva | `HOST` / `CDN` | `NETWORKS`, `APPLICATIONS` |
| DNS / org | Subfinder, Pius | `DOMAIN_NAME`, `COMPANY_NAME` | domain descriptors, netblocks |
| Web probe | httpx, Katana | `HOST` / `CDN` | `APPLICATIONS`, URL entities |
| Vuln scan | Nuclei | `HOST` | `SECURITY` → `FINDINGS` |

---

"""


def _ontology_composition_suffix() -> str:
    return """## Composing sub-graphs

The **investigation graph** is the union of contributed sub-graphs, correlated by shared keys (`IP_ADDRESS`, `INTERNET_NAME` / `DOMAIN_NAME`, URLs, findings):

```mermaid
flowchart LR
  sf["Subfinder\nDOMAIN_NAME"]
  hx["httpx\nweb probe"]
  ka["Katana\ncrawl URLs"]
  nm["Nmap\nHOST + SERVICE"]
  nv["Nerva\nfingerprint"]
  nu["Nuclei\nFINDINGS"]
  sf --> hx --> ka
  nm --> nv --> nu
  sf -.->|"hostname correlates"| nm
```

Shallow discovery leaves provisional endpoints until deeper sub-graphs justify reclassification.

---

## Expansion policy

- Prefer **extending** the unified model over forking per-tool ontologies.
- Keep each Mermaid diagram focused (≤12 nodes where possible).
- Document parser mappings in per-tool `*_nugget_graph_structure.md`; keep this file as the composed view.
- Regenerate via `render_structure_docs.py --ontology` after structure pack changes.

"""


def render_ontology_doc() -> str:
    """Compose _Current_Ontology.md from unified sections and tool structure packs."""
    shared_patterns = load_shared_structure_patterns()
    table_rows: list[str] = []
    tool_sections: list[str] = []

    for tool_id in ADAPTER_TOOLS:
        pack = load_tool_structure_pack(tool_id)
        table_rows.append(_tool_subgraph_table_row(tool_id, pack))
        tool_sections.append(_render_tool_subgraph_section(tool_id, pack, shared_patterns))

    table = "\n".join(
        [
            "| Sub-graph (tool) | Status | Structure doc | Generator |",
            "|------------------|--------|---------------|-----------|",
            *table_rows,
            "",
        ]
    )

    parts = [
        _ontology_unified_prefix(),
        table,
        _ontology_unified_intro(),
        "\n".join(tool_sections),
        _ontology_composition_suffix(),
    ]
    return "\n".join(parts).rstrip() + "\n"


def write_ontology_doc(*, dry_run: bool = False) -> Path:
    content = render_ontology_doc()
    if dry_run:
        return _ONTOLOGY_PATH
    _ONTOLOGY_PATH.parent.mkdir(parents=True, exist_ok=True)
    _ONTOLOGY_PATH.write_text(content, encoding="utf-8")
    return _ONTOLOGY_PATH


def validate_mermaid_purity(markdown: str) -> list[str]:
    """Return violations when Mermaid blocks contain value-like literals."""
    violations: list[str] = []
    blocks = re.findall(r"```mermaid\n(.*?)```", markdown, flags=re.DOTALL)
    for block in blocks:
        for line in block.splitlines():
            if _VALUE_LITERAL.search(line):
                violations.append(line.strip())
    return violations


def required_headings_present(markdown: str) -> list[str]:
    missing = [heading for heading in _REQUIRED_HEADINGS if f"## {heading}" not in markdown]
    if "## Field mapping" not in markdown and "## Field mapping (structured → nugget)" not in markdown:
        if "Field mapping" not in missing:
            missing.append("Field mapping")
    return missing
