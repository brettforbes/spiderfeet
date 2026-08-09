# Recon-ng Launcher CLI Options (Captured)

Authoritative flags from live help on **2026-08-10**. Full verbatim blocks: `.docs/docs-for-cli-tools/recon-ng-CLI-Options.md`. Raw captures: `.tmp_reconng_help/`.

| Field | Value |
|-------|-------|
| Version | **5.1.2** |
| Python | `C:\projects\spiderfeet\.venv\Scripts\python.exe` |
| Framework | `C:\projects\spiderfeet\.tools\recon-ng\` |
| Scripts | `recon-ng`, `recon-cli`, `recon-web` |

Set `PYTHONPATH` to the framework root before invoking scripts with the venv Python.

## Observed: `--stealth` and empty modules

Capture used `--stealth` for `recon-cli -G` and `recon-cli -M`:

- `[*] Marketplace disabled.`
- `[*] Version check disabled.`
- `-M` → `[!] No modules found.` plus `modules search [<regex>]` usage hint

**Implication:** `--stealth` disables marketplace (with analytics/version checks). Module list stays empty until marketplace/modules are installed with marketplace enabled. Install modules first; use `--stealth` only when modules are already local.

## `recon-ng` flags

| Flag | Description (from help) |
|------|-------------------------|
| `-h, --help` | show help and exit |
| `-w workspace` | load/create a workspace |
| `-r filename` | load commands from a resource file |
| `--no-version` | disable version check |
| `--no-analytics` | disable analytics reporting |
| `--no-marketplace` | disable remote module management |
| `--stealth` | disable all passive requests (`--no-*`) |
| `--accessible` | Use accessible outputs when available |
| `--version` | displays the current version |

## `recon-cli` flags

| Flag | Description (from help) |
|------|-------------------------|
| `-h, --help` | show help and exit |
| `-w workspace` | load/create a workspace |
| `-C command` | runs a command at the global context |
| `-c command` | runs a command at the module context (pre-run) |
| `-G` | show available global options |
| `-g name=value` | set a global option (repeatable) |
| `-M` | show modules |
| `-m module` | specify the module |
| `-O` | show available module options |
| `-o name=value` | set a module option (repeatable) |
| `-x` | run the module |
| `--no-version` | disable version check |
| `--no-analytics` | disable analytics reporting |
| `--no-marketplace` | disable remote module management |
| `--stealth` | disable all passive requests (`--no-*`) |
| `--version` | displays the current version |

## Captured global options (`recon-cli --stealth -G`)

| Name | Current Value | Required | Description |
|------|---------------|----------|-------------|
| NAMESERVER | 8.8.8.8 | yes | default nameserver for the resolver mixin |
| PROXY | *(empty)* | no | proxy server (address:port) |
| THREADS | 10 | yes | number of threads (where applicable) |
| TIMEOUT | 10 | yes | socket timeout (seconds) |
| USER-AGENT | Recon-ng/v5 | yes | user-agent string |
| VERBOSITY | 1 | yes | verbosity level (0 = minimal, 1 = verbose, 2 = debug) |

## `recon-web` flags

| Flag | Description (from help) |
|------|-------------------------|
| `-h, --help` | show help and exit |
| `--host HOST` | IP address to listen on |
| `--port PORT` | port to bind the web server to |

Banner notes: web UI + Recon-API at `/api/`. Capture also printed marketplace/version-disabled lines when started with stealth-equivalent flags.

## Do not invent

Console families (`workspaces`, `marketplace`, `modules`, `keys`, `db`, …) are interactive framework commands — document from wiki/operator practice, not as launcher flags. Never add undocumented `--json` / export flags to these launchers.
