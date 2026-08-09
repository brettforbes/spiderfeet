# Trajan Nugget Mapping

Map **redacted** Trajan findings to SpiderFeet ontology nodes. Never use raw secret values, tokens, or retrieve/attack loot as `nugget_data`.

## Suggested nugget types

Reuse catalogue entries from `.docs/analysis/nuggets.json` (and extensions) before inventing types.

| Source | Nugget ID | Notes |
|--------|-----------|-------|
| Finding label + severity + detection (redacted) | `VULNERABILITY_GENERAL` | Pipeline misconfig / abuse path — not CVE unless CVE id present |
| Detection / capability name | `RAW_RIR_DATA` | Descriptor on the finding (e.g. `pwn-request`) |
| Workflow / pipeline file path | `RAW_FILE_META_DATA` | Path relative to repo |
| Repository / project slug | `RAW_RIR_DATA` or `INTERNET_NAME` | Prefer host + path split when URL-shaped |
| Platform hostname | `INTERNET_NAME` | `github.com`, GHES host, GitLab host, Jenkins URL host |
| Software / action pin evidence | `SOFTWARE_USED` | When finding cites action/tool identity |
| Confirmed compromised credential (rare) | `PASSWORD_COMPROMISED` / account types | Only after confirmation — never store the secret string |

Add tool-specific types only to `nuggets_extension.json` when the operator approves.

## Graph pattern

```
SCAN (scan head)
  └─contains─> FINDING (VULNERABILITY_GENERAL — redacted summary)
        └─had─> DETECTION (RAW_RIR_DATA — capability id)
        └─had─> WORKFLOW_PATH (RAW_FILE_META_DATA)
        └─had─> REPO_OR_HOST (RAW_RIR_DATA / INTERNET_NAME)
```

Allowed relations: `contains`, `had`, `listens-to` per project ontology rules. Use shared `graph_builder.nugget_instance_id` only.

## Example payload (illustrative)

```json
{
  "nodes": [
    {
      "nugget_id": "VULNERABILITY_GENERAL",
      "nugget_data": "severity:high | detection:artifact-poisoning | workflow:.github/workflows/release.yml",
      "nugget_instance_id": "VULNERABILITY_GENERAL--<uuid5>"
    },
    {
      "nugget_id": "INTERNET_NAME",
      "nugget_data": "github.com",
      "nugget_instance_id": "INTERNET_NAME--<uuid5>"
    },
    {
      "nugget_id": "RAW_FILE_META_DATA",
      "nugget_data": ".github/workflows/release.yml",
      "nugget_instance_id": "RAW_FILE_META_DATA--<uuid5>"
    }
  ],
  "edges": [
    {"from": "<scan_instance>", "to": "<finding_instance>", "relation": "contains"},
    {"from": "<finding_instance>", "to": "<workflow_instance>", "relation": "had"},
    {"from": "<finding_instance>", "to": "<host_instance>", "relation": "had"}
  ]
}
```

## Validation gate

Promote to graph only after:

1. Scope is authorized and recorded.
2. Secret / token values are redacted in all exported artifacts.
3. Offline (`--path`) vs API mode coverage is annotated when relevant.
4. Attack/retrieve outputs are excluded or heavily redacted unless the scenario explicitly examines offensive evidence shapes.
5. Fixture repos are classified honestly (positive finding vs clean miss).
