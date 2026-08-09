# Naabu CLI Options

Operator reference for **ProjectDiscovery Naabu** port scanner. Prefer **`-json` / `-j` (JSONL)** for SpiderFeet corpus and automation.

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\naabu\naabu.exe` |
| Version | **2.6.1** |
| Capture date | **2026-08-10** |
| Help source | `.tmp_naabu_help/help_h.txt`, `help_long.txt`, `version.txt` |

> Flags below are from live `-h` / `-version` only — **do not invent options**.  
> `help_h.txt` and `help_long.txt` are identical for this capture.  
> **Windows:** help default `-scan-type` / `-s` is **`"c"` (CONNECT)**. SYN requires privileges + Npcap; `naabu -hc` may report `Privileged/NET_RAW: Ko`.

Skill: `.cursor/skills/naabu/SKILL.md`

---

## SpiderFeet preferred commands

```bash
naabu -host scanme.nmap.org -top-ports 100 -json -silent -o naabu.jsonl -duc
naabu -l hosts.txt -p 80,443,8080,8443 -json -silent -duc
echo example.com | naabu -json -silent -duc
subfinder -d example.com -silent | naabu -top-ports 1000 -json -silent -duc
naabu -host example.com -passive -json -silent -duc
naabu -host cdn.example.com -ec -cdn -json -silent -duc
```

---

## Captured help

Live help text captured from `C:\projects\spiderfeet\.tools\naabu\naabu.exe` on **2026-08-10**. Each block is the full stdout of the listed command (ANSI sequences retained where present).

### Version (`naabu -version`)

```text

                  __
  ___  ___  ___ _/ /  __ __
 / _ \/ _ \/ _ \/ _ \/ // /
/_//_/\_,_/\_,_/_.__/\_,_/

		projectdiscovery.io

[INF] Current Version: 2.6.1
```

### Root help (`naabu -h`)

```text
Naabu is a port scanning tool written in Go that allows you to enumerate open ports for hosts in a fast and reliable manner.

Usage:
  C:\projects\spiderfeet\.tools\naabu\naabu.exe [flags]

Flags:
INPUT:
   -host string[]              hosts to scan ports for (comma-separated)
   -list, -l string            list of hosts to scan ports (file)
   -exclude-hosts, -eh string  hosts to exclude from the scan (comma-separated)
   -exclude-file, -ef string   list of hosts to exclude from scan (file)

PORT:
   -port, -p string              ports to scan (80,443, 100-200)
   -top-ports, -tp string        top ports to scan (default 100) [full,100,1000]
   -exclude-ports, -ep string[]  ports to exclude from scan (file or comma-separated)
   -ports-file, -pf string[]     list of ports to scan (file or comma-separated)
   -port-threshold, -pts int     port threshold to skip port scan for the host
   -exclude-cdn, -ec             skip full port scans for CDN/WAF (only scan for port 80,443)
   -display-cdn, -cdn            display cdn in use

RATE-LIMIT:
   -c int     general internal worker threads (default 25)
   -rate int  packets to send per second (default 1000)

UPDATE:
   -up, -update                 update naabu to latest version
   -duc, -disable-update-check  disable automatic naabu update check

OUTPUT:
   -o, -output string                     file to write output to (optional)
   -lof, -list-output-fields              list of fields to output (comma separated)
   -eof, -exclude-output-fields string[]  exclude output fields output based on a condition
   -j, -json                              write output in JSON lines format
   -csv                                   write output in csv format

