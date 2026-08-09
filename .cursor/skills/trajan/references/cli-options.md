# Trajan CLI Options (skill reference)

Authoritative live help is pasted in `.docs/docs-for-cli-tools/Trajan-CLI-Options.md` (**Captured help**, dated **2026-08-10**). Do not invent flags.

## Binary / version

| Field | Value |
|-------|-------|
| Windows | `C:\projects\spiderfeet\.tools\trajan\trajan.exe` |
| Version | **1.0.2** |
| Git commit | `c9a58278f157401b363150d923795a0d172fd221` |
| Build date | `2026-06-21T21:00:13Z` |
| Help capture | `.tmp_trajan_help/` |

## Command tree (from root help)

| Command | Role |
|---------|------|
| `github` | GitHub Actions: enumerate, scan, attack, retrieve, search |
| `gitlab` | GitLab CI: enumerate, scan, attack |
| `ado` | Azure DevOps: enumerate, scan, attack, retrieve |
| `bitbucket` | Bitbucket: enumerate only (1.0.2) |
| `jenkins` | Jenkins: enumerate, scan, attack |
| `jfrog` | JFrog Artifactory: scan (secrets / token-info) |
| `version` | Print version information |
| `completion` | Shell completions (bash, zsh, fish, powershell) |
| `help` | Help about any command |

Global flags: `-h/--help`, `-o/--output` (`console`, `json`, `sarif`, `html`; default `console`), `--proxy`, `--socks-proxy`, `--token`, `-v/--verbose`.

## SpiderFeet preferred commands

```bash
# Primary structured capture
trajan github scan --repo owner/repo -o json
trajan gitlab scan --project group/project -o json
trajan ado scan --org myorg --repo project/repo -o json

# Offline workflows / pipelines
trajan github scan --path ./.github/workflows -o json

# Inventory before scan
trajan github enumerate token -o json
```

| Prefer | Avoid for corpus |
|--------|------------------|
| `-o json` / `--output json` | Console tables as structured source |
| `scan` / `enumerate` under ROE | Defaulting to `attack` / `retrieve` |
| `--dry-run` before any live attack | `--confirm` / `--all` / chains without ROE |
| Dedicated engagement output files | Mixing clients in one unlabelled dump |

## Flag classes (names only — see Captured help)

- **Scope (scan):** `--repo`, `--org`, `--user`, `--project`, `--group`, `--path`, `--url` (platform-specific)
- **Scan tuning:** `--concurrency`, `--severity`, `--capabilities`, `--detailed`, `--list`, `--timeout` (offline)
- **Output:** `-o` / `--output` → `console` \| `json` \| `sarif` \| `html`
- **Auth:** `--token`, platform flags (`--url`, `--azure-bearer-token`, `--email`, `--workspace`, `--username`, `--password`, JFrog `-u`/`-p`)
- **Proxies:** `--proxy`, `--socks-proxy`
- **Attack (offensive):** `--plugin`, `--dry-run`, `--confirm`, `--force`, `--chain*`, `--session`, cleanup subcommand — see Captured help
- **Retrieve (offensive):** `--run-id`, `--repo`, `--wait` (GitHub); ADO retrieve exists per parent help

## Examples

```bash
trajan version
trajan github scan --repo owner/repo -o json
trajan github scan --org myorg --severity critical,high -o json
trajan github scan --path ./.github/workflows -o json
trajan github scan --list
trajan gitlab scan --group mygroup -o json
trajan ado enumerate token --org myorg -o json
trajan jenkins scan --url https://jenkins.example.com -o json
trajan jfrog scan --url https://acme.jfrog.io --secrets -o json
trajan github attack --repo owner/repo --plugin secrets-dump --dry-run -o json
```
