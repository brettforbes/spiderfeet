# Nmap — Exploration Report

**Date:** 2026-06-23  
**Phase:** Exploration (pre–formal examination)  
**Runtime:** Windows, Nmap 7.80 (`C:\Program Files (x86)\Nmap\nmap.exe`)  
**Scan technique:** `-sT` (TCP connect) — no raw-socket admin on this host; `-sS`/full `-O` need elevation or Linux/WSL for parity.

## Targets exercised

| Class | Target | Result |
|-------|--------|--------|
| Permissive | `scanme.nmap.org` (45.33.32.156) | Rich: open/filtered TCP, versions, OS via `-A`, NSE, UDP states, traceroute |
| Corporate | `bbc.co.uk` (151.101.128.81) | Sparse: mostly **filtered** ports; 80/443 open only on top-10 |
| Local L2 | `192.168.1.0/24` | 2 hosts up (.12, .16); Windows SMB/RPC/http-alt pattern |

Scratch XML/text artifacts: `.docs/docs-for-cli-tools/exploration_scratch/nmap/` (not formal examination evidence).

---

## Results by scan class

### 1. Host discovery (`-sn`)

**scanme.nmap.org**
```
Host is up (0.15s latency).
Other addresses (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
```

**192.168.1.0/24** — 2/256 hosts up: `192.168.1.12`, `192.168.1.16`

**Semantics:** `host/status@up`, IPv4 `address`, `hostname`, alternate IPv6 in text, latency — **no ports**.

---

### 2. Port scanning (`-sT --top-ports`)

**scanme** — open: `22/ssh`, `80/http`, `9929/nping-echo`, `31337/Elite`; ~996 filtered (not shown with `--open`).

**bbc.co.uk** — open: `80`, `443`; remainder **filtered** on top-10.

**192.168.1.0/24** — per host: `135`, `139`, `445`, `8000` open.

**Semantics:** `port/state` = `open` → `TCP_PORT_OPEN`; `filtered` → **not** an open-port nugget (record separately); `closed` rare on scanme UDP.

---

### 3. Service / application version (`-sV`)

**scanme** (ports 22,80,443,9929):
| Port | Service | Product / version |
|------|---------|-------------------|
| 22 | ssh | OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 |
| 80 | http | Apache httpd 2.4.7 |
| 443 | filtered | — |
| 9929 | nping-echo | Nping echo |

**Semantics:** `service@name`, `@product`, `@version`, `@extrainfo`, `@tunnel`, CPE — map to `SOFTWARE_USED` / banners under open ports.

---

### 4. Remote OS detection (`-O` / `-A`)

| Command | scanme OS in XML? | Notes |
|---------|-------------------|-------|
| `-O --osscan-limit` only | **No** `osmatch` | Ports listed; text says "OS detection performed" but no guess |
| `-A` (with `-sV`) | **Yes** — Linux 2.6.x matches (acc 90–94) | Reliable OS semantics on permissive target |

**192.168.1.12** with `-sV -O -A`: no `osmatch` in XML; **Service Info: OS: Windows** + SMB NSE (`smb2-time`, `smb2-security-mode`).

**Conclusion:** On Windows connect scans, use **`-A`** (or `-sV` + NSE `smb-os-discovery` on 445) for OS archetype — not standalone `-O` alone.

---

### 5. NSE / scripts (`-sC`)

**scanme** (`-sC -p 22,80,443`): `ssh-hostkey`, `http-title` on open ports.

**local .12**: `fingerprint-strings`, `http-title`, `clock-skew`, `smb2-*` — rich **script table** output (distinct from port/service rows).

---

### 6. UDP (`-sU --top-ports 20`)

**scanme:** `udp/123 open ntp`; many `open|filtered`; some `closed` (53, 162).

**Semantics:** distinct from TCP — `open|filtered` needs policy (low confidence or separate descriptor); only confirmed `open` → `UDP_PORT_OPEN`.

---

### 7. Traceroute (`--traceroute`)

**scanme → port 80:** 13 hops with ISP hostnames and IPs (e.g. `eqix-sv1.linode.com`, final `scanme.nmap.org`).

**Semantics:** hop `address`, RTT, `hostname` — trace path / intermediate `IP_ADDRESS` + `INTERNET_NAME` (ontology: under trace/host hierarchy).

---

### 8. Skip ping (`-Pn`)

**scanme `-Pn -p80`:** host treated up; port 80 open in 0.44s.

**Semantics:** same as port scan but documents **no ICMP host-discovery phase** — relevant when discovery returns 0 hosts.

---

### 9. All-in-one (`-A`)

