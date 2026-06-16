---
name: tldfinder
description: Enumerate private and uncommon top-level domains with tldfinder when prompts mention private TLD discovery, DNS namespace reconnaissance, split-horizon DNS, corp/internal naming leaks, or pivoting from seed domains/organizations into broader INTERNET_NAME expansion for SpiderFeet mapping.
---

# tldfinder - Private TLD Enumeration

## Purpose

Use this skill to discover and validate private or non-standard TLD namespaces with `tldfinder`, then convert findings into SpiderFeet domain graph nuggets.

## Step-by-Step Instructions

1. Confirm authorization and legal boundaries for DNS namespace reconnaissance.
2. Start with seed domains/organizations gathered from earlier recon phases.
3. Run a baseline tldfinder pass against seeds and capture structured output.
4. Separate likely public-root TLD results from private/internal suffix candidates.
5. Validate candidate private TLDs by checking repeated host evidence and resolver behavior.
6. Expand discovered TLDs into candidate hostnames/domains for follow-up DNS resolution.
7. Convert validated discoveries to SpiderFeet graph payload:
   - `nodes[]` for `INTERNET_NAME` and related namespace entities,
   - `edges[]` linking seed domains to discovered suffixes/hosts.
8. Feed new host candidates into `dnsx`, then chain to `httpx`/port tooling.
9. Re-run incrementally as new seeds arrive to enrich namespace coverage.

## If/Then Decision Rules

| If | Then |
|----|------|
| Candidates appear only once | Mark low confidence and defer heavy pivots |
| Candidate suffix appears across many assets | Promote to high-confidence private TLD finding |
| Resolver behavior differs by network vantage | Record split-horizon possibility and keep both views |
| Public PSL/root TLD collides with candidate | Treat as public namespace, not private TLD discovery |
| No useful output from initial seeds | Broaden seeds from certs, whois, and passive DNS sources |
| Many noisy malformed domains | Normalize/clean seed input before rerun |

## Guardrails & Pitfalls

- Do not assume every uncommon suffix is private; validate evidence density.
- Keep raw observations and confidence scores.
- Avoid leaking internal namespaces beyond authorized reporting scope.
- Handle IDN/punycode consistently when comparing suffixes.
- Distinguish parser errors from true "no findings" outcomes.

## Strategies and Tactics

- **Seed diversity strategy:** combine org, cert, and DNS-derived seeds.
- **Confidence layering:** score candidate TLDs by recurrence and validation signals.
- **Namespace pivoting:** move from suffix discovery to host expansion and active validation.
- **Differential vantage checks:** compare outputs across resolver/geographic contexts.
- **Incremental updates:** process only new seeds and merge with prior findings.

## References directory for details on source material and usage indexed through `SKILLS.md`

See `references/SKILLS.md` for CLI options, output schema/parsing, nugget mapping, tactics/workflows, and source links.
