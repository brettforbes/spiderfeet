# dnsx CLI Options

Grouped flag reference from live help for **dnsx v1.2.3** (`C:\projects\spiderfeet\.tools\dnsx\dnsx.exe`, captured **2026-08-10**). Run `dnsx -h` on your install to confirm. Do not invent flags.

Full exact help text: `.docs/docs-for-cli-tools/dnsx-CLI-Options.md` → **Captured help**.

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-list` | `-l` | List of sub(domains)/hosts to resolve (file, comma-separated, or stdin) |
| `-domain` | `-d` | List of domains to bruteforce (file, comma-separated, or stdin) |
| `-wordlist` | `-w` | Wordlist for bruteforce (file, comma-separated, or stdin) |

```bash
dnsx -l hosts.txt -a -json -silent
echo scanme.nmap.org | dnsx -silent -a -json
dnsx -d example.com -w wordlist.txt -a -json -silent
```

## QUERY

| Flag | Short | Description |
|------|-------|-------------|
| `-a` | — | Query A record (**default**) |
| `-aaaa` | — | Query AAAA record |
| `-cname` | — | Query CNAME record |
| `-ns` | — | Query NS record |
| `-txt` | — | Query TXT record |
| `-srv` | — | Query SRV record |
| `-ptr` | — | Query PTR record |
| `-mx` | — | Query MX record |
| `-soa` | — | Query SOA record |
| `-any` | — | Query ANY record |
| `-axfr` | — | Query AXFR |
| `-caa` | — | Query CAA record |
| `-all` / `-recon` | — | Query all listed types (a,aaaa,cname,ns,txt,srv,ptr,mx,soa,axfr,caa) |
| `-exclude-type` | `-e` | Exclude query types from the set above (default none) |

```bash
dnsx -l hosts.txt -a -aaaa -cname -json -silent
dnsx -l hosts.txt -mx -txt -ns -soa -json -silent
dnsx -l hosts.txt -all -json -silent
dnsx -l hosts.txt -recon -e axfr -json -silent
```

## FILTER

| Flag | Short | Description |
|------|-------|-------------|
| `-resp` | `-re` | Display DNS response |
| `-resp-only` | `-ro` | Display DNS response only |
| `-rcode` | `-rc` | Filter by DNS status code (e.g. `noerror,servfail,refused`) |
| `-response-type-filter` | `-rtf` | Return entries with **no** records for specified types (e.g. `a`, `cname`) |

```bash
dnsx -l hosts.txt -a -resp -json -silent
dnsx -l hosts.txt -a -rcode noerror -json -silent
dnsx -l hosts.txt -a -rtf cname -json -silent
```

## PROBE

| Flag | Description |
|------|-------------|
| `-cdn` | Display CDN name |
| `-asn` | Display host ASN information |

```bash
dnsx -l hosts.txt -a -cdn -asn -json -silent
```

## RATE-LIMIT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-threads` | `-t` | 100 | Concurrent threads |
| `-rate-limit` | `-rl` | -1 (disabled) | DNS requests per second |

```bash
dnsx -l hosts.txt -a -json -t 50 -rl 100
```

## UPDATE

| Flag | Short | Description |
|------|-------|-------------|
| `-update` | `-up` | Update dnsx to latest version |
| `-disable-update-check` | `-duc` | Disable automatic update check |

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | File to write output |
| `-json` | `-j` | Write output in **JSONL** (**prefer for SpiderFeet**) |
| `-omit-raw` | `-or` | Omit raw DNS response from JSONL |
| `-output-template` | `-ot` | Custom template (e.g. `{{host}} {{a}}`) |

```bash
dnsx -l hosts.txt -a -aaaa -json -o dnsx.jsonl
dnsx -l hosts.txt -a -json -omit-raw -o compact.jsonl
dnsx -l hosts.txt -a -ot "{{host}} {{a}}"
```

## DEBUG

| Flag | Short | Description |
|------|-------|-------------|
| `-health-check` | `-hc` | Run diagnostic checkup |
| `-silent` | — | Display only results |
| `-verbose` | `-v` | Verbose output |
| `-debug` | `-raw` | Display raw DNS response |
| `-stats` | — | Display scan stats |
| `-version` | — | Display version |
| `-no-color` | `-nc` | Disable color |

## OPTIMIZATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-retry` | — | 2 | DNS attempts (must be ≥ 1) |
| `-hostsfile` | `-hf` | — | Use system hosts file |
| `-trace` | — | — | Perform DNS tracing |
| `-trace-max-recursion` | — | 255 | Max recursion for DNS trace |
| `-resume` | — | — | Resume existing scan |
| `-stream` | — | — | Stream mode (wordlist, wildcard, stats, stop/resume disabled) |
| `-timeout` | — | 3s | Max wait per DNS query |

```bash
dnsx -l hosts.txt -a -json -retry 3 -timeout 5s
dnsx -l hosts.txt -a -json -trace
dnsx -l hosts.txt -a -json -stream
dnsx -l hosts.txt -a -json -resume
```

## CONFIGURATIONS

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-auth` | — | true | Configure ProjectDiscovery Cloud Platform (PDCP) API key |
| `-resolver` | `-r` | — | Resolvers (file or comma-separated) |
| `-wildcard-threshold` | `-wt` | 5 | Wildcard filter threshold |
| `-auto-wildcard` | — | — | Automatically detect wildcard domains for filtering |
| `-wildcard-domain` | `-wd` | — | Manual wildcard domain (mutually exclusive with `-auto-wildcard`; other flags ignored — JSON recommended) |
| `-proxy` | — | — | Proxy (e.g. `socks5://127.0.0.1:8080`) |

```bash
dnsx -l hosts.txt -a -json -r 1.1.1.1,8.8.8.8
dnsx -l hosts.txt -a -json -auto-wildcard -wt 5
dnsx -l hosts.txt -a -json -wd example.com
dnsx -l hosts.txt -a -json -proxy socks5://127.0.0.1:8080
```
