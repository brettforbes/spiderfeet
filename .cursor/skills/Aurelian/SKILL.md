---
name: Aurelian
description: Run multi-cloud reconnaissance with Aurelian across AWS, Azure, and GCP. Trigger for cloud secret hunting, public resource exposure checks, IAM privilege path analysis, subdomain takeover checks, or OPSEC-aware cloud identity recon.
---

# Aurelian - Multi-Cloud Recon Framework

## Purpose

Use this skill when you need unified cloud security reconnaissance across AWS, Azure, and GCP, then convert findings into SpiderFeet-style nugget node/edge graphs.

## Step-by-Step Instructions

1. Confirm authorization and cloud scope (accounts/subscriptions/projects).
2. Start with identity and baseline visibility:
   - `aurelian aws recon whoami`
   - platform-specific listing modules as needed.
3. Run discovery modules by objective:
   - `find-secrets`
   - `public-resources`
   - `subdomain-takeover`
   - `graph` (AWS IAM path analysis)
4. Capture outputs in JSON-compatible form when available.
5. Normalize results by cloud, resource, issue type, severity/confidence.
6. Convert to SpiderFeet-style nuggets:
   - `nodes`: cloud account/project, resource, exposure type, secret indicator, IAM path.
   - `edges`: account owns resource, resource has risk, role/action enables path.
7. Re-run focused modules to validate high-risk findings before escalation.

## If/Then Decision Rules

- If objective is credential exposure, then start with `find-secrets`.
- If objective is internet exposure, then run `public-resources` first.
- If AWS privilege movement is in scope, then run `graph` and/or `analyze-iam-permissions`.
- If stealth requirement is high, then use `whoami` early for OPSEC-safe identity checks.
- If cloud-specific permissions block module output, then record as coverage blocker rather than silent pass.
- If memory constraints exist, then use supported build/storage options noted in docs.

## Guardrails & Pitfalls

- Authorized testing only; cloud recon may touch sensitive metadata.
- Respect provider rate limits and avoid broad scans without explicit approval.
- Distinguish discovered potential exposure from confirmed exploitability.
- Keep account IDs, project IDs, and secret artifacts redacted in shared reports.
- Preserve module context (which module emitted which finding) for remediation traceability.

## Strategies and Tactics

- Sequence by risk:
  1) `whoami`
  2) `public-resources`
  3) `find-secrets`
  4) IAM graph/path analysis
  5) takeover checks
- Start per-account/project, then scale to organization-wide inventories.
- Use offline analysis modules for repeatable IAM permission investigations.

## References

See `references/SKILLS.md` for options, parsing schema, nugget mapping, workflows, and sources.

## Examples

```bash
# AWS identity check (OPSEC-aware)
aurelian aws recon whoami

# AWS secrets and exposure recon
aurelian aws recon find-secrets
aurelian aws recon public-resources

# AWS IAM graph analysis
aurelian aws recon graph --neo4j-uri bolt://localhost:7687
aurelian aws analyze analyze-iam-permissions --gaad-file gaad.json

# Azure/GCP equivalents
aurelian azure recon find-secrets --subscription-id <id>
aurelian gcp recon public-resources --project-id <id>
```
