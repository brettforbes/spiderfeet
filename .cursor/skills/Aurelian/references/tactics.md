# Aurelian Tactics and Workflows

## Recommended sequence (AWS)

1. **Identity** — `aws recon whoami` (OPSEC-aware ARN leak techniques).
2. **Inventory / exposure** — `list-all` (optional `--scan-type summary`) then `public-resources`.
3. **Secrets** — `find-secrets` (narrow `-r` / `-t` / `-a` when full-account cost is high).
4. **IAM** — `iam-quick-analyze` for fast paths; `recon graph` (+ optional Neo4j) for depth; offline `analyze analyze-iam-permissions` when GAAD exists.
5. **Takeover** — `subdomain-takeover`, then `cloudfront-s3-takeover` / `cdk-bucket-takeover` if CDN/CDK in scope.
6. **Org context** — `org-policies`, `resource-policies`, `account-auth-details` as inputs to offline analyze.

## Azure / GCP variants

- **Azure triage:** `list-all` → `public-resources` → `find-secrets` → `configuration-scan` → `subdomain-takeover`; add `conditional-access-policies` / `apim-audit` when identity or APIM is in ROE.
- **GCP triage:** scope with `-p` / `-o` / `--folder-id` → `public-resources` → `find-secrets` → `subdomain-takeover`.
- **Never** run `apim-cross-tenant` `authenticated` / `bypass` without explicit offensive authorization (default help mode: `passive`).

## Workflow variants

| Variant | Modules | When |
|---------|---------|------|
| Rapid triage | whoami + public-resources + find-secrets (one scope) | First day / single account |
| Thorough assessment | Full recon suite + IAM graph/analyze + takeovers | Full cloud engagement |
| Offline IAM lab | account-auth-details → analyze-iam-permissions (+ policy files) | Repeatable analysis without live APIs |
| Continuous monitoring | Scheduled scoped modules + differential file compare | Recurring authorized monitoring |

## Rich / sparse / error tactics

- **Rich output:** permissive lab accounts; widen regions/types; avoid over-filtering `-t`/`-a`.
- **Sparse / clean miss:** hardened org with tight IAM — still capture empty structured files + exit metadata.
- **Errors:** invalid profile, missing subscription, denied Graph/Cloud Control — keep stderr/stdout ERROR (distinct from Windows enrich path quirk).
- **Windows enrich/analysis ERROR:** present on this host for every command — filter out when classifying tool errors.

## Tactics

- Prioritize findings that combine **public exposure + secrets**.
- Collect GAAD/policies once; re-run analyze modules without re-enumerating.
- Use `--concurrency` carefully against rate limits (default often `5`).
- Validate takeover and public-access candidates before escalation.
- Keep provider + module tags on every finding for graph provenance.
