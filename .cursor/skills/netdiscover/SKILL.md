---
name: netdiscover
description: ARP-based LAN host discovery with netdiscover. Use for local subnet reconnaissance, passive ARP sniffing, machine-readable -P output parsed via TextFSM into IP/MAC/vendor nuggets, and Netdiscover+Nmap layered discovery pipelines.
---

# Netdiscover — ARP Network Discovery

## Purpose

Use when discovering **live hosts on a local Layer-2 segment** via ARP (active scan, passive sniff, or parseable `-P` output), then mapping results to SpiderFeet nuggets and feeding discovered IPs into port scanners (Nmap → Nerva).

## Step-by-Step Instructions

1. **Confirm scope** — Netdiscover is for **local broadcast domains** (same VLAN/subnet). Requires root/CAP_NET_RAW on Linux. Not a substitute for routed WAN discovery.
2. **Pick interface** — List interfaces (`ip link` / `ifconfig`). Set `-i` when multiple NICs, VPN tunnels, or wireless adapters exist.
3. **Choose scan mode**:
   - Known CIDR → `-r 192.168.1.0/24`
   - Multiple ranges → `-l ranges.txt` (one CIDR per line)
   - Unknown subnet → auto-scan (no `-r`/`-l`/`-p`) or `-f` fast probe first
   - Stealth / no transmit → `-p` passive only
4. **Run for automation** — Always add `-P` (and `-N` to suppress header if available) for SpiderFeet/TextFSM pipelines. Redirect stdout to a file.
5. **Parse with TextFSM** — Apply `netdiscover_parsable.textfsm` (see `references/output-and-parsing.md`). Map rows → nuggets per `references/nugget-mapping.md`.
6. **Follow-on scanning** — For each discovered IP, run Nmap port discovery, then pipe open `host:port` targets to Nerva for service fingerprinting.
7. **Tune if results are thin** — Increase `-c` (retries), `-s` (inter-request delay), or disable `-S` hardcore mode on lossy/wireless links.

## If/Then Decision Rules

| If | Then |
|----|------|
| Target is remote/routed (not same L2) | Do **not** use netdiscover; use `nmap -sn` or ICMP/TCP discovery |
| Engagement requires zero extra ARP noise | Use `-p` passive; accept longer runtime and incomplete coverage |
| Subnet unknown | Auto-scan or `-f` fast mode on common ranges; refine with `-r` on hits |
| Building SpiderFeet module/parser | Use `-P` only; never parse interactive TUI output |
| Need hosts after active scan ends | Add `-L` with `-P` to keep passive ARP capture running |
| Packet loss / Wi-Fi | Increase `-c`, avoid `-S`, increase `-s` |
| Need maximum speed on large /16 | `-f` first, then full `-r` only on occupied /24 blocks |
| Duplicate source IP during scan | Change `-n` (last octet of scanner IP, 2–253) |
| Custom home ranges ignored | Check `~/.netdiscover/ranges` or use `-d` for defaults |
| Discovered IPs need services | `nmap -p- --open -oG - <ip>` → extract ports → `nerva --json` |

## Guardrails & Pitfalls

- Requires **elevated privileges** (raw sockets). Failures often mean missing `sudo` or container without `CAP_NET_RAW`.
- ARP discovery **does not cross routers**; /8 scans only find hosts on attached segments.
- Interactive mode (`-P` absent) is human-oriented — **do not TextFSM-parse** banner/header lines.
- `-S` (hardcore / sleep suppression) can miss hosts on lossy networks.
- `-f` fast mode scans only configured last-octets (default `.1`, `.100`, `.254`) — not a full subnet sweep.
- Vendor strings in `-P` output may contain spaces; template must capture remainder of line.
- Windows: run via WSL/Linux VM; no native binary.
- Document authorization before any active `-r` scan.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `cli-options.md` | All flags and interactive keys |
| `output-and-parsing.md` | `-P` format, TextFSM template |
| `nugget-mapping.md` | Rows → SpiderFeet nuggets |
| `tactics.md` | Passive vs active, Nmap combo |
| `sources.md` | Canonical URLs |

