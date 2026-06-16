---
name: Titus
description: Use when requests mention Titus, secret scanner workflows, credential leak triage, or repository secret detection at scale. Runs scan-to-triage workflows and converts validated findings into nugget nodes/edges arrays.
---

# Titus - Secret Scanning Workflows

## Purpose

Use this skill when an agent needs high-throughput secret scanning and triage across code artifacts with Titus.

## Step-by-Step Instructions

1. Confirm authorization and handling requirements.
2. Validate tooling with `titus --help`.
3. Define scope (repo, directories, changed files).
4. Run baseline scan and capture output.
5. Triage by detector class and confidence.
6. Validate context and remove false positives.
7. Export structured findings where available.
8. Convert validated results to nugget `nodes` and `edges`.
9. Document remediation and run post-fix verification scan.

## If/Then Decision Rules

| If | Then |
|----|------|
| Repository is very large | Use phased scans on critical directories first |
| Results contain many duplicates | De-duplicate by finding fingerprint |
| Findings look fixture/test related | Mark as synthetic until validated |
| Pipeline integration is needed | Normalize into stable parser schema first |

## Guardrails & Pitfalls

- Do not publish raw secrets in logs, PRs, or tickets.
- Do not equate match volume with impact.
- Keep engagement outputs separated.
- Re-scan after remediation to confirm closure.

## Strategies and Tactics

1. Baseline pass then focused pass.
2. Prioritize cloud keys/tokens/private keys.
3. Correlate findings with likely service impact.
4. Track deltas across recurring scans.

## References directory for details on source material and usage indexed through `SKILLS.md`

See `references/SKILLS.md`.
