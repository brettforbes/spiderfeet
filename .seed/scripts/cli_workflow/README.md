# SpiderFeet CLI Workflow (SPEC-007)

Canonical design:

| Doc | Path |
|-----|------|
| Example workflow | `.seed/12A_Workflow_YAML_Example.yaml` |
| DSL logic | `.seed/12B_Workflow_DSL_Description.md` |
| Graph Select Language | `.seed/12C_Graph_Select_Language.md` |
| Spec | `.governance/specs/SPEC-007-cli-workflow-dsl.md` |
| Agent plan | `.governance/project/SPEC007_AGENT_PLAN.md` |

## Package layout

```text
cli_workflow/
  schema/workflow_v1.schema.json
  schema/gse_v1.schema.json
  core/          # loader, GSE, context merge, variables, models
  runtime/       # executor, tempfile manager
  tools/         # driver registry + FixtureDriver for dry-run
  fixtures/      # invalid workflows + dry-run graph map
  cli.py         # validate | gse-eval | dry-run
```

## Commands

From repo root:

```powershell
$env:PYTHONPATH = ".seed/scripts"

# Validate workflow YAML + GSE bindings
poetry run python -m cli_workflow.cli validate .seed/12A_Workflow_YAML_Example.yaml

# Dry-run 12A using corpus scan graphs (no live CLI)
poetry run python -m cli_workflow.cli dry-run `
  --workflow .seed/12A_Workflow_YAML_Example.yaml `
  --fixtures .seed/scripts/cli_workflow/fixtures/dry_run_12a_graphs.yaml `
  --repo-root .
```

## Tool drivers (T2 pattern)

- `tools/registry.py` maps `tool.<adapter_id>` → driver.
- `FixtureDriver` loads a prebuilt scan graph for CI/dry-run (no binary required).
- Live CLI drivers call SPEC-004 adapters after capture — implement per tool in Epic T.

## Adding a driver

1. Implement `ToolDriver` with `tool_id` and `run(argv, input_path=, output_path=)`.
2. `register(driver)` in module init or factory.
3. Workflow step `uses: tool.<id>` must match `ADAPTER_TOOLS` in `core/loader.py`.

## Tests

```bash
poetry run pytest .tests/test_cli_workflow_*.py -q
```

## Do not

- Redesign GSE without updating 12C + schemas + tests together
- Invent nugget ids not in ontology
- Parse CLI text to build output variables
- Implement Langium / Monaco / visual sync in this package yet
