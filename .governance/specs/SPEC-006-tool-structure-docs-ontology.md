# SPEC-006 — Tool graph structure docs + unified ontology composition

**Status:** Active (follow-on to SPEC-004 / SPEC-005)  
**Parent coordination:** [#826](https://github.com/brettforbes/spiderfeet/issues/826)  
**Plan / agent playbook:** `.governance/project/SPEC006_AGENT_PLAN.md`  
**Issue index:** `.governance/project/SPEC006_ISSUE_INDEX.md` (populated after issue create)  
**Predecessor:** SPEC-004 (adapters + rule engine), SPEC-005 (narrative v2 + IP classify)

## Objective

Make the **Tools-page Structure** document (`nugget_structure/<tool>_nugget_graph_structure.md`) as trustworthy and excellent as the Nmap gold standard, via **centralized** YAML + engine logic (~80%) and thin per-tool packs (~20%). Then **compose** every tool sub-graph into `.docs/docs-for-cli-tools/_Current_Ontology.md` in the same Mermaid-first style.

Today: Nmap and Netdiscover structure docs are strong; Nerva / Pius / Subfinder / httpx are thin tables; Katana and Nuclei lack proper structure docs. Hand-maintained MD drifts from `rules/<tool>/mapping.yaml` and live graphs.

## Gold-standard reference

Treat this file as the **shape and quality bar** (do not dumb it down):

`.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md`

Required sections (every tool):

1. Title: `<Tool> — proposed nugget graph structure`
2. Header block: ontology seed refs, generator/adapter path, artifact naming
3. **Scan head** — prose + type-relation Mermaid (`SCAN_RECORD` → `had` descriptors)
4. **Primary endpoint tree(s)** — one Mermaid per distinct topology pattern (HOST/SYSTEM/CDN/DOMAIN, categories, descriptors)
5. **Optional specialty branches** — only when the tool emits them (SSH keys, TRACE, vulns, org trees, …)
6. **Scenario coverage** table — scenario id → primary structures demonstrated
7. **Field mapping** table — structured field/path → `nugget_id`
8. **Proposed nuggets** table when the tool introduces catalogue-worthy types
9. **Review notes** — intentional omissions, deferred fields, relation vocabulary reminder
10. Link to [_Current_Ontology.md](../_Current_Ontology.md)

Mermaid rules (same as narrative SPEC-005):

- Diagrams show **nugget types + relations only** (no instance values, no IP literals, no hostnames)
- Prefer focused diagrams (≤ ~12 nodes)
- Edge labels: only `contains` / `had` / `listens-to` unless a seed+SPEC adds a relation

## Requirements

| ID | Requirement |
|----|-------------|
| R6-01-01 | Shared structure-doc quality bar checklist checked into `.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md` derived from the Nmap gold file |
| R6-01-02 | Shared YAML `rules/_shared/structure_v1.yaml` defines reusable type-relation Mermaid patterns (aligned with `topology_templates.yaml`) |
| R6-01-03 | Per-tool `rules/<tool>/structure.yaml` declares which patterns apply, scenario→pattern map, field mapping, specialty sections, seed_doc citations |
| R6-01-04 | Central engine `core/structure_doc_engine.py` renders `nugget_structure/<tool>_nugget_graph_structure.md` from shared + per-tool YAML (adapters do not hand-author full MD) |
| R6-01-05 | CLI `render_structure_docs.py --tool <id>\|--all` regenerates structure docs without re-harvesting scans |
| R6-01-06 | Unit/governance tests: every ADAPTER_TOOLS tool has a structure doc; required sections present; Mermaid fences parse; no value literals in Mermaid node labels |
| R6-01-07 | All eight adapter tools (nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei) ship Nmap-quality structure docs via the engine |
| R6-01-08 | Engine or companion composer updates `.docs/docs-for-cli-tools/_Current_Ontology.md`: sub-graph table, per-tool sub-graph sections, composition Mermaid, scan-descriptor families, NETWORKS/APPLICATIONS extensions |
| R6-01-09 | Ontology composer folds seed authority docs (`.seed/05`, tool seeds `06B`/`07`/`07B`/`08`–`11B`, `14`, catalogue) as cited sources — not raw transcript dumps |
| R6-01-10 | Tools-page API `GET /api/v1/cli-corpus/tools/{id}/graph-structure` continues to serve the regenerated MD; checklist for operator visual review on Structure button |
| R6-01-11 | ONBOARDING + proj-06/07 require structure.yaml + regenerate step; no new tool completes formal examination without Structure doc |

## Non-goals

- Inventing Nexus
- Rewriting production `sfp_*` modules
- Changing narrative engine contracts (SPEC-005) except cross-links
- Byte-locking structure docs as golden fixtures before operator visual sign-off
- Re-harvesting CLI scans (structure docs derive from YAML + existing graph evidence)

## Architecture (80 / 20)

```text
rules/_shared/structure_v1.yaml     → reusable Mermaid type patterns + section order
rules/_shared/topology_templates.yaml → keep as graph-build source of truth; structure patterns must cite/align
rules/<tool>/structure.yaml         → which patterns, scenarios, field map, specialty prose hooks
rules/<tool>/mapping.yaml           → field→nugget authority (structure.yaml may reference paths)
core/structure_doc_engine.py        → render tool MD + optional ontology composer helpers
render_structure_docs.py            → CLI entry
nugget_structure/<tool>_…md         → Tools page Structure button
_Current_Ontology.md                → composed full-extent view
```

**Adapters** may supply only: tool display name, host entity id, specialty section ids already cited in seed docs, short factual blurb strings. No full hand-written structure MD for new tools after M1 lands.

## Acceptance (program)

1. Quality bar + shared patterns checked in.
2. Engine regenerates all eight tool structure docs; tests green.
3. Each Tools-page Structure view matches Nmap section/Mermaid depth for that tool’s evidence surface.
4. `_Current_Ontology.md` lists all eight tools with sub-graph Mermaid sections and composition diagram.
5. Operator can assign children from `SPEC006_ISSUE_INDEX.md` in order to lesser agents.

## Traceability

Implementation: GitHub epics under `[SPEC-006]` (see `SPEC006_ISSUE_INDEX.md`).
