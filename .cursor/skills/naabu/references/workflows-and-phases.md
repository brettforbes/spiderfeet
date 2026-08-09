# Naabu Workflows and Phases

## Phase model

```
Resolve targets → (optional host discovery) → Port scan → (optional verify/sV) → JSONL → Nuggets → Downstream
```

**Binary (this repo):** `C:\projects\spiderfeet\.tools\naabu\naabu.exe` **v2.6.1** — help captured **2026-08-10**.

## Phase 1 — Target resolution

| Input type | Example |
|------------|---------|
| Single host | `naabu -host scanme.nmap.org -json -silent -duc` |
| Multiple | `naabu -host a.com,b.com -json -silent -duc` |
| CIDR | `naabu -host 192.168.1.0/24 -json -silent -duc` |
| File | `naabu -l hosts.txt -json -silent -duc` |
| Stdin | `subfinder -d example.com -silent \| naabu -json -silent -duc` |
| ASN | `echo AS14421 \| naabu -p 80,443 -json -silent -duc` |

## Phase 2 — Host discovery (optional)

When scanning large nets where many IPs are down:

```bash
naabu -host 10.0.0.0/24 -sn -duc
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json -silent -duc
```

| Flag | Use |
|------|-----|
| `-sn` | Discovery only — no port scan |
| `-wn` | Discover live hosts before port scan |
| `-Pn` | Skip discovery when hosts are known live |

If ICMP blocked: combine `-wn` with `-ps 80,443` or `-arp` on LAN. ICMP/ARP/SYN discovery probes often need privileges — on Windows CONNECT-only hosts, discovery richness may be limited.

## Phase 3 — Port scan (core)

**Profile: quick recon**

```bash
naabu -host target.com -top-ports 100 -json -silent -duc
```

**Profile: standard assessment**

```bash
naabu -host target.com -p 22,80,443,8080,8443,3000,8000,11434 -json -o ports.jsonl -duc
```

**Profile: deep (single host)**

```bash
naabu -host highvalue.internal -top-ports full -json -verify -silent -duc
# or, per PD Running docs:
naabu -host highvalue.internal -p - -json -verify -silent -duc
```

**Scan type (this binary):**

| Mode | Flag | Requires |
|------|------|----------|
| CONNECT | `-s c` (**default in v2.6.1 help**) | Non-root / Windows OK |
| SYN | `-s s` | Privileges + libpcap/Npcap (`Privileged/NET_RAW` must not be `Ko`) |

## Phase 4 — Passive enrichment

No packets to target — queries Shodan InternetDB:

```bash
naabu -host example.com -passive -json -silent -duc
```

Use for low-touch recon when active scan is blocked or to seed an active port list.

## Phase 5 — Service enrichment

Flags present in live help:

```bash
naabu -host scanme.nmap.org -sV -json -silent -duc
naabu -host scanme.nmap.org -sD -json -silent -duc
naabu -host scanme.nmap.org -nmap-cli "nmap -sV -oX detail.xml" -duc
```

See [nmap-integration.md](nmap-integration.md). Do not invent extra `-sV-*` switches.

## Phase 6 — Downstream chaining

```bash
echo example.com | naabu -silent -duc | httpx -silent
naabu -host example.com -json -silent -duc | jq -r '(.host//.ip)+":"+(.port|tostring)' | nerva --json
```

For Julius LLM ports:

```bash
naabu -host corp.internal -p 11434,8000,8080,7860,4000 -json -silent -o ai_ports.jsonl -duc
```

## Formal examination (SpiderFeet corpus)

Capture per scenario:

- Exact CLI including `-json` (structured-first)
- Structured bundle with `records[]` parsed from JSONL (not raw `.jsonl` as the Structured pane file)
- Text derived from structured at harvest
- Graph + narrative mandatory

Targets: permissive (`scanme.nmap.org` / `scanme.sh`), corporate (filtered CDN), clean miss (no open ports), passive vs active comparison. On Windows examination hosts, document CONNECT default and SYN privilege gate.
