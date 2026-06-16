# PIUS Plugins and Three-Phase Pipeline

Pius discovers organizational assets through **26 plugins** orchestrated in a **three-phase pipeline** (plus late-stage enrichment). Plugins register via Go `init()` in `pkg/plugins/`.

## Pipeline overview

```
pius run --org "Acme" --domain acme.com
         │
         ▼
   Plugin Registry (mode filter: passive/active/all)
         │
┌────────┴──────────────────────────────────────┐
│ Phase 0 — Independent (concurrent)          │
│   Domain + direct CIDR plugins                │
│   crt-sh, gleif, passive-dns, asn-bgp, …    │
└────────┬──────────────────────────────────────┘
         │ domains, CIDRs
┌────────┴──────────────────────────────────────┐
│ Phase 1 — Handle discovery (concurrent)     │
│   whois, edgar                                │
└────────┬──────────────────────────────────────┘
         │ RIR org handles → Input.Meta
         ▼ enrichWithHandles()
┌────────┴──────────────────────────────────────┐
│ Phase 2 — Handle resolution (concurrent)    │
│   arin, ripe, lacnic (RDAP)                   │
│   apnic, afrinic (cached RPSL)                │
└────────┬──────────────────────────────────────┘
         │ CIDR blocks
         ▼ enrichWithAssets() — Meta["cidrs"], Meta["discovered_domains"]
┌────────┴──────────────────────────────────────┐
│ Late stage (Phase 3) — Asset consumers      │
│   dns-permutation, reverse-ip, builtwith, …   │
└────────┬──────────────────────────────────────┘
         ▼
   filterOutput() — drop cidr-handle
         ▼
   terminal | json | ndjson
```

## Phase reference

| Phase | Purpose | Emits |
|-------|---------|-------|
| **0** | Independent OSINT / direct lookups | `domain`, `cidr` |
| **1** | Map org name → RIR handles | `cidr-handle` (internal) |
| **2** | Map handles → CIDR blocks | `cidr` |
| **3** | Enrich from discovered domains/CIDRs | `domain` (additional) |

## Domain plugins (Phase 0 unless noted)

| Plugin | Source | Auth | Mode | Notes |
|--------|--------|------|------|-------|
| `crt-sh` | Certificate Transparency | None | Passive | Needs `--domain`; dedupes wildcards |
| `apollo` | Apollo.io API | `APOLLO_API_KEY` | Passive | 24h cache |
| `github-org` | GitHub org search | `GITHUB_TOKEN` opt | Passive | Confidence scored |
| `gleif` | GLEIF LEI registry | None | Passive | Parent/subsidiary |
| `passive-dns` | SecurityTrails | `SECURITYTRAILS_API_KEY` | Passive | Historical subdomains |
| `reverse-whois` | ViewDNS | `VIEWDNS_API_KEY` | Passive | 0.75 confidence typical |
| `whoxy-reverse-whois` | Whoxy API | `WHOXY_API_KEY` | Passive | Paginated |
| `builtwith` | BuiltWith | `BUILTWITH_API_KEY` | Passive | **Phase 3** — shared tracking codes |
| `dns-brute` | Local resolver | None | **Active** | 50 workers, wordlist |
| `dns-zone-transfer` | DNS AXFR | None | **Active** | A/AAAA/CNAME/MX/SRV |
| `doh-enum` | DNS-over-HTTPS | AWS opt | **Active** | DoH flags on CLI |
| `favicon-hash` | Shodan/FOFA | API keys | **Active** | MurmurHash3 favicon |
| `dns-permutation` | altdns-style | None | **Active** | **Phase 3** |
| `google-dorks` | Google Knowledge Graph | None | Passive | Subsidiary carousel |
| `reverse-ip` | PTR/ViewDNS | optional key | Passive | **Phase 3**, uses CIDRs |
| `wikidata` | SPARQL | None | Passive | Corporate relations |
| `censys-org` | Censys v3 | Censys tokens | **Active** | Domains + CIDRs |

## CIDR plugins

| Plugin | Phase | Source | Coverage |
|--------|-------|--------|----------|
| `asn-bgp` | 0 | RIPE RIS BGP | Global (needs `--asn`) |
| `shodan` | 0 | Shodan `net:` | Global |
| `whois` | 1 | All 5 RIRs | Handle discovery |
| `edgar` | 1 | SEC EDGAR | Public companies |
| `arin` | 2 | ARIN RDAP | North America |
| `ripe` | 2 | RIPE RDAP | Europe/Middle East/Central Asia |
| `lacnic` | 2 | LACNIC RDAP | Latin America |
| `apnic` | 2 | APNIC RPSL cache | Asia-Pacific |
| `afrinic` | 2 | AFRINIC RPSL cache | Africa |

## Meta enrichment between phases

Phase 1 populates `Input.Meta` keys such as:

- `arin_handles`, `ripe_handles`, `apnic_handles`, `afrinic_handles`, `lacnic_handles`

Phase 2+ uses:

- `cidrs` — comma-separated discovered CIDRs
- `discovered_domains` — comma-separated domains for Phase 3

## Plugin selection examples

```bash
# Default: all plugins that Accept() input + mode
pius run --org "Acme Corp" --domain acme.com

# Passive CT + RIR only
pius run --org "Acme" --domain acme.com --plugins crt-sh,whois,arin,ripe

# Skip EDGAR noise
pius run --org "Acme" --disable edgar

# Active DNS only
pius run --domain acme.com --mode active --plugins dns-brute,doh-enum
```

## Confidence model

Plugins like `github-org`, `reverse-whois`, and `apollo` call `SetConfidence()`:

| Range | Behaviour |
|-------|-----------|
| &lt; 0.35 | Dropped |
| 0.35 – 0.65 | Emitted with `needs_review` |
| ≥ 0.65 | Emitted as high confidence |

## Adding custom plugins

Implement `plugins.Plugin` (7 methods), register in `init()`, blank-import in `pkg/plugins/all/all.go`. See upstream `CONTRIBUTING` in GitHub repo.
