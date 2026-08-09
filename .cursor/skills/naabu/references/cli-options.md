# Naabu CLI Options

Grouped flag reference from live help for **naabu v2.6.1** (`C:\projects\spiderfeet\.tools\naabu\naabu.exe`, captured **2026-08-10**). Run `naabu -h` on your install to confirm. Do not invent flags.

Full exact help text: `.docs/docs-for-cli-tools/Naabu-CLI-Options.md` → **Captured help**.

**Windows:** Default scan type in this help is **`c` (CONNECT)**. SYN (`s`) requires privileges + Npcap; health-check may report `Privileged/NET_RAW: Ko`.

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-host` | — | Hosts to scan ports for (comma-separated) |
| `-list` | `-l` | List of hosts to scan ports (file) |
| `-exclude-hosts` | `-eh` | Hosts to exclude (comma-separated) |
| `-exclude-file` | `-ef` | List of hosts to exclude (file) |

Stdin is accepted unless `-no-stdin`. ASN input via stdin is supported by PD Running docs (`echo AS14421 | naabu …`).

```bash
naabu -host scanme.nmap.org -json -silent -duc
naabu -l hosts.txt -json -silent -duc
echo scanme.nmap.org | naabu -json -silent -duc
```

## PORT

| Flag | Short | Description |
|------|-------|-------------|
| `-port` | `-p` | Ports to scan (`80,443`, `100-200`) |
| `-top-ports` | `-tp` | Top ports (default `100`) — `[full,100,1000]` |
| `-exclude-ports` | `-ep` | Ports to exclude (file or comma-separated) |
| `-ports-file` | `-pf` | List of ports to scan (file or comma-separated) |
| `-port-threshold` | `-pts` | Port threshold to skip port scan for the host |
| `-exclude-cdn` | `-ec` | Skip full port scans for CDN/WAF (only 80,443) |
| `-display-cdn` | `-cdn` | Display CDN in use |

Official Running docs also document: full range via `-p -`, and UDP ports as `u:port` (e.g. `u:53`). Prefer `-top-ports full` when staying within help enum.

```bash
naabu -host scanme.nmap.org -p 22,80,443 -json -silent -duc
naabu -host scanme.nmap.org -top-ports 1000 -json -silent -duc
naabu -host scanme.nmap.org -top-ports full -json -silent -duc
naabu -host cdn.example.com -ec -cdn -json -silent -duc
```

## RATE-LIMIT

| Flag | Default | Description |
|------|---------|-------------|
| `-c` | 25 | General internal worker threads |
| `-rate` | 1000 | Packets to send per second |

```bash
naabu -host scanme.nmap.org -rate 300 -c 10 -json -silent -duc
```

## UPDATE

| Flag | Short | Description |
|------|-------|-------------|
| `-update` | `-up` | Update naabu to latest version |
| `-disable-update-check` | `-duc` | Disable automatic update check |

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | File to write output to (optional) |
| `-list-output-fields` | `-lof` | List of fields to output (comma separated) |
| `-exclude-output-fields` | `-eof` | Exclude output fields based on a condition |
| `-json` | `-j` | Write output in **JSON Lines** (**prefer for SpiderFeet**) |
| `-csv` | — | Write output in CSV format |

```bash
naabu -host scanme.nmap.org -json -o ports.jsonl -duc
naabu -host scanme.nmap.org -json -silent -duc
```

## CONFIGURATION

| Flag | Short | Description |
|------|-------|-------------|
| `-config` | — | Path to config file (default `$HOME/.config/naabu/config.yaml`) |
| `-scan-all-ips` | `-sa` | Scan all IPs associated with DNS record |
| `-ip-version` | `-iv` | IP version to scan of hostname (`4`,`6`) — help default `["4","6"]` |
| `-scan-type` | `-s` | Port scan type `SYN`/`CONNECT` — **this binary default `"c"`** |
| `-source-ip` | — | Source IP and port (`x.x.x.x:yyy` — might not work on OSX) |
| `-connect-payload` | `-cp` | Payload to send in CONNECT scans (optional) |
| `-interface-list` | `-il` | List available interfaces and public IP |
| `-interface` | `-i` | Network interface to use |
| `-nmap` | — | Invoke nmap on targets — **Deprecated** |
| `-nmap-cli` | — | Nmap command on found results (e.g. `-nmap-cli 'nmap -sV'`) |
| `-r` | — | Custom DNS resolvers (comma-separated or file) |
| `-proxy` | — | SOCKS5 proxy (`ip[:port]` / `fqdn[:port]`) |
| `-proxy-auth` | — | SOCKS5 auth (`username:password`) |
| `-dns-order` | — | DNS resolution order (`p`/`l`/`lp`/`pl`) (default `l`) |
| `-system-resolver` | `-sr` | Use system DNS as fallback resolver |
| `-resume` | — | Resume scan using `resume.cfg` |
| `-stream` | — | Stream mode (disables resume, nmap, verify, retries, shuffling, etc.) |
| `-passive` | — | Display passive open ports using Shodan InternetDB API |
| `-input-read-timeout` | `-irt` | Timeout on input read (default `3m0s`) |
| `-no-stdin` | — | Disable stdin processing |

```bash
naabu -host example.com -s c -json -silent -duc
naabu -host example.com -sa -iv 4,6 -p 443 -json -silent -duc
naabu -host example.com -passive -json -silent -duc
```

## HOST-DISCOVERY

| Flag | Short | Description |
|------|-------|-------------|
| `-host-discovery` | `-sn` | Perform only host discovery |
| `-skip-host-discovery` | `-Pn` | Skip host discovery |
| `-with-host-discovery` | `-wn` | Enable host discovery |
| `-probe-tcp-syn` | `-ps` | TCP SYN ping (host discovery must be enabled) |
| `-probe-tcp-ack` | `-pa` | TCP ACK ping |
| `-probe-icmp-echo` | `-pe` | ICMP echo request ping |
| `-probe-icmp-timestamp` | `-pp` | ICMP timestamp request ping |
| `-probe-icmp-address-mask` | `-pm` | ICMP address mask request ping |
| `-arp-ping` | `-arp` | ARP ping |
| `-nd-ping` | `-nd` | IPv6 Neighbor Discovery |
| `-rev-ptr` | — | Reverse PTR lookup for input IPs |

```bash
naabu -host 10.0.0.0/24 -sn -duc
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json -silent -duc
```

## SERVICES-DISCOVERY

| Flag | Short | Description |
|------|-------|-------------|
| `-service-discovery` | `-sD` | Service discovery |
| `-service-version` | `-sV` | Service version |

```bash
naabu -host scanme.nmap.org -sD -json -silent -duc
naabu -host scanme.nmap.org -sV -json -silent -duc
```

## OPTIMIZATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-retries` | — | 3 | Retries for the port scan |
| `-timeout` | — | `1s` | Wait before timing out |
| `-warm-up-time` | — | 2 | Seconds between scan phases |
| `-ping` | — | — | Ping probes for host verification |
| `-verify` | — | — | Validate ports again with TCP verification |
| `-smart-scan` | `-ss` | — | Predictive port scanning using port correlation model |
| `-prediction-threshold` | `-pt` | 20 | Minimum confidence for port predictions (0–100%) |

