# NetDiscover Zero to Hero

A guided path from first install to orchestrated LAN discovery, TextFSM parsing, and handoff to Nmap and Nerva for service fingerprinting.

## What Netdiscover does

Netdiscover is an **ARP-based** active/passive reconnaissance tool. It finds **live IPv4 hosts on your local Layer-2 segment** by sending or observing ARP traffic. It returns **IP, MAC, and vendor (OUI)** — not open ports or application banners.

Use it when:

- You are on the same broadcast domain as targets (typical office/Wi-Fi/Lab VLAN)
- You need fast host inventory with hardware hints
- ICMP/TCP host discovery is filtered but ARP still works

Do **not** rely on it for routed remote networks.

---

## Level 0 — Install and verify

### Linux (Debian/Ubuntu/Kali)

```bash
sudo apt update && sudo apt install netdiscover
netdiscover -h
```

### Fedora

```bash
sudo dnf install netdiscover
```

### macOS

```bash
brew install netdiscover
```

### Requirements

- Root or `CAP_NET_RAW`
- A connected interface with an IP on the target subnet

```bash
ip -br addr    # pick interface name for -i
```

---

## Level 1 — First scan (interactive)

Active scan of a /24:

```bash
sudo netdiscover -r 192.168.1.0/24
```

You will see a live table. Keys: `j`/`k` scroll, `q` quit.

Passive listen (no transmitted ARP):

```bash
sudo netdiscover -p -i eth0
```

Wait for traffic; only hosts that exchange ARP appear.

---

## Level 2 — Machine-readable output

For scripts and SpiderFeet, always use **parseable mode**:

```bash
sudo netdiscover -P -N -r 192.168.1.0/24
```

Example line:

```
192.168.1.100   08:00:27:53:81:2b       1       60      PCS Systemtechnik GmbH
```

Columns: IP, MAC, packet count, frame length, vendor.

Save to file:

```bash
sudo netdiscover -P -N -r 192.168.1.0/24 > /tmp/netdiscover.out
```

---

## Level 3 — Choose the right mode

| Situation | Command |
|-----------|---------|
| Known subnet | `netdiscover -P -N -r 192.168.1.0/24` |
| Multiple subnets | `netdiscover -P -N -l ranges.txt` |
| Unknown layout | `netdiscover -P -N -f` (fast) then full `-r` |
| Stealth | `netdiscover -p -i eth0` |
| Lossy Wi-Fi | add `-c 3 -s 50` |
| Wrong source IP | add `-n 200` |

See [NetDiscover-CLI-Options.md](NetDiscover-CLI-Options.md) for every flag.

---

## Level 4 — TextFSM parsing

Netdiscover output is **text**, not JSON. SpiderFeet uses TextFSM templates.

1. Capture `-P` stdout
2. Parse with `netdiscover_parsable.textfsm` (see `.cursor/skills/netdiscover/references/output-and-parsing.md`)
3. Map rows to nuggets: `IP_ADDRESS`, `MAC_ADDRESS`, vendor metadata

```python
import textfsm
from pathlib import Path

with Path("netdiscover_parsable.textfsm").open() as f:
    fsm = textfsm.TextFSM(f)
rows = fsm.ParseTextToDicts(open("/tmp/netdiscover.out").read())
```

Skill: `.cursor/skills/textfsm/SKILL.md`

---

## Level 5 — Combine with Nmap

Netdiscover finds **who is alive**; Nmap finds **what ports are open**.

### Recommended sequence (local LAN)

```bash
# 1. ARP host discovery
sudo netdiscover -P -N -r 192.168.1.0/24 | awk '{print $1}' | sort -u > ips.txt

# 2. Optional ARP ping cross-check
nmap -sn -PR -iL ips.txt -oG - | awk '/Up$/{print $2}' > ips_confirmed.txt

# 3. Port scan live hosts
nmap -p- --open -T4 -iL ips_confirmed.txt -oG ports.gnmap
```

### When to prefer Nmap for host discovery

- Targets are **remote** (across a router)
- You need ICMP/TCP/sCTP host probes
- Netdiscover is not installed

---

## Level 6 — Full pipeline to Nerva

Service fingerprinting belongs to **Nerva**, not netdiscover.

```bash
# Build host:port list from Nmap greppable output
awk '/\/open\//{
  ip=$2
  gsub(/.*Ports: /,"")
  n=split($0,a,",")
  for(i=1;i<=n;i++){
    split(a[i],f,"/")
    if(f[2]=="open") print ip":"f[1]
  }
}' ports.gnmap > targets.txt

# Fingerprint each open port
nerva -l targets.txt --json -o fingerprints.jsonl
```

Each JSON line describes protocol, transport, and metadata (versions, tech stack, etc.).

Skill: `.cursor/skills/nerva/SKILL.md`

---

## Level 7 — Orchestrated playbook

### Playbook A — Quick lab inventory

1. `netdiscover -P -N -r 192.168.1.0/24`
2. TextFSM → nuggets
3. `nmap -F --open` on discovered IPs (fast ports)
4. `nerva --json` on results

### Playbook B — Large corporate /16

1. `netdiscover -f -P -N -r 10.0.0.0/16` — find occupied /24s
2. Full `netdiscover -P -N -r 10.0.0.42.0/24` per hit
3. Nmap deep port scan on each /24 host set
4. Nerva on all open ports

### Playbook C — Stealth-first

1. Passive `netdiscover -p` for 10–30 minutes
2. If insufficient, narrow active `-r` on observed subnet only
3. Continue with Nmap/Nerva on confirmed IPs

### Playbook D — Continuous monitoring

```bash
sudo netdiscover -P -L -r 192.168.1.0/24
```

Stream parseable lines; emit nuggets as new hosts appear.

---

## Defensive / constrained networks

| Challenge | Response |
|-----------|----------|
| ARP monitoring | Prefer passive `-p`; limit active to off-hours |
| Sparse results | Increase `-c`, slow `-s`, drop `-S` |
| VLAN isolation | Run netdiscover **inside** each VLAN |
| Randomized MACs | Keep IP/MAC nuggets; treat vendor as untrusted |

---

## Configuration files

`~/.netdiscover/ranges` — auto-scan CIDR list  
`~/.netdiscover/fastips` — last-octets for `-f` mode

Override defaults with `-d`.

---

## Further reading

| Topic | Location |
|-------|----------|
| Agent skill | `.cursor/skills/netdiscover/SKILL.md` |
| CLI reference | [NetDiscover-CLI-Options.md](NetDiscover-CLI-Options.md) |
| TextFSM template | `.cursor/skills/netdiscover/references/output-and-parsing.md` |
| Tactics | `.cursor/skills/netdiscover/references/tactics.md` |
| Nerva pipeline | [Nerva-Zero-to-Hero.md](Nerva-Zero-to-Hero.md) |

---

## Authorization reminder

Only scan networks you are permitted to test. Active ARP generates broadcast traffic visible to defenders.
