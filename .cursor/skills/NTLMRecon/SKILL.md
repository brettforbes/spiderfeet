---
name: NTLMRecon
description: Discover HTTP(S) NTLM auth endpoints and extract unauthenticated challenge metadata (domain, host, DNS, forest) with Praetorian Go NTLMRecon. Trigger on NTLM challenge enumeration, Windows domain reconnaissance, Exchange/ADFS/EWS/OAB/Rpc path discovery. HTTP NTLM endpoint recon — not SMB.
---

# NTLMRecon — HTTP NTLM Endpoint Discovery and Challenge Metadata

## Purpose

Use when you must **find HTTP(S) paths that offer NTLM authentication** and **extract Active Directory metadata** from NTLM CHALLENGE_MESSAGE responses on authorized targets — without credentials. Canonical binary: **[praetorian-inc/NTLMRecon](https://github.com/praetorian-inc/NTLMRecon)** (Go). Preferred SpiderFeet command: **`NTLMRecon -t <URL> -o json`**.

This tool probes **web** endpoints (Exchange, ADFS, IIS, etc.). It is **not** SMB/NetBIOS port scanning or SMB auth fingerprinting — do not use it as a substitute for `smbclient`, Impacket, or nmap SMB scripts.

Do **not** confuse with the legacy Python **`ntlmrecon`** ([pwnfoo/NTLMRecon](https://github.com/pwnfoo/NTLMRecon)) — different flags and CSV output (see `references/python-fork.md`).

**Binary (this host):** `/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon` (also `C:\projects\spiderfeet\.tools\NTLMRecon\NTLMRecon`). Run via **WSL** on Windows. Case-sensitive name: **`NTLMRecon`**.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized URLs only. The tool sends unauthenticated NTLM negotiate probes across an embedded path wordlist (~70 Exchange/ADFS/IIS paths).
2. **Validate tooling** — `NTLMRecon --help` (exact capture in `references/cli-options.md` and `.docs/docs-for-cli-tools/NTLMRecon-CLI-Options.md`).
3. **Normalize target URL** — `-t` requires a full URL with scheme (`https://autodiscover.contoso.com`). Confirm live HTTPS/HTTP with **httpx** first when needed.
4. **Run JSON capture (formal examination / nuggets)** — one target per invocation:

```bash
NTLMRecon -t https://autodiscover.contoso.com -o json
```

5. **Parse JSON lines** — each hit is one object: `url` + `ntlm` (`netbiosComputerName`, `netbiosDomainName`, `dnsDomainName`, `dnsComputerName`, `forestName`). See `references/output-schema.md`.
6. **Map nuggets** — per `references/nugget-mapping.md`: prefer catalogue **`INTERNET_NAME`**, **`DOMAIN_NAME`**, **`LINKED_URL_INTERNAL`**; optional **`RAW_RIR_DATA`**.
7. **Handle clean miss** — empty stdout with exit 0 is valid when no paths return NTLM; still produce scan metadata in the structured bundle.
8. **Chain downstream** — correlate DNS/PIUS domains; flag high-value paths (`/EWS/`, `/adfs/`, `/Autodiscover/`) for MFA-bypass research **within scope**.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-o json`; never rely on plaintext URL list alone |
| Target is bare IP or hostname | Prefix with `https://` (or `http://`); confirm scheme with httpx first |
| Operator asks for “SMB NTLM recon” | Clarify this skill is **HTTP NTLM paths only**; use SMB tooling separately |
| Virtual host required (IP → mail FQDN) | Build from **main** (`-H` in README; **not in v1.1.0 release binary**) |
| No hits on autodiscover host | Retry apex, `www`, ADFS URL, or Exchange CAS hostname variants |
| Need bulk CIDR / file input | Go v1.1.0 has **no** batch flag — loop externally; do not invent Python `--input` flags on this binary |
| Troubleshooting probe failures | Build from **main** with `-debug` (not in v1.1.0) or capture HTTP manually |
| All embedded paths return same metadata | Tool may collapse to `/*` wildcard URL when every path matches |
| Empty JSON on known Exchange | Prefer FQDN in `-t`; confirm TLS/443; check WAF blocking NTLM headers |
| Rate limited / fragile target | One URL at a time; Go tool is sequential (no `-threads` in praetorian build) |

## Guardrails & Pitfalls

- **Authorization** — NTLM endpoint probing is active recon; permitted assets only.
- **Two different tools** — Praetorian **`NTLMRecon`** (Go, `-t` / `-o`) vs pwnfoo **`ntlmrecon`** (Python, `--input` / `--infile`). SpiderFeet corpus targets the Go tool. Never apply Python flags to the Go binary.
- **HTTP ≠ SMB** — Challenge metadata describes AD identity leaked over **HTTP NTLMSSP**; it does not prove SMB exposure.
- **Single URL per run** — v1.1.0 accepts one `-t` target; no stdin batch.
- **Structured-first** — JSON mode is mandatory for graph derivation; plaintext is human review only.
- **No credentials** — metadata comes from challenge packets only; do not add password spraying in this skill.
- **TLS verification disabled internally** — `InsecureSkipVerify`; that is probe behaviour, not a target vuln claim.
- **HTTP/1.1 only** — by design; HTTP/2 not used.
- **Inferential attribution** — NetBIOS/DNS names come from the server challenge; corroborate with DNS/inventory before high-confidence reporting.
- **Release vs main drift** — README documents `-H` and `-debug`; **v1.1.0 release binary only exposes `-t` and `-o`** (live capture 2026-08-10).

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Captured help, `-t` / `-o`, release vs main |
| `output-schema.md` | JSON / plaintext shapes, bundles, errors |
| `nugget-mapping.md` | JSON → SpiderFeet graph |
| `tactics.md` | Sequencing, pipelines, thin yield |
| `endpoints-and-behavior.md` | Embedded paths, probe logic |
| `python-fork.md` | Legacy pwnfoo CLI (not canonical) |
| `sources.md` | Official and ecosystem URLs |

Operator guides: `.docs/docs-for-cli-tools/NTLMRecon-Zero-to-Hero.md`, `NTLMRecon-CLI-Options.md`.

## Comprehensive Examples

### TARGET SELECTION

```bash
NTLMRecon -t https://autodiscover.contoso.com
NTLMRecon -t https://adfs.contoso.com -o json
NTLMRecon -t https://mail.contoso.com -o json
# IP + Host header requires main-branch build with -H (not v1.1.0)
```

### OUTPUT MODES

```bash
# Plaintext — one discovered URL per line (default)
NTLMRecon -t https://autodiscover.contoso.com

# JSON — one object per line (SpiderFeet structured capture)
NTLMRecon -t https://autodiscover.contoso.com -o json
```

### PREFERRED SPIDERFEET COMMAND

```bash
/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon \
  -t https://autodiscover.contoso.com -o json
```

### EXTERNAL BATCH LOOP (Go v1.1.0)

```bash
while read -r base; do
  NTLMRecon -t "$base" -o json
done < live_urls.txt
```

### PIPELINES

```bash
# Live web URLs → NTLM JSON per host
httpx -l hosts.txt -silent -json | jq -r '.url' | while read -r u; do
  NTLMRecon -t "$u" -o json
done

# Org recon chain (conceptual)
# subfinder → httpx → NTLMRecon -o json → dnsx (validate dnsDomainName)
```

### PARSE ONE JSON LINE (Python)

```python
import json

line = '{"url":"https://autodiscover.contoso.com/EWS/","ntlm":{"netbiosComputerName":"MSEXCH1","netbiosDomainName":"CONTOSO","dnsDomainName":"na.contoso.local","dnsComputerName":"msexch1.na.contoso.local","forestName":"contoso.local"}}'
row = json.loads(line)
host = row["url"]  # → INTERNET_NAME / LINKED_URL_INTERNAL
domain = row["ntlm"]["dnsDomainName"]  # → DOMAIN_NAME
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **High-value hosts first** — `autodiscover`, ADFS, legacy Exchange/O365 hybrid endpoints.
2. **JSON on confirmed live URLs** — httpx → `NTLMRecon -t <url> -o json` per URL.
3. **Correlate challenge metadata** — match `dnsDomainName` / `forestName` to PIUS org seeds and DNS zones as `DOMAIN_NAME`.
4. **Prioritize sensitive paths** — `/EWS/`, `/adfs/services/trust/`, `/Microsoft-Server-ActiveSync/` for follow-up review.
5. **Clean miss is signal** — no NTLM endpoints may mean modern auth-only or edge blocking; record as sparse scan, not failure.
