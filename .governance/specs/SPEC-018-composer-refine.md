# SPEC-018 — Composer refine (GSE chain, DAG viz, temp sequence)

**Status:** Ready for lesser-agent execution (CP1+CP2 complete 2026-08-14)
**Source:** `.seed/19_Refine_Composer_1.md` (operator grill 2026-08-14)
**Created:** 2026-08-14

**Parents (extends, does not replace):**
- CLI workflow DSL + GSE — `.governance/specs/SPEC-007-cli-workflow-dsl.md`
- SpiderFeet v2 engine — `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`
- YAML layout — `@yaml-workflow-widget/.governance/specs/SPEC-012-LAYOUT-RULES.md`
- Workflow live status — `.governance/specs/SPEC-015-workflow-live-status-viz.md`
- Multi temporary subgraphs — `.governance/specs/SPEC-017-multi-temporary-subgraphs-and-dag-colors.md`

**Repos in scope:**

| Repo | Role |
|------|------|
| `spiderfeet` | GSE proof + 12A chain fixes; persist-before-FINISHED; status `input_total`/`input_done`; E2E |
| `spiderfeet-widget` | Composer: progress postMessage; temp viewer sequence/reset (no flash, chip labels, production order) |
| `yaml-workflow-widget` | Short labels, larger type, export-only semantic edges, Target collector offset, `i/n` badge |

**Issue indexes:**
- Backend A/B/E — `.governance/project/SPEC018_ISSUE_INDEX.md`
- Host D — `@spiderfeet-widget/.governance/project/SPEC018_WIDGET_ISSUE_INDEX.md`
- YAML C — `@yaml-workflow-widget/.governance/project/SPEC018_ISSUE_INDEX.md`
- Agent plan — `.governance/project/SPEC018_AGENT_PLAN.md`

---

## 0. Operator-confirmed decisions (grill, 2026-08-14)

1. **Keep one batched CLI per step.** No per-value fan-out this spec. Tools keep `-iL` / `-l` list files.
2. **Progress `i/n`:** `n = len(resolved input_values)`. While `scan_status=RUNNING` show `0/n`. On `FINISHED` (including skip_step) show `n/n`. Badge lives on the **YAML DAG step node**, not a second Composer chrome badge.
3. **GSE stays in-memory** (`spiderfeet_v2/workflow/gse_eval.py`). No TypeQL rewrite. Prove 12A bindings against corpus graphs, then fix YAML/GSE/ontology so Nerva and Nuclei receive correct lists. Nuclei `timeout after 900.0s` is a **symptom** — fix inputs/argv first; only then retune timeout.
4. **Subfinder does export** (`context.export: scan_graph` stays). Seed §2.2 was wrong on this point.
5. **Semantic-export edges are data-driven:** draw a step→collector edge **only if** that step’s `context.export` is `scan_graph`. A rank still has a collector if **any** step on that rank exports (Nmap+HTTPX row: collector exists; HTTPX has no edge).
6. **Target collector offset (once per workflow):** Target’s collector + semantic-export edge is shifted slightly **further right** so it **vertically aligns** with the first-step (Subfinder) collector.
7. **Override SPEC-017 non-blocking persist:** exporting steps persist four-forms **and** `temporary_subgraph` **before** `scan_status=FINISHED`. The next wave starts only after that write. Viewer re-GETs on FINISHED and **must not** `clear()` to empty before the GET returns.
8. **Fonts always** (native iframe and Composer embed): clip `sfp_cli_` / `tool.` prefixes to the last token; shape labels ~14–16px; edge labels ~11–12px; tooltips/controls **150%** of current.

---

## 0.1 Root causes (to prove in A1, not assume)

- Nmap `ip_port_list` GSE may select `PORT` while graphs emit `TCP_PORT_OPEN` (or similar) → empty list → Nerva `empty: skip_step`.
- Subfinder `all_domains` does not union normalized `$workflow.inputs.targets` with discovered names (seed §1 requires both).
- HTTPX/Katana selectors must match real adapter `nugget_id`s or Nuclei gets empty/huge URL lists and burns the 900s wall clock.
- YAML `mapper.js` currently draws a semantic-export edge from **every** step on a rank to the collector, ignoring `context.export`.
- Temp viewer `loadFromServer` historically `clear()`d before GET (flash) and Reset re-GETed temps (graphs came back). Status-poll reloads raced Reset.
- SPEC-017 allowed non-blocking temp persist, so FINISHED could fire before the temp row existed.

