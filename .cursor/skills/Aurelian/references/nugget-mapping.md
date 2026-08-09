# Aurelian Nugget Mapping

Map **redacted** Aurelian findings to SpiderFeet ontology nodes. Never use raw secret values, console federation URLs, or APIM subscription keys as `nugget_data`.

## Suggested nugget types

Reuse catalogue entries from `.docs/analysis/nuggets.json` (and extensions) before inventing types.

| Source | Nugget ID | Notes |
|--------|-----------|-------|
| Public / open cloud bucket or anonymous storage | `CLOUD_STORAGE_BUCKET_OPEN` / `CLOUD_STORAGE_BUCKET` | Prefer open variant when public access is confirmed |
| Internet-facing hostname / DNS name | `INTERNET_NAME` | From takeover or public resource DNS |
| Hijackable / dangling DNS candidate | `AFFILIATE_INTERNET_NAME_HIJACKABLE` or `INTERNET_NAME` | Use hijackable when evidence supports takeover class |
| Misconfig / IAM escalation / exposure finding (redacted) | `VULNERABILITY_GENERAL` | Not CVE unless a CVE id is present |
| Module / rule / technique / ARN descriptor | `RAW_RIR_DATA` | e.g. `module:find-secrets`, `technique:timestream`, policy name |
| Confirmed compromised credential (rare) | `PASSWORD_COMPROMISED` / account types | Only after confirmation — never store the secret string |
| IP belonging to AWS (from `ip-lookup`) | `IPV4_ADDRESS` / `IPV6_ADDRESS` via `classify_ip` | Attach `RAW_RIR_DATA` for service/region labels |
| Cloud account / subscription / project id | `RAW_RIR_DATA` | Until a catalogue/extension type is approved — do not invent `CLOUD_ACCOUNT` |

## Graph pattern

```
SCAN (scan head)
  └─contains─> FINDING (VULNERABILITY_GENERAL or CLOUD_STORAGE_BUCKET_OPEN — redacted)
        └─had─> DESCRIPTOR (RAW_RIR_DATA — module, severity, technique)
        └─had─> HOST_OR_NAME (INTERNET_NAME when DNS/URL shaped)
        └─had─> SCOPE (RAW_RIR_DATA — account/subscription/project)
```

Allowed relations: `contains`, `had`, `listens-to` per project ontology rules. Use shared `graph_builder.nugget_instance_id` only.

## Example payload (illustrative)

```json
{
  "nodes": [
    {
      "nugget_id": "CLOUD_STORAGE_BUCKET_OPEN",
      "nugget_data": "s3://example-public-bucket",
      "nugget_instance_id": "CLOUD_STORAGE_BUCKET_OPEN--<uuid5>"
    },
    {
      "nugget_id": "RAW_RIR_DATA",
      "nugget_data": "module:public-resources | cloud:aws | account:123456789012",
      "nugget_instance_id": "RAW_RIR_DATA--<uuid5>"
    },
    {
      "nugget_id": "INTERNET_NAME",
      "nugget_data": "assets.example.com",
      "nugget_instance_id": "INTERNET_NAME--<uuid5>"
    }
  ],
  "edges": [
    {"from": "<scan_instance>", "to": "<bucket_instance>", "relation": "contains"},
    {"from": "<bucket_instance>", "to": "<descriptor_instance>", "relation": "had"},
    {"from": "<bucket_instance>", "to": "<dns_instance>", "relation": "had"}
  ]
}
```

## Validation gate

Promote to graph only after:

1. Scope is authorized and recorded.
2. Secret / token / console URL values are redacted in all exported artifacts.
3. Permission-denied empties are classified as blockers, not clean misses, when relevant.
4. Offensive modules (`get-console`, `apim-cross-tenant` non-passive modes) are excluded or heavily redacted unless the scenario explicitly examines those shapes.
5. IP literals go through `classify_ip` — never hardcode ambiguous `IP_ADDRESS`.
