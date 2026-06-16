---
name: nmap
description: Run Nmap network scans with adaptive discovery→port→service/OS→NSE workflows, capture -oX XML only, parse with ElementTree, and map hosts/ports/services to SpiderFeet nuggets (IP_ADDRESS, TCP_PORT_OPEN, OPERATING_SYSTEM). Use for nmap, port scan, OS fingerprint, host discovery, or NSE on authorized targets.
---

# Nmap — Network Scan to Nuggets

## Purpose

Use when an agent must **scan networks or hosts with Nmap**, adapt technique to hostile or filtered environments, capture **XML output only** (`-oX`), and convert results into SpiderFeet nugget nodes and edges.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized targets only (IP, CIDR, hostname). Note constraints (stealth, speed, invasive NSE).
2. **Plan phases** — Discovery → port scan → service/OS → NSE. See [workflows-and-phases.md](references/workflows-and-phases.md).
3. **Run discovery** — `nmap -sn -oX discovery.xml <targets>`; if 0 hosts, retry with `-Pn` and TCP ping ports.
4. **Port scan live hosts** — `-sS` (or `-sT` unprivileged) with appropriate `-p` / `--top-ports`; always `-oX ports.xml`.
5. **Enrich** — `-sV -O --osscan-limit` on hosts with open ports; `-oX detail.xml`.
6. **NSE** — `--script "default,safe"` or targeted scripts; `-oX nse.xml`.
7. **Parse XML** — `xml.etree.ElementTree`; never parse normal `-oN` text for automation.
8. **Map to nuggets** — Per [nugget-mapping.md](references/nugget-mapping.md): `IP_ADDRESS`, `TCP_PORT_OPEN`, `UDP_PORT_OPEN`, `OPERATING_SYSTEM`, `SOFTWARE_USED`, etc.
9. **Adapt** — If filtered/down/incomplete, apply [evasion-and-tactics.md](references/evasion-and-tactics.md); re-run phase with new flags; keep separate XML per attempt.
10. **Emit graph** — Return `nodes`, `edges` with provenance (`nmaprun@args`, xml path).

## If/Then Decision Rules

| If | Then |
|----|------|
| 0 hosts up in XML | Retry with `-Pn`; then `-PS80,443 -sn` |
| All ports `filtered` | `-sT -T2`, `-f`, or `-g 53`; see evasion doc |
| No raw sockets / Windows user | `-sT` instead of `-sS` |
| Large netblock (/16+) | `-sn` first; never `-p-` whole net without list |
| `open\|filtered` on UDP | Do not emit `UDP_PORT_OPEN` without policy; rescan or mark low confidence |
| `osmatch@accuracy` < 90 | Skip `OPERATING_SYSTEM` or use NSE `smb-os-discovery` |
| Need version strings | Ensure `-sV`; raise `--version-intensity` |
| Operator wants vuln data | `--script vuln` on narrow port set; invasive = approval |
| Output is not XML | Re-run with `-oX`; do not use TextFSM on nmap text |
| Legacy `sfp_tool_nmap` parity | Same nugget types; switch parser to XML |

## Guardrails & Pitfalls

- **XML only** for agents — grep of human output is fragile; DTD is at nmap.org.
- **Authorization** — no scanning out-of-scope addresses; `invasive`/`exploit` NSE needs explicit approval.
- **`-A` / `-p-`** on wide nets — extreme time and noise; split phases.
- **Do not** emit closed/filtered ports as `TCP_PORT_OPEN`.
- **Duplicate scans** — dedupe by `ip:port` and seed id.
- **Privileges** — SYN/OS scan needs root/admin; document when falling back to `-sT`.
- **Rate** — `-T5` causes false negatives on lossy links.
- Store each `nmaprun@args` in provenance for audit.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `xml-output-schema.md` | Element/attribute reference |
| `workflows-and-phases.md` | Phase sequences |
| `evasion-and-tactics.md` | Hostile network tactics |
| `cli-flags.md` | Flag groups |
| `nugget-mapping.md` | XML → nuggets |
| `sources.md` | nmap.org URLs |

Operator guides: `.docs/docs-for-cli-tools/NMAP-Zero-to-Hero.md`, `NMAP-CLI-Options.md`.

## Comprehensive Examples

### Output (always include `-oX`)

```bash
nmap -oX scan.xml 192.168.1.1
nmap -oA scanbase 10.0.0.1          # parse scanbase.xml
nmap -oX - 192.168.1.1 > scan.xml   # stdout XML
```

### Target specification

```bash
nmap -sn -oX out.xml 192.168.1.0/24
nmap -oX out.xml 10.0.0.1-10.0.0.20
nmap -iL hosts.txt -oX out.xml
nmap -oX out.xml -6 2001:db8::1
nmap -oX out.xml --exclude 192.168.1.1 192.168.1.0/24
```

### Host discovery

