# SPEC-016 — Workflow run robustness & per-project temporary context

**Status:** Draft (issues opened; awaiting lesser-agent execution)
**Source:** Operator request (2026-08-10) after live k2am runs — nuclei step failed silently on a 180s timeout; the temporary context is shared across every project and appears only after a full run finishes; the DAG target box needs a context port + a target-seeded context collector; and the temporary-context viewer needs tighter subgraph clustering plus clickable labels that centre their nodes.

**Parents (extends, does not replace):**
- Backend engine — `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`
- Projects & Composer refinement — `.governance/specs/SPEC-013-projects-composer-refinement.md`
- Workflow live status visualization — `.governance/specs/SPEC-015-workflow-live-status-viz.md`
- YAML DSL Workflow iFrame layout — `@yaml-workflow-widget/.governance/specs/SPEC-012-LAYOUT-RULES.md`

**Repos in scope (split delivery):**

| Repo | Role in this phase |
|------|--------------------|
| `spiderfeet` | Per-step nuclei timeout in the seed workflow + module default; non-blocking temporary-context export; per-project canonical context id resolution + PUT hardening; tests |
| `spiderfeet-widget` | Reload temporary context per project on switch; incremental per-step import on FINISHED; grouped subgraph clustering; clickable label chips that centre their nodes |
| `yaml-workflow-widget` | Right-edge context port on the Target box; a target context-collector node seeded from `inputs.targets`; docs/smoke |

**Issue indexes:**
- Backend — `.governance/project/SPEC016_ISSUE_INDEX.md`
- Widget — `@spiderfeet-widget/.governance/project/SPEC016_WIDGET_ISSUE_INDEX.md`
- YAML widget — `@yaml-workflow-widget/.governance/project/SPEC016_ISSUE_INDEX.md`

---

## 0. Operator-confirmed decisions

1. **Per-repo specs + issues.** One master spec (this file) plus three mirrored issue-index docs; epics/stories opened in each owning repo, cross-linked. (Operator, 2026-08-10.)
2. **Context appears incrementally.** Each step's nugget graph is imported into the temporary-context viewer the moment that step transitions to `FINISHED` during the status poll — not deferred to run completion. (Operator, 2026-08-10.)
3. **Temporary context is strictly per-project.** Switching the Composer project dropdown must clear the current temporary context and load the newly selected project's temporary context; switching back restores the prior project's context. The temporary context is never shared or leaked across projects.
4. **Target-first context.** When a workflow runs with a target, the first nodes/edges to arrive in the temporary context are the target values. The Target box carries a context port on its right edge, and all targets are copied to a context collector placed to the right of the target.

## 0.1 Root causes (verified during planning)

- **Nuclei `timeout after 180.0s`.** `modules_v2/sfp_cli_nuclei.py` uses `float(spec.get("timeout") or 180.0)` per batch (L381, L458). The nuclei step in `.seed/12A_Workflow_YAML_Example.yaml` (L335–365) sets **no** `config.timeout`, unlike nmap which sets `timeout: 900` (L109). A full-template pass over katana crawl URLs exceeds 180s and the run aborts `ERROR-FAILED`.
- **Temporary context shared across projects.** The viewer `spiderfeet-widget/src/js/composer-temp-graph.js` keeps a session-global in-memory store (`_subgraphs`, `_temporarySubgraphId`, L37–42). `Projects.openProjectInComposer` (`src/js/projects.js` L758–853) never clears or reloads it, and `SpiderfeetApi.getTemporaryContext(projectId)` (`src/js/spiderfeet-api.js` L576–587) is never called. `Composer.loadProjectContexts` is referenced (`composer.js` L1227) but never defined. On the backend, `spiderfeet_v2/api/routes/contexts.py` resolves the subgraph by `_first_subgraph_id` (projection-first, L52–61/75) and PUT trusts a client `temporary_subgraph_id` (L164–168) instead of the deterministic `temporary_subgraph_id_for(project_id)` (`engine/persist.py` L28–29).
- **Slow to appear.** Temp graphs import only after `run_state` is terminal (`composer.js` `_importWorkflowTempGraphs` L903–943, L1043–1062), then sequentially `getScanStep` per step. The 1s status poll updates DAG colours only. Additionally, temporary-context export ran on the step's worker thread and could block wave progression on large graphs (already mitigated on branch `fix/workflow-defer-temp-export`).
- **DAG target port/collector.** The diagram is the `yaml-workflow-widget` iframe (Vue + Nice-DAG). Step collectors exist (`mapper.js` `__ctxcol_*`); the Target box (`src/workflow-dag/components/TargetNode.vue`) has only in/out ports and no collector.
- **Viewer clustering/labels.** `composer.js` mounts the temp graph with `variant: 'default'` (L1746–1755); the `'grouped'` force-by-group variant in `canvas-graph.js` VARIANTS (L181–199) is unused. Label chips (`composer-temp-graph.js` `renderSubgraphToggles` L507–547) bind only a remove handler; `CanvasGraph` has no `centerOnNodes`.

