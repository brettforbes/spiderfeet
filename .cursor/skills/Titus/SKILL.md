---
name: Titus
description: Use when requests mention Titus, secret scanner workflows, credential leak triage, or repository secret detection at scale. Runs scan-to-triage workflows and converts validated findings into nugget nodes/edges arrays.
---

# Titus — Secret Scanning to Nuggets

## Purpose

Use when you must **find and triage hardcoded secrets** in files, directories, Git history, Docker/OCI images, remote GitHub/GitLab URLs, or SaaS surfaces with [Titus](https://github.com/praetorian-inc/titus) (Go port of Nosey Parker) — capture **`--format json`** from `scan` / `report`, redact values, and map rule + provenance metadata into SpiderFeet nuggets.

Typical pipeline: `scan` → datastore (`titus.ds`) → `report --format json` → redact → graph. Prefer Titus for greenfield secret scanning; keep [Nosey Parker](../nosey_parker/SKILL.md) for legacy datastore replay.

**Binary (this host):**

| Platform | Path |
|----------|------|
| Windows | `C:\projects\spiderfeet\.tools\Titus\titus-windows-amd64.exe` |
| Linux | `C:\projects\spiderfeet\.tools\Titus\titus-linux-amd64` |

**Version:** **v1.2.7** (`titus version` — “Go port of NoseyParker”). Help capture: **2026-08-10** (`.tmp_titus_help/`).

## Step-by-Step Instructions

1. **Confirm authorization** — scanning paths, cloning repos, Docker images, or SaaS (`enum`) requires explicit permission; treat findings as sensitive.
2. **Verify binary** — `titus version` and `titus --help` (see Captured help in CLI Options doc).
3. **Choose datastore** — dedicated path per engagement (`--output ./engagement.ds` on scan; default `titus.ds`). Use `:memory:` for ephemeral runs or `:auto:` to derive from target name.
4. **Run scan** — select one input class (from live help):
   - Local file/directory: `titus scan ./repo-or-dir --format json --output ./engagement.ds`
   - Git history: `titus scan --git ./repo --format json --output ./engagement.ds`
   - Remote shorthand: `titus scan github.com/org/repo` or `gitlab.com/namespace/project`
   - Docker/OCI: `titus scan --docker alpine:latest` or `docker://ghcr.io/owner/image:tag`
   - Binary extract: add `--extract=all` (or `xlsx,docx,pdf,zip`) when secrets may live in Office/PDF/archives
5. **Optional live checks** — `--validate` (API validation) and/or `--score-scope` (HTTP dynamic scoring) when authorized and network calls are acceptable.
6. **Export structured findings** — SpiderFeet / automation only:
   ```bash
   titus report --datastore ./engagement.ds --format json
   ```
   Or emit JSON at scan time with `titus scan … --format json`.
7. **Triage** — use `titus explore ./engagement.ds` (TUI accept/reject); re-export with `--show-rejected` only when needed. Prefer `titus report summary --format json` for counts.
8. **Redact before sharing** — never paste raw secret values in chat, tickets, or logs.
9. **Map nuggets** — redacted rule + provenance → `nodes`/`edges` per `references/nugget-mapping.md`.
10. **Remediate and re-scan** — rotate/revoke; re-scan (optionally `--incremental`) into a fresh or same datastore.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `--format json` on `scan` and/or `report`; never parse human tables alone |
| Scope is a large monorepo | Phase high-risk paths; tune `--max-file-size`, `--ignore`, `--readers` / `--workers` |
| Need Git history secrets | `titus scan --git <repo>` (or `enum github … --git`) |
| Target is a container image | `--docker` or `docker://` prefix — no daemon required per upstream docs |
| Secrets may be in Office/PDF/zip | `--extract=all` (tune `--extract-max-*`, `--sqlite-row-limit`) |
| Results are noisy | Avoid `--include-noisy` unless intentional; use `--rules-include` / `--rules-exclude`; triage in `explore` |
| Need custom detectors | `--rules ./custom/` plus `--ruleset` (`default`, `np.assets`, `np.hashes`, `all`) |
| Org-wide GitHub/GitLab/SaaS | `titus enum <service> …` (default datastore `titus.db`) with `--format json` |
| Burp / live HTTP stream | `titus serve` (NDJSON stdin/stdout) — not a corpus harvest path |
| Confirm live credentials | `--validate` (and optionally `--score-scope`) on authorized targets only |
| Windows host | Use `.tools\Titus\titus-windows-amd64.exe` |

## Guardrails & Pitfalls

- **Authorized targets only** — includes cloning third-party GitHub/GitLab repos and SaaS enum.
- **Never publish raw secrets** — redact values; keep datastores access-controlled.
- **Pattern match ≠ confirmed compromise** — validate fixtures, examples, and revoked keys; use `--validate` when appropriate.
- **Separate datastores per engagement** — scan default `titus.ds`; enum default `titus.db`.
- **Do not invent flags** — only options from live `--help` / Captured help blocks (2026-08-10).
- **Do not use TextFSM on human report text** — parse `json` (or `sarif` for CI) from `scan`/`report`.
- **`--include-noisy` / serve default** — noisy rules are off for `scan` by default; `serve` defaults `--include-noisy` to true.
- **`--score-scope` / `--validate`** — make outbound API calls; may trigger alerts or rate limits.
- **TUI `explore`** — operator triage only; formal SpiderFeet examination still uses `--format json`.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Command tree, SpiderFeet defaults |
| `output-and-parsing.md` | JSON/SARIF, datastores, harvest bundles |
| `nugget-mapping.md` | JSON → SpiderFeet graph (redacted) |
| `tactics.md` | Sequencing, GitHub vs filesystem, triage |
| `sources.md` | Official URLs, blog, pkg.go.dev |

Operator guides: `.docs/docs-for-cli-tools/Titus-Zero-to-Hero.md`, `Titus-CLI-Options.md`.

## Comprehensive Examples

Prefer the Windows binary path or put it on `PATH` as `titus`.

### LOCAL PATH / GIT HISTORY

```bash
titus scan ./repo --format json --output ./engagement.ds
titus scan --git ./repo --format json --output ./engagement.ds
titus scan ./monorepo --ignore .titusignore --max-file-size 10485760 --format json
```

### REMOTE GITHUB / GITLAB (scan shorthand)

```bash
titus scan github.com/praetorian-inc/titus --format json --output ./engagement.ds
titus scan gitlab.com/gitlab-org/cli --format json --output ./engagement.ds
titus scan https://github.com/org/repo --format json
```

### DOCKER / OCI

```bash
titus scan --docker alpine:latest --format json --output ./img.ds
titus scan docker://ghcr.io/owner/repo:tag --format json
titus scan --docker ./my-app.tar --format json
```

### EXTRACT / VALIDATE / SCORE

```bash
titus scan ./files --extract=all --format json --output ./engagement.ds
titus scan ./code --validate --validate-workers 4 --format json
titus scan ./code --score-scope --accessibility auto --format json
```

### ENUM (GitHub / Slack examples)

```bash
titus enum github praetorian-inc/titus --format json --output ./gh.db
titus enum github --org myorg --token $env:GITHUB_TOKEN --format json --output ./org.db
titus enum slack --token $env:SLACK_TOKEN --format json --output ./slack.db
```

### REPORT / RULES / EXPLORE

```bash
titus report --datastore ./engagement.ds --format json
titus report summary --datastore ./engagement.ds --format json
titus report --datastore ./engagement.ds --format sarif
titus rules list --format json
titus explore ./engagement.ds
```

### SERVE (Burp NDJSON — not corpus primary)

```bash
titus serve
```

### Parse one JSON finding (Python)

```python
import json

# Shape varies by Titus version — inspect keys; never log secret values
raw = open("findings.json", encoding="utf-8").read()
data = json.loads(raw)
# Redact before printing — use rule names / paths / scores only
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Scan → structured report** — never stop at human tables for corpus work; prefer `--format json`.
2. **One datastore per engagement** — `titus.ds` (scan) vs `titus.db` (enum defaults).
3. **GitHub-aware** — public `scan github.com/org/repo` without token; org-wide via `enum github` + `GITHUB_TOKEN`.
4. **History vs working tree** — add `--git` when deleted secrets matter.
5. **Signal first** — skip `--include-noisy` unless hunting recall; triage in `explore`; validate high-severity first.
6. **Maximize on thin yield** — `--extract=all`, raise `--max-file-size`, `--ruleset all`, custom `--rules`.
7. **Retirement path** — Nosey Parker → Titus for new work; keep NP for comparative corpus replay.
