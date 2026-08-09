# NTLMRecon Nugget Mapping

Map **`-o json`** records to SpiderFeet nuggets. Reuse catalogue entries from `.docs/analysis/nuggets.json` (and extensions) before inventing types.

## Field → nugget (prefer catalogue)

| Source field | Nugget | Notes |
|--------------|--------|-------|
| Hostname from `url` | `INTERNET_NAME` | Parse host; strip port; lowercase |
| `ntlm.dnsComputerName` | `INTERNET_NAME` | Server FQDN from challenge |
| `ntlm.dnsDomainName` | `DOMAIN_NAME` | DNS domain (AD DNS name) |
| `ntlm.forestName` | `DOMAIN_NAME` | Forest / DNS tree root — may equal or parent `dnsDomainName` |
| `ntlm.netbiosDomainName` | `DOMAIN_NAME` | Short NetBIOS form; prefer DNS names when both exist for identity; keep NetBIOS as separate node when distinct |
| `ntlm.netbiosComputerName` | `RAW_RIR_DATA` | Short NetBIOS host label — no dedicated NetBIOS nugget; attach via `had` to the related `INTERNET_NAME` when useful |
| Full path `url` | `LINKED_URL_INTERNAL` | Discovered NTLM-enabled path |
| Full JSON line (optional) | `RAW_RIR_DATA` | Verbatim evidence string |

### Affiliate variants (reuse, do not invent)

Use **`AFFILIATE_INTERNET_NAME`** / **`AFFILIATE_DOMAIN_NAME`** only when challenge names clearly describe **third-party / partner** infrastructure relative to the seed org (same catalogue pattern as other affiliate findings). Default first pass: **`INTERNET_NAME`** + **`DOMAIN_NAME`**.

Do **not** emit `OPERATING_SYSTEM` from NTLM metadata alone — insufficient confidence.

## IP literals

Extract host from `url`; if value is IPv4/IPv6 literal, create address nodes only through `core.ip_classify.classify_ip` — never hardcode `IP_ADDRESS`.

## Topology pattern

```
SCAN (tool run)
  └── contains → INTERNET_NAME (target host from url)
        ├── had → DOMAIN_NAME (dnsDomainName, forestName, netbiosDomainName)
        ├── had → INTERNET_NAME (dnsComputerName)
        ├── had → RAW_RIR_DATA (netbiosComputerName / optional full JSON)
        └── contains → LINKED_URL_INTERNAL (discovered path URLs)
```

## Example graph payload

```json
{
  "nodes": [
    {"nugget_id": "INTERNET_NAME", "nugget_data": "autodiscover.contoso.com"},
    {"nugget_id": "INTERNET_NAME", "nugget_data": "msexch1.na.contoso.local"},
    {"nugget_id": "DOMAIN_NAME", "nugget_data": "na.contoso.local"},
    {"nugget_id": "DOMAIN_NAME", "nugget_data": "contoso.local"},
    {"nugget_id": "LINKED_URL_INTERNAL", "nugget_data": "https://autodiscover.contoso.com/EWS/"},
    {"nugget_id": "RAW_RIR_DATA", "nugget_data": "netbiosComputerName=MSEXCH1"}
  ],
  "edges": [
    {"from": "INTERNET_NAME--…", "to": "INTERNET_NAME--…", "relation": "had"},
    {"from": "INTERNET_NAME--…", "to": "DOMAIN_NAME--…", "relation": "had"},
    {"from": "INTERNET_NAME--…", "to": "LINKED_URL_INTERNAL--…", "relation": "contains"},
    {"from": "INTERNET_NAME--…", "to": "RAW_RIR_DATA--…", "relation": "had"}
  ]
}
```

Use shared `graph_builder.nugget_instance_id` for all node IDs. Exactly one node per `(nugget_id, nugget_data)`.

## Clean miss graph

Valid graph: scan head + target `INTERNET_NAME` with no child metadata nodes when `records` is empty.

## Intentionally unmapped

| Field / concept | Reason |
|-----------------|--------|
| HTTP status codes | Not in JSON output |
| Auth scheme on non-NTLM paths | Go tool skips; not in output |
| SMB signing / SMB dialect | **Not collected** — this is HTTP NTLM endpoint recon |
| MFA bypass as a nugget type | Operator finding narrative; no catalogue type |

Document gaps in the tool structure doc during corpus onboarding.
