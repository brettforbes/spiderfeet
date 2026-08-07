# SPEC-007 agent plan — CLI Workflow DSL + runtime foundation

**Spec:** `.governance/specs/SPEC-007-cli-workflow-dsl.md`  
**Seed:** `.seed/12A_Workflow_YAML_Example.yaml`, `.seed/12B_Workflow_DSL_Description.md`, `.seed/12C_Graph_Select_Language.md`  
**Issue index:** `.governance/project/SPEC007_ISSUE_INDEX.md`  
**Audience:** Lesser agents — **one child issue at a time**

---

## How to pick up work (every agent)

1. Read this plan’s epic section for your issue code + the GitHub issue body + SPEC-007 requirement IDs.
2. Read **12B** (logic) and **12C** (GSE) end-to-end before changing schema or evaluator behaviour.
3. Branch from `develop`: `feature/<issue>-<slug>`.
4. Implement **only** that child scope.
5. Run the verification commands on the issue; paste evidence in an issue comment.
6. Open PR to `develop` linking the issue; after merge, closing comment with paths + test output.
7. **Forbidden:** redesign GSE operators without updating 12C + schema together; invent nugget ids; parse CLI text for variables; implement Langium/Monaco/visual sync; rewrite `sfp_*`; invent Nexus; skip structured-first / graph-mandatory laws.

---

## Architecture target (do not invent alternatives)

```text
.seed/12A_Workflow_YAML_Example.yaml     → canonical authoring example
.seed/12B_Workflow_DSL_Description.md    → logic master
.seed/12C_Graph_Select_Language.md       → GSE normative semantics

.seed/scripts/cli_workflow/
  README.md
  schema/
    workflow_v1.schema.json
    gse_v1.schema.json
  core/
    models.py            → dataclasses for Workflow, Step, GseSelect
    loader.py            → YAML load + schema validate + DAG check
    graph_index.py       → adjacency for contains/had/listens-to
    gse_eval.py          → evaluate select/for_each/union
    variables.py         → $workflow / $step / $steps resolution
    context_export.py    → merge nodes/edges uniquely
    normalize.py         → hostname_from_url etc.
  runtime/
    executor.py          → schedule DAG, run steps
    tempfile_mgr.py      → auto input/output files
    result_bundle.py     → persist step graphs + vars + context
  tools/
    registry.py          → tool.<id> → driver
    base.py              → driver protocol
    drivers/             → thin CLI wrappers → adapter graph build
  fixtures/              → tiny graphs for unit tests (optional)
  cli.py                 → validate / gse-eval / dry-run entrypoints

.tests/test_cli_workflow_*.py
```

**Reuse:** SPEC-004 adapters under `.seed/scripts/cli_corpus/adapters/` + `rules/<tool>/mapping.yaml` for scan graph production. Do not fork mapping logic into cli_workflow.

---

## Epic map

| Epic | Code | Intent | Children |
|------|------|--------|----------|
| Schema + seed freeze | P | Lock 12A/12B/12C + JSON Schemas | P0–P2 |
| GSE engine | Q | Index + evaluator + fixture tests | Q1–Q3 |
| Loader + variables | R | Parse, DAG, env resolution | R1–R3 |
| Runtime + context | S | Executor, temps, context merge, dry-run | S1–S4 |
| Tool drivers + E2E | T | Registry, 6 example drivers, dry E2E of 12A | T1–T3 |
| Docs + handoff | U | README, AGENTS, continuity, operator note | U1–U2 |

**Execution order:**

```text
P0 → P1 → P2
  → Q1 → Q2 → Q3
  → R1 → R2 → R3
  → S1 → S2 → S3 → S4
  → T1 → T2 → T3
  → U1 → U2
```

P0 may start immediately (schemas already stubbed). Q* must not change 12C semantics without a docs PR. T2 (live CLI drivers) may lag T3 (dry-run E2E) — prefer dry-run first.

---

## Epic P — Schema + seed freeze

### P0 — Inventory + gap note vs sketch

**Do**

1. Confirm 12A/12B/12C exist and cross-link.
2. Write `.governance/project/SPEC007_SKETCH_GAP_NOTES.md` listing every sketch defect that 12A/12C fixed (for reviewers).

**Done when:** Gap notes file checked in.

**Verify:** File lists concat/SUBDOMAIN/sum/sequence/sfp_*/shell-string issues.

### P1 — `workflow_v1.schema.json`

**Do**

1. Author JSON Schema covering `apiVersion`, `info`, `inputs`, `steps[]` fields per 12B §4.
2. Ensure 12A validates; add a deliberate invalid fixture that fails.

**Verify:**

```bash
poetry run python -m cli_workflow.cli validate .seed/12A_Workflow_YAML_Example.yaml
# or pytest .tests/test_cli_workflow_schema.py -q
```

### P2 — `gse_v1.schema.json`

**Do**

1. Schema for select / for_each / collect / emit / union / from_var / literal / where.
2. Extract GSE fragments from 12A and validate each.

**Verify:** pytest schema tests green; invalid `concat({{IP}})` sample rejected.

---

## Epic Q — GSE engine

### Q1 — `graph_index.py`

**Do**

1. Build out/in adjacency keyed by relation.
2. Implement `reachable(node, relation, transitive)`.

**Verify:** Unit tests on a 5-node handmade graph.

