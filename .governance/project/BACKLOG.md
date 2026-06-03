# Backlog (mapped to SPEC-001)

| ID | Spec | Title | Status | Priority |
|----|------|-------|--------|----------|
| BL-001 | R1 | Install VibeGov rules GOV-01–GOV-09 and mirror to `.cursor/rules/` | Done | P0 |
| BL-002 | R2 | Extract OSINT services → `osint_services.json` | Done | P0 |
| BL-003 | R2 | Document quarantined modules (54) | Done | P0 |
| BL-004 | R2 | Document core non-OSINT modules (2 storage) | Done | P0 |
| BL-005 | R3 | Git workflow artifacts (AGENTS, INIT-TODO, PR template, branch checklist, `develop`) | Done | P0 |
| BL-006 | R4 | GitHub preflight + canonical project board | Blocked | P1 |
| BL-007 | R5 | Continuity scaffold and operating guidance | Done | P1 |
| BL-008 | R6 | Bootstrap reporting (current + history bundle) | Done | P0 |
| BL-009 | R2 | Verify quarantined DNS modules (`sfp_dnsbrute`, `sfp_dnsresolve`, …) | Backlog | P1 |
| BL-010 | R2 | Verify quarantined tool wrappers (`sfp_tool_*`) | Backlog | P2 |
| BL-011 | — | Define product SPEC-002 after intent confirmation | Backlog | P2 |

## Default pickup flow

1. Read `INIT-TODO.md` for blockers.
2. Pick highest-priority **Ready** item from this backlog (or GitHub board when configured).
3. Confirm work maps to an open spec section; create/adjust spec before implementation.
4. Branch from `develop` → PR to `develop` → promote to `master` per `GIT_WORKFLOW.md`.