---

## 1. Objective

Make a workflow run complete reliably and make its temporary context trustworthy and legible: nuclei (and any other long step) no longer dies on a too-short default timeout; the temporary context is per-project, arrives step-by-step as each step finishes, and is seeded target-first; and the viewer clusters each step's subgraph and lets the operator click a label to centre its nodes. On the DAG, the Target box shows a context port and a target-seeded context collector.

## 2. Non-goals

- Parallel step execution semantics (unchanged from SPEC-015; waves as-is).
- Changing what a scan produces (four forms / nugget graph) or the ontology.
- New OSINT modules.
- Reworking the project-context (persistent) graph beyond the same per-project id-resolution fix applied to temporary context.

---

## 3. Requirements

### Backend (`spiderfeet`) — Epic A

| ID | Requirement |
|----|-------------|
| R16-01 | **Per-step nuclei timeout.** Add `timeout: 900` to the nuclei step `config` in `.seed/12A_Workflow_YAML_Example.yaml`; raise the `sfp_cli_nuclei` module default from 180 to 300 as defence-in-depth (both single-run L381 and batched L458 paths); audit the other long steps (katana, nerva) and add explicit per-step timeouts where the module default is shorter than a realistic run. Reseed the affected seed workflows so live projects pick up the new YAML. |
| R16-02 | **Non-blocking temporary-context export.** The per-step temporary-context export must not block wave progression: run it off the step's critical path (daemon thread) and make the temporary-subgraph write best-effort (never raise). Land the change on branch `fix/workflow-defer-temp-export` (`engine/step_runner.py`, `engine/persist.py` `_write_temporary_context`) with its unit test via PR into `develop`. |
| R16-03 | **Per-project canonical context resolution.** In `spiderfeet_v2/api/routes/contexts.py`, resolve the temporary and project subgraph ids via `temporary_subgraph_id_for(project_id)` (import from `engine/persist.py`; add the project-context equivalent) as the canonical key, falling back to the projection id only when the canonical row is absent. In `PUT .../contexts/temporary`, reject or coerce a body `temporary_subgraph_id` that does not equal the project's canonical id, so one project can never write into another's subgraph. |
| R16-04 | **Tests, OpenAPI, docs.** Add context-route isolation tests (two distinct projects resolve to distinct subgraph ids and never bleed after writes); assert the seed nuclei step carries a `timeout`; keep `poetry run pytest` green for the touched suites. |

### Host widget (`spiderfeet-widget`) — Epic B

| ID | Requirement |
|----|-------------|
| R16-05 | **Per-project temporary context reload.** Define `Composer.loadProjectContexts(projectId)` and call it from `Projects.openProjectInComposer` and `restoreComposerFromStorage`. Add `ComposerTempGraph.loadFromServer(projectId)` using `SpiderfeetApi.getTemporaryContext`. Reset `_subgraphs` and null `_temporarySubgraphId` in `clear()`; ensure `buildServerPayload` never sends a cross-project id. Result: switching projects clears and reloads the temporary context; switching back restores it. |
| R16-06 | **Incremental import on FINISHED.** During `startStatusPoller` `onUpdate`/`setStepStatuses`, when a step transitions to `FINISHED`, immediately import that step's graph (reuse the per-step import path) instead of waiting for the terminal `run_state`; dedupe so the terminal importer does not double-add; parallelize the per-step `getScanStep` fetches. |
| R16-07 | **Subgraph clustering.** Mount the temp-subgraph CanvasGraph with `variant: 'grouped'` (and/or strengthen the polar offsets in `toCanvasGraph`) so each imported step's subgraph clusters visibly rather than dispersing. |
| R16-08 | **Clickable labels centre nodes.** Add `Viz.CanvasGraph.centerOnNodes(ids)` (compute the bbox of the matching nodes and apply a `d3.zoom` transform to centre/fit them). Make the label chips in `renderSubgraphToggles`/`bindUi` clickable (distinct from the remove control) so selecting a label centres that subgraph's nodes/edges in the view. |

