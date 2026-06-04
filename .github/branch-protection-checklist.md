# Branch Protection Checklist

Use when configuring `brettforbes/spiderFeet` on GitHub.

## `master` (release / stable)

- [ ] Require pull request before merging
- [ ] Require approvals (≥1)
- [ ] Require status checks (CI: Tests workflow)
- [ ] Require branch up to date before merge
- [ ] Restrict force pushes
- [ ] Restrict deletions

## `develop` (integration)

- [ ] Require pull request before merging
- [ ] Require status checks (CI: Tests workflow)
- [ ] Allow fast-forward or merge commits per team preference
- [ ] Restrict force pushes

## Notes

- **Private repo limitation:** GitHub branch protection UI/API availability may differ on private repos or free plans. If verification fails, record as **degraded verification** in `INIT-TODO.md` with exact error evidence—do not treat as bootstrap failure.
- Local `develop` may exist before remote; push and protect separately.

## Verification commands (when permitted)

```bash
gh api repos/brettforbes/spiderfeet/branches/master/protection
gh api repos/brettforbes/spiderfeet/branches/develop/protection
```
