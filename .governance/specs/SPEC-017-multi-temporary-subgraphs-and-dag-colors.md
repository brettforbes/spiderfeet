# SPEC-017 — Multi temporary subgraphs (TypeDB-first) + YAML DAG color settings

**Status:** Ready for lesser-agent execution (CP1+CP2 complete 2026-08-12)
**Source:** Operator request (2026-08-12) — architectural change from one merged temporary context blob to many TypeDB `temporary_subgraph` rows per project; Temporary Subgraph Viewer becomes a read-only consumer; YAML DSL settings gain hex+picker for status and edge colors with new defaults.

**Parents (extends, does not replace):**
- SpiderFeet v2 engine — `.governance/specs/SPEC-010-spiderfeet-v2-engine.md`
- Projects & Composer — `.governance/specs/SPEC-011-composer-projects-ui.md` / SPEC-013
- Workflow live status — `.governance/specs/SPEC-015-workflow-live-status-viz.md`
- Per-project context robustness — `.governance/specs/SPEC-016-workflow-run-robustness-and-per-project-context.md`
- YAML layout — `@yaml-workflow-widget/.governance/specs/SPEC-012-LAYOUT-RULES.md`

**Repos in scope:**

| Repo | Role |
|------|------|
| `spiderfeet` | Schema repair; multi-row temp persist; target materialize; list API; reset deletes all temps; engine-only writes |
| `spiderfeet-widget` | Read-only viewer from list API; reload on FINISHED / project switch; cluster icon; Run disabled until Reset; chips centre-only |
| `yaml-workflow-widget` | Hex + picker for status + 3 edge types; new default colors |

**Issue indexes:**
- Backend — `.governance/project/SPEC017_ISSUE_INDEX.md`
- Widget — `@spiderfeet-widget/.governance/project/SPEC017_WIDGET_ISSUE_INDEX.md`
- YAML widget — `@yaml-workflow-widget/.governance/project/SPEC017_ISSUE_INDEX.md`
- Agent plan — `.governance/project/SPEC017_AGENT_PLAN.md`

---

## 0. Operator-confirmed decisions (grill, 2026-08-12)

1. **Many TypeDB `temporary_subgraph` relations per project** — one per semantic export (and one for target). Retire the single uuid5-per-project merged blob as source of truth.
2. **Per-node canvas identity ≠ subgraph identity.** Each node gets `temporary_id = temporary--<uuidv4>`; edges remap to those ids so uuid5 `nugget_instance_id` overlaps can coexist on one canvas. TypeDB key remains `temporary_subgraph_id = temporary-subgraph--<uuidv4>` (one id per subgraph relation holding many nodes/edges). Stamp `source` = `scan_name` on nodes and edges.
3. **Reset Workflow** deletes **all** project temporary subgraphs and all current scan-step results. It does **not** re-create a target temporary subgraph — viewer is empty until the next Run / Scan Now.
4. **Run Workflow stays disabled** after a run completes/aborts until **Reset Workflow** is pressed.
5. **Target temporary subgraph on first Run / Scan Now only** (not on project open): when **Run Workflow** or the first **Scan Now** is pressed — the same moment the DAG Target node colour state changes — upsert `target_context` and create a project `temporary_subgraph` with `scan_name = target`. Project open / Composer load must not create that temp row.
6. **On exporting step FINISHED:** wave control and DAG colour updates must not wait on temp persist; engine copies `scan_result_graph` → new `temporary_subgraph`; viewer re-GETs the project temp list.
7. **Engine/API owns writes;** Temporary Subgraph Viewer is **read-only** (no client PUT of temp graphs as source of truth).
8. **This phase persists `json_string`** (viewer-ready `{nodes,edges}` with stamps). Native nugget/edge duplication into temp is out of scope.
9. **`scan_name`** = YAML step key (e.g. `subfinder_enum`); target uses `target`. `scan_description` from YAML `description` when present.
10. **Chips:** centre-on-click only; remove delete control. Clearing is via Reset Workflow only.
11. **YAML colors:** picker **and** hex text for 4 status + 3 edge types; same hex defaults for light and dark themes:

