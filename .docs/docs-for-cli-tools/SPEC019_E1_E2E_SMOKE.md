# SPEC-019 E1 — Cross-repo E2E smoke matrix (R19-13)

Evidence that SPEC-019 program fixes are covered by **automated tests and fixtures**. A live Composer Run is optional supporting evidence; it is **not** required when this matrix is green.

## How to run (spiderfeet)

From repo root with the project venv active:

```bash
python -m pytest \
  spiderfeet_v2/workflow/tests/test_gse_ip_port_host_scope.py \
  spiderfeet_v2/workflow/tests/test_gse_12a_chain.py \
  spiderfeet_v2/workflow/tests/test_gse_nerva_list_fixture.py \
  modules_v2/tests/test_sfp_cli_nerva.py::test_run_hydrates_jsonl_from_output_file \
  modules_v2/_core/tests/test_spec019_f3_subfinder.py \
  modules_v2/_core/tests/test_spec019_f4_httpx.py \
  modules_v2/_core/tests/test_spec019_f5_katana.py \
  modules_v2/_core/tests/test_spec019_f7_nerva.py \
  modules_v2/_core/tests/test_spec019_f8_validator.py \
  modules_v2/tests/test_sfp_cli_nuclei.py::test_progress_totals_one_to_twenty_urls_one_batch_r19_08 \
  -q
```

## How to run (yaml-workflow-widget)

After D3 lands on `develop`:

```bash
node src/workflow-dag/spec019.smoke.mjs
node src/workflow-dag/components/mapper.smoke.mjs
node src/workflow-dag/components/workflowSeedEdgePoints.smoke.mjs
```

## Scenario matrix

| Scenario | Expected outcome | Automated evidence |
|----------|------------------|-------------------|
| Two-host Nmap → Nerva fingerprints | `ip_port_list` is host-scoped; count matches real open ports (no cross-host cartesian product) | `test_gse_ip_port_host_scope.py::test_ip_port_list_no_cross_host_cartesian`; `test_gse_12a_chain.py::test_nmap_ip_port_list_non_empty_on_corpus` |
| Nerva graph hydrated from `--output` | Empty stdout with JSONL on disk still yields records + non-empty graph (not clean-miss SUCCESS) | `modules_v2/tests/test_sfp_cli_nerva.py::test_run_hydrates_jsonl_from_output_file` |
| Nuclei `i/n` batching | URL lists batch (e.g. 45 URLs → 3 batches; 1–20 URLs → 1 batch) | `test_gse_12a_chain.py::test_nuclei_45_urls_three_batches_r19_09`; `test_sfp_cli_nuclei.py::test_progress_totals_one_to_twenty_urls_one_batch_r19_08` |
| Nuclei / Katana `crawl_urls` | No bare `DOMAIN_NAME` hostname strings in crawl URL list | `test_gse_12a_chain.py::test_katana_crawl_urls_excludes_domain_name_r19_09` |
| YAML collectors | Nmap/Nerva ranks export via `semantic-export`; HTTPX/Katana absent from `collector.dependencies` | `yaml-workflow-widget`: `spec019.smoke.mjs` (D3); `mapper.smoke.mjs` (no httpx/katana semantic edges) |
| Subfinder hierarchy | COMPANY → DOMAIN_NAME(apex) → SUBDOMAIN | `test_spec019_f3_subfinder.py`; F8 `validate_apex_domain_company_parent` |
| HTTPX / Katana URL placement | HTTP status + homepage under apex/subdomain; crawl URLs under matching hosts | `test_spec019_f4_httpx.py`; `test_spec019_f5_katana.py` |
| Nerva apex wrap | Scan target domain under COMPANY | `test_spec019_f7_nerva.py`; F8 validator on adapter graphs |

## Cross-repo wiring (12A)

- **Backend GSE / step runner:** `spiderfeet_v2/workflow/tests/test_gse_12a_chain.py`, fixtures under `spiderfeet_v2/workflow/tests/fixtures/`.
- **Workflow diagram:** `@yaml-workflow-widget` mapper + `spec019.smoke.mjs` on `.seed/12A_Workflow_YAML_Example.yaml` (same document id as backend 12A tests).

## Out of scope (E1)

- **E2 (#1331)** operator GOV-08 exploratory gate — not part of this evidence bundle.
- Re-opening SPEC-017 temp subgraph persistence or SPEC-018 FINISHED semantics.

## Sign-off

When the pytest and node smoke commands above pass on `develop`, E1 acceptance is satisfied for R19-13.
