# Project Intent

**Status:** Active — first-four-stages program (2026-06-03)  
**Spec:** SPEC-002  
**Plan:** `.seed/02_stage_by_stage_reengineer.md`

## Summary

**Spiderfeet** is a governed reengineering of SpiderFoot into a two-repo platform:

- **`spiderfeet`** — Python backend (modules, FastAPI, TypeDB map model)
- **`spiderfeet-widget`** — iFrame UI (Bootstrap 5, D3 force graphs)

Near-term delivery covers **stages 0–4**: governance, rebrand, API layer, TypeDB OSINT map with visualisation, and systematic module/route testing (177 OSINT modules).

## Goals

1. **Governed delivery** — VibeGov rules + project-specific rules; GitHub issues per epic/story
2. **Rebrand** — SpiderFoot → Spiderfeet, Apache 2.0, operator-selected logo (stage 1)
3. **API-first** — FastAPI over CLI for widget integration (stage 2)
4. **Map model** — TypeDB `spiderfeet-map` from analysis artefacts + force graph UI (stage 3)
5. **Module verification** — one issue per OSINT module; all routes tested and recorded (stage 4)
6. **Maintain analysis artefacts** — `osint_services.json`, nuggets, grouping docs

## Non-goals (stages 0–4)

- Quarantine module promotion (stage 5)
- Favourites, sequences, Maltego-style investigation UI (stages 6–8)
- TypeDB replacement for scan storage (`spiderfeet-actual`, stage 7)

## Stakeholders

- **Operator:** Brett Forbes (`brettforbes`)
- **Agents:** Cursor / VibeGov-governed automation

## Success signals

- SPEC-002 requirements met with verification evidence per stage
- 177 module-test issues closed or documented exception (paid/untested)
- Widget Maps and Tests tabs pass exploratory review (GOV-08)
- `develop` aligned with integration workflow after reengineering baseline merge

## References

| Resource | Path |
|----------|------|
| Bootstrap spec | `.governance/specs/SPEC-001-governance-bootstrap.md` |
| Product spec (stages 0–4) | `.governance/specs/SPEC-002-first-four-stages.md` |
| GitHub epics | `.seed/planning/github_issues_manifest.json` |