| Token | Hex |
|-------|-----|
| waiting | `#FFFF99` |
| running | `#F2AA84` |
| complete | `#4E95D9` |
| failed | `#FF7979` |
| semantic-export | `#78206E` |
| used-by | `#E97132` |
| followed-by | `#156082` |

---

## 0.1 Root causes / schema gaps (verified in planning)

- SPEC-016 kept one canonical `temporary_subgraph_id_for(project_id)` (uuid5) and merged exports into one blob (`engine/persist.py`, `api/routes/contexts.py`). Viewer also client-merged and PUT back.
- Schema sketch already has multi-row `temporary_subgraph` + `target_context` (`.seed/spiderfeet_v2_semantic.tql` L26–37) but is **not load-safe**: `scan_name`, `scan_description`, `target_nugget_type` are owned without attribute definitions; `scan_step` does not `plays temporary_subgraph:scan_step`.
- YAML settings already have status color pickers (`statusColors.js`) but no hex text field and no edge-type color pickers (`edgeMeta.js` EDGE_COLORS are code-only).

---

## 1. Objective

Make temporary context TypeDB-first and multi-subgraph: every exporting scan (and the target) becomes an independent `temporary_subgraph` addressable by `scan_name`, loadable in one project list API call, and visualised as discrete stamped graphs in the Temporary Subgraph Viewer. Reset clears the set; Run cannot restart until Reset. Separately, YAML DSL settings let operators set status and edge colours via picker or hex with the new defaults.

## 2. Non-goals

- Materializing duplicate native nugget/edge entities into every temporary_subgraph (json_string only this phase).
- Changing scan four-form production or ontology catalogues.
- Project Context Viewer (persistent) redesign beyond leaving it alone.
- Client-side editing/deletion of individual temp subgraphs.
- Parallel wave semantics changes.

---

## 3. Requirements

### Backend (`spiderfeet`) — Epic A

| ID | Requirement |
|----|-------------|
| R17-01 | **Schema load-safe.** Repair `.seed/spiderfeet_v2_semantic.tql`: define `scan_name`, `scan_description`, `target_nugget_type` (and any other missing attribute decls); add `scan_step plays temporary_subgraph:scan_step`; keep/extend `project_temporary_subgraph_ids` for multi-row; load cleanly on a scratch DB per typedb skill checklist; document reload notes for `spiderfeet-actual`. |
| R17-02 | **Per-export temporary_subgraph write.** When a step with semantic export to context finishes and four forms exist, copy `scan_result_graph` into a **new** `temporary_subgraph` (uuid4 id), stamp every node with `temporary_id=temporary--<uuidv4>` and `source=<scan_name>`, remap edges to those ids and stamp `source`, persist as `json_string`, link `project` + `scan_step`, set `scan_name` / `scan_description`. Non-blocking / best-effort (must not stall waves). Retire merge-into-singleton uuid5 as the write path. |
| R17-03 | **Target materialize on Run / Scan Now.** When `run_workflow` or `run_single_step` starts for a project (live, not dry-run), upsert `target_context` from target nugget(s) and create a project `temporary_subgraph` with `scan_name=target` if one is not already present. Must **not** run on project-open / `GET …/complete`. Host reloads the temp list when the run/scan starts so the viewer shows the target as the DAG Target colour changes. |
| R17-04 | **List temporary contexts API.** `GET` for a project returns `{ subgraphs: [{ temporary_subgraph_id, scan_name, scan_description, nodes, edges }] }` for **all** project temps. Deprecate or no-op the old merged PUT as source of truth. **Reset** deletes every project `temporary_subgraph` and clears scan steps/results; it does **not** re-seed a target temp (R17-03). |
| R17-05 | **Run-until-reset contract.** After a workflow run reaches a terminal state, the host must not treat Run as available until Reset succeeds. Backend reset remains the wipe+reseed authority; document/status fields the host needs if any beyond existing reset/status endpoints. |
| R17-06 | **Tests + OpenAPI.** Cover multi-row create, list shape, reset wipe+target reseed, no client-id cross-project write; OpenAPI updated; targeted pytest green. |

