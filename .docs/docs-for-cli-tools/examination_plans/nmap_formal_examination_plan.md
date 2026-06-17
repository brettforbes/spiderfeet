# Nmap — Formal Examination Plan

**Output path type:** 1 (structured XML + separate text runs per §2.2.1 rule 4)  
**Runtime:** Windows native (`C:\Program Files (x86)\Nmap\nmap.exe`)  
**Primary parser:** XML (`-oX -` or `-oX file`)  
**Manifest:** `.seed/scripts/cli_corpus/manifests/nmap.yaml`

## Exploration summary

Nmap exposes a single XML schema (`nmaprun`) across scan phases. Semantic breadth comes from:

| Phase | Flags | New XML elements / semantics |
|-------|-------|------------------------------|
| Host discovery | `-sn` | `host/status`, `address`, `hostnames` |
| Port scan | `-sT/-sS`, `-p`, `--top-ports` | `ports/port`, `state`, `service` (table) |
| Version | `-sV` | `service@product`, `@version`, `cpe` |
| OS | `-O` | `os/osmatch`, `osclass` (deferred — needs privileges) |
| NSE | `--script` | `script`, `elem`, `table`, `prescript`/`postscript` |
| Traceroute | `--traceroute` | `trace/hop` (deferred — add in pass 2) |
| UDP | `-sU` | UDP `port` states (deferred — add in pass 2) |

**Permissive vs corporate:** `scanme.nmap.org` yields open ports, version strings, and rich NSE output. `bbc.co.uk` resolves but returns fewer open ports / more filtered states — important for `clean_miss` and low-confidence paths.

## Scenarios (formal examination)

| Exam IDs | Scenario | Target | Structured | Text |
|----------|----------|--------|------------|------|
| 2–3 | Host discovery | scanme.nmap.org | XML | yes |
| 4–5 | TCP top-20 ports | scanme.nmap.org | XML | yes |
| 6–7 | Service version `-sV` ports 22,80,443 | scanme.nmap.org | XML | yes |
| 8 | NSE default+safe | scanme.nmap.org | XML | (text in same run — long) |
| 9–10 | Host discovery | bbc.co.uk | XML | yes |
| 11 | TCP top-10 ports | bbc.co.uk | XML | — |

Evidence: `.docs/docs-for-cli-tools/app_examination_docs/nmap/`

## Deferred scenarios (pass 2)

- `-O --osscan-limit` on scanme (admin / raw socket)
- `-sU` selected UDP ports
- `--traceroute` host path
- `-oA` multi-format export (grepable + normal) for text-derivation templates
- IPv6 `-6` single host

## Expected nugget types

From XML mapping (see `.cursor/skills/nmap/references/nugget-mapping.md`):

- `IP_ADDRESS`, `INTERNET_NAME`, `TCP_PORT_OPEN`, `UDP_PORT_OPEN`
- `OPERATING_SYSTEM`, `SOFTWARE_USED`, `WEBSERVER_TECHNOLOGY`
- `VULNERABILITY_GENERAL` / CVE from NSE tables
- `RAW_RIR_DATA` (whois scripts)
- Abstract: `Host`, `Networking`, `Application`, `Service` (V2 hierarchy)

## Review status

All examinations: `pending` — awaiting operator approval.
