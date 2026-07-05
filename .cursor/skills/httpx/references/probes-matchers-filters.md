# httpx Probes, Matchers, and Filters

## Probes — what to collect

Probes are **display/capture toggles** on the HTTP response. Enable the minimum set for the scenario goal.

| Goal | Recommended probes |
|------|-------------------|
| Live URL list only | none (default URL output) or `-probe` |
| Basic fingerprint | `-status-code -title -web-server` |
| Stack for nuclei tags | add `-tech-detect` |
| Infrastructure context | add `-ip -cdn -asn -cname` |
| TLS research | `-jarm` (separate pass) |
| Favicon correlation | `-favicon` (separate pass) |
| Timing analysis | `-response-time` |

**Do not** enable all probes on huge host lists — cost scales with threads × probes × hosts.

## Matchers — keep rows that qualify

Matchers **retain** output that matches criteria. Combine for focused sets:

```bash
# Only successful pages
httpx -l hosts.txt -match-code 200,301,302 -json -silent

# Pages mentioning admin
httpx -l hosts.txt -match-string admin -json

# Fast responses only
httpx -l hosts.txt -match-response-time '< 1' -json
```

Use matchers when upstream list is large and you need a **high-signal subset** before nuclei.

## Filters — drop noise

Filters **exclude** unwanted rows:

```bash
# Drop 404/403
httpx -l hosts.txt -filter-code 404,403 -json -silent

# Drop CDN edges you will not exploit directly
httpx -l hosts.txt -filter-cdn cloudfront -json

# Collapse duplicate soft-404 pages
httpx -l hosts.txt -filter-duplicates -json

# ML error page classifier
httpx -l urls.txt -path /api -filter-error-page
```

## Matcher vs filter decision

| Situation | Use |
|-----------|-----|
| Know what you want (200, admin) | **Matcher** |
| Know what to drop (404, errors) | **Filter** |
| Soft-404 spam on path scan | **`-filter-error-page`** or **`-filter-duplicates`** |
| Empty output after matchers | Widen codes or remove matchers |

## Probe modes that are separate scenarios

Run these **standalone** — not bundled with default mass probe:

| Flag | Why separate |
|------|----------------|
| `-path` | Multiplies requests per host |
| `-screenshot` | Headless browser; very slow |
| `-vhost` | Different input semantics |
| `-tls-probe` / `-csp-probe` | Extra DNS-derived hosts |
| `-favicon` / `-jarm` | Extra requests per URL |

## JSONL interaction

- Matchers/filters apply **before** JSONL write — omitted rows never appear in output.
- For corpus negative fixtures (403-only host), **disable filters** so evidence is captured.

## Common combinations

```bash
# Recon fingerprint pass
httpx -l live.txt -sc -title -td -server -cdn -json -o web.jsonl

# Clean URL list for nuclei
httpx -l live.txt -match-code 200,301,302,401,403 -json -silent

# Path discovery
httpx -l urls.txt -path /api,/admin,/v1 -sc -json -o paths.jsonl
```