### Host widget (`spiderfeet-widget`) — Epic B

| ID | Requirement |
|----|-------------|
| R17-07 | **Read-only multi-subgraph load.** `ComposerTempGraph` + `SpiderfeetApi` consume the list payload; clear then render all subgraphs; remove outbound PUT sync as source of truth; remove chip delete control; chips label by `scan_name`/`source` and centre via existing `centerOnNodes`. |
| R17-08 | **Reload on FINISHED + project switch.** When a step transitions to FINISHED during status poll, re-GET the project temporary list (do not client-merge scan_step graphs). Project dropdown: empty viewer, load workflow, load temps. |
| R17-09 | **Cluster icon.** Title-bar icon packs subgraphs close with small separation so most data fits fullscreen without overlap; complements label-centre. |
| R17-10 | **Run disabled until Reset.** After run terminal, keep Run Workflow disabled until Reset Workflow completes successfully; Reset clears viewer then reloads target-seeded temps from API. |

### YAML widget (`yaml-workflow-widget`) — Epic C

| ID | Requirement |
|----|-------------|
| R17-11 | **Status colors: hex + picker + defaults.** Settings: color picker and hex text (`#RRGGBB`) for waiting/running/complete/failed; defaults both themes = operator hexes; persist localStorage. |
| R17-12 | **Edge colors: hex + picker + defaults.** Same for followed-by / used-by / semantic-export; wire into `resolveEdgeColor` / legend; both themes; persist. |
| R17-13 | **Docs + smoke.** Note settings UX + defaults in widget docs; smoke/assert defaults or settings round-trip as appropriate. |

### Integration — Epic D

| ID | Requirement |
|----|-------------|
| R17-14 | **E2E smoke evidence.** Open project → viewer empty of temps → Run or Scan Now → target temp appears with DAG Target colour change → each exporting FINISHED grows list via GET → labels centre → cluster icon → Reset wipes (empty viewer) + Run re-enabled. Doc under `.docs/docs-for-cli-tools/`. |
| R17-15 | **GOV-08 exploratory review** with scenario matrix. **[OPERATOR GATE]** |

---

## 4. Execution order & dependencies

```
Backend:  A1 (schema) → A2 (export write) ∥ A3 (target materialize) → A4 (list API + reset) → A5 (run-until-reset contract) → A6 (tests)
Host:     B1 (needs A4) → B2 ; B3 ; B4 (needs A5 signals / reset path)
YAML:     C1 ∥ C2 → C3
Integr.:  D1 (needs A6,B*,C3) → D2 (OPERATOR GATE)
```

Hard edge: host **B1/B2** require backend **A4** list API. YAML **C*** is independent.

## 5. Governance & lesser-agent execution

- One issue at a time per repo. Branch from `develop` → PR into `develop` → close with evidence → merge → return to `develop` (GOV-02).
- Schema/DB: `.cursor/skills/typedb/SKILL.md`.
- Do not reintroduce client PUT as source of truth.
- Commit/merge only per operator-approved policy.
- Full live E2E deferred to Epic D.

## 6. Traceability

Requirement IDs `R17-01`…`R17-15`. Issues tagged `[SPEC-017]`. Milestone “done” (except D2) = operator can open a project (empty temp viewer), press Run/Scan Now and see the target temp appear with the Target colour change, watch per-step temps appear via API reload, cluster/centre subgraphs, reset to clear (no auto re-seed), and use new YAML color settings.
