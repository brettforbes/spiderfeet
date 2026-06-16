---
name: nosey_parker
description: Use when requests mention noseyparker, secret scanning, leaked credentials, or git history secret triage. Runs scan-to-report workflows and converts validated findings into nugget nodes/edges arrays.
---

# nosey_parker - Secret Discovery and Triage

## Purpose

Use this skill when an agent needs to discover and triage possible secrets from repositories or file paths with `noseyparker`.

## Step-by-Step Instructions

1. Confirm authorization and scan boundaries.
2. Verify tooling with `noseyparker --help`.
3. Choose scope (repo/path/history) and set a dedicated datastore.
4. Run baseline scan, then report findings.
5. Triage high-confidence findings first.
6. Validate context and remove false positives.
7. Export structured output where available.
8. Convert validated findings to nugget `nodes` and `edges` arrays.
9. Document remediation actions (rotate/revoke/remove).

## If/Then Decision Rules

| If | Then |
|----|------|
| Scope is very large | Scan high-risk directories first |
| Results are noisy | Filter by high-confidence rule classes |
| Same secret repeats | De-duplicate by fingerprint |
| Findings look synthetic | Mark as fixture until validated |
| Pipeline ingest is required | Normalize output before nugget conversion |

## Guardrails & Pitfalls

- Authorized targets only.
- Never publish raw secret values in tickets/chats.
- Do not treat every pattern match as confirmed compromise.
- Keep datastores separate per engagement.

## Strategies and Tactics

1. Broad discovery pass, then focused high-risk pass.
2. Prioritize cloud keys, tokens, and private keys.
3. Correlate findings with recency and likely blast radius.
4. Re-scan after remediation to confirm closure.

## References directory for details on source material and usage indexed through `SKILLS.md`

See `references/SKILLS.md`.
