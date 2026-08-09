# Nosey Parker Zero to Hero — Secret Scanning

Operator guide from install through `scan` → `summarize` → `report`, JSON/JSONL export, GitHub modes, triage, and SpiderFeet nugget notes.

> **Status:** Nosey Parker is [officially retired](https://www.praetorian.com/blog/titus-open-source-secret-scanner/) in favour of **[Titus](https://github.com/praetorian-inc/titus)**. This guide supports SpiderFeet CLI corpus examination, legacy datastore analysis, and WSL workflows on Windows hosts.

## 0. What Nosey Parker does

Nosey Parker finds **secrets and sensitive strings** in textual data using high-precision regex **rules**. It scans:

- Files and directories on disk
- **Full Git history** of local repositories (automatic when a directory is a Git repo)
- Remote Git repos (`--git-url`)
- GitHub users and organizations (`--github-user`, `--github-organization` / `--github-org`)
- Experimental enumerator JSONL streams (`--enumerator`)

Findings land in a SQLite-backed **datastore**, then export via `summarize` (overview) and `report` (detail). Matches that share the same rule + capture-group value merge into **findings** — the unit you triage.

**SpiderFeet uses Nosey Parker for:** secret-finding examination scenarios; structured capture via `report -f json` or `jsonl`; graph mapping of rule + provenance metadata (**never** raw secret values).

## 1. Install and path

### WSL / Linux (recommended on Windows)

This host’s binary:

| Field | Value |
|-------|-------|
| Path | `/home/brett/.local/spiderfeet-cli/bin/noseyparker` |
| Version | **0.24.0** |
| Capture date | **2026-08-10** |

Fresh install of the prebuilt **v0.24.0** x86_64 Linux GNU tarball:

```bash
CLI_ROOT="$HOME/.local/spiderfeet-cli"
mkdir -p "$CLI_ROOT/bin"
curl -fsSL \
  https://github.com/praetorian-inc/noseyparker/releases/download/v0.24.0/noseyparker-v0.24.0-x86_64-unknown-linux-gnu.tar.gz \
  -o /tmp/np.tar.gz
tar -xzf /tmp/np.tar.gz -C /tmp
cp /tmp/bin/noseyparker "$CLI_ROOT/bin/"
chmod +x "$CLI_ROOT/bin/noseyparker"
export PATH="$CLI_ROOT/bin:$PATH"
noseyparker --version
```

### Other install paths

| Method | Command |
|--------|---------|
| Homebrew (macOS/Linux) | `brew install noseyparker` |
| Docker | `docker pull ghcr.io/praetorian-inc/noseyparker:v0.24.0` |
| Arch AUR | `noseyparker` package |

**Windows native:** not supported. Use WSL or Docker.

### Verify

```bash
noseyparker --help
noseyparker rules list | head
```

Full live help: `.docs/docs-for-cli-tools/Nosey-Parker-CLI-Options.md` (section **Captured help**).

## 2. Core workflow: scan → summarize → report

Pick a **dedicated datastore** per engagement (`-d` or `NP_DATASTORE`; default `datastore.np`):

```bash
noseyparker scan -d ./np-demo.np ./path/to/repo-or-directory
```

Nosey Parker prints a **summarize** table when finished (rule, findings, matches, accept/reject/mixed/unlabeled counts). Re-run anytime:

```bash
noseyparker summarize -d ./np-demo.np
noseyparker summarize -d ./np-demo.np -f json -o summary.json
```

Human detail:

```bash
noseyparker report -d ./np-demo.np
```

**Structured export (SpiderFeet / automation — preferred):**

```bash
noseyparker report -d ./np-demo.np -f jsonl -o findings.jsonl
noseyparker report -d ./np-demo.np -f json -o findings.json
```

Do **not** treat human-only `summarize`/`report` text as the corpus structured artifact when JSON/JSONL is available.

## 3. JSON and JSONL

| Format (`-f`) | Commands | Use |
|---------------|----------|-----|
| `human` | summarize, report | Terminal review |
| `json` | summarize, report | Single pretty-printed document |
| `jsonl` | summarize, report | One object per line — pipelines / harvest |
| `sarif` | report only | Experimental CI / SARIF consumers |

Schema for `report` output ships with the release (`share/noseyparker/report-schema.json`) and can be regenerated with `noseyparker generate json-schema`.

Filter noise at export time:

```bash
noseyparker report -d ./np-demo.np -f jsonl \
  --min-score 0.15 \
  --finding-status null \
  --max-matches 5 \
  --max-provenance 5 \
  -o filtered.jsonl
```

## 4. GitHub modes

Set a token for higher rate limits and private access:

```bash
export NP_GITHUB_TOKEN=ghp_...
```

**Enumerate without scanning:**

```bash
noseyparker github repos list --user octocat -f jsonl
noseyparker github repos list --organization acme --repo-type source -f jsonl
```

**Scan a remote HTTPS repo:**

```bash
noseyparker scan -d ./np-remote.np \
  --git-url https://github.com/praetorian-inc/noseyparker
```

**Scan a GitHub user or org (authorized):**

```bash
noseyparker scan -d ./np-user.np --github-user octocat
noseyparker scan -d ./np-org.np --github-organization acme --github-repo-type source
```

GitHub Enterprise: set `--github-api-url` to the full base including `/api/v3` (for example `https://github.example.com/api/v3`). `--all-github-organizations` requires GHES + a non-default API URL.

**Docker:**

```bash
docker run -v "$PWD":/scan -w /scan ghcr.io/praetorian-inc/noseyparker:v0.24.0 \
  scan -d /scan/np.np /scan/repo
```

## 5. Triage

1. Read `summarize` — spot noisy rules (generic password / API key classes).
2. Export with `--min-score` and `--finding-status`.
3. Validate context — fixtures, examples, docs, and revoked keys are common false positives.
4. Optional: [Nosey Parker Explorer](https://github.com/praetorian-inc/noseyparkerexplorer) or experimental `annotations export` / `import` for accept/reject.
5. **Never** paste raw secret values in tickets, chat, or logs.
6. Remediate (rotate/revoke/remove) and re-scan to confirm closure.

## 6. Essential flags and environment

| Flag / env | Purpose |
|------------|---------|
| `-d`, `--datastore` / `NP_DATASTORE` | Findings database (default `datastore.np`) |
| `-j`, `--jobs` | Parallel scan threads (default `3`) |
| `--git-url` | Clone and scan HTTPS Git URL |
| `--github-user` / `--github-organization` | Enumerate and scan GitHub repos |
| `NP_GITHUB_TOKEN` | Higher GitHub rate limits; private repo access |
| `-f json` / `jsonl` on `report` | **Structured pipeline output** |
| `--min-score` | Filter low-confidence findings on report |
| `--max-file-size` | Skip huge files (default 100 MiB) |
| `-i`, `--ignore` | Gitignore-style path exclusions |
| `--git-history full\|none` | Full history (default) vs none |

Full reference (live Captured help + curated tables): `.docs/docs-for-cli-tools/Nosey-Parker-CLI-Options.md`

## 7. Parse JSONL in Python

```python
import json
from pathlib import Path

def iter_findings(path: Path):
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            yield json.loads(line)

for finding in iter_findings(Path("findings.jsonl")):
    rule = finding.get("rule", {}).get("name", "unknown")
    # Redact — do not log capture groups or secret values
    print(rule, finding.get("num_matches", 0))
```

Field names follow the release report schema — map via `report-schema.json`, not hard-coded stale keys.

## 8. SpiderFeet nugget notes

| Nosey Parker concept | SpiderFeet direction |
|----------------------|----------------------|
| Finding (redacted label / rule metadata) | `RAW_RIR_DATA` or promoted secret-finding type in `nuggets_extension.json` |
| Compromised password evidence (validated) | `PASSWORD_COMPROMISED` when appropriate |
| Leak site / public paste context | `LEAKSITE_URL` / `LEAKSITE_CONTENT` when provenance is a leak surface |
| Git host / repo hostname | `INTERNET_NAME` |
| Email / username in non-secret context | `EMAILADDR` / `USERNAME` only after validation |
| File path / commit provenance | Descriptor via `had` (`RAW_RIR_DATA`) |

**Rules:** never store raw secret bytes as `nugget_data`; reuse catalogue IDs before inventing types; one node per `(nugget_id, nugget_data)` via shared `graph_builder`.

Detail: `.cursor/skills/nosey_parker/references/nugget-mapping.md`

## 9. Examination scenario matrix (CLI profiling)

| Scenario | Command sketch |
|----------|----------------|
| Rich local Git repo | `scan -d DS ./vuln-lab-repo` → `report -f jsonl` |
| Filesystem only | `scan -d DS ./dir --git-history=none` |
| Clean miss | `scan -d DS ./empty-repo` → zero findings |
| GitHub (small, authorized) | `scan -d DS --github-user TARGET` + token |
| Invalid target | Missing path / bad URL → capture stderr + exit code |
| Filtered report | `report --min-score 0.2 -f jsonl` |

## 10. Troubleshooting

| Problem | Fix |
|---------|-----|
| `command not found` on Windows | Install in WSL; add `~/.local/spiderfeet-cli/bin` to PATH |
| GitHub rate limit | Set `NP_GITHUB_TOKEN` |
| Out of memory | Lower `--max-file-size`; add `-i` ignore files |
| Too many generic password hits | Raise `--min-score`; manual triage; custom `--ruleset` |
| Slow Git metadata | Try `--git-blob-provenance minimal` |
| Useless remote scan | Do not pair `--git-url` with `--git-history=none` |
| Need fresh tool for new work | Migrate to **Titus** |

## 11. Safety

Secret scanning is intrusive — filesystem and Git history reads, GitHub cloning. Authorized targets only. Store datastores with access controls; redact before any external share.

## 12. Skill and references

- `.cursor/skills/nosey_parker/SKILL.md`
- `.cursor/skills/nosey_parker/references/SKILLS.md`
- `.docs/docs-for-cli-tools/Nosey-Parker-CLI-Options.md`
