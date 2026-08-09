---
name: cli_app_profiling
description: Explore, formally examine, and profile CLI OSINT tools for SpiderFeet V2 nugget graphs. Use when driving CLI apps per .seed/04_Driving and Integrating_CLI_Apps.md — install/probe tools, run scenario matrices, capture evidence bundles, draft nodes/edges proposals, and prepare operator review artifacts.
---

# CLI App Profiling — Exploration and Formal Examination

## Canonical process

**Driving doc:** `.seed/04_Driving and Integrating_CLI_Apps.md`  
**Corpus index:** `.docs/docs-for-cli-tools/corpus_index.json`  
**Harvest runner:** `.seed/scripts/cli_corpus/harvest.py`  
**Tool manifests:** `.seed/scripts/cli_corpus/manifests/<tool>.yaml`  
**New-tool onboarding (start here):** `.seed/scripts/cli_corpus/ONBOARDING.md`  
**Graph/narrative rules:** `.cursor/rules/proj-07-cli-graph-rules-engine.mdc`  
**Narrative v3 (SPEC-014):** `.governance/specs/SPEC-014-narrative-meta-concept-reports.md`  
**Architecture guide:** `.docs/docs-for-cli-tools/SPEC004_SYSTEM_GUIDE.md`

## Phases (per tool)

1. **Exploration** — map semantic output types; build a **semantic outcome matrix** (mandatory); no evidence files yet (1h+ allowed).
2. **Formal examination plan** — named scenarios, targets, expected data types; every matrix row mapped to a scenario or documented limitation.
3. **Strategy skill** — `.strategy/<tool>_strategy.skill` (complements `.cursor/skills/<tool>/`).
4. **CLI help capture** — `.docs/docs-for-cli-tools/<Tool>-CLI-Options.md` (heading + fenced raw `--help` / `-h` output).
5. **Adapter + YAML** — copy `adapters/_template` + `rules/_template`; implement four-output API; wire `harvest.py` `ADAPTER_TOOLS` (see ONBOARDING.md). **No new `*_to_graph.py`.** Narrative: thin `to_narrative()` → `render_narrative` only; tool knobs live in `rules/<tool>/narrative.yaml` (no per-tool narrative Python).
6. **Formal examination** — run `harvest.py`; outputs under `app_examination_docs/<tool>/` plus `nugget_structure/` graph + narrative.
7. **Nugget / narrative proposal** — tool structure MD + per-scenario graph JSON + §4.3 description MD from the **shared meta-concept engine** (`core/narrative_engine.py` + `core/meta_narrative.py` + `rules/_shared/narrative_v2.yaml`).
8. **Operator review** — CLI Profiling four panes; `*_review.status.json` → `approved` | `rejected`; `corpus_index.json` → `complete` on sign-off.

**Excluded:** Aircrack-ng (hardware pending).

## Ontology catalogue (all converters and graph builders)

- Load **both** `.docs/analysis/nuggets.json` and `.docs/analysis/nuggets_extension.json` via `graph_builder.load_nugget_templates()`.
- New archetypes go in `nuggets_extension.json` only; match TypeQL when promoting.
- Resolve `nugget_type` / colour / description from catalogue — do not guess (e.g. `NETWORKS` → `CATEGORY`).
- Instance ids: `uuid5(ONTOLOGY_NAMESPACE, nugget_data)`; one node per `(nugget_id, nugget_data)`.
- **IPs:** `core.ip_classify.classify_ip` only — never map IPv6 literals to `IP_ADDRESS`.

## Exploration discipline (weakness remediated)

Default commands and single targets are **insufficient**. Before formal runs:

1. List every semantic outcome class the tool can produce (rich, sparse, empty scan, passive vs active, text vs structured, error, clean miss, invalid input).
2. Tune targets and flags until each class is demonstrated or proven impossible.
3. Search the web for practitioner example commands when local trials under-deliver.
4. Do not run `harvest.py` until the outcome matrix is complete on paper.
5. **Exploration is incomplete** if batches were skipped due to empty exports, or only low-value noise was captured while the matrix needs rich/CVE/org signal — see `references/exploration-examination-lessons.md`.
6. Multi-mode scanners: one batch / one goal; tech fingerprint then chained selective passes (tool strategy skill when applicable).

## Output rules (fixed)

**Structured-first law:** if structured output is available, use it exclusively for examination and graph derivation. Never harvest a text-only scenario when structured flags exist.

**Graph-mandatory law:** the point is the nugget graph. No graph = invalid scenario. `graph_deferred` is forbidden.