```bash
naabu -host scanme.nmap.org -verify -json -silent -duc
naabu -host scanme.nmap.org -ss -pt 40 -json -silent -duc
```

## DEBUG

| Flag | Short | Description |
|------|-------|-------------|
| `-health-check` | `-hc` | Run diagnostic check up |
| `-debug` | — | Display debugging information |
| `-verbose` | `-v` | Display verbose output |
| `-no-color` | `-nc` | Disable colors |
| `-silent` | — | Display only results |
| `-version` | — | Display version |
| `-stats` | — | Display stats (**deprecated**) |
| `-stats-interval` | `-si` | Seconds between stats updates (**deprecated**, default 5) |
| `-metrics-port` | `-mp` | Port to expose naabu metrics (default `63636`) |

```bash
naabu -hc
naabu -version
```

## CLOUD

| Flag | Short | Description |
|------|-------|-------------|
| `-auth` | — | Configure ProjectDiscovery cloud (pdcp) API key (default true) |
| `-auth-config` | `-ac` | PDCP API key credential file |
| `-dashboard` | `-pd` | Upload / view output in PDCP UI dashboard |
| `-team-id` | `-tid` | Upload asset results to team id |
| `-asset-id` | `-aid` | Upload new assets to existing asset id |
| `-asset-name` | `-aname` | Assets group name |
| `-dashboard-upload` | `-pdu` | Upload naabu JSONL output file to PDCP dashboard |

Prefer local `-json -o` for SpiderFeet corpus; use CLOUD flags only when operator requests PDCP upload.
