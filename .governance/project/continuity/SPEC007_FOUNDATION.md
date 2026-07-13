# SPEC-007 foundation handoff (2026-07-13)

**Spec:** `.governance/specs/SPEC-007-cli-workflow-dsl.md`  
**Plan:** `.governance/project/SPEC007_AGENT_PLAN.md`  
**Issues:** `.governance/project/SPEC007_ISSUE_INDEX.md`

## Program status

## Landing record

| Range | Method |
|-------|--------|
| #1015 P0, #1016 P1 | PRs #1034, #1035 |
| #1033 foundation | PR #1033 |
| #1017–#1032 (P2–U2) | Direct commits on `develop` (`f31a8ec3`…`e3880763`) — batch automation failed to create feature branches; evidence on each issue comment |

Prefer PR-per-issue for future SPEC-007 follow-ups (live CLI drivers, Langium, etc.).

| Layer | Status |
|-------|--------|
| P0 sketch gap notes | Complete #1015 |
| P1 workflow schema tests | Complete #1016 |
| P2 GSE schema tests | Complete #1017 |
| Q1–Q3 GSE engine + corpus fixtures | Complete #1018–#1020 |
| R1–R3 loader / DAG / variables | Complete #1021–#1023 |
| S1–S4 runtime + dry-run CLI | Complete #1024–#1027 |
| T1–T3 registry + dry E2E 12A | Complete #1028–#1030 |
| U1–U2 README + handoff | Complete #1031–#1032 |

## Verify bundle

```powershell
$env:PYTHONPATH = ".seed/scripts"
poetry run pytest .tests/test_cli_workflow_*.py .tests/test_spec007_sketch_gap_notes.py -q
poetry run python -m cli_workflow.cli validate .seed/12A_Workflow_YAML_Example.yaml
poetry run python -m cli_workflow.cli dry-run --workflow .seed/12A_Workflow_YAML_Example.yaml --fixtures .seed/scripts/cli_workflow/fixtures/dry_run_12a_graphs.yaml --repo-root .
```

## Deferred (not SPEC-007)

Langium grammar, Monaco editor, workflow visualisation, AST↔diagram sync, context force-graph UI, live CLI drivers for all tools, `sfp_*` EVENT rewrite.
