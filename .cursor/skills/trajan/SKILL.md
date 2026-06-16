---
name: trajan
description: Scan CI/CD pipelines for supply-chain risks with Trajan. Trigger when tasks mention GitHub Actions, GitLab CI, Azure DevOps, Jenkins, JFrog, workflow YAML analysis, pipeline misconfigurations, or CI token/secret abuse paths.
---

# Trajan - CI/CD Security Scanning

## Purpose

Use this skill when you need to assess CI/CD workflows for security weaknesses, map exploitable pipeline paths, and convert findings into SpiderFeet-style nugget `nodes` and `edges`.

## Step-by-Step Instructions

1. Confirm authorization and scope (org, repo, or local path).
2. Identify platform (`github`, `gitlab`, `ado`, `jenkins`, or `jfrog`) and required token.
3. Run a scoped baseline scan for one repository before org-wide scans.
4. Re-run with JSON output for machine parsing.
5. Normalize findings by severity, workflow file, detection type, and evidence.
6. Convert parsed output into SpiderFeet-style nugget arrays:
   - `nodes`: unique entities (repo, workflow, finding, secret exposure, token scope).
   - `edges`: relationships (`repo` -> `workflow`, `workflow` -> `finding`, `finding` -> `evidence`).
7. Escalate to broader scans only after validating parser assumptions on the baseline sample.

## If/Then Decision Rules

- If platform is unknown, then run `trajan list platforms` first and branch by supported adapter.
- If scanning private GitHub repos, then require PAT with `repo`; for public-only use `public_repo`.
- If API access is restricted, then use local/offline path mode (`--path`) and mark API-only detections as skipped.
- If output is intended for automation, then force JSON output and avoid table-only parsing.
- If org scan volume is high, then reduce concurrency and split repos into batches.
- If non-fatal errors occur, then keep partial findings but annotate confidence and coverage gaps.

## Guardrails & Pitfalls

- Authorized testing only; CI/CD scanning can expose sensitive build metadata.
- Do not assume local path mode equals API mode coverage; some detections are API-dependent.
- Avoid treating a single workflow misconfiguration as full repo compromise without chain context.
- Preserve workflow filename and step evidence text; it is needed for reproducible remediation.
- Keep tokens out logs and reports; redact before sharing.

## Strategies and Tactics

- Start narrow: repo scan -> validate parser -> expand to org.
- Use graph mindset: workflow/job/step dependencies reveal privilege escalation paths.
- Prioritize findings that combine credential exposure + untrusted input + deploy permissions.
- Run periodic differential scans to catch newly introduced pipeline risk.

## References

See `references/SKILLS.md` for CLI options, parsing schema, nugget mapping, tactics/workflows, and source links.

## Examples

```bash
# GitHub repo scan
trajan github scan --repo owner/repo -o json > trajan-results.json

# GitHub org scan with tuned concurrency
trajan github scan --org myorg --concurrency 20 -o json > trajan-org.json

# GitLab group scan
trajan gitlab scan --group mygroup -o json > trajan-gitlab.json

# Azure DevOps repo scan
trajan ado scan --org myorg --repo myproject/myrepo -o json > trajan-ado.json

# Offline scan from local workflow files
trajan github scan --path ./.github/workflows -o json > trajan-local.json
```
