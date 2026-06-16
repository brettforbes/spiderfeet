---
name: uncover
description: Query provider search APIs with uncover to discover exposed internet assets, then convert normalized findings into SpiderFeet nuggets and graph edges. Trigger on uncover, shodan/censys/fofa/netlas queries, dorks, external attack-surface expansion, or provider-backed recon workflows.
---

# uncover

## Purpose

Use uncover for provider-backed discovery of internet-facing hosts/services and map results into SpiderFeet node/edge data.

## Step-by-Step Instructions

1. Confirm legal scope and API credential readiness.
2. Select provider(s) and draft focused query.
3. Run uncover with provider engine options.
4. Parse output and normalize host/port/protocol.
5. Merge duplicates across providers.
6. Convert into nuggets and nodes/edges arrays.
7. Queue validated high-value results for deeper scans.

### Examples

```bash
uncover -q 'ssl:"example.org"' -e shodan
uncover -q 'title:"login" port:443' -e shodan,censys -silent
uncover -q 'domain:"example.org"' -e netlas -silent
```

## If/Then Decision Rules

- If API key is missing, then fail fast with provider setup guidance.
- If query returns too much noise, then add org/domain/port constraints.
- If provider rate-limits, then backoff or pivot to alternate engine.
- If duplicate host:port appears, then merge evidence metadata.
- If finding is critical-looking, then validate live before severity claim.

## Guardrails & Pitfalls

- Authorized reconnaissance only.
- Respect provider terms and limits.
- Keep credentials out of repo and logs.
- Treat provider data as leads, not final truth.
- Always validate exposures with direct checks.

## references

- `references/SKILLS.md`
- `references/cli-options.md`
- `references/output-and-parsing.md`
- `references/nugget-mapping.md`
- `references/tactics.md`
- `references/sources.md`
