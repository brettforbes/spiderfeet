---
name: NTLMRecon
description: Use when requests mention NTLM challenge enumeration, SMB auth fingerprinting, or Windows domain reconnaissance. Runs probe-to-parse workflows and converts validated metadata into nugget nodes/edges arrays.
---

# NTLMRecon - NTLM Challenge Enumeration

## Purpose

Use this skill when an agent must collect NTLM challenge metadata to profile Windows hosts, domains, and auth posture.

## Step-by-Step Instructions

1. Confirm authorized scope and protocols.
2. Validate tooling with `ntlmrecon -h`.
3. Build target set (IP/FQDN).
4. Run baseline probes on priority hosts.
5. Parse domain, host, DNS, and signing/auth-related fields.
6. De-duplicate by host and challenge fingerprint.
7. Convert parsed output to nugget `nodes` and `edges`.
8. Report anomalies and hardening recommendations.

## If/Then Decision Rules

| If | Then |
|----|------|
| Endpoint is non-responsive | Retry with alternate in-scope path/port |
| Output is text only | Normalize with parser template |
| Metadata varies between retries | Mark unstable until corroborated |
| SMB signing appears weak | Escalate as high-priority hardening finding |

## Guardrails & Pitfalls

- No brute-force activity in this workflow.
- Stay inside authorization boundaries.
- Treat challenge metadata as inferential until corroborated.
- Do not overstate OS certainty from weak fingerprints.

## Strategies and Tactics

1. Probe domain controllers first.
2. Expand to high-value servers.
3. Compare metadata consistency across subnets.
4. Correlate output with DNS and inventory context.

## References directory for details on source material and usage indexed through `SKILLS.md`

See `references/SKILLS.md`.
