## Problem statement

Tests cannot run for ~523/527 modules because API keys are not configured. Keys must be editable without touching SpiderFeet CLI config files directly, and must flow into runtime module opts so `scan_ui` and Tests tab can execute services.

## Desired outcome

- REST API for **Subscriptions** (per OSINT module):
  - `GET /subscriptions/modules` — list services requiring keys + current key status (masked)
  - `GET /subscriptions/modules/{module_id}` — detail (description, URL, consumed/produced nuggets, tier)
  - `PUT /subscriptions/modules/{module_id}` — set/update secret opts (e.g. `api_key`); persist to SpiderFeet DB config (`configGet`/`configSet` path used by API bootstrap)
- After key save, `/tests/plan` reports `has_api_key=true` for that module immediately.

## Epic

Parent: #66 [Epic] Stage 4c — Route test execution platform

## Spec binding

- SPEC-002: **R2-04-05** (SPEC_GAP — promote before implementation)
- Related: R2-04-06 tier gating

## Acceptance criteria

- [ ] Keys persisted in same store as SpiderFeet module opts (survive API restart)
- [ ] Responses never return full secret in GET (masked, e.g. `••••••last4`)
- [ ] Only secret opt names (`api_key`, `token`, etc.) writable via this API
- [ ] Setting key on `sfp_emailrep` allows module test to run without "did not set an API key" log error
- [ ] OpenAPI docs for all three endpoints

## Verification

- API integration test: set key → `/tests/plan` shows runnable → `POST /scan_ui` produces events (or documented external failure)
- Security: unauthenticated local dev only (stage 4); document stage-5 auth gap

## Non-goals

- Key rotation, encryption at rest beyond existing SpiderFeet config
- Paid subscription billing
