# Titus Nugget Mapping

Map **validated, redacted** findings to SpiderFeet ontology nodes. Never use raw secret values as `nugget_data`.

## Suggested nugget types

| Source field | Nugget ID | Notes |
|--------------|-----------|-------|
| Rule name / finding label (redacted) | `RAW_RIR_DATA` | Or promote a tool-specific type in `nuggets_extension.json` when approved |
| Validated compromised password | `PASSWORD_COMPROMISED` | Only after confirmation — never store the password string |
| Public leak surface URL | `LEAKSITE_URL` | When provenance is a paste/leak site |
| Leak body excerpt (redacted) | `LEAKSITE_CONTENT` | Descriptor only; no secret bytes |
| Git / SaaS hostname | `INTERNET_NAME` | From provenance URL host (`github.com`, etc.) |
| File path / commit / image ref | `RAW_RIR_DATA` | Path, commit, or image tag as descriptor on finding |
| Email in non-secret context | `EMAILADDR` | Skip if part of secret material |
| Username patterns | `USERNAME` | Validate not fixture |

Reuse catalogue entries from `.docs/analysis/nuggets.json` before inventing types. Add tool-specific types only to `nuggets_extension.json` when the operator approves.

## Graph pattern

```
SCAN (scan head)
  └─contains─> FINDING (one per validated finding, redacted label)
        └─had─> RULE_DESCRIPTOR (rule name / id — RAW_RIR_DATA)
        └─had─> PROVENANCE (repo/path/commit/image — RAW_RIR_DATA or INTERNET_NAME)
```

## Example payload (illustrative)

```json
{
  "nodes": [
    {
      "nugget_id": "RAW_RIR_DATA",
      "nugget_data": "rule:AWS Access Key ID | severity:high | validation:unknown",
      "nugget_instance_id": "RAW_RIR_DATA--<uuid5>"
    },
    {
      "nugget_id": "INTERNET_NAME",
      "nugget_data": "github.com",
      "nugget_instance_id": "INTERNET_NAME--<uuid5>"
    }
  ],
  "edges": [
    {"from": "<scan_instance>", "to": "<finding_instance>", "relation": "contains"},
    {"from": "<finding_instance>", "to": "<provenance_instance>", "relation": "had"}
  ]
}
```

Use shared `graph_builder.nugget_instance_id` only — no alternate UUID schemes. Allowed relations: `contains`, `had`, `listens-to` per project ontology rules.

## Validation gate

Promote to graph only after:

1. Finding is not marked rejected in `explore` without override rationale.
2. Secret value is redacted in all exported artifacts.
3. Provenance links to authorized scope.
4. Fixture/test strings are classified as `clean_miss` or negative scenario, not live credentials.
5. Optional: `--validate` confirmed/denied status recorded as descriptor text (not secret material).
