# Project Intent

**Status:** Provisional (bootstrap init — 2026-05-23)

## Summary

This repository is a **SpiderFoot fork** (`brettforbes/spiderfeet`) used to analyse, document, and eventually visualise SpiderFoot's module and data-model surface—not to ship a unrelated greenfield product.

SpiderFoot itself is an OSINT automation platform (233 modules, SQLite backend, web UI and CLI). This fork's near-term intent is **understanding and cataloguing** that surface before deeper product changes.

## Goals

1. **Classify modules** into OSINT services, quarantined specialised modules, and core non-OSINT infrastructure.
2. **Document data sources and event types** (nuggets, OSINT service metadata, force-graph colour scheme).
3. **Establish governed delivery** via VibeGov so future implementation work is spec-driven and traceable.
4. **Defer product implementation** until module behaviour is verified and intent is confirmed.

## Non-goals (for now)

- Rewriting SpiderFoot core scanning engine
- Adding new OSINT modules without spec and verification
- Treating every `dataSource`-less module as generic infrastructure

## Stakeholders

- **Operator:** Repository owner (`brettforbes`)
- **Agents:** Cursor / VibeGov-governed automation assisting analysis and documentation

## Success signals

- Canonical module taxonomy documented (OSINT / quarantine / non-OSINT)
- `osint_services.json` and related analysis artifacts maintained
- Quarantined modules verified or retired with evidence
- Governed backlog drives the next implementation tranche

## Open questions

- Final product direction beyond analysis (visualisation widget, API, export tooling) — **not yet decided**
- Which quarantined modules remain viable in this fork
- GitHub Issues vs alternative backlog tracking (Issues currently disabled on the repo)
