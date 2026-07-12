# SPEC-005 — Narrative engine v2 + IP address ontology refinement

**Status:** Active (refinement after SPEC-004)  
**Parent coordination:** [#826](https://github.com/brettforbes/spiderfeet/issues/826), visual gate [#932](https://github.com/brettforbes/spiderfeet/issues/932)  
**Plan / agent playbook:** `.governance/project/SPEC005_AGENT_PLAN.md`  
**Issue index:** `.governance/project/SPEC005_ISSUE_INDEX.md`  
**Predecessor:** SPEC-004 (complete — adapters + rule engine landed)

## Objective

Upgrade the **centralized** structured→graph→narrative path so that:

1. IPv4 vs IPv6 values are classified into the correct ontology nugget ids via shared regex rules (not per-tool guesses).
2. Narrative Markdown for **every** adapter tool matches the quality bar set by nmap/netdiscover: meta-concept sections, category subsections, type-relation Mermaid diagrams, short prose stories, optional tables, and a full appendix — driven ~80% by YAML/ontology machinery and ~20% by thin tool hooks.
3. Artifact completeness in the CLI Profiling UI is trustworthy (graph + description resolve for every scenario that should have them).

## Requirements

| ID | Requirement |
|----|-------------|
| R5-01-01 | Shared IP classifier in `core/` driven by `rules/_shared/ip_patterns.yaml`; role-aware mapping to `IP_ADDRESS` / `INTERNAL_IP_ADDRESS` / `AFFILIATE_IPADDR` / `IPV6_ADDRESS` / `AFFILIATE_IPV6_ADDRESS` |
| R5-01-02 | All adapter / topology IP node creation calls the shared classifier (nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei, `core/topology.py`) |
| R5-01-03 | Unit tests prove regex fixtures for IPv4, IPv6 (full + compressed), and rejection of non-IP strings |
| R5-01-04 | Narrative engine v2 in `core/` (promote/refactor `narrative_report.py`): one render path for all tools |
| R5-01-05 | Shared YAML `rules/_shared/narrative_v2.yaml` defines meta-concepts (Scan, Host/System, CDN, Trace), category order, type-only Mermaid templates, appendix/footer |
| R5-01-06 | Per-tool `rules/<tool>/narrative.yaml` supplies host entity id, which meta-concepts apply, factual intro templates, phrasing — **sections must be consumed by the engine** (no dead YAML) |
| R5-01-07 | Every narrative section/subsection: (1) short prose story connecting values, (2) Mermaid of **nugget types + relations only** (not values), (3) optional value table when useful |
| R5-01-08 | Introduction is factual: tool used + ontology hierarchy guide for how the report is laid out (types/containment), not marketing fluff |
| R5-01-09 | Appendix retains complete node/edge inventory (table preferred); `validate_narrative_coverage` still passes |
| R5-01-10 | UI/API scenario-key resolution finds graph + description for format-suffixed scenario ids (`_text`, `_json`, `_xml`, …) |
| R5-01-11 | Text-only paired scenarios either (a) derive structured→graph→narrative from text, or (b) are explicitly flagged `graph_deferred: true` with operator-visible reason — no silent missing panes |
| R5-01-12 | Regenerate `nugget_structure/*_proposed_nuggets_edges*.json|md` for all eight tools after engine+IP land; operator re-review before byte goldens |

## Non-goals

- Inventing Nexus
- Byte-locking golden narrative fixtures before operator visual re-sign-off
- Rewriting all production `sfp_tool_*` modules (Epic E / #723 remains separate)
- Changing Data Viewer embed contracts

## Seed / ontology binding

| Topic | Source |
|-------|--------|
| Narrative structure | `.seed/05_Onotology_for_Nuggets.md` §4.1–§4.3 |
| Business conversion rules | `.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md` |
| Tool seeds | 06B, 07/07B, 08–11B (unchanged authority for mapping) |
| Nugget catalogue | `.docs/analysis/nuggets.json` (IP_* already defined) |
| Engine boundaries | `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` |

## Quality bar (reference narratives)

Treat these as the **target shape** (improve Introduction only):

- `.docs/docs-for-cli-tools/nugget_structure/nmap_*_proposed_nuggets_edges_description.md`
- `.docs/docs-for-cli-tools/nugget_structure/netdiscover_*_proposed_nuggets_edges_description.md`

All other tools must reach equivalent section/Mermaid/table/appendix quality via the shared engine — not by copying nmap-specific prose into adapters.

## Acceptance (program)

1. Shared IP classifier used everywhere IP nodes are created; fixtures green.
2. One `core` narrative engine; adapters’ `to_narrative` is a thin wrapper.
3. Regenerated descriptions for D1–D5 tools show meta-concept sections + type Mermaid + appendix.
4. CLI Profiling UI shows Graph + Markdown for every non-deferred scenario.
5. Visual review checklist updated; operator can assign child issues in index order to lesser agents.

## Traceability

Implementation: GitHub epics under `[SPEC-005]` (see `SPEC005_ISSUE_INDEX.md`).
