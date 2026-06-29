# Naabu CLI Options

Full flag reference from Naabu v2.6.x (ProjectDiscovery). Run `naabu -h` on your install to confirm.

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-host` | — | Hosts to scan (comma-separated), repeatable |
| `-list` | `-l` | File with hosts (one per line) |
| `-exclude-hosts` | `-eh` | Hosts to exclude (comma-separated) |
| `-exclude-file` | `-ef` | File of hosts to exclude |

**Stdin:** pipe hosts unless `-no-stdin`.

```bash
naabu -host scanme.sh,example.com
naabu -l hosts.txt
echo scanme.sh | naabu
echo AS14421 | naabu -p 80,443
cat subs.txt | naabu -p 80,443 -json
```

## PORT

| Flag | Short | Description |
|------|-------|-------------|
| `-port` | `-p` | Ports: `80,443`, ranges `1-1000`, UDP `u:53`, full `-p -` |
| `-top-ports` | `-tp` | `100`, `1000`, or `full` (default top 100) |
| `-exclude-ports` | `-ep` | Ports to skip |
| `-ports-file` | `-pf` | Port list file |
| `-port-threshold` | `-pts` | Skip host if open port count exceeds threshold |
| `-exclude-cdn` | `-ec` | CDN/WAF hosts: scan only 80,443 |
| `-display-cdn` | `-cdn` | Show CDN provider in output |

```bash
naabu -host scanme.sh -p 22,80,443
naabu -host scanme.sh -p 1-65535
naabu -host scanme.sh -top-ports 1000
naabu -host scanme.sh -p u:53,u:161 -uP
naabu -host scanme.sh -p - -exclude-ports 80,443
naabu -host cdn.example.com -ec
```

## RATE-LIMIT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-c` | — | 25 | Internal worker threads |
| `-rate` | — | 1000 | Packets per second |

```bash
naabu -host 10.0.0.0/24 -rate 500
naabu -host corp.local -rate 200 -c 10
```

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-o` | `-output` | Write results to file |
| `-json` | `-j` | **JSON Lines** (required for agents) |
| `-csv` | — | CSV output |
| `-silent` | — | Results only (pipe-friendly) |
| `-nc` | `-no-color` | Disable colors |
| `-v` | `-verbose` | Verbose logging |

```bash
naabu -host scanme.sh -json -o out.jsonl
naabu -host scanme.sh -json -silent
naabu -host scanme.sh -csv -o out.csv
```

## SERVICES-DISCOVERY

| Flag | Short | Description |
|------|-------|-------------|
| `-sD` | `-service-discovery` | Map port number to service name |
| `-sV` | `-service-version` | nmap-service-probes version detection |
| `-sV-fast` | — | Port-hinted probes only (faster) |
| `-sV-timeout` | — | Probe timeout (default 5s) |
| `-sV-workers` | — | Concurrent version workers (default 25) |
| `-sV-probes` | — | Custom nmap-service-probes path |
| `-uP` | `-udp-probes` | UDP payloads from nmap-service-probes |

Requires local Nmap probe database for `-sV` / `-uP` (not shipped with naabu).

## CONFIGURATION

| Flag | Short | Description |
|------|-------|-------------|
| `-config` | — | Config YAML (default `$HOME/.config/naabu/config.yaml`) |
| `-scan-all-ips` | `-sa` | Scan all DNS A/AAAA for hostname |
| `-ip-version` | `-iv` | `4`, `6`, or both (default 4,6) |
| `-scan-type` | `-s` | `s` SYN or `c` CONNECT (default `c`) |
| `-source-ip` | — | Source IP:port |
| `-connect-payload` | `-cp` | Custom UDP CONNECT payload |
| `-interface-list` | `-il` | List interfaces |
| `-interface` | `-i` | Bind interface |
| `-nmap-cli` | — | Run nmap command on findings |
| `-r` | — | Custom DNS resolvers |
| `-proxy` | — | SOCKS5 proxy |
| `-proxy-auth` | — | SOCKS5 auth |
| `-dns-order` | — | `p/l/lp/pl` (default `l`) |
| `-system-resolver` | `-sr` | System DNS fallback |
| `-resume` | — | Resume from resume.cfg |
| `-stream` | — | Stream mode (disables resume, nmap, verify, etc.) |
| `-passive` | — | Shodan InternetDB passive ports (enables stream) |
| `-input-read-timeout` | `-irt` | Stdin read timeout |
| `-no-stdin` | — | Disable stdin |

```bash
naabu -host scanme.sh -s s -json
naabu -host scanme.sh -iv 6 -p 80
naabu -host scanme.sh -sa -p 80 -silent
naabu -host scanme.sh -passive -json
naabu -host scanme.sh -nmap-cli 'nmap -sV -oX nmap.xml'
```

## HOST-DISCOVERY

| Flag | Short | Description |
|------|-------|-------------|
| `-sn` | `-host-discovery` | Host discovery only |
| `-show-dead` | — | Show non-responding hosts (with discovery) |
| `-wn` | `-with-host-discovery` | Enable host discovery before scan |
| `-ps` | `-probe-tcp-syn` | TCP SYN ping ports |
| `-pa` | `-probe-tcp-ack` | TCP ACK ping |
| `-pe` | `-probe-icmp-echo` | ICMP echo |
| `-pp` | `-probe-icmp-timestamp` | ICMP timestamp |
| `-pm` | `-probe-icmp-address-mask` | ICMP address mask |
| `-arp` | `-arp-ping` | ARP ping (LAN) |
| `-nd` | `-nd-ping` | IPv6 neighbor discovery |
| `-rev-ptr` | — | Reverse PTR on input IPs |

```bash
naabu -host 192.168.1.0/24 -sn
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json
```

## OPTIMIZATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-retries` | — | 3 | Port scan retries |
| `-timeout` | — | 1000 | Timeout ms |
| `-warm-up-time` | — | 2 | Seconds between phases |
| `-ping` | — | — | Ping verify hosts |
| `-verify` | — | — | TCP re-verify open ports |
| `-smart-scan` | `-ss` | — | Predictive port scan (not with stream) |
| `-prediction-threshold` | `-pt` | 20 | Smart scan confidence % |

## DEBUG / MISC

| Flag | Description |
|------|-------------|
| `-health-check` / `-hc` | Diagnostics |
| `-debug` | Debug output |
| `-version` | Version |
| `-metrics-port` / `-mp` | Metrics HTTP port (default 63636) |

## UPDATE / CLOUD (PDCP)

| Flag | Description |
|------|-------------|
| `-update` / `-up` | Update binary |
| `-disable-update-check` / `-duc` | Skip update check |
| `-auth`, `-auth-config` | ProjectDiscovery cloud auth |
| `-dashboard` / `-pd` | PDCP dashboard |
| `-dashboard-upload` / `-pdu` | Upload JSONL to dashboard |

Cloud flags optional; not required for local SpiderFeet workflows.
