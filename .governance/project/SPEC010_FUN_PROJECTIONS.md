# SPEC-010 — TypeQL `fun` JSON projection contracts (R10-08 / AI2)

**Issue:** [#1073](https://github.com/brettforbes/spiderfeet/issues/1073)  
**Schema:** `.seed/spiderfeet_v2_semantic.tql` (functions section)  
**Edge names:** `.governance/project/SPEC010_EDGE_NAMING.md`  
**Consumer:** AL3 Python wrappers — `spiderfeet_v2/db/projections.py` (`ProjectionStore`, `project_json` / `workflow_json` / `scan_step_json` / `meta_subgraph_json`); tests `spiderfeet_v2/db/tests/test_projections.py`

TypeDB `fun` returns concept/value streams. JSON objects are assembled in the driver layer by collecting these streams into the field maps below.

---

## 1. Meta-concept subgraph

| Fun | Args | Returns | JSON use |
|-----|------|---------|----------|
| `contains_recursive` | `$container_A: nugget` | `{ nugget }` | nested contains targets |
| `meta_member` | `$root: nugget` | `{ nugget }` | root ∪ contains closure |
| `meta_related` | `$root: nugget` | `{ nugget }` | members + `had`/`listens-to` targets |
| `meta_contains_edge_ends` | `$root: nugget` | `{ nugget_instance_id, nugget_instance_id }` | `contains` edges |
| `meta_had_edge_ends` | `$root: nugget` | `{ nugget_instance_id, nugget_instance_id }` | `had` edges |
| `meta_listens_edge_ends` | `$root: nugget` | `{ nugget_instance_id, nugget_instance_id }` | `listens-to` edges |

Example assembly: call the three edge-end funs and tag each pair with the graph-JSON `type` from SPEC010_EDGE_NAMING.

---

## 2. Project

| Fun | Args | Returns | JSON field |
|-----|------|---------|------------|
| `project_ids` | — | `{ string }` | catalogue of `project_id` |
| `project_workflow_ids` | `$pid` | `{ string }` | `workflows[]` ids |
| `project_target_ids` | `$pid` | `{ string }` | `targets[]` via workflows |
| `project_context_ids` | `$pid` | `{ string }` | `project_context` ids |
| `project_temporary_subgraph_ids` | `$pid` | `{ string }` | `temporary_subgraph` ids |

```json
{
  "project_id": "project--…",
  "workflows": ["workflow--…"],
  "targets": ["target--…"],
  "project_context": ["project-context--…"],
  "temporary_subgraph": ["temporary-subgraph--…"]
}
```

---

## 3. Workflow

| Fun | Args | Returns | JSON field |
|-----|------|---------|------------|
| `workflow_target_ids` | `$wid` | `{ string }` | `target` |
| `workflow_first_step_ids` | `$wid` | `{ string }` | `first_step` |
| `workflow_prior_step_ids` | `$wid` | `{ string }` | `prior_step` |
| `workflow_next_step_ids` | `$wid` | `{ string }` | `next_step` |
| `workflow_yaml_string` | `$wid` | `{ string }` | `workflow_yaml` |

---

## 4. Scan step

| Fun | Args | Returns | JSON field |
|-----|------|---------|------------|
| `scan_step_cli_command` | `$sid` | `{ string }` | `cli_command` |
| `scan_step_text_form` | `$sid` | `{ string }` | `text_form` |
| `scan_step_structured_form` | `$sid` | `{ string }` | `structured_form` |
| `scan_step_graph_form` | `$sid` | `{ string }` | `graph_form` |
| `scan_step_markdown_narrative_form` | `$sid` | `{ string }` | `markdown_narrative_form` |
| `scan_step_consumed_ids` | `$sid` | `{ string }` | `consumed[]` nugget_instance_id |
| `scan_step_produced_ids` | `$sid` | `{ string }` | `produced[]` nugget_instance_id |
| `scan_step_result_graph_ids` | `$sid` | `{ string }` | `scan_result_graph` ids |

---

## 5. Verification

Seeded scratch DB smoke: `.tests/test_fun_projections.py`  
(`spiderfeet-ai2-smoke` — create, load schema, insert fixture, call each fun, delete).
