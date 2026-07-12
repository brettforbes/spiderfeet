# SPEC-006 ontology source inventory

**Date:** 2026-07-13  
**Requirement:** R6-01-09  
**Composer:** `.seed/scripts/cli_corpus/core/structure_doc_engine.py` (`render_ontology_doc`)  
**Output:** `.docs/docs-for-cli-tools/_Current_Ontology.md`

This inventory lists authoritative sources the ontology composer must cite — not raw transcript dumps.

## Tier 1 — Canonical ontology seed

| Source | Role in composition |
|--------|---------------------|
| `.seed/05_Onotology_for_Nuggets.md` | Meta-concepts, relation vocabulary (`contains`, `had`, `listens-to`), scan head, IPS/OSI hierarchy, §4.3 narrative contract |
| `.docs/analysis/nuggets.json` | Legacy archetype catalogue |
| `.docs/analysis/nuggets_extension.json` | Tool-specific and promoted nugget types (SSH keys, Nuclei tiers, …) |
| `.seed/spiderfeet_map.tql` | TypeDB schema authority for nugget shapes |

## Tier 2 — Cross-tool business rules

| Source | Role |
|--------|------|
| `.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md` | SPEC-004 80/20 law; structured→graph→narrative pipeline |
| `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md` | Host/SYSTEM/CDN correlation and reclassification |
| `.governance/specs/SPEC-004-cli-graph-rules-engine.md` | Adapter + rules engine requirements |
| `.governance/specs/SPEC-005-narrative-v2-ip-classify.md` | Narrative v2 + `classify_ip` |
| `.governance/specs/SPEC-006-tool-structure-docs-ontology.md` | Structure doc + ontology composition requirements |

## Tier 3 — Per-tool seed docs (cite in structure packs)

| Tool | Seed docs | structure.yaml |
|------|-----------|------------------|
| nmap | `.seed/06B_NMAP_Ontology_Update_Ruleset.md`, `.seed/06_Updates_to_NMAP_Cli_App_Profiling.md` | `rules/nmap/structure.yaml` |
| netdiscover | `.seed/06A_Updates_to_NetDiscover_Cli_App_Profiling copy.md` | `rules/netdiscover/structure.yaml` |
| nerva | `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md`, `.seed/07B_Nerva_Ontology_Rules.md` | `rules/nerva/structure.yaml` |
| pius | `.seed/08_Rules_for_Pius.md` | `rules/pius/structure.yaml` |
| subfinder | `.seed/09_Ontology_For_Subfinder.md` | `rules/subfinder/structure.yaml` |
| httpx | `.seed/10_Rules_For_Httpx.md` | `rules/httpx/structure.yaml` |
| katana | `.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md` (D4 migration) | `rules/katana/structure.yaml` |
| nuclei | `.seed/11_Ontology_for_Nuclei.md`, `.seed/11B_Rules_for_Nuclei.md` | `rules/nuclei/structure.yaml` |

## Tier 4 — Runtime mapping authority (structure cites paths; does not fork)

| Artifact | Role |
|----------|------|
| `rules/<tool>/mapping.yaml` | Field→nugget paths for scan head descriptors |
| `rules/<tool>/narrative.yaml` | §4.3 narrative profile keys |
| `rules/_shared/topology_templates.yaml` | Graph-build topology templates |
| `rules/_shared/structure_v1.yaml` | Structure-doc Mermaid type patterns (aligned with topology) |
| `adapters/<tool>/hooks.py` | Cited graph hooks when YAML cannot express behavior |

## Tier 5 — Generated operator artifacts (regenerated, not hand-edited)

| Artifact | Generator |
|----------|-----------|
| `nugget_structure/<tool>_nugget_graph_structure.md` | `render_structure_docs.py --tool <id>` |
| `nugget_structure/<tool>_<scenario>_proposed_nuggets_edges.json` | `adapters/<tool>/build_outputs` / harvest |
| `nugget_structure/<tool>_<scenario>_proposed_nuggets_edges_description.md` | `core/narrative_engine.render_narrative` |
| `_Current_Ontology.md` | `render_structure_docs.py --ontology` or `compose_current_ontology.py` |

## Tier 6 — Examination manifests (scenario ids)

| Manifest | Used for |
|----------|----------|
| `.seed/scripts/cli_corpus/manifests/<tool>.yaml` | `structure.yaml` scenario coverage tables |

## Composition rules

1. **Extend** `_Current_Ontology.md` unified sections (qualification hierarchy, global relations) — do not delete without operator approval.
2. Per-tool **Sub-graph** sections summarize type Mermaid from `structure_v1.yaml` patterns named in each `structure.yaml`.
3. Deep field tables stay in per-tool Structure docs; the composed doc links to them.
4. New tools must add Tier 3 seed doc + `structure.yaml` before formal examination sign-off (R6-01-11).

## Regeneration commands

```bash
poetry run python .seed/scripts/cli_corpus/render_structure_docs.py --all
poetry run python .seed/scripts/cli_corpus/compose_current_ontology.py
```
