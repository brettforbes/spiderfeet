# Netdiscover Tactics

Workflows for maximizing host discovery on local segments and chaining into port/service identification.

## Passive vs active

| Dimension | Passive (`-p`) | Active (`-r` / `-l` / auto) |
|-----------|----------------|------------------------------|
| Transmits ARP | No | Yes |
| Detectability | Very low | Moderate (broadcast ARP) |
| Completeness | Only hosts with recent ARP traffic | Probes every IP in range |
| Duration | Indefinite (manual stop) | Bounded (finishes range) |
| Automation | Poor (TUI); use `-P -L` instead | Excellent with `-P -N` |
| Best for | Stealth, compliance, monitoring | Inventory, pentest mapping |

### When to start passive

- Rules of engagement forbid active probing
- You need to observe natural traffic before touching targets
- Wireless guest VLAN with ARP visible but ICMP filtered

### When to go active

- Time-boxed assessment needs full host list
- Passive yielded too few hosts after observation window
- Building definitive asset inventory for Nmap follow-up

### Hybrid pattern

```bash
# Phase 1: quick active parseable sweep
sudo netdiscover -P -N -r 192.168.10.0/24 -o /tmp/nd_phase1.txt

# Phase 2: passive tail for stragglers (optional)
sudo timeout 300 netdiscover -P -L -r 192.168.10.0/24 -o /tmp/nd_phase2.txt
```

Merge and dedupe IP sets before port scanning.

---

## Discovery depth ladder

```
1. Fast occupancy     netdiscover -f -P -N -r 10.0.0.0/16
2. Full subnet        netdiscover -P -N -r 10.0.0.42.0/24
3. L2 confirm         nmap -sn -PR 10.0.0.42.0/24
4. Port discovery     nmap -p- --open -T4 <ips>
5. Fingerprint        nerva --json -l targets.txt
```

Advance to the next step only when the previous step returns actionable targets.

---

## Netdiscover + Nmap combo

### Why both?

| Tool | Layer | Strength |
|------|-------|----------|
| Netdiscover | L2 ARP | Fast local sweep; MAC + OUI vendor |
| Nmap `-sn -PR` | L2/L3 | ARP on local; ICMP/TCP elsewhere |

### Complementary usage

**Netdiscover primary (local VLAN):**

```bash
sudo netdiscover -P -N -r 192.168.1.0/24 | tee hosts.txt
# Extract IPs → nmap port scan each
nmap -p- --open -T4 -iL ips.txt -oG nmap_ports.gnmap
```

**Nmap cross-check when netdiscover misses hosts:**

```bash
nmap -sn -PR 192.168.1.0/24 -oG - | awk '/Up$/{print $2}' > nmap_up.txt
```

Union `hosts.txt` IPs with `nmap_up.txt`.

**Nmap when netdiscover unavailable (remote netblock):**

```bash
nmap -sn 10.20.30.0/24   # no ARP across routers
```

Do not run netdiscover against remote routed ranges expecting results.

### Port scan handoff

Greppable Nmap → Nerva target list:

```bash
nmap -p- --open 192.168.1.0/24 -oG - | \
  grep '/open/' | \
  awk '{ip=$2; gsub(/.*Ports: /,"",$0); n=split($0,ports,",");
        for(i=1;i<=n;i++){split(ports[i],f,"/"); if(f[2]=="open") print ip":"f[1]}}' \
  > targets.txt

nerva -l targets.txt --json -o fingerprints.jsonl
```

---

## Full pipeline: L2 hosts → services

```mermaid
flowchart LR
  A[netdiscover -P -N] --> B[TextFSM rows]
  B --> C[IP nuggets]
  C --> D[nmap open ports]
  D --> E[host:port list]
  E --> F[nerva --json]
  F --> G[service nuggets]
```

1. **Netdiscover** — MAC, vendor, live IPv4 on segment
2. **TextFSM** — structured rows
3. **Nmap** — TCP/UDP open ports per IP
4. **Nerva** — protocol fingerprint + metadata JSON lines
5. **Nugget emit** — `TCP_PORT_OPEN`, banners, tech stack from Nerva `metadata`

---

## Adapting to defensive networks

| Symptom | Tactic |
|---------|--------|
| Few hosts vs expected | Increase `-c`; remove `-S`; try `-n` alternate source |
| ARP storm alerts | Switch to `-p`; widen passive window; smaller `-r` chunks with `-s` delay |
| Wrong subnet | `-f` sweep / auto-scan; verify `-i` interface and VLAN |
| MAC randomization | Still map IP; treat vendor as low confidence |
| Double NAT / guest isolation | No cross-segment ARP; scan from inside each VLAN |

---

## Timing and performance

| Scenario | Flags |
|----------|-------|
| Lab /24 full sweep | `-P -N -r 192.168.1.0/24` |
| Corporate /16 recon | `-f -P -N -r 10.0.0.0/16` then targeted /24 |
| Lossy Wi-Fi | `-c 3 -s 50` (no `-S`) |
| Maximum speed (risky) | `-S -s 0` on stable wired LAN |

---

## What not to do

- Do not treat netdiscover as a port scanner
- Do not parse interactive TUI for production nuggets
- Do not run active ARP across unauthorized networks
- Do not skip Nerva after Nmap — port numbers alone are insufficient for service ID

---

## Related docs

- [`cli-options.md`](cli-options.md)
- [`../../nerva/references/tactics.md`](../../nerva/references/tactics.md)
- [`.docs/docs-for-cli-tools/NetDiscover-Zero-to-Hero.md`](../../../.docs/docs-for-cli-tools/NetDiscover-Zero-to-Hero.md)
