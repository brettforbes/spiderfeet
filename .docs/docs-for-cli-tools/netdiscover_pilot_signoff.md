# Netdiscover CLI Profiling — Operator Sign-Off

**Date:** 2026-06-29  
**Parent program:** CLI Profiling V2 ontology discovery  
**Spec:** `.seed/04_Driving and Integrating_CLI_Apps.md`, `.seed/05_Onotology_for_Nuggets.md` §4.3

## Outcome

Netdiscover is the **second completed CLI application profiling pilot** (text-only / TextFSM path). All five formal examination scenarios are **operator-approved**. Evidence bundles, semantic graph proposals, per-scenario narrative reports, and graph-structure documentation are in-repo and exposed via `GET /api/v1/cli-corpus/*`.

## Approved scenarios (5)

| Exam | Scenario key | Notes |
|------|--------------|-------|
| 1 | `local_subnet_active_parsable` | Single parsable table dump; 1 try, 0 empty |
| 2 | `local_subnet_active_text` | TUI text capture; multi-frame empty scans |
| 3 | `local_subnet_fast_parsable` | Fast scan mode; sparse host set |
| 4 | `passive_snippet_text` | Passive ARP snippet; multi-frame text |
| 5 | `sparse_subnet_parsable` | Full /24 rescan; rich host table |

## Deliverables

| Artifact | Location |
|----------|----------|
| Harvest manifest | `.seed/scripts/cli_corpus/manifests/netdiscover.yaml` |
| Evidence bundles | `.docs/docs-for-cli-tools/app_examination_docs/netdiscover/` (exams 1–5) |
| Graph structure | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_nugget_graph_structure.md` |
| Per-scenario graphs + narratives | `.docs/docs-for-cli-tools/nugget_structure/netdiscover_<scenario>_proposed_nuggets_edges.{json,description.md}` |
| Converters | `netdiscover_text_to_json.py`, `netdiscover_json_to_graph.py`, `graph_builder.py` |
| Corpus index | `corpus_index.json` — `phase: complete`, `runtime: windows-lan` |

## Reference patterns for next tools

- Load `nuggets.json` + `nuggets_extension.json`; uuid5 instance ids via `graph_builder.py`
- One node per `(nugget_id, nugget_data)`; `MAC_VENDOR` via `had` edges
- `cls` before each text-only capture; structured JSON mirrors text (`scan_tries`, `empty_scans`)
- Semantic outcome matrix before formal examination (see updated `proj-06` rule)

## Next tool

Per `corpus_index.json` priority 3: **nerva** (`operator_review` — validate or complete per updated examination rules).
