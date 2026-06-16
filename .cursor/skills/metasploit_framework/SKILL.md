---
name: metasploit_framework
description: Use for msfconsole, msfvenom, use auxiliary/, search, set RHOSTS, exploit/multi/handler, db_nmap, workspace, resource script, and payload staging in authorized assessments where MSF discovery output must be mapped into SpiderFeet nugget graphs.
---

# Metasploit Framework Skill

## Purpose
Use Metasploit when authorized assessment workflows need auxiliary discovery modules, workspace-backed data, and optional payload/handler lab validation. Prefer dedicated scanners for pure scanning when MSF module depth is unnecessary.

## Step-by-Step Instructions
1. Install and verify `msfconsole`, `msfvenom`, `msfdb`.
2. Initialize DB: `msfdb init`; confirm with `db_status`.
3. Create/select workspace.
4. `search` then `use` module (start with `auxiliary/scanner/*` or `auxiliary/gather/*`).
5. Review `info`, `show options`, `show advanced`, `show evasion`.
6. `set` required datastore options (`RHOSTS`, `RPORT`, creds, threads).
7. Run with `run` (or `exploit` only when explicitly authorized).
8. Review `hosts`, `services`, `vulns`, `creds`, `loot`, `notes`.
9. Export and map to SpiderFeet nuggets/nodes/edges.

## If/Then Decision Rules
- If DB is unavailable, initialize/start `msfdb` before workspace workflows.
- If module supports `check`, run `check` before `exploit`.
- If objective is recon only, stay in auxiliary modules.
- If callback testing is needed, pair `msfvenom` with `exploit/multi/handler`.
- If staged payload fails, switch to stageless.
- If workspace remains empty, verify scope/options and module fit.

## Guardrails & Pitfalls
- Authorized targets only.
- Exploitation modules are out-of-scope unless explicitly approved.
- Read `info` references and side effects before execution.
- Use safe lab defaults for payload/handler tests.
- Separate engagements with workspaces.

## MSFvenom workflows
Generate payloads with explicit platform/arch/format, tune badchars/encoders cautiously, and pair reverse payloads with matching handler settings.

## Automation
- `msfconsole -r script.rc`
- `msfconsole -x "workspace <w>; use ...; set ...; run"`
- Keep workspace selection explicit in scripts.

## SpiderFeet nugget mapping
- `hosts` -> `IP_ADDRESS` / `INTERNET_NAME`
- `services` -> `TCP_PORT_OPEN` / `UDP_PORT_OPEN`
- `vulns` -> vulnerability nuggets
- `creds` / `loot` / session metadata -> structured sensitive nuggets
- Build `nodes[]` and `edges[]` (`contains`, `has`, `runs`, `affected_by`) from exports.
- Use TextFSM only when parsing unstructured console text that is not present in DB exports.

## References directory
See `references/SKILLS.md` for command families, module metadata, msfvenom workflows, database/workspaces, handlers/sessions, automation, and sources.
