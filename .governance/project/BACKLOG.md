# Backlog

Primary tracker: [GitHub Issues](https://github.com/brettforbes/spiderfeet/issues) (+ [widget repo](https://github.com/brettforbes/spiderfeet-widget/issues)).  
Spec: **SPEC-002** (stages 0–4). Legacy bootstrap items: SPEC-001 below.

## Stage program (SPEC-002)

| Stage | Epic (spiderfeet) | Epic (widget) | Spec IDs | Status |
|-------|-------------------|---------------|----------|--------|
| 0 | [#1](https://github.com/brettforbes/spiderfeet/issues/1) Governance (Python) | [widget #1](https://github.com/brettforbes/spiderfeet-widget/issues/1) | R2-00-01, R2-00-02 | In progress |
| 0 cross | [#7](https://github.com/brettforbes/spiderfeet/issues/7) Program setup | — | R2-00-02 | Backlog |
| 1 | [#13](https://github.com/brettforbes/spiderfeet/issues/13) Rebrand backend | [widget #7](https://github.com/brettforbes/spiderfeet-widget/issues/7) | R2-01-01 | Backlog |
| 1 cross | [#21](https://github.com/brettforbes/spiderfeet/issues/21) Logo sign-off | — | R2-01-01 | Backlog |
| 2 | [#26](https://github.com/brettforbes/spiderfeet/issues/26) FastAPI over CLI | — | R2-02-01 | Backlog |
| 3a | [#40](https://github.com/brettforbes/spiderfeet/issues/40) TypeDB ORM | — | R2-03-01 | Backlog |
| 3b | [#48](https://github.com/brettforbes/spiderfeet/issues/48) Map FastAPI | — | R2-03-02 | Backlog |
| 3c | — | [widget #13](https://github.com/brettforbes/spiderfeet-widget/issues/13) Maps UI | R2-03-03 | Backlog |
| 4a–c | [#56](https://github.com/brettforbes/spiderfeet/issues/56)–[#66](https://github.com/brettforbes/spiderfeet/issues/66) | — | R2-04-01–03 | Backlog |
| 4 modules | [#74](https://github.com/brettforbes/spiderfeet/issues/74) + 177 `[Module test]` issues | [widget #32](https://github.com/brettforbes/spiderfeet-widget/issues/32) Tests tab | R2-04-03, R2-04-04 | Backlog |
| 4 sign-off | [#75](https://github.com/brettforbes/spiderfeet/issues/75) | — | R2-04-03 | Backlog |

## Bootstrap backlog (SPEC-001) — completed / carry-over

| ID | Spec | Title | Status | Priority |
|----|------|-------|--------|----------|
| BL-001 | R1 | VibeGov GOV-01–09 + mirror | Done | P0 |
| BL-002 | R2 | OSINT services → `osint_services.json` | Done | P0 |
| BL-003 | R2 | Quarantined modules documented | Done | P0 |
| BL-004 | R2 | Core non-OSINT modules documented | Done | P0 |
| BL-005 | R3 | Git workflow artifacts | Done | P0 |
| BL-006 | R4 | GitHub project board | Blocked | P1 |
| BL-007 | R5 | Continuity scaffold | Done | P1 |
| BL-008 | R6 | Bootstrap reporting | Done | P0 |
| BL-009 | R2 | Verify quarantined DNS modules | Deferred → stage 5 | P1 |
| BL-010 | R2 | Verify quarantined tool wrappers | Deferred → stage 5 | P2 |
| BL-011 | — | SPEC-002 first-four-stages | Done | P0 |

## Pickup flow

1. Read `INIT-TODO.md` for blockers.
2. Pick highest-priority **Ready** GitHub issue for the active stage epic.
3. Confirm SPEC-002 requirement binding; branch `feature/<issue>-<slug>`.
4. PR to `develop` (after `develop` is aligned with `master` baseline).
