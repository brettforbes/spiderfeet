---
name: recon_ng
description: Trigger for recon-ng, marketplace install, modules load, workspaces create, options set SOURCE, recon-cli, resource scripts, and OSINT module chaining when modular web OSINT pipelines must persist data in workspaces and feed SpiderFeet text/data/graph nugget outputs with controlled API spend.
---

# Recon-ng — Modular Web OSINT Framework

## Purpose

Use when the task needs a **modular, database-backed web OSINT workflow** — workspaces, marketplace modules, and table-to-table chaining — rather than a one-shot CLI.

Recon-ng ([lanmaster53/recon-ng](https://github.com/lanmaster53/recon-ng)) is an interactive Python framework (Metasploit-style console) with:

- **Workspaces** isolating engagement data
- **SQLite** tables that seed the next module
- A **module marketplace** (`recon-ng-marketplace`)
- Headless automation via **`recon-cli`** and resource files (`recon-ng -r script.rc`)
- Optional **`recon-web`** UI / Recon-API for review

Choose Recon-ng when you need workspace isolation, module chaining (`recon/<input>-<output>/…`), marketplace-driven capability, or repeatable headless runs for SpiderFeet nugget graphs.

Prefer standalone tools (dnsx, theHarvester, subfinder, etc.) when you only need one narrow collection step with no persistent workspace.

**Not Metasploit** — recon only, no exploit payloads. Distinguish from dnsx/uncover/theHarvester one-shot CLIs.

**Install (this host):**

| Piece | Path |
|-------|------|
| Python | `C:\projects\spiderfeet\.venv\Scripts\python.exe` |
| Framework root | `C:\projects\spiderfeet\.tools\recon-ng\` |
| Launchers | `recon-ng`, `recon-cli`, `recon-web` (run with venv Python; `PYTHONPATH` = framework root) |
| Version | **5.1.2** (`recon-ng --version`) |
| Help capture | **2026-08-10** (`.tmp_reconng_help/`) |

**SpiderFeet preference:** automate with **`recon-cli`** (workspace → global/module options → `-x`). Use interactive `recon-ng` for exploration and `script record`; use `recon-ng -r` for resource replay.

## Step-by-Step Instructions

1. **Confirm authorization** — web OSINT against approved orgs/domains only; respect API ToS and rate limits.
2. **Verify tooling** — from framework root (or with `PYTHONPATH` set):
   ```powershell
   $env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
   & C:\projects\spiderfeet\.venv\Scripts\python.exe C:\projects\spiderfeet\.tools\recon-ng\recon-ng --version
   & C:\projects\spiderfeet\.venv\Scripts\python.exe C:\projects\spiderfeet\.tools\recon-ng\recon-cli -h
   ```
3. **Bootstrap** — launch once without `--stealth` so marketplace can initialize; create/select a workspace.
4. **Keys** — `keys list` / `keys add <provider> <value>` before K-marked modules; never commit keys.
5. **Marketplace** — refresh, search, install only modules needed for the chain. **Do not use `--stealth` until modules are installed** — stealth disables marketplace; `recon-cli -M` then reports `No modules found`.
6. **Load and configure** — `modules load recon/<input>-<output>/…`; `show info` / `show options`; set `SOURCE` (literal, file, or SQL).
7. **Run and validate** — execute module; `db query` / `show` for row growth before chaining.
8. **Chain** — domains → hosts → contacts/ports → reporting; gate expensive API modules on non-zero table deltas.
9. **Export** — `reporting/*` and/or SQL extracts; map rows to SpiderFeet nuggets (`references/nugget-mapping.md`).
10. **Automate** — promote proven sequences to `recon-cli` or `recon-ng -r` for SpiderFeet pipelines.

## If/Then Decision Rules

| If | Then |
|----|------|
| SpiderFeet / CI / corpus automation | Prefer **`recon-cli`** (`-w`, `-m`, `-o`, `-x`); capture structured exports, not TUI only |
| Fresh host / empty module list | Install marketplace modules **without** `--stealth` / `--no-marketplace` first |
| Need OPSEC / no outbound framework checks | `--stealth` (implies `--no-version --no-analytics --no-marketplace`) — modules must already be installed |
| Module shows dependency (D) | Install dependency before run |
| Module requires key (K) | `keys add` then smoke-test on a tiny `SOURCE` |
| High API spend / rate risk | Passive free/passive modules; gate paid modules on new-row yield |
| Large `SOURCE` | Batch; checkpoint `db query` between runs |
| Prerequisite table empty | Pivot module family or fix `SOURCE` — do not treat as “tool broken” |
| Module stale / disabled / removed | Alternate in same `recon/<input>-<output>/` path |
| Workspace looks mixed | Stop; `workspaces select` correct engagement |
| Interactive exploration done | `script record` → resource file → `recon-cli` for production |

## Guardrails & Pitfalls

- **Authorized targets only** — framework modules query third-party APIs and web sources.
- **Marketplace quality varies** — validate metadata and sample output; do not install the entire catalog blindly.
- **One workspace per engagement** — never mix clients.
- **`--stealth` ≠ “stealthy modules”** — it disables framework passive requests (version/analytics/marketplace). Documented capture: with stealth, marketplace disabled and module list empty until modules are installed.
- **Do not invent launcher flags** — only options from Captured help (`recon-ng` / `recon-cli` / `recon-web`).
- **Empty tables ≠ success** — verify row deltas before reporting or chaining.
- **Keys in scripts** — inject from secure env; keep secrets out of `.rc` files committed to git.
- **Abandoned modules** — check marketplace issues; replace with maintained peers in the same I/O path.

## Automation

| Mode | When |
|------|------|
| **`recon-cli`** (preferred for SpiderFeet) | Headless: `-w`, `-C`/`-c`, `-g`/`-o`, `-m`, `-x` |
| **`recon-ng -r script.rc`** | Deterministic resource replay |
| **`script record` / `script execute`** | Capture interactive → replay |
| **`spool`** | Console evidence for text tab / audit |

Minimal `recon-cli` pattern (after modules installed):

```powershell
$py = "C:\projects\spiderfeet\.venv\Scripts\python.exe"
$cli = "C:\projects\spiderfeet\.tools\recon-ng\recon-cli"
$env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
& $py $cli -w acme-ext -m recon/domains-hosts/example_module -o "SOURCE=example.com" -x
```

Use `-G` / `-O` / `-M` to inspect options and installed modules (without inventing flags).

## SpiderFeet nugget mapping

Map workspace tables / reporting exports into nuggets (see `references/nugget-mapping.md`):

| Recon-ng | Nugget direction |
|----------|------------------|
| `domains` | `INTERNET_NAME` / `DOMAIN_NAME` |
| `hosts` | `INTERNET_NAME`, `IPV4_ADDRESS` / `IPV6_ADDRESS` via `classify_ip` |
| `contacts` | `HUMAN_NAME`, `EMAILADDR`, `PHONE_NUMBER` |
| `ports` | `TCP_PORT_OPEN` / `UDP_PORT_OPEN` |
| `vulnerabilities` | `VULNERABILITY_GENERAL` (+ CVE types when present) |

Edges: `contains` (domain→host, host→port); `had` for descriptor attributes. Align with `.seed/04_Driving and Integrating_CLI_Apps.md` and catalogue reuse before inventing types.

Output tabs: text (spool/report) · structured data (SQL/reporting JSON/CSV) · graph (nodes/edges from structured rows).

## Strategies and Tactics

### Module selection by path

- Pick `recon/<input>-<output>/` where `<input>` matches a non-empty table.
- Keep alternate modules per path for staleness.
- Run `reporting/*` only after tables validate.

### SOURCE strategy

- Literal — smoke-test module viability.
- File — curated bulk seeds.
- SQL — adaptive chaining from workspace truth (prefer for hosts→ports).

### API spend

- Passive first → paid only on new high-value seeds.
- Track per-module row delta; stop zero-growth repeats.
- Reuse workspace rows instead of re-querying providers.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Launcher flags from live capture; stealth/module-empty note |
| `workspaces-and-database.md` | Workspaces, SQLite, `db query` gates |
| `marketplace-and-modules.md` | Marketplace lifecycle, disabled/stale modules |
| `module-io-paths-and-source.md` | Path heuristics, SOURCE strategies |
| `keys-and-global-options.md` | Keys + captured global options |
| `automation-and-scripting.md` | recon-cli, `-r`, script, spool |
| `reporting-and-recon-web.md` | reporting/*, recon-web /api/ |
| `nugget-mapping.md` | Tables → SpiderFeet graph |
| `development-api-and-metadata.md` | Module meta, D/K, issue routing |
| `sources.md` | Canonical URLs |

Operator guides: `.docs/docs-for-cli-tools/recon-ng-Zero-to-Hero.md`, `recon-ng-CLI-Options.md`.

## Comprehensive Examples

### WORKSPACES

```text
workspaces create acme-ext-2026q3
workspaces select acme-ext-2026q3
workspaces list
```

### MARKETPLACE (interactive; marketplace enabled)

```text
marketplace refresh
marketplace search domains-hosts
marketplace info recon/domains-hosts/<module>
marketplace install recon/domains-hosts/<module>
```

### MODULES + SOURCE (domains → hosts)

```text
modules load recon/domains-hosts/<module>
show info
show options
options set SOURCE example.com
run
db query SELECT COUNT(*) FROM hosts
```

### DOMAINS → CONTACTS

```text
modules load recon/domains-contacts/<module>
options set SOURCE example.com
run
db query SELECT * FROM contacts LIMIT 20
```

### HOSTS → PORTS (SQL SOURCE)

```text
modules load recon/hosts-ports/<module>
options set SOURCE query SELECT host FROM hosts WHERE host IS NOT NULL
run
```

### REPORTING

```text
modules load reporting/<module>
show options
run
```

### RECON-CLI (headless)

```powershell
$env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
$py = "C:\projects\spiderfeet\.venv\Scripts\python.exe"
$cli = "C:\projects\spiderfeet\.tools\recon-ng\recon-cli"
& $py $cli -w acme-ext -G
& $py $cli -w acme-ext -M
& $py $cli -w acme-ext -m recon/domains-hosts/<module> -O
& $py $cli -w acme-ext -m recon/domains-hosts/<module> -o SOURCE=example.com -x
```

### RESOURCE FILE

```powershell
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-ng -w acme-ext -r .\pipelines\acme-domain.rc
```

### RECON-WEB

```powershell
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-web --host 127.0.0.1 --port 5000
# Browser UI + Recon-API under /api/
```