1. Full verbosity when available.
2. Structured preference: JSON → XML → YAML → CSV — **mandatory** when the tool offers it.
3. Structured-native tools: one harvest run with structured flags; **derive** Text pane from structured at harvest.
4. **Forbidden:** second scenario for native TUI/text when structured mode exists (no paired `terminal` + `ndjson`, no nerva without `--json`).
5. Truly text-only tools (no structured mode): capture native text → TextFSM to structured → graph derivation.
6. **Text-only isolation:** run `cls` / `Clear-Host` / `clear` before each text-native examination command; one scenario → one capture; structured JSON must match the text (`scan_tries` = TUI frames or single parsable dump; `empty_scans` = frames with no host table rows).
7. **Never truncate** stdout/stderr in capture commands; include `exit_status` and stderr in structured artifacts when present.
8. **Errors are scenarios:** auth, dependency, invalid target, and network failures get full structured captures (and derived text); not log-only notes.
9. **JSONL → single JSON bundle** (`schema` + `records[]`); never `structured_ext: jsonl`.
10. **Four UI artifacts** required: Text, Structured, **Graph**, Markdown — all four or the scenario is incomplete.

## Targets

| Class | Examples | Purpose |
|-------|----------|---------|
| Permissive | `scanme.nmap.org` | Full data breadth |
| Intentional vuln lab | `pentest-ground.com`, vulnweb | High-signal vuln/CVE classes when tool supports them |
| Smaller real org | `squarepeg.vc`, `theupside.com.au` | Org-intelligence / enrichment tools |
| Corporate | `bbc.co.uk`, `sbs.com.au` | Filtered / protected behaviour (often negative fixtures) |
| Deferred | offline site | Placeholder bundle + `harvest_deferred`; re-harvest later |

See [exploration-examination-lessons.md](references/exploration-examination-lessons.md) for 2026-07 Nuclei/Pius pitfalls (skip-existing, WSL DNS, hostname vs URL, protocol families).

## Evidence bundle (per examination)

Directory: `.docs/docs-for-cli-tools/app_examination_docs/<tool>/`

| File | Content |
|------|---------|
| `{id}_manifest.json` | Metadata, paths, review status |
| `{id}_command.txt` | Exact command line |
| `{id}_output_text.txt` | Human text output |
| `{id}_output_structured.{ext}` | XML/JSON/YAML/CSV |
| `{id}_review.status.json` | `pending` / `approved` / `rejected` |

Nugget drafts: `.docs/docs-for-cli-tools/nugget_structure/`

- `<tool>_<scenario_id>_proposed_nuggets_edges.json`
- `<tool>_<scenario_id>_proposed_nuggets_edges_description.md` — §4.3 narrative (progressive disclosure; see Narrative contract)
- `<tool>_nugget_graph_structure.md` — tool-level structure doc (SPEC-006; type-only Mermaids)

## Running examinations

```bash
# Single scenario
python .seed/scripts/cli_corpus/harvest.py --tool nmap --scenario host_discovery_permissive_xml

# All scenarios in manifest
python .seed/scripts/cli_corpus/harvest.py --tool nmap

# Dry run
python .seed/scripts/cli_corpus/harvest.py --tool nmap --dry-run

# Regenerate graph + narrative from existing structured (no CLI re-run)
python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --tool nmap

# Force-overwrite graph + narrative for all scenarios of a tool (or omit --tool for all eight)
python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --tool nmap --force
```

## Operator review UI

Widget tab **CLI Profiling** (`spiderfeet-widget`) + API `GET /api/v1/cli-corpus/*`.

- **Scenarios:** one API row per scan command (`/tools/{tool}/scenarios/{scenario_key}`), not per file type.
- **Bundles:** `app_examination_docs/<tool>/scenarios/<key>/` with `output_text.txt`, `output_structured.*`, `proposed_nuggets_edges.json`, `nugget_graph_structure.md`.
- **Legacy numbered exams:** pairs like `foo_xml` + `foo_text` are one scenario; consolidate into scenario bundles during examination.
- Confirm **T / S / G / MD** badges before claiming complete. No text-only scenarios when structured modes exist; no `graph_deferred` when structured was skipped.

