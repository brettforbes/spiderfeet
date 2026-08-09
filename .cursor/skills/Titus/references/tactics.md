# Titus Strategies and Tactics

## Default sequence

1. **Authorize** — confirm path/repo/image/SaaS scope.
2. **Baseline scan** — local or single remote URL with `--format json` into a dedicated datastore.
3. **Orient** — `report summary --format json`; skim high severity / validated findings.
4. **Triage** — `explore` accept/reject; re-export JSON (omit rejected unless `--show-rejected`).
5. **Enrich** — optional `--validate` / `--score-scope` on a focused re-scan when live checks are in scope.
6. **Graph** — redacted nuggets only; remediate; re-scan (`--incremental` when appropriate).

## Input-class tactics

| Goal | Approach |
|------|----------|
| Working-tree secrets only | `titus scan ./checkout --format json` (no `--git`) |
| Deleted / historical secrets | `titus scan --git ./repo` or `enum github … --git` |
| Public GitHub one-shot | `titus scan github.com/org/repo --format json` |
| Org / user fan-out | `titus enum github --org NAME --token … --format json` |
| Container layers | `titus scan --docker image:tag --format json` |
| Office / PDF / zip | `--extract=all` with size/depth caps |
| Burp traffic | `titus serve` + extension (NDJSON) — separate from corpus harvest |

## Signal vs noise

- Leave `--include-noisy` **off** for first pass (scan default).
- Narrow with `--rules-include` / `--rules-exclude` or `--ruleset` (`default`, `np.assets`, `np.hashes`, `all`).
- Prefer severity/score from Titus scoring over raw match count.
- Mark fixtures/examples rejected in `explore` before graph promotion.

## Thin yield

When authorized target should have secrets but JSON is empty:

1. Confirm target path / URL / image pull auth (`~/.docker/config.json`).
2. Add `--git` for history; try `--extract=all`.
3. Raise `--max-file-size`; relax `--ignore` (or point at `/dev/null` / NUL to disable defaults — see help).
4. Try `--ruleset all` and carefully `--include-noisy` as a last recall pass.
5. For GitHub: set `GITHUB_TOKEN`; use `enum github` for org coverage.

## Performance

- Tune `--workers` / `--readers` on large trees.
- Use `--incremental` for repeat scans of the same datastore.
- Cap extract with `--extract-max-size` / `--extract-max-total` / `--extract-max-depth`.
- On large org enum: `--rate-limit` / `--jitter` (GitHub help) to avoid bans.

## Engagement hygiene

- One datastore directory/file per client.
- Never commit `*.ds` / `*.db` or blob stores with secrets.
- Redact before any chat, ticket, or PR paste.
- After remediation, re-scan and compare `report summary` JSON counts.
