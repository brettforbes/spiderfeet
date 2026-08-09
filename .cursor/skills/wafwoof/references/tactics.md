# WAFWOOF Tactics — Adaptive Fingerprint Sequences

## Tactic 1: Standard fingerprint (SpiderFeet)

**Goal:** Named WAF products + generic fallback in one pass.

```bash
wafw00f -a -o- -f json https://TARGET
```

**Adapt:**

- Named `firewall` in JSON → record WEBSERVER_TECHNOLOGY, tune downstream scans
- Only `Generic` → WAF present but unidentified; try Tactic 2–4
- `detected: false` → likely no WAF or silent drop; verify with `-v -v`

## Tactic 2: Redirect comparison

**When:** CDN/WAF only on canonical host.

```bash
# Follow redirects (default)
wafw00f -a -o- -f json https://example.com

# Original host only
wafw00f -r -a -o- -f json https://example.com
```

Compare `url` and `trigger_url` fields in JSON.

## Tactic 3: Header and client impersonation

**When:** Default Chrome fingerprint blocked or sanitized.

`headers.txt`:

```
User-Agent: MyApp/2.0 (Internal Scanner)
Accept: application/json
X-Requested-With: XMLHttpRequest
```

```bash
wafw00f -a -H headers.txt -o- -f json https://TARGET
```

**Adapt:** Mobile app UA, API client Accept headers, or removing User-Agent (wafw00f generic detect compares responses).

## Tactic 4: Regional proxy

**When:** Geo-specific WAF policies.

```bash
wafw00f -a -p socks5://127.0.0.1:1080 -o- -f json https://TARGET
```

## Tactic 5: Hypothesis-driven single test

**When:** `-a` is slow or noisy; you suspect one vendor.

```bash
wafw00f -l | grep -i cloudflare
wafw00f -t "Cloudflare (Cloudflare Inc.)" -o- -f json https://TARGET
```

## Tactic 6: Bulk asset sweep

```bash
# JSON input
jq -n '[.url|{url:.}]' --arg url https://a.com > one.json
wafw00f -a -i urls.json -o- -f json

# Parallel shell (operator responsibility for rate limits)
xargs -a urls.txt -P 4 -I{} wafw00f -a -o- -f json {} > all.jsonl
```

## Tactic 7: Pipeline with CMSeeK and Nuclei

```
1. wafw00f -a -o- -f json URL
2. If Cloudflare/Akamai → CMSeeK with --random-agent
3. Pipe hosts without WAF to Nuclei with lower rate limits on WAF-protected hosts
```

## Tactic 8: Timeout and availability

**When:** `Site appears to be down` or empty stdout.

```bash
wafw00f -T 15 -v -a -o- -f json https://TARGET
```

Verify DNS, TLS, and whether target requires specific SNI/Host header (custom `-H`).

## Decision matrix

| Result | Next step |
|--------|-----------|
| Named WAF + Generic | Trust named; Generic is supporting signal |
| Generic only | Try headers/proxy; scan origin if known |
| None detected | Proceed with full active scan if authorized |
| Multiple named WAFs | Common with CDN + origin WAF; emit all |
| Subprocess timeout (300s) | Reduce parallelism; increase `-T`; split bulk |

## Tactic 9: Output format variants

**When:** Corpus needs CSV/text review or file artifacts instead of stdout.

```bash
wafw00f -a -o scan.json https://TARGET
wafw00f -a -o scan.csv -f csv https://TARGET
wafw00f -a -o scan.txt -f text https://TARGET
wafw00f --no-colors -a -o- -f json https://TARGET
```

SpiderFeet module always uses `-a -o- -f json`; other formats are manual/corpus-only.

## SpiderFeet constraints

Module hard-codes `-a -o- -f json`. Operator tactics with other flags require manual runs or future manifest options.