Cross-skill: [`../textfsm/SKILL.md`](../textfsm/SKILL.md) for template authoring; [`../nmap/SKILL.md`](../nmap/SKILL.md) and [`../nerva/SKILL.md`](../nerva/SKILL.md) for downstream fingerprinting.

## Examples (per flag)

### `-i` — interface

```bash
sudo netdiscover -i wlan0 -P -N -r 192.168.43.0/24
```

### `-r` — range scan

```bash
sudo netdiscover -P -N -r 10.0.0.0/24,192.168.1.0/24
```

### `-l` — range list file

```bash
# ranges.txt: one CIDR per line
sudo netdiscover -P -N -l ranges.txt
```

### `-p` — passive mode

```bash
sudo netdiscover -p -i eth0
# No -P: runs until 'q'; use for live TUI observation only
```

### `-s` — sleep between ARP requests (ms)

```bash
sudo netdiscover -P -N -s 100 -r 192.168.1.0/24
```

### `-c` — ARP retry count per host

```bash
sudo netdiscover -P -N -c 5 -r 192.168.1.0/24
```

### `-n` — source IP last octet

```bash
sudo netdiscover -P -N -n 200 -r 192.168.1.0/24
```

### `-S` — hardcore (suppress per-host sleep)

```bash
sudo netdiscover -P -N -S -r 192.168.1.0/24
```

### `-f` — fast mode (gateway/common hosts only)

```bash
sudo netdiscover -P -N -f -r 192.168.0.0/16
```

### `-d` — ignore `~/.netdiscover/` config

```bash
sudo netdiscover -P -N -d -f
```

### `-P` — parseable output (required for TextFSM)

```bash
sudo netdiscover -P -N -r 192.168.1.0/24 > /tmp/nd.out
```

### `-L` — continue passive after active `-P` scan

```bash
sudo netdiscover -P -L -r 192.168.1.0/24
# Emits parseable lines while passively capturing; longer-running
```

### Auto-scan (no `-r`, `-l`, or `-p`)

```bash
sudo netdiscover -P -N
```

## Strategies & Tactics

### Layered discovery pipeline

```
netdiscover -P -N -r <cidr>     →  IPs + MACs + vendors (TextFSM)
        ↓
nmap -sn -PR <cidr>             →  confirm / fill gaps (optional cross-check)
        ↓
nmap -p- --open -oG - <each_ip> →  open TCP ports
        ↓
nerva --json -l targets.txt     →  service fingerprints per host:port
```

### Passive vs active

| Goal | Mode | Command sketch |
|------|------|----------------|
| Stealth / compliance | Passive | `netdiscover -p -i eth0` |
| Full inventory fast | Active parseable | `netdiscover -P -N -r 192.168.x.0/24` |
| Unknown LAN layout | Fast then deep | `-f` auto → full `-r` on busy /24 |
| Long-term presence | Active then passive | `-P -L -r …` |

### Netdiscover + Nmap combo

- **Netdiscover first** when you need MAC/vendor at L2 and the segment is local; ARP is faster and quieter than full `nmap -sn` on dense /24s.
- **Nmap `-sn -PR`** when you want a second opinion or netdiscover is unavailable; merge IP sets before port scan.
- **Never skip port discovery** — netdiscover does not find open ports; always hand IPs to Nmap/Naabu, then **Nerva** on `host:port` pairs.
- On **filtered WLAN**, combine passive netdiscover (`-p`) with triggered active `-r` on observed subnets.

### Adapting to weak results

1. Zero hosts → wrong interface (`-i`), wrong VLAN, or all hosts blocking ARP (rare).
2. Partial hosts → increase `-c`, remove `-S`, slow down with `-s`.
3. Too slow on /16 → `-f` sweep, then targeted `-r /24`.
4. New hosts appear later → `-P -L` or periodic passive `-p`.
