# Naabu CLI Options

Complete command-line reference for ProjectDiscovery Naabu port scanner.

**Binary:** `naabu`  
**Install:** https://github.com/projectdiscovery/naabu/releases  
**Prerequisite:** libpcap (Linux/macOS) or Npcap (Windows) for SYN scans

---

## Synopsis

```
naabu [flags]
```

Hosts via `-host`, `-list`, or stdin (unless `-no-stdin`).

---

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-host` | — | Comma-separated hosts (IP, CIDR, domain) |
| `-list` | `-l` | Host list file |
| `-exclude-hosts` | `-eh` | Hosts to exclude |
| `-exclude-file` | `-ef` | Exclude file |

```bash
naabu -host scanme.sh
naabu -host 192.168.1.0/24,10.0.0.1
naabu -l targets.txt
echo scanme.sh | naabu
echo AS15169 | naabu -p 443
```

---

## PORT

| Flag | Short | Description |
|------|-------|-------------|
| `-port` | `-p` | Ports (`80,443`, `1-1000`, `u:53`, `-` for all) |
| `-top-ports` | `-tp` | `100`, `1000`, `full` |
| `-exclude-ports` | `-ep` | Excluded ports |
| `-ports-file` | `-pf` | Port list file |
| `-port-threshold` | `-pts` | Skip host if too many ports open |
| `-exclude-cdn` | `-ec` | CDN hosts: scan 80,443 only |
| `-display-cdn` | `-cdn` | Show CDN name |

```bash
naabu -host scanme.sh -p 22,80,443
naabu -host scanme.sh -top-ports 1000
naabu -host scanme.sh -p -
naabu -host scanme.sh -p u:53,u:161 -uP
```

---

## RATE-LIMIT

| Flag | Default | Description |
|------|---------|-------------|
| `-c` | 25 | Worker threads |
| `-rate` | 1000 | Packets per second |

```bash
naabu -host 10.0.0.0/24 -rate 400 -c 15
```

---

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | Output file |
| `-json` | `-j` | JSON Lines (**use for SpiderFeet**) |
| `-csv` | — | CSV format |
| `-silent` | — | Results only |
| `-no-color` | `-nc` | No ANSI colors |
| `-verbose` | `-v` | Verbose |

```bash
naabu -host scanme.sh -json -o ports.jsonl
naabu -host scanme.sh -json -silent
```

---

## SERVICES-DISCOVERY

| Flag | Short | Description |
|------|-------|-------------|
| `-service-discovery` | `-sD` | Service name by port |
| `-service-version` | `-sV` | Version via nmap-service-probes |
| `-sV-fast` | — | Fast version mode |
| `-sV-timeout` | — | Probe timeout |
| `-sV-workers` | — | Version worker count |
| `-sV-probes` | — | Custom probes file |
| `-udp-probes` | `-uP` | UDP payloads from probes DB |

---

## CONFIGURATION (selected)

| Flag | Short | Description |
|------|-------|-------------|
| `-config` | — | Config YAML path |
| `-scan-all-ips` | `-sa` | Scan all DNS A/AAAA |
| `-ip-version` | `-iv` | `4`, `6`, or both |
| `-scan-type` | `-s` | `s` SYN, `c` CONNECT |
| `-connect-payload` | `-cp` | Custom UDP payload |
| `-nmap-cli` | — | Run Nmap on results |
| `-passive` | — | Shodan InternetDB |
| `-stream` | — | Stream mode |
| `-resume` | — | Resume scan |
| `-proxy` | — | SOCKS5 proxy |
| `-no-stdin` | — | Disable stdin input |

```bash
naabu -host scanme.sh -s s -json
naabu -host example.com -passive -json
naabu -host scanme.sh -nmap-cli 'nmap -sV'
```

---

## HOST-DISCOVERY

| Flag | Short | Description |
|------|-------|-------------|
| `-host-discovery` | `-sn` | Discovery only |
| `-with-host-discovery` | `-wn` | Discover before scan |
| `-probe-tcp-syn` | `-ps` | TCP SYN ping |
| `-probe-tcp-ack` | `-pa` | TCP ACK ping |
| `-probe-icmp-echo` | `-pe` | ICMP echo |
| `-arp-ping` | `-arp` | ARP (LAN) |
| `-nd-ping` | `-nd` | IPv6 ND |
| `-rev-ptr` | — | Reverse PTR |

```bash
naabu -host 192.168.1.0/24 -sn
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 443 -json
```

---

## OPTIMIZATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-retries` | — | 3 | Scan retries |
| `-timeout` | — | 1000 | Timeout (ms) |
| `-verify` | — | — | Re-verify open ports |
| `-smart-scan` | `-ss` | — | Predictive ports |
| `-prediction-threshold` | `-pt` | 20 | Smart scan threshold % |

---

## DEBUG / METRICS

| Flag | Description |
|------|-------------|
| `-health-check` / `-hc` | Diagnostics |
| `-debug` | Debug mode |
| `-version` | Version string |
| `-metrics-port` / `-mp` | Metrics HTTP (default 63636) |

---

## UPDATE / CLOUD

| Flag | Description |
|------|-------------|
| `-update` / `-up` | Self-update |
| `-disable-update-check` / `-duc` | Skip update check |
| PDCP flags | ProjectDiscovery cloud upload (optional) |

---

## Common recipes

```bash
# Standard recon
naabu -host TARGET -top-ports 1000 -json -silent

# Root SYN
sudo naabu -host TARGET -s s -top-ports 1000 -json

# Subdomain sweep
subfinder -d example.com -silent | naabu -json -silent | httpx -silent

# Service versions
naabu -host scanme.sh -sV -json

# LLM port sweep
naabu -host corp.internal -p 11434,8000,8080,7860,4000 -json -silent
```

---

## Related documentation

| Resource | Path |
|----------|------|
| Agent skill | `.cursor/skills/naabu/SKILL.md` |
| Reference index | `.cursor/skills/naabu/references/SKILLS.md` |
| ProjectDiscovery running guide | https://docs.projectdiscovery.io/opensource/naabu/running |
| Zero to Hero | `Naabu-Zero-to-Hero.md` |