```bash
nmap -sn -oX live.xml 192.168.1.0/24
nmap -Pn -oX assumeup.xml 203.0.113.0/24
nmap -PS22,80,443 -PA80 -sn -oX tcpping.xml 10.0.0.0/24
nmap -PR -sn -oX arp.xml 192.168.1.0/24
nmap -sn -n -oX nodns.xml 192.168.1.0/24
```

### Port specification

```bash
nmap -p 22,80,443 -oX ports.xml target
nmap -p 1-65535 -oX alltcp.xml target
nmap -F -oX fast.xml target
nmap --top-ports 1000 -oX top1k.xml target
nmap -p U:53,161,T:21-25,80,443 -sU -sS -oX mixed.xml target
```

### Scan techniques

```bash
nmap -sS -p 22,80,443 -oX syn.xml target
nmap -sT -p 1-10000 -oX connect.xml target
nmap -sU --top-ports 50 -oX udp.xml target
nmap -sA -p 1-1024 -oX ack.xml target
nmap -sN -p 22,80 -oX null.xml target
nmap -sI zombie:80 -p 22,80 -oX idle.xml target
```

### Service and version

```bash
nmap -sV -p 22,80,443 -oX sv.xml target
nmap -sV --version-intensity 9 -p 80,443 -oX sv9.xml target
nmap -sV --version-light -oX svlight.xml target
```

### OS detection

```bash
nmap -O --osscan-limit -oX os.xml target
nmap -O --osscan-guess -oX osguess.xml target
nmap -A -oX aggressive.xml target
```

### Timing

```bash
nmap -T4 -p 22,80,443 -oX t4.xml target
nmap -T2 --scan-delay 300ms -oX slow.xml target
nmap --min-rate 100 -p- -oX rate.xml target
nmap --host-timeout 120s -oX timeout.xml target
```

### Evasion

```bash
nmap -f -sS -p 80,443 -oX frag.xml target
nmap --mtu 24 -sS -p 443 -oX mtu.xml target
nmap -D RND:10 -sS -p 22,80 -oX decoy.xml target
nmap -g 53 -sS -p 80,443 -oX srcport.xml target
nmap --data-length 32 -sS -p 80 -oX pad.xml target
```

### NSE

```bash
nmap -sC -oX defaultscripts.xml target
nmap --script "default,safe" -p 22,80,443 -oX safe.xml target
nmap --script "http-title,ssl-cert" -p 80,443 -oX web.xml target
nmap --script vuln -p 80,443 -oX vuln.xml target
nmap --script smb-os-discovery -p 445 -oX smb.xml target
```

### DNS and traceroute

```bash
nmap -R --traceroute -oX trace.xml target
nmap -n -oX nodns.xml target
```

### IPv6

```bash
nmap -6 -sS -p 22,80,443 -oX v6.xml 2001:db8::1
```

### Python parse (minimal)

```python
import xml.etree.ElementTree as ET

root = ET.parse("scan.xml").getroot()
for host in root.findall("host"):
    if host.find("status").get("state") != "up":
        continue
    ip = next(a.get("addr") for a in host.findall("address") if a.get("addrtype") == "ipv4")
    for port in host.findall(".//port"):
        if port.find("state").get("state") == "open":
            print(ip, port.get("protocol"), port.get("portid"))
```

## Strategies and Tactics

### Maximize data on unknown networks

1. **Discover quietly** — `-sn` on CIDR; extract live IPs from XML.
2. **Scan open-only** — `--open` reduces noise in logs; XML still has state.
3. **Tier ports** — `--top-ports 1000` first; full `-p-` only on high-value hosts.
4. **Layer enrichment** — add `-sV` then `-O` then NSE per open port class (22→SSH scripts, 443→ssl/http).
5. **Compare XML runs** — if phase 2 finds nothing, escalate evasion before wider ports.

### Hostile / filtered network

1. Assume ICMP blocked: **always `-Pn`** after failed discovery.
2. Prefer **`-sT -T1`** over **`-sS -T4`** when SYN is filtered.
3. Use **fragmentation** and **decoys** only with scope approval (collateral noise).
4. Map firewall with **`-sA`** before wasting full connect scans.
5. Pull OS from **NSE** when `-O` fails (HTTP Server header, SMB).

### Speed vs depth (authorized assessment)

| Profile | Command pattern |
|---------|-----------------|
| Quick | `nmap -F -sV -oX q.xml` |
| Standard | `nmap -sS -sV -O --top-ports 1000 --open -oX s.xml` |
| Deep | `nmap -sS -p- -sV -O -sU --top-ports 100 -sC -oX d.xml` |

### SpiderFeet seed workflows

- Single `IP_ADDRESS` seed → `-sV -O --osscan-limit -oX` → `OPERATING_SYSTEM` + ports.
- `NETBLOCK_OWNER` → discovery on /24 max (module policy) → per-live-IP detail scan.
- Attach `source_module` and xml filename to every node for Tests tab replay.

### When to stop escalating

- Sufficient nuggets for investigation goal (e.g. web ports + titles only).
- `--host-timeout` exceeded repeatedly — shrink target list.
- `runstats/finished@exit=error` — fix privileges or syntax before blind retries.
