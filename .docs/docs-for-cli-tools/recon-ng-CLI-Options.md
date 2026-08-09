# Recon-ng CLI Options

Operator reference for **Recon-ng** framework launchers and console command families. Prefer **`recon-cli`** for SpiderFeet automation after marketplace modules are installed.

| Field | Value |
|-------|-------|
| Version | **5.1.2** |
| Python | `C:\projects\spiderfeet\.venv\Scripts\python.exe` |
| Framework root | `C:\projects\spiderfeet\.tools\recon-ng\` |
| Launchers | `recon-ng`, `recon-cli`, `recon-web` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_reconng_help/*.txt` |

> Launcher flags below are from live `-h` / `--version` / `-G` / `-M` only — **do not invent options**.  
> Console families (`workspaces`, `marketplace`, …) are interactive framework commands (wiki / Features); they are not additional launcher flags.

Skill: `.cursor/skills/recon_ng/SKILL.md`

---

## SpiderFeet preferred commands

```powershell
$env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
$py = "C:\projects\spiderfeet\.venv\Scripts\python.exe"
$cli = "C:\projects\spiderfeet\.tools\recon-ng\recon-cli"

# Inspect (after modules installed; avoid --stealth until then)
& $py $cli -w acme-ext -G
& $py $cli -w acme-ext -M

# Run a module headlessly
& $py $cli -w acme-ext -m recon/domains-hosts/<module> -o SOURCE=example.com -x

# Resource replay
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-ng -w acme-ext -r .\pipelines\acme.rc
```

### Observed: `--stealth` disables marketplace

Captures of `recon-cli --stealth -G` and `recon-cli --stealth -M` show:

- `[*] Marketplace disabled.`
- `[*] Version check disabled.`
- `-M` → `[!] No modules found.`

Install marketplace modules **with marketplace enabled** first. Use `--stealth` only when local modules already exist and you want all `--no-*` passive framework requests disabled.

---

## Captured help

Live help text captured from `C:\projects\spiderfeet\.tools\recon-ng\` via Windows Python on **2026-08-10**. Each block is the full content of the listed capture file (ANSI sequences retained where present).

### recon-ng

#### Version (`recon-ng --version`) — `.tmp_reconng_help/recon-ng_version.txt`

```text
5.1.2
```

#### Root help (`recon-ng -h`) — `.tmp_reconng_help/recon-ng_help.txt`

```text
usage: recon-ng [-h] [-w workspace] [-r filename] [--no-version]
                [--no-analytics] [--no-marketplace] [--stealth] [--accessible]
                [--version]

recon-ng - Tim Tomes (@lanmaster53)

options:
  -h, --help        show this help message and exit
  -w workspace      load/create a workspace
  -r filename       load commands from a resource file
  --no-version      disable version check
  --no-analytics    disable analytics reporting
  --no-marketplace  disable remote module management
  --stealth         disable all passive requests (--no-*)
  --accessible      Use accessible outputs when available
  --version         displays the current version
```

### recon-cli

#### Root help (`recon-cli -h`) — `.tmp_reconng_help/recon-cli_help.txt`

```text
usage: recon-cli [-h] [-w workspace] [-C command] [-c command] [-G]
                 [-g name=value] [-M] [-m module] [-O] [-o name=value] [-x]
                 [--no-version] [--no-analytics] [--no-marketplace]
                 [--stealth] [--version]

recon-cli - Tim Tomes (@lanmaster53)

options:
  -h, --help        show this help message and exit
  -w workspace      load/create a workspace
  -C command        runs a command at the global context
  -c command        runs a command at the module context (pre-run)
  -G                show available global options
  -g name=value     set a global option (can be used more than once)
  -M                show modules
  -m module         specify the module
  -O                show available module options
  -o name=value     set a module option (can be used more than once)
  -x                run the module
  --no-version      disable version check
  --no-analytics    disable analytics reporting
  --no-marketplace  disable remote module management
  --stealth         disable all passive requests (--no-*)
  --version         displays the current version
