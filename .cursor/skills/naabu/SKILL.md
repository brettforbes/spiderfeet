---
name: naabu
description: Fast SYN/CONNECT/UDP port scanning with Naabu, JSON-lines output, and SpiderFeet nugget mapping. Use for port enumeration, host discovery, passive InternetDB recon, CDN-aware scans, and pipelines to httpx, Nerva, Nmap, or Julius on authorized targets.
---

# Naabu — Port Scan to Nuggets

## Purpose

Use when you must **enumerate open TCP/UDP ports** on hosts, CIDRs, or stdin-fed target lists faster than full Nmap, capture **`naabu -json`** JSON Lines, and map results to SpiderFeet **`TCP_PORT_OPEN`** / **`UDP_PORT_OPEN`** nuggets — then chain to **httpx**, **Nerva**, **Nmap**, or **Julius**.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized hosts/CIDRs only. Install **libpcap** (Linux/macOS) or **Npcap** (Windows) for SYN scans.
2. **Choose scan mode** — SYN (`-s s`, root) vs CONNECT (`-s c`, default); passive (`-passive`) when active scan blocked.
3. **Select ports** — `-top-ports 100`, explicit `-p`, or `-p -` for full range on single high-value host.
4. **Optional discovery** — `-wn` / `-sn` on large nets before port scan.
5. **Run with JSON** — `naabu -host TARGET -json -o out.jsonl` (add `-silent` for pipes).
6. **Parse JSONL** — Line-by-line; see `references/json-output-schema.md`.
7. **Map nuggets** — `IP_ADDRESS`, `INTERNET_NAME`, port nodes per `references/nugget-mapping.md`.
8. **Adapt** — Lower `-rate`, `-ec` for CDN, `-verify`, `-passive`, or escalate to Nmap `-sV`/`-nmap-cli`.
9. **Chain downstream** — httpx, Nerva, Julius on AI port lists.

## If/Then Decision Rules

| If | Then |
|----|------|
| Non-root / Windows user | Default CONNECT `-s c`; or run as admin for SYN |
| Large CIDR | `-wn` discovery first; avoid `-p -` on whole net |
| CDN/WAF target | `-ec` or `-cdn` to label; expect 80/443 only with `-ec` |
| IDS / packet drops | Lower `-rate 200-500`, increase `-timeout`, reduce `-c` |
| Need structured output | Always `-json`; never parse banner art |
| UDP services | `-p u:53,u:161` plus `-uP` for payloads |
| No packets allowed | `-passive -json` (InternetDB) |
| Need service versions | `-sV` (requires local nmap probes) or `-nmap-cli` |
| Pipe to httpx | `-json -silent` |
| Pipe to Nerva | `jq` to `host:port` or compatible JSON pipe |
| AI / LLM hunt | `-p 11434,8000,8080,7860,4000,3000` → Julius |
| Zero open ports | Valid **clean_miss** for negative fixtures |
| IPv6 focus | `-iv 6` |
| Multiple DNS A records | `-sa` |

## Guardrails & Pitfalls

- **Authorization** — mass scanning without scope is prohibited.
- **JSON Lines** — not a JSON array; parse per line.
- **VPS vs laptop** — default `-rate 1000` may be too fast locally; tune down.
- **`-nmap-cli`** executes shell Nmap — injection risk if built from untrusted input.
- **Passive ≠ confirmed** — InternetDB may be stale; re-scan actively when allowed.
- **Do not** emit closed ports as open nuggets.
- **SYN scan** requires privileges; document fallback to CONNECT.
- **Full port scan** `-p -` on many hosts is slow and noisy — tier targets.
- `-stream` disables resume, verify, nmap integration — know tradeoffs.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | All flags |
| `json-output-schema.md` | JSONL fields |
| `workflows-and-phases.md` | Phase sequences |
| `tactics.md` | CDN, rate, passive |
| `nugget-mapping.md` | JSON → nuggets |
| `nmap-integration.md` | `-sV`, `-nmap-cli`, UDP |
| `sources.md` | URLs |

