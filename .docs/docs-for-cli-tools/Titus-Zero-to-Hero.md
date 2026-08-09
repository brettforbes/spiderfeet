# Titus Zero to Hero — Secret Scanning

Operator guide from install through `scan` → datastore → `report --format json`, triage, Docker/GitHub modes, and SpiderFeet nugget notes.

Titus is Praetorian’s high-performance secrets scanner (Go port of Nosey Parker) with Hyperscan/Vectorscan acceleration when available, live validation, risk scoring, Docker/OCI scanning, and SaaS `enum` modes.

## 0. What Titus does

Titus finds **credentials, API keys, and tokens** using regex detection rules (hundreds of rules drawn from Nosey Parker and Kingfisher). It can scan:

- Files and directories on disk
- **Git history** (`--git`)
- Remote **GitHub / GitLab** URLs (`github.com/org/repo`, `gitlab.com/namespace/project`)
- **Docker / OCI** images (`--docker` or `docker://`)
- Binary formats via `--extract` (Office, PDF, archives, SQLite, …)
- Remote SaaS via `titus enum` (GitHub, GitLab, Slack, Notion, Linear, Confluence, Jira, Microsoft 365)
- Live HTTP streams via `titus serve` (Burp NDJSON)

Findings land in a **datastore** (`titus.ds` by default for `scan`), then export via `report`. Interactive triage uses `explore`.

**SpiderFeet uses Titus for:** secret-finding examination scenarios; structured capture via `--format json`; graph mapping of rule + provenance metadata (**never** raw secret values).

## 1. Install and path

### This workspace

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\Titus\titus-windows-amd64.exe` |
| Linux binary | `C:\projects\spiderfeet\.tools\Titus\titus-linux-amd64` |
| Version | **v1.2.7** |
| Help capture | **2026-08-10** (`.tmp_titus_help/`) |

```powershell
& C:\projects\spiderfeet\.tools\Titus\titus-windows-amd64.exe version
& C:\projects\spiderfeet\.tools\Titus\titus-windows-amd64.exe --help
```

Optional: copy/rename to `titus` on `PATH`, or set an alias.

### Upstream install

Download prebuilt binaries from [Releases](https://github.com/praetorian-inc/titus/releases), or build from source (`make build` → `dist/titus`). See the [README](https://github.com/praetorian-inc/titus/blob/main/README.md).

### Verify

```bash
titus version
titus rules list --format json
```

Full live help: `.docs/docs-for-cli-tools/Titus-CLI-Options.md` (section **Captured help**).

## 2. Core workflow: scan → report (JSON)

Pick a **dedicated datastore** per engagement (`--output` on scan; default `titus.ds`):

```bash
titus scan ./path/to/repo-or-directory --format json --output ./engagement.ds
```

Re-read findings anytime:

```bash
titus report --datastore ./engagement.ds --format json
titus report summary --datastore ./engagement.ds --format json
```

Human detail (operator review only):

```bash
titus report --datastore ./engagement.ds
titus explore ./engagement.ds
```

**Structured export (SpiderFeet / automation — preferred):**

```bash
titus scan ./target --format json --output ./engagement.ds
titus report --datastore ./engagement.ds --format json
```

Do **not** treat human-only console tables as the corpus structured artifact when JSON is available.

## 3. Output formats

| `--format` | Commands | Use |
|------------|----------|-----|
| `json` | `scan`, `report`, `report summary`, `enum`, `rules list` | **SpiderFeet primary** |
| `sarif` | `scan`, `report` | CI / GitHub Advanced Security |
| `human` | default | Operator console / TUI companion |
| NDJSON stream | `serve` | Burp extension only |

## 4. Common scan modes

### Local + git history

```bash
titus scan ./repo --format json --output ./engagement.ds
titus scan --git ./repo --format json --output ./engagement.ds
```

### Remote GitHub / GitLab (no token for public)

```bash
titus scan github.com/praetorian-inc/titus --format json --output ./engagement.ds
titus scan gitlab.com/gitlab-org/cli --format json
```

### Docker / OCI

```bash
titus scan --docker alpine:latest --format json --output ./img.ds
titus scan docker://ghcr.io/owner/repo:tag --format json
```

### Extract binaries + validate

```bash
titus scan ./files --extract=all --format json --output ./engagement.ds
titus scan ./code --validate --format json --output ./engagement.ds
titus scan ./code --score-scope --format json
```

### Rules filtering

```bash
titus rules list --format json
titus scan ./code --rules-include "aws,gcp" --format json
titus scan ./code --rules-exclude "kingfisher.generic" --format json
titus scan ./code --rules ./custom-rules.yaml --format json
```

## 5. Enum (org / SaaS)

`enum` defaults to datastore **`titus.db`** (not `titus.ds`). Prefer `--format json`.

```bash
titus enum github praetorian-inc/titus --format json --output ./gh.db
titus enum github --org myorg --token "$GITHUB_TOKEN" --format json --output ./org.db
titus enum slack --token "$SLACK_TOKEN" --format json --output ./slack.db
```

Use `titus enum <service> --help` for service-specific flags (token, URL, rate-limit, etc.).

## 6. Triage and remediation

1. Open `titus explore ./engagement.ds` — accept/reject with comments.
2. Re-export JSON; rejected findings stay hidden unless `--show-rejected`.
3. Rotate/revoke confirmed secrets; never paste raw values into tickets.
4. Re-scan; compare `report summary --format json`.

## 7. SpiderFeet nugget notes

- Map **redacted** rule + provenance only — see `.cursor/skills/Titus/references/nugget-mapping.md`.
- Typical types: `RAW_RIR_DATA` (finding/rule/path), `INTERNET_NAME` (host), `PASSWORD_COMPROMISED` / leak types only when confirmed and redacted.
- Relations: `contains`, `had` via shared `graph_builder`.
- Formal examination: structured JSON → graph → narrative; no text-only harvest when `--format json` exists.

## 8. Strategies and tactics (summary)

1. **JSON first** — `--format json` on scan and/or report.
2. **One datastore per engagement** — `titus.ds` (scan) vs `titus.db` (enum).
3. **History when needed** — `--git` for deleted secrets.
4. **Signal first** — avoid `--include-noisy` until a recall pass; triage in `explore`.
5. **Thin yield** — extract, raise max file size, `--ruleset all`, token for private/org GitHub.
6. **Live checks carefully** — `--validate` / `--score-scope` make outbound API calls.

## 9. Related docs

| Doc | Role |
|-----|------|
| `Titus-CLI-Options.md` | Flags + Captured help (2026-08-10) |
| `.cursor/skills/Titus/SKILL.md` | Agent skill |
| `Nosey-Parker-Zero-to-Hero.md` | Legacy predecessor workflows |
