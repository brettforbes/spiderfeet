# Nmap Workflows and Scan Phases

Nmap executes internal **phases** (see https://nmap.org/book/nmap-phases.html). Agents compose **commands** that enable the phases needed for the investigation goal, always writing **XML** for machine parsing.

## Internal scan phases (conceptual)

| Phase | What happens | Typical flags |
|-------|----------------|---------------|
| 1. Target enumeration | Expand CIDR, ranges, lists | Target spec on CLI |
| 2. Host discovery | Which hosts are up | Default ping, `-Pn`, `-sn` |
| 3. Reverse DNS | PTR lookups | `-n` to skip, `-R` to always |
| 4. Parallelization grouping | Batch hosts for efficiency | Automatic |
| 5. Port scan | Probe ports | `-sS`, `-sT`, `-sU`, `-p` |
| 6. Service/version | Banner and probe matching | `-sV` |
| 7. OS detection | IP stack fingerprint | `-O`, `--osscan-limit` |
| 8. Traceroute | Path mapping | `--traceroute` |
| 9. NSE scripts | Scripted enrichment | `-sC`, `--script` |
| 10. Output | Write results | **`-oX file.xml`** |

Not every command runs all phases. `-sn` stops after phase 2. `-p 80 -sV` skips OS unless `-O` added.

## Adaptive workflow (recommended)

Maximize data on unknown or hostile networks by chaining scans and adapting to results.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│  Discovery  │────▶│  Port scan   │────▶│ Service/OS  │────▶│     NSE     │
│  (-sn/-Pn)  │     │ (-sS/-sT/-p) │     │ (-sV/-O)    │     │ (--script)  │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │                    │
       └────────────────────┴────────────────────┴────────────────────┘
                         Each step: -oX stepN.xml
```

### Phase A — Discovery (low noise)

**Goal:** Live host list without port noise.

```bash
nmap -sn -oX discovery.xml 192.168.1.0/24
```

| Situation | Adjust |
|-----------|--------|
| ICMP blocked | `-Pn` then light port probe on common ports |
| Local Ethernet | `-PR` ARP discovery (default on /24 LAN) |
| Large subnet | Split CIDR, use `-T4` or `--min-rate` |

Parse `discovery.xml`: emit `IP_ADDRESS` for `status state="up"`.

### Phase B — Port scan

**Goal:** Open TCP (and optionally UDP) ports on live hosts.

```bash
nmap -sS -p- -T4 --open -oX ports.xml -iL live_hosts.txt
```

| Situation | Adjust |
|-----------|--------|
| No raw socket (Windows unprivileged) | `-sT` connect scan |
| Firewall drops SYN | `-sA` ACK map rules, or `-sT` |
| Time budget | `-F` (100 ports), `--top-ports 1000`, or `-p 22,80,443,...` |
| UDP services | `-sU --top-ports 100` (slow) |

Parse: `TCP_PORT_OPEN` / `UDP_PORT_OPEN` for `state="open"` only unless policy includes `open|filtered`.

### Phase C — Service and OS

**Goal:** Product/version strings and OS family.

```bash
nmap -sV -O --osscan-limit -p "$(paste -sd, open_ports.txt)" -oX detail.xml target
```

| Situation | Adjust |
|-----------|--------|
| Version unknown | `--version-intensity 9` |
| OS unreliable | Check `accuracy` in XML; require `>= 90` before `OPERATING_SYSTEM` |
| Many ports open | `--osscan-limit` (only open ports for OS probes) |

Parse: `SOFTWARE_USED`, `OPERATING_SYSTEM`, `TCP_PORT_OPEN_BANNER` from `service` attributes.

### Phase D — NSE enrichment

**Goal:** Vuln hints, HTTP titles, SSL certs, SMB shares.

```bash
nmap -sV --script "default,safe" -p 22,80,443,445 -oX nse.xml target
nmap --script vuln -p 80,443 -oX vuln.xml target
```

| Situation | Adjust |
|-----------|--------|
| Safe only | `--script "default,safe"` |
| Specific protocol | `--script "http-*"`, `ssl-cert`, `smb-os-discovery` |
| Aggressive | `intrusive` category — operator approval only |

Parse: map `script` output to nuggets per [nugget-mapping.md](nugget-mapping.md).

## Timing templates

| Flag | Profile | When |
|------|---------|------|
| `-T0` | Paranoid | IDS evasion, very slow |
| `-T1` | Sneaky | Stealth priority |
| `-T2` | Polite | Low bandwidth impact |
| `-T3` | Normal | Default |
| `-T4` | Aggressive | Fast LAN / authorized pentest |
| `-T5` | Insane | Lab only; may lose accuracy |

Fine-tune: `--min-rate 100`, `--max-retries 1`, `--host-timeout 5m`.

## Target specification patterns

```bash
nmap -oX out.xml 192.168.1.1                    # single IP
nmap -oX out.xml 192.168.1.0/24                   # CIDR
nmap -oX out.xml 10.0.0.1-10.0.0.50               # range
nmap -oX out.xml -iL targets.txt                  # list file
nmap -oX out.xml example.com                      # DNS resolution
nmap -oX out.xml -p 80,443 192.168.1.0/24         # specific ports only
```

Exclude: `--exclude 192.168.1.1` or `--excludefile exclude.txt`.

## Scan technique selection

| Technique | Flag | Needs root | Typical use |
|-----------|------|------------|-------------|
| SYN (half-open) | `-sS` | Yes (Unix) | Default fast TCP |
| Connect | `-sT` | No | Windows / unprivileged |
| UDP | `-sU` | Yes | DNS, SNMP, DHCP |
| ACK | `-sA` | Yes | Firewall rule mapping |
| Null/FIN/Xmas | `-sN`, `-sF`, `-sX` | Yes | RFC 793 anomalies |
| Idle (zombie) | `-sI zombie` | Yes | Maximum stealth |

## Multi-stage file handoff

```bash
# Extract live IPs from discovery.xml (Python or xpath), write live_hosts.txt
nmap -sn -oX discovery.xml 10.0.0.0/24
python scripts/nmap_live_hosts.py discovery.xml > live_hosts.txt
nmap -sS --open -p- -oX ports.xml -iL live_hosts.txt
```

Keep each `-oX` as provenance. Merge into one nugget graph in Python, not by editing XML by hand.

## Decision matrix after each phase

| Observation | Next action |
|-------------|-------------|
| 0 hosts up | Retry with `-Pn -p 80,443,22`; check target spec |
| All ports filtered | Evasion: `-sT -f`, `--data-length 25`, different source port `-g 53` |
| Many open ports | Narrow NSE to relevant scripts; split by port groups |
| `osscan` no match | Rely on `-sV` `ostype` and NSE `smb-os-discovery` |
| Scan timeout | Reduce scope, `-T4`, `--host-timeout`, fewer ports |
| XML `exit="error"` in runstats | Read stderr; fix privileges, syntax, or targets |

## SpiderFeet integration notes

- Legacy `sfp_tool_nmap` uses `-O --osscan-limit` and parses **text** stdout — new work should use **XML** and the nugget mapping layer.
- Always store raw XML path in module provenance for audit replay.
- For netblocks: respect `netblockscanmax` policy (see module opts); prefer discovery before full `-p-` on /16+.

## Quick reference commands

```bash
# Minimal OSINT footprint (single host)
nmap -sV -O --osscan-limit -oX host.xml 203.0.113.10

# Network inventory
nmap -sn -oX live.xml 192.168.0.0/24 && nmap -sS -sV -O --open -oX detail.xml -iL live_ips.txt

# Web-focused
nmap -sV -p 80,443,8080,8443 --script "http-title,ssl-cert" -oX web.xml target

# Full TCP + top UDP (authorized assessment)
nmap -sS -p- -sV -O -sU --top-ports 100 -oX full.xml target
```
