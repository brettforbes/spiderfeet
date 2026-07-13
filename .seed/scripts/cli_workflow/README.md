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
  core/          # loader, GSE, context merge, normalize
  runtime/       # executor (Epic S)
  tools/         # CLI drivers (Epic T)
  cli.py         # validate / gse-eval
```

## Commands

From repo root (Poetry env):

```bash
# Ensure .seed/scripts is on PYTHONPATH
set PYTHONPATH=.seed/scripts   # Windows PowerShell: $env:PYTHONPATH=".seed/scripts"

poetry run python -m cli_workflow.cli validate .seed/12A_Workflow_YAML_Example.yaml
```

## Foundation already landed

- JSON Schemas for workflow + GSE
- GSE evaluator (`for_each` + product join, where/related, union)
- Workflow loader + DAG wave computation + adapter allow-list
- Context graph merge (unique nodes/edges)
- Hostname normalize helper

## Do not

- Redesign GSE without updating 12C + schemas + tests together
- Invent nugget ids not in ontology
- Parse CLI text to build output variables
- Implement Langium / Monaco / visual sync in this package yet
