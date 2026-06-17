---
name: pius
description: Organizational attack-surface discovery with Pius — domains, subdomains, and RIR CIDRs from org names. Use when running pius run --output ndjson, mapping INTERNET_NAME and NETBLOCK_OWNER nuggets, piping to Nuclei/Nmap/Nerva, or configuring the 3-phase plugin pipeline.
---

# PIUS — Attack Surface Discovery

## Purpose

Use when you need to **map an organization's external assets** from a company name: domains, subdomains, and IP CIDR blocks via certificate transparency, RIR registries, passive DNS, and 26 plugins. Default output for pipelines: **NDJSON** (`--output ndjson`).

Install: `go install github.com/praetorian-inc/pius/cmd/pius@latest`

## Step-by-Step Instructions

1. **Install binary** — Go 1.25+; ensure `$GOPATH/bin` or `$HOME/go/bin` on PATH.
2. **Gather hints** — `--org` required; add `--domain` and/or `--asn` to unlock more plugins.
3. **Choose mode** — `--mode passive` (default, OSINT only), `active` (DNS brute, zone transfer, DoH), or `all`.
4. **Run with NDJSON** — one JSON object per line for streaming:

```bash
pius run --org "Acme Corp" --domain acme.com --output ndjson
```

5. **Filter findings** — `Type` is `domain` or `cidr` (Go JSON field names are capitalized).
6. **Map to nuggets** — domains → `INTERNET_NAME`; CIDRs → `NETBLOCK_OWNER` (with org context in data).
7. **Pipe downstream** — CIDRs to port scanners, domains to WAFWOOF/CMSeeK/Nuclei/Nerva.
8. **Review low confidence** — `Data.needs_review` and `Data.confidence` on ambiguous matches.

## If/Then Decision Rules

| If | Then |
|----|------|
| No domains without `--domain` | Add `--domain known.example.com` to enable crt-sh, passive-dns, DNS plugins |
| No CIDRs | Ensure Phase 1 ran (`whois`, `edgar`); try alternate org spellings |
| API plugin skipped | Set env var (`SECURITYTRAILS_API_KEY`, `VIEWDNS_API_KEY`, etc.) |
| Need intrusive DNS | `--mode active` or `--mode all` |
| Too slow / rate limited | Lower `--concurrency`; restrict `--plugins` |
| Stale APNIC/AFRINIC | `rm -rf ~/.pius/cache/` |
| Noisy low-confidence rows | Filter `Data.needs_review == true` or `confidence < 0.65` |
| CIDR-only pipeline | `jq` select `Type == "cidr"` → Nmap/naabu/Nerva |
| Domain-only pipeline | `jq` select `Type == "domain"` → WAFWOOF/Nuclei |
| Plugin list unknown | `pius list` |

## Guardrails & Pitfalls

- **Authorization** — passive OSINT still queries third parties about the org; active mode sends DNS traffic to targets.
- **JSON field casing** — NDJSON uses Go struct fields: `Type`, `Value`, `Source`, `Data` (not lowercase `type`).
- **Internal handles filtered** — `cidr-handle` findings never appear in final output.
- **Confidence** — `needs_review` findings (≈0.35–0.65) need human validation before treating as in-scope.
- **Org name ambiguity** — "Acme" may return unrelated entities; use `--domain` hint and confidence filters.
- **Do not use TextFSM** — NDJSON/JSON native parse only.

## Strategies and Tactics

**Passive baseline**

```bash
pius run --org "Acme Corporation" --domain acme.com --output ndjson
```

**CIDR-focused (RIR pipeline)**

```bash
pius run --org "Acme Corporation" --plugins whois,edgar,arin,ripe,apnic,afrinic,lacnic --output ndjson
```

**Full active expansion (authorized)**

```bash
pius run --org "Acme Corp" --domain acme.com --mode all --output ndjson
```

**Stream to Nuclei/Nmap/Nerva**

```bash
pius run --org "Acme" --domain acme.com --output ndjson \
  | jq -r 'select(.Type=="domain") | .Value' > domains.txt

pius run --org "Acme" --output ndjson \
  | jq -r 'select(.Type=="cidr") | .Value' > cidrs.txt
```

## Examples

### Minimal passive

```bash
pius run --org "Acme Corp" --output ndjson
```

### With domain hint (recommended)

```bash
pius run --org "Acme Corp" --domain acme.com --output ndjson
```

### ASN hint + BGP

```bash
pius run --org "Acme Corp" --asn AS12345 --plugins asn-bgp --output ndjson
```

### Plugin whitelist

```bash
pius run --org "Acme Corp" --domain acme.com --plugins crt-sh,gleif,whois,arin --output ndjson
```

### Disable noisy plugins

```bash
pius run --org "Acme Corp" --disable edgar,dns-brute --output ndjson
```

### JSON array (not streaming)

```bash
pius run --org "Acme Corp" --output json > acme.json
```

### List plugins

```bash
pius list
```

### High concurrency

```bash
pius run --org "Acme Corp" --domain acme.com --concurrency 10 --output ndjson
```

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `cli-options.md` | `pius run` flags and env vars |
| `ndjson-output-schema.md` | Finding record schema |
| `plugins-and-phases.md` | 3-phase pipeline and plugin catalog |
| `nugget-mapping.md` | `INTERNET_NAME`, `NETBLOCK_OWNER` |
| `tactics.md` | Adaptive discovery sequences |
| `sources.md` | GitHub, Praetorian blog |

Operator guides: `.docs/docs-for-cli-tools/PIUS-Zero-to-Hero.md`, `PIUS-CLI-Options.md`.
