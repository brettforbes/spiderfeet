# Aurelian Output and Parsing

Prefer **file artifacts** written via global `-f/--output-file` (overrides `--output-dir`) or module `--output-dir` (default `aurelian-output`). Several modules state they emit **JSON by default** (e.g. AWS `recon graph`); always capture to a path for SpiderFeet.

## Streams vs files

| Stream / path | Role |
|---------------|------|
| stdout ERROR lines (`enrich\aws`, `analysis\aws`) | Host quirk on Windows captures — discard for findings |
| ANSI banner (`list-modules`) | Not structured evidence |
| `-f` / `--output-file` | Primary structured capture for examination |
| `--output-dir` / module output trees | Multi-file module dumps (GAAD, policies, Titus DB via `--db-path`) |
| Titus `--db-path` | SQLite datastore for secret scanning side-effects |

## Parsing priorities

1. Record **provider** (`aws` / `azure` / `gcp`) and **module** name.
2. Keep **scope identifiers** (AWS account/profile/region; Azure subscription id; GCP project/org/folder).
3. Parse **resource identifiers** (ARN, Azure resource id, GCP name) separately from finding text.
4. Classify finding family: secret, public exposure, IAM path, takeover, misconfig, inventory, identity.
5. Redact secret material before any shared artifact or nugget `nugget_data`.

## Suggested normalized finding

```json
{
  "cloud": "aws",
  "scope_id": "123456789012",
  "module": "public-resources",
  "resource_type": "AWS::S3::Bucket",
  "resource_id": "arn:aws:s3:::example-bucket",
  "finding_type": "public_access",
  "evidence": "bucket policy allows anonymous read",
  "artifact_path": "aws-public.json"
}
```

## Module-specific notes

- **`find-secrets`:** Titus-backed; may write `--db-path` SQLite; optional `--validate` makes outbound API calls.
- **`account-auth-details` / `org-policies` / `resource-policies` / `list-all`:** feed offline `analyze analyze-iam-permissions` via `--gaad-file`, `--org-policies-file`, `--resource-policies-file`, `--resources-file`.
- **`recon graph`:** JSON by default; `--neo4j-uri` also populates Neo4j for later `analyze graph`.
- **`cost-summary`:** help describes markdown table display — still use `-f` if the run writes a file; otherwise retain full stdout as text-only exception for that module shape.
- **`get-console`:** console URL is credential-equivalent — store encrypted / redacted.

## Parser guardrails

- Expect **module-specific schema variation**; never merge findings without source module tags.
- Treat missing permissions / empty inventory as **blocked or sparse**, not automatic clean miss.
- Do not invent fields absent from the artifact; map only observed keys.
- For corpus harvest: structured file → derive Text pane; graph from structured only.