Combines **version + OS + default NSE** in one run (~24s on scanme for 22,80,443). Best single command for permissive enrichment after discovery.

---

## Semantic output classes (archetypes)

Distinct XML/text shapes that need separate formal scenarios:

| # | Archetype | Minimal command pattern | Key nugget semantics |
|---|-----------|-------------------------|----------------------|
| A | Host discovery (single) | `-sn -oX - <host>` | IP, hostname, up/down, IPv6 hint |
| B | Host discovery (subnet) | `-sn -oX - <cidr>` | Multiple hosts; mostly empty port sections |
| C | TCP port scan | `-sT --top-ports N --open -oX -` | `TCP_PORT_OPEN`, service name only |
| D | Filtered-heavy (corporate) | `-sT --top-ports N -oX - <corp>` | Mostly `filtered`; few opens |
| E | Service version | `-sT -sV -p <ports> -oX -` | `SOFTWARE_USED`, product/version |
| F | OS fingerprint | `-sT -A -p <ports> -oX -` | `OPERATING_SYSTEM` / `osmatch` |
| G | NSE default | `-sT -sC -p <ports> -oX -` | `script` tables, banners, keys |
| H | UDP ports | `-sU --top-ports N -oX -` | `UDP_PORT_OPEN`, `open\|filtered`, `closed` |
| I | Traceroute | `-sT --traceroute -p <port> -oX -` | Hop chain |
| J | Skip ping | `-sT -Pn -p <ports> -oX -` | Host up without prior `-sn` |
| K | Aggressive all-in-one | `-sT -A -p <ports> -oX -` | E+F+G combined |
| L | Local Windows enrich | `-sT -sV -A -p 135,445,8000 -oX - <lan-ip>` | Windows services + SMB scripts |

**Not in initial matrix (defer):** `-sS` SYN, idle scan, IPv6-only scan, `-p-` full range, `vuln` NSE, ARP `-PR` (local discovery already covered by `-sn` on /24).

---

## Refined command set (ready for formal examination)

Windows-safe; each scenario runs **twice** in examination (XML + text) per driving doc §2.2.1.

### Permissive — `scanme.nmap.org`

```bash
nmap -sn -T3 -oX - scanme.nmap.org
nmap -sT -T3 --top-ports 1000 --open -oX - scanme.nmap.org
nmap -sT -sV -T3 -p 22,80,443,9929,31337 -oX - scanme.nmap.org
nmap -sT -A -T3 -p 22,80,443 -oX - scanme.nmap.org
nmap -sT -sC -T3 -p 22,80,443 -oX - scanme.nmap.org
nmap -sU -T3 --top-ports 20 -oX - scanme.nmap.org
nmap -sT --traceroute -T3 -p 80 -oX - scanme.nmap.org
nmap -sT -Pn -T3 -p 80 -oX - scanme.nmap.org
```

### Corporate — `bbc.co.uk`

```bash
nmap -sn -T3 -oX - bbc.co.uk
nmap -sT -T3 --top-ports 20 -oX - bbc.co.uk
nmap -sT -sV -T3 -p 80,443 -oX - bbc.co.uk
```

### Local — `192.168.1.0/24` / `192.168.1.12`

```bash
nmap -sn -T3 -oX - 192.168.1.0/24
nmap -sT -T3 --top-ports 100 --open -oX - 192.168.1.0/24
nmap -sT -sV -A -T3 -p 135,445,8000 -oX - 192.168.1.12
```

### All-in-one (permissive capstone)

```bash
nmap -sT -A -T3 --top-ports 1000 --open -oX - scanme.nmap.org
```

---

## Gaps / follow-ups before examination

1. ~~Capture `nmap --help`~~ → `cli_help_text/nmap_cli_help_text.md` ✓
2. ~~Strategy skill~~ → `.strategy/nmap_strategy.skill` ✓
3. ~~Update manifest~~ `nmap.yaml` v2 ✓
4. ~~Formal harvest~~ — 30 bundles (15 scenario keys) ✓
5. **Next:** draft `nugget_structure/nmap_nugget_graph_structure.md` + proposed graphs
6. **Optional:** WSL run with `-sS -O` on scanme for privileged parity

---

## Exploration completeness

| Goal | Status |
|------|--------|
| Host discovery | Verified (scanme + /24) |
| Port scanning | Verified (open + filtered) |
| Service/version | Verified |
| OS detection | Verified via `-A` (not standalone `-O` on Windows) |
| Archetype matrix | Defined (A–L) |
| All-in-one | Verified (`-A` and capstone command proposed) |

**Recommendation:** Approve this report → proceed to formal examination plan + help text + strategy skill → harvest evidence bundles.
