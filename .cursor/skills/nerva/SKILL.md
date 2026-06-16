---
name: nerva
description: Service fingerprint open ports with Nerva using --json JSON-lines output mapped to SpiderFeet nuggets. Use after port discovery (Nmap/Naabu/netdiscover→nmap), for host:port protocol ID, UDP/SCTP plugins, and pipeline integration.
---

# Nerva — Service Fingerprinting

## Purpose

Use when **TCP/UDP/SCTP ports are already known open** and you need fast, accurate **service/protocol identification** with structured **`--json` JSON-lines** output converted to SpiderFeet nuggets — typically after netdiscover host discovery and Nmap port scanning.

## Step-by-Step Instructions

1. **Confirm prerequisites** — Nerva expects `host:port` or `ip:port` targets; it does not discover open ports itself.
2. **Build target list** — From Nmap greppable output, Naabu, or Masscan: one `host:port` per line in `targets.txt`.
3. **Choose transport flags** — TCP (default), add `-U` for UDP services, `-S` for SCTP (Linux only).
4. **Run with JSON** — `nerva -l targets.txt --json -o results.jsonl` (or pipe stdout).
5. **Parse JSON lines** — One JSON object per line; skip empty lines. See `references/json-output-schema.md`.
6. **Map to nuggets** — Emit `TCP_PORT_OPEN` / `UDP_PORT_OPEN`, protocol, banners, and metadata per `references/nugget-mapping.md`.
7. **Tune performance** — `--fast` for large lists; `-w <ms>` for slow services; `-v` for stderr diagnostics only.
8. **Chain upstream** — Standard pipeline: **netdiscover** → **nmap** → **nerva**.

## If/Then Decision Rules

| If | Then |
|----|------|
| Only host IPs, no ports | Run Nmap/Naabu first; do not invoke Nerva |
| DNS name + open port | `nerva -t example.com:443 --json` |
| Many targets from file | `nerva -l targets.txt --json` |
| UDP service (53, 161, 123…) | Add `-U`; may require `sudo` |
| Telecom Diameter / SCTP | Add `-S` on Linux |
| Huge target list, speed priority | `--fast` (default-port plugins only) |
| Slow or latent service | Increase `-w 5000` or higher |
| Need spreadsheet | `--csv -o results.csv` instead of JSON |
| Parsing for SpiderFeet module | Always `--json`; never parse human `ssh://` lines |
| Port scan from Nmap | See `references/tactics.md` awk pipeline |

## Guardrails & Pitfalls

- Nerva **assumes ports are open** — closed ports waste time or return no fingerprint.
- `--json` emits **JSON Lines** (NDJSON), not a single JSON array — parse line-by-line.
- `metadata` shape varies per protocol plugin — treat as semi-structured; do not assume fixed keys globally.
- UDP fingerprinting may need root and is less reliable than TCP.
- SCTP (`-S`) is **Linux-only**.
- `--fast` can miss services on non-standard ports.
- Do not use Nerva for host discovery — use netdiscover/Nmap `-sn` first.
- Human-readable output (`ssh://host:22`) is for operators only, not parsers.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `cli-options.md` | All flags |
| `json-output-schema.md` | `--json` field reference |
| `protocol-list.md` | 54 plugins by category |
| `nugget-mapping.md` | JSON → SpiderFeet nuggets |
| `tactics.md` | Pipelines, port discovery → nerva |
| `sources.md` | Canonical URLs |

## Examples (per flag)

### `--targets` / `-t`

```bash
nerva -t example.com:22 --json
nerva -t server.example.com:22,server.example.com:80,server.example.com:443 --json
```

### `--list` / `-l`

```bash
nerva -l targets.txt --json -o results.jsonl
```

### `--output` / `-o`

```bash
nerva -l targets.txt --json -o /tmp/nerva_out.jsonl
# Default: JSON lines to stdout
```

### `--json`

```bash
nerva -t 192.168.1.10:22 --json
# {"host":"192.168.1.10","ip":"192.168.1.10","port":22,"protocol":"ssh","transport":"tcp","metadata":{...}}
```

### `--csv`

```bash
nerva -l targets.txt --csv -o results.csv
```

### `--fast` / `-f`

```bash
nerva -l large_targets.txt --fast --json
```

### `--udp` / `-U`

```bash
sudo nerva -t example.com:53 -U --json
```

### `--sctp` / `-S`

```bash
nerva -t mme.telecom.local:3868 -S --json
```

### `--timeout` / `-w`

```bash
nerva -t slow-server.example.com:8080 -w 5000 --json
```

### `--verbose` / `-v`

```bash
nerva -l targets.txt --json -v 2>nerva_debug.log
```

### Stdin pipe (from Naabu)

```bash
naabu -host example.com -silent | nerva --json
```

## Strategies & Tactics

### Standard SpiderFeet pipeline

```
netdiscover -P -N -r <cidr>  →  IPs (TextFSM)
nmap -p- --open <ips>        →  host:port list
nerva -l targets.txt --json  →  service nuggets
```

### Port discovery → fingerprint

| Scanner | Handoff command |
|---------|-----------------|
| Naabu | `naabu -host TARGET -silent \| nerva --json` |
| Masscan | `masscan … -oL - \| awk … \| nerva --json` |
| Nmap | greppable `-oG` awk extract (see `tactics.md`) |

### Adapting to results

| Observation | Next step |
|-------------|-----------|
| `protocol: http` with rich `metadata` | Emit web tech nuggets; optional Wappalyzer fields |
| `protocol: unknown` or empty | Retry without `--fast`; increase `-w` |
| UDP no match | Confirm `-U` and `sudo` |
| Many targets, tight SLA | `--fast --json` first pass; full scan on interesting hosts |
| SSH/RDP found | Emit remote-access nuggets; link to parent IP from netdiscover |

### TCP vs UDP vs SCTP

1. **TCP** — default; cover web, DB, remote access
2. **UDP** — split target file; run `nerva -l udp_targets.txt -U --json`
3. **SCTP** — telecom targets only; Linux scanner host

See [`references/tactics.md`](references/tactics.md) for full playbooks.
