# Aurelian Zero to Hero — Multi-Cloud Recon

Operator guide from install through identity checks, secrets/exposure/IAM/takeover modules, structured capture (`-f`), and SpiderFeet nugget mapping.

Skill reference: `.cursor/skills/Aurelian/SKILL.md`

**Binary:** `aurelian` (Praetorian). Skill folder: `Aurelian`.

---

## 0. What Aurelian does

**Aurelian** ([praetorian-inc/aurelian](https://github.com/praetorian-inc/aurelian)) is a **multi-cloud security reconnaissance** CLI. One command shape works across providers:

```text
aurelian <aws|azure|gcp> <recon|analyze> <module> [flags]
```

It helps you:

- Find **hardcoded secrets** in cloud resources (via [Titus](https://github.com/praetorian-inc/titus))
- Detect **publicly accessible** resources
- Analyze **IAM privilege escalation** paths (AWS graph / offline analyze)
- Find **subdomain / CDN / CDK** takeover candidates
- Run **OPSEC-aware** AWS identity checks (`whoami`)

Aurelian does **not**:

- Replace compliance CSPM frameworks (Prowler / ScoutSuite)
- Replace CI/CD supply-chain scanning (**Trajan**)
- Replace general repo secret scanning outside cloud extract paths (**Titus** / Nosey Parker standalone)

**SpiderFeet uses:** `-f/--output-file` (and module output dirs) → structured artifacts → redacted nugget graphs.

**This guide matches binary 1.0.4** (Captured help **2026-08-10**). Do not invent flags.

---

## 1. Install and path

### This workspace

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\aurelian\aurelian.exe` |
| Version | **1.0.4** (build `09333e9e`, built `2026-06-24T14:06:03Z`) |
| Help capture | **2026-08-10** (`.tmp_aurelian_help/`) |

```powershell
& C:\projects\spiderfeet\.tools\aurelian\aurelian.exe version
& C:\projects\spiderfeet\.tools\aurelian\aurelian.exe --help
& C:\projects\spiderfeet\.tools\aurelian\aurelian.exe list-modules
```

### Upstream install

From [README](https://github.com/praetorian-inc/aurelian):

```bash
git clone https://github.com/praetorian-inc/aurelian.git
cd aurelian
go build -o aurelian main.go   # Go 1.24+
```

Docker / releases: see upstream docs and [GitHub releases](https://github.com/praetorian-inc/aurelian/releases).

### Verify

```bash
aurelian version
aurelian list-modules
```

Full live help: `.docs/docs-for-cli-tools/Aurelian-CLI-Options.md` (**Captured help**).

### Windows host quirk

On this capture host, commands often print:

```text
ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
```

before normal output. Treat as a **path quirk**, not a module finding.

---

## 2. Credentials and scope

Configure provider CLIs / env as usual (AWS profiles, Azure CLI / env, GCP ADC or `-c/--creds-file`). Aurelian modules take scope flags from help, for example:

| Cloud | Common scope flags (from help) |
|-------|--------------------------------|
| AWS | `-p/--profile`, `-p/--profiles`, `--profile-dir`, `-r/--regions`, `-a/--resource-arn`, `-t/--resource-type` |
| Azure | `-s/--subscription-ids` (default `all`) |
| GCP | `-p/--project-id`, `-o/--org-id`, `--folder-id`, `-c/--creds-file` |

**Authorized targets only.** Even read-only enumeration can generate CloudTrail / activity logs (except OPSEC-oriented `whoami` techniques).

---

## 3. First commands

```bash
aurelian aws recon whoami -f whoami.json
aurelian list-modules
```

Whoami techniques (`--action`): `timestream`, `pinpoint`, `sqs`, or `all` (default).

---

## 4. Secrets discovery

```bash
aurelian aws recon find-secrets -f aws-secrets.json
aurelian azure recon find-secrets -s <subscription-id> -f azure-secrets.json
aurelian gcp recon find-secrets -p <project-id> -f gcp-secrets.json
```

Useful flags (see Captured help): `--validate`, `--ruleset`, `--db-path`, `--disabled-titus-rules`, `--concurrency`, AWS `-r`/`-t`/`-a`.

**Redact** all secret values before sharing.

---

## 5. Public resources and inventory

```bash
aurelian aws recon public-resources -f aws-public.json
aurelian aws recon list-all --scan-type summary -f aws-list.json
aurelian azure recon public-resources -s <subscription-id> -f azure-public.json
aurelian gcp recon public-resources -p <project-id> -f gcp-public.json
```

---

## 6. IAM privilege paths (AWS)

Fast path (no Neo4j):

```bash
aurelian aws recon iam-quick-analyze -p default -f iam-quick.json
```

Full graph (JSON; optional Neo4j):

```bash
aurelian aws recon graph -f aws-graph.json
aurelian aws recon graph --neo4j-uri bolt://localhost:7687 -f aws-graph-neo4j.json
aurelian aws analyze graph --neo4j-uri bolt://localhost:7687 -f iam-paths.json
```

Offline from GAAD:

```bash
aurelian aws recon account-auth-details -f gaad.json
aurelian aws analyze analyze-iam-permissions --gaad-file gaad.json -f iam-offline.json
```

---

## 7. Takeover and Azure configuration

```bash
aurelian aws recon subdomain-takeover -f aws-takeover.json
aurelian aws recon cloudfront-s3-takeover -f cf-takeover.json
aurelian aws recon cdk-bucket-takeover -f cdk-takeover.json
aurelian azure recon subdomain-takeover -s <subscription-id> -f azure-takeover.json
aurelian azure recon configuration-scan -s <subscription-id> -f azure-config.json
aurelian gcp recon subdomain-takeover -p <project-id> -f gcp-takeover.json
```

Azure APIM:

```bash
aurelian azure recon apim-audit -s <subscription-id> -f apim-audit.json
# apim-cross-tenant: default --mode passive; authenticated/bypass need explicit ROE
```

---

## 8. Practical workflow

1. Authorize scope and configure cloud credentials  
2. `whoami` / identity check  
3. `public-resources` (+ optional `list-all`)  
4. `find-secrets`  
5. IAM graph / quick-analyze / offline analyze  
6. Takeover + configuration modules  
7. Capture with `-f`, redact, map nuggets  

---

## 9. Convert to SpiderFeet nuggets

Build `nodes` / `edges` from **structured files** (not banners):

- Open buckets → `CLOUD_STORAGE_BUCKET_OPEN`  
- Hostnames / dangling DNS → `INTERNET_NAME` / hijackable affiliate types when evidenced  
- Misconfig / IAM paths → `VULNERABILITY_GENERAL` (redacted)  
- Descriptors (module, account, technique) → `RAW_RIR_DATA`  
- Confirmed credentials only → `PASSWORD_COMPROMISED` (never store raw secret)

See `.cursor/skills/Aurelian/references/nugget-mapping.md`.

---

## 10. Common pitfalls

- Inventing flags from README that are absent in **1.0.4** `--help`
- Using Azure `--subscription-id` (singular) — this binary uses `-s/--subscription-ids`
- Treating Windows `enrich\aws` ERROR lines as scan failures
- Treating empty output as clean without proving permissions/scope
- Sharing unredacted secrets or `get-console` URLs
- Running `apim-cross-tenant` bypass/authenticated modes without offensive ROE
- Skipping `-f` and losing structured evidence for corpus/graph work
