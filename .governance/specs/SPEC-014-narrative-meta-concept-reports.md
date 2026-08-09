# SPEC-014 — Narrative reports v3: meta-concept progressive disclosure (+ nuclei large-input batching)

**Status:** Active (refinement after SPEC-005; precedes the first v2 live-scan campaign)
**Plan / agent playbook:** `.governance/project/SPEC014_AGENT_PLAN.md`
**Issue index:** `.governance/project/SPEC014_ISSUE_INDEX.md`
**Predecessors:** SPEC-004 (adapters + rule engine), SPEC-005 (central narrative engine v2 + IP classify), SPEC-006 (tool Structure docs + `structure_v1.yaml` pattern library)

## Objective

Before we run live scans on the v2 machinery, upgrade the narrative report generator so it always tells the **graph-hierarchy story** — not a flat recital of elements — and so it does so with **maximum common code and minimum tool-specific code**.

Two concrete outcomes:

1. **Meta-concept progressive-disclosure narratives.** Every meta-concept present in a scenario graph (Scan, Host/System, CDN, Domain -> subdomains, URL, Organization -> domains/netblocks, Service/Port, Environment/OS, Security -> findings, and Trace as a category-like container) is rendered with a small overview diagram of its categories, then one small per-category diagram showing a few example instances (rest in a table), plus a short prose story. Diagrams stay large-and-readable (few shapes), mirroring the quality of `modules_v2/content/<tool>/graph_structure.md`.
2. **Nuclei large-input handling.** The nuclei module automatically chunks very large target lists (e.g. 15,000 URLs) into blocks of 20, runs every configured option pass over all blocks, aggregates results into one bundle for the four outputs, and reports scanning progress (batches done / total, per option pass).

## Problem evidence

- Generic path in `.seed/scripts/cli_corpus/core/narrative_engine.py` (`render_narrative` -> `type_relation_mermaid`) emits bullet lists + **one** flat global `flowchart LR` + a duplicated appendix. Example: `.docs/docs-for-cli-tools/nugget_structure/pius_corporate_upside_ndjson_proposed_nuggets_edges_description.md` (no apex->subdomain story; ~130 lines of duplicated edges).
- Only nmap/netdiscover get richer prose, and only via ~950 lines of bespoke Python builders in `.seed/scripts/cli_corpus/narrative_report.py` (`NarrativeReportBuilder`, `NetdiscoverNarrativeReportBuilder`) that `render_narrative` hard-branches into — the one real "maximum tool-specific" violation.
- The SPEC-006 `structure_doc_engine.py` already renders clean small per-concept type Mermaid via `render_mermaid_from_pattern` from `rules/_shared/structure_v1.yaml`, but only from static templates, not from live scenario graphs.

## The design: one meta-concept model, two renderers

A single shared **meta-concept registry** is consumed by both the canonical Structure doc (template view, SPEC-006) and the per-scenario narrative (live-data view, this spec), so they tell the same hierarchy story. The narrative renderer derives small diagrams from the actual graph using progressive disclosure.

## Requirements

