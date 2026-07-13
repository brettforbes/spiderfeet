# Agent Entrypoint — spiderFeet

Governed SpiderFeet fork. Read this before doing substantive work.

## Canonical sources

| What | Where |
|------|--------|
| Project intent | `.governance/project/PROJECT_INTENT.md` |
| Active spec (bootstrap) | `.governance/specs/SPEC-001-governance-bootstrap.md` |
| Active spec (product) | `.governance/specs/SPEC-002-first-four-stages.md` |
| Active spec (stage 5) | `.governance/specs/SPEC-003-stage5-quarantine.md` |
| Active spec (CLI graph rules) | `.governance/specs/SPEC-004-cli-graph-rules-engine.md` |
| Active spec (narrative v2 + IP classify) | `.governance/specs/SPEC-005-narrative-v2-ip-classify.md` |
| Active spec (Structure docs + ontology) | `.governance/specs/SPEC-006-tool-structure-docs-ontology.md` |
| Active spec (CLI workflow DSL) | `.governance/specs/SPEC-007-cli-workflow-dsl.md` |
| Project rules | `.cursor/rules/proj-*.mdc` (subset also under `.governance/project/rules/`) |
| Stage plan | `.seed/02_stage_by_stage_reengineer.md` |
| Backlog | `.governance/project/BACKLOG.md` |
| Governance rules | `.governance/rules/gov-*.mdc` (mirrored in `.cursor/rules/`) |
| Bootstrap status | `.governance/project/bootstrap/STATUS.md` |
| Setup blockers | `INIT-TODO.md` |
| Git workflow | `.governance/project/GIT_WORKFLOW.md` |
| Continuity | `.governance/project/continuity/README.md` |

## Module taxonomy docs

- OSINT services: `.docs/analysis/osint_services.json` (`service_state`, `fixture_category`)
- Quarantined modules: `.docs/quarantine_modules.md`
- Core non-OSINT: `.docs/non_osint_modules.md`
- **Nugget ontology (canonical):** `.seed/05_Onotology_for_Nuggets.md` · rule: `.cursor/rules/proj-05-spiderfeet-nugget-ontology.mdc`
- **CLI Profiling:** skill `.cursor/skills/cli_app_profiling/SKILL.md` · exercising rule `.cursor/rules/proj-06-spiderfeet-cli-app-exercising.mdc` · **new-tool onboarding** `.seed/scripts/cli_corpus/ONBOARDING.md` · Nmap pilot `.docs/docs-for-cli-tools/nmap_pilot_signoff.md`
- **SPEC-004 structured→graph→narrative (complete):** spec `.governance/specs/SPEC-004-cli-graph-rules-engine.md` · rule `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` · issue index `.governance/project/SPEC004_ISSUE_INDEX.md` · handoff `.governance/project/continuity/SPEC004_PROGRAM_COMPLETION.md` · four UI outputs (Text, Structured, Graph, Markdown Report)
- **SPEC-005 narrative v2 + IP classify (active refinement):** spec `.governance/specs/SPEC-005-narrative-v2-ip-classify.md` · agent plan `.governance/project/SPEC005_AGENT_PLAN.md` · issue index `.governance/project/SPEC005_ISSUE_INDEX.md` · system guide `.docs/docs-for-cli-tools/SPEC004_SYSTEM_GUIDE.md`
- **SPEC-006 tool Structure docs + unified ontology (active):** spec `.governance/specs/SPEC-006-tool-structure-docs-ontology.md` · agent plan `.governance/project/SPEC006_AGENT_PLAN.md` · quality bar `.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md` · issue index `.governance/project/SPEC006_ISSUE_INDEX.md` · gold example `nugget_structure/nmap_nugget_graph_structure.md` · compose target `_Current_Ontology.md`
- **SPEC-007 CLI workflow DSL + GSE (active foundation):** spec `.governance/specs/SPEC-007-cli-workflow-dsl.md` · agent plan `.governance/project/SPEC007_AGENT_PLAN.md` · issue index `.governance/project/SPEC007_ISSUE_INDEX.md` · seed `.seed/12A_Workflow_YAML_Example.yaml` · `.seed/12B_Workflow_DSL_Description.md` · `.seed/12C_Graph_Select_Language.md` · package `.seed/scripts/cli_workflow/`
- **Widget Data Viewer embed:** `@spiderfeet-widget/.docs/data-viewer-embed.md` (Structured tabs, postMessage contract)

## Stage 4 — Tests corpus (read before seed or Tests work)

| Topic | Where |
|-------|--------|
| **Agent guide** | `.docs/analysis/stage4_seed_corpus_and_tests.md` |
| **Smoke seeds** | `.docs/analysis/module_test_seeds.json` |
| **Project rule** | `.cursor/rules/proj-04-spiderfeet-stage4-corpus.mdc` |
| **Pass semantics** | Positive: produced output · Negative: `module_execution.verdict = clean_miss` |
| **Hidden modules** | 8 upstream-broken services: `service_state: error` (excluded from Tests/Subscriptions) |
| **Probe scripts** | `.seed/scripts/validate_test_seeds.py`, `research_pending_seeds*.py`, `sync_service_state.py` |

None-tier seed research is **closed** (79 smoke + 8 error). Upstream-blocked modules need **module fixes**, not more seed tuning.

## Operating rules

1. **Stage 0–4 work** must map to SPEC-002 requirement IDs (see `.governance/project/BACKLOG.md`).
2. **SPEC-004 CLI graph/rules work** must map to R4-01-* and follow proj-07; pickup from `SPEC004_ISSUE_INDEX.md` in order (do not invent Nexus; no `sfp_*` rewrite until Epic E).
3. Follow GOV-02 delivery loop: Observe → Plan → Implement → Verify → Document.
4. Issue-first / spec-first for implementation tasks (GOV-06).
5. Checkpoint continuity per GOV-09 when instructions change, blockers appear, or handoff risk is high.
6. **Commit policy:** only when the operator explicitly requests commits.

## Default work pickup

1. Check `INIT-TODO.md` and `.governance/project/bootstrap/BLOCKERS.md`.
2. Select backlog item from `.governance/project/BACKLOG.md` (or canonical GitHub board when available).
3. Confirm spec coverage; extend spec before coding.
4. Stop before product implementation if still in bootstrap phase.

## VibeGov bootstrap

- Contract: https://vibegov.io/docs/bootstrap
- This repo was bootstrapped in **`init`** mode on 2026-05-23.
