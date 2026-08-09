# Aurelian CLI Options (skill reference)

Authoritative live help is pasted in `.docs/docs-for-cli-tools/Aurelian-CLI-Options.md` (**Captured help**, dated **2026-08-10**). Do not invent flags.

## Binary / version

| Field | Value |
|-------|-------|
| Windows | `C:\projects\spiderfeet\.tools\aurelian\aurelian.exe` |
| Version | **1.0.4** |
| Build | `09333e9e` |
| Built at | `2026-06-24T14:06:03Z` |
| Help capture | `.tmp_aurelian_help/` |

## Command tree (from root + list-modules)

| Command | Role |
|---------|------|
| `aws` (`amazon`) | `recon` (14 modules) + `analyze` (6 modules) |
| `azure` (`az`) | `recon` (8 modules) |
| `gcp` (`google`) | `recon` (4 modules) |
| `list-modules` | Tree of installed modules |
| `version` | Print version |
| `gendoc` | Generate Markdown documentation |
| `completion` | Shell completions (bash, zsh, fish, powershell) |
| `help` | Help about any command |

Global flags: `-h/--help`, `--no-color`, `--output-dir` (default `aurelian-output`), `-f/--output-file` (overrides `--output-dir`), `--quiet`.

### AWS recon modules

`account-auth-details`, `cdk-bucket-takeover`, `cloudfront-s3-takeover`, `cost-summary`, `find-secrets`, `get-console`, `graph`, `iam-quick-analyze`, `list-all`, `org-policies`, `public-resources`, `resource-policies`, `subdomain-takeover`, `whoami`

### AWS analyze modules

`access-key-to-account-id`, `analyze-iam-permissions`, `expand-actions`, `graph`, `ip-lookup`, `known-account`

### Azure recon modules

`apim-audit`, `apim-cross-tenant`, `conditional-access-policies`, `configuration-scan`, `find-secrets`, `list-all`, `public-resources`, `subdomain-takeover`

### GCP recon modules

`find-secrets`, `list-all`, `public-resources`, `subdomain-takeover`

## SpiderFeet preferred commands

```bash
aurelian aws recon whoami -f whoami.json
aurelian aws recon find-secrets -f aws-secrets.json
aurelian aws recon public-resources -f aws-public.json
aurelian aws recon graph -f aws-graph.json
aurelian aws recon iam-quick-analyze -p default -f iam-quick.json
aurelian azure recon find-secrets -s <subscription-id> -f azure-secrets.json
aurelian gcp recon public-resources -p <project-id> -f gcp-public.json
aurelian list-modules
```

| Prefer | Avoid for corpus |
|--------|------------------|
| `-f` / `--output-file` structured captures | Banner/TTY as sole evidence |
| Module `--output-dir` when writing multi-file runs | Mixing unrelated modules in one unlabelled dump |
| Explicit `-s` / `-p` scope on Azure/GCP | Silent `all` sweeps without ROE |
| `iam-quick-analyze` / offline `analyze-iam-permissions` when sufficient | Always requiring Neo4j |

## Flag classes (names only — see Captured help)

- **Global output:** `--output-dir`, `-f/--output-file`, `--no-color`, `--quiet`
- **AWS common:** `-p/--profile`, `--profiles`, `--profile-dir`, `-r/--regions`, `-a/--resource-arn`, `-t/--resource-type`, `--concurrency`, `--opsec_level`
- **AWS IAM / Neo4j:** `--neo4j-uri`, `--neo4j-username`, `--neo4j-password`, `--gaad-file`, `--org-policies-file`, `--resource-policies-file`, `--resources-file`, `-D/--gaad-dir`
- **AWS secrets (Titus):** `--db-path`, `--ruleset`, `--disabled-titus-rules`, `--ignore-file`, `--validate`, `--max-events`, `--max-streams`
- **Azure scope:** `-s/--subscription-ids` (default `all`), `-i/--resource-id` (find-secrets), `--template-dir`
- **GCP scope:** `-p/--project-id`, `-o/--org-id`, `--folder-id`, `-c/--creds-file`, `--include-sys-projects`, `-t/--resource-type`
- **whoami:** `--action` (`timestream`, `pinpoint`, `sqs`, or `all`)
- **APIM cross-tenant:** `--target`, `--mode`, `--email`, `--password`, `--attacker`, `--openai-key`, `-k/--insecure`, …

## Windows host quirk

Captures show ERROR lines for missing `enrich\aws` and `analysis\aws` before normal output. Not findings — see CLI Options doc.

## Examples

```bash
aurelian version
aurelian aws recon whoami --action all -f whoami.json
aurelian aws recon list-all --scan-type summary -f list-summary.json
aurelian aws analyze known-account --account-id 123456789012 -f known.json
aurelian azure recon configuration-scan -s <id> -f config.json
aurelian gcp recon list-all -p <project-id> -f gcp-list.json
```
