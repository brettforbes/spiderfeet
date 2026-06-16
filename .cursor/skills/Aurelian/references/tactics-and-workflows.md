# Aurelian Tactics and Workflows

## Recommended sequence

1. **Identity and context**
   - Run `whoami` or equivalent identity checks.
2. **Exposure discovery**
   - `public-resources` to surface externally reachable assets.
3. **Secrets discovery**
   - `find-secrets` for credential/token leakage.
4. **Privilege path analysis**
   - `graph` and IAM analysis modules.
5. **Takeover and DNS checks**
   - `subdomain-takeover`.

## Workflow variants

- **Rapid triage**: one account/project, exposure + secrets only.
- **Thorough assessment**: full module suite plus IAM path analysis.
- **Continuous monitoring**: scheduled module runs with differential reporting.

## Tactics

- Prioritize findings that combine exposure + credential leakage.
- Validate high-impact findings manually before escalation.
- Keep provider-specific constraints documented per finding.