Operator guides: `.docs/docs-for-cli-tools/Naabu-Zero-to-Hero.md`, `Naabu-CLI-Options.md`.

## Comprehensive Examples

### Input targets

```bash
naabu -host scanme.sh -json
naabu -host a.com,b.com -p 80,443 -json
naabu -host 192.168.1.0/24 -top-ports 100 -json
naabu -l hosts.txt -json -o out.jsonl
echo scanme.sh | naabu -json
subfinder -d example.com -silent | naabu -json
echo AS13335 | naabu -p 443 -json
```

### Port selection

```bash
naabu -host scanme.sh -p 22,80,443 -json
naabu -host scanme.sh -top-ports 1000 -json
naabu -host scanme.sh -p - -json
naabu -host scanme.sh -p u:53,u:161 -uP -json
naabu -host scanme.sh -p - -exclude-ports 80,443 -json
```

### Output

```bash
naabu -host scanme.sh -json -o ports.jsonl
naabu -host scanme.sh -json -silent
naabu -host scanme.sh -csv -o ports.csv
naabu -host scanme.sh -silent
```

### Scan type and rate

```bash
naabu -host scanme.sh -s s -json
naabu -host scanme.sh -s c -json
naabu -host scanme.sh -rate 300 -c 10 -json
```

### Host discovery

```bash
naabu -host 192.168.1.0/24 -sn
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json
naabu -host 192.168.1.0/24 -arp -wn -p 22,80,443 -json
```

### CDN / passive

```bash
naabu -host cloudflare.site -ec -cdn -json
naabu -host example.com -passive -json
```

### Service detection

```bash
naabu -host scanme.sh -sV -json
naabu -host scanme.sh -sD -json
naabu -host scanme.sh -sV-fast -json
naabu -host scanme.sh -nmap-cli 'nmap -sV -oX out.xml'
```

### Verify / smart

```bash
naabu -host scanme.sh -p 1-1000 -verify -json
naabu -host scanme.sh -ss -json
```

### IPv6 / all IPs

```bash
naabu -host example.com -iv 6 -p 80 -json
naabu -host example.com -sa -p 443 -json -silent
```

### Pipelines

```bash
naabu -host example.com -json -silent | httpx -silent
naabu -host example.com -json -silent | jq -r '(.host//.ip)+":"+(.port|tostring)' | nerva --json
naabu -host corp.internal -p 11434,8000 -json -silent -o ai.jsonl
```

## Strategies and Tactics

### Maximize port data on unknown network

1. **dnsx/subfinder** → host list.
2. **Discovery** `-wn` on large nets → live IP file.
3. **Top 1000** `-top-ports 1000 -json` on live hosts.
4. **Verify** if noisy; **full `-p -`** only on interesting hosts.
5. **httpx** on web ports; **Nerva** on full open set.
6. Compare **passive** `-passive` JSONL with active for gap analysis.

### Hostile / filtered network

1. Drop `-rate` to 200–500.
2. Switch **CONNECT** if SYN filtered.
3. **`-ec`** on CDN domains.
4. **Passive** first, active confirm on subset.
5. Escalate to **Nmap `-sT -T2`** on stubborn hosts (separate skill).

### Bug bounty quick sweep

```bash
subfinder -d target.com -silent | naabu -top-ports 1000 -json -silent | httpx -silent
```

### SpiderFeet seed workflows

| Seed | Command pattern |
|------|-----------------|
| `INTERNET_NAME` | `naabu -host SEED -top-ports 100 -json` |
| `IP_ADDRESS` | `naabu -host SEED -p 22,80,443,8080 -json` |
| `NETBLOCK_OWNER` | cap size; `-wn` then top ports only |

### Pipeline with Julius (shadow AI)

```bash
naabu -host internal.corp -p 11434,8000,8080,7860,4000,3000,443 -json -silent -o ports.jsonl
jq -r '"https://" + (.ip) + ":" + (.port|tostring)' ports.jsonl | julius probe - -o jsonl
```

Attach `source_module` and jsonl path to every port nugget for Tests tab replay.
