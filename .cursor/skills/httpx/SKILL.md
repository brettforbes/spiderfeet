---
name: httpx
description: HTTP probe and web fingerprinting with ProjectDiscovery httpx, JSONL export, and SpiderFeet nugget mapping. Use for live web server discovery, status/title/tech-detect, CDN/WAF metadata, redirect chains, piping from subfinder/dnsx/naabu, and WEBSERVER_TECHNOLOGY nuggets.
---

# httpx — HTTP Probe to Nuggets

## Purpose

Use when you must **confirm live HTTP/HTTPS services** and fingerprint web surfaces on authorized targets using [ProjectDiscovery httpx](https://github.com/projectdiscovery/httpx) — **not** the Python `httpx` client or Kali `httpx-toolkit`. Capture **JSON Lines** (`-j` / `-json`), map to **`HTTP_CODE`**, **`WEBSERVER_TECHNOLOGY`**, **`WEBSERVER_BANNER`**, **`LINKED_URL_INTERNAL`**, and related nuggets, then chain to **nuclei**, **webanalyze**, or **Julius**.

Run **after** host lists exist (`subfinder`, `dnsx`, `naabu`, `nmap`); httpx does not replace subdomain enum or port scanning.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized URLs/hosts only. httpx sends real HTTP requests.
2. **Prepare inputs** — Hostnames, URLs, `host:port`, list file `-l`, or stdin from upstream tools.
3. **Choose probe profile** — Baseline live check vs rich fingerprint (`-status-code -title -tech-detect -server -cdn -ip`).
4. **Run with JSONL** — `httpx -json -o out.jsonl` (+ `-silent` for pipes). Add `-include-chain` for redirects, `-irh` for headers when mapping `WEBSERVER_HTTPHEADERS`.
5. **Parse JSONL** — One object per line; fields depend on enabled probes (see `references/json-output-schema.md`).
6. **Map nuggets** — Per `references/nugget-mapping.md`: URL/host, status, tech stack, banner, IP.
7. **Filter noise** — Use `-match-code` / `-filter-code`, `-filter-duplicates`, `-fep` for error pages when needed.
8. **Chain downstream** — **nuclei** on confirmed URLs; **webanalyze** for alternate tech pass; re-run httpx on new paths/ports from naabu.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-json`; never parse banner art only |
| Input is bare hostname | httpx probes HTTPS then HTTP (default fallback) |
| Need both schemes explicitly | `-no-fallback` |
| Input already has scheme | Consider `-no-fallback-scheme` |
| Upstream is subfinder/naabu list | Pipe with `-silent -json` |
| Only web ports matter after naabu | `naabu -json -silent \| httpx -json -silent` |
| CDN/WAF masks origin | Use `-cdn` metadata; `-exclude-cdn` limits port fan-out |
| Many 404/403 noise | `-filter-code 404,403` or `-match-code 200,301,302` |
| Redirect investigation | `-follow-redirects` + `-include-chain` in JSON |
| Non-default ports | `-p http:8080,https:8443` or custom `-ports` syntax |
| Path discovery | Separate run with `-path` (do not mix with default mass probe) |
| Empty JSONL on known live site | Try `-no-fallback`, alternate ports, `-probe-all-ips` |
| Rate limited / fragile target | Lower `-threads`, `-rate-limit`, increase `-timeout` |
| Tech-detect empty | Retry with paths (`/login`, `/api`); check CDN blocking |
| Body evidence needed | `-store-response` or `-body-preview` (size limits apply) |
| Screenshot needed | `-screenshot` (slow; headless Chrome) — separate scenario |

## Guardrails & Pitfalls

- **Authorization** — Probing third-party assets without permission is prohibited.
- **Not Python httpx** — Always ProjectDiscovery binary `httpx` on PATH.
- **Default HTTPS→HTTP fallback** — A single input may yield one URL; use `-no-fallback` to see both.
- **JSONL ≠ JSON array** — Parse line by line; harvest bundles use `records[]`.
- **`-path` / `-screenshot` / `-vhost`** — Heavy modes; run as dedicated scenarios, not default corpus noise.
- **Response storage** — `-store-response` / `-irr` can produce huge artifacts; cap with `-response-size-to-read`.
- **Headless screenshots** — Very slow; disable in bulk pipelines unless scenario requires visuals.
- **WAF/CDN** — Tech-detect may show edge stack only, not origin.
- **Do not** treat httpx as vulnerability scanning — use **nuclei** next.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | All flags by category |
| `json-output-schema.md` | JSONL fields |
| `probes-matchers-filters.md` | Probes vs matchers vs filters |
| `config-and-ports.md` | Config file, ports, paths |
| `workflows-and-phases.md` | Pipeline phases |
| `tactics.md` | CDN, thin yield, rate limits |
| `nugget-mapping.md` | JSONL → SpiderFeet graph |
| `sources.md` | Official URLs |

Operator guides: `.docs/docs-for-cli-tools/Httpx-Zero-to-Hero.md`, `Httpx-CLI-Options.md`.

## Comprehensive Examples

### INPUT

```bash
httpx -u https://scanme.sh
httpx -u scanme.sh,example.com
httpx -l hosts.txt
echo scanme.sh | httpx -silent
cat subs.txt | httpx -json -silent
echo AS13335 | httpx -silent
echo 192.168.1.0/24 | httpx -silent -json
```

### PROBES (fingerprint pass)

```bash
httpx -u https://scanme.sh -status-code -title -tech-detect -server -cdn -ip -json -o probe.jsonl
httpx -l hosts.txt -sc -title -td -web-server -cdn -silent
httpx -l hosts.txt -favicon -jarm -rt -json -o rich.jsonl
httpx -l hosts.txt -probe
```

### OUTPUT (JSONL)

```bash
httpx -l hosts.txt -json -o results.jsonl
httpx -l hosts.txt -json -include-chain -irh -o full.jsonl
httpx -l hosts.txt -json -csv -o results.csv
httpx -l hosts.txt -silent -o urls.txt
```

### MATCHERS / FILTERS

```bash
httpx -l hosts.txt -match-code 200,301,302 -json -silent
httpx -l hosts.txt -filter-code 404,403 -json -silent
httpx -l hosts.txt -match-string admin -json
httpx -l hosts.txt -filter-duplicates -json
httpx -l urls.txt -path /api -filter-error-page
```

### RATE-LIMIT / TIMEOUT

```bash
httpx -l hosts.txt -threads 25 -rate-limit 50 -timeout 15 -json
httpx -l hosts.txt -retries 2 -max-host-error 10 -json
```

### PORTS / PATHS

```bash
httpx -l hosts.txt -p http:8080,https:8443 -json
httpx -l urls.txt -path /v1/api,/admin -status-code
httpx -u https://example.com -tls-probe -csp-probe
```

### PIPELINES

```bash
subfinder -d example.com -silent | httpx -title -tech-detect -status-code -json -silent
subfinder -d example.com -silent | dnsx -silent -a | httpx -json -silent
naabu -host scanme.sh -json -silent | httpx -json -silent
httpx -l live.txt -json -silent | nuclei -silent -jsonl
```

### Parse one JSONL line (Python)

```python
import json

line = '{"url":"https://api.example.com","status_code":200,"webserver":"nginx","tech":["Nginx"]}'
row = json.loads(line)
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Live first, fingerprint second** — `-silent` URL list pass, then `-json -tech-detect -title` on hits only.
2. **Pipeline order** — `subfinder → dnsx → httpx` (early web confirm) and `naabu → httpx` (open web ports).
3. **CDN-aware** — Record `-cdn`; avoid over-scanning; origin may need different host header or direct IP pass.
4. **Redirect clarity** — `-include-chain` for 301/302 matrices; map final URL as `LINKED_URL_INTERNAL`.
5. **Maximize on thin yield** — `-no-fallback`, `-probe-all-ips`, custom `-p`, `-path` list, lower rate limits.
