# Metasploit Framework Zero to Hero

## 1) Install and initialize
1. Install Metasploit Framework.
2. Run `msfdb init`.
3. Start `msfconsole` and verify `db_status`.

## 2) Workspace and discovery-first flow
1. Create/select workspace.
2. Use auxiliary scanner modules for host/service enumeration.
3. Inspect module metadata and options before each run.
4. Execute and review `hosts`, `services`, `vulns`, `creds`, `loot`.

## 3) Optional lab payload flow
1. Generate payload with `msfvenom`.
2. Configure `exploit/multi/handler`.
3. Validate callback only in authorized lab contexts.

## 4) Export and map to SpiderFeet graph
- Use DB-backed results and exports to create `nodes[]` and `edges[]`.
- Typical edges: `contains`, `has`, `runs`, `affected_by`.
- Preserve provenance from workspace/module metadata.

## 5) Safety defaults
- Authorized targets only.
- Auxiliary/discovery-first unless exploit scope is explicitly approved.