### YAML widget (`yaml-workflow-widget`) — Epic C

| ID | Requirement |
|----|-------------|
| R16-09 | **Target right-edge context port.** Add a context port on the right edge of the Target box in `src/workflow-dag/components/TargetNode.vue`, reusing the existing `.wf-connector-context-right` style from `ports.css`; set `target.data.contextSide = 'right'` so `portCentre(..., "ctx")` anchors on the right edge. |
| R16-10 | **Target context collector.** In `mapper.js` (`workflowDocToNiceDagModel`, ~L146–165 inside the `hasInputs` block), create a target collector node (e.g. `__ctxcol_target__`, `dependencies: [__workflow_target__]`, semantic-export `edgeMeta`) seeded from `doc.inputs.targets`, chained as the first collector in the rail. Position it in `workflowSeedRoles.js` at `layoutCx = CX + TARGET_W/2 + COLLECTOR_GAP` on the target's row (same `layoutCy`, no new rank). Anchor the `Target.ctx → collector` edge in `workflowSeedEdgePoints.js` (mirror the step→collector branch). The collector is diagram chrome and is stripped from the YAML round-trip. |
| R16-11 | **Docs + smoke.** Update the relevant layout/host docs (`SPEC-012-LAYOUT-RULES.md` note, `HOST_PROTOCOL.md`/`EMBED_GUIDE.md` if the collector is host-visible) and add/extend a smoke that asserts the target context port and collector render on 12A without shifting existing step coordinates. |

### Integration + acceptance — Epic D

| ID | Requirement |
|----|-------------|
| R16-12 | **Cross-repo E2E smoke.** With API + widget + yaml widget running, re-run k2am end-to-end: nuclei FINISHED (no 180s abort); temporary context isolates per project on dropdown switch and restores on switch-back; nuggets appear step-by-step as each step finishes, target values first; the DAG shows the target context port + collector; subgraphs cluster and label chips centre their nodes. Evidence recorded. |
| R16-13 | **GOV-08 exploratory review** of the above (scenario matrix: full run, nuclei timeout regression, project switch isolation both directions, incremental appearance, target-first seeding, DAG port/collector render, clustering, label centring) classified with tracked follow-ups. **[OPERATOR GATE]** |

---

## 4. Execution order & cross-repo dependencies

```
Backend:  A1 (nuclei timeout) ∥ A2 (non-block export, branch exists) ∥ A3 (per-project resolution) → A4 (tests/docs)
Host:     B1 (per-project reload, needs A3) → B4 ; B2 (incremental import) ; B3 (clustering) ; B4 (label centre)
YAML:     C1 (target port) → C2 (collector) → C3 (docs/smoke)
Integr.:  D1 (needs A4,B*,C3) → D2 (OPERATOR GATE)
```

- Hard cross-repo edge: host **B1** (per-project reload) is most robust once backend **A3** lands the canonical id resolution.
- Unblockers to start first, in parallel lanes: backend **A1/A2/A3**, YAML **C1**, host **B2/B3**.

## 5. Governance & lesser-agent execution

- One issue at a time per repo. For each issue: branch `fix/<n>-<slug>` (or `feature/`,`chore/`,`docs/`) from `develop` → smallest coherent change → verify → PR into `develop` → close the issue with a completion note + evidence → merge → return the repo to `develop` before the next (GOV-02).
- Verification bar = build + lint + targeted unit/smoke tests + a manual UI note. Full live end-to-end is deferred to Epic D (D1 smoke, D2 operator-gate review).
- Schema/DB work follows `.cursor/skills/typedb/SKILL.md`. YAML widget work integrates via the documented postMessage contract; do not change frozen 12A/12A2 step coordinates — only add the target port + collector.
- Commit/merge only per each repo's operator-approved policy.

## 6. Traceability

Requirement IDs `R16-01`…`R16-13`. GitHub epics/issues tagged `[SPEC-016]` in each repo; the three issue-index docs hold the ID → epic → issue → status map. Milestone "done" = the operator can run k2am and watch per-project temporary context fill in step-by-step (target first), nuclei completes, the DAG shows a target context port + collector, and viewer labels centre their subgraphs.
