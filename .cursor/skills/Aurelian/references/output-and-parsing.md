# Aurelian Output and Parsing

Aurelian modules emit resource and issue-centric findings that should be normalized by cloud context.

## Parsing priorities

1. Track provider context (`aws`, `azure`, `gcp`).
2. Keep account/subscription/project identifiers.
3. Preserve module name (`find-secrets`, `public-resources`, etc.).
4. Parse resource identifiers and finding metadata separately.
5. Keep optional validation evidence for secrets when present.

## Suggested normalized finding

```json
{
  "cloud": "aws",
  "scope_id": "123456789012",
  "module": "public-resources",
  "resource_type": "s3_bucket",
  "resource_id": "my-public-bucket",
  "finding_type": "public_access",
  "evidence": "bucket policy allows public read"
}
```

## Parser guardrails

- Expect module-specific schema variation.
- Do not merge findings across modules without preserving source module tags.
- Treat missing permissions as explicit blocked coverage, not clean results.
