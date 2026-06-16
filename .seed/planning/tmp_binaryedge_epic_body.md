## Problem statement

BinaryEdge shut down **31 Mar 2025** and was absorbed into **Coalition Control**. The legacy module `sfp_binaryedge` still calls `https://api.binaryedge.io/v2/query/...` with an `X-Key` API key — that upstream is dead.

**Interim (landed):** `sfp_binaryedge` added to `UPSTREAM_ERROR_MODULE_IDS` → `service_state: error` (hidden from Tests/Subscriptions; visible on Maps).

## Desired outcome

Fully re-engineer BinaryEdge integration as a **Coalition Control** OSINT service: module, catalogue/map metadata, Subscriptions auth model, and Stage 4 tests.

## Key references

- [BinaryEdge Transition FAQ](https://help.coalitioninc.com/hc/en-us/articles/34383910057371-BinaryEdge-Transition-FAQ)
- [Coalition Control API QuickStart](https://help.coalitioninc.com/hc/en-us/articles/43715669577627-Coalition-Control-API-Basics-and-QuickStart)
- API docs: https://api.control.coalitioninc.com/docs/api
- Free signup: https://www.coalitioninc.com/control
- In-repo analysis: `.docs/analysis/binaryedge_coalition_control_transition.md`

## Architectural note

Coalition Control ASM is **entity-scoped** (your registered organization), not a public arbitrary-target query API like legacy BinaryEdge. Migration must decide which legacy routes are dropped, quarantined, or reinterpreted (`SPEC_GAP` if needed).

## Child work (this epic)

- [ ] Spike: API + free-tier scope + legacy route mapping
- [ ] Module rewrite (`modules/sfp_binaryedge.py` or successor)
- [ ] Subscriptions: Bearer auth (login credentials / token refresh / `entity_id`)
- [ ] Map + catalogue: `osint_services.json`, signup links, branding
- [ ] Tests: seeds, routes, unblock #474

## Spec binding

- SPEC-002: R2-04-03 (module testing)
- Likely `SPEC_GAP` for auth model and org-scoped semantics vs legacy public lookup

## Supersedes / relates

- #474 — module test issue blocked until migration completes
