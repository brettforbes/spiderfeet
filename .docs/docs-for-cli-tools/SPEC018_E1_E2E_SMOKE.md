# SPEC-018 E1 — Cross-repo E2E smoke evidence

**Date:** 2026-08-14  
**Issue:** [#1296](https://github.com/brettforbes/spiderfeet/issues/1296) (R18-18)  
**Spec:** `.governance/specs/SPEC-018-composer-refine.md`  
**Workflow:** `.seed/12A_Workflow_YAML_Example.yaml` (canonical 12A recon chain)

## Delivery landed (all three repos)

| Lane | Stories | Merged PRs |
|------|---------|------------|
| Backend A (GSE) | A1–A5 | [#1298](https://github.com/brettforbes/spiderfeet/pull/1298) proof matrix, [#1299](https://github.com/brettforbes/spiderfeet/pull/1299) GSE/YAML fixes, [#1300](https://github.com/brettforbes/spiderfeet/pull/1300) Nerva chain, [#1301](https://github.com/brettforbes/spiderfeet/pull/1301) Nuclei proof, [#1302](https://github.com/brettforbes/spiderfeet/pull/1302) GSE tests |
| Backend B (persist + progress) | B1–B3 | [#1303](https://github.com/brettforbes/spiderfeet/pull/1303) persist-before-FINISHED, [#1304](https://github.com/brettforbes/spiderfeet/pull/1304) `input_total`/`input_done`, [#1305](https://github.com/brettforbes/spiderfeet/pull/1305) tests + OpenAPI |
| YAML widget C | C1–C6 | [#290](https://github.com/brettforbes/yaml-workflow-widget/pull/290)–[#295](https://github.com/brettforbes/yaml-workflow-widget/pull/295) labels, typography, export-only edges, Target offset, `i/n` badge, smoke |
| Host widget D | D1–D3 | [#273](https://github.com/brettforbes/spiderfeet-widget/pull/273) temp stability + Reset, [#274](https://github.com/brettforbes/spiderfeet-widget/pull/274) FINISHED reload, [#275](https://github.com/brettforbes/spiderfeet-widget/pull/275) forward `i/n` |

Supporting docs: `.docs/docs-for-cli-tools/SPEC018_A1_GSE_PROOF.md`, `.docs/docs-for-cli-tools/SPEC018_A4_NUCLEI.md`.

---

## Automated evidence (2026-08-14)

### Backend (`develop`)

Run from repo root with Poetry:

```bash
poetry run pytest \
  spiderfeet_v2/workflow/tests/test_gse_12a_fixtures.py \
  spiderfeet_v2/workflow/tests/test_gse_12a_chain.py \
  spiderfeet_v2/engine/tests/test_persist_before_finished.py \
  spiderfeet_v2/api/tests/test_workflow_status_input_progress.py \
  spiderfeet_v2/engine/tests/test_step_runner.py \
  -q
```

| Check | Result (2026-08-14) |
|-------|---------------------|
| GSE 12A corpus fixtures (A5) | **2 passed** — `test_gse_12a_fixtures.py` |
| GSE chain Nerva/Nuclei (A3/A4) | **6 passed** — `test_gse_12a_chain.py` |
| Persist-before-FINISHED (B1/R18-06) | **2 passed** — `test_persist_before_finished.py` |
| Status `input_total`/`input_done` (B2/R18-07) | **4 passed** — `test_workflow_status_input_progress.py` |
| Step runner export ordering (R18-06) | **7 passed** — `test_step_runner.py` (includes persist-before-FINISHED regression) |
| **Total** | **21 passed** |

Verified behaviours in tests:

| Requirement | Test / module |
|-------------|---------------|
| R18-01/02 GSE bindings on corpus graphs | `test_gse_12a_fixtures.py`, `test_gse_12a_chain.py` |
| R18-03 Nerva `--list` receives non-empty `ip:port` when Nmap graph has ports | `test_nerva_argv_receives_ip_port_list`, `test_nmap_ip_port_list_non_empty_on_corpus` |
| R18-03 Empty GSE still `skip_step` | `test_nerva_empty_ip_port_list_is_empty_input` |
| R18-04 Katana `crawl_urls` non-empty on corpus; Nuclei wired from vars | `test_katana_crawl_urls_non_empty_on_corpus`, `test_nuclei_input_from_katana_vars` |
| R18-04 Empty crawl → Nuclei skip | `test_nuclei_empty_crawl_urls_is_skip_step` |
| R18-06 Temp row exists before `scan_status=FINISHED` for exporting steps | `test_persist_before_finished.py`, `test_step_runner.py` |
| R18-07 RUNNING → `input_done=0`, `input_total=n`; FINISHED → `n/n` | `test_workflow_status_running_input_progress`, `test_workflow_status_finished_input_progress` |
| R18-08 OpenAPI exposes `input_total`/`input_done` | `test_openapi_workflow_step_status_includes_input_progress` |

Regenerate GSE proof table (optional):

```bash
poetry run python .seed/scripts/spec018_gse_proof.py
```

### YAML widget (`develop`)

```bash
node src/workflow-dag/spec018.smoke.mjs
```

| Check | Result (2026-08-14) |
|-------|---------------------|
| Export-only semantic edges + Target rail (C3/C4) | **OK** — `components/mapper.smoke.mjs` |
| `i/n` badge normalization (C5) | **STEP_STATUS_SMOKE_OK** |
| Host `setStepStatuses` object protocol (C5) | **HOST_STEP_STATUSES_SMOKE_OK** |
| Bundle | **SPEC018_SMOKE_OK** |

Code-path coverage (merged on develop):

- Short labels: last token of `sfp_cli_*` / `tool.*` (`subfinder`, `nmap`, …) — R18-09
- Typography ~14–16px shapes, ~11–12px edges, 150% tooltips — R18-10
- Semantic-export edge only when `context.export: scan_graph` — R18-11
- Target collector extra-right X aligns with first scan-step collector — R18-12
- `setStepStatuses` accepts `{ status, input_done, input_total }` — R18-13

See `src/workflow-dag/HOST_PROTOCOL.md` and `.governance/specs/SPEC-012-LAYOUT-RULES.md` (SPEC-018 addendum).

### Host widget (`develop`)

No dedicated Jest/pytest suite; behaviour verified by merged code paths:

| Requirement | Key file / behaviour |
|-------------|---------------------|
| R18-15 Forward `input_total`/`input_done` into YAML `setStepStatuses` | `src/js/composer.js` — `_buildStepStatusEntry`, status poller |
| R18-15 Reset clears badges | `ComposerWorkflow.setStepStatuses({})` on Reset |
| R18-16 No `clear()` before GET; load-generation stale guard | `src/js/composer-temp-graph.js` — `loadFromServer`, `_loadGeneration` |
| R18-16 Reset stops poller, no `loadProjectContexts` after Reset | `src/js/composer.js` — Reset handler |
| R18-16 Chips labeled by `scan_name`/`source` (not uuid) | `ComposerTempGraph.subgraphLabel`, `inferSourceLabel` |
| R18-16 List order = `produced_at` (production order) | `ComposerTempGraph.sortSubgraphsByProducedAt` |
| R18-17 Re-GET temps immediately on step FINISHED | `composer.js` status poller → `loadFromServer` on FINISHED |

---

## Live Composer checklist (operator)

**Status:** Ready for operator verification (automated lane green; full interactive run not executed in E1 pass).

### Preconditions

1. All three repos on **`develop`** (commits at or after merged PRs above).
2. Restart stack: `spiderfeet/start.ps1` (API + TypeDB), `spiderfeet-widget/start.ps1` (host), yaml-workflow-widget dev server if not embedded via widget build.
3. API health: `GET http://127.0.0.1:8001/api/v1/health` → 200.
4. Open **Composer** tab on a seeded project with 12A workflow YAML loaded (e.g. project with `.seed/12A_Workflow_YAML_Example.yaml` workflow).
5. TypeDB schema current (see `SPEC017_A1_SCHEMA_RELOAD.md` if temp list API errors).

### Scenario matrix

| # | Scenario | Expected behaviour | Verification method | E1 status |
|---|----------|-------------------|---------------------|-----------|
| S1 | **Reset baseline** | Temporary Subgraph Viewer empty; no stale chips; DAG badges cleared | Manual: click **Reset Workflow** before run | Ready for operator verification |
| S2 | **Run → Target temp** | Target node colour changes (running/complete per SPEC-017); `scan_name=target` chip appears in viewer | Manual: **Run Workflow**; optional `GET /api/v1/projects/{id}/contexts/temporary` | Ready for operator verification |
| S3 | **Exporting FINISHED → chip order** | Each `context.export: scan_graph` step FINISHED adds a chip in **production order** (`produced_at`: target, then subfinder, nmap, nerva, nuclei) while next step may already show RUNNING `0/n` | Manual: watch viewer during run; compare chip order to API `produced_at` | Ready for operator verification |
| S4 | **Progress badges `0/n` → `n/n`** | RUNNING step shows `0/n` on DAG node; FINISHED/skip shows `n/n`. Badge on YAML step node, not separate Composer chrome | Manual: watch DAG during run; optional status poll JSON | Partial — API tests prove fields; UI Ready for operator verification |
| S5 | **Export-only semantic edges** | **No** step→collector edge for HTTPX, Katana (`export: none`). **Yes** for Subfinder, Nmap, Nerva, Nuclei (`export: scan_graph`). Rank collector remains when any exporter on rank | Manual: inspect DAG layout; automated: `mapper.smoke.mjs` | Partial — YAML smoke OK; live embed Ready for operator verification |
| S6 | **Target collector alignment** | Target semantic-export collector X vertically aligns with Subfinder (first scan step) collector; offset applied once, not on other collectors | Manual: compare Target vs Subfinder collector columns in DAG | Partial — C4 smoke OK; live embed Ready for operator verification |
| S7 | **Readable labels** | Step shapes show `subfinder`, `nmap`, … not full `sfp_cli_*`; tooltips ~150% size | Manual: zoomed-out Composer embed view | Ready for operator verification |
| S8 | **No temp flash on FINISHED** | Viewer does not blank before new chip; no duplicate chips after Reset | Manual: watch viewer at each FINISHED transition | Ready for operator verification |
| S9 | **Reset terminal** | Reset empties viewer (no temps); **Run** re-enabled (`run_ready: true` per SPEC-017) | Manual: after terminal run, Reset; confirm empty + Run enabled | Ready for operator verification |
| S10 | **Nerva not skip_step** | When Nmap produced ip:port in graph, Nerva runs (not `skip_step` from empty input) | Manual: check step status / logs; automated: `test_nerva_argv_receives_ip_port_list` | Partial — GSE/argv tests pass; live run Ready for operator verification |
| S11 | **Nuclei inputs documented** | Nuclei either completes or fails with **non-empty bounded** `crawl_urls` (not mystery empty-input timeout). If timeout, logs show large `-l` list count | Manual: inspect Nuclei step logs / input file; see `SPEC018_A4_NUCLEI.md` | Partial — corpus proves 3411 URLs; live bounded-run Ready for operator verification |

### Exporting steps reference (12A)

| Step | `context.export` | Expect semantic-export edge | Expect temp chip on FINISHED |
|------|------------------|----------------------------|------------------------------|
| Target (seed) | scan_graph (ensure) | yes (Target collector) | yes (`target`) |
| Subfinder | scan_graph | yes | yes |
| Nmap | scan_graph | yes | yes |
| Nerva | scan_graph | yes | yes |
| HTTPX | none | **no** | no |
| Katana | none | **no** | no |
| Nuclei | scan_graph | yes | yes |

### Optional API checks during live run

```bash
# Temporary subgraph list (production order field)
curl -s "http://127.0.0.1:8001/api/v1/projects/{project_id}/contexts/temporary" | jq '.subgraphs[] | {scan_name, produced_at}'

# Workflow status with progress fields
curl -s "http://127.0.0.1:8001/api/v1/workflows/{workflow_id}/status" | jq '.steps[] | {step_id, scan_status, input_done, input_total}'
```

---

## Residual / out of scope (E1)

- **E2 GOV-08 exploratory review** ([#1297](https://github.com/brettforbes/spiderfeet/issues/1297), R18-19) is the **operator gate** — scenario matrix classification, persistence proof on refresh, and backlog hydration. E1 does not claim E2 complete.
- Live Nuclei on full Katana URL lists may exceed 900s wall clock; that is an operational/template-scope concern when inputs are proven non-empty (see `SPEC018_A4_NUCLEI.md`). Do not treat timeout alone as GSE failure.
- Host widget has no automated UI test harness; D1–D3 evidence is code-path + manual checklist until E2.

## Traceability

| Requirement | E1 evidence |
|-------------|-------------|
| R18-18 E2E smoke doc | this file |
| R18-01..05 GSE | automated tests + `SPEC018_A1_GSE_PROOF.md` |
| R18-06 persist-before-FINISHED | `test_persist_before_finished.py` |
| R18-07 progress fields | `test_workflow_status_input_progress.py` |
| R18-09..14 YAML DAG | `spec018.smoke.mjs` |
| R18-15..17 host Composer | code paths + manual scenarios S1–S11 |
| R18-19 GOV-08 | deferred to E2 (#1297) |
