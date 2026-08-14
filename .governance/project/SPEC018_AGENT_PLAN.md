# SPEC-018 agent plan — lesser-agent kickoff

**Spec:** `.governance/specs/SPEC-018-composer-refine.md`  
**Seed:** `.seed/19_Refine_Composer_1.md`  
**Goal:** GSE 12A chain actually feeds Nerva/Nuclei; DAG readable + export-only semantic edges + Target collector align; persist-before-FINISHED; `i/n` badges; temp viewer appears at FINISHED and stays empty after Reset.

## Kickoff order (operator)

Start **one issue at a time** per repo. Preferred first wave (parallel across repos):

| Lane | First issue | Then |
|------|-------------|------|
| Backend GSE | **A1** fixture proof | A2 → A3 ∥ A4 → A5 |
| Backend engine | **B1** persist-before-FINISHED (after A1 ok) or **B2** status fields | B1 ∥ B2 → B3 |
| YAML | **C1** short labels and/or **C2** typography | C3 → C4 → C5 → C6 |
| Host | wait for **B2 + C5** | D1; D2 anytime; D3 after B1 |
| Integration | wait for A5+B3+C6+D* | E1 → E2 (operator) |

Do **not** start host D1 until B2 and C5 are on `develop`.
Do **not** start E1 until A5, B3, C6, D1–D3 are on `develop`.

## Per-issue contract

1. Read the GitHub issue body + SPEC-018 requirement ID + this plan’s epic notes.
2. Branch `feature/<n>-<slug>` or `fix/<n>-<slug>` from `develop` only.
3. Smallest coherent change; verify; PR into `develop` with evidence.
4. Comment on the issue at start / blocker / PR / close.
5. Merge, close issue, return repo to `develop` before next issue in that repo.
6. Update the matching `SPEC018*_ISSUE_INDEX.md` status column when closing.

## Skills

- GSE / workflow YAML: `.seed/12C_Graph_Select_Language.md`, `.cursor/skills/typedb/SKILL.md` (schema only — **do not** rewrite GSE to TypeQL)
- Multi-repo paths: `.cursor/skills/cursor-multi-repo/SKILL.md`
- YAML DAG: `@yaml-workflow-widget/.cursor/skills/nice-dag/SKILL.md`
- Nerva/Nuclei/Nmap/Subfinder skills under `.cursor/skills/` when diagnosing argv

## Anti-patterns

- Per-value CLI fan-out / true mid-batch `1/n`
- TypeQL GSE evaluation
- Inventing nugget ids not in `nuggets.json` / `nuggets_extension.json`
- Drawing semantic-export edges for `context.export: none`
- Removing Subfinder `export: scan_graph`
- `ComposerTempGraph.clear()` before GET (flash)
- Reset calling `loadProjectContexts` (temps come back)
- Setting FINISHED before temp persist on exporting steps
- Blind Nuclei timeout bump without proving `crawl_urls`

## Checkpoint status

| CP | Meaning | Status |
|----|---------|--------|
| 1 | Spec + indexes + this plan | **done** (2026-08-14) |
| 2 | GitHub issues open + linked | **done** — A/B/E [#1285](https://github.com/brettforbes/spiderfeet/issues/1285)–[#1297](https://github.com/brettforbes/spiderfeet/issues/1297); C [#283](https://github.com/brettforbes/yaml-workflow-widget/issues/283)–[#289](https://github.com/brettforbes/yaml-workflow-widget/issues/289); D [#269](https://github.com/brettforbes/spiderfeet-widget/issues/269)–[#272](https://github.com/brettforbes/spiderfeet-widget/issues/272) |
| 3 | Implementation complete for review | pending — E2 remains operator gate |

## First issues to assign

1. Backend: [#1288 A1](https://github.com/brettforbes/spiderfeet/issues/1288)
2. YAML (parallel): [#284 C1](https://github.com/brettforbes/yaml-workflow-widget/issues/284) and/or [#285 C2](https://github.com/brettforbes/yaml-workflow-widget/issues/285)
3. Backend engine (parallel): [#1293 B1](https://github.com/brettforbes/spiderfeet/issues/1293) and/or [#1294 B2](https://github.com/brettforbes/spiderfeet/issues/1294)
4. Host: [#271 D2](https://github.com/brettforbes/spiderfeet-widget/issues/271) immediately; **D1** only after B2+C5 merge → [#270](https://github.com/brettforbes/spiderfeet-widget/issues/270)

## Epic notes (for issue bodies)

### Epic A — GSE / 12A chain (`spiderfeet`)

Canonical YAML: `.seed/12A_Workflow_YAML_Example.yaml`. Evaluator: `spiderfeet_v2/workflow/gse_eval.py`. Corpus graphs: `.docs/docs-for-cli-tools/nugget_structure/*_proposed_nuggets_edges.json`.

A1 writes a proof table; A2 changes YAML/GSE only for measured gaps; A3/A4 are tool-specific; A5 locks tests.

### Epic B — Engine sequence (`spiderfeet`)

R18-06 **overrides** SPEC-017 R17-02 non-blocking persist for exporting steps. `step_runner.py` must wait for `persist_temporary_export` before `STATUS_FINISHED`. Status poll already exists (SPEC-015); extend schema only.

### Epic C — YAML widget

`mapper.js` currently `edgeMeta.set(edgeKey(s.id, cid), SEMANTIC_EXPORT)` for every step at rank — that is the C3 bug. C4 is Target-only extra-right, once. C5 must stay backward compatible with string statuses.

### Epic D — Host widget

D2 includes work already started in this Composer session (load-generation, no pre-clear, Reset without reload). Complete and land it under D2; do not regress.

### Epic E — Integration

E2 is operator-only GOV-08. Lesser agents stop after E1 evidence doc.
