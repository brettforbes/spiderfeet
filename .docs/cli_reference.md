# SpiderFeet / SpiderFeet CLI Reference

This document describes the command-line interfaces in this repository (**SpiderFeet**, based on **SpiderFeet 4.0.0**). SpiderFeet is an OSINT automation platform with two primary CLI entry points:

| Program | Role |
|---------|------|
| [`sf.py`](../sf.py) | Main application: run scans from the terminal, start the web UI, list modules/types, run correlations |
| [`sfcli.py`](../sfcli.py) | Interactive client that talks to a **running** SpiderFeet web server over HTTP |

Most day-to-day scanning can be done entirely with `sf.py`. Use `sfcli.py` when a server is already running and you want a REPL-style workflow (manage scans, query results, export data) without opening the browser.

---

## Prerequisites

- **Python**: 3.7 or newer (this repo is tested with Poetry using Python 3.11).
- **Dependencies**: install via Poetry (`poetry install`) or `pip install -r requirements.txt`.
- **Invocation** (from the repository root):

```bash
poetry run python sf.py [options]
poetry run python sfcli.py [options]
```

If the virtual environment is activated (`poetry shell`), you can omit `poetry run`.

---

## `sf.py` — overview

`sf.py` operates in several **mutually exclusive modes**, determined by which flags you pass. If you run `sf.py` with no arguments, it exits with a message requiring `-l <ip>:<port>` to start the web server.

| Mode | Trigger | Behavior |
|------|---------|----------|
| Web server | `-l IP:port` | Starts the CherryPy web UI and API |
| CLI scan | `-s TARGET` (+ module/type/use-case options) | Runs a scan; results stream to stdout |
| List modules | `-M` / `--modules` | Prints all loadable modules and descriptions |
| List event types | `-T` / `--types` | Prints all event type names and descriptions |
| Run correlations | `-C scanID` | Applies YAML correlation rules to an existing scan in the DB |
| Version | `-V` / `--version` | Prints version and exits |

Only one “primary” action runs per invocation (for example, you cannot combine `-l` and `-s` in a single process).

---

## `sf.py` — global options

```
usage: sf.py [-h] [-d] [-l IP:port] [-m mod1,mod2,...] [-M] [-C scanID]
             [-s TARGET] [-t type1,type2,...]
             [-u {all,footprint,investigate,passive}] [-T]
             [-o {tab,csv,json}] [-H] [-n] [-r] [-S LENGTH] [-D DELIMITER]
             [-f] [-F type1,type2,...] [-x] [-q] [-V]
             [-max-threads MAX_THREADS]
```

### General

| Flag | Description |
|------|-------------|
| `-h`, `--help` | Show help and exit |
| `-d`, `--debug` | Enable debug logging (also persisted to DB config for scans) |
| `-q` | Disable logging entirely (**errors are hidden too**) |
| `-V`, `--version` | Print `SpiderFeet 4.0.0` (from [`VERSION`](../VERSION)) and exit |
| `-max-threads N` | Override default concurrent module limit (default: **3**, key `_maxthreads`) |

### Web server

| Flag | Description |
|------|-------------|
| `-l IP:port` | Bind address for the web UI (e.g. `127.0.0.1:5001`, `0.0.0.0:5001`) |

On start, the process prints the URL to open in a browser. If TLS certificate files exist under the data directory (`spiderFeet.crt`, `spiderFeet.key`), HTTPS is enabled automatically.

### Scan target and module selection

