---
name: wafwoof
description: Fingerprint Web Application Firewalls with wafw00f (WAFWOOF). Use when detecting Cloudflare, Akamai, AWS WAF, etc., parsing JSON from wafw00f -a -o- -f json, mapping WEBSERVER_TECHNOLOGY and RAW_RIR_DATA, or running sfp_tool_wafw00f.
---

# WAFWOOF (wafw00f) — Web Application Firewall Fingerprinting

## Purpose

Use when you need to **detect and identify WAF products** protecting a web target before deeper scanning. wafw00f sends benign and attack-like HTTP probes, matches responses against hundreds of vendor signatures, and can report named products or generic WAF-like behaviour. SpiderFeet emits `WEBSERVER_TECHNOLOGY` (vendor + product) and `RAW_RIR_DATA` (full JSON array on stdout).

**Binary name:** `wafw00f` (three zeros). Skill directory: `wafwoof`.

## Step-by-Step Instructions

1. **Install** — `pip install wafw00f` (SpiderFeet venv: `.\.venv\Scripts\pip.exe install wafw00f`); confirm with `wafw00f --version`.
2. **Normalize URL** — wafw00f prepends `https://` if scheme missing. SpiderFeet passes `INTERNET_NAME` as URL.
3. **Run JSON scan (SpiderFeet default)** — find all matching WAFs, JSON on stdout:

```bash
wafw00f -a -o- -f json https://example.com
```

4. **Parse JSON array** — each element is one detection result (see `references/json-output-schema.md`).
5. **Map to nuggets** — full array → `RAW_RIR_DATA`; each non-Generic named detection → `WEBSERVER_TECHNOLOGY` as `"<manufacturer> <firewall>"`.
6. **Adapt if blocked or empty** — try `-H headers.txt`, `-p proxy`, `-r` (no redirect), `-T` timeout, `-v -v` debug, or `-t` single-WAF test.
7. **Batch targets** — multiple URLs on CLI, or `-i targets.json` with `url` field per row.
8. **Chain downstream** — tune CMSeeK user-agent and Nuclei rate/templates based on detected WAF.

## If/Then Decision Rules

| If | Then |
|----|------|
| `detected: false` and `firewall: "None"` | No signature match; with `-a`, generic row may still appear |
| `firewall: "Generic"` | WAF-like behaviour, unknown product — SpiderFeet **skips** WEBSERVER_TECHNOLOGY for Generic |
| Multiple WAF entries in array | `-a` found stacked/CDN+WAF products; emit each distinct vendor |
| Site down / timeout | Increase `-T`; check URL scheme; verify host resolves; use `-v -v` |
| Behind redirect to different host | Default follows redirects; use `-r` to test original URL only |
| Need one product test | `-t "Cloudflare (Cloudflare Inc.)"` — name from `wafw00f -l` (quote spaces) |
| Corporate egress required | `-p http://proxy:8080` or `socks5://host:1080` |
| Custom browser fingerprint | `-H headers.txt` (colon-delimited `Name: value` lines; **replaces** defaults) |
| Bulk scan | `-i urls.json` or `wafw00f -a -o- -f json url1 url2 url3` |
| Log capture breaks on ANSI | Add `--no-colors` |
| Faster first-match only | Omit `-a` (stop at first signature) |
| Need CSV or text export | `-o file.csv` or `-o file.txt` / `-f csv` / `-f text` |

## Guardrails & Pitfalls

- **Intrusive probes** — wafw00f sends XSS, SQLi, LFI, XXE, and RCE-like test strings. Authorized targets only.
- **Generic is not a product** — do not report as definitive WAF vendor.
- **stdout vs stderr** — JSON goes to stdout with `-o- -f json`; human art/diagnostics may appear on stderr.
- **Parse as array** — output is JSON **array**, even for single URL.
- **300s timeout** — SpiderFeet module uses 300s subprocess timeout.
- **`-H` replaces defaults** — partial header files drop wafw00f's Chrome-on-Windows set entirely.
- **`-t` names must match `-l`** — include manufacturer parenthesis exactly as listed.
- **Do not use TextFSM** — native JSON is the structured source.

