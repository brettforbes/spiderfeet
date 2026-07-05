# httpx CLI Options

Grouped flag reference from ProjectDiscovery httpx v1.x. Run `httpx -h` on your install to confirm.

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-list` | `-l` | File with hosts/URLs (one per line) |
| `-target` | `-u` | Target host(s) or URL(s) |
| `-request` | `-rr` | Raw HTTP request file |

```bash
httpx -u https://scanme.sh
httpx -u scanme.sh,example.com
httpx -l hosts.txt
echo scanme.sh | httpx
cat subs.txt | httpx -json -silent
echo AS13335 | httpx -silent
echo 10.0.0.0/24 | httpx -json -silent
```

## PROBES

| Flag | Short | Description |
|------|-------|-------------|
| `-status-code` | `-sc` | Response status code |
| `-content-length` | `-cl` | Content-Length |
| `-content-type` | `-ct` | Content-Type |
| `-location` | — | Redirect location |
| `-favicon` | — | Favicon mmh3 hash |
| `-hash` | — | Body hash (md5, mmh3, sha256, …) |
| `-jarm` | — | JARM TLS fingerprint |
| `-response-time` | `-rt` | Response time |
| `-line-count` | `-lc` | Body line count |
| `-word-count` | `-wc` | Body word count |
| `-title` | — | Page title |
| `-body-preview` | `-bp` | First N chars of body |
| `-web-server` | `-server` | Server header |
| `-tech-detect` | `-td` | Wappalyzer-style technologies |
| `-method` | — | HTTP method used |
| `-websocket` | — | WebSocket support |
| `-ip` | — | Host IP |
| `-cname` | — | CNAME |
| `-asn` | — | ASN info |
| `-cdn` | — | CDN/WAF provider |
| `-probe` | — | SUCCESS/FAILED status |

```bash
httpx -l hosts.txt -sc -title -td -server -cdn -ip -json
httpx -l hosts.txt -favicon -jarm -json
httpx -l hosts.txt -probe -silent
```

## HEADLESS

| Flag | Short | Description |
|------|-------|-------------|
| `-screenshot` | `-ss` | Save page screenshot |
| `-system-chrome` | — | Use system Chrome |
| `-exclude-screenshot-bytes` | `-esb` | Omit screenshot bytes from JSON |
| `-exclude-headless-body` | `-ehb` | Omit headless body from JSON |

## MATCHERS

| Flag | Short | Description |
|------|-------|-------------|
| `-match-code` | `-mc` | Match status codes |
| `-match-length` | `-ml` | Match content length |
| `-match-string` | `-ms` | Match body string |
| `-match-regex` | `-mr` | Match body regex |
| `-match-cdn` | `-mcdn` | Match CDN provider |
| `-match-response-time` | `-mrt` | Match response time |
| `-match-condition` | `-mdc` | DSL condition |

## EXTRACTOR

| Flag | Short | Description |
|------|-------|-------------|
| `-extract-regex` | `-er` | Extract via regex |
| `-extract-preset` | `-ep` | Preset extractors (ipv4, mail, url) |

## FILTERS

| Flag | Short | Description |
|------|-------|-------------|
| `-filter-code` | `-fc` | Exclude status codes |
| `-filter-error-page` | `-fep` | ML error-page filter |
| `-filter-duplicates` | `-fd` | Drop near-duplicate responses |
| `-filter-string` | `-fs` | Exclude body string |
| `-filter-regex` | `-fe` | Exclude regex |
| `-filter-cdn` | `-fcdn` | Exclude CDN provider |
| `-strip` | — | Strip HTML/XML tags from body |

## RATE-LIMIT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-threads` | `-t` | 50 | Worker threads |
| `-rate-limit` | `-rl` | 150 | Requests per second |
| `-rate-limit-minute` | `-rlm` | — | Requests per minute |

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | Output file |
| `-json` | `-j` | JSON Lines |
| `-csv` | — | CSV output |
| `-include-response-header` | `-irh` | Headers in JSON |
| `-include-response` | `-irr` | Full req/resp in JSON |
| `-include-chain` | — | Redirect chain in JSON |
| `-store-response` | `-sr` | Save responses to disk |
| `-store-response-dir` | `-srd` | Custom response directory |
| `-silent` | — | URLs/results only |

## CONFIGURATIONS

| Flag | Short | Description |
|------|-------|-------------|
| `-config` | — | `config.yaml` path |
| `-resolvers` | `-r` | Custom DNS resolvers |
| `-follow-redirects` | `-fr` | Follow redirects |
| `-max-redirects` | `-maxr` | Max redirects (default 10) |
| `-header` | `-H` | Custom request headers |
| `-http-proxy` | `-proxy` | HTTP proxy |
| `-ports` | `-p` | Ports to probe (nmap syntax) |
| `-path` | — | Path(s) to probe |
| `-tls-probe` | — | Probe TLS SAN names |
| `-csp-probe` | — | Probe CSP domains |
| `-vhost` | — | VHOST probing |
| `-probe-all-ips` | `-pa` | Probe all IPs for host |

## OPTIMIZATIONS

| Flag | Short | Description |
|------|-------|-------------|
| `-no-fallback` | `-nf` | Probe both HTTP and HTTPS |
| `-no-fallback-scheme` | `-nfs` | Use input scheme only |
| `-exclude-cdn` | `-ec` | CDN: only 80/443 |
| `-timeout` | — | Timeout seconds (default 10) |
| `-retries` | — | Retry count |
| `-max-host-error` | `-maxhr` | Skip host after N errors |
| `-no-stdin` | — | Disable stdin |

## DEBUG

| Flag | Short | Description |
|------|-------|-------------|
| `-verbose` | `-v` | Verbose |
| `-debug` | — | Debug req/resp |
| `-version` | — | Version |
| `-health-check` | `-hc` | Diagnostics |

See [`config-and-ports.md`](config-and-ports.md) for port/path detail.
