# Subfinder JSONL → SpiderFeet Nugget Mapping

Convert **`-oJ`** JSON Lines into graph payloads with explicit `nodes[]` and `edges[]` arrays.

Aligns with `sfp_sublist3r` behavior: resolved hosts → **`INTERNET_NAME`**; unresolved → **`INTERNET_NAME_UNRESOLVED`**.

## Node conversion

| subfinder signal | Node type | `data` | Notes |
|------------------|-----------|--------|-------|
| `host` (resolves) | `INTERNET_NAME` | fqdn | After dnsx or `-active` confirmation |
| `host` (passive only) | `INTERNET_NAME_UNRESOLVED` | fqdn | Until dnsx proves A/AAAA |
| `host` (child of seed) | `AFFILIATE_INTERNET_NAME` | fqdn | Optional when seed is `DOMAIN_NAME` and policy distinguishes affiliate children |
| `ip` (with `-oI`) | `IP_ADDRESS` | ip | From active resolution |
| `sources` / `source` | metadata | string[] | Provenance on host node |

**Recommendation:** Use `INTERNET_NAME` / `INTERNET_NAME_UNRESOLVED` for corpus parity with `sfp_sublist3r`; use `AFFILIATE_INTERNET_NAME` when ontology requires explicit parent-domain affiliation edges.

## Edge conversion

| Relationship | Edge shape |
|--------------|------------|
| seed domain → subdomain | `DOMAIN_NAME` → `AFFILIATE_INTERNET_NAME` or `INTERNET_NAME` (`child_of` / `affiliate_of`) |
| host resolves to IP | `INTERNET_NAME` → `IP_ADDRESS` (`resolves_to`) |
| parent INTERNET_NAME → discovered host | `INTERNET_NAME` → `INTERNET_NAME` (`subdomain_of`) |

## Example: passive JSONL only

Input:

```jsonl
{"host":"api.example.com","source":"crtsh"}
{"host":"www.example.com","source":"hackertarget"}
```

Output contract:

```json
{
  "nodes": [
    {"type": "DOMAIN_NAME", "data": "example.com"},
    {"type": "INTERNET_NAME_UNRESOLVED", "data": "api.example.com", "meta": {"sources": ["crtsh"]}},
    {"type": "INTERNET_NAME_UNRESOLVED", "data": "www.example.com", "meta": {"sources": ["hackertarget"]}}
  ],
  "edges": [
    {"source": "example.com", "target": "api.example.com", "relationship": "affiliate_of"},
    {"source": "example.com", "target": "www.example.com", "relationship": "affiliate_of"}
  ]
}
```

## Example: active JSONL with IP

Input:

```jsonl
{"host":"api.example.com","ip":"203.0.113.20"}
```

```json
{
  "nodes": [
    {"type": "INTERNET_NAME", "data": "api.example.com"},
    {"type": "IP_ADDRESS", "data": "203.0.113.20"}
  ],
  "edges": [
    {"source": "api.example.com", "target": "203.0.113.20", "relationship": "resolves_to"}
  ]
}
```

## Deduplication

- Node key: `type + normalized fqdn` (or `type + ip`).
- Skip if host equals seed apex already present as `DOMAIN_NAME`.
- Merge `sources` arrays when duplicate host lines appear.

## Provenance fields (corpus / Tests tab)

Every node should record:

- `source_tool`: `subfinder`
- `source_command`: full CLI string
- `source_artifact`: path to `.jsonl`
- `passive_sources`: from `-cs` when present
- `resolution`: `passive` | `active` | `dnsx_confirmed`

## Downstream edges

| Next tool | Input from subfinder |
|-----------|----------------------|
| dnsx | FQDN list (stdin or file) |
| httpx | Live hostnames |
| naabu | Resolvable hosts / IPs |
| nuclei | httpx URLs |

## Do not emit

- Duplicate apex `DOMAIN_NAME` as a discovery
- `IP_ADDRESS` without a host or seed context
- Out-of-scope domains not matching target allowlist

## Promotion after dnsx

When dnsx confirms resolution, upgrade node type:

`INTERNET_NAME_UNRESOLVED` → `INTERNET_NAME` and add `IP_ADDRESS` + `resolves_to` edges from dnsx JSON.
