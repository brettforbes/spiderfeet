# dnsx JSONL → SpiderFeet Nugget Mapping

Convert **`-json`** JSON Lines into graph payloads with `nodes[]` and `edges[]`. Catalogue ids from `.docs/analysis/nuggets.json` / `nuggets_extension.json`.

**IP literals:** create address nodes only via `core.ip_classify.classify_ip` (IPv4 → `IPV4_ADDRESS` / related; IPv6 → `IPV6_ADDRESS`). Do not hardcode `IP_ADDRESS` for colon-form values. (Legacy docs may say `IP_ADDRESS`; prefer classifier output.)

## Primary mappings

| dnsx field / signal | nugget_id | `data` / notes |
|---------------------|-----------|----------------|
| `host` (has A/AAAA or useful answers) | `INTERNET_NAME` | FQDN |
| `host` (confirmed non-existent / no useful answers after validation policy) | `INTERNET_NAME_UNRESOLVED` | FQDN — use when scenario tracks misses |
| each `a[]` / `aaaa[]` IP | classifier result | Via `classify_ip` |
| each `cname[]` target | `INTERNET_NAME` | Canonical name |
| each `ns[]` | `INTERNET_NAME` + optional `PROVIDER_DNS` | Nameserver host; provider when catalogued |
| each `mx[]` (non-empty host) | `INTERNET_NAME` + optional `PROVIDER_MAIL` | Mail exchanger |
| `txt[]` generic | `DNS_TEXT` | Full TXT string |
| `txt[]` starting `v=spf1` | `DNS_SPF` | Prefer over generic TXT |
| `srv[]` | `DNS_SRV` | Serialized SRV target/port |
| SOA / AXFR / CAA / raw `all[]` | `RAW_DNS_RECORDS` | When keeping wire or authority blobs |
| `-cdn` label | `PROVIDER_HOSTING` (or meta) | When CDN name present |
| `-asn` info | `BGP_AS_OWNER` / member meta | When ASN payload present |
| PTR `ptr[]` | `INTERNET_NAME` | Reverse name; link from IP node |

## Edges (practical)

Prefer shared ontology relations (`contains`, `had`) when promoting to TypeDB; examination graphs often use descriptive relationship labels for operator review:

| Relationship | Shape |
|--------------|--------|
| host → IPv4/IPv6 | `INTERNET_NAME` → address (`resolves_to` / `had`) |
| host → CNAME | `INTERNET_NAME` → `INTERNET_NAME` (`had` / alias) |
| domain → NS | `INTERNET_NAME` → NS name (`had`) |
| domain → MX | `INTERNET_NAME` → MX name (`had`) |
| host → TXT/SPF/SRV | `INTERNET_NAME` → descriptor (`had`) |
| IP → PTR name | address → `INTERNET_NAME` (`had`) |

## Example: A/AAAA row

Input:

```json
{
  "host": "scanme.nmap.org",
  "a": ["45.33.32.156"],
  "aaaa": ["2600:3c01::f03c:91ff:fe18:bb2f"],
  "status_code": "NOERROR"
}
```

Output contract (illustrative):

```json
{
  "nodes": [
    {"type": "INTERNET_NAME", "data": "scanme.nmap.org"},
    {"type": "IPV4_ADDRESS", "data": "45.33.32.156"},
    {"type": "IPV6_ADDRESS", "data": "2600:3c01::f03c:91ff:fe18:bb2f"}
  ],
  "edges": [
    {"source": "scanme.nmap.org", "target": "45.33.32.156", "relationship": "resolves_to"},
    {"source": "scanme.nmap.org", "target": "2600:3c01::f03c:91ff:fe18:bb2f", "relationship": "resolves_to"}
  ]
}
```

## Example: TXT / SPF / NS

```json
{
  "host": "example.com",
  "ns": ["elliott.ns.cloudflare.com"],
  "txt": ["v=spf1 -all"]
}
```

→ `INTERNET_NAME` (`example.com`) `had` `DNS_SPF` (`v=spf1 -all`); NS name as `INTERNET_NAME` + optional `PROVIDER_DNS`.

## Deduplication

- Node identity: `nugget_instance_id = f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}"` via shared `graph_builder`.
- Exactly one node per `(nugget_id, nugget_data)`.
- Deduplicate host→IP and host→CNAME edges before ingestion.
- Skip empty MX targets (e.g. `"."` / `""` null MX).

## Provenance (corpus / Tests tab)

- `source_tool`: `dnsx`
- `source_command`: full CLI
- `source_artifact`: path to JSONL or harvest bundle
- `query_profile`: flags used (`-a -aaaa -cname`, …)

## Downstream

| Tool | Input |
|------|--------|
| httpx | `host` values (or hostnames from text pipe) |
| naabu | Resolved hosts / IPs |
| nuclei | Live URLs after httpx |

## Do not emit

- Address nuggets without `classify_ip`
- `DNS_SPF` for non-SPF TXT
- Treating SERVFAIL as a confirmed hostname
- Orphan TXT/IP nodes with no host edge
