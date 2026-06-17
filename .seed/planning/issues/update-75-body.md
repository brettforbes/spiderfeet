## Problem statement

Sign-off must account for subscription tiers: modules untested because keys not configured vs genuinely failing.

## Desired outcome (extends original)

Route coverage audit report includes:

- Count by `subscription_tier` (none / free_auth / paid_auth)
- Runnable vs hidden (no key) vs failed strict test
- List modules with validated seeds vs pending corpus (#660)

## Epic

Parent program Stage 4 exit

## Spec binding

- SPEC-002: R2-04-03, R2-04-06, R2-04-07

## Acceptance criteria (revised)

- [ ] Report distinguishes "blocked: no API key" from "failed: no output"
- [ ] Operator review checklist updated for Subscriptions page
- [ ] Every planned route exercised **or** documented exception with tier reason

## Dependencies

- #657, #658, #660, widget #50
