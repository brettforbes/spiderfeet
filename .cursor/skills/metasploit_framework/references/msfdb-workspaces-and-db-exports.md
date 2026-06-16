# msfdb, Workspaces, and DB Exports

- Initialize DB with `msfdb init`; verify in console via `db_status`.
- Use one workspace per engagement.
- Capture discovery results in `hosts`, `services`, `vulns`, `creds`, `loot`.
- Export structured data with `db_export` for downstream nugget conversion.
- Use `db_nmap` when importing Nmap scan data into MSF DB context.
