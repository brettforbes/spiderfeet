# SPEC-013 issue index — backend (`spiderfeet`)

**Spec:** `.governance/specs/SPEC-013-projects-composer-refinement.md`
**Repo:** `brettforbes/spiderfeet` · integration branch `develop`
**Skill (mandatory for schema work):** `.cursor/skills/typedb/SKILL.md`

Status legend: `planned` (issue text ready) → `open` (created on GitHub) → `in progress` → `in review` → `done`.

| Code | Issue | Requirement | Depends on | Status |
|------|-------|-------------|------------|--------|
| Epic B1 — Project schema, CRUD & API alignment | [#1151](https://github.com/brettforbes/spiderfeet/issues/1151) | R13-01..03 | — | open |
| B1-1 — Schema: project entity + workflow relates project + declare attrs | [#1154](https://github.com/brettforbes/spiderfeet/issues/1154) | R13-01 | — | open |
| B1-2 — Flip Python layer to new direction + project attrs | [#1155](https://github.com/brettforbes/spiderfeet/issues/1155) | R13-02 | B1-1 | open |
| B1-3 — Align project API models (no required workflow_ids) | [#1156](https://github.com/brettforbes/spiderfeet/issues/1156) | R13-03 | B1-2 | open |
| Epic B2 — YAML⇄TypeDB round-trip & project lifecycle API | [#1152](https://github.com/brettforbes/spiderfeet/issues/1152) | R13-04..06 | B1 | open |
| B2-1 — Create-new-project service (entity + info-only workflow) | [#1157](https://github.com/brettforbes/spiderfeet/issues/1157) | R13-04 | B1-3 | open |
| B2-2 — `PUT /workflows/{id}` re-parse (replace bundle) | [#1158](https://github.com/brettforbes/spiderfeet/issues/1158) | R13-05 | B1-3 | open |
| B2-3 — `GET /projects/{id}/complete` (workflow_yaml inline) | [#1159](https://github.com/brettforbes/spiderfeet/issues/1159) | R13-06 | B1-3 | open |
| Epic B3 — Seed 5 projects + verification | [#1153](https://github.com/brettforbes/spiderfeet/issues/1153) | R13-07..09 | B2 | open |
| B3-1 — Idempotent seed script for 5 projects (fully materialized, no results) | [#1160](https://github.com/brettforbes/spiderfeet/issues/1160) | R13-07 | B2-1..3 | open |
| B3-2 — Seed verification query (OPERATOR GATE) | [#1161](https://github.com/brettforbes/spiderfeet/issues/1161) | R13-08 | B3-1 | open |
| B3-3 — pytest coverage for B1/B2 + seed smoke | [#1162](https://github.com/brettforbes/spiderfeet/issues/1162) | R13-09 | B3-1 | open |

## Execution order

```
B1-1 → B1-2 → B1-3 → (B2-1 ∥ B2-2 ∥ B2-3) → B3-1 → (B3-2 ∥ B3-3)
```

## Per-issue detail

### B1-1 — Schema: project entity + workflow relates project + declare attrs (R13-01)
- **Files:** `.seed/spiderfeet_v2_semantic.tql` (attribute defs block ~L778–832; `project` **entity** ~L738–746; `workflow` **relation** ~L707–718; `project_workflow_ids` + related **functions** ~L914–918), `spiderfeet_v2/db/bootstrap.py` (reload path).
- **Do:** add `attribute project_name, value string; attribute project_description, value string; attribute project_created, value datetime;`. Confirm the operator-revised shape is complete: `entity project` (`plays workflow:project`, `plays project_context:project`, `plays temporary_subgraph:project`) and `relation workflow` with `relates project @card(0..1)`. Update the `project_workflow_ids` schema function (and any that walked `project` → `workflow`) to the new direction (`$w isa workflow, links (project: $p)`).
- **Verify:** schema loads via a TypeDB schema transaction / `typeql-check`; `match $p isa project; limit 1;` and `match $w isa workflow, links (project: $p); limit 1;` succeed (empty OK). Follow the typedb skill load checklist. Document the data-safe reload for a populated `spiderfeet-actual`.
- **Note:** the operator changed `project` from relation → entity on 2026-08-09 — finish this shape, don't revert to the relation form.

### B1-2 — Flip Python layer to new direction + project attrs (R13-02)
- **Files:** `spiderfeet_v2/db/crud.py` (`PROJECT_ATTRS` ~L41–44; `create/get/update/list_project` ~L627–745 — currently insert/query project as a **relation** with `links (workflow: ...)`, which is now wrong), `spiderfeet_v2/workflow/typedb_convert.py` (workflow forms), `spiderfeet_v2/db/projections.py` (`get_project` ~L122–150).
- **Do:** `PROJECT_ATTRS = ("stix_incident_id", "project_name", "project_description", "project_created")`. Rewrite `create_project` to insert `$p isa project` (entity) with attrs only; link workflows by giving each `workflow` relation `links (project: $p)`. Rewrite `get_project`/`list_projects`/`update_project` to find workflows via `$w isa workflow, links (project: $p); $w has workflow_id $v`. Add optional `project` link to the workflow forms in `typedb_convert.py`.
- **Verify:** unit test create→get→update→list a project (entity) with all attrs and 0..N linked workflows.

### B1-3 — API model alignment (R13-03)
- **Files:** `spiderfeet_v2/api/schemas.py` (`ProjectCreate/Update/Out` ~L168–192), `spiderfeet_v2/api/routes/projects.py`.
- **Do:** expose `project_name`, `project_description`, `project_created`, optional `stix_incident_id`. `ProjectCreate` no longer requires `workflow_ids` (an entity project is valid standalone); `ProjectOut.workflow_ids` is derived from workflows that link the project.
- **Verify:** OpenAPI shows new fields; existing projects route tests pass.

### B2-1 — Create-new-project service (R13-04)
- **Files:** new helper in `spiderfeet_v2/workflow/` (info-only YAML builder), `spiderfeet_v2/api/routes/projects.py`, `crud.py`.
- **Do:** build info-only YAML (`apiVersion: spiderfeet.workflow/v1`, `kind: Workflow`, generated `workflow--<uuid>`, `info{name,description,author:"User",created:<now ISO8601>}`; no `inputs`/`target`/`steps`). Generate `project--<uuid>`. Persist: create the `project` **entity** (name/description/created) → create the `workflow` relation with `links (project: $p)` and `workflow_yaml` = info-only. Return `ProjectOut`.
- **Constraint (§0.1):** with the entity/relation shape, the workflow's link to the project is its one valid role player — **no placeholder target**. The workflow gains target/steps later via B2-2.
- **Verify:** `POST` then `GET /projects` shows the new row; `GET /projects/{id}/complete` returns the info-only YAML.

### B2-2 — PUT workflow re-parse (R13-05)
- **Files:** `spiderfeet_v2/api/routes/workflows.py`, `spiderfeet_v2/workflow/typedb_convert.py` (`persist_workflow_yaml` L346–375 exists; reuse with `replace=True`).
- **Do:** `PUT /workflows/{id}` body carries the new `workflow_yaml`; validate + convert; `persist_workflow_yaml` deletes the old bundle and writes target/steps/workflow. Reject invalid YAML (400) without mutating stored state. Return updated projection.
- **Verify:** unit test — start from info-only, PUT the full 12A YAML, assert steps/target/edges materialized and `workflow_yaml` updated; PUT invalid YAML → 400, stored bundle unchanged.

### B2-3 — Complete project endpoint (R13-06)
- **Files:** `spiderfeet_v2/api/routes/projects.py`, `spiderfeet_v2/db/projections.py` (`get_project` L122–150).
- **Do:** `GET /projects/{id}/complete` → `{project:{...}, workflows:[{...workflow attrs, workflow_yaml, steps:[summary], target}]}`.
- **Verify:** shape test against a seeded project; single call yields the YAML the Composer needs.

### B3-1 — Seed script (R13-07)
- **Files:** new `.seed/scripts/seed_projects.py` (pattern from `bootstrap.py` + `persist_workflow_yaml`).
- **Do:** for each of the 5 rows (§0.4): load template YAML, for clones rewrite `id`, `info.name/description`, and `inputs.targets.values=[https://<input>]`; `persist_workflow_yaml`; `create_project`. Idempotent (skip/replace if ids exist). Do **not** populate any `scan_step` result/UI fields.
- **Verify:** run against `spiderfeet-actual`; then B3-2.

### B3-2 — Seed verification (R13-08)
- **Do:** read-tx asserts 5 projects; project 1 → 1 step (netdiscover), no target-input; clones → subfinder/nmap/nerva/httpx/katana/nuclei steps + expected `needs` edges; no `scan_result_graph`/results. Record output in the issue.

### B3-3 — pytest (R13-09)
- **Do:** cover B1-2/B1-3/B2-1/B2-2/B2-3 + a seed smoke; `poetry run pytest`. Bind tests to R13 IDs in docstrings/markers.

## Governance
Branch from `develop`; PR into `develop`; close each issue with a completion note + evidence; merge before the next. Commit only when the operator has approved (per AGENTS.md commit policy) — confirm the repo's autonomous-merge posture with the operator before B-lane self-merge.