## Strategies and Tactics

**Pre-CMS / pre-Nuclei gate**

```
INTERNET_NAME → wafw00f -a -o- -f json → if WAF detected, tune CMSeeK UA and Nuclei rate
```

**Maximize detections**

1. Default: `wafw00f -a -o- -f json URL` (findall + generic fallback)
2. If empty: `-v -v` for debug, compare with/without `-r`
3. If CDN obscures origin: scan origin IP/host if known from PIUS/passive DNS

**Evade false negative**

- Custom headers mimicking mobile app or internal client (`-H`)
- Proxy through region matching target (`-p`)
- Test specific WAF hypothesis (`-t`) after `wafw00f -l`
- Increase `-T` on slow targets

**Bulk asset sweep**

- `-i urls.json` for structured batch; cap parallelism to avoid WAF rate blocks
- SpiderFeet module scans one `INTERNET_NAME` per event — manual bulk for corpus

See `references/tactics.md` for full decision matrix.

## Comprehensive Examples

### Help and version

```bash
wafw00f -h
wafw00f --help
wafw00f -V
wafw00f --version
```

### SpiderFeet default (findall + JSON stdout)

```bash
wafw00f -a -o- -f json https://example.com
```

### Single-match mode (faster, stop at first WAF)

```bash
wafw00f -o- -f json https://example.com
```

### Verbose debug

```bash
wafw00f -v -a -o- -f json https://example.com
wafw00f -v -v -a -o- -f json https://example.com
```

### List detectable products

```bash
wafw00f -l
wafw00f --list
```

### Test one specific WAF

```bash
wafw00f -t "Cloudflare (Cloudflare Inc.)" -o- -f json https://example.com
wafw00f -t "AWS Elastic Load Balancer (Amazon)" -o- -f json https://example.com
```

### No redirect follow

```bash
wafw00f -r -a -o- -f json https://example.com
wafw00f --noredirect -a -o- -f json https://example.com
```

### Proxy

```bash
wafw00f -a -p http://127.0.0.1:8080 -o- -f json https://example.com
wafw00f -a -p socks5://127.0.0.1:1080 -o- -f json https://example.com
wafw00f -a -p http://user:pass@proxy.corp:8080 -o- -f json https://example.com
```

### Custom headers file

```bash
wafw00f -a -H headers.txt -o- -f json https://example.com
```

`headers.txt`:

```
User-Agent: MyApp/2.0 (Internal)
Accept: application/json
```

### Request timeout

```bash
wafw00f -T 15 -a -o- -f json https://example.com
wafw00f --timeout 30 -a -o- -f json https://example.com
```

### Disable ANSI colours

```bash
wafw00f --no-colors -a -o- -f json https://example.com
```

### Multiple URLs (positional)

```bash
wafw00f -a -o- -f json https://a.com https://b.com https://c.com
```

### Bulk from input file

```bash
wafw00f -a -i targets.json -o- -f json
wafw00f -a -i targets.csv -o- -f json
wafw00f -a -i urls.txt -o- -f json
```

`targets.json`:

```json
[{"url": "https://a.com"}, {"url": "https://b.com"}]
```

### Save to file (format by extension or `-f`)

```bash
wafw00f -a -o results.json https://example.com
wafw00f -a -o results.csv -f csv https://example.com
wafw00f -a -o results.txt -f text https://example.com
wafw00f -a -o - -f json https://example.com
```

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `cli-options.md` | Full CLI flags + captured help |
| `json-output-schema.md` | stdout JSON array schema |
| `nugget-mapping.md` | `WEBSERVER_TECHNOLOGY`, `RAW_RIR_DATA` |
| `tactics.md` | Adaptive sequences |
| `sources.md` | Upstream docs |

Operator guides: `.docs/docs-for-cli-tools/WAFWOOF-Zero-to-Hero.md`, `WAFWOOF-CLI-Options.md`.