| ID | Requirement |
|----|-------------|
| R14-01 | Shared **meta-concept registry** in `rules/_shared/narrative_v2.yaml` (+ `modules_v2/_rules/_shared/` mirror), aligned with `structure_v1.yaml`. Per concept: `heading`, `order`, `root_nugget_ids`, `category_nugget_ids`, `example_cap`, `prose`, `table` columns. Concepts: scan, host, system, cdn, domain (with subdomain children), url, org, service_port, environment, security, trace (category-like). Single source of truth — no hard-coded concept lists in Python. |
| R14-02 | Central `core/meta_narrative.py`: `detect_meta_concepts(graph)`, `concept_overview_mermaid`, `category_example_mermaid` (capped + `+N more`), `category_table`, `concept_prose`, and a deduped `append_appendix` (fixes the duplicate-edge bug). |
| R14-03 | `render_narrative` generic path composes: Title -> factual Introduction (tool + hierarchy guide) -> Scan section -> per meta-concept sections (overview diagram + per-category example diagram + full table + prose) -> Trace -> Conclusion -> deduped Appendix -> Footer. |
| R14-04 | Diagrams are small and readable: hard shape cap (default <= 12 nodes) per Mermaid block; `example_cap` (default 3) example instances per category diagram with an explicit `+N more` affordance; the full set always appears in the adjacent table. |
| R14-05 | Narrative category diagrams **may** show capped example values (documented divergence from the strictly type-only SPEC-006 Structure doc). Overview/type diagrams remain type-only. |
| R14-06 | **Unify:** nmap and netdiscover render through the shared engine; the bespoke `NarrativeReportBuilder` / `NetdiscoverNarrativeReportBuilder` are retired. A reference snapshot + match-or-beat gate (section presence + `validate_narrative_coverage`) must pass before deletion. |
| R14-07 | **Max-common / min-specific invariant (enforced):** all hierarchy/diagram/table/prose/appendix logic lives in `core/` driven by the registry; a tool may contribute only declarative `rules/<tool>/narrative.yaml`; adapters expose only the one-line `to_narrative()` shim. A test gate fails if any adapter grows narrative logic. |
| R14-08 | Validators: extend `validate_narrative_coverage`; add `validate_meta_concept_coverage` (every present concept has an overview; every category with instances has an example diagram + full table), mermaid shape-size guard, example-cap + table-completeness check, appendix-dedupe check. Unit tests for each. |
| R14-09 | Regenerate all 8 tools' scenario `*_proposed_nuggets_edges.json|md` via `backfill_adapter_four_outputs.py --force` (no re-scan); build an operator review index; **operator visual review gate** before locking. |
| R14-10 | Mirror engine + `narrative_v2.yaml` into `modules_v2/_core` + `_rules`; refresh parity tests; update `modules_v2/_core/tests/PARITY_DIFFS.md`. |
| R14-11 | **Nuclei batching:** `modules_v2/sfp_cli_nuclei.py` collects the full target set (`urls`/`hosts`/`host_list`), chunks into blocks of `batch_size` (default 20, configurable), runs each configured option pass (nuclei_strategy tag/severity families) over every block, and aggregates all JSONL into one `nuclei_finding_v1` bundle for the four outputs. Argv-only dispatch; overall timeout/limit guard. |
| R14-12 | **Nuclei progress:** report `batch i/N (pass: tags=..., severity=...)` and a final "bundles scanned across all options" summary via a progress callback and a structured progress field on the result. |

## Non-goals

- Byte-locking golden narrative fixtures before operator visual sign-off (R14-09 gate).
- Changing the FastAPI corpus contract or the widget Report tab rendering (they consume the same files).
- Rewriting production `sfp_tool_*` modules beyond the nuclei batching scope (R14-11/12).
- Changing SPEC-006 Structure-doc type-only purity (narrative divergence R14-05 is scoped to narrative category diagrams only).

## Seed / ontology binding

| Topic | Source |
|-------|--------|
| Narrative structure | `.seed/05_Onotology_for_Nuggets.md` §4.1–§4.3 |
| Meta-concept patterns | `rules/_shared/structure_v1.yaml` (SPEC-006), `rules/_shared/narrative_v2.yaml` (SPEC-005) |
| Engine boundaries | `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` |
| Nuclei strategy | `.cursor/skills/nuclei_strategy/SKILL.md`, `.seed/11_Ontology_for_Nuclei.md`, `.seed/11B_Rules_for_Nuclei.md` |

## Quality bar (reference)

Target shape for the hierarchy story: `modules_v2/content/<tool>/graph_structure.md` (small type diagrams per meta-concept). Narrative reports must reach equivalent hierarchy legibility via the shared engine, adding capped example values + tables — not by per-tool prose in adapters.

## Acceptance (program)

1. One shared registry; `core/meta_narrative.py` renders all tools; adapters' `to_narrative` remain thin one-liners; invariant test gate green (R14-06/07).
2. Every present meta-concept renders overview + per-category example diagram + full table + prose; no diagram exceeds the shape cap; appendix has no duplicate edges (R14-02/03/04/08).
3. nmap/netdiscover match-or-beat their reference snapshots, then bespoke builders are deleted (R14-06).
4. All ~70 scenarios regenerated; operator visual review passed (R14-09).
5. modules_v2 parity green (R14-10).
6. Nuclei runs a 15k-URL input as blocks of 20 across all option passes with progress reporting; aggregated four outputs produced (R14-11/12).

## Traceability

Implementation: GitHub epics under `[SPEC-014]` (Epics BA–BH) — see `SPEC014_ISSUE_INDEX.md`.
