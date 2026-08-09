# dnsx CLI Options

Operator reference for **ProjectDiscovery dnsx** DNS toolkit. Prefer **`-json` / `-j` (JSONL)** for SpiderFeet corpus and automation.

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\dnsx\dnsx.exe` |
| Version | **1.2.3** |
| Capture date | **2026-08-10** |
| Help source | `.tmp_dnsx_help/help_h.txt`, `help_long.txt`, `version.txt` |

> Flags below are from live `-h` / `-version` only — **do not invent options**.  
> `help_h.txt` and `help_long.txt` are identical for this capture.

Skill: `.cursor/skills/dnsx/SKILL.md`

---

## SpiderFeet preferred commands

```bash
dnsx -l hosts.txt -a -aaaa -cname -json -silent -o dnsx.jsonl
echo scanme.nmap.org | dnsx -silent -a -aaaa -json
subfinder -d example.com -silent | dnsx -silent -a -aaaa -json
dnsx -d example.com -w wordlist.txt -a -aaaa -json -silent -auto-wildcard
```

---

## Captured help

Live help text captured from `C:\projects\spiderfeet\.tools\dnsx\dnsx.exe` on **2026-08-10**. Each block is the full stdout of the listed command (ANSI sequences retained where present).

### Version (`dnsx -version`)

```text

      _             __  __
   __| | _ __   ___ \ \/ /
  / _' || '_ \ / __| \  / 
 | (_| || | | |\__ \ /  \ 
  \__,_||_| |_||___//_/\_\

		projectdiscovery.io

[[34mINF[0m] Current Version: 1.2.3
```

### Root help (`dnsx -h`)

```text
dnsx is a fast and multi-purpose DNS toolkit allow to run multiple probes using retryabledns library.

Usage:
  C:\projects\spiderfeet\.tools\dnsx\dnsx.exe [flags]

Flags:
INPUT:
   -l, -list string      list of sub(domains)/hosts to resolve (file or comma separated or stdin)
   -d, -domain string    list of domain to bruteforce (file or comma separated or stdin)
   -w, -wordlist string  list of words to bruteforce (file or comma separated or stdin)

QUERY:
   -a                       query A record (default)
   -aaaa                    query AAAA record
   -cname                   query CNAME record
   -ns                      query NS record
   -txt                     query TXT record
   -srv                     query SRV record
   -ptr                     query PTR record
   -mx                      query MX record
   -soa                     query SOA record
   -any                     query ANY record
   -axfr                    query AXFR
   -caa                     query CAA record
   -all, -recon             query all the dns records (a,aaaa,cname,ns,txt,srv,ptr,mx,soa,axfr,caa)
   -e, -exclude-type value  dns query type to exclude (a,aaaa,cname,ns,txt,srv,ptr,mx,soa,axfr,caa) (default none)

FILTER:
   -re, -resp                          display dns response
   -ro, -resp-only                     display dns response only
   -rc, -rcode string                  filter result by dns status code (eg. -rcode noerror,servfail,refused)
   -rtf, -response-type-filter string  return entries with no records for the specified query types (e.g., a, cname)

PROBE:
   -cdn  display cdn name
   -asn  display host asn information

RATE-LIMIT:
   -t, -threads int      number of concurrent threads to use (default 100)
   -rl, -rate-limit int  number of dns request/second to make (disabled as default) (default -1)

UPDATE:
   -up, -update                 update dnsx to latest version
   -duc, -disable-update-check  disable automatic dnsx update check

OUTPUT:
   -o, -output string            file to write output
   -j, -json                     write output in JSONL(ines) format
   -omit-raw, -or                omit raw dns response from jsonl output
   -ot, -output-template string  custom output template (e.g. -ot '{{host}} {{a}}')

DEBUG:
   -hc, -health-check  run diagnostic check up
   -silent             display only results in the output
   -v, -verbose        display verbose output
   -raw, -debug        display raw dns response
   -stats              display stats of the running scan
   -version            display version of dnsx
   -nc, -no-color      disable color in output

OPTIMIZATION:
   -retry int                number of dns attempts to make (must be at least 1) (default 2)
   -hf, -hostsfile           use system host file
   -trace                    perform dns tracing
   -trace-max-recursion int  Max recursion for dns trace (default 255)
   -resume                   resume existing scan
   -stream                   stream mode (wordlist, wildcard, stats and stop/resume will be disabled)
   -timeout value            maximum time to wait for a DNS query to complete (default 3s)

CONFIGURATIONS:
   -auth                         configure ProjectDiscovery Cloud Platform (PDCP) api key (default true)
   -r, -resolver string          list of resolvers to use (file or comma separated)
   -wt, -wildcard-threshold int  wildcard filter threshold (default 5)
   -auto-wildcard                automatically detect wildcard domains for filtering
   -wd, -wildcard-domain string  domain name for manual wildcard filtering (mutually exclusive with -auto-wildcard; other flags will be ignored - json output recommended)
   -proxy string                 proxy to use (eg socks5://127.0.0.1:8080)
```

---

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-list` | `-l` | Sub(domains)/hosts to resolve (file, comma-separated, or stdin) |
| `-domain` | `-d` | Domains to bruteforce |
| `-wordlist` | `-w` | Bruteforce wordlist |

```bash
dnsx -l hosts.txt -a -json -silent
echo scanme.nmap.org | dnsx -silent -a -json
dnsx -d example.com -w wordlist.txt -a -json -silent
```

---

## QUERY

| Flag | Description |
|------|-------------|
| `-a` | A (default) |
| `-aaaa` | AAAA |
| `-cname` | CNAME |
| `-ns` | NS |
| `-txt` | TXT |
| `-srv` | SRV |
| `-ptr` | PTR |
| `-mx` | MX |
| `-soa` | SOA |
| `-any` | ANY |
| `-axfr` | AXFR |
| `-caa` | CAA |
| `-all` / `-recon` | All of: a,aaaa,cname,ns,txt,srv,ptr,mx,soa,axfr,caa |
| `-e` / `-exclude-type` | Exclude types from that set |

```bash
dnsx -l hosts.txt -a -aaaa -cname -json -silent
dnsx -l hosts.txt -mx -txt -ns -soa -json -silent
dnsx -l hosts.txt -all -json -silent
```

---

## FILTER

| Flag | Short | Description |
|------|-------|-------------|
| `-resp` | `-re` | Display DNS response |
| `-resp-only` | `-ro` | Response only |
| `-rcode` | `-rc` | Filter by status (`noerror`, `servfail`, `refused`, …) |
| `-response-type-filter` | `-rtf` | Keep entries with **no** records for given types |

---

## PROBE

| Flag | Description |
|------|-------------|
| `-cdn` | Display CDN name |
| `-asn` | Display ASN information |

---

## RATE-LIMIT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-threads` | `-t` | 100 | Concurrent threads |
| `-rate-limit` | `-rl` | -1 (off) | Requests per second |

---

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | Output file |
| `-json` | `-j` | **JSONL** (SpiderFeet preferred) |
| `-omit-raw` | `-or` | Omit raw DNS from JSONL |
| `-output-template` | `-ot` | Custom template |

```bash
dnsx -l hosts.txt -a -aaaa -json -o dnsx.jsonl
dnsx -l hosts.txt -a -json -omit-raw -o compact.jsonl
```

---

## DEBUG

| Flag | Short | Description |
|------|-------|-------------|
| `-health-check` | `-hc` | Diagnostics |
| `-silent` | — | Results only |
| `-verbose` | `-v` | Verbose |
| `-debug` | `-raw` | Raw DNS response |
| `-stats` | — | Scan stats |
| `-version` | — | Version |
| `-no-color` | `-nc` | No color |

---

## OPTIMIZATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-retry` | — | 2 | Attempts (≥ 1) |
| `-hostsfile` | `-hf` | — | Use system hosts file |
| `-trace` | — | — | DNS tracing |
| `-trace-max-recursion` | — | 255 | Trace recursion limit |
| `-resume` | — | — | Resume scan |
| `-stream` | — | — | Stream mode (disables wordlist, wildcard, stats, stop/resume) |
| `-timeout` | — | 3s | Per-query timeout |

---

## CONFIGURATIONS

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-auth` | — | true | PDCP API key config |
| `-resolver` | `-r` | — | Resolver list (file or comma-separated) |
| `-wildcard-threshold` | `-wt` | 5 | Wildcard threshold |
| `-auto-wildcard` | — | — | Auto wildcard detection |
| `-wildcard-domain` | `-wd` | — | Manual wildcard domain (exclusive with `-auto-wildcard`; other flags ignored — JSON recommended) |
| `-proxy` | — | — | e.g. `socks5://127.0.0.1:8080` |

---

## UPDATE

| Flag | Short | Description |
|------|-------|-------------|
| `-update` | `-up` | Update dnsx |
| `-disable-update-check` | `-duc` | Skip update check |

---

## Common recipes

```bash
# Validate subfinder output
subfinder -d example.com -silent | dnsx -silent -a -aaaa -json

# Enrich live names
dnsx -l live.txt -cname -mx -txt -ns -json -silent

# Bruteforce with wildcard filter
dnsx -d example.com -w dns.txt -a -json -silent -auto-wildcard

# Pipe to httpx
subfinder -d example.com -silent | dnsx -silent -a -aaaa | httpx -json -silent

# PTR sweep
dnsx -l ips.txt -ptr -json -silent
```

---

## Related documentation

| Resource | Path |
|----------|------|
| Agent skill | `.cursor/skills/dnsx/SKILL.md` |
| Reference index | `.cursor/skills/dnsx/references/SKILLS.md` |
| Zero to Hero | `dnsx-Zero-to-Hero.md` |
| Upstream usage | https://docs.projectdiscovery.io/opensource/dnsx/usage |
