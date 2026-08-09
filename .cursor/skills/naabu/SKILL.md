---
name: naabu
description: Fast SYN/CONNECT port scanning with Naabu, JSON-lines output, and SpiderFeet nugget mapping. Use for port enumeration, host discovery, passive InternetDB recon, CDN-aware scans, and pipelines to httpx, Nerva, Nmap, or Julius on authorized targets.
---

# Naabu — Port Scan to Nuggets

## Purpose

Use when you must **enumerate open ports** on hosts, CIDRs, ASN lists, or stdin-fed targets with [ProjectDiscovery Naabu](https://github.com/projectdiscovery/naabu), capture **`-json` / `-j` JSON Lines**, and map results to SpiderFeet **`TCP_PORT_OPEN`** (and **`UDP_PORT_OPEN`** when UDP ports are requested via `u:port` syntax), then chain to **httpx**, **Nerva**, **Nmap**, or **Julius**.

Run **after** host/name lists exist (`subfinder`, `dnsx`, seed IPs/CIDRs). Prefer Naabu for mass port inventory; escalate to **Nmap** for OS/NSE depth.

**Binary (this repo):** `C:\projects\spiderfeet\.tools\naabu\naabu.exe` — **v2.6.1** (captured **2026-08-10**).

**Windows note:** This binary’s help defaults **`-scan-type` / `-s` to `c` (CONNECT)**. Health-check on this host showed `Privileged/NET_RAW: Ko`. SYN (`-s s`) needs elevated privileges + Npcap; without that, stay on CONNECT.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized hosts/CIDRs/ASNs only. SYN needs root/admin + libpcap/Npcap; CONNECT works unprivileged.
2. **Prepare inputs** — `-host`, `-list` / `-l`, or stdin (unless `-no-stdin`). Exclude with `-eh` / `-ef` when needed.
3. **Choose port profile** — `-top-ports 100|1000|full` (default top 100), explicit `-p` (`80,443`, ranges `100-200`, full via `-p -` per PD running docs), or `-ports-file`.
4. **Optional discovery** — Large nets: `-wn` before port scan, or `-sn` discovery-only; skip with `-Pn` when hosts are known live.
5. **Run with JSONL** — Always `-json` / `-j` for corpus and nuggets. Add `-silent` for pipes; `-o` for a file. Prefer `-duc` in automation to skip update checks.
6. **Parse JSONL** — One object per open port; fields in `references/json-output-schema.md`.
7. **Map nuggets** — Host → `INTERNET_NAME`; IPs via `classify_ip`; ports → `TCP_PORT_OPEN` / `UDP_PORT_OPEN` per `references/nugget-mapping.md`.
8. **Adapt** — Lower `-rate`/`-c` on filtered nets; `-ec`/`-cdn` for CDN; `-verify` for false positives; `-passive` when active scan is blocked; escalate with `-sV`/`-sD` or `-nmap-cli`.
9. **Chain downstream** — httpx on web ports; Nerva on open `host:port`; Julius on AI port lists.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-json` (`-j`); never parse banner art only |
| Windows / non-root / `Privileged/NET_RAW: Ko` | Stay on CONNECT (`-s c`, this binary’s default); do not assume SYN works |
| Elevated Linux/macOS + pcap | Prefer SYN `-s s` for speed when authorized |
| Large CIDR / many downs | `-wn` (or `-sn` first); avoid `-top-ports full` / `-p -` on whole net |
| CDN/WAF front | `-ec` (only 80/443 on CDN IPs) and/or `-cdn` to label |
| IDS / packet drops / laptop | Lower `-rate` (e.g. 200–500), raise `-timeout`, reduce `-c` |
| Need historical ports without touching target | `-passive -json` (Shodan InternetDB) — then optionally confirm actively |
| Need service name/version in naabu | `-sD` and/or `-sV` (local nmap probes); or `-nmap-cli 'nmap -sV …'` |
| Multiple A/AAAA for one name | `-sa` (+ `-iv 4,6` when both families matter) |
| IPv6-only focus | `-iv 6` |
| Stream large stdin lists | `-stream` (disables resume, nmap, verify, retries, shuffling, etc.) |
| Resume interrupted scan | `-resume` (not with `-stream`) |
| Predictive ports | `-ss` / `-smart-scan` with optional `-pt` threshold |
| Pipe to httpx | Prefer `-silent` host:port lines, or JSONL + jq |
| Pipe to Nerva | `jq` to `host:port` from JSONL |
| AI / LLM hunt | `-p 11434,8000,8080,7860,4000,3000` → Julius |
| Zero open ports | Valid **clean_miss** for negative fixtures |
| Empty JSONL on known-open host | Check `-Pn`, rate/timeout, IPv4 vs `-iv 6`, CONNECT vs SYN |

## Guardrails & Pitfalls

- **Authorization** — Mass scanning without scope is prohibited.
- **JSONL ≠ JSON array** — Parse line by line; harvest bundles use `records[]`.
- **Do not invent flags** — Use only options from live `naabu -h` (see CLI docs Captured help). Port syntax extras (`-p -`, `u:53`) come from official PD Running docs, not inventing new switches.
- **Windows SYN** — Without NET_RAW/Npcap privileges, SYN is unreliable or unavailable; CONNECT is the safe default here.
- **VPS vs laptop** — Default `-rate 1000` assumes VPS-class capacity; tune down locally.
- **`-nmap-cli`** executes shell Nmap — injection risk if built from untrusted input.
- **Passive ≠ confirmed** — InternetDB may be stale; re-scan actively when allowed.
- **`-stream` tradeoffs** — Disables resume, nmap integration, verify, retries, shuffling.
- **Full port sweeps** — `-top-ports full` / `-p -` on many hosts is slow and noisy — tier targets.
- **Do not** emit closed/filtered ports as open nuggets.
- **IP nuggets** — Use `core.ip_classify.classify_ip`; never hardcode `IP_ADDRESS` for colon-form literals.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | All flags by category |
| `json-output-schema.md` | JSONL fields |
| `workflows-and-phases.md` | Phase sequences |
| `tactics.md` | CDN, rate, passive, hostile nets |
| `nugget-mapping.md` | JSONL → SpiderFeet graph |
| `nmap-integration.md` | `-sV`, `-sD`, `-nmap-cli` |
| `sources.md` | Official URLs |

Operator guides: `.docs/docs-for-cli-tools/Naabu-Zero-to-Hero.md`, `Naabu-CLI-Options.md`.

Help captures: `.tmp_naabu_help/` (`help_h.txt`, `help_long.txt`, `version.txt`) — **2026-08-10**.

## Comprehensive Examples

### INPUT

```bash
naabu -host scanme.nmap.org -json -silent -duc
naabu -host a.com,b.com -p 80,443 -json -silent -duc
naabu -host 192.168.1.0/24 -top-ports 100 -json -silent -duc
naabu -l hosts.txt -json -o out.jsonl -duc
echo scanme.nmap.org | naabu -json -silent -duc
subfinder -d example.com -silent | naabu -json -silent -duc
echo AS14421 | naabu -p 80,443 -json -silent -duc
```

### PORT

```bash
naabu -host scanme.nmap.org -p 22,80,443 -json -silent -duc
naabu -host scanme.nmap.org -top-ports 1000 -json -silent -duc
naabu -host scanme.nmap.org -top-ports full -json -silent -duc
naabu -host scanme.nmap.org -p - -json -silent -duc
naabu -host scanme.nmap.org -p 80,443,u:53 -json -silent -duc
naabu -host scanme.nmap.org -p - -exclude-ports 80,443 -json -silent -duc
naabu -host cdn.example.com -ec -cdn -json -silent -duc
```

### OUTPUT (JSONL preferred)

```bash
naabu -host scanme.nmap.org -json -o ports.jsonl -duc
naabu -host scanme.nmap.org -json -silent -duc
naabu -host scanme.nmap.org -csv -o ports.csv -duc
```

### CONFIGURATION (scan type / IPs)

```bash
naabu -host scanme.nmap.org -s c -json -silent -duc
naabu -host scanme.nmap.org -s s -json -silent -duc
naabu -host example.com -sa -iv 4,6 -p 443 -json -silent -duc
naabu -host example.com -iv 6 -p 80 -json -silent -duc
naabu -host scanme.nmap.org -rate 300 -c 10 -json -silent -duc
```

### HOST-DISCOVERY

```bash
naabu -host 192.168.1.0/24 -sn -duc
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json -silent -duc
naabu -host 192.168.1.0/24 -wn -arp -p 22,80,443 -json -silent -duc
naabu -host 10.0.0.0/24 -Pn -top-ports 100 -json -silent -duc
```

### PASSIVE / CDN

```bash
naabu -host example.com -passive -json -silent -duc
naabu -host cloudflare.site -ec -cdn -json -silent -duc
```

### SERVICES-DISCOVERY

```bash
naabu -host scanme.nmap.org -sD -json -silent -duc
naabu -host scanme.nmap.org -sV -json -silent -duc
naabu -host scanme.nmap.org -nmap-cli "nmap -sV -oX out.xml" -duc
```

### OPTIMIZATION

```bash
naabu -host scanme.nmap.org -p 1-1000 -verify -json -silent -duc
naabu -host scanme.nmap.org -ss -json -silent -duc
naabu -host scanme.nmap.org -ss -pt 40 -json -silent -duc
naabu -host scanme.nmap.org -retries 5 -timeout 2s -json -silent -duc
```

### PIPELINES

```bash
echo example.com | naabu -silent -duc | httpx -silent
naabu -host example.com -json -silent -duc | jq -r '(.host//.ip)+":"+(.port|tostring)' | nerva --json
naabu -host corp.internal -p 11434,8000,8080,7860,4000,3000 -json -silent -o ai.jsonl -duc
```

### Parse one JSONL line (Python)

```python
import json

line = '{"host":"scanme.nmap.org","ip":"45.33.32.156","timestamp":"2026-08-10T00:00:00Z","port":80,"protocol":"tcp","tls":false}'
row = json.loads(line)
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Discover → top ports → deep on winners** — `-wn` / top 1000, then `-p -` only on interesting hosts.
2. **Windows / unprivileged** — CONNECT first; document SYN as privilege-gated.
3. **CDN-aware** — `-ec` + `-cdn`; do not waste full sweeps on edge IPs.
4. **Hostile nets** — Drop rate, raise timeout, verify, optionally passive-then-active.
5. **Pipeline order** — `subfinder → dnsx → naabu -json → httpx / nerva / julius`; Nmap for OS/NSE.
6. **Maximize thin yield** — `-sa`, both IP versions, `-verify`, passive gap-fill, then Nerva on opens.