CONFIGURATION:
   -config string                   path to the naabu configuration file (default $HOME/.config/naabu/config.yaml)
   -scan-all-ips, -sa               scan all the IP's associated with DNS record
   -ip-version, -iv string[]        ip version to scan of hostname (4,6) - (default 4,6) (default ["4", "6"])
   -scan-type, -s string            type of port scan (SYN/CONNECT) (default "c")
   -source-ip string                source ip and port (x.x.x.x:yyy - might not work on OSX) 
   -connect-payload, -cp string     payload to send in CONNECT scans (optional)
   -interface-list, -il             list available interfaces and public ip
   -interface, -i string            network Interface to use for port scan
   -nmap                            invoke nmap scan on targets (nmap must be installed) - Deprecated
   -nmap-cli string                 nmap command to run on found results (example: -nmap-cli 'nmap -sV')
   -r string                        list of custom resolver dns resolution (comma separated or from file)
   -proxy string                    socks5 proxy (ip[:port] / fqdn[:port]
   -proxy-auth string               socks5 proxy authentication (username:password)
   -dns-order string                dns resolution order (p/l/lp/pl) (default "l")
   -sr, -system-resolver            use system DNS as fallback resolver
   -resume                          resume scan using resume.cfg
   -stream                          stream mode (disables resume, nmap, verify, retries, shuffling, etc)
   -passive                         display passive open ports using shodan internetdb api
   -irt, -input-read-timeout value  timeout on input read (default 3m0s)
   -no-stdin                        Disable Stdin processing

HOST-DISCOVERY:
   -sn, -host-discovery           Perform Only Host Discovery
   -Pn, -skip-host-discovery      Skip Host discovery
   -wn, -with-host-discovery      Enable Host discovery
   -ps, -probe-tcp-syn string[]   TCP SYN Ping (host discovery needs to be enabled)
   -pa, -probe-tcp-ack string[]   TCP ACK Ping (host discovery needs to be enabled)
   -pe, -probe-icmp-echo          ICMP echo request Ping (host discovery needs to be enabled)
   -pp, -probe-icmp-timestamp     ICMP timestamp request Ping (host discovery needs to be enabled)
   -pm, -probe-icmp-address-mask  ICMP address mask request Ping (host discovery needs to be enabled)
   -arp, -arp-ping                ARP ping (host discovery needs to be enabled)
   -nd, -nd-ping                  IPv6 Neighbor Discovery (host discovery needs to be enabled)
   -rev-ptr                       Reverse PTR lookup for input ips

SERVICES-DISCOVERY:
   -sD, -service-discovery  Service Discovery
   -sV, -service-version    Service Version

OPTIMIZATION:
   -retries int                    number of retries for the port scan (default 3)
   -timeout value                  millisecond to wait before timing out (default 1s)
   -warm-up-time int               time in seconds between scan phases (default 2)
   -ping                           ping probes for verification of host
   -verify                         validate the ports again with TCP verification
   -ss, -smart-scan                predictive port scanning using port correlation model
   -pt, -prediction-threshold int  minimum confidence for port predictions (0-100%) (default 20)

DEBUG:
   -health-check, -hc        run diagnostic check up
   -debug                    display debugging information
   -verbose, -v              display verbose output
   -no-color, -nc            disable colors in CLI output
   -silent                   display only results in output
   -version                  display version of naabu
   -stats                    display stats of the running scan (deprecated)
   -si, -stats-interval int  number of seconds to wait between showing a statistics update (deprecated) (default 5)
   -mp, -metrics-port int    port to expose naabu metrics on (default 63636)

CLOUD:
   -auth                           configure projectdiscovery cloud (pdcp) api key (default true)
   -ac, -auth-config string        configure projectdiscovery cloud (pdcp) api key credential file
   -pd, -dashboard                 upload / view output in projectdiscovery cloud (pdcp) UI dashboard
   -tid, -team-id string           upload asset results to given team id (optional)
   -aid, -asset-id string          upload new assets to existing asset id (optional)
   -aname, -asset-name string      assets group name to set (optional)
   -pdu, -dashboard-upload string  upload naabu output file (jsonl) in projectdiscovery cloud (pdcp) UI dashboard
```

---

## Flag groups (summary)

### INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-host` | — | Hosts to scan (comma-separated) |
| `-list` | `-l` | Host list file |
| `-exclude-hosts` | `-eh` | Hosts to exclude |
| `-exclude-file` | `-ef` | Exclude file |

### PORT

| Flag | Short | Description |
|------|-------|-------------|
| `-port` | `-p` | Ports (`80,443`, ranges `100-200`) |
| `-top-ports` | `-tp` | `full`, `100`, `1000` (default 100) |
| `-exclude-ports` | `-ep` | Ports to skip |
| `-ports-file` | `-pf` | Port list file |
| `-port-threshold` | `-pts` | Skip host when open-port count exceeds threshold |
| `-exclude-cdn` | `-ec` | CDN/WAF: only 80,443 |
| `-display-cdn` | `-cdn` | Show CDN in use |

Official Running docs also document full range via `-p -` and UDP as `u:port`.

### RATE-LIMIT

| Flag | Default | Description |
|------|---------|-------------|
| `-c` | 25 | Worker threads |
| `-rate` | 1000 | Packets per second |

### OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | Output file |
| `-list-output-fields` | `-lof` | Fields to include |
| `-exclude-output-fields` | `-eof` | Fields to exclude |
| `-json` | `-j` | **JSONL (preferred)** |
| `-csv` | — | CSV |

### CONFIGURATION (highlights)

| Flag | Short | Notes |
|------|-------|-------|
| `-scan-type` | `-s` | `SYN`/`CONNECT` — **default `"c"` on this binary** |
| `-scan-all-ips` | `-sa` | All DNS IPs |
| `-ip-version` | `-iv` | `4`,`6` |
| `-passive` | — | Shodan InternetDB |
| `-stream` | — | Disables resume/nmap/verify/retries/shuffling |
| `-nmap-cli` | — | Run nmap on findings |
| `-nmap` | — | Deprecated |
| `-connect-payload` | `-cp` | Optional CONNECT payload |

### HOST-DISCOVERY / SERVICES / OPTIMIZATION

See Captured help for full lists: `-sn`, `-Pn`, `-wn`, probe flags (`-ps`, `-pa`, `-pe`, …), `-sD`, `-sV`, `-verify`, `-ss`, `-pt`.

### CLOUD

PDCP upload/auth flags (`-auth`, `-pd`, `-pdu`, …) — optional; local `-json -o` is enough for SpiderFeet.

---

## Notes

- Online Usage docs may lag this binary (missing CLOUD, SERVICES-DISCOVERY, smart-scan, etc.). Prefer this capture.
- Tune `-rate` / `-c` when scanning from a laptop (PD assumes VPS-class defaults).
- Metrics listen on localhost port `63636` by default (`-mp`).
