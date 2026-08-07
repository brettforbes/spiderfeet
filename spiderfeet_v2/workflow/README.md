# spiderfeet_v2.workflow (SPEC-010 AM1–AM3 / R10-20–R10-22)

Workflow DSL parse/validate/schedule + GSE runtime + YAML ↔ TypeDB conversion
+ temporary-context export/merge.
Ported from `.seed/scripts/cli_workflow/` (SPEC-007) and extended for v2.

## Capabilities

| Concern | Entry point |
|---------|-------------|
| Load + schema validate | `load_workflow`, `validate_workflow_dict` |
| Schedule `needs` DAG | `schedule_waves` / `topological_waves` |
| Resolve `input.from` (+ normalize) | `resolve_step_inputs` |
| Build argv + auto files | `build_step_command` (argv arrays only) |
| Evaluate `output.vars` GSE | `evaluate_output_vars` / `eval_binding` |
| YAML → TypeDB forms | `yaml_to_typedb_forms` / `persist_workflow_yaml` |
| TypeDB → YAML | `load_workflow_yaml` / `typedb_forms_to_yaml` |
| TypeDB → API JSON | `load_workflow_api_json` / `typedb_to_api_json` |
| Context export mark | `step_exports_scan_graph` / `mark_scan_result_for_export` |
| Append-unique merge | `merge_graph` / `merge_graphs` / `apply_context_export` |

Schemas: `schema/workflow_v1.schema.json`, `schema/gse_v1.schema.json`.
Canonical authoring shape: `.seed/12A_Workflow_YAML_Example.yaml`
(`inputs.*.values` or `default`).

### YAML ↔ TypeDB (AM2 / R10-21)

- Typed entities/relations: `workflow` / `scan_step` / `target` via AL1 `CrudStore`
- String shadows: `workflow_yaml`, `scan_yaml`, `target_yaml`
- DAG roles: `first_step` (roots), `prior_step` (depended-upon), `next_step` (leaves)
- API JSON shape matches AL3 / `SPEC010_FUN_PROJECTIONS` §3

### Context export + merge (AM3 / R10-22)

- `context.export: scan_graph` marks a step's scan_result_graph for temporary-context export
- `none` / omitted does not export (vars may still flow)
- Merge is append-unique: nodes by `id`/`nugget_instance_id`, edges by `(source,target,relation)`
- Orchestrator (AO) calls `apply_context_export` after each step; persistence of temporary/project subgraphs remains AL + AN

## Verify

```bash
poetry run pytest spiderfeet_v2/workflow/tests/test_dsl.py -q
poetry run pytest spiderfeet_v2/workflow/tests/test_typedb_convert.py -q
poetry run pytest spiderfeet_v2/workflow/tests/test_context_export.py -q
```