---

## 1. Objective

Make Composer workflow runs **semantically correct and visually followable**: GSE output variables actually feed Nerva/Nuclei; the DAG is readable at Composer zoom and only shows semantic-export edges for exporting steps; Target collector lines up with Subfinder; each step shows `i/n`; temporary subgraphs appear as soon as an exporting step is FINISHED (because persist already completed); Reset leaves the viewer empty.

## 2. Non-goals

- Per-input CLI fan-out / true mid-batch `1/n` while a single `-iL` process runs.
- TypeQL GSE evaluation / recursive TypeDB `contains` functions.
- Changing scan four-form production or adapter graph builders except aligning GSE `nugget_id`s with what adapters already emit.
- Project Context Viewer redesign.
- SPEC-017 D2 operator gate (separate).

---

## 3. Requirements

### Backend (`spiderfeet`) — Epic A (GSE / 12A chain)

| ID | Requirement |
|----|-------------|
| R18-01 | **Fixture proof matrix.** Run each 12A `output.vars` binding through `evaluate_output_vars` on canonical corpus graphs (subfinder, nmap, httpx, katana). Write a results table (empty vs expected). No product YAML change in this issue except documenting gaps. |
| R18-02 | **Fix GSE/YAML mismatches** found in R18-01 (likely: PORT vs `TCP_PORT_OPEN`; Subfinder `all_domains` union with normalized workflow targets; HTTPX/Katana URL nugget ids). Update `.seed/12A_Workflow_YAML_Example.yaml` and `.seed/12C_Graph_Select_Language.md` if `union` with `$workflow.inputs.*` needs documenting. Do not invent nugget ids. |
| R18-03 | **Nerva chain.** With non-empty `ip_port_list`, dry-run/fixture proves argv `--list` receives `ip:port` lines. Regression: empty GSE still `skip_step`. |
| R18-04 | **Nuclei chain.** After Katana GSE is proven, inspect resolved `crawl_urls` size/shape; fix selector/argv (not a blind timeout bump). Only then retune `timeout` if a bounded correct list still exceeds wall clock. |
| R18-05 | **GSE tests.** Unit tests on corpus fixtures for the 12A bindings; 12A still validates against workflow schema. |

### Backend (`spiderfeet`) — Epic B (persist + progress fields)

| ID | Requirement |
|----|-------------|
| R18-06 | **Persist-before-FINISHED.** For `context.export: scan_graph`, persist four-forms **and** `temporary_subgraph` **synchronously** before `scan_status=FINISHED`. Next wave must not start until that write completes. Failures must not leave FINISHED-without-row for exporting steps. Keep `scan_name=target` dedupe under `_TEMP_CONTEXT_LOCK`. Overrides SPEC-017 R17-02 “non-blocking persist” for exporting steps. |
| R18-07 | **Status progress fields.** `WorkflowStepStatusOut` includes `input_total` and `input_done`. RUNNING: `0, n`; FINISHED/skip: `n, n`; UNKNOWN: `0, 0` or omit with host treating as no badge. Source: already-resolved `input_values` on the step/run. |
| R18-08 | **Tests + OpenAPI** for R18-06 and R18-07. |

### YAML widget (`yaml-workflow-widget`) — Epic C

