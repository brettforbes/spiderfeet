# Trajan Zero to Hero — CI/CD Supply-Chain Scanning

Operator guide from install through `enumerate` → `scan -o json`, nugget notes, and carefully gated `attack` / `retrieve` usage.

Trajan ([praetorian-inc/trajan](https://github.com/praetorian-inc/trajan)) finds **CI/CD pipeline weaknesses** attackers use against software supply chains: pwn requests, artifact/cache poisoning, secrets exposure paths, self-hosted runners, and related abuse patterns across GitHub Actions, GitLab CI, Azure DevOps, Jenkins, and JFrog (plus Bitbucket token enum in 1.0.2).

## 0. What Trajan does

Trajan:

- **Enumerates** token scopes and accessible CI resources
- **Scans** workflow/pipeline configs (API or offline `--path`)
- Optionally **attacks** / **retrieves** to verify exploitability (**offensive** — authorized ROE only)

Trajan does **not**:

- Replace general secret scanning of source/history (use **Titus** / Nosey Parker)
- Port-scan hosts or crawl web apps (use **naabu** / **httpx** / **nuclei**)

**SpiderFeet uses Trajan for:** CI/CD supply-chain examination scenarios; structured capture via `-o json`; graph mapping of redacted findings (**never** raw secret bytes from retrieve/attack).

---

## 1. Install and path

### This workspace

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\trajan\trajan.exe` |
| Version | **1.0.2** |
| Help capture | **2026-08-10** (`.tmp_trajan_help/`) |

```powershell
& C:\projects\spiderfeet\.tools\trajan\trajan.exe version
& C:\projects\spiderfeet\.tools\trajan\trajan.exe --help
```

Optional: put `trajan` on `PATH`, or set an alias.

### Upstream install

Prebuilt binaries: [Releases](https://github.com/praetorian-inc/trajan/releases). From source (see upstream README): clone and `make build`.

### Verify

```bash
trajan version
trajan github scan --list
```

Full live help: `.docs/docs-for-cli-tools/Trajan-CLI-Options.md` (section **Captured help**).

---

## 2. Credentials

Prefer environment variables over `--token` on the command line.

| Platform | Common env / flags (from help) |
|----------|--------------------------------|
| GitHub | `GH_TOKEN` / `GITHUB_TOKEN`; GHES `--url` |
| GitLab | `GITLAB_TOKEN` / `GL_TOKEN`; self-hosted `--url` |
| Azure DevOps | `AZURE_DEVOPS_PAT` / `AZDO_PAT`; Entra `--azure-bearer-token` / `AZURE_BEARER_TOKEN` |
| Bitbucket | token + `--email` (`BITBUCKET_EMAIL` / `BB_EMAIL`) + `--workspace` |
| Jenkins | `--username` / `--password` (`JENKINS_USERNAME` / `JENKINS_PASSWORD`) |
| JFrog | `JFROG_TOKEN` or `-u`/`-p` + `--url` |

**Authorized targets only.** Tokens can read secrets metadata and trigger pipeline side effects under attack modes.

---

## 3. Core workflow: enumerate → scan (JSON)

```bash
export GH_TOKEN="..."   # or Windows: $env:GH_TOKEN = "..."

trajan github enumerate token -o json
trajan github scan --repo owner/repo -o json > trajan-repo.json
```

List detectors:

```bash
trajan github scan --list
```

Focus severity / capabilities:

```bash
trajan github scan --repo owner/repo --severity critical,high -o json
trajan github scan --repo owner/repo --capabilities pwn_request,artifact_poisoning -o json
```

**Structured export (SpiderFeet / automation — preferred):**

```bash
trajan github scan --repo owner/repo -o json
```

Do **not** treat default `console` output as the corpus structured artifact when JSON is available.

---

## 4. Output formats

| `-o` / `--output` | Use |
|-------------------|-----|
| `json` | **SpiderFeet primary** |
| `sarif` | CI / code scanning |
| `html` | Human report |
| `console` | Default operator view |

---

## 5. Platforms (1.0.2)

### GitHub (fullest)

```bash
trajan github enumerate repos -o json
trajan github scan --org myorg --concurrency 10 -o json
trajan github scan --path ./.github/workflows -o json
trajan github search -p sourcegraph -o json
```

### GitLab

```bash
trajan gitlab enumerate projects -o json
trajan gitlab scan --project group/project -o json
trajan gitlab scan --group mygroup -o json
trajan gitlab scan --path ./.gitlab-ci.yml -o json
```

### Azure DevOps

```bash
trajan ado enumerate token --org myorg -o json
trajan ado scan --org myorg --repo project/repo -o json
trajan ado scan --path ./azure-pipelines.yml -o json
```

### Bitbucket (enumerate only)

```bash
trajan bitbucket enumerate token --email you@example.com --workspace my-ws -o json
```

### Jenkins

```bash
trajan jenkins enumerate access --username user --password "$JENKINS_PASSWORD" -o json
trajan jenkins scan --url https://jenkins.example.com -o json
trajan jenkins scan --path ./Jenkinsfile -o json
```

### JFrog

```bash
trajan jfrog scan --url https://acme.jfrog.io --secrets --token-info -o json
```

Help states JFrog does **not** support vulnerability scanning of CI/CD pipelines — secrets/token-info enumeration only.

---

## 6. Offline / path mode

When API access is limited:

```bash
trajan github scan --path ./.github/workflows -o json
trajan gitlab scan --path ./ci -o json
trajan ado scan --path ./pipelines -o json
trajan jenkins scan --path ./Jenkinsfile -o json
```

`--timeout` applies in offline mode (help: `0` = 5m default). Mark results as **partial coverage** — API-only detections and live Jenkins instance checks are skipped.

---

## 7. Offensive paths (ROE only)

Help for `attack` includes: **SAFETY WARNING — executes real attacks that modify resources. Always use `--dry-run` first.**

```bash
# Preview
trajan github attack --repo owner/repo --plugin secrets-dump --dry-run -o json

# Live requires --confirm — do not run without written authorization
# trajan github attack --repo owner/repo --plugin secrets-dump --confirm -o json

# After secrets-dump workflow completes
# trajan github retrieve --run-id <id> --repo owner/repo -o json
```

For SpiderFeet corpus profiling, prefer **`scan` / `enumerate` JSON**. Do not harvest live attack loot into examination graphs. Redact everything.

---

## 8. Expand safely

```bash
trajan github scan --org myorg --concurrency 10 -o json > trajan-org.json
```

Staged rollout: one repo → critical deploy/release repos → full org/group. Lower concurrency under rate limits.

---

## 9. Convert to SpiderFeet nuggets

Build `nodes` / `edges` from **JSON findings** (redacted):

- Finding summary → `VULNERABILITY_GENERAL` (or catalogue CVE tiers if CVE ids appear)
- Detection name / workflow path → `RAW_RIR_DATA` / `RAW_FILE_META_DATA`
- Host → `INTERNET_NAME`

See `.cursor/skills/trajan/references/nugget-mapping.md`. Never store retrieve/attack secret values as `nugget_data`.

---

## 10. Operational playbook

1. Authorize scope and store tokens securely
2. `enumerate token` / access probe
3. Baseline single-target `scan -o json`
4. Validate parser / nugget mapping
5. Org or critical-set sweep
6. Optional ROE-gated attack verification + cleanup
7. Remediate; differential re-scan

---

## 11. Common mistakes

- Using console output as structured evidence when `-o json` exists
- Treating `--path` offline scans as full API coverage
- Running `attack` / `retrieve` without ROE, or without `--dry-run`
- Inventing flags from a newer upstream README than binary **1.0.2**
- Pasting raw secrets into tickets, chat, or graph nodes
- Expecting Bitbucket `scan` or JFrog pipeline CVE scan (not in 1.0.2 help)

---

## 12. Useful references

- Skill: `.cursor/skills/trajan/SKILL.md`
- References index: `.cursor/skills/trajan/references/SKILLS.md`
- CLI options + Captured help: `Trajan-CLI-Options.md`
- Upstream: https://github.com/praetorian-inc/trajan
