## Problem statement

Module test API (#68) must align with strict pass semantics and subscription gates used by Tests tab.

## Desired outcome (extends original)

- `POST /scan_ui` remains canonical test execution path
- **Pass:** `status=FINISHED` AND `produced.length > 0`
- **Fail:** timeout, non-FINISHED status, or zero produced (with reason code)
- Reject run at API layer if module requires key and `has_api_key=false` (409/422)

## Epic

Parent: #66

## Spec binding

- SPEC-002: **R2-04-03**, **R2-04-08**

## Acceptance criteria (revised)

- [ ] Response documents failure reason (`missing-api-key`, `no-produced-objects`, `timeout`, etc.)
- [ ] Module opts injected from Subscriptions store before scan start
- [ ] Widget strict pass rule matches API contract

## Verification

- API tests for pass/fail cases
- `sfp_dnsresolve` + valid seed → pass; `sfp_duckduckgo` + bad seed → fail with reason

## Note

Partial implementation exists in widget; this issue tracks API contract completion.
