# Titus CLI Options (skill reference)

Authoritative live help is pasted in `.docs/docs-for-cli-tools/Titus-CLI-Options.md` (**Captured help**, dated **2026-08-10**). Do not invent flags.

## Binary / version

| Field | Value |
|-------|-------|
| Windows | `C:\projects\spiderfeet\.tools\Titus\titus-windows-amd64.exe` |
| Linux | `C:\projects\spiderfeet\.tools\Titus\titus-linux-amd64` |
| Version | **v1.2.7** (Go port of NoseyParker) |
| Help capture | `.tmp_titus_help/` |

## Command tree (from root help)

| Command | Role |
|---------|------|
| `scan` | Scan file, directory, git repo, Docker image, or remote GitHub/GitLab URL |
| `report` | Report from datastore (`human`, `json`, `sarif`); subcommand `summary` |
| `explore` | Interactive TUI triage on a datastore |
| `enum` | Enumerate remote services (github, gitlab, slack, notion, linear, confluence, jira, microsoft) |
| `rules` | Manage rules (`list`) |
| `serve` | Streaming NDJSON server for Burp extension |
| `version` | Show version |
| `completion` | Shell completions |

Global: `-h/--help`, `-q/--quiet`, `-v/--verbose`.

## SpiderFeet preferred commands

```bash
# Scan with JSON + engagement datastore
titus scan <target> --format json --output ./engagement.ds

# Re-export structured findings for graphs / harvest
titus report --datastore ./engagement.ds --format json

# Counts by rule
titus report summary --datastore ./engagement.ds --format json
```

| Prefer | Avoid for corpus |
|--------|------------------|
| `--format json` on `scan` and/or `report` | Human-only console tables as structured source |
| Dedicated `--output` / `--datastore` per engagement | Mixing clients in default `titus.ds` |
| `rules list --format json` when cataloguing detectors | Parsing TUI `explore` as examination text |

## `scan` flag classes (names only — see Captured help)

- **Target modes:** `--git`, `--docker`, remote `github.com/…` / `gitlab.com/…`
- **Output:** `--format` (`json`, `sarif`, `human`), `--output` (default `titus.ds`; `:memory:`, `:auto:`)
- **Rules:** `--rules`, `--ruleset`, `--rules-include`, `--rules-exclude`, `--include-noisy`
- **Extract:** `--extract`, `--extract-max-depth`, `--extract-max-size`, `--extract-max-total`, `--sqlite-row-limit`
- **Perf:** `--workers`, `--readers`, `--max-file-size`, `--incremental`, `--ignore`
- **Scoring / validation:** `--validate`, `--validate-workers`, `--score-scope`, `--score-timeout`, `--score-budget`, `--accessibility`, `--context-lines`
- **Blobs:** `--store-blobs`
- **SaaS attachments (Asana/GDrive helpers on scan):** `--asana-*`, `--gdrive-*` (see Captured help)

## `report` / `explore` / `enum` / `serve`

- **report:** `--datastore` (default `titus.ds`), `--format` (`human`, `json`, `sarif`), `--color`, `--show-rejected`; subcommand `summary` (Captured help included)
- **explore:** positional datastore or `--datastore`
- **enum:** providers fully captured in CLI Options — `github`, `gitlab`, `slack`, `notion`, `linear`, `confluence`, `jira`, `microsoft` (parent `--format` `json`/`human`, `--output` default `titus.db`, rule filters)
- **serve:** `--ruleset` default `all`, `--include-noisy` default true; NDJSON over stdin/stdout

## Examples

```bash
titus scan ./repo --format json --output ./engagement.ds
titus scan --git ./repo --validate --format json
titus scan --docker alpine:latest --format json
titus scan github.com/org/repo --format json
titus report --datastore ./engagement.ds --format json
titus rules list --format json
titus enum github owner/repo --format json --output ./gh.db
```
