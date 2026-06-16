# CMSeeK Tactics — Adaptive Scan Sequences

Sequences to maximize CMS intelligence when networks use redirects, WAFs, or minimal fingerprints.

## Tactic 1: Baseline passive fingerprint

**Goal:** CMS name + version with lowest noise.

```bash
python3 cmseek.py --follow-redirect --batch --light-scan -u https://TARGET
```

**Adapt:**

- If `CMS Detection failed` → Tactic 2 (UA rotation)
- If version empty but CMS known → remove `--light-scan` once for version module only (or full scan without deep modules: `--only-cms` first, then version pass)

## Tactic 2: User-agent rotation

**When:** 403/empty body, Cloudflare challenge, or generic "Access Denied".

Try in order:

```bash
# Random browser UA
python3 cmseek.py --batch --follow-redirect --random-agent -u https://TARGET

# Explicit modern Chrome
python3 cmseek.py --batch --follow-redirect \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" \
  -u https://TARGET

# Googlebot (only where policy allows)
python3 cmseek.py --batch --follow-redirect --googlebot -u https://TARGET
```

**Adapt:** If detection succeeds under alternate UA, record `detection_param` — header vs source hints at WAF bypass vector.

## Tactic 3: Redirect discipline

**When:** Apex redirects to `www`, HTTP→HTTPS, or regional subdomain hosts the CMS.

| Situation | Flag |
|-----------|------|
| Need final host CMS | `--follow-redirect` (default) |
| CMS only on apex, CDN on www | `--no-redirect` and scan both URLs separately |
| SpiderFeet path mismatch | Align `eventData` with directory name under `Result/` or normalize seed to final host |

Batch both:

```bash
printf "https://example.com\nhttps://www.example.com\n" > hosts.txt
python3 cmseek.py --batch --follow-redirect -l hosts.txt
```

## Tactic 4: Constrain false positives

**When:** Multi-CMS signals or custom PHP app mimics WordPress paths.

```bash
# Confirm only Drupal
python3 cmseek.py --batch --follow-redirect --strict-cms drupal -u https://TARGET

# Ignore Joomla noise
python3 cmseek.py --batch --follow-redirect --ignore-cms joomla -u https://TARGET
```

## Tactic 5: Scale across asset list

**When:** PIUS, subdomain enum, or SpiderFeet produced many `INTERNET_NAME` values.

```bash
# One host per line
python3 cmseek.py --batch --follow-redirect --skip-scanned -l internet_names.txt
```

**Adapt:**

- Use `--skip-scanned` on periodic re-runs
- `--clear-result` only when intentionally invalidating cache

## Tactic 6: Deep enumeration (authorized)

**When:** Engagement scope includes plugin/theme/user discovery.

```bash
python3 cmseek.py --batch --follow-redirect -u https://TARGET
# No --light-scan, no --only-cms
```

Review `Result/TARGET/` for CMS-specific files beyond `cms.json`. High request volume — not for continuous monitoring.

## Tactic 7: Combine with WAFWOOF

```
INTERNET_NAME
    → wafw00f -a -o- -f json URL     (WAF fingerprint)
    → cmseek --follow-redirect --batch  (CMS behind WAF)
```

If WAFWOOF reports `Cloudflare` / `Akamai` and CMSeeK fails:

1. Rotate UA (Tactic 2)
2. Scan origin IP or alternate hostname if discovered
3. Fall back to passive sources (BuiltWith, WhatWeb) outside CMSeeK

## Tactic 8: SpiderFeet module alignment

SpiderFeet command (fixed):

```
python3 cmseek.py --follow-redirect --batch -u <INTERNET_NAME>
```

Tactics that change flags require module/manifest updates. For operator-driven scans, run tactics manually and ingest `cms.json` in custom pipelines.

## Decision matrix

| Observation | Next action |
|-------------|-------------|
| `detection_param: header` | CMS obvious; optional light scan |
| `detection_param: dirscheck` | Weak signal; consider `--strict-cms` confirm |
| Empty `cms_version` | Re-run without `--light-scan` |
| `target_url` ≠ seed | Update seeds to final host for path consistency |
| Repeated failures across UAs | Mark blocked; do not brute-force CMSeeK paths without scope |