**Data Viewer (Structured tab):** embed [json-yaml-xml-csv-widget](https://github.com/brettforbes/json-yaml-xml-csv-widget) via `DataViewerHost` — see `@spiderfeet-widget/.docs/data-viewer-embed.md`. Dev URL `http://localhost:3000/widget` (`SPIDERFEET_DATA_VIEWER_URL` / `data-data-viewer-url` on `#widget-root`). Pass `filename` + content; bridge sends `set-mode` then `set` with inferred format.

Approve/Reject updates `review.status.json` in scenario bundle (or legacy `*_review.status.json`).

## V2 graph contract

Every examination produces a **scan head** node plus discovered entities linked by:

- `contains` — entity → entity / category containment
- `listens-to` — service → port (canonical spelling)
- `had` — entity → descriptor (e.g. MAC → vendor)

Emit `nodes[]` and `edges[]`; scan owns discoveries via `contains`. Use `core.graph_builder` for catalogue lookup, uuid5 ids, deduplication, and `validate_graph()`. Prefer `adapters/` + `rules/` over legacy converters. See [v2-graph-rules.md](references/v2-graph-rules.md) and proj-07.

## Narrative contract (SPEC-014 progressive disclosure)

**Active path:** `.seed/scripts/cli_corpus/core/` (what harvest/backfill/API write). Mirror under `modules_v2/_core` when changing shared code.

| Piece | Role |
|-------|------|
| `rules/_shared/narrative_v2.yaml` | Meta-concept registry (scan, host, system, cdn, org, domain, url, service_port, environment, security, trace) |
| `core/meta_narrative.py` | Overview Mermaid, capped example Mermaid (`+N more`), category tables, prose, deduped appendix |
| `core/narrative_engine.py` → `render_narrative` | Composes Title → Introduction → present meta-concepts → Conclusion → Appendix |
| `rules/<tool>/narrative.yaml` | Declarative overrides only (`tool_name`, `phrasing`, `intro_facts`, `meta_concepts`, `include_*`, …) |
| Adapter `to_narrative()` | **One-line shim** calling `render_narrative` — no bespoke builders |

**Report shape (not a single flat type graph):**

1. Factual **Introduction** (tool + hierarchy guide).
2. Per **present** meta-concept: prose → **Structure overview** Mermaid (**type-only**) → per present category: capped **example** Mermaid (values allowed, `example_cap` + `+N more`) + **full value table**.
3. **Conclusion** → one **Appendix** (nodes + edges once; no duplicate edge inventories).
4. Shape cap ~12 nodes per Mermaid; empty categories are omitted.

**Forbidden:** per-tool narrative Python; `NarrativeReportBuilder`-style forks; primary diagram = one global `type_relation_mermaid`; regenerating by re-scanning when `backfill --force` suffices.

**Validators (run after backfill / before claiming MD complete):**

```bash
# Coverage + meta-concept + shape cap + example-cap + appendix dedupe
poetry run pytest .tests/test_narrative_validators.py .tests/test_max_common_invariant.py -q

# nmap/netdiscover match-or-beat vs BD1 reference fixtures (after engine changes)
poetry run python .seed/scripts/cli_corpus/match_or_beat.py
```

Use `core.narrative_validators.validate_narrative_report(graph, md)` in ad-hoc checks. Max-common gate fails if adapters grow narrative logic or `narrative.yaml` introduces unknown keys.

**Quality target:** hierarchy legibility of `modules_v2/content/<tool>/graph_structure.md`, plus capped example values + tables in the Report tab. Review index pattern: `.governance/project/SPEC014_REVIEW_INDEX.md`.

## Nuclei large inputs (modules_v2)

When profiling or executing nuclei against large URL sets: `modules_v2/sfp_cli_nuclei.py` chunks targets (`batch_size` default **20**), fans out `option_passes` (tags/severity/templates), aggregates JSONL into one `nuclei_finding_v1` bundle, and reports `progress` / `bundles scanned across all options: N`. Argv arrays only — never shell strings. Prefer one-batch-one-goal passes per `nuclei_strategy` skill.

## Tool order

**Nmap pilot:** complete (2026-06-26) — see `.docs/docs-for-cli-tools/nmap_pilot_signoff.md`.

**Netdiscover:** complete (2026-06-29) — five windows-lan scenarios; now on the **same** shared narrative engine as other tools (SPEC-014 BD2).

**SPEC-004 adapters:** nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei — patterns to copy.

Next tools: follow `corpus_index.json` priority after exploration gate passes; onboard via `ONBOARDING.md`.

## References

| File | Topic |
|------|--------|
| [references/SKILLS.md](references/SKILLS.md) | Index |
| [references/v2-graph-rules.md](references/v2-graph-rules.md) | Nodes, edges, scan head |
| [references/examination-checklist.md](references/examination-checklist.md) | Per-tool checklist |
| [references/exploration-examination-lessons.md](references/exploration-examination-lessons.md) | Nuclei/Pius lessons; target taxonomy; harvest pitfalls |
| [references/evidence-layout.md](references/evidence-layout.md) | File naming + scenario bundles |
| `../../ONBOARDING.md` (cli_corpus) | End-to-end new-tool checklist |
| `.governance/specs/SPEC-014-narrative-meta-concept-reports.md` | Narrative v3 + nuclei batching requirements |
| `@spiderfeet-widget/.docs/data-viewer-embed.md` | Data Viewer host integration |

Per-tool skills: `.cursor/skills/<tool>/SKILL.md` and Zero-to-Hero docs under `.docs/docs-for-cli-tools/`.
