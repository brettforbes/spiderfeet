# SPEC-007 foundation bootstrap (2026-07-13)

**Spec:** `.governance/specs/SPEC-007-cli-workflow-dsl.md`  
**Plan:** `.governance/project/SPEC007_AGENT_PLAN.md`  
**Issues:** `.governance/project/SPEC007_ISSUE_INDEX.md` (#1009–#1032)

## What landed in this bootstrap

| Artifact | Path |
|----------|------|
| Example workflow (v1) | `.seed/12A_Workflow_YAML_Example.yaml` |
| DSL logic master | `.seed/12B_Workflow_DSL_Description.md` |
| Graph Select Language | `.seed/12C_Graph_Select_Language.md` |
| Sketch gap notes | `.governance/project/SPEC007_SKETCH_GAP_NOTES.md` |
| Package | `.seed/scripts/cli_workflow/` |
| Schemas | `schema/workflow_v1.schema.json`, `schema/gse_v1.schema.json` |
| GSE + loader + context merge | `core/*` |
| Foundation tests | `.tests/test_cli_workflow_foundation.py` (**6 passed**) |

## Verify

```bash
$env:PYTHONPATH=".seed/scripts"   # PowerShell
poetry run pytest .tests/test_cli_workflow_foundation.py -q
poetry run python -m cli_workflow.cli validate .seed/12A_Workflow_YAML_Example.yaml
```

## Next agent pickup

Start at **P0 #1015** (or harden P1/P2/Q* against the already-landed stubs). Follow `SPEC007_AGENT_PLAN.md` order. Do **not** redesign GSE.

## Explicitly deferred

Langium, Monaco, visualisation, AST sync, context force-graph UI, `sfp_*` EVENT rewrite.
