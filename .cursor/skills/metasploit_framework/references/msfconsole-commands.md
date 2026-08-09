# MSFconsole Interactive Commands

These are **console** commands (typed at the `msf6 >` prompt or passed via `-x` / resource scripts). They are **not** `msfconsole` process argv flags. Argv flags are in `cli-options.md` / the operator CLI-Options doc.

## Module selection and metadata

| Command | Role |
|---------|------|
| `search <terms>` | Find modules (`type:auxiliary`, `platform:windows`, CVE, name fragments) |
| `use <module>` | Load module path |
| `back` | Leave current module context |
| `info` / `info -d` | Module summary; `-d` opens documentation when available |
| `show options` | Required/optional datastore |
| `show advanced` | Advanced datastore |
| `show evasion` | Evasion options |
| `show payloads` | Compatible payloads (exploit context) |
| `show targets` | Exploit targets |

## Datastore

| Command | Role |
|---------|------|
| `set <OPT> <val>` | Module-local option |
| `setg <OPT> <val>` | Global (persists across modules — use sparingly) |
| `unset` / `unsetg` | Clear local / global |
| `get` / `getg` | Inspect values |

## Execution

| Command | Role |
|---------|------|
| `run` | Execute auxiliary (also common for handler) |
| `check` | Non-exploit validation when implemented |
| `exploit` | Launch exploit — **authorized only** |
| `exploit -j` / `run -j` | Jobify (background) |
| `jobs` / `jobs -k <id>` | List / kill jobs |

## Sessions

| Command | Role |
|---------|------|
| `sessions` / `sessions -l` | List |
| `sessions -i <id>` | Interact |
| `sessions -k <id>` | Kill |
| `sessions -k 1,2-4` | Ranges (comma; `-` or `..`) — see shipped `msfconsole.md` |

## Workspaces and database views

| Command | Role |
|---------|------|
| `workspace` | List / select |
| `workspace -a <name>` | Add |
| `workspace -d <name>` | Delete |
| `db_status` | Connectivity |
| `db_nmap <nmap args>` | Run nmap into DB |
| `db_import` / `db_export` | Import/export workspace data |
| `hosts` | Host table |
| `services` | Service table |
| `vulns` | Vulnerability table |
| `creds` | Credentials |
| `loot` | Loot files/metadata |
| `notes` | Notes |

## Ranges (shipped package doc)

From package `msfconsole.md` (captured `.tmp_msf_help/msfconsole.md`):

- ID lists: comma-separated; ranges with `-` or `..` (no spaces around commas).
- IP lists: spaces/commas, `BEGIN-END`, CIDR with full address (`127.0.0.0/8`), Nmap-style octet ranges, IPv6 supported.
- Examples: `sessions -k 1`, `jobs -k 2-6,7,8,11..15`, `set RHOSTS 127.0.0.0/16`.

## Workflow rule

Always `info` → `show options` → `set` → `run`/`check` before any `exploit`. Prefer reviewing `hosts`/`services` after every discovery module.
