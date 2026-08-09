# msfdb, Workspaces, and DB Exports

## msfdb CLI (reconstructed 2026-08-10)

```text
Usage: msfdb [options] <command>
```

**Commands:** `init`, `reinit`, `delete`, `status`, `start`, `stop`, `restart`

**Component:** `--component database|webservice` (default `database`)

Common init:

```bash
msfdb init --use-defaults
msfdb status
msfdb start
```

Database options include `--msf-db-name`, `--msf-db-user-name`, test DB names/users, `--db-port` (default 5432), `--db-pool`, `--connection-string` (existing Postgres URI).

Webservice options include bind `-a`/`-p`, SSL toggles, admin `--user`/`--pass`, daemon flags. Full flag list: operator CLI-Options doc.

## Console verification

```text
msf6 > db_status
msf6 > workspace
msf6 > workspace -a eng_client_a
msf6 > workspace eng_client_a
```

Disable DB at console launch when intentional: `msfconsole -n`.

## Workspace discipline

- One workspace per engagement / corpus scenario family.
- Do not leave discovery results in `default` if they must be exported cleanly.
- Switch workspace **inside** every resource script before `use`/`run`.

## Populating the DB

| Method | When |
|--------|------|
| Auxiliary `run` | Native MSF discovery |
| `db_nmap …` | Nmap results straight into MSF DB |
| `db_import` | Import prior nmap/nessus/etc. supported formats |
| Manual `hosts -a` / notes | Sparse lab bookmarks |

## Review tables

`hosts`, `services`, `vulns`, `creds`, `loot`, `notes` — primary operator views before export.

## Export for SpiderFeet

Prefer structured export over copying TUI:

```text
msf6 > db_export -f xml /path/to/workspace_export.xml
```

Then map hosts/services/vulns into nuggets (`nugget-mapping.md`). When export is unavailable, capture `-o` console log and parse with TextFSM only for fields not in DB.

## Windows package caveat

On the SpiderFeet nightly extract, `msfdb` may fail at Bundler setup (`GemNotFound`) the same way as msfconsole — initialize DB only on a working install (complete MSI, Kali package, or fixed gem tree).
