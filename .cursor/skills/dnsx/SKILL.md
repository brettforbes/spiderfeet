---
name: dnsx
description: Resolve DNS records and validate subdomains with dnsx when prompts mention dns resolution, wildcard filtering, A/AAAA/CNAME/MX/TXT lookups, DNS brute force, or recon pipelines from subfinder/httpx/naabu into SpiderFeet INTERNET_NAME and IP_ADDRESS graph nodes.
---

# dnsx — DNS Resolve to Nuggets

## Purpose

Use when you must **validate hostnames**, **query DNS record classes**, or **bruteforce subdomains** on authorized domains with [ProjectDiscovery dnsx](https://github.com/projectdiscovery/dnsx), capture **JSON Lines** (`-j` / `-json`), and map answers to SpiderFeet **`INTERNET_NAME`**, **`IPV4_ADDRESS` / `IPV6_ADDRESS`** (via `classify_ip`), **`DNS_TEXT`**, **`DNS_SRV`**, **`DNS_SPF`**, **`PROVIDER_DNS` / `PROVIDER_MAIL`**, then chain to **httpx**, **naabu**, or **nuclei**.

Run **after** name lists exist (`subfinder`, wordlists, passive OSINT); dnsx does not replace passive enumeration or HTTP probing.

**Binary (this repo):** `C:\projects\spiderfeet\.tools\dnsx\dnsx.exe` — **v1.2.3** (captured **2026-08-10**).

## Step-by-Step Instructions

1. **Confirm scope** — Authorized domains/hosts only. dnsx sends real DNS queries to resolvers (default public set or `-r`).
2. **Prepare inputs** — One hostname per line (`-l`), stdin from upstream, or bruteforce with `-d` + `-w`.
3. **Choose query profile** — Liveness (`-a` default, add `-aaaa`) vs enrichment (`-cname -ns -mx -txt -soa -caa`) vs reverse (`-ptr` on IPs).
4. **Run with JSONL** — Always `-json` / `-j` for corpus and nuggets. Add `-resp` when you need answer values in text mode; JSON already carries typed arrays (`a`, `aaaa`, `cname`, …). Prefer `-omit-raw` / `-or` to shrink JSONL when `all` RR wire text is not needed.
5. **Parse JSONL** — One object per line; fields depend on enabled query flags (see `references/json-output-schema.md`).
6. **Map nuggets** — Per `references/nugget-mapping.md`: host → `INTERNET_NAME`; IPs via `classify_ip`; TXT/SPF/SRV/NS/MX to catalogue types.
7. **Handle wildcards** — Use `-wt`, `-auto-wildcard`, or `-wd` when synthetic answers pollute results (`-wd` recommends JSON and is mutually exclusive with `-auto-wildcard`).
8. **Chain downstream** — Pipe live names to **httpx** / **naabu**; re-run dnsx on new hostnames from TLS SAN / crawl discoveries.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-json` (`-j`); never parse banner art only |
| Input is subfinder hostname list | `subfinder … -silent \| dnsx -silent -a -aaaa -json` |
| Need only live host validation | `-a -aaaa` first; defer heavy record classes |
| Need mail / SPF posture | `-mx -txt` (map SPF strings to `DNS_SPF`) |
| Need CDN / SaaS pivot | `-cname` (+ `-cdn` when labeling edge) |
| Need zone / hosting context | `-ns -soa` → `PROVIDER_DNS` candidates |
| Reverse infrastructure mapping | `-ptr` on discovered IPs |
| Wildcard false positives | `-auto-wildcard` or `-wd domain` + raise/lower `-wt` (default 5) |
| Resolver rate limits / SERVFAIL spikes | Lower `-t`, set `-rl`, raise `-retry`, rotate `-r` |
| Bruteforce enumeration needed | `-d target.tld -w wordlist.txt` with `-a -json` |
| Stream large stdin lists | `-stream` (disables wordlist, wildcard, stats, stop/resume) |
| Resume interrupted scan | `-resume` (not with `-stream`) |
| Downstream HTTP misses IPv6 | Ensure `-aaaa` was enabled |
| Empty JSONL on known-good name | Check `-rcode`, try alternate `-r`, increase `-retry` / `-timeout` |
| Raw DNS wire noise in JSONL | `-omit-raw` / `-or` |

## Guardrails & Pitfalls

- **Authorization** — Only resolve in-scope names; queries leave the host via chosen resolvers.
- **JSONL ≠ JSON array** — Parse line by line; harvest bundles use `records[]`.
- **Do not invent flags** — Use only options from live `dnsx -h` (see CLI docs Captured help).
- **`-wd` vs `-auto-wildcard`** — Mutually exclusive; help notes other flags ignored with `-wd` and recommends JSON.
- **`-stream` tradeoffs** — Disables wordlist, wildcard, stats, and stop/resume.
- **Single-resolver trust** — Do not treat one SERVFAIL/NXDOMAIN as definitive in wildcard-heavy zones.
- **IP nuggets** — Use `core.ip_classify.classify_ip` (IPv4 vs IPv6); never hardcode `IP_ADDRESS` for colon-form literals.
- **`-all` / `-recon`** — Broad and noisy; prefer explicit record flags for corpus scenarios.
- **Do not** treat dnsx as HTTP probing or vuln scanning — use **httpx** / **nuclei** next.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | All flags by category |
| `json-output-schema.md` | JSONL fields |
| `workflows-and-phases.md` | Pipeline phases |
| `tactics.md` | Wildcards, thin yield, resolvers |
| `nugget-mapping.md` | JSONL → SpiderFeet graph |
| `sources.md` | Official URLs |

Operator guides: `.docs/docs-for-cli-tools/dnsx-Zero-to-Hero.md`, `dnsx-CLI-Options.md`.

Help captures: `.tmp_dnsx_help/` (`help_h.txt`, `help_long.txt`, `version.txt`) — **2026-08-10**.

## Comprehensive Examples

### INPUT

```bash
dnsx -l hosts.txt -silent -a -json
echo scanme.nmap.org | dnsx -silent -a -aaaa -json
cat subs.txt | dnsx -silent -a -aaaa -cname -json
dnsx -d example.com -w wordlist.txt -silent -a -json
```

### QUERY (record classes)

```bash
dnsx -l hosts.txt -a -aaaa -json -silent
dnsx -l hosts.txt -cname -ns -soa -json -silent
dnsx -l hosts.txt -mx -txt -caa -json -silent
dnsx -l hosts.txt -srv -ptr -json -silent
dnsx -l hosts.txt -all -json -silent
dnsx -l hosts.txt -recon -e axfr -json -silent
```

### FILTER / RESPONSE

```bash
dnsx -l hosts.txt -a -resp -json -silent
dnsx -l hosts.txt -a -resp-only -silent
dnsx -l hosts.txt -a -rcode noerror -json -silent
dnsx -l hosts.txt -a -rtf cname -json -silent
```

### PROBE (CDN / ASN)

```bash
dnsx -l hosts.txt -a -cdn -asn -json -silent
```

### OUTPUT (JSONL)

```bash
dnsx -l hosts.txt -a -aaaa -cname -json -o dnsx.jsonl
dnsx -l hosts.txt -a -json -omit-raw -o compact.jsonl
dnsx -l hosts.txt -a -ot "{{host}} {{a}}" -o custom.txt
```

### RATE-LIMIT / OPTIMIZATION

```bash
dnsx -l hosts.txt -a -json -t 50 -rl 100 -retry 3 -timeout 5s
dnsx -l hosts.txt -a -json -r resolvers.txt
dnsx -l hosts.txt -a -json -auto-wildcard -wt 5
dnsx -l hosts.txt -a -json -wd example.com
dnsx -l hosts.txt -a -json -trace
dnsx -l hosts.txt -a -json -stream
dnsx -l hosts.txt -a -json -resume
```

### PIPELINES

```bash
subfinder -d example.com -silent | dnsx -silent -a -aaaa -json
subfinder -d example.com -silent | dnsx -silent -a -aaaa | httpx -json -silent
subfinder -d example.com -silent | dnsx -silent -a | naabu -json -silent
dnsx -l hosts.txt -silent -a -aaaa -json | jq -r '.host' | httpx -json -silent
```

### Parse one JSONL line (Python)

```python
import json

line = '{"host":"scanme.nmap.org","a":["45.33.32.156"],"aaaa":["2600:3c01::f03c:91ff:fe18:bb2f"],"status_code":"NOERROR"}'
row = json.loads(line)
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Validate first, enrich second** — `-a -aaaa` liveness, then CNAME/MX/TXT/NS on hits only.
2. **Pipeline order** — `subfinder → dnsx → httpx` (early web) and `dnsx → naabu` (ports on resolved names).
3. **Wildcard-aware** — Detect synthetic answers before treating every A record as a host.
4. **Resolver differential** — Re-query suspicious names with alternate `-r` lists.
5. **Maximize thin yield** — Add `-aaaa`, `-cname`, raise `-retry`, lower `-t`, try trusted resolvers.
