# SPEC-004 — CLI structured → graph → narrative rules engine

**Status:** Active (planning artifacts landed; implementation via GitHub epic tree)  
**Plan:** `.cursor/plans/centralize_graph_rules_23c5169b.plan.md` (operator workspace) / project continuity  
**Driving docs:** `.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md`, `.seed/05_Onotology_for_Nuggets.md`  
**Related:** SPEC-002 (stages 0–4; this work does **not** block stage exit), SPEC-003 R3-05-08 (runtime CLI manifests), epic [#826](https://github.com/brettforbes/spiderfeet/issues/826)

## Objective

Centralize conversion of CLI examination structured output into a **common semantic graph** and **Markdown narrative report**, using a hybrid declarative rule engine (YAML) plus thin per-tool adapters. Every CLI app must produce four UI artifacts: **Text**, **Structured**, **Graph**, **Markdown Report**. CLI-app-specific code stays in one adapter package (later one thin `sfp_<app>` module). Do **not** invent a Nexus tool.

## Requirements

| ID | Requirement |
|----|-------------|
| R4-01-01 | Four-output contract (Text, Structured JSON/XML, Graph nodes/edges, Markdown narrative with full appendix) + single shared instance-id function `nugget_id--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}` |
| R4-01-02 | Hybrid rule engine: declarative packs under `rules/` (~80%) + cited Python hooks (~20%); shared `core/` package |
| R4-01-03 | Dual capture families: `structured_native` (must derive/pair Text) and `text_native` (must produce Structured via TextFSM or equivalent) |
| R4-01-04 | Executable host/CDN correlation from `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md` (A→C→B) and Nerva ontology mapping from `.seed/07B_Nerva_Ontology_Rules.md` (N0–N5) |
| R4-01-05 | Generic narrative engine (§4.3): scan → meta-concepts → appendix of every node/edge; per-tool `narrative.yaml` profiles |
| R4-01-06 | Per-tool adapter packages for: nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei (seeds 06B, 07/07B, 08–10, 11/11B) |
| R4-01-07 | Governance: `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` + anti-sprawl tests; no hardcoded full mappers when YAML suffices |
| R4-01-08 | Operator visual-review gate before locking golden graph/narrative fixtures |
| R4-01-09 | Second-push thin `sfp_<app>` modules (abuse.ch-shaped) that call shared adapters — **after** goldens |

## Non-goals (this spec)

- Production rewrite of all `modules/sfp_tool_*` in the first implementation wave (tracked as Epic E placeholder).
- Inventing Nexus or other non-existent CLI tools.
- Premature golden byte-lock tests before visual review.

## Seed document index

| Tool | Ontology / rules |
|------|------------------|
| Nmap | `.seed/06B_NMAP_Ontology_Update_Ruleset.md` |
| Nerva correlation | `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md` |
| Nerva ontology | `.seed/07B_Nerva_Ontology_Rules.md` |
| Pius | `.seed/08_Rules_for_Pius.md` |
| Subfinder | `.seed/09_Ontology_For_Subfinder.md` |
| Httpx | `.seed/10_Rules_For_Httpx.md` |
| Nuclei ontology | `.seed/11_Ontology_for_Nuclei.md` |
| Nuclei rules | `.seed/11B_Rules_for_Nuclei.md` |
| Overview | `.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md` |
| Unified ontology | `.docs/docs-for-cli-tools/_Current_Ontology.md` |

## Acceptance (program)

1. Nmap + Netdiscover graphs/narratives generated only via adapters + YAML (cited hooks only).
2. Zero divergent UUID helpers.
3. Nerva uses 07 + 07B (correlation + ontology) with fired-rule evidence.
4. Harvest writes all four artifacts for graph-emitting tools in scope.
5. Visual review completed before goldens (R4-01-08).
6. New-tool PRs that hardcode full mappers fail governance checks (R4-01-07).

## Traceability

Implementation issues: GitHub epics under label `epic` titled `[SPEC-004] …` (Epics A–E). Parent coordination: #826, #723.
