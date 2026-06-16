## Problem statement

Original scope: mark paid/API-key modules as untested. Stage 4 analysis requires explicit **three-tier subscription model** driving Tests and Subscriptions UI.

## Desired outcome (revised)

Document and encode in catalog:

| Tier | `subscription_tier` | Tests visibility |
|------|---------------------|------------------|
| No subscription | `none` | Always visible |
| Free subscription | `free_auth` | Visible when key configured |
| Paid subscription | `paid_auth` | Visible when key configured |

Include mapping rules from `access_tier`, `data_source.model`, `flags.apikey`, `module_opts`.

## Epic

Parent: #61

## Spec binding

- SPEC-002: **R2-04-06**

## Acceptance criteria (revised)

- [ ] `.docs/analysis/osint_services.json` includes `subscription_tier` on every service
- [ ] Ambiguous cases documented in `.docs/analysis/subscription_tiers.md`
- [ ] Map/TypeDB metadata can store `untested` + reason for paid without key

## Verification

- Tier counts reconcile with `/tests/plan` skip stats
- Cross-check 20 random modules against module source `meta` / `opts`

## Related

- SF-04C-10 implements API exposure
