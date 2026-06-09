# Governance Gap Audit — spiderFeet (Stage 0)

**Date:** 2026-06-03  
**Epic:** GitHub [#1](https://github.com/brettforbes/spiderfeet/issues/1)  
**Spec:** SPEC-002 R2-00-01

## Summary

Generic VibeGov rules (GOV-01–GOV-09) are installed and mirrored to `.cursor/rules/`. Project-specific rules for the SpiderFeet v2 reengineering program were **missing** until this epic. `develop` is not yet aligned with `master` (reengineering baseline lives on `master`).

## Matrix

| Area | Generic (`.governance/rules/`) | Project (`.governance/project/`) | Cursor mirror | Gap / action |
|------|----------------------------------|-----------------------------------|---------------|--------------|
| Workflow & git | GOV-02 ✅ | GIT_WORKFLOW.md ✅ | gov-02 ✅ | Align `develop` with `master` (operator) |
| Quality & testing | GOV-04, GOV-05 ✅ | — | mirrored ✅ | Add Python/FastAPI/TypeDB test norms → **proj rules** |
| Issues & tasks | GOV-06, GOV-07 ✅ | BACKLOG.md ⚠️ | mirrored ✅ | Extend backlog for stages 0–4 → **SF-00-05** |
| Exploratory review | GOV-08 ✅ | — | mirrored ✅ | Widget Maps/Tests scenarios referenced in SPEC-002 |
| Continuity | GOV-09 ✅ | continuity/ ✅ | mirrored ✅ | — |
| GOV-10–13 | Referenced in GOV-01 | Not present | Not mirrored | Optional future sync from VibeGov upstream |
| Project intent | — | PROJECT_INTENT.md ⚠️ provisional | — | Update for first-four program → **SF-00-04** |
| Active product spec | SPEC-001 bootstrap ✅ | — | — | SPEC-002 added for stages 0–4 |
| Python stack | — | **missing** | **missing** | Poetry, modules/, FastAPI, pytest → **proj-01** |
| TypeDB / map model | — | **missing** | **missing** | typedb + type-bridge skills, `spiderFeet-map` → **proj-01** |
| Multi-repo (widget) | — | **missing** | **missing** | Cross-root paths, API base URL → **proj-02** |
| Stage program | — | **missing** | **missing** | Stages 0–4 boundaries, no stage 5+ without spec → **proj-03** |
| GitHub Project board | — | BLOCKERS.md ⚠️ | — | Needs `gh auth refresh -s project,read:project` |

## Residual risks

1. **`develop` drift:** Feature branches should eventually target `develop`; until it matches `master`, branch from `master` or merge first.
2. **Dual rule sources:** Project rules live under `.governance/project/rules/` and must be mirrored to `.cursor/rules/` on change.
3. **Widget root:** EPIC-SFW-00 (widget repo) is a separate pass with JS-specific project rules.

## Verification

- [x] Audit documented (this file)
- [x] Project rules authored and mirrored (SF-00-02, SF-00-03)
- [x] PROJECT_INTENT and BACKLOG updated (SF-00-04, SF-00-05)
