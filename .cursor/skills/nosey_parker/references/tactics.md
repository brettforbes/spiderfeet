# nosey_parker Strategies and Tactics

## Core workflow sequence

1. **Scope** — define paths, repos, or GitHub actors; separate datastore per engagement.
2. **Discover** — `scan` with appropriate input specifiers and `-j` parallelism.
3. **Orient** — `summarize` for rule-level signal (printed post-scan).
4. **Export** — `report -f jsonl` (or `json`) with score/status filters.
5. **Triage** — human review or Explorer / annotations (`accept`/`reject`).
6. **Respond** — rotate, revoke, remove; document without raw secrets.
7. **Verify** — re-scan; confirm finding closure.

## Input strategy

| Target class | Command pattern |
|--------------|-----------------|
| Single repo checkout | `scan -d DS ./repo` (Git history automatic) |
| Directory tree (no `.git`) | `scan -d DS ./path` |
| Remote public repo | `scan -d DS --git-url https://github.com/org/repo` |
| GitHub user | `scan -d DS --github-user USER` |
| GitHub org | `scan -d DS --github-organization ORG --github-repo-type source` |
| Pre-enumerate repos | `github repos list --organization ORG -f jsonl` |
| Streamed content | `scan -d DS --enumerator inputs.jsonl` |

Set `NP_GITHUB_TOKEN` before large GitHub sweeps.

## Performance tactics

- Increase `-j` on multicore hosts (default `3`).
- Use `-i` gitignore-style files to skip `node_modules/`, `vendor/`, build artifacts.
- Lower `--max-file-size` under memory pressure; raise only when secrets may live in large files.
- `--git-history=none` for fast filesystem-only passes (not for secret-in-history goals; conflicts with useful `--git-url` scans).
- `--git-blob-provenance minimal` on pathological repos if metadata collection stalls.

## Signal-to-noise tactics

- Start with default ruleset; add `--rules-path` only for engagement-specific patterns.
- Raise `--min-score` on report (e.g. `0.15`–`0.3`) before export.
- Filter `--finding-status null` to focus unlabeled findings on first pass.
- Prioritize rules: PEM private keys, cloud access keys, API tokens; treat generic password rules as noisy until validated.
- Use finding deduplication — one finding may list many provenance entries; read all paths before declaring blast radius.

## SpiderFeet examination tactics

| Scenario class | Approach |
|----------------|----------|
| Rich local Git repo | Scan permissive lab clone with history; export jsonl report |
| Clean miss | Scan empty/minimal repo; expect zero findings in summarize |
| Sparse / large repo | Tune `--max-file-size`, `-i` ignores; document proven limitation if timeout |
| GitHub (authorized) | Small org/user with token; defer if rate-limited |
| Invalid input | Bad `--git-url` or missing path; capture error stderr |
| Custom rules | `--rules-path` + `--ruleset`; verify with `rules check` |

## Retirement note

Praetorian retired Nosey Parker in favour of **Titus** ([announcement](https://www.praetorian.com/blog/titus-open-source-secret-scanner/)). Prefer Titus for new engagements; retain Nosey Parker for corpus replay, legacy datastore analysis, and comparative examination.

## Integrations (upstream)

- Homebrew, Arch AUR, Docker (`ghcr.io/praetorian-inc/noseyparker`)
- GitHub Action: `noseyparker-action`
- DefectDojo parser (JSON family)
- Nosey Parker Explorer for interactive triage
