**Parent epic:** #710  
**Depends on:** spike issue (API mapping)

## Problem statement

`modules/sfp_binaryedge.py` uses dead `api.binaryedge.io` + `binaryedge_api_key`. Rewrite to Coalition Control REST API.

## Scope

- Replace `query()` transport: `POST /auth/login` → Bearer token; ASM calls under `/asm/entity/{entity_id}/…`
- Replace opts: drop `binaryedge_api_key`; add Coalition credentials / token / `entity_id` per spike
- Map Coalition JSON → existing SpiderFeet event types where semantics align
- Remove or guard routes with no Coalition equivalent
- Update module meta (`meta` dict): website, references, descriptions
- Unit tests in `test/unit/modules/test_sfp_binaryedge.py`

## Non-goals (unless spike expands scope)

- Widget changes (backend-only unless Subscriptions issue requires API schema changes)
- Paid Coalition subscription automation

## Acceptance criteria

- [ ] Module runs against live Coalition API with operator free account
- [ ] At least one validated consumption→production route per spike “supported” row
- [ ] Unsupported legacy routes documented and do not error-loop
- [ ] No secrets committed; opts documented in catalogue

## Spec binding

- SPEC-002: R2-04-03

## Verification

- Targeted unit tests + one API integration smoke via Tests tab after service_state returns to `in-test`
