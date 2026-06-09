# Bootstrap Analysis

**Run:** 2026-05-23-init  
**Mode:** init

## Repository profile

- **Remote:** https://github.com/brettforbes/spiderFeet
- **Base:** SpiderFeet OSINT platform fork (233 modules)
- **Prior work:** Module analysis artifacts in `.docs/analysis/` (OSINT services, nuggets, quarantine docs) from pre-bootstrap sessions

## Classification

| Signal | Finding |
|--------|---------|
| Product brief | None validated — intent marked **provisional** |
| Governance | Absent → created `.governance/` scaffold |
| Provider rules | `.cursor/` present → mirrored `.governance/rules/*.mdc` → `.cursor/rules/` |
| Issues | Disabled on GitHub repo |
| GitHub Projects | Token lacks `read:project` — preflight blocked |

## Module taxonomy correction

Initial heuristic ("no `dataSource` = non-OSINT") was wrong. Corrected split:

- **177** OSINT service modules
- **54** quarantined specialised modules (pending verification)
- **2** true non-OSINT infrastructure modules (`sfp__stor_db`, `sfp__stor_stdout`)

## Risk notes

- Dirty working tree at bootstrap start — bootstrap continued in init mode without resolving pre-existing edits (commit policy forbidden)
- Upstream SpiderFeet codebase is large; quarantined module verification is non-trivial (BL-009+)
- GOV-01 from upstream VibeGov references GOV-10–13 in loading order; only GOV-01–09 installed per bootstrap.json `active_rules`

## Historical vs current

This file reflects analysis at run time. Final git state: bootstrap files added locally, no commits made.
