---
name: wafwoof
description: Fingerprint Web Application Firewalls with wafw00f (WAFWOOF). Use when detecting Cloudflare, Akamai, AWS WAF, etc., parsing JSON stdout from wafw00f -a -o- -f json, mapping WEBSERVER_TECHNOLOGY and RAW_RIR_DATA nuggets, or running SpiderFeet sfp_tool_wafw00f.
---

# WAFWOOF (wafw00f) — Web Application Firewall Fingerprinting

## Purpose

Use when you need to **detect and identify WAF products** protecting a web target before deeper scanning. SpiderFeet emits `WEBSERVER_TECHNOLOGY` (vendor + product) and `RAW_RIR_DATA` (full JSON array on stdout).

**Binary name:** `wafw00f` (three zeros). Skill directory: `wafwoof`.

## Step-by-Step Instructions

1. **Install** — `pip install wafw00f` or system package; binary must be on PATH or configured in SpiderFeet.
2. **Normalize URL** — wafw00f prepends `https://` if scheme missing. SpiderFeet passes `INTERNET_NAME` as URL.
3. **Run JSON scan (SpiderFeet default)** — find all matching WAFs, stdout JSON:

```bash
wafw00f -a -o- -f json https://example.com
```

4. **Parse JSON array** — each element is one detection result (see `references/json-output-schema.md`).
5. **Map to nuggets** — full array → `RAW_RIR_DATA`; each non-Generic detection → `WEBSERVER_TECHNOLOGY` as `"<manufacturer> <firewall>"`.
6. **Adapt if blocked** — try `-H headers.txt`, `-p proxy`, `-r` (no redirect), or `-t` single-WAF test.
7. **Batch targets** — multiple URLs on CLI, or `-i targets.json` with `url` field.

## If/Then Decision Rules

| If | Then |
|----|------|
| `detected: false` and `firewall: "None"` | No signature match; generic detection may still run with `-a` |
| `firewall: "Generic"` | WAF-like behaviour, unknown product — SpiderFeet **skips** WEBSERVER_TECHNOLOGY for Generic |
| Multiple WAF entries in array | `-a` found stacked/CDN+WAF products; emit each distinct vendor |
| Site down / timeout | Increase `-T`; check URL scheme; verify host resolves |
| Behind redirect to different host | Default follows redirects; use `-r` to test original URL only |
| Need one product test | `-t "Cloudflare (Cloudflare Inc.)"` — name from `wafw00f -l` |
| Corporate egress required | `-p http://proxy:8080` or `socks5://host:1080` |
| Custom browser fingerprint | `-H headers.txt` (colon-delimited `Name: value` lines) |
| Bulk scan | `-i urls.json` or `wafw00f -a -o- -f json url1 url2 url3` |

## Guardrails & Pitfalls

- **Intrusive probes** — wafw00f sends XSS, SQLi, LFI, and RCE-like test strings. Authorized targets only.
- **Generic is not a product** — do not report as definitive WAF vendor.
- **stdout vs stderr** — JSON goes to stdout with `-o-`; use `-o- -f json` together (SpiderFeet pattern).
- **Parse as array** — output is JSON **array**, even for single URL.
- **300s timeout** — SpiderFeet module uses 300s subprocess timeout.
- **Windows colours** — `--no-colors` if log capture breaks on ANSI codes.

## Strategies and Tactics

**Pre-CMS / pre-Nuclei gate**

```
INTERNET_NAME → wafw00f -a -o- -f json → if WAF detected, tune CMSeeK UA and Nuclei rate
```

**Maximize detections**

1. Default: `wafw00f -a -o- -f json URL` (findall + generic fallback)
2. If empty: `-v -v` for debug, verify redirect final URL
3. If CDN obscures origin: scan origin IP/host if known from PIUS/passive DNS

**Evade false negative**

- Custom headers mimicking mobile app or internal client (`-H`)
- Proxy through region matching target (`-p`)
- Test specific WAF hypothesis (`-t`) after `wafw00f -l`

## Examples

### SpiderFeet default

```bash
wafw00f -a -o- -f json https://example.com
```

### Single WAF mode (faster)

```bash
wafw00f -o- -f json https://example.com
```

### List detectable products

```bash
wafw00f -l
```

### Test only Cloudflare

```bash
wafw00f -t "Cloudflare (Cloudflare Inc.)" -o- -f json https://example.com
```

### No redirect follow

```bash
wafw00f -r -a -o- -f json https://example.com
```

### Proxy

```bash
wafw00f -a -p http://127.0.0.1:8080 -o- -f json https://example.com
```

### Custom headers file

```bash
wafw00f -a -H headers.txt -o- -f json https://example.com
```

### Bulk from JSON input

```bash
wafw00f -a -i targets.json -o- -f json
# targets.json: [{"url":"https://a.com"},{"url":"https://b.com"}]
```

### Save to file

```bash
wafw00f -a -o results.json -f json https://example.com
```

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `cli-options.md` | Full CLI flags |
| `json-output-schema.md` | stdout JSON array schema |
| `nugget-mapping.md` | `WEBSERVER_TECHNOLOGY`, `RAW_RIR_DATA` |
| `tactics.md` | Adaptive sequences |
| `sources.md` | Upstream docs |

Operator guides: `.docs/docs-for-cli-tools/WAFWOOF-Zero-to-Hero.md`, `WAFWOOF-CLI-Options.md`.