### Q2 — `gse_eval.py` simple select + where

**Do**

1. Implement match, where related/not, project, distinct, union.
2. Fixture test: subfinder corpus → `apex_domains` / `subdomains` logic from 12A.

**Fixture:**  
`.docs/docs-for-cli-tools/nugget_structure/subfinder_corporate_upside_au_passive_cs_proposed_nuggets_edges.json`

**Verify:** Both lists non-empty; intersection empty; union == all DOMAIN_NAME data (or document intentional filter diffs).

### Q3 — `gse_eval.py` for_each product

**Do**

1. Implement for_each + collect + emit.product/join.
2. Fixture test: nmap corpus → `ip_port_list` contains strings matching `\d+\.\d+\.\d+\.\d+:\d+`.

**Fixture:**  
`.docs/docs-for-cli-tools/nugget_structure/nmap_tcp_top_ports_permissive_proposed_nuggets_edges.json`

**Verify:** At least one `ip:port`; every port appears only paired with IPs under the **same** endpoint (spot-check one HOST).

---

## Epic R — Loader + variables

### R1 — models + loader

**Do**

1. Dataclasses / typed dicts for WorkflowDocument.
2. Load YAML → validate schema → build step map.

**Verify:** 12A loads; missing `id` fails.

### R2 — DAG validation

**Do**

1. Detect cycles, unknown `needs`, duplicate step ids.
2. Compute topological waves (parallel sets).

**Verify:** Cycle fixture fails; 12A yields wave0=`sfp_cli_subfinder`, wave1=`sfp_cli_nmap|sfp_cli_httpx`, etc.

### R3 — `variables.py` + `normalize.py`

**Do**

1. Resolve `$workflow.inputs.targets`, `$steps.x.vars.y`, `$step.scan_graph`.
2. `hostname_from_url` strips scheme/path.

**Verify:** `https://example.com/a` → `example.com`.

---

## Epic S — Runtime + context

### S1 — tempfile manager

**Do**

1. Auto write `line_text` input files from string lists.
2. Allocate output paths; cleanup policy documented (keep on failure).

**Verify:** Temp file line count == list length.

### S2 — context merge

**Do**

1. `merge_graph(context, scan_graph)` unique nodes by id, edges by triple.
2. `export: none` no-op.

**Verify:** Merging same graph twice does not duplicate nodes.

### S3 — executor skeleton

**Do**

1. Walk DAG waves; for each step call a **injected** runner protocol (interface only).
2. Persist `ResultBundle` (JSON) with vars + graphs + context.

**Verify:** With mock runner returning fixture graphs, 12A dry path fills vars.

### S4 — dry-run CLI

**Do**

1. `python -m cli_workflow.cli dry-run --workflow 12A --fixtures-map <yaml>`  
   Map each step id → path of `*_proposed_nuggets_edges.json`.
2. Skip live CLI; run GSE + context only.

**Verify:** Context contains nodes from subfinder+nmap+nerva+nuclei fixtures only (not httpx/katana).

---

## Epic T — Tool drivers + E2E

### T1 — registry + base driver protocol

**Do**

1. `ToolDriver.run(argv, files) -> CaptureResult`.
2. Registry resolves `tool.nmap` etc.; unknown tool errors clearly.

**Verify:** Registry unit test.

### T2 — Drivers for example tools (optional live)

**Do**

1. Thin drivers: subfinder, nmap, nerva, httpx, katana, nuclei.
2. Each: run CLI when binary present; always support “structured path provided” for CI.
3. Call existing adapters to build scan_graph.

**Verify:** At least one driver integration test skipped-if-missing-binary; adapter call unit-tested with recorded structured artifact.

**Note:** Live network scans are **not** required to close T2 if dry-run + adapter unit tests pass. Document binary requirements in README.

### T3 — Dry E2E of 12A

**Do**

1. Fixture map for all six steps using existing corpus graphs.
2. Assert key vars exist; context export policy holds.
3. Write result bundle under `.docs/docs-for-cli-tools/workflow_runs/` (gitignored or small golden summary only).

**Verify:** pytest e2e dry-run green on CI without network.

---

## Epic U — Docs + handoff

### U1 — Package README + AGENTS.md pointer

**Do**

1. README: architecture, CLI commands, how to add a driver, how to author GSE.
2. AGENTS.md table row for SPEC-007 + seed docs.

### U2 — Continuity + operator checklist

**Do**

1. `.governance/project/continuity/SPEC007_FOUNDATION.md`
2. Checklist: validate 12A, run GSE fixture tests, dry-run E2E.

---

## Definition of done (program)

- [ ] All P–U children merged to `develop`
- [ ] 12A schema-valid
- [ ] GSE nmap + subfinder fixture tests green
- [ ] Dry-run E2E of example workflow green without live CLI
- [ ] No Langium/Monaco/visual code in this SPEC
- [ ] Continuity handoff written

## Future (explicitly NOT SPEC-007)

| Phase | Work |
|-------|------|
| 2 | Langium grammar for workflow+GSE → AST |
| 3 | Monaco embed in widget |
| 4 | Workflow visualisation library + annotations |
| 5 | Bidirectional AST ↔ diagram transformer |
| 6 | Context force-graph UI (connect/disconnect/delete) |
| 7 | Bridge `sfp_*` / FastAPI modules onto the same DSL |
