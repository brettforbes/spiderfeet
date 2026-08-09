# Titus CLI Options

Operator reference for `titus` **v1.2.7**. Prefer structured JSON for SpiderFeet corpus and automation.

## SpiderFeet preferred commands

```bash
# Scan into an engagement datastore with JSON (default path if omitted: titus.ds)
titus scan <target> --format json --output ./engagement.ds

# Primary structured export for graphs / harvest
titus report --datastore ./engagement.ds --format json

# Per-rule counts
titus report summary --datastore ./engagement.ds --format json
```

| Field | Value |
|-------|-------|
| Version | **v1.2.7** (Go port of NoseyParker) |
| Windows binary | `C:\projects\spiderfeet\.tools\Titus\titus-windows-amd64.exe` |
| Linux binary | `C:\projects\spiderfeet\.tools\Titus\titus-linux-amd64` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_titus_help/*.txt` |

> Titus succeeds [Nosey Parker](https://github.com/praetorian-inc/noseyparker) for greenfield secret scanning. Flags below are from live `--help` on v1.2.7 only — do not invent options.

---

## Captured help

Live help text captured from `.tools/Titus/titus-windows-amd64.exe` on **2026-08-10**. Each block is the full stdout of the listed command (global options repeated by the CLI are retained).

### Root (`titus --help`)

```text
Titus is a fast secrets scanner that finds credentials in code, files, and git history.
It uses regex-based detection rules to identify sensitive data like API keys, passwords, and tokens.

Usage:
  titus [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  enum        Enumerate remote services for secrets
  explore     Interactively explore scan results
  help        Help about any command
  report      Generate a report from scan results
  rules       Manage detection rules
  scan        Scan a target for secrets
  serve       Run as streaming server for Burp extension integration
  version     Show version information

Flags:
  -h, --help      help for titus
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output

Use "titus [command] --help" for more information about a command.
```

### `version` (`titus version`)

```text

  ______ ____ ______ __  __ _____
 /_  __//  _//_  __// / / // ___/
  / /   / /   / /  / / / / \__ \
 / /  _/ /   / /  / /_/ / ___/ /
/_/  /___/  /_/   \____/ /____/
 There's always something.
 Praetorian Security, Inc.

Titus v1.2.7 (Go port of NoseyParker)
```

### `scan` (`titus scan --help`)

```text
Scan a file, directory, git repository, Docker image, or remote GitHub/GitLab repository for secrets using detection rules.
Supports github.com/org/repo and gitlab.com/namespace/project URLs for direct remote scanning.
Use --docker for image references or prefix the target with docker://.

Usage:
  titus scan <target> [flags]

Flags:
      --accessibility string            code accessibility: "public" (no penalty), "private" (-25 to all scores),
                                        or "auto" (detect via git remote/GitHub API, defaults to private if undetermined) (default "auto")
      --asana-attachment-max-size int   Maximum Asana attachment size in bytes to download (default 52428800)
      --asana-concurrency int           Number of workers processing tasks within a project (0 = use default of 5)
      --asana-include-attachments       Download and scan Asana-hosted file attachments
      --asana-rate-limit float          Asana API requests per second (free tier ≈ 2.5/sec; paid tier ≈ 25/sec) (default 10)
      --context-lines int               Lines of context before/after matches (0 to disable) (default 3)
      --docker                          Treat target as Docker image (uses docker image save)
      --extract extensions              Extract text from binary files (extensions: xlsx,docx,pdf,zip or 'all')
      --extract-max-depth int           Max nested archive depth (default 5)
      --extract-max-size string         Max uncompressed size per extracted file (default "10MB")
      --extract-max-total string        Max total bytes to extract from one archive (default "100MB")
      --format string                   Output format: json, sarif, human (default "human")
      --gdrive-concurrency int          Google Drive parallel file workers (default 5; 0 = use default; clamped to [1, 100])
      --gdrive-rate-limit float         Google Drive API requests per second (default 16; 0 = use default). Per-user cap is ~325k quota units/min
      --git                             Treat target as git repository (enumerate git history)
  -h, --help                            help for scan
      --ignore string                   Path to gitignore-style ignore file (replaces built-in defaults; use /dev/null to disable)
      --include-noisy                   Enable rules marked noisy: true (off by default; high false-positive rate)
      --incremental                     Skip already-scanned blobs
      --max-file-size int               Maximum file size to scan (bytes) (default 10485760)
      --output string                   Output datastore path (:memory: for in-memory, :auto: to derive from target name) (default "titus.ds")
      --readers int                     Number of parallel file readers (0 = NumCPU)
      --rules string                    Path to custom rules file or directory
      --rules-exclude string            Exclude rules matching regex pattern (comma-separated)
      --rules-include string            Include rules matching regex pattern (comma-separated)
      --ruleset string                  Ruleset to use: default, np.assets, np.hashes, all (all = no filtering) (default "default")
      --score-budget duration           per-finding overall scoring budget across all modifiers (default 60s; 0 = unlimited) (default 1m0s)
      --score-scope                     enable HTTP dynamic scoring modifiers (calls external APIs to determine secret scope/permissions)
      --score-timeout duration          per-modifier HTTP timeout for dynamic scoring (default 10s) (default 10s)
      --sqlite-row-limit int            Max rows per table for SQLite extraction (0 for unlimited) (default 1000)
      --store-blobs                     Store file contents in blobs/ directory
      --validate                        validate detected secrets against their source APIs
      --validate-workers int            number of concurrent validation workers (default 4)
      --workers int                     Number of parallel scan workers (default 8)

Global Flags:
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output
```

### `report` (`titus report --help`)

```text
Read findings from a datastore and output a summary report

Usage:
  titus report [flags]
  titus report [command]

Available Commands:
  summary     Show a summary of findings by rule type

Flags:
      --color string[="always"]   Color output: auto, always, never (default "auto")
      --datastore string          Path to datastore directory or file (default "titus.ds")
      --format string             Output format: human, json, sarif (default "human")
  -h, --help                      help for report
      --show-rejected             Include findings marked as rejected via the explore command (hidden by default)

Global Flags:
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output

Use "titus report [command] --help" for more information about a command.
```

### `report summary` (`titus report summary --help`)

```text
Display total counts and per-rule breakdown of findings and matches

Usage:
  titus report summary [flags]

Flags:
      --format string   Output format: human, json (default "human")
  -h, --help            help for summary

Global Flags:
      --color string[="always"]   Color output: auto, always, never (default "auto")
      --datastore string          Path to datastore directory or file (default "titus.ds")
  -q, --quiet                     Quiet mode (errors only)
      --show-rejected             Include findings marked as rejected via the explore command (hidden by default)
  -v, --verbose                   Verbose output
```

### `enum` (`titus enum --help`)

```text
Enumerate remote services (GitHub, GitLab, Slack, Notion, Linear, Confluence, Jira, Microsoft 365)
for secrets using detection rules.

Usage:
  titus enum [command]

Available Commands:
  confluence  Scan a Confluence instance for secrets
  github      Scan GitHub repositories for secrets
  gitlab      Scan GitLab projects
  jira        Scan a Jira instance for secrets
  linear      Scan a Linear workspace for secrets
  microsoft   Scan Microsoft 365 services for secrets
  notion      Scan a Notion workspace for secrets
  slack       Scan a Slack workspace for secrets

Flags:
      --format string          Output format: json, human (default "human")
  -h, --help                   help for enum
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")

Global Flags:
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output

Use "titus enum [command] --help" for more information about a command.
```

### `enum github` (`titus enum github --help`)

```text
Scan GitHub repositories by cloning and scanning locally.
Supports github.com and GitHub Enterprise Server instances.

Authentication:
  No token needed for public repositories (60 requests/hour).
  Use --token or GITHUB_TOKEN env var for private repos and higher rate limits (5000/hour).

GitHub Enterprise:
  Use --url or GITHUB_BASE_URL env var to point at a GHE Server instance.
  Example: --url https://github.example.com

Rate limiting:
  Use --rate-limit to add a delay between repository clones (recommended for large, self-hosted orgs).
  Example: --rate-limit 2 adds a 2-second delay between each repo.

Stealth scanning:
  Use --jitter to add random delays between repository clones.
  Combined with --rate-limit, it creates a random delay between the
  rate-limit (minimum) and jitter (maximum) values.
  Example: --rate-limit 300 --jitter 1200 = random 5-20 minute delays.

Examples:
  titus enum github praetorian-inc/titus                          # single public repo
  titus enum github --token ghp_xxx --org praetorian-inc          # all repos in org
  titus enum github --url https://ghe.corp.com --token ghp_xxx --org myorg --rate-limit 2
  titus enum github --token ghp_xxx --user octocat --git          # user repos with full history
  titus enum github --token ghp_xxx --org myorg --jitter 1200             # 0-20min random delay between clones
  titus enum github --token ghp_xxx --org myorg --rate-limit 300 --jitter 1200  # 5-20min random delay (stealth)

Usage:
  titus enum github [owner/repo] [flags]
  titus enum github [command]

Available Commands:
  scan        Scan GitHub repository or organization

Flags:
      --git                Scan full git history (slower; default scans only current files)
  -h, --help               help for github
      --jitter float       Maximum random delay in seconds between repository clones (e.g., 1200 for 20min; combined with --rate-limit as minimum)
      --no-clone           Fetch files via API instead of cloning (requires token, no git history)
      --org string         Scan all repositories in organization
      --rate-limit float   Delay in seconds between repository clones (e.g., 2 or 0.5; 0 = no delay)
      --skip-forks         Skip forked repositories when scanning orgs or users
      --token string       GitHub API token (or GITHUB_TOKEN env; optional for public repos)
      --url string         GitHub Enterprise base URL (or GITHUB_BASE_URL env; e.g., https://github.example.com)
      --user string        Scan all repositories for user
  -y, --yes                Skip confirmation prompt for scan time estimate

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output

Use "titus enum github [command] --help" for more information about a command.
```

### `enum gitlab` (`titus enum gitlab --help`)

```text
Scan GitLab projects by cloning and scanning locally.
No API token needed for public projects.
Use --token or GITLAB_TOKEN for private projects and higher rate limits.
Use --git to scan full git history (slower but finds deleted secrets).

Stealth scanning:
  Use --jitter to add random delays between project clones.
  Combined with --rate-limit, it creates a random delay between the
  rate-limit (minimum) and jitter (maximum) values.
  Example: --rate-limit 300 --jitter 1200 = random 5-20 minute delays.

Usage:
  titus enum gitlab [namespace/project] [flags]
  titus enum gitlab [command]

Available Commands:
  scan        Scan GitLab project or group

Flags:
      --git                Scan full git history (slower; default scans only current files)
      --group string       Scan all projects in group
  -h, --help               help for gitlab
      --jitter float       Maximum random delay in seconds between project clones (e.g., 1200 for 20min; combined with --rate-limit as minimum)
      --no-clone           Fetch files via API instead of cloning (requires token, no git history)
      --rate-limit float   Delay in seconds between project clones (e.g., 2 or 0.5; 0 = no delay)
      --token string       GitLab token (or GITLAB_TOKEN env; optional for public projects)
      --url string         GitLab base URL (default: gitlab.com)
      --user string        Scan all projects for user
  -y, --yes                Skip confirmation prompt for scan time estimate

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output

Use "titus enum gitlab [command] --help" for more information about a command.
```

### `enum slack` (`titus enum slack --help`)

```text
Scan an entire Slack workspace for secrets via the Slack Web API.
Enumerates channels, messages, and thread replies.

Authentication:
  Use --token or SLACK_TOKEN env var with a Slack token.
  Supported token types: xoxb- (bot), xoxp- (user), xoxc- (browser session).
  Browser session tokens (xoxc-) also require --cookie with the xoxd- session cookie.
  To get xoxc/xoxd: open Slack in browser → DevTools → Application →
    token: Local Storage → search for xoxc-
    cookie: Cookies → cookie named "d" (starts with xoxd-)

Examples:
  titus enum slack --token xoxb-xxx
  SLACK_TOKEN=xoxb-xxx titus enum slack
  titus enum slack --token xoxb-xxx --channels general,engineering
  titus enum slack --token xoxb-xxx --output slack-scan.db --format json
  titus enum slack --token xoxc-xxx --cookie xoxd-xxx -v          # browser session token

Usage:
  titus enum slack [flags]

Flags:
      --channels string    Comma-separated channel names to scan (default: all)
      --cookie string      Slack session cookie (xoxd-...) — required for xoxc- tokens (or SLACK_COOKIE env)
  -h, --help               help for slack
      --rate-limit float   API requests per second (default 0.75, Slack Tier 3 = 50 req/min) (default 0.75)
      --token string       Slack API token (or SLACK_TOKEN env)

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output
```

### `enum notion` (`titus enum notion --help`)

```text
Scan an entire Notion workspace for secrets using the internal API.
Requires a token_v2 session cookie from an authenticated Notion session.

Authentication:
  Use --token or NOTION_TOKEN env var with a token_v2 session cookie.
  To obtain the token: open Notion in a browser, open DevTools, find the
  token_v2 cookie under Application > Cookies > www.notion.so.

Examples:
  titus enum notion --token <token_v2>
  titus enum notion --token <token_v2> --concurrency 20
  NOTION_TOKEN=<token_v2> titus enum notion --output notion-scan.db
  titus enum notion --token <token_v2> --page https://app.notion.com/p/Page-Title-abc123def456
  titus enum notion --token <token_v2> --page 37da484a-7dc4-80dd-936b-d247d86f7ef7
  titus enum notion --token <token_v2> --teamspace Engineering
  titus enum notion --token <token_v2> --workspace Praetorian --teamspace "Sales & Marketing"

Usage:
  titus enum notion [flags]

Flags:
      --concurrency int    Number of parallel page fetchers (default 10)
  -h, --help               help for notion
      --page string        Scan a single page (URL or page ID)
      --teamspace string   Scan only pages in this teamspace (name or ID)
      --token string       Notion token_v2 session cookie (or NOTION_TOKEN env)
      --workspace string   Workspace name or ID (for multi-workspace accounts)

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output
```

### `enum linear` (`titus enum linear --help`)

```text
Scan an entire Linear workspace for secrets via the GraphQL API.
Enumerates issues (with comments), documents, and project updates.

Authentication:
  Use --token or LINEAR_TOKEN env var with a Linear API key.
  Create one at: https://linear.app/settings/api

Examples:
  titus enum linear --token lin_api_xxx
  LINEAR_TOKEN=lin_api_xxx titus enum linear
  titus enum linear --token lin_api_xxx --output linear-scan.db --format json

Usage:
  titus enum linear [flags]

Flags:
  -h, --help           help for linear
      --token string   Linear API key (or LINEAR_TOKEN env)

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output
```

### `enum confluence` (`titus enum confluence --help`)

```text
Scan an entire Confluence instance for secrets via the REST API.
Enumerates pages, blog posts, and comments across all spaces.

Authentication:
  For Confluence Cloud: use --username and --token with an API token.
  For Confluence Server/Data Center: use --token with a PAT (Personal Access Token).
  Create a Cloud API token at: https://id.atlassian.com/manage-profile/security/api-tokens

Examples:
  titus enum confluence --base-url https://mysite.atlassian.net/wiki --username user@example.com --token ATATT...
  CONFLUENCE_BASE_URL=https://mysite.atlassian.net/wiki CONFLUENCE_USERNAME=user@example.com CONFLUENCE_TOKEN=ATATT... titus enum confluence
  titus enum confluence --base-url https://confluence.internal --token PAT_TOKEN --spaces DEV,OPS

Usage:
  titus enum confluence [flags]

Flags:
      --base-url string    Confluence base URL (or CONFLUENCE_BASE_URL env)
  -h, --help               help for confluence
      --rate-limit float   Requests per second (default 5)
      --spaces string      Comma-separated space keys to scan (empty = all)
      --token string       Confluence API token or PAT (or CONFLUENCE_TOKEN env)
      --username string    Confluence username for Cloud basic auth (or CONFLUENCE_USERNAME env)

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output
```

### `enum jira` (`titus enum jira --help`)

```text
Scan an entire Jira instance for secrets via the REST API.
Enumerates issue descriptions and comments across all projects.
Supports both Jira Cloud (API v3) and Jira Server/Data Center (API v2),
with automatic version detection.

Authentication:
  For Jira Cloud: use --username and --token with an API token.
  For Jira Server/Data Center: use --token with a PAT (Personal Access Token).
  Create a Cloud API token at: https://id.atlassian.com/manage-profile/security/api-tokens

Examples:
  titus enum jira --base-url https://mysite.atlassian.net --username user@example.com --token ATATT...
  JIRA_BASE_URL=https://mysite.atlassian.net JIRA_USERNAME=user@example.com JIRA_TOKEN=ATATT... titus enum jira
  titus enum jira --base-url https://jira.internal --token PAT_TOKEN --projects DEV,OPS
  titus enum jira --base-url http://jira.local:8080 --token PAT --allow-insecure

Usage:
  titus enum jira [flags]

Flags:
      --allow-insecure     Allow plaintext HTTP base URLs (for internal instances)
      --base-url string    Jira base URL (or JIRA_BASE_URL env)
  -h, --help               help for jira
      --projects string    Comma-separated project keys to scan (empty = all)
      --rate-limit float   Requests per second (default 5)
      --token string       Jira API token or PAT (or JIRA_TOKEN env)
      --username string    Jira username for Cloud basic auth (or JIRA_USERNAME env)

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output
```

### `enum microsoft` (`titus enum microsoft --help`)

```text
Scan Microsoft 365 services (SharePoint, OneDrive, Teams) for secrets
via the Microsoft Graph API.

Usage:
  titus enum microsoft [command]

Available Commands:
  sharepoint  Scan SharePoint sites for secrets

Flags:
      --client-id string       Azure AD application (client) ID for device code auth (default "1950a258-227b-4e31-a9cf-717495945fc2")
  -h, --help                   help for microsoft
      --refresh-token string   Microsoft refresh token (or SHAREPOINT_REFRESH_TOKEN env)
      --tenant-id string       Azure AD tenant ID (or 'organizations') (default "organizations")
      --token string           Graph API OAuth bearer token (or SHAREPOINT_TOKEN env)

Global Flags:
      --format string          Output format: json, human (default "human")
      --include-noisy          Include noisy rules that may produce more false positives
      --output string          Output database path (:memory: for in-memory, :auto: to derive from target name) (default "titus.db")
  -q, --quiet                  Quiet mode (errors only)
      --rules string           Path to custom rules file or directory (merged with builtins)
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (default "default")
  -v, --verbose                Verbose output

Use "titus enum microsoft [command] --help" for more information about a command.
```

### `explore` (`titus explore --help`)

```text
Launch an interactive TUI to browse findings from a scan datastore.

The datastore path can be provided as a positional argument or via --datastore.
If omitted, defaults to titus.ds in the current directory.

Features:
  - Three-pane layout: filters, findings table, match details
  - Faceted search by rule name, category, and validation status
  - Accept/reject annotations with comments
  - Vi-style navigation (hjkl, Ctrl-f/b, g/G)
  - Source viewer for matched content
  - Sortable findings table

Usage:
  titus explore [datastore] [flags]

Flags:
      --datastore string   Path to datastore directory or file (default "titus.ds")
  -h, --help               help for explore

Global Flags:
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output
```

### `rules` (`titus rules --help`)

```text
Commands for listing and inspecting detection rules

Usage:
  titus rules [command]

Available Commands:
  list        List available rules

Flags:
  -h, --help   help for rules

Global Flags:
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output

Use "titus rules [command] --help" for more information about a command.
```

### `rules list` (`titus rules list --help`)

Captured alongside rules management (from `.tmp_titus_help/rules_list_help.txt`):

```text
Display all available detection rules with their IDs and names

Usage:
  titus rules list [flags]

Flags:
      --exclude string   Exclude rules matching regex pattern (comma-separated)
      --format string    Output format: table, json (default "table")
  -h, --help             help for list
      --include string   Include rules matching regex pattern (comma-separated)
      --include-noisy    Include rules marked noisy: true (off by default; high false-positive rate)
      --rules string     Path to custom rules file or directory

Global Flags:
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output
```

> Note: `.tmp_titus_help/rules_check_help.txt` matches `titus rules --help` (no separate `rules check` subcommand on v1.2.7 — only `list`).

### `serve` (`titus serve --help`)

```text
Run Titus as a long-lived streaming server that accepts scan requests
via stdin and outputs findings via stdout using NDJSON format.

This mode is designed for integration with the Burp Suite extension.
The process loads rules once at startup and processes requests until
stdin closes or SIGTERM is received.

Usage:
  titus serve [flags]

Flags:
  -h, --help                   help for serve
      --include-noisy          Enable rules marked noisy: true (high false-positive rate) (default true)
      --rules string           Path to custom rules file or directory
      --rules-exclude string   Exclude rules matching regex pattern (comma-separated)
      --rules-include string   Include rules matching regex pattern (comma-separated)
      --ruleset string         Ruleset to use: default, np.assets, np.hashes, all (all = no filtering) (default "all")

Global Flags:
  -q, --quiet     Quiet mode (errors only)
  -v, --verbose   Verbose output
```

---

## Quick reference (non-authoritative summary)

Use Captured help above for exact wording. Summary only:

| Area | Key flags |
|------|-----------|
| Formats | `--format json\|sarif\|human` (`scan`/`report`); enum/rules-list: `json` |
| Datastore | `scan --output` → `titus.ds`; `enum --output` → `titus.db`; `report --datastore` |
| Git / Docker | `--git`, `--docker`, `docker://…`, `github.com/…`, `gitlab.com/…` |
| Rules | `--rules`, `--ruleset`, `--rules-include`, `--rules-exclude`, `--include-noisy` |
| Extract | `--extract`, `--extract-max-*`, `--sqlite-row-limit` |
| Validate / score | `--validate`, `--validate-workers`, `--score-scope`, `--accessibility` |
| Triage | `explore`; `report --show-rejected` |

## Related

- Zero-to-Hero: `Titus-Zero-to-Hero.md`
- Agent skill: `.cursor/skills/Titus/SKILL.md`
- Upstream: https://github.com/praetorian-inc/titus
