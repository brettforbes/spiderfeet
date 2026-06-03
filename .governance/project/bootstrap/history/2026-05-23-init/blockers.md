# Bootstrap Blockers

**Run:** 2026-05-23-init

## B1 — GitHub Project API scope

| Field | Value |
|-------|--------|
| State | `blocked-with-tracked-issue` |
| Impact | Cannot list/adopt/normalize canonical VibeGov board |
| Evidence | `gh project list` → missing `read:project` scope |
| Remediation | `gh auth refresh -s project` then bootstrap **update** |

## B2 — GitHub Issues disabled

| Field | Value |
|-------|--------|
| State | `blocked-with-tracked-issue` |
| Impact | Cannot import/link issues to project board |
| Evidence | `gh issue list` → repository has disabled issues |
| Remediation | Enable Issues in repo Settings **or** document file-only backlog as canonical (operator decision) |

## B3 — Branch protection not verified

| Field | Value |
|-------|--------|
| State | degraded verification |
| Impact | Protection rules unknown |
| Remediation | Push `develop`, then verify per `.github/branch-protection-checklist.md` |

## Non-blockers (explicit)

- Dirty working tree — recorded, not resolved (commit policy forbidden)
- Product implementation — intentionally stopped per bootstrap gate
