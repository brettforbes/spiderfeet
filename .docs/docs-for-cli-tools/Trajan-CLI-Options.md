# Trajan CLI Options

Operator reference for `trajan` **1.0.2**. Prefer structured JSON for SpiderFeet corpus and automation.

## SpiderFeet preferred commands

```bash
# Primary structured scan (GitHub example)
trajan github scan --repo owner/repo -o json

# Inventory then scan
trajan github enumerate token -o json
trajan gitlab scan --project group/project -o json
trajan ado scan --org myorg --repo project/repo -o json

# Offline workflow / pipeline files
trajan github scan --path ./.github/workflows -o json
```

| Field | Value |
|-------|-------|
| Version | **1.0.2** |
| Windows binary | `C:\projects\spiderfeet\.tools\trajan\trajan.exe` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_trajan_help/*.txt` |

> Flags below are from live `--help` on **1.0.2** only — do not invent options. Upstream README may describe newer CLI shapes; re-capture help after upgrades.

---

## Captured help

Live help text captured from `.tools/trajan/trajan.exe` on **2026-08-10**. Each block is the full stdout of the listed command (global options repeated by the CLI are retained).

### Version (`trajan version`)

```text
trajan version 1.0.2
  Git commit: c9a58278f157401b363150d923795a0d172fd221
  Build date: 2026-06-21T21:00:13Z
```

### Root (`trajan --help`)

```text
Trajan - CI/CD Security Scanner

Usage:
  trajan [command]

Platforms:
  github      Trajan - GitHub
  gitlab      Trajan - GitLab CI
  ado         Trajan - Azure DevOps
  bitbucket   Trajan - Bitbucket
  jenkins     Trajan - Jenkins
  jfrog       Trajan - JFrog

Utilities:
  version     Print version information
  help        Help about any command
  completion  Generate the autocompletion script for the specified shell

Flags:
  -h, --help                 help for trajan
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan [command] --help" for more information about a command.
```

### Root short (`trajan -h`)

Identical to `--help` in this capture.

```text
Trajan - CI/CD Security Scanner

Usage:
  trajan [command]

Platforms:
  github      Trajan - GitHub
  gitlab      Trajan - GitLab CI
  ado         Trajan - Azure DevOps
  bitbucket   Trajan - Bitbucket
  jenkins     Trajan - Jenkins
  jfrog       Trajan - JFrog

Utilities:
  version     Print version information
  help        Help about any command
  completion  Generate the autocompletion script for the specified shell

Flags:
  -h, --help                 help for trajan
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan [command] --help" for more information about a command.
```

### version (`trajan version --help`)

```text
Trajan - Version

Usage:
  trajan version [flags]

Flags:
  -h, --help   help for version

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output
```

### completion (`trajan completion --help`)

```text
Generate the autocompletion script for trajan for the specified shell.
See each sub-command's help for details on how to use the generated script.

Usage:
  trajan completion [command]

Available Commands:
  bash        Generate the autocompletion script for bash
  zsh         Generate the autocompletion script for zsh
  fish        Generate the autocompletion script for fish
  powershell  Generate the autocompletion script for powershell

Flags:
  -h, --help   help for completion

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan completion [command] --help" for more information about a command.
```

### github (`trajan github --help`)

```text
Trajan - GitHub

Usage:
  trajan github [command]

Available Commands:
  enumerate   Enumerate GitHub resources and attack surface
  scan        Scan GitHub repositories for CI/CD vulnerabilities
  attack      Execute attacks against GitHub CI/CD vulnerabilities
  retrieve    Retrieve and decrypt secrets from a workflow run
  search      Search for repositories with self-hosted runners

Flags:
  -h, --help         help for github
      --url string   base URL for GitHub Enterprise Server (e.g., https://github.example.com/api/v3)

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan github [command] --help" for more information about a command.
```

### github enumerate (`trajan github enumerate --help`)

```text
Trajan - GitHub - Enumerate

Enumerate and discover GitHub resources accessible to the authenticated token.

The enumerate command provides detailed reconnaissance capabilities including:
  - Token validation and accessible organizations
  - Repository discovery and access mapping
  - Secrets enumeration (Actions secrets and workflow references)

Usage:
  trajan github enumerate [command]

Available Commands:
  token       Validate and analyze GitHub token capabilities
  repos       Discover accessible repositories
  secrets     Enumerate repository and organization secrets

Flags:
  -h, --help   help for enumerate

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for GitHub Enterprise Server (e.g., https://github.example.com/api/v3)
  -v, --verbose              verbose output

Use "trajan github enumerate [command] --help" for more information about a command.
```

### github scan (`trajan github scan --help`)

```text
Trajan - GitHub - Scan

Scan GitHub Actions CI/CD configurations for security vulnerabilities.
Analyzes workflow files across a repository, organization, or user for attack
patterns including pwn requests, artifact poisoning, and secrets exfiltration.

Use --path to scan local workflow files offline (no API access required).

Usage:
  trajan github scan [flags]

Flags:
      --repo string           repository to scan (owner/repo)
      --org string            organization to scan
      --user string           user to scan
      --concurrency int       number of concurrent workers (default 10)
      --severity string       comma-separated severity levels to show (critical, high, medium, low, info)
      --capabilities string   comma-separated detection types to run (e.g., pwn_request,artifact_poisoning)
      --detailed              show detailed evidence for each finding
      --list                  list active detection capabilities and exit
      --path string           filesystem path (file or directory) to scan offline; if set, skips platform API and reads from local files
      --timeout duration      max scan duration in offline mode (when --path is set, e.g. 5m); 0 = 5m default
  -h, --help                  help for scan

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for GitHub Enterprise Server (e.g., https://github.example.com/api/v3)
  -v, --verbose              verbose output
```

### github attack (`trajan github attack --help`)

```text
Trajan - GitHub - Attack

Execute offensive operations against detected GitHub CI/CD vulnerabilities.

SAFETY WARNING: This command executes real attacks that modify resources.
Always use --dry-run first to preview changes.

Available Plugins:
  secrets-dump        Exfiltrate repository secrets via encrypted workflow
  workflow-injection  Inject malicious workflow into repository
  pr-attack           Pull request based attack (pwn request exploitation)
  runner-on-runner    Pivot from self-hosted runner to C2
  interactive-shell   Get interactive shell on self-hosted runner
  c2-setup            Set up C2 infrastructure using GitHub repos
  persistence         Establish persistent access (deploy key, backdoor workflow)

Attack Chains (pre-built sequences):
  ror            Runner-on-Runner: C2 setup, deploy implant, connect shell
  secrets        Secrets Exfiltration: Dump pipeline secrets (no C2 needed)
  persistence    Establish Persistence: C2 setup, deploy persistent backdoor
  full           Full Attack: C2, RoR, shell, secrets dump, persistence
  ai-takeover    AI-powered CI/CD takeover chain
  supply-chain   Supply chain poisoning via artifacts
  toctou-exploit TOCTOU race condition exploitation
  stealth        Stealthy persistence via review bypass

Categories: secrets, cicd, runners, persistence, c2

Usage:
  trajan github attack [flags]
  trajan github attack [command]

Available Commands:
  cleanup     Clean up resources created by attacks

Flags:
      --repo string                 repository to attack (owner/repo)
      --org string                  organization to attack
      --plugin strings              attack plugins to run (comma-separated)
      --category string             attack category filter (secrets, cicd, runners, persistence, c2)
      --all                         run all applicable attacks
      --dry-run                     preview attack without executing
      --confirm                     confirm live execution (required without --dry-run)
      --force                       bypass vulnerability check for attack plugins (force execution)
      --timeout duration            attack timeout (default 5m0s)
      --session string              session ID for tracking/cleanup
      --payload string              custom payload file or inline script
      --branch string               branch name for PR-based attacks
      --c2-repo string              C2 repository for runner-on-runner and interactive-shell (owner/repo)
      --c2-org string               C2 organization for GitHub App installation tokens (creates C2 repo in this org)
      --target-os string            target OS for runner-on-runner (linux|win|macos) (default "linux")
      --target-arch string          target architecture for runner-on-runner (x64|arm64) (default "x64")
      --runner-labels string        runner labels for runner-on-runner (comma-separated) (default "self-hosted")
      --persistence-method string   persistence method (deploy_key|malicious_workflow|scheduled_backdoor) (default "malicious_workflow")
      --chain string                execute named attack chain (ror, secrets, persistence, full)
      --chain-plugins strings       execute custom chain with specified plugins in order
      --chain-list                  list available attack chains
      --chain-deps                  show dependency graph for specified chain
  -h, --help                        help for attack

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for GitHub Enterprise Server (e.g., https://github.example.com/api/v3)
  -v, --verbose              verbose output

Use "trajan github attack [command] --help" for more information about a command.
```

### github retrieve (`trajan github retrieve --help`)

```text
Trajan - GitHub - Retrieve

Download and decrypt artifacts from a secrets-dump workflow run.

After running 'trajan github attack --plugin secrets-dump', use this command
to retrieve the exfiltrated secrets once the workflow completes.

Usage:
  trajan github retrieve [flags]

Flags:
      --run-id int      workflow run ID to retrieve artifacts from
      --repo string     repository (owner/repo) - auto-detected from session if not specified
      --wait duration   max time to wait for workflow completion (default 5m0s)
  -h, --help            help for retrieve

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for GitHub Enterprise Server (e.g., https://github.example.com/api/v3)
  -v, --verbose              verbose output
```

### github search (`trajan github search --help`)

```text
Trajan - GitHub - Search

Search for repositories potentially using self-hosted runners.

This command searches GitHub code search or SourceGraph for workflow files
that reference self-hosted runners, helping identify targets with
non-ephemeral CI/CD infrastructure.

Supported Providers:
  github       Search via GitHub code search API (requires token)
  sourcegraph  Search via SourceGraph public API (no auth required)

Usage:
  trajan github search [flags]

Flags:
  -p, --provider string      Search provider (github, sourcegraph) (default "github")
      --org string           Organization to search within
  -q, --query string         Custom search query
      --output-file string   Output file for results
  -h, --help                 help for search

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for GitHub Enterprise Server (e.g., https://github.example.com/api/v3)
  -v, --verbose              verbose output
```

### gitlab (`trajan gitlab --help`)

```text
Trajan - GitLab CI

Usage:
  trajan gitlab [command]

Available Commands:
  enumerate   Enumerate GitLab resources and attack surface
  scan        Scan GitLab repositories for CI/CD vulnerabilities
  attack      Execute attacks against GitLab CI/CD vulnerabilities

Flags:
  -h, --help         help for gitlab
      --url string   base URL for self-hosted GitLab (e.g., https://gitlab.example.com)

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan gitlab [command] --help" for more information about a command.
```

### gitlab enumerate (`trajan gitlab enumerate --help`)

```text
Trajan - GitLab CI - Enumerate

Capabilities:
  * Token validation and scope analysis
  * Project discovery and access mapping
  * Group hierarchy and shared access
  * CI/CD variable (secrets) enumeration
  * Runner enumeration and workflow tag analysis
  * Branch protection rule analysis

Authentication:
  Tokens can be provided via --token flag or environment variables:
    GITLAB_TOKEN, GL_TOKEN

Usage:
  trajan gitlab enumerate [command]

Available Commands:
  token              Validate and analyze GitLab token capabilities
  projects           Discover accessible projects
  groups             Discover accessible groups and organizational structure
  secrets            Enumerate CI/CD variables (secrets)
  branch-protections Enumerate branch protection rules
  runners            Enumerate GitLab runners and analyze workflow tag coverage

Flags:
  -h, --help   help for enumerate

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for self-hosted GitLab (e.g., https://gitlab.example.com)
  -v, --verbose              verbose output

Use "trajan gitlab enumerate [command] --help" for more information about a command.
```

### gitlab scan (`trajan gitlab scan --help`)

```text
Trajan - GitLab CI - Scan

Targets:
  --project   Scan a single project (group/project)
  --group     Scan all projects in a group
  --user      Scan all projects for a user

Authentication:
  Tokens can be provided via --token flag or environment variables:
    GITLAB_TOKEN, GL_TOKEN

Use --path to scan local workflow files offline (no API access required).

Usage:
  trajan gitlab scan [flags]

Flags:
      --project string        project to scan (group/project)
      --group string          group to scan
      --user string           user to scan (all user's projects)
      --concurrency int       number of concurrent workers (default 10)
      --severity string       comma-separated severity levels to show (critical, high, medium, low, info)
      --capabilities string   comma-separated detection types to run (e.g., script_injection,token_exposure)
      --detailed              show detailed evidence for each finding
      --list                  list active detection capabilities and exit
      --path string           filesystem path (file or directory) to scan offline; if set, skips platform API and reads from local files
      --timeout duration      max scan duration in offline mode (when --path is set, e.g. 5m); 0 = 5m default
  -h, --help                  help for scan

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for self-hosted GitLab (e.g., https://gitlab.example.com)
  -v, --verbose              verbose output
```

### gitlab attack (`trajan gitlab attack --help`)

```text
Trajan - GitLab CI - Attack

SAFETY WARNING: This command executes real attacks that modify resources.
Always use --dry-run first to preview changes.

Available Plugins:
  secrets-dump        Exfiltrate CI/CD secrets via PPE (Poisoned Pipeline Execution)
  runner-exec         Execute commands on self-hosted runners

Usage:
  trajan gitlab attack [flags]

Flags:
      --list                 list available attack plugins
      --project string       project to attack (namespace/project)
      --plugin strings       attack plugins to run
      --dry-run              preview attack without executing
      --confirm              confirm live execution (required without --dry-run)
      --timeout duration     timeout for pipeline execution (default 5m0s)
      --output-file string   save command output to file
      --runner-tags string   comma-separated runner tags for runner-exec
      --command string       command to execute for runner-exec
      --no-cleanup           preserve artifacts after attack (branch, pipeline, logs)
  -h, --help                 help for attack

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           base URL for self-hosted GitLab (e.g., https://gitlab.example.com)
  -v, --verbose              verbose output
```

### ado (`trajan ado --help`)

```text
Trajan - Azure DevOps

Usage:
  trajan ado [command]

Available Commands:
  enumerate   Enumerate token permissions and accessible resources
  scan        Scan Azure DevOps repositories for CI/CD vulnerabilities
  attack      Execute attacks against Azure DevOps CI/CD vulnerabilities
  retrieve    Retrieve and decrypt secrets from an ADO pipeline run

Flags:
      --azure-bearer-token string   Azure Entra ID bearer token (or set AZURE_BEARER_TOKEN)
  -h, --help                        help for ado

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan ado [command] --help" for more information about a command.
```

### ado enumerate (`trajan ado enumerate --help`)

```text
Trajan - Azure DevOps - Enumerate

Enumerate the permissions and accessible resources for an API token.

This command supports subcommands for different enumeration operations:
  - token: Validate PAT and enumerate accessible resources
  - projects, repos, pipelines, users, groups, etc.: List accessible resources
  - search: Search code and credentials

Usage:
  trajan ado enumerate [command]

Available Commands:
  token           Validate PAT and enumerate accessible resources
  projects        List all accessible projects
  repos           List repositories
  pipelines       List pipelines in a project
  variable-groups List variable groups in a project
  connections     List service connections in a project
  secure-files    List secure files in a project
  agent-pools     List agent pools
  users           List users in the organization
  groups          List groups in the organization
  branch-policies List branch policies
  search          Search code, logs, files, and credentials
  fork-security   Detect pipelines with insecure fork build configurations
  attack-paths    Analyze permissions, triggers, and policies to identify attack paths

Flags:
      --azure-bearer-token string   Azure Entra ID bearer token (or set AZURE_BEARER_TOKEN)
  -h, --help                        help for enumerate
      --org string                  Organization name (required for azuredevops)
  -o, --output string               Output format (console, json, csv) (default "console")
      --platform string             Platform to enumerate (azuredevops, github, gitlab) (default "azuredevops")
      --project string              Project name/ID (optional, for scoping to single project)
      --token string                API token (or use env var: AZURE_DEVOPS_PAT, GH_TOKEN, GL_TOKEN)
      --url string                  Custom instance URL (for self-hosted GitLab, etc.)

Global Flags:
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
  -v, --verbose              verbose output

Use "trajan ado enumerate [command] --help" for more information about a command.
```

### ado scan (`trajan ado scan --help`)

```text
Trajan - Azure DevOps - Scan

Scan Azure DevOps Pipelines CI/CD configurations for security vulnerabilities.

Authentication:
  Tokens can be provided via --token flag or environment variables:
    AZURE_DEVOPS_PAT, AZDO_PAT

Targets:
  --org     Azure DevOps organization name or URL
  --repo    Specific repository (project/repo)

Use --path to scan local workflow files offline (no API access required).

Usage:
  trajan ado scan [flags]

Flags:
      --repo string           repository to scan (project/repo)
      --org string            Azure DevOps organization name or URL (e.g., myorg or https://dev.azure.com/myorg)
      --concurrency int       number of concurrent operations (default 10)
      --severity string       comma-separated severity levels to show (critical, high, medium, low, info)
      --capabilities string   comma-separated detection types to run (e.g., pipeline-injection,secrets-exposure)
      --detailed              show detailed evidence for each finding
      --list                  list active detection capabilities and exit
      --path string           filesystem path (file or directory) to scan offline; if set, skips platform API and reads from local files
      --timeout duration      max scan duration in offline mode (when --path is set, e.g. 5m); 0 = 5m default
  -h, --help                  help for scan

Global Flags:
      --azure-bearer-token string   Azure Entra ID bearer token (or set AZURE_BEARER_TOKEN)
  -o, --output string               output format (console, json, sarif, html) (default "console")
      --proxy string                HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string          SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string                API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose                     verbose output
```

### ado attack (`trajan ado attack --help`)

```text
Trajan - Azure DevOps - Attack

Execute offensive operations against detected Azure DevOps CI/CD vulnerabilities.

SAFETY WARNING: This command executes real attacks that modify resources.
Always use --dry-run first to preview changes.

Available Plugins:
  ado-secrets-dump        Dump all secrets (env vars + variable groups), or target a specific group with --group
  ado-pipeline-injection  Inject into pipelines via poisoned pipeline execution (PPE)
  ado-pr-attack           PR-based pipeline execution attack
  ado-extract-connections Extract service connection credentials
  ado-extract-securefiles Download secure files
  ado-privesc             Privilege escalation in Azure DevOps
  ado-persistence         Establish persistent access via PAT or SSH key creation
                          NOTE: Requires --azure-bearer-token (Entra ID). PATs cannot
                          create other PATs or SSH keys — Azure DevOps rejects these
                          requests with 401 when authenticated via PAT.
  ado-agent-exec          Execute commands on self-hosted agents
  ado-ai-probe            Probe AI/ML service endpoints for token exfiltration

Categories: secrets, cicd, runners, persistence, c2

Usage:
  trajan ado attack [flags]
  trajan ado attack [command]

Available Commands:
  cleanup     Clean up resources created by attacks

Flags:
      --repo string              repository to attack (project/repo)
      --org string               Azure DevOps organization name or URL
      --plugin strings           attack plugins to run (comma-separated)
      --category string          attack category filter (secrets, cicd, runners, persistence, c2)
      --all                      run all applicable attacks
      --dry-run                  preview attack without executing
      --confirm                  confirm live execution (required without --dry-run)
      --force                    bypass vulnerability check for attack plugins (force execution)
      --timeout duration         attack timeout (default 5m0s)
      --session string           session ID for tracking/cleanup
      --group string             variable group name (for ado-secrets-dump, targets specific group)
      --connection string        service connection name (for ado-extract-connections)
      --connection-type string   service connection type: azure, github, aws, kubernetes, docker, ssh, sonarqube (for ado-extract-connections)
      --secure-file string       secure file name (for ado-extract-securefiles)
      --user-descriptor string   user descriptor to escalate (for ado-privesc)
      --pool string              self-hosted agent pool name (for ado-agent-exec)
      --command string           command to execute on self-hosted agent (for ado-agent-exec)
      --method string            persistence method: pat or ssh (for ado-persistence, default: pat)
      --public-key string        path to SSH public key file (for ado-persistence --method ssh)
      --output-file string       write extracted secrets/output to file
  -h, --help                     help for attack

Global Flags:
      --azure-bearer-token string   Azure Entra ID bearer token (or set AZURE_BEARER_TOKEN)
  -o, --output string               output format (console, json, sarif, html) (default "console")
      --proxy string                HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string          SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string                API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose                     verbose output

Use "trajan ado attack [command] --help" for more information about a command.
```

### bitbucket (`trajan bitbucket --help`)

```text
Trajan - Bitbucket

Usage:
  trajan bitbucket [command]

Available Commands:
  enumerate   Enumerate Bitbucket resources and attack surface

Flags:
      --email string       email address for API token auth (or set BITBUCKET_EMAIL/BB_EMAIL)
  -h, --help               help for bitbucket
      --workspace string   Bitbucket workspace slug (or set BITBUCKET_WORKSPACE)

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan bitbucket [command] --help" for more information about a command.
```

### bitbucket enumerate (`trajan bitbucket enumerate --help`)

```text
Trajan - Bitbucket - Enumerate

Enumerate and discover Bitbucket resources accessible to the authenticated token.

The enumerate command provides detailed reconnaissance capabilities including:
  - Token validation and scope analysis
  - User identity and account status

Usage:
  trajan bitbucket enumerate [command]

Available Commands:
  token       Validate and analyze Bitbucket token capabilities

Flags:
  -h, --help   help for enumerate

Global Flags:
      --email string         email address for API token auth (or set BITBUCKET_EMAIL/BB_EMAIL)
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output
      --workspace string     Bitbucket workspace slug (or set BITBUCKET_WORKSPACE)

Use "trajan bitbucket enumerate [command] --help" for more information about a command.
```

### bitbucket scan capture (`trajan bitbucket scan --help`)

Capture returned parent Bitbucket help — **no `scan` subcommand** in 1.0.2.

```text
Trajan - Bitbucket

Usage:
  trajan bitbucket [command]

Available Commands:
  enumerate   Enumerate Bitbucket resources and attack surface

Flags:
      --email string       email address for API token auth (or set BITBUCKET_EMAIL/BB_EMAIL)
  -h, --help               help for bitbucket
      --workspace string   Bitbucket workspace slug (or set BITBUCKET_WORKSPACE)

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan bitbucket [command] --help" for more information about a command.
```

### jenkins (`trajan jenkins --help`)

```text
Trajan - Jenkins

Usage:
  trajan jenkins [command]

Available Commands:
  enumerate   Enumerate Jenkins resources and attack surface
  scan        Scan Jenkins pipelines for security vulnerabilities
  attack      Execute attacks against Jenkins vulnerabilities

Flags:
  -h, --help              help for jenkins
      --password string   Jenkins password or API token for Basic auth (env: JENKINS_PASSWORD)
      --username string   Jenkins username for Basic auth (env: JENKINS_USERNAME)

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan jenkins [command] --help" for more information about a command.
```

### jenkins enumerate (`trajan jenkins enumerate --help`)

```text
Trajan - Jenkins - Enumerate

Enumerate and discover Jenkins resources accessible with the current credentials.

Subcommands:
  access   - Probe access level, user identity, and server info
  jobs     - List all accessible jobs and folders
  nodes    - List build agents/nodes
  plugins  - List installed plugins and versions

Usage:
  trajan jenkins enumerate [command]

Available Commands:
  access      Probe access level and server info
  jobs        List all accessible jobs and folders
  nodes       List build agents/nodes
  plugins     List installed plugins and versions

Flags:
  -h, --help   help for enumerate

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --password string      Jenkins password or API token for Basic auth (env: JENKINS_PASSWORD)
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --username string      Jenkins username for Basic auth (env: JENKINS_USERNAME)
  -v, --verbose              verbose output

Use "trajan jenkins enumerate [command] --help" for more information about a command.
```

### jenkins scan (`trajan jenkins scan --help`)

```text
Trajan - Jenkins - Scan

Scan Jenkins pipeline definitions for security vulnerabilities.
Checks for script injection, hardcoded credentials, excessive permissions,
insecure agent configurations, and CSRF/anonymous access issues.
Scans a single job (--repo) or all jobs in an instance (default).

Use --path to scan local workflow files offline (no API access required).
Note: live instance checks (anonymous access, CSRF, script console) are
skipped in offline mode as they require a running Jenkins instance.

Usage:
  trajan jenkins scan [flags]

Flags:
      --repo string        Jenkins job to scan
      --org string         Jenkins folder/organization to scan
      --concurrency int    number of concurrent workers (default 10)
      --url string         Jenkins instance URL (e.g., https://jenkins.example.com)
      --path string        filesystem path (file or directory) to scan offline; if set, skips platform API and reads from local files
      --timeout duration   max scan duration in offline mode (when --path is set, e.g. 5m); 0 = 5m default
      --detailed           show detailed evidence for each finding
  -h, --help               help for scan

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --password string      Jenkins password or API token for Basic auth (env: JENKINS_PASSWORD)
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --username string      Jenkins username for Basic auth (env: JENKINS_USERNAME)
  -v, --verbose              verbose output
```

### jfrog (`trajan jfrog --help`)

```text
Trajan - JFrog

Usage:
  trajan jfrog [command]

Available Commands:
  scan        Scan JFrog Artifactory for secrets and token information

Flags:
  -h, --help         help for jfrog
      --url string   JFrog instance URL (e.g., https://acme.jfrog.io)

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan jfrog [command] --help" for more information about a command.
```

### jfrog scan (`trajan jfrog scan --help`)

```text
Trajan - JFrog - Scan

Scan JFrog Artifactory instances for secrets and enumerate token capabilities.

JFrog does not support vulnerability scanning of CI/CD pipelines.
Available operations:
  --secrets     Enumerate secrets from artifacts, builds, remote repos, and ML
  --token-info  Display token capabilities and accessible resources

Authentication:
  Tokens can be provided via --token flag or environment variable:
    JFROG_TOKEN
  Or use username/password with -u and -p flags.

Usage:
  trajan jfrog scan [flags]

Flags:
      --secrets           enumerate secrets from artifacts, builds, remote repos, and ML
      --token-info        display token capabilities and accessible resources
  -u, --username string   username for basic auth
  -p, --password string   password for basic auth
  -h, --help              help for scan

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
      --url string           JFrog instance URL (e.g., https://acme.jfrog.io)
  -v, --verbose              verbose output
```

### jfrog enumerate capture (`trajan jfrog enumerate --help`)

Capture returned parent JFrog help — **no `enumerate` subcommand** in 1.0.2 (use `jfrog scan --token-info` / `--secrets`).

```text
Trajan - JFrog

Usage:
  trajan jfrog [command]

Available Commands:
  scan        Scan JFrog Artifactory for secrets and token information

Flags:
  -h, --help         help for jfrog
      --url string   JFrog instance URL (e.g., https://acme.jfrog.io)

Global Flags:
  -o, --output string        output format (console, json, sarif, html) (default "console")
      --proxy string         HTTP proxy URL (e.g., http://proxy:8080)
      --socks-proxy string   SOCKS5 proxy URL (e.g., socks5://proxy:1080)
      --token string         API token (or set GH_TOKEN/GITHUB_TOKEN env var)
  -v, --verbose              verbose output

Use "trajan jfrog [command] --help" for more information about a command.
```

---

## Synopsis (from Captured help)

```text
trajan [command]
trajan <platform> [command] [flags]
```

**Platforms:** `github`, `gitlab`, `ado`, `bitbucket`, `jenkins`, `jfrog`.

**Global flags:** `-o/--output` (`console`|`json`|`sarif`|`html`), `--proxy`, `--socks-proxy`, `--token`, `-v/--verbose`, `-h/--help`.

**SpiderFeet default:** `-o json`.

## Offensive commands (authorized ROE only)

- `github attack` / `gitlab attack` / `ado attack` / `jenkins attack` — help warns these execute real attacks; use `--dry-run` first, then `--confirm` for live runs.
- `github retrieve` / `ado retrieve` — decrypt/exfiltrate artifacts from prior attack runs; redact all outputs.
- Do **not** use attack/retrieve as default corpus harvest scenarios.

## Re-capture

```powershell
$exe = "C:\projects\spiderfeet\.tools\trajan\trajan.exe"
$out = "C:\projects\spiderfeet\.tmp_trajan_help"
New-Item -ItemType Directory -Force -Path $out | Out-Null
& $exe version | Out-File -Encoding utf8 "$out\version.txt"
& $exe --help | Out-File -Encoding utf8 "$out\root_help.txt"
# Repeat for each platform and nested command --help
```

## Related

- Skill: `.cursor/skills/trajan/SKILL.md`
- Zero to Hero: `Trajan-Zero-to-Hero.md`
