# INIT-TODO

Durable bootstrap / adoption remediation tracker.

## Preflight

- [x] `git` available (`git version 2.40.1.windows.1`)
- [x] `gh` available (`gh version 2.89.0`)
- [x] GitHub auth — logged in as `brettforbes` (`repo`, `workflow`, `read:org`, `gist`)
- [x] Repo access — `brettforbes/spiderfeet`
- [ ] GitHub **project read** access
  - Blocker: token missing `read:project` scope
  - Next action: `gh auth refresh -s read:project`
- [ ] GitHub **project write** access
  - Blocker: not verified (depends on project scopes; likely needs `project` write)
  - Next action: `gh auth refresh -s project` then re-run bootstrap update for board normalization
- [ ] Branch protection verification
  - State: **degraded** — not verified this run
  - Next action: after `develop` is pushed, verify protection via repo Settings or `gh api repos/brettforbes/spiderfeet/branches/develop/protection`

## GitHub board / issues

- [ ] Canonical VibeGov project board
  - Blocker: project API access not available with current token scopes
  - Next action: refresh auth (above), then run bootstrap **update** mode to adopt/create/normalize board per [GitHub Project Bootstrap](https://vibegov.io/docs/github-project-bootstrap)
- [x] GitHub Issues enabled on `brettforbes/spiderfeet` and `brettforbes/spiderfeet-widget` (2026-06-03)
- [ ] First-four issues linked to GitHub Project
  - Blocker: `gh` token missing `project` / `read:project` scopes
  - Next action: `gh auth refresh -h github.com -s project,read:project` then `python .seed/planning/add_issues_to_github_project.py` (see `.seed/planning/PROJECT_SETUP.md`)

## Git workflow follow-up

- [ ] Push local `develop` branch to `origin`
  - Next action: `git push -u origin develop` (operator-initiated)
- [ ] Configure branch protection on `master` / `develop` per `.github/branch-protection-checklist.md`

## Bootstrap follow-up

- [ ] Re-run VibeGov bootstrap in **`update`** mode after GitHub project scope refresh
- [ ] Operator review of provisional `PROJECT_INTENT.md`
- [ ] Begin quarantined module verification (BL-009+) only after SPEC-002 or explicit operator direction
