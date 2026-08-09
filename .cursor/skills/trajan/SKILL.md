---
name: trajan
description: Scan CI/CD pipelines for supply-chain risks with Trajan. Trigger when tasks mention GitHub Actions, GitLab CI, Azure DevOps, Bitbucket, Jenkins, JFrog, workflow YAML analysis, pipeline misconfigurations, or CI token/secret abuse paths.
---

# Trajan — CI/CD Supply-Chain Scanning to Nuggets

## Purpose

Use when you must **assess CI/CD pipelines for supply-chain weaknesses** with [Praetorian Trajan](https://github.com/praetorian-inc/trajan) on **authorized** targets — GitHub Actions, GitLab CI, Azure DevOps, Bitbucket (enum), Jenkins, or JFrog Artifactory. Capture **`-o json`** (or `--output json`), map findings to SpiderFeet nuggets, and only escalate to `attack` / `retrieve` under explicit offensive scope with `--dry-run` first.

Trajan is **not** a general secret scanner (use [Titus](../Titus/SKILL.md) / [Nosey Parker](../nosey_parker/SKILL.md) for credential hunting in code). It analyzes **pipeline configs, permissions, runners, and CI attack paths**.

**Binary (this host):**

| Field | Value |
|-------|-------|
| Windows | `C:\projects\spiderfeet\.tools\trajan\trajan.exe` |
| Version | **1.0.2** (`trajan version` — commit `c9a58278…`, build `2026-06-21T21:00:13Z`) |
| Help capture | **2026-08-10** (`.tmp_trajan_help/`) |

## Step-by-Step Instructions

1. **Confirm authorization** — org/repo/project ownership or written ROE. `attack` / `retrieve` modify or exfiltrate; treat as offensive.
2. **Verify binary** — `trajan version` and `trajan --help` (see Captured help in CLI Options).
3. **Choose platform** — `github` | `gitlab` | `ado` | `bitbucket` | `jenkins` | `jfrog` (capabilities differ; Bitbucket is enumerate-only in 1.0.2).
4. **Set credentials** — prefer env vars over `--token` on the CLI:
   - GitHub: `GH_TOKEN` / `GITHUB_TOKEN` (+ `--url` for GHES)
   - GitLab: `GITLAB_TOKEN` / `GL_TOKEN` (+ `--url` for self-hosted)
   - Azure DevOps: `AZURE_DEVOPS_PAT` / `AZDO_PAT`; Entra bearer via `--azure-bearer-token` / `AZURE_BEARER_TOKEN` when required
   - Bitbucket: `--token` + `--email` (`BITBUCKET_EMAIL` / `BB_EMAIL`) + `--workspace`
   - Jenkins: `--username` / `--password` (`JENKINS_USERNAME` / `JENKINS_PASSWORD`) + instance `--url` on scan
   - JFrog: `JFROG_TOKEN` or `-u`/`-p` + `--url`
5. **Enumerate first (when available)** — validate token/scopes and inventory before scanning:
   - `trajan github enumerate token|repos|secrets -o json`
   - `trajan gitlab enumerate token|projects|groups|secrets|runners|branch-protections -o json`
   - `trajan ado enumerate … --org <org> -o json`
   - `trajan jenkins enumerate access|jobs|nodes|plugins -o json`
   - `trajan bitbucket enumerate token -o json`
6. **Scan with JSON** — SpiderFeet / automation only:
   ```bash
   trajan github scan --repo owner/repo -o json
   trajan gitlab scan --project group/project -o json
   trajan ado scan --org myorg --repo project/repo -o json
   trajan jenkins scan --url https://jenkins.example.com -o json
   trajan jfrog scan --url https://acme.jfrog.io --secrets --token-info -o json
   ```
   Offline YAML: `--path <file-or-dir>` on github/gitlab/ado/jenkins `scan` (skips platform API; Jenkins live checks skipped offline).
7. **List detectors before tuning** — `trajan github scan --list` (and peer `--list` on gitlab/ado scan) to see active capabilities.
8. **Parse JSON** — primary records are findings (severity, capability/detection, workflow/pipeline context, evidence). See `references/output-and-parsing.md`.
9. **Map nuggets** — redacted finding labels + repo/workflow provenance per `references/nugget-mapping.md`. Never store exfiltrated secret bytes as `nugget_data`.
10. **Offensive paths (explicit ROE only)** — `attack` requires `--dry-run` first, then `--confirm` for live runs. `retrieve` follows secrets-dump / ADO pipeline exfil. Prefer documenting findings from `scan` for corpus work; do not harvest live attack loot into examination bundles without operator approval.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-o json` (or `--output json`); never parse console tables alone |
| Platform unknown | Inspect `trajan --help` platforms; branch by adapter |
| Private GitHub / org scan | Require token with adequate scopes; start `--repo` before `--org` |
| API blocked / no token | `scan --path` offline on workflow/pipeline files; mark API-only detections skipped |
| Need detector catalogue | `trajan <platform> scan --list` where supported |
| High/critical only | `--severity critical,high` |
| Specific detectors | `--capabilities <comma-list>` (names from `--list` / help examples) |
| Self-hosted runner hunt (GitHub) | `trajan github search -p github` or `-p sourcegraph` (then scan hits) |
| Bitbucket in scope | Only `enumerate token` in 1.0.2 — no `scan`/`attack` |
| JFrog in scope | `jfrog scan --secrets` / `--token-info` — not pipeline YAML CVE scanning |
| Offensive verification | `attack --dry-run` → review → `attack --confirm` under ROE; never default to `--all` / chains |
| ADO persistence plugins | Need `--azure-bearer-token` (PAT alone cannot create PATs/SSH keys per help) |
| Post secrets-dump | `trajan github retrieve --run-id …` or ADO `retrieve` (offensive; redact) |
| Rate limits / large org | Lower `--concurrency`, split orgs/groups, raise patience |

## Guardrails & Pitfalls

- **Authorized targets only** — CI APIs expose secrets metadata, runners, and deploy paths.
- **`attack` / `retrieve` are offensive** — they modify resources or decrypt exfiltrated secrets. Always `--dry-run` first; require `--confirm` for live execution. Document carefully; do not run casually in corpus harvest.
- **Do not invent flags** — only options from live `--help` / Captured help (**2026-08-10**, binary **1.0.2**). Upstream README may describe newer CLI shapes (`run`/`report` phases); this skill targets the installed binary.
- **Prefer JSON** — `-o json` for SpiderFeet; `sarif`/`html` are secondary. Default `console` is operator triage only.
- **Never publish raw secrets** — redact retrieve/attack output; keep tokens out of logs and tickets.
- **Offline ≠ API coverage** — `--path` skips platform API; Jenkins anonymous/CSRF/script-console checks need a live instance.
- **Bitbucket / JFrog surface is smaller** — do not assume parity with GitHub `scan`/`attack`.
- **Global `--token` help text** mentions `GH_TOKEN`/`GITHUB_TOKEN`; platform help documents the correct env vars per adapter — follow platform help.
- **Related tools** — Titus for secret content in files/git; Trajan for pipeline abuse paths.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Command tree, SpiderFeet defaults |
| `platforms.md` | Per-platform commands and auth |
| `output-and-parsing.md` | JSON / SARIF / harvest notes |
| `nugget-mapping.md` | Findings → SpiderFeet graph (redacted) |
| `tactics.md` | Sequencing, thin yield, offensive gates |
| `sources.md` | Official URLs |

Operator guides: `.docs/docs-for-cli-tools/Trajan-Zero-to-Hero.md`, `Trajan-CLI-Options.md`.

## Comprehensive Examples

Prefer the workspace binary or put `trajan` on `PATH`.

### VERSION / HELP

```bash
trajan version
trajan --help
trajan github --help
```

### GITHUB — ENUMERATE / SCAN

```bash
trajan github enumerate token -o json
trajan github enumerate repos -o json
trajan github scan --repo owner/repo -o json
trajan github scan --org myorg --concurrency 10 -o json
trajan github scan --repo owner/repo --severity critical,high --detailed -o json
trajan github scan --list
trajan github scan --path ./.github/workflows -o json
```

### GITHUB — SEARCH / OFFENSIVE (ROE ONLY)

```bash
trajan github search -p sourcegraph -o json
trajan github search -p github --org myorg -o json
# Preview only
trajan github attack --repo owner/repo --plugin secrets-dump --dry-run -o json
# Live requires --confirm; cleanup when done
trajan github attack cleanup --help
trajan github retrieve --run-id 123456789 --repo owner/repo -o json
```

### GITLAB

```bash
trajan gitlab enumerate token -o json
trajan gitlab enumerate projects -o json
trajan gitlab scan --project group/project -o json
trajan gitlab scan --group mygroup -o json
trajan gitlab scan --path ./.gitlab-ci.yml -o json
trajan gitlab attack --project group/project --plugin secrets-dump --dry-run -o json
```

### AZURE DEVOPS

```bash
trajan ado enumerate token --org myorg -o json
trajan ado enumerate projects --org myorg -o json
trajan ado scan --org myorg --repo project/repo -o json
trajan ado scan --path ./azure-pipelines.yml -o json
trajan ado attack --org myorg --repo project/repo --plugin ado-secrets-dump --dry-run -o json
```

### BITBUCKET / JENKINS / JFROG

```bash
trajan bitbucket enumerate token --email you@example.com --workspace my-ws -o json
trajan jenkins enumerate access --username user --password "$JENKINS_PASSWORD" -o json
trajan jenkins scan --url https://jenkins.example.com -o json
trajan jenkins scan --path ./Jenkinsfile -o json
trajan jfrog scan --url https://acme.jfrog.io --secrets --token-info -o json
```

### OUTPUT FORMATS

```bash
trajan github scan --repo owner/repo -o json
trajan github scan --repo owner/repo -o sarif
trajan github scan --repo owner/repo -o html
trajan github scan --repo owner/repo -o console
```

### Parse findings (Python)

```python
import json

# Shape varies by platform/version — inspect keys; never log secret values
raw = open("trajan-results.json", encoding="utf-8").read()
data = json.loads(raw)
# Prefer severity / detection / workflow path fields for nuggets
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Enumerate → scan → (optional) attack** — never start with `attack`/`retrieve`.
2. **JSON always for SpiderFeet** — `-o json`; derive Text from structured later.
3. **Narrow then wide** — one `--repo`/`--project` → critical set → `--org`/`--group`.
4. **Offline when API-limited** — `--path` for YAML; document coverage gaps.
5. **Offensive is gated** — `--dry-run`, then `--confirm`; cleanup sessions; redact loot.
6. **Platform-aware** — Bitbucket enum-only; JFrog secrets/token-info; Jenkins needs instance URL for live checks.
7. **Chain to Titus** — Trajan finds pipeline abuse; Titus finds secrets in repo/history content.
