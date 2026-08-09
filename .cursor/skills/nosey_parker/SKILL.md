---
name: nosey_parker
description: Discover secrets in files, Git repos, and GitHub with Nosey Parker (scan→datastore→report). Trigger on noseyparker, secret scanning, leaked credentials, git history secret triage, or JSON/JSONL finding export for SpiderFeet graphs.
---

# Nosey Parker — Secret Discovery and Triage

## Purpose

Use when you must **find and triage hardcoded secrets** in files, directories, local Git history, remote Git URLs, or GitHub users/orgs with [Nosey Parker](https://github.com/praetorian-inc/noseyparker) — capture **`report -f json` / `jsonl`**, redact values, and map rule + provenance metadata into SpiderFeet nuggets.

Typical pipeline: `scan` → SQLite **datastore** → `summarize` → `report -f jsonl` → redact → graph. Upstream is **retired** in favour of [Titus](https://github.com/praetorian-inc/titus); keep Nosey Parker for SpiderFeet corpus examination and legacy datastores.

**Binary (this host):** `/home/brett/.local/spiderfeet-cli/bin/noseyparker` (WSL), **v0.24.0**. No native Windows build — use WSL or Docker (`ghcr.io/praetorian-inc/noseyparker`).

## Step-by-Step Instructions

1. **Confirm authorization** — scanning paths, cloning repos, or enumerating GitHub orgs requires explicit permission; treat findings as sensitive.
2. **Verify binary** — `noseyparker --version` and `noseyparker --help` (see Captured help in CLI Options doc).
3. **Choose datastore** — dedicated path per engagement (`-d ./engagement.np` or `NP_DATASTORE`); default is `datastore.np`.
4. **Run scan** — select one input class:
   - Local path / Git checkout: `noseyparker scan -d ./np-ds ./repo-or-dir`
   - Remote Git: `noseyparker scan -d ./np-ds --git-url https://github.com/org/repo`
   - GitHub user/org: `--github-user NAME` or `--github-organization NAME` (set `NP_GITHUB_TOKEN` for rate limits)
   - Enumerator JSONL (experimental): `--enumerator path.jsonl`
5. **Orient** — `noseyparker summarize -d ./np-ds` (also printed after scan).
6. **Export structured findings** — SpiderFeet / automation only:
   ```bash
   noseyparker report -d ./np-ds -f jsonl -o findings.jsonl
   ```
7. **Triage** — prioritize private keys, cloud keys, and tokens; use `--min-score`, `--finding-status`, and annotation export/import for noise.
8. **Redact before sharing** — never paste raw secret values in chat, tickets, or logs.
9. **Map nuggets** — redacted rule + provenance → `nodes`/`edges` per `references/nugget-mapping.md`.
10. **Remediate and re-scan** — rotate/revoke; re-scan the same or a fresh datastore.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `report -f json` or `jsonl`; never parse human `summarize`/`report` text alone |
| Scope is a large monorepo | Phase high-risk paths; tune `--max-file-size`, `-i` gitignore-style ignores |
| Git history is not needed | `--git-history=none` (do **not** combine with `--git-url` expecting useful results) |
| GitHub rate limits hit | Export `NP_GITHUB_TOKEN`; use `--github-api-url` for GitHub Enterprise |
| Results are noisy | Raise `--min-score` on `report`; filter `--finding-status`; inspect with `rules list` |
| Need custom detectors | `--rules-path ./custom/` plus `--ruleset CUSTOM_ID` (also `--ruleset default` to keep builtins) |
| Same secret in many files | Expect one **finding** per rule + capture group — review provenance lists |
| Enumerate repos without scanning | `github repos list` with `--user` / `--organization` and `-f jsonl` |
| Windows host | Run via WSL or Docker; no native `.exe` |
| Starting greenfield secret scanning today | Prefer **Titus**; keep Nosey Parker for corpus replay and legacy datastore analysis |

## Guardrails & Pitfalls

- **Authorized targets only** — includes cloning third-party GitHub repos.
- **Never publish raw secrets** — redact values; keep datastores access-controlled.
- **Pattern match ≠ confirmed compromise** — validate fixtures, examples, and revoked keys.
- **Separate datastores per engagement** — default `datastore.np`; use `datastore export` for archives.
- **Memory** — `--max-file-size` defaults to 100 MiB; entire file contents are read into memory.
- **Do not invent flags** — only options from live `--help` / Captured help blocks.
- **Do not use TextFSM on human report text** — parse `json`/`jsonl` from `report`.
- **`--git-url` constraints** — HTTPS only; no credentials, query parameters, or fragments.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Command tree, env, SpiderFeet defaults |
| `output-and-parsing.md` | `report` JSON/JSONL/SARIF, filtering, harvest bundles |
| `data-model.md` | Datastore, blob, provenance, match, finding |
| `nugget-mapping.md` | JSONL → SpiderFeet graph (redacted) |
| `tactics.md` | Sequencing, GitHub vs filesystem, triage |
| `sources.md` | Official URLs, retirement, integrations |

Operator guides: `.docs/docs-for-cli-tools/Nosey-Parker-Zero-to-Hero.md`, `Nosey-Parker-CLI-Options.md`.

## Comprehensive Examples

### LOCAL PATH / GIT HISTORY

```bash
noseyparker scan -d ./np-ds ./repo
noseyparker scan -d ./np-ds -j 8 ./monorepo
noseyparker scan -d ./np-ds --git-history=none ./checkout
noseyparker scan -d ./np-ds -i .npignore ./monorepo
```

### REMOTE GIT URL

```bash
noseyparker scan -d ./np-ds --git-url https://github.com/praetorian-inc/noseyparker
noseyparker scan -d ./np-ds --git-url https://github.com/org/a --git-url https://github.com/org/b
```

### GITHUB USER / ORG

```bash
export NP_GITHUB_TOKEN=ghp_...   # optional; higher limits / private access
noseyparker scan -d ./np-ds --github-user octocat
noseyparker scan -d ./np-ds --github-organization acme --github-repo-type source
noseyparker github repos list --organization acme -f jsonl
```

### ENUMERATOR (EXPERIMENTAL)

```bash
noseyparker scan -d ./np-ds --enumerator inputs.jsonl
# each line: {"content":"...","provenance":{...}} or content_base64
```

### SUMMARIZE / REPORT

```bash
noseyparker summarize -d ./np-ds
noseyparker summarize -d ./np-ds -f json -o summary.json
noseyparker report -d ./np-ds -f jsonl -o findings.jsonl
noseyparker report -d ./np-ds -f json -o findings.json
noseyparker report -d ./np-ds -f sarif -o report.sarif
```

### TRIAGE FILTERS

```bash
noseyparker report -d ./np-ds -f jsonl \
  --finding-status null \
  --min-score 0.2 \
  --max-matches 5 \
  --max-provenance 5 \
  -o high_signal.jsonl
```

### RULES

```bash
noseyparker rules list -f json
noseyparker scan -d ./np-custom --rules-path ./rules/ --ruleset default --ruleset internal ./target/
noseyparker rules check --rules-path ./rules/
```

### DATASTORE / DOCKER

```bash
noseyparker datastore init -d ./np-ds
noseyparker datastore export -d ./np-ds -o np-backup.tgz
docker run -v "$PWD":/scan -w /scan ghcr.io/praetorian-inc/noseyparker:v0.24.0 \
  scan -d /scan/datastore.np /scan/repo
```

### Parse one JSONL finding (Python)

```python
import json

line = '{"rule":{"name":"PEM-Encoded Private Key"},"num_matches":2}'
row = json.loads(line)
# Redact — never log capture groups or secret values
print(row["rule"]["name"], row.get("num_matches"))
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Scan → summarize → structured report** — never stop at human tables for corpus work.
2. **One datastore per engagement** — avoid mixing clients; `datastore export` for archives.
3. **GitHub-aware** — set `NP_GITHUB_TOKEN`; enumerate with `github repos list` before large org scans.
4. **History vs working tree** — default `full` history; use `--git-history=none` only for filesystem-only goals.
5. **Signal first** — raise `--min-score`, filter status, prioritize PEM/cloud/token rules over generic passwords.
6. **Maximize on thin yield** — drop ignores carefully, raise `--max-file-size` when secrets may live in large artifacts, add custom `--rules-path`.
7. **Retirement path** — new greenfield work → Titus; keep Nosey Parker for replay and comparative examination.
