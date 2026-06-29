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

## Phases (per tool)

1. **Exploration** — map semantic output types; no evidence files yet (1h+ allowed).
2. **Formal examination plan** — named scenarios, targets, expected data types.
3. **Strategy skill** — `.strategy/<tool>_strategy.skill` (complements `.cursor/skills/<tool>/`).
4. **CLI help capture** — `.docs/docs-for-cli-tools/cli_help_text/<tool>_cli_help_text.md`.
5. **Formal examination** — run `harvest.py`; outputs under `app_examination_docs/<tool>/`.
6. **Nugget proposal** — `nugget_structure/<tool>_nugget_graph_structure.md` + JSON draft.
7. **Operator review** — `*_review.status.json` → `approved` | `rejected`.

**Excluded:** Aircrack-ng (hardware pending).

## Output rules (fixed)

1. Full verbosity when available.
2. Structured preference: JSON → XML → YAML → CSV.
3. If tool supports both structured + text simultaneously → capture both in one run.
4. If only one format at a time → run twice (structured run + text run).
5. Text-only tools → TextFSM to structured before graph derivation.
6. **Text-only isolation:** run `cls` / `Clear-Host` / `clear` before each examination command; one scenario → one capture; structured JSON must match the text (`scan_tries` = TUI frames or single parsable dump; `empty_scans` = frames with no host table rows).

## Targets

| Class | Examples | Purpose |
|-------|----------|---------|
| Permissive | `scanme.nmap.org` | Full data breadth |
| Corporate | `bbc.co.uk`, `sbs.com.au` | Filtered / protected behaviour |

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

## Running examinations

```bash
# Single scenario
python .seed/scripts/cli_corpus/harvest.py --tool nmap --scenario host_discovery_permissive_xml

# All scenarios in manifest
python .seed/scripts/cli_corpus/harvest.py --tool nmap

# Dry run
python .seed/scripts/cli_corpus/harvest.py --tool nmap --dry-run
```

## Operator review UI

Widget tab **CLI Profiling** (`spiderfeet-widget`) + API `GET /api/v1/cli-corpus/*`.

- **Scenarios:** one API row per scan command (`/tools/{tool}/scenarios/{scenario_key}`), not per file type.
- **Bundles:** `app_examination_docs/<tool>/scenarios/<key>/` with `output_text.txt`, `output_structured.*`, `proposed_nuggets_edges.json`, `nugget_graph_structure.md`.
- **Legacy numbered exams:** pairs like `foo_xml` + `foo_text` are one scenario; consolidate into scenario bundles during examination.

**Data Viewer (Structured tab):** embed [json-yaml-xml-csv-widget](https://github.com/brettforbes/json-yaml-xml-csv-widget) via `DataViewerHost` — see `@spiderfeet-widget/.docs/data-viewer-embed.md`. Dev URL `http://localhost:3000/widget` (`SPIDERFEET_DATA_VIEWER_URL` / `data-data-viewer-url` on `#widget-root`). Pass `filename` + content; bridge sends `set-mode` then `set` with inferred format.

Approve/Reject updates `review.status.json` in scenario bundle (or legacy `*_review.status.json`).

## V2 graph contract

Every examination produces a **scan head** node plus discovered entities linked by:

- `has` — entity → attribute
- `contains` — entity → entity (transitive modelling allowed)
- `listens on` — service → port

Emit `nodes[]` and `edges[]`; scan owns discoveries via `contains`. See [v2-graph-rules.md](references/v2-graph-rules.md).

## Tool order

**Nmap pilot:** complete (2026-06-26) — see `.docs/docs-for-cli-tools/nmap_pilot_signoff.md`.

Next: **netdiscover** (priority 2 in `corpus_index.json`). Do not skip exploration before formal examination.

## References

| File | Topic |
|------|--------|
| [references/SKILLS.md](references/SKILLS.md) | Index |
| [references/v2-graph-rules.md](references/v2-graph-rules.md) | Nodes, edges, scan head |
| [references/examination-checklist.md](references/examination-checklist.md) | Per-tool checklist |
| [references/evidence-layout.md](references/evidence-layout.md) | File naming + scenario bundles |
| `@spiderfeet-widget/.docs/data-viewer-embed.md` | Data Viewer host integration |

Per-tool skills: `.cursor/skills/<tool>/SKILL.md` and Zero-to-Hero docs under `.docs/docs-for-cli-tools/`.
