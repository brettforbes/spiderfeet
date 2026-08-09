# tldfinder JSONL → SpiderFeet Nugget Mapping

Convert **`-oJ`** JSON Lines into graph payloads with explicit `nodes[]` and `edges[]`.

Align with subdomain-style mapping used by Subfinder / `sfp_sublist3r`: resolved hosts → **`INTERNET_NAME`**; unresolved → **`INTERNET_NAME_UNRESOLVED`**. Prefer catalogue types from `.docs/analysis/nuggets.json` / `nuggets_extension.json`.

## Node conversion

| tldfinder signal | Node type | `data` | Notes |
|------------------|-----------|--------|-------|
| `input` (private TLD label) | `INTERNET_NAME` or seed metadata | label / suffix | Keep as scan/seed context; not a public `DOMAIN_NAME` apex |
| `host` (passive only) | `INTERNET_NAME_UNRESOLVED` | fqdn | Until dnsx or `-active` proves A/AAAA |
| `host` (resolves) | `INTERNET_NAME` | fqdn | After dnsx or `-active` confirmation |
| `ip` (with `-oI`) | via `classify_ip` | ip | `IPV4_ADDRESS` / `IPV6_ADDRESS` / internal variants |
| `source` / `sources` | metadata | string / string[] | Provenance on host node |

## Edge conversion

| Relationship | Edge shape |
|--------------|------------|
| seed / private TLD → discovered host | seed → host (`contains` or affiliate-style edge per project mapping pack) |
| host resolves to IP | `INTERNET_NAME` → IP node (`had` / resolves relation per shared rules) |

Use shared `graph_builder` identity: `nugget_instance_id = f"{nugget_id}--{uuid5(...)}"`. No orphan nodes.

## Example: passive JSONL

Input:

```jsonl
{"host":"docs.sandbox.google","input":"google","source":"crtsh"}
{"host":"storage.google","input":"google","source":"crtsh"}
```

Output contract (illustrative):

```json
{
  "nodes": [
    {"type": "INTERNET_NAME", "data": "google", "meta": {"role": "private_tld_seed"}},
    {"type": "INTERNET_NAME_UNRESOLVED", "data": "docs.sandbox.google", "meta": {"sources": ["crtsh"]}},
    {"type": "INTERNET_NAME_UNRESOLVED", "data": "storage.google", "meta": {"sources": ["crtsh"]}}
  ],
  "edges": [
    {"source": "google", "target": "docs.sandbox.google", "relationship": "contains"},
    {"source": "google", "target": "storage.google", "relationship": "contains"}
  ]
}
```

## Example: active JSONL with IP

Input:

```jsonl
{"host":"cache2.c.play.google","ip":"142.250.183.46","input":"google","source":"crtsh"}
```

```json
{
  "nodes": [
    {"type": "INTERNET_NAME", "data": "cache2.c.play.google"},
    {"type": "IPV4_ADDRESS", "data": "142.250.183.46"}
  ],
  "edges": [
    {"source": "cache2.c.play.google", "target": "142.250.183.46", "relationship": "had"}
  ]
}
```

## Mode-specific mapping caution

| Mode | Mapping note |
|------|----------------|
| `-dm dns` | Primary private-TLD host expansion → `INTERNET_NAME*` under seed suffix |
| `-dm tld` | May emit public-looking FQDNs (`google.wf`); do **not** auto-label as private TLD without PSL/context checks |
| `-dm domain` | Map only after inspecting record density; sparse runs are valid clean-miss |

## Deduplication

- Node key: `nugget_id + normalized host/ip`.
- Merge `sources` when duplicate host lines appear.
- Skip emitting the seed label again as a “discovery” host if it equals `input` only.

## Provenance (corpus / Tests)

Record on each host node or scan metadata:

- tool: `tldfinder`
- command (full argv)
- `input`, `source`/`sources`
- discovery mode (`-dm`)
- exit status / duration when harvesting
