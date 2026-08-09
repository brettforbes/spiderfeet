# Aurelian CLI Options

Operator reference for **`aurelian`** **1.0.4** ([praetorian-inc/aurelian](https://github.com/praetorian-inc/aurelian)). Prefer structured artifacts written with `-f` / `--output-file` (and module `--output-dir` when used) for SpiderFeet corpus and automation.

## SpiderFeet preferred commands

```bash
# Identity (OPSEC-aware AWS)
aurelian aws recon whoami -f whoami.json

# Secrets (Titus-backed) — capture to file
aurelian aws recon find-secrets -f aws-find-secrets.json
aurelian azure recon find-secrets -s <subscription-id> -f azure-find-secrets.json
aurelian gcp recon find-secrets -p <project-id> -f gcp-find-secrets.json

# Public exposure
aurelian aws recon public-resources -f aws-public.json
aurelian azure recon public-resources -s <subscription-id> -f azure-public.json
aurelian gcp recon public-resources -p <project-id> -f gcp-public.json

# IAM (AWS): live graph JSON, quick analyze, offline analyze
aurelian aws recon graph -f aws-graph.json
aurelian aws recon iam-quick-analyze -p default -f iam-quick.json
aurelian aws recon account-auth-details -f gaad.json
aurelian aws analyze analyze-iam-permissions --gaad-file gaad.json -f iam-analyze.json

# Takeover
aurelian aws recon subdomain-takeover -f aws-takeover.json
```

| Field | Value |
|-------|-------|
| Version | **1.0.4** (build `09333e9e`, built `2026-06-24T14:06:03Z`) |
| Windows binary | `C:\projects\spiderfeet\.tools\aurelian\aurelian.exe` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_aurelian_help/*.txt` |
| Skill | `.cursor/skills/Aurelian/SKILL.md` |

> Flags below are from live `--help` on **1.0.4** only. Do not invent options. Upstream README may document behaviors or flag values not spelled out in help — verify against Captured help before use.

### Global flags (all commands)

From root help: `-h/--help`, `--no-color`, `--output-dir` (default `aurelian-output`), `-f/--output-file` (overrides `--output-dir`), `--quiet`.

### Observed Windows host quirk

On this capture host, every invocation printed:

```text
ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
```

These lines appear **before** normal help/version/module output. Treat them as a **host/binary path quirk** (relative `enrich\aws` / `analysis\aws` lookups), not as module findings. They are retained in Captured help blocks below because they were present in stdout.

### Command tree (1.0.4)

`aurelian <platform> <category> <module> [flags]`

| Platform | Alias | Categories | Module count (`list-modules`) |
|----------|-------|------------|-------------------------------|
| `aws` | `amazon` | `recon`, `analyze` | 20 AWS |
| `azure` | `az` | `recon` | 8 Azure |
| `gcp` | `google` | `recon` | 4 GCP |

Utilities: `list-modules`, `version`, `gendoc`, `completion`, `help`.

---

## Captured help

Live help text captured from `C:\projects\spiderfeet\.tools\aurelian\aurelian.exe` on **2026-08-10**. Each block is the full stdout of the listed command (including ERROR lines and ANSI sequences where present). Source files: `.tmp_aurelian_help/`.

### Root (`aurelian --help`)

Source: `root_help.txt`

```text
2026/08/10 02:58:31 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:58:31 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Aurelian is a cloud security testing framework that helps identify
potential security issues in cloud environments.

Usage:
  aurelian [command]

Available Commands:
  aws          aws platform commands
  azure        azure platform commands
  completion   Generate the autocompletion script for the specified shell
  gcp          gcp platform commands
  gendoc       Generate Markdown documentation
  help         Help about any command
  list-modules Display available Aurelian modules in a tree structure
  version      Print the version number of Aurelian

Flags:
  -h, --help                 help for aurelian
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian [command] --help" for more information about a command.
```

### Version output (`aurelian version`)

Source: `version.txt`

```text
2026/08/10 02:58:31 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:58:31 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Aurelian 1.0.4, build 09333e9e, built at 2026-06-24T14:06:03Z
```

### `version` help (`aurelian version --help`)

Source: `version_help.txt`

```text
2026/08/10 02:59:03 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:03 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
All software has versions. This is Aurelian's

Usage:
  aurelian version [flags]

Flags:
  -h, --help   help for version

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `list-modules` help (`aurelian list-modules --help`)

Source: `list-modules_help.txt`

```text
2026/08/10 02:59:03 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:03 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Display available Aurelian modules in a tree structure

Usage:
  aurelian list-modules [flags]

Flags:
  -h, --help   help for list-modules

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `list-modules` output (`aurelian list-modules`)

Source: `list-modules_out.txt` (ANSI banner retained)

```text
2026/08/10 02:59:03 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:03 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
[1;38;2;230;56;72m                      _ _            [0m 
[1;38;2;230;56;72m  __ _ _   _ _ __ ___| (_) __ _ _ __  [0m
[1;38;2;230;56;72m / _` | | | | '__/ _ \ | |/ _` | '_ \ [0m
[1;38;2;230;56;72m| (_| | |_| | | |  __/ | | (_| | | | |[0m
[1;38;2;230;56;72m \__,_|\__,_|_|  \___|_|_|\__,_|_| |_|[0m
[1;38;2;230;56;72m[0m                                      
[1;38;2;230;56;72m Praetorian Security, Inc.[0m            
[1;38;2;230;56;72m 20 AWS, 8 Azure, 4 GCP modules[0m       

aws
├─ analyze
  ├─ access-key-to-account-id - Derives the AWS account ID from an access key ID using base32 decoding without making any API calls.
  ├─ analyze-iam-permissions - Analyzes IAM permissions from GAAD data to detect privilege escalation paths, cross-account access, and create-then-use attack patterns. Requires GAAD JSON file from account-auth-details module.
  ├─ expand-actions - Expands wildcard IAM action patterns (e.g. s3:Get* or *) into the full list of matching AWS actions by fetching the AWS Policy Generator service map.
  ├─ graph - Analyzes a Neo4j graph populated by `aws recon graph --neo4j-uri` and surfaces privilege-escalation paths (non-admin principal → admin target) as risk findings. Requires --neo4j-uri pointing at the seeded graph.
  ├─ ip-lookup - Looks up an IP address against the AWS published IP ranges to determine whether it belongs to AWS, and if so, which service, region, and network border group.
  ├─ known-account - Looks up an AWS account ID against known public account databases to identify the owning organization.
├─ recon
  ├─ account-auth-details - Retrieves IAM account authorization details including users, roles, groups, and policies. Supports multiple profiles for multi-account collection. IAM is a global service, so this module always queries us-east-1 region.
  ├─ cdk-bucket-takeover - Detects AWS CDK S3 bucket takeover vulnerabilities by identifying missing CDK staging buckets and insecure IAM policies. Scans for CDK bootstrap roles and validates associated S3 buckets for potential account takeover risks.
  ├─ cloudfront-s3-takeover - Detects CloudFront distributions with S3 origins pointing to non-existent buckets, which could allow attackers to take over the domain by creating the missing bucket. Also identifies Route53 records pointing to vulnerable distributions.
  ├─ cost-summary - Use Cost Explorer to summarize the services and regions in use, displaying costs in a markdown table.
  ├─ find-secrets - Enumerates AWS resources via Cloud Control, extracts content likely to contain hardcoded secrets (EC2 user data, Lambda code, CloudFormation templates, CloudWatch logs, ECS task definitions, SSM documents and Parameter Store parameters, Step Functions executions), and scans with Titus.
  ├─ get-console - Generates a federated AWS Console sign-in URL using STS credentials. Supports three credential paths: existing assumed-role session, role assumption via AssumeRole, and federation token via GetFederationToken.
  ├─ graph - Collects AWS IAM data (GAAD, resources, policies), evaluates permissions, and detects privilege escalation paths. Outputs JSON by default; use --neo4j-uri to populate graph database with relationships.
  ├─ iam-quick-analyze - Quick IAM analysis: collects GAAD from one or more AWS profiles, scans for privilege escalation paths and trust relationship issues. Faster than the full graph module — no resource enumeration or Neo4j required.
  ├─ list-all - List resources in an AWS account using CloudControl API. Supports 'full' scan for all resources or 'summary' scan for key services. Can scan multiple regions concurrently.
  ├─ org-policies - Collects AWS Organizations service control policies (SCPs) and resource control policies (RCPs), including the organizational hierarchy and policy-to-target mappings.
  ├─ public-resources - Finds publicly accessible AWS resources through policy evaluation, property inspection, and enrichment. Combines resource listing, enrichment, policy fetching, and public access evaluation to identify resources that are exposed to the internet or allow anonymous access.
  ├─ resource-policies - Retrieves resource-based policies for AWS resources that support them (S3 buckets, Lambda functions, SNS topics, SQS queues, EFS file systems, OpenSearch/Elasticsearch domains). Policies are added to the ResourcePolicy property of each resource.
  ├─ subdomain-takeover - Detects dangling DNS records in Route53 that are vulnerable to subdomain takeover. Enumerates all records from public hosted zones and checks for: Elastic Beanstalk CNAME hijacking, dangling Elastic IP A records, and orphaned NS delegations.
  ├─ whoami - Covert whoami using AWS APIs that leak the caller ARN in error messages without logging to CloudTrail. Supports timestream, pinpoint, and sqs techniques.


azure
├─ recon
  ├─ apim-audit - Audits Azure API Management services for security weaknesses across two checks: (1) APIs (including MCP servers) with no authentication controls at the service, product, or API scope — inspects policy XML for validate-jwt, validate-azure-ad-token, ip-filter, and check-header elements, and confirms whether a subscription is required; (2) backends configured behind APIM that are reachable without traversing the gateway — Azure App Service backends are checked for publicNetworkAccess and IP restrictions, non-Azure backends (OpenShift, GCP Cloud Run, internal hosts) are flagged for manual triage.
  ├─ apim-cross-tenant - Enumerates Azure APIM developer portal resources (APIs, products, delegation settings) without authentication, then optionally performs a cross-tenant captcha relay attack to create an account on the target portal and enumerate authenticated resources and subscription keys.
  ├─ conditional-access-policies - Enumerates Azure AD Conditional Access Policies via the Microsoft Graph API
  ├─ configuration-scan - Detects Azure configuration issues including weak authentication, disabled RBAC, privilege escalation paths, and overly permissive access rules via Azure Resource Graph.
  ├─ find-secrets - Enumerates Azure resources via Resource Graph, extracts content likely to contain hardcoded secrets (VM user data, web app settings, automation variables, storage blobs, container env vars, Cosmos DB, APIM named values, Key Vault, and 30+ other sources), and scans with Titus.
  ├─ list-all - List all Azure resources across subscriptions using Azure Resource Graph. Supports scanning specific subscriptions or all accessible subscriptions.
  ├─ public-resources - Identifies publicly accessible Azure resources by executing Azure Resource Graph query templates against target subscriptions. Detects public storage accounts, databases, key vaults, web apps, and other resources exposed to the internet.
  ├─ subdomain-takeover - Scan for dangling DNS records in Azure DNS zones that could enable subdomain takeover. Checks CNAME records for unclaimed App Service, Blob Storage, CDN, and Traffic Manager names; A/AAAA records for orphaned public IPs; and NS delegations to non-existent Azure DNS zones.


gcp
├─ recon
  ├─ find-secrets - Enumerates GCP resources via project hierarchy, extracts content likely to contain hardcoded secrets (Compute metadata/startup scripts, Cloud Functions source, Cloud Run environment variables, App Engine environment variables), and scans with Titus.
  ├─ list-all - List GCP resources across organization, folder, or project scope. Supports filtering by resource type and evaluates public/anonymous access.
  ├─ public-resources - List GCP resources with public network exposure or anonymous access. Focuses on resource types with meaningful public access indicators.
  ├─ subdomain-takeover - Scan for dangling DNS records in Cloud DNS that could enable subdomain takeover. Checks CNAME records for non-existent Cloud Storage buckets, Cloud Run services, and App Engine apps; A/AAAA records for orphaned IPs; and NS delegations to unclaimed Cloud DNS zones.
```

### `completion` (`aurelian completion --help`)

Source: `completion_help.txt`

```text
2026/08/10 02:59:03 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:03 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Generate the autocompletion script for aurelian for the specified shell.
See each sub-command's help for details on how to use the generated script.

Usage:
  aurelian completion [command]

Available Commands:
  bash        Generate the autocompletion script for bash
  fish        Generate the autocompletion script for fish
  powershell  Generate the autocompletion script for powershell
  zsh         Generate the autocompletion script for zsh

Flags:
  -h, --help   help for completion

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian completion [command] --help" for more information about a command.
```

### `gendoc` (`aurelian gendoc --help`)

Source: `gendoc_help.txt`

```text
2026/08/10 02:59:03 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:03 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Generate Markdown documentation for the CLI and its subcommands.

Usage:
  aurelian gendoc [flags]

Flags:
  -h, --help   help for gendoc

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws` (`aurelian aws --help`)

Source: `aws_help.txt`

```text
2026/08/10 02:59:02 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:02 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
aws platform commands

Usage:
  aurelian aws [command]

Aliases:
  aws, amazon

Available Commands:
  analyze     analyze commands for aws
  recon       recon commands for aws

Flags:
  -h, --help   help for aws

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian aws [command] --help" for more information about a command.
```

### `aws recon` (`aurelian aws recon --help`)

Source: `aws_recon_help.txt`

```text
2026/08/10 02:59:33 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:33 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
recon commands for aws

Usage:
  aurelian aws recon [command]

Available Commands:
  account-auth-details   Retrieves IAM account authorization details including users, roles, groups, and policies. Supports multiple profiles for multi-account collection. IAM is a global service, so this module always queries us-east-1 region.
  cdk-bucket-takeover    Detects AWS CDK S3 bucket takeover vulnerabilities by identifying missing CDK staging buckets and insecure IAM policies. Scans for CDK bootstrap roles and validates associated S3 buckets for potential account takeover risks.
  cloudfront-s3-takeover Detects CloudFront distributions with S3 origins pointing to non-existent buckets, which could allow attackers to take over the domain by creating the missing bucket. Also identifies Route53 records pointing to vulnerable distributions.
  cost-summary           Use Cost Explorer to summarize the services and regions in use, displaying costs in a markdown table.
  find-secrets           Enumerates AWS resources via Cloud Control, extracts content likely to contain hardcoded secrets (EC2 user data, Lambda code, CloudFormation templates, CloudWatch logs, ECS task definitions, SSM documents and Parameter Store parameters, Step Functions executions), and scans with Titus.
  get-console            Generates a federated AWS Console sign-in URL using STS credentials. Supports three credential paths: existing assumed-role session, role assumption via AssumeRole, and federation token via GetFederationToken.
  graph                  Collects AWS IAM data (GAAD, resources, policies), evaluates permissions, and detects privilege escalation paths. Outputs JSON by default; use --neo4j-uri to populate graph database with relationships.
  iam-quick-analyze      Quick IAM analysis: collects GAAD from one or more AWS profiles, scans for privilege escalation paths and trust relationship issues. Faster than the full graph module — no resource enumeration or Neo4j required.
  list-all               List resources in an AWS account using CloudControl API. Supports 'full' scan for all resources or 'summary' scan for key services. Can scan multiple regions concurrently.
  org-policies           Collects AWS Organizations service control policies (SCPs) and resource control policies (RCPs), including the organizational hierarchy and policy-to-target mappings.
  public-resources       Finds publicly accessible AWS resources through policy evaluation, property inspection, and enrichment. Combines resource listing, enrichment, policy fetching, and public access evaluation to identify resources that are exposed to the internet or allow anonymous access.
  resource-policies      Retrieves resource-based policies for AWS resources that support them (S3 buckets, Lambda functions, SNS topics, SQS queues, EFS file systems, OpenSearch/Elasticsearch domains). Policies are added to the ResourcePolicy property of each resource.
  subdomain-takeover     Detects dangling DNS records in Route53 that are vulnerable to subdomain takeover. Enumerates all records from public hosted zones and checks for: Elastic Beanstalk CNAME hijacking, dangling Elastic IP A records, and orphaned NS delegations.
  whoami                 Covert whoami using AWS APIs that leak the caller ARN in error messages without logging to CloudTrail. Supports timestream, pinpoint, and sqs techniques.

Flags:
  -h, --help   help for recon

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian aws recon [command] --help" for more information about a command.
```

### `aws analyze` (`aurelian aws analyze --help`)

Source: `aws_analyze_help.txt`

```text
2026/08/10 02:59:33 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:33 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
analyze commands for aws

Usage:
  aurelian aws analyze [command]

Available Commands:
  access-key-to-account-id Derives the AWS account ID from an access key ID using base32 decoding without making any API calls.
  analyze-iam-permissions  Analyzes IAM permissions from GAAD data to detect privilege escalation paths, cross-account access, and create-then-use attack patterns. Requires GAAD JSON file from account-auth-details module.
  expand-actions           Expands wildcard IAM action patterns (e.g. s3:Get* or *) into the full list of matching AWS actions by fetching the AWS Policy Generator service map.
  graph                    Analyzes a Neo4j graph populated by `aws recon graph --neo4j-uri` and surfaces privilege-escalation paths (non-admin principal → admin target) as risk findings. Requires --neo4j-uri pointing at the seeded graph.
  ip-lookup                Looks up an IP address against the AWS published IP ranges to determine whether it belongs to AWS, and if so, which service, region, and network border group.
  known-account            Looks up an AWS account ID against known public account databases to identify the owning organization.

Flags:
  -h, --help   help for analyze

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian aws analyze [command] --help" for more information about a command.
```

### `azure` (`aurelian azure --help`)

Source: `azure_help.txt`

```text
2026/08/10 02:59:02 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:02 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
azure platform commands

Usage:
  aurelian azure [command]

Aliases:
  azure, az

Available Commands:
  recon       recon commands for azure

Flags:
  -h, --help   help for azure

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian azure [command] --help" for more information about a command.
```

### `azure recon` (`aurelian azure recon --help`)

Source: `azure_recon_help.txt`

```text
2026/08/10 02:59:33 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:33 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
recon commands for azure

Usage:
  aurelian azure recon [command]

Available Commands:
  apim-audit                  Audits Azure API Management services for security weaknesses across two checks: (1) APIs (including MCP servers) with no authentication controls at the service, product, or API scope — inspects policy XML for validate-jwt, validate-azure-ad-token, ip-filter, and check-header elements, and confirms whether a subscription is required; (2) backends configured behind APIM that are reachable without traversing the gateway — Azure App Service backends are checked for publicNetworkAccess and IP restrictions, non-Azure backends (OpenShift, GCP Cloud Run, internal hosts) are flagged for manual triage.
  apim-cross-tenant           Enumerates Azure APIM developer portal resources (APIs, products, delegation settings) without authentication, then optionally performs a cross-tenant captcha relay attack to create an account on the target portal and enumerate authenticated resources and subscription keys.
  conditional-access-policies Enumerates Azure AD Conditional Access Policies via the Microsoft Graph API
  configuration-scan          Detects Azure configuration issues including weak authentication, disabled RBAC, privilege escalation paths, and overly permissive access rules via Azure Resource Graph.
  find-secrets                Enumerates Azure resources via Resource Graph, extracts content likely to contain hardcoded secrets (VM user data, web app settings, automation variables, storage blobs, container env vars, Cosmos DB, APIM named values, Key Vault, and 30+ other sources), and scans with Titus.
  list-all                    List all Azure resources across subscriptions using Azure Resource Graph. Supports scanning specific subscriptions or all accessible subscriptions.
  public-resources            Identifies publicly accessible Azure resources by executing Azure Resource Graph query templates against target subscriptions. Detects public storage accounts, databases, key vaults, web apps, and other resources exposed to the internet.
  subdomain-takeover          Scan for dangling DNS records in Azure DNS zones that could enable subdomain takeover. Checks CNAME records for unclaimed App Service, Blob Storage, CDN, and Traffic Manager names; A/AAAA records for orphaned public IPs; and NS delegations to non-existent Azure DNS zones.

Flags:
  -h, --help   help for recon

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian azure recon [command] --help" for more information about a command.
```

### `gcp` (`aurelian gcp --help`)

Source: `gcp_help.txt`

```text
2026/08/10 02:59:03 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:03 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
gcp platform commands

Usage:
  aurelian gcp [command]

Aliases:
  gcp, google

Available Commands:
  recon       recon commands for gcp

Flags:
  -h, --help   help for gcp

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian gcp [command] --help" for more information about a command.
```

### `gcp recon` (`aurelian gcp recon --help`)

Source: `gcp_recon_help.txt`

```text
2026/08/10 02:59:33 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 02:59:33 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
recon commands for gcp

Usage:
  aurelian gcp recon [command]

Available Commands:
  find-secrets       Enumerates GCP resources via project hierarchy, extracts content likely to contain hardcoded secrets (Compute metadata/startup scripts, Cloud Functions source, Cloud Run environment variables, App Engine environment variables), and scans with Titus.
  list-all           List GCP resources across organization, folder, or project scope. Supports filtering by resource type and evaluates public/anonymous access.
  public-resources   List GCP resources with public network exposure or anonymous access. Focuses on resource types with meaningful public access indicators.
  subdomain-takeover Scan for dangling DNS records in Cloud DNS that could enable subdomain takeover. Checks CNAME records for non-existent Cloud Storage buckets, Cloud Run services, and App Engine apps; A/AAAA records for orphaned IPs; and NS delegations to unclaimed Cloud DNS zones.

Flags:
  -h, --help   help for recon

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)

Use "aurelian gcp recon [command] --help" for more information about a command.
```

### `aws analyze access-key-to-account-id` (`aurelian aws analyze access-key-to-account-id --help`)

Source: `mod_aws_analyze_access_key_to_account_id.txt`

```text
2026/08/10 03:00:07 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:07 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Derives the AWS account ID from an access key ID using base32 decoding without making any API calls.

Usage:
  aurelian aws analyze access-key-to-account-id [flags]

Flags:
  -k, --access-key-id string   AWS access key ID (AKIA... or ASIA...) (required)
  -h, --help                   help for access-key-to-account-id

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws analyze analyze-iam-permissions` (`aurelian aws analyze analyze-iam-permissions --help`)

Source: `mod_aws_analyze_analyze_iam_permissions.txt`

```text
2026/08/10 03:00:07 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:07 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Analyzes IAM permissions from GAAD data to detect privilege escalation paths, cross-account access, and create-then-use attack patterns. Requires GAAD JSON file from account-auth-details module.

Usage:
  aurelian aws analyze analyze-iam-permissions [flags]

Flags:
      --gaad-file string                Path to GAAD JSON file (from account-auth-details module) (required)
  -h, --help                            help for analyze-iam-permissions
      --org-policies-file string        Path to Org Policies JSON file (from org-policies module)
      --resource-policies-file string   Path to Resource Policies JSON file
      --resources-file string           Path to Resources JSON file (from list-all module)

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws analyze expand-actions` (`aurelian aws analyze expand-actions --help`)

Source: `mod_aws_analyze_expand_actions.txt`

```text
2026/08/10 03:00:07 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:07 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Expands wildcard IAM action patterns (e.g. s3:Get* or *) into the full list of matching AWS actions by fetching the AWS Policy Generator service map.

Usage:
  aurelian aws analyze expand-actions [flags]

Flags:
      --action string   IAM action pattern to expand (supports wildcards, e.g. s3:Get* or *) (required)
  -h, --help            help for expand-actions

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws analyze graph` (`aurelian aws analyze graph --help`)

Source: `mod_aws_analyze_graph.txt`

```text
2026/08/10 03:00:07 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:07 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Analyzes a Neo4j graph populated by `aws recon graph --neo4j-uri` and surfaces privilege-escalation paths (non-admin principal → admin target) as risk findings. Requires --neo4j-uri pointing at the seeded graph.

Usage:
  aurelian aws analyze graph [flags]

Flags:
  -h, --help                    help for graph
      --neo4j-password string   Neo4j password (default "neo4j")
      --neo4j-uri string        Neo4j connection URI (e.g., bolt://localhost:7687)
      --neo4j-username string   Neo4j username (default "neo4j")

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws analyze ip-lookup` (`aurelian aws analyze ip-lookup --help`)

Source: `mod_aws_analyze_ip_lookup.txt`

```text
2026/08/10 03:00:08 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:08 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Looks up an IP address against the AWS published IP ranges to determine whether it belongs to AWS, and if so, which service, region, and network border group.

Usage:
  aurelian aws analyze ip-lookup [flags]

Flags:
  -h, --help        help for ip-lookup
      --ip string   IP address to look up in AWS IP ranges (required)

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws analyze known-account` (`aurelian aws analyze known-account --help`)

Source: `mod_aws_analyze_known_account.txt`

```text
2026/08/10 03:00:08 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:08 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Looks up an AWS account ID against known public account databases to identify the owning organization.

Usage:
  aurelian aws analyze known-account [flags]

Flags:
      --account-id string   AWS account ID to look up (required)
  -h, --help                help for known-account

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon account-auth-details` (`aurelian aws recon account-auth-details --help`)

Source: `mod_aws_recon_account_auth_details.txt`

```text
2026/08/10 03:00:05 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:05 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Retrieves IAM account authorization details including users, roles, groups, and policies. Supports multiple profiles for multi-account collection. IAM is a global service, so this module always queries us-east-1 region.

Usage:
  aurelian aws recon account-auth-details [flags]

Flags:
  -h, --help                 help for account-auth-details
      --output-dir string    Base output directory (default "aurelian-output")
      --profile string       AWS profile to use
      --profile-dir string   Set to override the default AWS profile directory
  -p, --profiles strings     AWS profiles to collect (comma-separated)

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon cdk-bucket-takeover` (`aurelian aws recon cdk-bucket-takeover --help`)

Source: `mod_aws_recon_cdk_bucket_takeover.txt`

```text
2026/08/10 03:00:05 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:05 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Detects AWS CDK S3 bucket takeover vulnerabilities by identifying missing CDK staging buckets and insecure IAM policies. Scans for CDK bootstrap roles and validates associated S3 buckets for potential account takeover risks.

Usage:
  aurelian aws recon cdk-bucket-takeover [flags]

Flags:
  -q, --cdk-qualifiers strings   CDK bootstrap qualifiers to check (default [hnb659fds])
      --concurrency int          Maximum concurrent API requests (default 5)
  -h, --help                     help for cdk-bucket-takeover
      --opsec_level string       Operational security level for AWS operations (default "none")
      --output-dir string        Base output directory (default "aurelian-output")
  -p, --profile string           AWS profile to use
      --profile-dir string       Set to override the default AWS profile directory
  -r, --regions strings          AWS regions to scan (default [all])
  -a, --resource-arn strings     AWS target resource ARN
  -t, --resource-type strings    AWS Cloud Control resource type (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon cloudfront-s3-takeover` (`aurelian aws recon cloudfront-s3-takeover --help`)

Source: `mod_aws_recon_cloudfront_s3_takeover.txt`

```text
2026/08/10 03:00:05 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:05 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Detects CloudFront distributions with S3 origins pointing to non-existent buckets, which could allow attackers to take over the domain by creating the missing bucket. Also identifies Route53 records pointing to vulnerable distributions.

Usage:
  aurelian aws recon cloudfront-s3-takeover [flags]

Flags:
      --concurrency int         Maximum concurrent API requests (default 5)
  -h, --help                    help for cloudfront-s3-takeover
      --opsec_level string      Operational security level for AWS operations (default "none")
      --output-dir string       Base output directory (default "aurelian-output")
  -p, --profile string          AWS profile to use
      --profile-dir string      Set to override the default AWS profile directory
  -r, --regions strings         AWS regions to scan (default [all])
  -a, --resource-arn strings    AWS target resource ARN
  -t, --resource-type strings   AWS Cloud Control resource type (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon cost-summary` (`aurelian aws recon cost-summary --help`)

Source: `mod_aws_recon_cost_summary.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Use Cost Explorer to summarize the services and regions in use, displaying costs in a markdown table.

Usage:
  aurelian aws recon cost-summary [flags]

Flags:
  -d, --days int             Number of days to look back for cost data (default 30)
  -h, --help                 help for cost-summary
      --opsec_level string   Operational security level for AWS operations (default "none")
      --output-dir string    Base output directory (default "aurelian-output")
  -p, --profile string       AWS profile to use
      --profile-dir string   Set to override the default AWS profile directory

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon find-secrets` (`aurelian aws recon find-secrets --help`)

Source: `mod_aws_recon_find_secrets.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Enumerates AWS resources via Cloud Control, extracts content likely to contain hardcoded secrets (EC2 user data, Lambda code, CloudFormation templates, CloudWatch logs, ECS task definitions, SSM documents and Parameter Store parameters, Step Functions executions), and scans with Titus.

Usage:
  aurelian aws recon find-secrets [flags]

Flags:
      --concurrency int                Maximum concurrent API requests (default 5)
      --db-path string                 Path for Titus SQLite database
      --disabled-titus-rules strings   Rule IDs to exclude from scanning
  -h, --help                           help for find-secrets
      --ignore-file string             Path to gitignore-style file for skipping paths; when empty uses a default list
      --max-events int                 Max log events per log group (default 10000)
      --max-streams int                Max streams to sample per log group (default 10)
      --opsec_level string             Operational security level for AWS operations (default "none")
      --output-dir string              Base output directory (default "aurelian-output")
  -p, --profile string                 AWS profile to use
      --profile-dir string             Set to override the default AWS profile directory
  -r, --regions strings                AWS regions to scan (default [all])
  -a, --resource-arn strings           AWS target resource ARN
  -t, --resource-type strings          AWS Cloud Control resource type (default [all])
      --ruleset string                 Titus ruleset to apply; empty string disables ruleset filtering (default "default")
      --validate                       Validate detected secrets against their source APIs

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon get-console` (`aurelian aws recon get-console --help`)

Source: `mod_aws_recon_get_console.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Generates a federated AWS Console sign-in URL using STS credentials. Supports three credential paths: existing assumed-role session, role assumption via AssumeRole, and federation token via GetFederationToken.

Usage:
  aurelian aws recon get-console [flags]

Flags:
      --duration int               Session duration in seconds (900-129600) (default 3600)
      --federation-name string     Name for federation token request (default "aurelian-console")
  -h, --help                       help for get-console
      --mfa-token string           MFA token code for role assumption
      --opsec_level string         Operational security level for AWS operations (default "none")
      --output-dir string          Base output directory (default "aurelian-output")
  -p, --profile string             AWS profile to use
      --profile-dir string         Set to override the default AWS profile directory
      --role-arn string            IAM role ARN to assume before generating console URL
      --role-session-name string   Session name for assumed role (default "aurelian-console")

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon graph` (`aurelian aws recon graph --help`)

Source: `mod_aws_recon_graph.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Collects AWS IAM data (GAAD, resources, policies), evaluates permissions, and detects privilege escalation paths. Outputs JSON by default; use --neo4j-uri to populate graph database with relationships.

Usage:
  aurelian aws recon graph [flags]

Flags:
      --concurrency int            Maximum concurrent API requests (default 5)
  -h, --help                       help for graph
      --neo4j-password string      Neo4j password (default "neo4j")
      --neo4j-uri string           Neo4j connection URI (e.g., bolt://localhost:7687)
      --neo4j-username string      Neo4j username (default "neo4j")
      --opsec_level string         Operational security level for AWS operations (default "none")
      --org-policies-file string   Path to Org Policies JSON file
      --output-dir string          Base output directory (default "aurelian-output")
  -p, --profile string             AWS profile to use
      --profile-dir string         Set to override the default AWS profile directory
  -r, --regions strings            AWS regions to scan (default [all])
  -a, --resource-arn strings       AWS target resource ARN
  -t, --resource-type strings      AWS Cloud Control resource type (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon iam-quick-analyze` (`aurelian aws recon iam-quick-analyze --help`)

Source: `mod_aws_recon_iam_quick_analyze.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Quick IAM analysis: collects GAAD from one or more AWS profiles, scans for privilege escalation paths and trust relationship issues. Faster than the full graph module — no resource enumeration or Neo4j required.

Usage:
  aurelian aws recon iam-quick-analyze [flags]

Flags:
  -D, --gaad-dir string      Directory of pre-collected GAAD JSON files (skips live collection)
  -h, --help                 help for iam-quick-analyze
      --output-dir string    Base output directory (default "aurelian-output")
      --profile-dir string   Set to override the default AWS profile directory
  -p, --profiles strings     AWS profiles to analyze (comma-separated)

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon list-all` (`aurelian aws recon list-all --help`)

Source: `mod_aws_recon_list_all.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
List resources in an AWS account using CloudControl API. Supports 'full' scan for all resources or 'summary' scan for key services. Can scan multiple regions concurrently.

Usage:
  aurelian aws recon list-all [flags]

Flags:
      --concurrency int         Maximum concurrent API requests (default 5)
  -h, --help                    help for list-all
      --opsec_level string      Operational security level for AWS operations (default "none")
      --output-dir string       Base output directory (default "aurelian-output")
  -p, --profile string          AWS profile to use
      --profile-dir string      Set to override the default AWS profile directory
  -r, --regions strings         AWS regions to scan (default [all])
  -a, --resource-arn strings    AWS target resource ARN
  -t, --resource-type strings   AWS Cloud Control resource type (default [all])
  -s, --scan-type string        Scan type - 'full' for all resources or 'summary' for key services (default "full")

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon org-policies` (`aurelian aws recon org-policies --help`)

Source: `mod_aws_recon_org_policies.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Collects AWS Organizations service control policies (SCPs) and resource control policies (RCPs), including the organizational hierarchy and policy-to-target mappings.

Usage:
  aurelian aws recon org-policies [flags]

Flags:
  -h, --help                 help for org-policies
      --opsec_level string   Operational security level for AWS operations (default "none")
      --output-dir string    Base output directory (default "aurelian-output")
  -p, --profile string       AWS profile to use
      --profile-dir string   Set to override the default AWS profile directory

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon public-resources` (`aurelian aws recon public-resources --help`)

Source: `mod_aws_recon_public_resources.txt`

```text
2026/08/10 03:00:06 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:06 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Finds publicly accessible AWS resources through policy evaluation, property inspection, and enrichment. Combines resource listing, enrichment, policy fetching, and public access evaluation to identify resources that are exposed to the internet or allow anonymous access.

Usage:
  aurelian aws recon public-resources [flags]

Flags:
      --concurrency int            Maximum concurrent API requests (default 5)
  -h, --help                       help for public-resources
      --opsec_level string         Operational security level for AWS operations (default "none")
      --org-policies-file string   Path to Org Policies JSON file
      --output-dir string          Base output directory (default "aurelian-output")
  -p, --profile string             AWS profile to use
      --profile-dir string         Set to override the default AWS profile directory
  -r, --regions strings            AWS regions to scan (default [all])
  -a, --resource-arn strings       AWS target resource ARN
  -t, --resource-type strings      AWS Cloud Control resource type (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon resource-policies` (`aurelian aws recon resource-policies --help`)

Source: `mod_aws_recon_resource_policies.txt`

```text
2026/08/10 03:00:07 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:07 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Retrieves resource-based policies for AWS resources that support them (S3 buckets, Lambda functions, SNS topics, SQS queues, EFS file systems, OpenSearch/Elasticsearch domains). Policies are added to the ResourcePolicy property of each resource.

Usage:
  aurelian aws recon resource-policies [flags]

Flags:
      --concurrency int         Maximum concurrent API requests (default 5)
  -h, --help                    help for resource-policies
      --opsec_level string      Operational security level for AWS operations (default "none")
      --output-dir string       Base output directory (default "aurelian-output")
  -p, --profile string          AWS profile to use
      --profile-dir string      Set to override the default AWS profile directory
  -r, --regions strings         AWS regions to scan (default [all])
  -a, --resource-arn strings    AWS target resource ARN
  -t, --resource-type strings   AWS Cloud Control resource type (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon subdomain-takeover` (`aurelian aws recon subdomain-takeover --help`)

Source: `mod_aws_recon_subdomain_takeover.txt`

```text
2026/08/10 03:00:07 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:07 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Detects dangling DNS records in Route53 that are vulnerable to subdomain takeover. Enumerates all records from public hosted zones and checks for: Elastic Beanstalk CNAME hijacking, dangling Elastic IP A records, and orphaned NS delegations.

Usage:
  aurelian aws recon subdomain-takeover [flags]

Flags:
      --concurrency int         Maximum concurrent API requests (default 5)
  -h, --help                    help for subdomain-takeover
      --opsec_level string      Operational security level for AWS operations (default "none")
      --output-dir string       Base output directory (default "aurelian-output")
  -p, --profile string          AWS profile to use
      --profile-dir string      Set to override the default AWS profile directory
  -r, --regions strings         AWS regions to scan (default [all])
  -a, --resource-arn strings    AWS target resource ARN
  -t, --resource-type strings   AWS Cloud Control resource type (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `aws recon whoami` (`aurelian aws recon whoami --help`)

Source: `mod_aws_recon_whoami.txt`

```text
2026/08/10 03:00:07 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:07 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Covert whoami using AWS APIs that leak the caller ARN in error messages without logging to CloudTrail. Supports timestream, pinpoint, and sqs techniques.

Usage:
  aurelian aws recon whoami [flags]

Flags:
      --action string        Whoami technique: timestream, pinpoint, sqs, or all (default "all")
  -h, --help                 help for whoami
      --opsec_level string   Operational security level for AWS operations (default "none")
      --output-dir string    Base output directory (default "aurelian-output")
  -p, --profile string       AWS profile to use
      --profile-dir string   Set to override the default AWS profile directory

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon apim-audit` (`aurelian azure recon apim-audit --help`)

Source: `mod_azure_recon_apim_audit.txt`

```text
2026/08/10 03:00:08 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:08 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Audits Azure API Management services for security weaknesses across two checks: (1) APIs (including MCP servers) with no authentication controls at the service, product, or API scope — inspects policy XML for validate-jwt, validate-azure-ad-token, ip-filter, and check-header elements, and confirms whether a subscription is required; (2) backends configured behind APIM that are reachable without traversing the gateway — Azure App Service backends are checked for publicNetworkAccess and IP restrictions, non-Azure backends (OpenShift, GCP Cloud Run, internal hosts) are flagged for manual triage.

Usage:
  aurelian azure recon apim-audit [flags]

Flags:
      --concurrency int            Maximum concurrent API requests (default 5)
  -h, --help                       help for apim-audit
      --output-dir string          Base output directory (default "aurelian-output")
  -s, --subscription-ids strings   Azure subscription ID(s) or 'all' to enumerate all accessible subscriptions (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon apim-cross-tenant` (`aurelian azure recon apim-cross-tenant --help`)

Source: `mod_azure_recon_apim_cross_tenant.txt`

```text
2026/08/10 03:00:08 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:08 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Enumerates Azure APIM developer portal resources (APIs, products, delegation settings) without authentication, then optionally performs a cross-tenant captcha relay attack to create an account on the target portal and enumerate authenticated resources and subscription keys.

Usage:
  aurelian azure recon apim-cross-tenant [flags]

Flags:
      --attacker string     Attacker-controlled APIM portal URL (required for bypass mode)
      --email string        Account email (required for authenticated and bypass modes)
      --first string        First name for registration (bypass mode) (default "Test")
  -h, --help                help for apim-cross-tenant
  -k, --insecure            Skip TLS certificate verification
      --last string         Last name for registration (bypass mode) (default "User")
      --mode string         Scan mode: passive (unauthenticated enum only), authenticated (login + enum), bypass (cross-tenant captcha relay + signup + enum) (default "passive")
      --openai-key string   OpenAI API key for audio captcha transcription (bypass mode); falls back to OPENAI_API_KEY env var if unset
      --password string     Account password (required for authenticated and bypass modes)
      --target string       Target APIM developer portal URL (required)

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon conditional-access-policies` (`aurelian azure recon conditional-access-policies --help`)

Source: `mod_azure_recon_conditional_access_policies.txt`

```text
2026/08/10 03:00:08 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:08 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Enumerates Azure AD Conditional Access Policies via the Microsoft Graph API

Usage:
  aurelian azure recon conditional-access-policies [flags]

Flags:
  -h, --help                help for conditional-access-policies
      --output-dir string   Base output directory (default "aurelian-output")

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon configuration-scan` (`aurelian azure recon configuration-scan --help`)

Source: `mod_azure_recon_configuration_scan.txt`

```text
2026/08/10 03:00:08 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:08 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Detects Azure configuration issues including weak authentication, disabled RBAC, privilege escalation paths, and overly permissive access rules via Azure Resource Graph.

Usage:
  aurelian azure recon configuration-scan [flags]

Flags:
      --concurrency int            Maximum concurrent API requests (default 5)
      --enricher-timeout int       Per-resource enricher timeout in seconds (default 120)
  -h, --help                       help for configuration-scan
      --output-dir string          Base output directory (default "aurelian-output")
  -s, --subscription-ids strings   Azure subscription ID(s) or 'all' to enumerate all accessible subscriptions (default [all])
      --template-dir string        Optional directory with additional YAML query templates

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon find-secrets` (`aurelian azure recon find-secrets --help`)

Source: `mod_azure_recon_find_secrets.txt`

```text
2026/08/10 03:00:08 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:08 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Enumerates Azure resources via Resource Graph, extracts content likely to contain hardcoded secrets (VM user data, web app settings, automation variables, storage blobs, container env vars, Cosmos DB, APIM named values, Key Vault, and 30+ other sources), and scans with Titus.

Usage:
  aurelian azure recon find-secrets [flags]

Flags:
      --concurrency int                Maximum concurrent API requests (default 5)
      --db-path string                 Path for Titus SQLite database
      --disabled-titus-rules strings   Rule IDs to exclude from scanning
  -h, --help                           help for find-secrets
      --ignore-file string             Path to gitignore-style file for skipping paths; when empty uses a default list
      --max-cosmos-doc-scan int        Max total Cosmos documents to scan per container (default 50)
      --max-cosmos-doc-size int        Max individual Cosmos document size in bytes (default 1048576)
      --output-dir string              Base output directory (default "aurelian-output")
  -i, --resource-id strings            Azure resource ID(s) to scan directly, skipping enumeration
      --ruleset string                 Titus ruleset to apply; empty string disables ruleset filtering (default "default")
  -s, --subscription-ids strings       Azure subscription ID(s) or 'all' to enumerate all accessible subscriptions (default [all])
      --validate                       Validate detected secrets against their source APIs

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon list-all` (`aurelian azure recon list-all --help`)

Source: `mod_azure_recon_list_all.txt`

```text
2026/08/10 03:00:09 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:09 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
List all Azure resources across subscriptions using Azure Resource Graph. Supports scanning specific subscriptions or all accessible subscriptions.

Usage:
  aurelian azure recon list-all [flags]

Flags:
      --concurrency int            Maximum concurrent API requests (default 5)
  -h, --help                       help for list-all
      --output-dir string          Base output directory (default "aurelian-output")
  -s, --subscription-ids strings   Azure subscription ID(s) or 'all' to enumerate all accessible subscriptions (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon public-resources` (`aurelian azure recon public-resources --help`)

Source: `mod_azure_recon_public_resources.txt`

```text
2026/08/10 03:00:09 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:09 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Identifies publicly accessible Azure resources by executing Azure Resource Graph query templates against target subscriptions. Detects public storage accounts, databases, key vaults, web apps, and other resources exposed to the internet.

Usage:
  aurelian azure recon public-resources [flags]

Flags:
      --concurrency int            Maximum concurrent API requests (default 5)
  -h, --help                       help for public-resources
      --output-dir string          Base output directory (default "aurelian-output")
  -s, --subscription-ids strings   Azure subscription ID(s) or 'all' to enumerate all accessible subscriptions (default [all])
      --template-dir string        Optional directory with additional YAML query templates

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `azure recon subdomain-takeover` (`aurelian azure recon subdomain-takeover --help`)

Source: `mod_azure_recon_subdomain_takeover.txt`

```text
2026/08/10 03:00:09 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:09 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Scan for dangling DNS records in Azure DNS zones that could enable subdomain takeover. Checks CNAME records for unclaimed App Service, Blob Storage, CDN, and Traffic Manager names; A/AAAA records for orphaned public IPs; and NS delegations to non-existent Azure DNS zones.

Usage:
  aurelian azure recon subdomain-takeover [flags]

Flags:
      --concurrency int            Maximum concurrent API requests (default 5)
  -h, --help                       help for subdomain-takeover
      --output-dir string          Base output directory (default "aurelian-output")
  -s, --subscription-ids strings   Azure subscription ID(s) or 'all' to enumerate all accessible subscriptions (default [all])

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `gcp recon find-secrets` (`aurelian gcp recon find-secrets --help`)

Source: `mod_gcp_recon_find_secrets.txt`

```text
2026/08/10 03:00:09 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:09 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Enumerates GCP resources via project hierarchy, extracts content likely to contain hardcoded secrets (Compute metadata/startup scripts, Cloud Functions source, Cloud Run environment variables, App Engine environment variables), and scans with Titus.

Usage:
  aurelian gcp recon find-secrets [flags]

Flags:
      --concurrency int                Max concurrent API requests (default 5)
  -c, --creds-file string              Path to GCP credentials JSON
      --db-path string                 Path for Titus SQLite database
      --disabled-titus-rules strings   Rule IDs to exclude from scanning
      --folder-id strings              GCP folder IDs
  -h, --help                           help for find-secrets
      --ignore-file string             Path to gitignore-style file for skipping paths; when empty uses a default list
      --include-sys-projects           Include system projects
  -o, --org-id strings                 GCP organization IDs
      --output-dir string              Base output directory (default "aurelian-output")
  -p, --project-id strings             GCP project IDs
  -t, --resource-type strings          Resource types to enumerate (default [all])
      --ruleset string                 Titus ruleset to apply; empty string disables ruleset filtering (default "default")
      --validate                       Validate detected secrets against their source APIs

Global Flags:
      --no-color             Disable colored output
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `gcp recon list-all` (`aurelian gcp recon list-all --help`)

Source: `mod_gcp_recon_list_all.txt`

```text
2026/08/10 03:00:09 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:09 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
List GCP resources across organization, folder, or project scope. Supports filtering by resource type and evaluates public/anonymous access.

Usage:
  aurelian gcp recon list-all [flags]

Flags:
      --concurrency int         Max concurrent API requests (default 5)
  -c, --creds-file string       Path to GCP credentials JSON
      --folder-id strings       GCP folder IDs
  -h, --help                    help for list-all
      --include-sys-projects    Include system projects
  -o, --org-id strings          GCP organization IDs
  -p, --project-id strings      GCP project IDs
  -t, --resource-type strings   Resource types to enumerate (default [all])

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `gcp recon public-resources` (`aurelian gcp recon public-resources --help`)

Source: `mod_gcp_recon_public_resources.txt`

```text
2026/08/10 03:00:09 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:09 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
List GCP resources with public network exposure or anonymous access. Focuses on resource types with meaningful public access indicators.

Usage:
  aurelian gcp recon public-resources [flags]

Flags:
      --concurrency int         Max concurrent API requests (default 5)
  -c, --creds-file string       Path to GCP credentials JSON
      --folder-id strings       GCP folder IDs
  -h, --help                    help for public-resources
      --include-sys-projects    Include system projects
  -o, --org-id strings          GCP organization IDs
  -p, --project-id strings      GCP project IDs
  -t, --resource-type strings   Resource types to enumerate (default [all])

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

### `gcp recon subdomain-takeover` (`aurelian gcp recon subdomain-takeover --help`)

Source: `mod_gcp_recon_subdomain_takeover.txt`

```text
2026/08/10 03:00:09 ERROR failed to read subdirectory path=enrich\aws error="open enrich\\aws: file does not exist"
2026/08/10 03:00:09 ERROR failed to read subdirectory path=analysis\aws error="open analysis\\aws: file does not exist"
Scan for dangling DNS records in Cloud DNS that could enable subdomain takeover. Checks CNAME records for non-existent Cloud Storage buckets, Cloud Run services, and App Engine apps; A/AAAA records for orphaned IPs; and NS delegations to unclaimed Cloud DNS zones.

Usage:
  aurelian gcp recon subdomain-takeover [flags]

Flags:
      --concurrency int         Max concurrent API requests (default 5)
  -c, --creds-file string       Path to GCP credentials JSON
      --folder-id strings       GCP folder IDs
  -h, --help                    help for subdomain-takeover
      --include-sys-projects    Include system projects
  -o, --org-id strings          GCP organization IDs
  -p, --project-id strings      GCP project IDs
  -t, --resource-type strings   Resource types to enumerate (default [all])

Global Flags:
      --no-color             Disable colored output
      --output-dir string    Output directory (default: aurelian-output) (default "aurelian-output")
  -f, --output-file string   Output file path (overrides --output-dir)
      --quiet                Suppress user messages (overrides default verbose CLI mode)
```

