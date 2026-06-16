# Trajan Tactics and Workflows

## Recommended workflow

1. **Single repo baseline**
   - Validate credentials, permissions, and parser output.
2. **High-risk repo sweep**
   - Prioritize deploy pipelines, release workflows, infra repos.
3. **Org-wide expansion**
   - Scan at larger scope with bounded concurrency and timeout.
4. **Chain analysis**
   - Correlate findings that combine untrusted input, secret access, and deploy rights.
5. **Remediation loop**
   - Re-scan changed workflows and compare against prior findings.

## Tactics

- Prefer path-scoped local scans when API access is unavailable.
- Use API-mode scans for complete org inventory and metadata enrichment.
- Prioritize high/critical findings with concrete exploit path evidence.
- Store both raw output and normalized records for auditability.

## Practical triage order

1. token/secret leakage
2. unsafe workflow trigger contexts
3. unpinned actions/dependencies
4. privilege boundary bypasses
5. policy and hardening gaps
