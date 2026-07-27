# Git Workflow

## Branches

| Branch | Purpose |
|--------|---------|
| `master` | Stable / release-aligned with upstream SpiderFeet baseline |
| `develop` | Integration branch for governed changes |

## Flow

1. Pick work from `.governance/project/BACKLOG.md` (or GitHub board when configured).
2. Branch from `develop`: `feature/<backlog-id>-short-description`
3. Implement against spec section; run relevant tests.
4. Open PR → `develop` using `.github/pull_request_template.md`.
5. After validation, promote `develop` → `master` via PR.

## Issue pickup (default)

GitHub Issues are **enabled and in active use** on this repo (this note previously said
otherwise and was stale — see e.g. the SPEC-004 through SPEC-008 issue indexes under
`.governance/project/`). Default pickup:

1. Pick the next unblocked issue from a SPEC issue index (e.g.
   `.governance/project/SPEC008_ISSUE_INDEX.md`) or from `.governance/project/BACKLOG.md`.
2. Branch from `develop`: `feature/<issue-number>-<slug>`.
3. Implement against the linked spec requirement IDs; run relevant tests/verification.
4. Open PR → `develop` linking the issue and citing verification evidence.
5. Record blockers in `INIT-TODO.md` or as an issue comment.

## Commit message convention (when committing)

```
#<issue> type(scope): short description

- Spec: SPEC-00N / requirement Rx
- Verification: ...
```

## Commit policy for agents

Default: agents must **not** commit unless the operator explicitly requests it.

**Standing exception:** for work executed under a SPEC that explicitly authorizes autonomous
execution in its own `SPEC*_AGENT_PLAN.md` ("Autonomous execution protocol" section — e.g.
SPEC-008), agents may commit, open PRs, and self-merge into `develop` without waiting for
per-task approval, because that authorization **is** the operator's explicit request, given once
for the whole SPEC rather than repeated per commit. This depends on `develop` having no
branch-protection review requirement (`gh api repos/<org>/<repo>/branches/develop/protection`);
if protection requiring review is ever added, autonomous self-merge stops working automatically
and PRs will wait for a human reviewer.
