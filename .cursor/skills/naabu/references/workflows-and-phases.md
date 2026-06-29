# Naabu Workflows and Phases

## Phase model

```
Resolve targets → (optional host discovery) → Port scan → (optional verify/sV) → JSONL → Nuggets → Downstream
```

## Phase 1 — Target resolution

| Input type | Example |
|------------|---------|
| Single host | `naabu -host scanme.sh -json` |
| Multiple | `naabu -host a.com,b.com -json` |
| CIDR | `naabu -host 192.168.1.0/24 -json` |
| File | `naabu -l hosts.txt -json` |
| Stdin | `subfinder -d example.com -silent \| naabu -json` |
| ASN | `echo AS13335 \| naabu -p 443 -json` |

## Phase 2 — Host discovery (optional)

When scanning large nets where many IPs are down:

```bash
naabu -host 10.0.0.0/24 -sn
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json
```

| Flag | Use |
|------|-----|
| `-sn` | Discovery only — no port scan |
| `-wn` | Discover live hosts before port scan |

If ICMP blocked: combine `-wn` with `-ps 80,443` or `-arp` on LAN.

## Phase 3 — Port scan (core)

**Profile: quick recon**

```bash
naabu -host target.com -top-ports 100 -json -silent
```

**Profile: standard assessment**

```bash
naabu -host target.com -p 22,80,443,8080,8443,3000,8000,11434 -json -o ports.jsonl
```

**Profile: deep (single host)**

```bash
naabu -host highvalue.internal -p - -json -verify
```

**Scan type:**

| Mode | Flag | Requires |
|------|------|----------|
| CONNECT | `-s c` (default) | Non-root OK |
| SYN | `-s s` | root/admin + libpcap |

## Phase 4 — Passive enrichment

No packets to target — queries Shodan InternetDB:

```bash
naabu -host example.com -passive -json
```

Use for low-touch recon when active scan is blocked or to seed active scan port list.

## Phase 5 — Service enrichment

```bash
naabu -host scanme.sh -sV -json
naabu -host scanme.sh -sD -json
naabu -host scanme.sh -nmap-cli 'nmap -sV -oX detail.xml'
```

See [nmap-integration.md](nmap-integration.md).

## Phase 6 — Downstream chaining

```bash
naabu -host example.com -json -silent | httpx -silent
naabu -host example.com -json -silent | jq -r '(.host//.ip)+":"+(.port|tostring)' | nerva --json
```

For Julius LLM ports:

```bash
naabu -host corp.internal -p 11434,8000,8080,7860,4000 -json -silent -o ai_ports.jsonl
```

## Formal examination (SpiderFeet corpus)

Capture per scenario:

- `{key}_command.txt` with exact CLI including `-json`
- `{key}_output_structured.jsonl`
- Optional text via `-silent` redirect for human-readable pair

Targets: permissive (`scanme.sh`), corporate (filtered CDN), clean miss (no open ports), passive vs active comparison.
