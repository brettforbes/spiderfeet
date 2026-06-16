## Problem statement

Stage 4 Tests need three subscription groups: (1) no subscription/API key, (2) free subscription (API key required, no cost), (3) paid subscription (API key costs money). Current plan metadata conflates tiers and mis-detects keys (e.g. `api_hostname` treated as API key).

## Desired outcome

- Every OSINT service in `osint_services.json` exposes `subscription_tier`: `none` | `free_auth` | `paid_auth`.
- `/tests/plan` and `/tests/modules` return tier + `requires_api_key` + `has_api_key` (from runtime config only — secret opts like `api_key`, `token`, not `api_hostname`).
- Paid vs free distinction uses existing `access_tier` + `data_source.model` where available; document uncertainty when ambiguous.

## Epic

Parent: #66 [Epic] Stage 4c — Route test execution platform

## Spec binding

- SPEC-002: **R2-04-06** (SPEC_GAP — promote before implementation)
- Related: R2-04-03 module catalog

## Acceptance criteria

- [ ] Tier enum documented in API schemas and catalog
- [ ] `requires_api_key` true only when module has secret opt or auth tier; **never** inferred from `api_*` hostname opts
- [ ] `/tests/plan` items include `subscription_tier`, `requires_api_key`, `has_api_key`, `skip_reason`
- [ ] Unit tests cover `sfp_threatjammer` (hostname only → no key) and `sfp_emailrep` (key required)

## Verification

- `poetry run pytest .tests/api/test_tests.py -q`
- Manual: `/tests/plan` counts match tier expectations for sample modules

## Non-goals

- UI for editing keys (see Subscriptions API issue)
- Charging/billing integration
