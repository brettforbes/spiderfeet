# Nmap CLI Flags — Grouped Reference

Quick lookup for command composition. Full detail: `.docs/docs-for-cli-tools/NMAP-CLI-Options.md` and https://nmap.org/book/man.html

**Agent rule:** every invocation must include `-oX path.xml` (or `-oA basename`).

## Output (mandatory for agents)

| Flag | Description |
|------|-------------|
| `-oX file` | **XML output — parse this** |
| `-oN file` | Normal human-readable |
| `-oG file` | Grepable |
| `-oA base` | All formats: `base.xml`, `.nmap`, `.gnmap` |
| `-v` / `-vv` | Increase verbosity (stderr) |
| `-d` / `-dd` | Debug |
| `--reason` | Include port state reason in normal output (also in XML `reason`) |
| `--stats-every 30s` | Progress every N seconds |
| `--resume file` | Resume aborted scan |

## Target specification

| Flag / form | Example |
|-------------|---------|
| Single host | `scanme.nmap.org` |
| CIDR | `192.168.1.0/24` |
| Range | `10.0.0.1-50` |
| List | `-iL targets.txt` |
| Random | `-iR 100` (100 random IPs) |
| Exclude | `--exclude 1.2.3.4` |
| Exclude file | `--excludefile exclude.txt` |
| IPv6 | `-6` |

## Host discovery

| Flag | Description |
|------|-------------|
| `-sn` | Ping scan only (no port scan) |
| `-Pn` | Skip host discovery (treat all as up) |
| `-PS/PA/PU/PY/PO` | TCP SYN/ACK/UDP/SCTP/IP proto ping |
| `-PE` / `-PP` / `-PM` | ICMP echo, timestamp, netmask |
| `-PR` | ARP ping (LAN) |
| `-n` | No DNS resolution |
| `-R` | Always resolve DNS |
| `--dns-servers` | Custom resolvers |
| `--system-dns` | Use OS resolver |
| `--traceroute` | Trace path to host |
| `--resolve-all` | Resolve all IPs of a name |

## Port specification

| Flag | Description |
|------|-------------|
| `-p 22` | Single port |
| `-p 1-1024` | Range |
| `-p-` | All 65535 ports |
| `-p U:53,T:21-25,80` | UDP + TCP mix |
| `-F` | Fast (100 common ports) |
| `--top-ports N` | Top N from frequency DB |
| `-r` | Don't randomize port order |

## Scan techniques

| Flag | Technique |
|------|-----------|
| `-sS` | TCP SYN (default, needs root) |
| `-sT` | TCP connect |
| `-sU` | UDP scan |
| `-sA` | TCP ACK |
| `-sW` | TCP Window |
| `-sM` | TCP Maimon |
| `-sN` / `-sF` / `-sX` | Null / FIN / Xmas |
| `-sI host` | Idle scan |
| `-sO` | IP protocol scan |
| `-sY` / `-sZ` | SCTP INIT / COOKIE-ECHO |
| `-b FTP relay` | FTP bounce (deprecated/rare) |

## Service / version detection

| Flag | Description |
|------|-------------|
| `-sV` | Probe open ports for service/version |
| `--version-intensity 0-9` | Probe depth (default 7) |
| `--version-light` | Intensity 2 |
| `--version-all` | Intensity 9 |
| `--version-trace` | Debug version probes |

## OS detection

| Flag | Description |
|------|-------------|
| `-O` | Enable OS detection |
| `-O --osscan-limit` | Only fingerprint hosts with open+closed |
| `--osscan-guess` | Guess when unsure |
| `--max-os-tries` | Limit OS probe rounds |

## Timing and performance

| Flag | Description |
|------|-------------|
| `-T0` … `-T5` | Timing templates (paranoid → insane) |
| `--min-hostgroup` / `--max-hostgroup` | Parallel host batching |
| `--min-parallelism` / `--max-parallelism` | In-flight probes |
| `--min-rtt-timeout` / `--max-rtt-timeout` / `--initial-rtt-timeout` | RTT tuning |
| `--host-timeout` | Per-host cap |
| `--scan-delay` | Delay between probes |
| `--max-scan-delay` | Upper bound on delay |
| `--min-rate` / `--max-rate` | Packet rate caps |
| `--max-retries` | Probe retransmit limit |

## Firewall / IDS evasion

| Flag | Description |
|------|-------------|
| `-f` | Fragment packets |
| `--mtu N` | Custom MTU fragmentation |
| `-D decoy1,decoy2,...` | Decoy scan (`ME` for real IP) |
| `-S IP` | Spoof source IP |
| `-e iface` | Egress interface |
| `-g port` / `--source-port` | Fixed source port |
| `--data-length N` | Append random data to packets |
| `--data-string hex` | Append fixed payload |
| `--spoof-mac` | Spoof MAC |
| `--badsum` | Invalid checksum probes |
| `--proxies` | Chain via proxies |
| `--ttl N` | Set IP TTL |

## NSE (scripting engine)

| Flag | Description |
|------|-------------|
| `-sC` | Default scripts (= `--script=default`) |
| `--script name` | Run named scripts |
| `--script-args k=v` | Script arguments |
| `--script-args-file` | Args from file |
| `--script-trace` | Show script traffic |
| `--script-updatedb` | Update script DB |
| `--script-help` | Help for scripts |
| `--script-timeout` | Per-script limit |
| `--script-category` | Filter by category |

Categories: `auth`, `broadcast`, `brute`, `default`, `discovery`, `dos`, `exploit`, `external`, `fuzzer`, `intrusive`, `malware`, `safe`, `version`, `vuln`.

## Misc

| Flag | Description |
|------|-------------|
| `-6` | IPv6 scanning |
| `-A` | Aggressive: `-O -sV -sC --traceroute` |
| `--open` | Only show open ports (normal output) |
| `--packet-trace` | Log packets |
| `--iflist` | List interfaces |
| `--send-eth` / `--send-ip` | L2 vs L3 |
| `--privileged` / `--unprivileged` | Assume raw socket availability |
| `-V` | Version |
| `-h` | Help |

## Common composed profiles

```bash
# Safe recon single host
nmap -sV -sC -O --osscan-limit -oX recon.xml TARGET

# LAN discovery
nmap -sn -PR -oX lan.xml 192.168.1.0/24

# Stealth slow
nmap -sS -T2 -f --scan-delay 200ms -oX stealth.xml -p 22,80,443 TARGET

# Full assessment (authorized)
nmap -A -p- -sU --top-ports 100 -oX full.xml TARGET

# No root
nmap -sT -sV -p 1-10000 -oX nroot.xml TARGET
```

## Flag interactions to remember

- `-sn` disables port scan; `-p` has no effect.
- `-O` requires at least one open and one closed TCP port for best results.
- `-sU` with `-sS` lengthens scan significantly.
- `-A` implies aggressive timing; may combine with `-T4`.
- `-oX -` writes XML to stdout (useful for pipes; still XML).