```

#### Global options (`recon-cli --stealth -G`) — `.tmp_reconng_help/recon-cli_global_opts.txt`

```text
[32m[*][m Marketplace disabled.
[32m[*][m Version check disabled.

  Name        Current Value  Required  Description
  ----------  -------------  --------  -----------
  NAMESERVER  8.8.8.8        yes       default nameserver for the resolver mixin
  PROXY                      no        proxy server (address:port)
  THREADS     10             yes       number of threads (where applicable)
  TIMEOUT     10             yes       socket timeout (seconds)
  USER-AGENT  Recon-ng/v5    yes       user-agent string
  VERBOSITY   1              yes       verbosity level (0 = minimal, 1 = verbose, 2 = debug)

```

#### Modules list (`recon-cli --stealth -M`) — `.tmp_reconng_help/recon-cli_modules.txt`

```text
[32m[*][m Marketplace disabled.
[32m[*][m Version check disabled.
[31m[!] No modules found.[m
Searches installed modules

Usage: modules search [<regex>]

```

### recon-web

#### Root help / startup (`recon-web -h`) — `.tmp_reconng_help/recon-web_help.txt`

```text
*************************************************************************
 * Welcome to Recon-web, the analytics and reporting engine for Recon-ng!
 * This is a web-based user interface. Open the URL below in your browser to begin.
 * Recon-web includes the Recon-API, which can be accessed via the `/api/` URL.
*************************************************************************
[32m[*][m Marketplace disabled.
[32m[*][m Version check disabled.
 * Workspace initialized: C:\Users\brett\.recon-ng\workspaces\default
usage: recon-web [-h] [--host HOST] [--port PORT]

options:
  -h, --help   show this help message and exit
  --host HOST  IP address to listen on
  --port PORT  port to bind the web server to
```

### Re-capture

```powershell
$env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
$py = "C:\projects\spiderfeet\.venv\Scripts\python.exe"
$root = "C:\projects\spiderfeet\.tools\recon-ng"
$out = "C:\projects\spiderfeet\.tmp_reconng_help"
New-Item -ItemType Directory -Force -Path $out | Out-Null

& $py "$root\recon-ng" --version | Out-File -Encoding utf8 "$out\recon-ng_version.txt"
& $py "$root\recon-ng" -h        | Out-File -Encoding utf8 "$out\recon-ng_help.txt"
& $py "$root\recon-cli" -h       | Out-File -Encoding utf8 "$out\recon-cli_help.txt"
& $py "$root\recon-cli" --stealth -G | Out-File -Encoding utf8 "$out\recon-cli_global_opts.txt"
& $py "$root\recon-cli" --stealth -M | Out-File -Encoding utf8 "$out\recon-cli_modules.txt"
& $py "$root\recon-web" -h       | Out-File -Encoding utf8 "$out\recon-web_help.txt"
```

---

## Launcher options reference (tables)

### `recon-ng`

| Flag | Description |
|------|-------------|
| `-h, --help` | show this help message and exit |
| `-w workspace` | load/create a workspace |
| `-r filename` | load commands from a resource file |
| `--no-version` | disable version check |
| `--no-analytics` | disable analytics reporting |
| `--no-marketplace` | disable remote module management |
| `--stealth` | disable all passive requests (`--no-*`) |
| `--accessible` | Use accessible outputs when available |
| `--version` | displays the current version |

### `recon-cli`

| Flag | Description |
|------|-------------|
| `-h, --help` | show this help message and exit |
| `-w workspace` | load/create a workspace |
| `-C command` | runs a command at the global context |
| `-c command` | runs a command at the module context (pre-run) |
| `-G` | show available global options |
| `-g name=value` | set a global option (can be used more than once) |
| `-M` | show modules |
| `-m module` | specify the module |
| `-O` | show available module options |
| `-o name=value` | set a module option (can be used more than once) |
| `-x` | run the module |
| `--no-version` | disable version check |
| `--no-analytics` | disable analytics reporting |
| `--no-marketplace` | disable remote module management |
| `--stealth` | disable all passive requests (`--no-*`) |
| `--version` | displays the current version |

### `recon-web`

| Flag | Description |
|------|-------------|
| `-h, --help` | show this help message and exit |
| `--host HOST` | IP address to listen on |
| `--port PORT` | port to bind the web server to |

---

## Console command families

Interactive `recon-ng` console (and `recon-cli -C` / `-c` command strings). Confirm exact subcommands with in-console `help` on your install — wiki [Features](https://github.com/lanmaster53/recon-ng/wiki/Features) is canonical.

### `workspaces`

Create, select, list engagement contexts. Example: `workspaces create acme-ext` → `workspaces select acme-ext`.

### `marketplace`

Discover/install/remove/update modules when marketplace is **enabled** (not under `--stealth` / `--no-marketplace`). Refresh → search → info → install.

### `modules`

Search/load by path (`recon/<input>-<output>/…`, `reporting/*`). Capture note: with no installed modules, `modules search` usage is shown.

### `options`

Set module options including `SOURCE` (literal, file, or SQL). Via CLI: `recon-cli -o name=value`.

### `keys`

List/add provider API credentials before K-marked modules.

### `db`

`db query` against workspace SQLite for row-count gates and SQL `SOURCE` construction.

### `show`

Inspect module metadata, options, and table visibility (`show info`, `show options`, …).

### `dashboard`

High-level workspace status before deep `db query`.

### `snapshots`

Point-in-time workspace state for rollback/comparison around high-impact sequences.

### `spool`

Capture console output to file for evidence and parser ingestion.

### `script`

`script record` / `script execute` to capture and replay interactive sessions.

### Global options

Framework-wide posture. Captured names: `NAMESERVER`, `PROXY`, `THREADS`, `TIMEOUT`, `USER-AGENT`, `VERBOSITY`. Set with `recon-cli -g name=value`.

---

## Module category worked examples

### `recon/domains-hosts/*`

Goal: domain seeds → host assets. Start literal/file `SOURCE`, then SQL if chaining from prior domain rows.

### `recon/hosts-ports/*`

Goal: enrich hosts with port/service data. SQL-filter to new/priority hosts to reduce redundant calls.

### `recon/domains-contacts/*`

Goal: people/contact artifacts from domains. Literal or SQL subset for segmentation.

### `reporting/*`

Goal: export for operator review and SpiderFeet text/data/graph tabs. Prefer structured export formats when the module provides them.

---

## Tactical usage rules

- Choose modules by current table state, not a static favorite list.
- Treat empty prerequisite tables as sequencing blockers.
- Run low-cost/passive modules before quota-heavy API modules.
- Stop repeated zero-delta modules.
- Reuse workspace data through SQL `SOURCE` rather than re-querying identical inputs.
- Prefer **`recon-cli`** for SpiderFeet; keep interactive console for exploration and `script record`.