| ID | Requirement |
|----|-------------|
| R18-09 | **Short step labels.** Display last token of `sfp_cli_*` / `tool.*` (`subfinder`, `nmap`). Full id remains in tooltip and YAML. `start` / `target` / `context` labels unchanged except remaining readable at the new type size (`context` may stay slightly smaller if needed). |
| R18-10 | **Typography.** Shape labels ~14–16px; edge labels ~11–12px; tooltips and tooltip buttons **150%** of current. Apply always (native and Composer embed), not embed-only. Prefer a slightly narrower but larger font if needed for fit. |
| R18-11 | **Export-only semantic-export edges.** Layout reads YAML `context.export`. Step→collector edge only when export is `scan_graph`. Rank collector exists if **any** step on that rank exports. HTTPX (no export) on Nmap’s row: collector remains, no HTTPX edge. Katana on Nerva’s row: same. Collector→collector rail unchanged. Robust when steps are expanded or collapsed; collectors stay on the same row as the exporting step(s). |
| R18-12 | **Target collector extra-right offset (once).** Target’s collector X (and its semantic-export edge) shifts right so it **vertically aligns** with the first scan-step (Subfinder) collector. Do not apply this extra length to other collectors. |
| R18-13 | **`setStepStatuses` progress.** Protocol accepts `{ [stepId]: { status, input_done, input_total } }` and remains backward compatible with string statuses (`waiting`/`running`/`complete`/`failed`). Render `i/n` on the step node. |
| R18-14 | **Docs + smoke** for C labels, type, export edges, Target offset, protocol. |

### Host widget (`spiderfeet-widget`) — Epic D

| ID | Requirement |
|----|-------------|
| R18-15 | **Forward progress.** Status poll maps B2 fields into YAML `setStepStatuses` objects. Reset clears badges (`statuses: {}`). |
| R18-16 | **Temp viewer stability.** No `clear()` before GET; load-generation so stale GETs cannot repaint after Reset; Reset **stops the status poller** and does **not** `loadProjectContexts` afterward; chips labeled by `scan_name`/`source` (never `temporary-subgraph--` uuid); list order = `produced_at` (production order). |
| R18-17 | **Immediate temp show.** On step FINISHED, re-GET temps immediately (persist already happened per R18-06) while the next step may already be RUNNING `0/n`. |

### Integration — Epic E

| ID | Requirement |
|----|-------------|
| R18-18 | **E2E smoke evidence** under `.docs/docs-for-cli-tools/SPEC018_E1_E2E_SMOKE.md`: Run → Target temp + DAG Target colour → each exporting FINISHED shows chip in production order as next step goes running `0/n` → `n/n` on complete → HTTPX/Katana have no export edge → Subfinder/Nmap/Nerva/Nuclei do → Target collector aligns with Subfinder collector → Reset empties viewer. Nerva is not skip_step on a graph that has ip:port; Nuclei either completes or fails with **proven** non-empty bounded inputs (not a mystery timeout). |
| R18-19 | **GOV-08 exploratory review** with scenario matrix. **[OPERATOR GATE]** |

---

## 4. Execution order & dependencies

```
Backend A:  A1 → A2 → A3 ∥ A4 → A5
Backend B:  B1 ∥ B2 → B3     (B1 may start after A1; must merge before E1)
YAML C:     C1 ∥ C2 → C3 → C4 → C5 → C6
Host D:     D1 needs B2 + C5;  D2 ∥ D3 (D3 needs B1)
Integr. E:  E1 needs A5, B3, C6, D1–D3 → E2 (OPERATOR GATE)
```

Hard edges:
- Host **D1** requires backend **B2** status fields and YAML **C5** protocol.
- Host **D3** requires backend **B1** persist-before-FINISHED.
- **E1** waits for A5 + B3 + C6 + D*.

## 5. Governance & lesser-agent execution

- One issue at a time **per repo**. Branch from `develop` → PR into `develop` → close with evidence → merge → return to `develop` (GOV-02).
- Read the GitHub issue body + this spec’s requirement ID + `.governance/project/SPEC018_AGENT_PLAN.md`.
- Do not reintroduce client PUT as source of truth for temps (SPEC-017).
- Do not fan-out CLI per input value.
- Do not rewrite GSE to TypeQL.
- Commit/merge only per operator-approved policy.

## 6. Traceability

Requirement IDs `R18-01`…`R18-19`. Issues tagged `[SPEC-018]`. Milestone “done” (except E2) = operator can Run the 12A recon workflow, see readable DAG labels and export-only edges, watch `0/n`→`n/n`, see temps appear at FINISHED without flash/duplicates, Reset to empty, and Nerva/Nuclei receive proven GSE lists.
