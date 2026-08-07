# spiderfeet_v2.workflow (SPEC-010 AM1 / R10-20)

Workflow DSL parse/validate/schedule + GSE runtime, ported from
`.seed/scripts/cli_workflow/` (SPEC-007).

## Capabilities

| Concern | Entry point |
|---------|-------------|
| Load + schema validate | `load_workflow`, `validate_workflow_dict` |
| Schedule `needs` DAG | `schedule_waves` / `topological_waves` |
| Resolve `input.from` (+ normalize) | `resolve_step_inputs` |
| Build argv + auto files | `build_step_command` (argv arrays only) |
| Evaluate `output.vars` GSE | `evaluate_output_vars` / `eval_binding` |

Schemas: `schema/workflow_v1.schema.json`, `schema/gse_v1.schema.json`.
Canonical authoring shape: `.seed/12A_Workflow_YAML_Example.yaml`
(`inputs.*.values` or `default`).

## Verify

```bash
poetry run pytest spiderfeet_v2/workflow/tests/test_dsl.py -q
```
