---
name: Aurelian
description: Run multi-cloud reconnaissance with Aurelian across AWS, Azure, and GCP. Trigger for cloud secret hunting, public resource exposure checks, IAM privilege path analysis, subdomain takeover checks, or OPSEC-aware cloud identity recon.
---

# Aurelian — Multi-Cloud Recon Framework

## Purpose

Use when you must run **authorized multi-cloud security reconnaissance** with [Praetorian Aurelian](https://github.com/praetorian-inc/aurelian) across **AWS / Azure / GCP** — secrets (`find-secrets` + Titus), public exposure, IAM privilege paths, subdomain/CDN takeovers, and OPSEC-aware identity checks — then convert **structured** module outputs into SpiderFeet nugget graphs.

**Binary (this host):**

| Platform | Path |
|----------|------|
| Windows | `C:\projects\spiderfeet\.tools\aurelian\aurelian.exe` |

**Version:** **1.0.4** (`aurelian version` — build `09333e9e`, built `2026-06-24T14:06:03Z`). Help capture: **2026-08-10** (`.tmp_aurelian_help/`).

Command shape: `aurelian <platform> <category> <module> [flags]`  
Platforms: `aws` (`amazon`), `azure` (`az`), `gcp` (`google`).  
`list-modules` on 1.0.4: **20 AWS, 8 Azure, 4 GCP**.

## Step-by-Step Instructions

1. **Confirm authorization and cloud scope** — accounts / subscriptions / projects / orgs; record ROE before any API call (including “read-only” Cloud Control / Resource Graph / Graph API traffic).
2. **Verify binary** — `aurelian version` and `aurelian --help` (verbatim Captured help in `.docs/docs-for-cli-tools/Aurelian-CLI-Options.md`). Ignore or note the Windows `enrich\aws` / `analysis\aws` ERROR lines if present (host quirk — not findings).
3. **Enumerate modules** — `aurelian list-modules` then `aurelian <platform> <category> <module> --help` for exact flags (do not invent).
4. **Establish identity / baseline**
   - AWS: `aurelian aws recon whoami` (CloudTrail-silent techniques: `timestream` / `pinpoint` / `sqs` / `all`).
   - Inventory: `list-all` (AWS Cloud Control; Azure Resource Graph; GCP hierarchy).
5. **Run modules by objective** (always prefer `-f` / `--output-file` for SpiderFeet):
   - Secrets → `find-secrets` (optional `--validate`, Titus `--ruleset` / `--db-path`).
   - Exposure → `public-resources` (Azure/GCP scope via `-s` / `-p` as in help).
   - IAM → `aws recon graph` (JSON default; optional `--neo4j-uri`), or faster `iam-quick-analyze`; offline `aws analyze analyze-iam-permissions --gaad-file …`.
   - Takeover → `subdomain-takeover`; AWS also `cdk-bucket-takeover`, `cloudfront-s3-takeover`.
   - Azure extras → `configuration-scan`, `conditional-access-policies`, `apim-audit` (and only with explicit ROE: `apim-cross-tenant`).
6. **Preserve structured artifacts** — use global `-f/--output-file` (overrides `--output-dir`) or module `--output-dir` (default `aurelian-output`). Prefer JSON/files modules emit; do not treat ANSI banners as structured source.
7. **Normalize findings** — tag `cloud`, scope id, module name, resource id/type, finding class; keep permission failures as blocked coverage.
8. **Map nuggets** — redacted secrets / exposures / IAM paths / DNS names per `references/nugget-mapping.md` (catalogue first: `CLOUD_STORAGE_BUCKET(_OPEN)`, `INTERNET_NAME`, `VULNERABILITY_GENERAL`, `RAW_RIR_DATA`, `PASSWORD_COMPROMISED` only when confirmed).
9. **Re-validate high-risk hits** before escalation; chain to Titus skill only when Aurelian already embedded Titus output needs separate triage.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-f` / `--output-file` (or explicit `--output-dir`); never parse TTY alone |
| Objective is credential exposure | Start `find-secrets`; optional `--validate` only when outbound checks are authorized |
| Objective is internet exposure | Run `public-resources` (and AWS `resource-policies` / `org-policies` when policy context matters) |
| AWS privilege movement in scope | Prefer `iam-quick-analyze` for speed; full `recon graph` (+ optional Neo4j) for depth; offline `analyze analyze-iam-permissions` when GAAD files exist |
| Stealth / OPSEC priority (AWS) | Run `whoami` early; tune `--opsec_level` only with values your build accepts (help default `"none"` — verify before inventing levels) |
| Azure subscription scope | Use `-s/--subscription-ids` (default `[all]`) — **not** a singular `--subscription-id` flag on this binary |
| GCP project/org/folder scope | Use `-p/--project-id`, `-o/--org-id`, `--folder-id`, optional `-c/--creds-file` |
| Need GAAD for offline IAM | `aws recon account-auth-details` then `aws analyze analyze-iam-permissions --gaad-file …` |
| Neo4j path hunting after seed | `aws recon graph --neo4j-uri …` then `aws analyze graph --neo4j-uri …` |
| APIM developer-portal attack modes | `apim-cross-tenant` only with explicit offensive ROE; default help mode is `passive` |
| Empty module output | Treat as suspect until permissions / scope / profile are proven; record AccessDenied as blocker, not clean miss |
| Windows ERROR about `enrich\aws` | Document as host quirk; continue — help still printed |

## Guardrails & Pitfalls

- **Authorized testing only** — cloud recon touches sensitive metadata, policies, and possible secret material.
- **Do not invent flags** — authoritative surface is Captured help **2026-08-10** for **1.0.4**. README may mention behaviors not listed in `--help`.
- **Redact secrets** — never paste raw keys/tokens from `find-secrets` / Titus / console URLs into chat or tickets.
- **Discovery ≠ exploitability** — public exposure and takeover candidates need validation before claim.
- **Rate limits / concurrency** — many modules default `--concurrency 5`; widen only with approval.
- **`get-console`** — generates federated console sign-in URLs (STS); treat as sensitive session material.
- **Azure `apim-cross-tenant`** — `authenticated` / `bypass` modes are offensive (captcha relay, account creation); do not run casually.
- **Preserve module provenance** — which module emitted which finding matters for remediation and graph edges.
- **Structured-first** — CLI Profiling / corpus must use file outputs (`-f`), not banner text.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Command tree, SpiderFeet defaults, Captured help pointer |
| `output-and-parsing.md` | Output dirs/files, module artifact shapes |
| `nugget-mapping.md` | Findings → SpiderFeet `nodes[]` / `edges[]` |
| `tactics.md` | Sequencing, rich/sparse/error tactics |
| `sources.md` | Official repo, blog, releases, docs |

Operator guides: `.docs/docs-for-cli-tools/Aurelian-Zero-to-Hero.md`, `Aurelian-CLI-Options.md`.

## Comprehensive Examples

### IDENTITY / MODULE TREE

```bash
aurelian version
aurelian list-modules
aurelian aws recon whoami -f whoami.json
aurelian aws recon whoami --action timestream -f whoami-ts.json
```

### SECRETS (TITUS)

```bash
aurelian aws recon find-secrets -f aws-secrets.json
aurelian aws recon find-secrets -r us-east-1 -t AWS::Lambda::Function --validate -f lambda-secrets.json
aurelian azure recon find-secrets -s <subscription-id> -f azure-secrets.json
aurelian gcp recon find-secrets -p <project-id> -f gcp-secrets.json
```

### PUBLIC EXPOSURE / INVENTORY

```bash
aurelian aws recon public-resources -f aws-public.json
aurelian aws recon list-all --scan-type summary -f aws-list-summary.json
aurelian azure recon public-resources -s <subscription-id> -f azure-public.json
aurelian gcp recon public-resources -p <project-id> -f gcp-public.json
```

### IAM (AWS)

```bash
aurelian aws recon iam-quick-analyze -p default -f iam-quick.json
aurelian aws recon graph -f aws-graph.json
aurelian aws recon graph --neo4j-uri bolt://localhost:7687 -f aws-graph-neo4j.json
aurelian aws recon account-auth-details -f gaad.json
aurelian aws analyze analyze-iam-permissions --gaad-file gaad.json -f iam-offline.json
aurelian aws analyze graph --neo4j-uri bolt://localhost:7687 -f iam-paths.json
```

### TAKEOVER / AZURE CONFIG

```bash
aurelian aws recon subdomain-takeover -f aws-takeover.json
aurelian aws recon cloudfront-s3-takeover -f cf-s3-takeover.json
aurelian azure recon subdomain-takeover -s <subscription-id> -f azure-takeover.json
aurelian azure recon configuration-scan -s <subscription-id> -f azure-config.json
aurelian gcp recon subdomain-takeover -p <project-id> -f gcp-takeover.json
```

### OFFLINE / UTILITY ANALYZE

```bash
aurelian aws analyze access-key-to-account-id -k AKIA... -f account-from-key.json
aurelian aws analyze known-account --account-id 123456789012 -f known-account.json
aurelian aws analyze ip-lookup --ip 3.5.140.2 -f aws-ip.json
aurelian aws analyze expand-actions --action 's3:Get*' -f expand-s3.json
```

### PREFERRED SPIDERFEET PATH (WINDOWS)

```powershell
& C:\projects\spiderfeet\.tools\aurelian\aurelian.exe aws recon whoami -f whoami.json
& C:\projects\spiderfeet\.tools\aurelian\aurelian.exe aws recon find-secrets -f aws-secrets.json
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **whoami → exposure → secrets → IAM → takeover** for AWS offensive recon sequencing.
2. **One account/subscription/project first** — prove parsers and permissions before org-wide sweeps.
3. **Structured-first** — `-f` JSON/files are examination sources; map catalogue nuggets; redact secrets.
4. **Split live vs offline IAM** — collect GAAD / policies once; re-run `analyze` modules without re-enumerating.
5. **Treat empty + AccessDenied distinctly** — empty is not clean until scope is proven.