| Flag | Description |
|------|-------------|
| `-s TARGET` | **Required** for CLI scans. Seed target (see [Scan targets](#scan-targets)) |
| `-m mod1,mod2,...` | Comma-separated module names (e.g. `sfp_dnsresolve,sfp_whois`) |
| `-t type1,type2,...` | Comma-separated **event types** to collect; SpiderFeet auto-enables modules that produce those types and their dependency chain |
| `-u {all,footprint,investigate,passive}` | Enable modules by **use case** (see [Use cases](#use-cases-u)) |
| `-x` | **Strict mode** — see [Strict mode](#strict-mode-x) |

If **none** of `-m`, `-t`, or `-u` is given, **all** modules are enabled (with a warning).

### Scan output (CLI scan mode only)

These flags configure the internal `sfp__stor_stdout` module, which prints events as the scan runs:

| Flag | Description |
|------|-------------|
| `-o {tab,csv,json}` | Output format (default: **tab**) |
| `-H` | Omit column headers (tab/csv only) |
| `-n` | Strip newlines from event data |
| `-r` | Include “source data” column (tab/csv only) |
| `-S LENGTH` | Truncate displayed data to `LENGTH` characters |
| `-D DELIMITER` | CSV delimiter (default `,`; only with `-o csv`) |
| `-f` | Filter stdout to **only** event types listed in `-t` (requires `-t`) |
| `-F type1,type2,...` | Show only these event types on stdout (implies filter behavior) |

**Tab/csv columns:**

- Without `-r`: `Source`, `Type`, `Data`
- With `-r`: `Source`, `Type`, `Source Data`, `Data`

**JSON output:** events are printed as a JSON array; the opening `[` is emitted before the scan and `]` after completion.

### Discovery / maintenance

| Flag | Description |
|------|-------------|
| `-M`, `--modules` | List modules (name + description); internal `sfp_*` modules with `__` in the name are hidden |
| `-T`, `--types` | List event types (name + human description) |
| `-C scanID`, `--correlate scanID` | Run all loaded correlation rules against scan `scanID` in the SQLite DB |

---

## Scan targets

SpiderFeet infers the target **type** from the `-s` string using regex rules in [`spiderFeet/helpers.py`](../spiderfeet/helpers.py) (`targetTypeFromString`). Supported types:

| Type | Example input | Notes |
|------|---------------|-------|
| `IP_ADDRESS` | `8.8.8.8` | IPv4 |
| `IPV6_ADDRESS` | `2001:4860:4860::8888` | Hex/colon form |
| `NETBLOCK_OWNER` | `192.168.0.0/24` | CIDR IPv4 |
| `NETBLOCKV6_OWNER` | `2001:db8::/32` | IPv6 CIDR |
| `INTERNET_NAME` | `example.com` | Hostname / domain label rules |
| `EMAILADDR` | `user@example.com` | Contains `@` |
| `PHONE_NUMBER` | `+15551234567` | Must start with `+` and digits |
| `HUMAN_NAME` | `"John Smith"` | Quoted; must contain a space |
| `USERNAME` | `"jsmith"` | Quoted single token |
| `BGP_AS_OWNER` | `15169` | Numeric AS |
| `BITCOIN_ADDRESS` | `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` | BTC address pattern |

**Quoting behavior:** If the target contains spaces, or has no `.` and does not look like a phone number (`+...`), `sf.py` wraps it in quotes before type detection. When passing names or usernames on the shell, use quotes so the shell does not split tokens:

```bash
poetry run python sf.py -s "\"Jane Doe\"" -u passive
poetry run python sf.py -s "\"alice\"" -u investigate
```

Invalid targets cause exit with: `Could not determine target type`.

---

## Use cases (`-u`)

Modules declare one or more use cases in metadata (`useCases`: `Footprint`, `Investigate`, `Passive`). The CLI maps `-u` to module groups:

| `-u` value | Modules included |
|------------|------------------|
| `passive` | Modules tagged **Passive** (no direct contact with target) |
| `footprint` | Modules tagged **Footprint** |
| `investigate` | Modules tagged **Investigate** |
| `all` | Every module regardless of tag |

Use case selection can be combined with output filters but is **not** compatible with strict mode’s override behavior in the same way as `-m` (see below).

---

## Strict mode (`-x`)

Strict mode limits work to modules and types that directly relate to the seed target:

- **Requires** `-t` (event types).
- **Cannot** be used with `-m`.
- Enables only modules that **consume** the inferred target type.
- Further filters to modules whose `provides` list intersects the requested `-t` types.
- Sets `__outputfilter` so downstream modules only pass through requested event types.

Example — only resolve DNS and show `INTERNET_NAME` results:

```bash
poetry run python sf.py -s example.com -t INTERNET_NAME -x
```

---

## Module selection by event type (`-t`)

When `-t` is specified, SpiderFeet:

1. Finds all modules that **produce** any listed type.
2. Walks the module dependency graph (types consumed → modules producing them) until the set stabilizes.
3. Always appends storage modules `sfp__stor_db` and `sfp__stor_stdout`.

This is useful when you care about **data types** (e.g. `EMAILADDR`, `MALICIOUS_IPADDR`) rather than picking modules manually.

List types with:

```bash
poetry run python sf.py -T
```

There are hundreds of event types (e.g. `EMAILADDR`, `TCP_PORT_OPEN`, `LINKED_URL_INTERNAL`). Names are uppercase with underscores.

---

## CLI scan lifecycle

1. Target validated; modules resolved.
2. Scan record created in SQLite (`SpiderFeetDb`).
3. Scanner runs in a background process (`startSpiderFeetScanner` in [`sfscan.py`](../sfscan.py)).
4. Main process polls every second until status is terminal.
5. Post-scan correlation may run (up to **60 seconds** join timeout).
6. Exit code **0** on `FINISHED`; errors on timeout or failed states.

**Terminal scan statuses** (field index 5 in scan instance):

| Status | Meaning |
|--------|---------|
| `FINISHED` | Completed successfully |
| `ABORTED` | User aborted (Ctrl+C sets `ABORTED` via signal handler) |
| `ABORT-REQUESTED` | Stop requested (e.g. from UI/CLI) |
| `ERROR-FAILED` | Scan failed |

**In-progress statuses** include `STARTING`, `STARTED`, `RUNNING`.

**Abort:** Press **Ctrl+C** during a CLI scan to mark the scan `ABORTED` and exit.

---

## `sf.py` examples

### Start web UI (default install flow)

```bash
poetry run python sf.py -l 127.0.0.1:5001
```

### List modules

```bash
poetry run python sf.py -M
```

### Passive footprint of a domain

```bash
poetry run python sf.py -s example.com -u passive
```

### Specific modules only

```bash
poetry run python sf.py -s 8.8.8.8 -m sfp_dnsresolve,sfp_whois,sfp_shodan
```

### Collect emails and output CSV

```bash
poetry run python sf.py -s example.com -t EMAILADDR -o csv -f
```

### JSON to stdout with source field

```bash
poetry run python sf.py -s example.com -t IP_ADDRESS -o json -r
```

### Re-run correlations for an existing scan

```bash
poetry run python sf.py -C <scan_id>
```

### Debug with more concurrent modules

```bash
poetry run python sf.py -d -max-threads 10 -s example.com -u footprint
```

---

## Data, configuration, and security files

SpiderFeet stores runtime data under a configurable directory (default: `~/.spiderFeet/`):

| Item | Location | Purpose |
|------|----------|---------|
| Database | `$SPIDERFEET_DATA/spiderFeet.db` or `~/.spiderFeet/spiderFeet.db` | Scan results, config |
| Passwords | `~/.spiderFeet/passwd` | HTTP digest auth for web UI (`username:password` per line) |
| TLS | `~/.spiderFeet/spiderFeet.crt`, `spiderFeet.key` | Optional HTTPS for web UI |
| Cache | `$SPIDERFEET_CACHE` or `~/.spiderFeet/cache` | Cached downloads |

Override with environment variable:

```bash
export SPIDERFEET_DATA=/path/to/spiderFeet-data
export SPIDERFEET_CACHE=/path/to/cache
```

**Legacy paths:** `sf.py` refuses to start if `spiderFeet.db` or `passwd` exist in the **application directory** (project root); move them to `~/.spiderFeet/`.

**Global scan options** (defaults in `sf.py`, overridable per module / via UI) include:

| Key | Default | Meaning |
|-----|---------|---------|
| `_maxthreads` | `3` | Concurrent modules |
| `_useragent` | Firefox UA string | HTTP User-Agent |
| `_fetchtimeout` | `5` | HTTP timeout (seconds) |
| `_dnsserver` | empty | Custom resolver (e.g. `8.8.8.8`) |
| `_debug` | `false` | Debug mode |
| SOCKS `_socks1type` … `_socks5pwd` | empty | Proxy settings |

---

## Correlation engine (CLI)

SpiderFeet 4.0 ships with **37** YAML correlation rules under [`correlations/`](../correlations/) (plus `template.yaml`). Rules run automatically after scans complete (with a short grace period). To **manually** re-run all rules against a scan:

```bash
poetry run python sf.py -C <scan_id>
```

Rule authoring is documented in [`correlations/README.md`](../correlations/README.md). Correlation output appears in logs and in the web UI / `sfcli` `correlations` command.

---

## `sfcli.py` — overview

`sfcli.py` is an **interactive command shell** that uses the SpiderFeet **REST-style HTTP API** exposed by the web server. It does not run scans locally; it sends requests to `cli.server_baseurl` (default `http://127.0.0.1:5001`).

**Typical workflow:**

```bash
# Terminal 1 — server
poetry run python sf.py -l 127.0.0.1:5001

# Terminal 2 — CLI client
poetry run python sfcli.py -s http://127.0.0.1:5001
```

At startup, `sfcli` runs `ping`, loads module/type lists for tab completion, and optionally restores command history from `~/.spiderFeet_history`.

### Platform note (Windows)

`sfcli` imports `readline` (or `pyreadline` on Windows). If neither is installed, startup fails. Install with:

```bash
poetry add pyreadline3 --group dev
# or: pip install pyreadline3
```

(Linux/macOS usually have GNU readline available.)

---

## `sfcli.py` — startup flags

```
usage: sfcli.py [-h] [-d] [-s URL] [-u USER] [-p PASS] [-P PASSFILE]
                [-e FILE] [-l FILE] [-n] [-o FILE] [-i] [-q] [-k] [-b]
```

| Flag | Description |
|------|-------------|
| `-d`, `--debug` | Enable CLI debug messages (`[+]` prefix) |
| `-s URL` | Server base URL (default `http://127.0.0.1:5001`) |
| `-u USER` | HTTP digest username |
| `-p PASS` | HTTP digest password (visible in process list; prefer `-P`) |
| `-P PASSFILE` | File with password on first line |
| `-e FILE` | Execute commands from file then exit (non-interactive) |
| `-l FILE` | History log file (default `~/.spiderFeet_history`) |
| `-n` | Disable history logging |
| `-o FILE` | Spool all commands and output to `FILE` |
| `-i` | Allow insecure HTTPS (disable TLS verify) |
| `-q` | Silent mode — only errors |
| `-k` | Disable color output |
| `-b`, `-v` | Print banner/version and exit |

**Non-interactive batch:**

```bash
poetry run python sfcli.py -e commands.txt -q
```

Where `commands.txt` contains one command per line (same as interactive input, without the `sf>` prompt).

---

## `sfcli` — interactive commands

Type `help` at the `sf>` prompt for a summary table.

### Server and metadata

| Command | Syntax | Description |
|---------|--------|-------------|
| `ping` | `ping` | Test server; warn if CLI/server versions differ |
| `modules` | `modules` | List modules (JSON from `/modules`) |
| `types` | `types` | List event types (`/eventtypes`) |
| `correlationrules` | `correlationrules` | List correlation rules (`/correlationrules`) |
| `set` | `set` / `set opt` / `set opt = val` | View or set CLI and server options |

### Scan management

| Command | Syntax | Description |
|---------|--------|-------------|
| `start` | `start <target> (-m mods \| -t types \| -u case) [-n name] [-w]` | Start scan (`/startscan`). **Requires** one of `-m`, `-t`, or `-u`. `-w` tails logs |
| `stop` | `stop <sid>` | Request abort (`/stopscan`) |
| `delete` | `delete <sid>` | Delete scan (`/scandelete`) |
| `scans` | `scans [-x]` | List scans (`/scanlist`); `-x` extended columns |
| `scaninfo` | `scaninfo <sid> [-c]` | Scan metadata; `-c` includes configuration |
| `logs` | `logs <sid> [-l count] [-w]` | Scan logs; `-w` watch until Ctrl+C |

### Results and export

| Command | Syntax | Description |
|---------|--------|-------------|
| `data` | `data <sid> [-t type] [-x] [-u]` | Event data (`/scaneventresults` or `...unique`). Default type `ALL`. `-x` extended columns. `-u` unique values only |
| `summary` | `summary <sid> [-t]` | Per-type counts (`/scansummary`); `-t` types only |
| `correlations` | `correlations <sid> [-c rule_id]` | Correlation hits; `-c` drills into events for one rule |
| `find` | `find "<string\|/regex/>" [-s sid] [-t type] [-x]` | Search scan DB (`/search`) |
| `search` | alias of `find` | Same as `find` |
| `export` | `export <sid> [-t json\|csv\|gexf] [-f file]` | Export scan; write to `-f` if given |
| `query` | `query <SQL>` | Run SQL against SQLite (`/query`) — use with care |

### Utilities

| Command | Description |
|---------|-------------|
| `debug` | Toggle `cli.debug` |
| `history` | Toggle history; `history -l` lists |
| `spool` | Toggle output spooling (requires `cli.spool_file`) |
| `clear` | Clear screen |
| `shell <cmd>` | Run local shell command |
| `exit` / Ctrl+D | Quit CLI (does not stop running scans) |

### `start` examples

```text
sf> start example.com -u passive
sf> start 8.8.8.8 -m sfp_dnsresolve,sfp_whois -n "DNS lookup"
sf> start user@corp.com -t EMAILADDR -w
```

Use case values for `-u` match `sf.py`: `all`, `footprint`, `investigate`, `passive`.

---

## `sfcli` — output pipes

Many commands support **Unix-style pipes** parsed after `|` in the command line. Pipes process the **text** sent to the terminal (after pretty-printing or JSON formatting).

| Pipe | Syntax | Behavior |
|------|--------|----------|
| `grep` / `str` | `\| grep pattern` | Lines containing `pattern` (case-insensitive) |
| `regex` | `\| regex ^pattern` | Lines matching regex |
| `top` | `\| top N` | First N lines |
| `last` | `\| last N` | Last N lines |
| `file` | `\| file path` | Write output to `path` |

Example:

```text
sf> scans -x | grep FINISHED
sf> data <sid> -t EMAILADDR | top 20 | file emails.txt
```

---

## `sfcli` — configuration variables

### CLI-local (`set cli.* = value`)

| Variable | Default | Purpose |
|----------|---------|---------|
| `cli.debug` | `false` | Verbose debug output |
| `cli.silent` | `false` | Errors only |
| `cli.color` | `true` | ANSI colors |
| `cli.output` | `pretty` | `pretty` or `json` for command results |
| `cli.history` | `true` | Readline history |
| `cli.history_file` | `~/.spiderFeet_history` | History path |
| `cli.spool` | `false` | Log all output to spool file |
| `cli.spool_file` | `""` | Spool path |
| `cli.ssl_verify` | `true` | TLS certificate verification |
| `cli.username` | `""` | Digest auth user |
| `cli.password` | `""` | Digest auth password |
| `cli.server_baseurl` | `http://127.0.0.1:5001` | API base URL |

Variables prefixed with `$` in commands are expanded from `ownopts` (e.g. for scripting).

### Server-side

`set <server_opt> = <value>` posts to `/savesettingsraw` using options from `/optsraw`. These mirror the global/module options in the web UI (thread count, User-Agent, module API keys, etc.). Use `set` with no arguments to dump CLI + server options.

---

## Internal storage modules

CLI scans always enable:

| Module | Role |
|--------|------|
| `sfp__stor_db` | Persists all events to SQLite |
| `sfp__stor_stdout` | Streams events to stdout using `-o`, `-f`, `-F`, etc. |

Modules whose names contain `__` (other than the stor modules above) are omitted from `-M` listings.

---

## Module catalog

This tree includes **233** module files under [`modules/`](../modules/) (template excluded from load). List names:

```bash
poetry run python sf.py -M
```

Module metadata (`flags`, `useCases`, `categories`, API requirements) is defined per module in each file’s `meta` dict — see [`modules/sfp_template.py`](../modules/sfp_template.py) for the schema.

---

## Quick reference — choosing an interface

| Goal | Command |
|------|---------|
| One-shot scan, scriptable output | `sf.py -s TARGET ...` |
| Run web UI | `sf.py -l 127.0.0.1:5001` |
| Explore results interactively | `sfcli.py` against running server |
| Automate server via script file | `sfcli.py -e cmds.txt` |
| Export GEXF/CSV/JSON from old scan | `sfcli` → `export <sid> -t gexf -f out.gexf` |
| Re-run correlation rules | `sf.py -C <sid>` |

---

## Further reading

- Project README: [`README.md`](../README.md)
- Correlation rules: [`correlations/README.md`](../correlations/README.md)
- Upstream documentation: https://www.spiderfeet.net/documentation
- Tests: [`test/README.md`](../test/README.md)

---

*Generated for the SpiderFeet repository (SpiderFeet 4.0.0). Flags and behavior reflect the current `sf.py` and `sfcli.py` sources; if upstream changes, compare against `python sf.py --help`.*
