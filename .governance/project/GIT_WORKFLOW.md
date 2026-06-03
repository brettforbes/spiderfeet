# Git Workflow

## Branches

| Branch | Purpose |
|--------|---------|
| `master` | Stable / release-aligned with upstream SpiderFoot baseline |
| `develop` | Integration branch for governed changes |

## Flow

1. Pick work from `.governance/project/BACKLOG.md` (or GitHub board when configured).
2. Branch from `develop`: `feature/<backlog-id>-short-description`
3. Implement against spec section; run relevant tests.
4. Open PR → `develop` using `.github/pull_request_template.md`.
5. After validation, promote `develop` → `master` via PR.

## Issue pickup (default)

GitHub Issues are **currently disabled** on this repo. Until enabled:

1. Use backlog IDs (`BL-###`) in commits and PRs when commits are operator-requested.
2. Record blockers in `INIT-TODO.md`.
3. When Issues are enabled, mirror backlog items to GitHub Issues and link to spec sections.

## Commit message convention (when committing)

```
BL-### type(scope): short description

- Spec: SPEC-001 / section Rx
- Verification: ...
```

## Commit policy for agents

Agents must **not** commit unless the operator explicitly requests it.
