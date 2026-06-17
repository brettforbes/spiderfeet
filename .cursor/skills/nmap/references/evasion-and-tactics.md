# Nmap Evasion and Hostile-Network Tactics

Use when scans return all `filtered`, zero hosts `up`, incomplete `service` data, or IDS alerts. Always stay within **authorized scope** — these techniques exist for legitimate assessment and OSINT on networks you may probe.

Reference: https://nmap.org/book/man-bypass-firewalls-ids.html

## Symptoms and first responses

| Symptom in XML | Likely cause | First tactic |
|----------------|--------------|--------------|
| `status state="down"` for known live IP | ICMP blocked | `-Pn` |
| All ports `filtered` | Stateful firewall | `-sT`, reduce rate `-T2`, `-f` |
| `open\|filtered` on UDP | Normal UDP ambiguity | `-sU` rescan with `--reason` |
| Missing `service` names | `filtered` or no `-sV` | Rescan open ports with `-sV --version-intensity 9` |
| No `os` section | No open TCP for fingerprint | Open at least one TCP port; `--osscan-guess` |
| Truncated scan / timeouts | Rate limiting | Lower parallelism, `--scan-delay`, `-T1` |

## Host discovery evasion

### Skip ping (`-Pn`)

Treat all targets as up — essential when ICMP echo is dropped.

```bash
nmap -Pn -sS -p 22,80,443,8443 -oX pn.xml target
```

Cost: scans every host in range even if dead.

### ARP on LAN (`-PR`)

On local Ethernet, ARP often works when ICMP does not. Default on many local scans; explicit:

```bash
nmap -PR -sn -oX arp.xml 192.168.1.0/24
```

### TCP/UDP ping

```bash
nmap -PS80,443 -PA443 -PU53 -sn -oX tcp_ping.xml target
```

| Flag | Meaning |
|------|---------|
| `-PS` | SYN ping to ports |
| `-PA` | ACK ping |
| `-PU` | UDP ping |

### Slow discovery

```bash
nmap -sn -T1 --scan-delay 1s -oX slow_disc.xml 10.0.0.0/24
```

## Port scan evasion

### Fragmentation (`-f`, `--mtu`)

Split probes into tiny packets to confuse simple ACLs and IDS.

```bash
nmap -f -sS -p 22,80,443 -oX frag.xml target
nmap --mtu 16 -sS -p 80,443 -oX mtu.xml target
```

### Decoy scans (`-D`)

Mix attacker IP with decoys (RND or specified).

```bash
nmap -D RND:10 -sS -p 22,80 -oX decoy.xml target
nmap -D 192.168.1.5,ME,192.168.1.7 -sS -p 80 -oX decoy2.xml target
```

`ME` = your real IP position in list.

### Source port manipulation (`-g`, `--source-port`)

Firewalls often allow `53/udp` or `20/tcp`:

```bash
nmap -g 53 -sS -p 80,443 -oX src53.xml target
```

### Idle scan (`-sI zombie`)

Uses a third-party zombie host — advanced; zombie must meet IP ID predictability requirements.

```bash
nmap -sI zombie.example.com:80 -p 22,80 -oX idle.xml target
```

### ACK scan for firewall mapping (`-sA`)

Does not find open ports reliably; maps **filtered vs unfiltered**:

```bash
nmap -sA -p 1-1024 -oX ackmap.xml target
```

### Connect scan (`-sT`)

Completes TCP handshake — slower, logged more, but works without raw sockets and through some proxies.

```bash
nmap -sT -p 22,80,443 -oX connect.xml target
```

## Timing and noise reduction

```bash
nmap -T0 -sS -p 22,80 --max-retries 1 --scan-delay 500ms -oX quiet.xml target
nmap --min-rate 50 --max-rate 100 -sS -p- -oX capped.xml target
```

| Flag | Effect |
|------|--------|
| `-T0`–`-T1` | Slower, less conspicuous |
| `--scan-delay` | Fixed delay between probes |
| `--max-retries` | Fewer retransmits |
| `--host-timeout` | Abandon slow hosts |
| `--max-parallelism` | Cap concurrent probes |

## Spoofing (advanced, often blocked)

```bash
nmap -S spoofed.ip -e eth0 -Pn -sS -p 80 target   # requires L2 adjacency
nmap --proxies socks4://127.0.0.1:9050 -sT -p 80 target
```

Spoofed source rarely works across routed internet; document as `Blocked` when unavailable.

## NSE under filtering

When ports are open but scripts fail:

```bash
nmap -sV -p 443 --script ssl-cert,ssl-enum-ciphers -oX ssl.xml target
nmap -p 80 --script http-headers,http-title --script-args http.useragent="Mozilla/5.0" -oX http.xml target
```

Use `--script-timeout` and `--script-args` to reduce hung scripts.

## Adaptive escalation ladder

Apply in order; stop when data quality suffices:

1. **Baseline:** `-sS -sV -O -oX baseline.xml`
2. **No hosts:** add `-Pn`
3. **All filtered:** `-sT -T2 -p common_ports`
4. **Still filtered:** `-f` or `--mtu 24`
5. **IDS suspected:** `-T1`, `--scan-delay`, `-D RND:5`
6. **LAN:** `-PR`, `-sn` first
7. **Service gaps:** `--version-intensity 9`, NSE `banner`
8. **OS gaps:** `--osscan-guess`, `smb-os-discovery`, `http-server-header`

Record each attempt's XML separately for comparison.

## Data-quality guardrails

- Do not treat `open|filtered` as confirmed open without corroboration.
- Decoy and idle scans may produce **incomplete** XML — note confidence in nugget metadata.
- Aggressive NSE (`intrusive`, `vuln`) may crash fragile services — use `safe` first.
- Evasion increases duration; set `--host-timeout` on wide nets.

## XML signals for tactic success

| XML change | Interpretation |
|------------|----------------|
| `status` `up` after `-Pn` | Host was icmp-blocked |
| `open` ports appear with `-sT` | SYN filtered, connect allowed |
| `reason` changes to `syn-ack` | Probe path improved |
| `service@conf` increases | Version detection succeeded |
| `osmatch@accuracy` ≥ 90 | Reliable OS nugget candidate |

## Combining with workflow phases

See [workflows-and-phases.md](workflows-and-phases.md). Evasion is **per-phase**: discovery may need `-PS` while port scan needs `-f`. Do not reuse one command for all phases on hostile networks.
