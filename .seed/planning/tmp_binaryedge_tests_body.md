**Parent epic:** #710  
**Blocks:** #474  
**Depends on:** module + subscriptions issues

## Problem statement

#474 `[Module test] sfp_binaryedge: BinaryEdge` cannot progress while upstream is dead and `service_state: error` hides the module from Tests UI.

## Scope

- Add/update `module_test_seeds.json` entries per validated Coalition routes
- Run route tests for each supported consumed×produced pair
- Update `test/integration/modules/test_sfp_binaryedge.py`
- Mark upstream-blocked routes in seed registry where Coalition has no equivalent
- Promote `service_state` from `error` → `in-test` when first route passes
- Close or complete #474 with evidence

## Acceptance criteria

- [ ] Module visible on Tests tab after state promotion
- [ ] Each supported route has seed + at least one `hit` or documented `clean_miss`
- [ ] Unsupported legacy routes recorded with `upstream_blocked` / notes
- [ ] Verification logged on #474

## Spec binding

- SPEC-002: R2-04-03

## Verification

- `pytest` map/tests modules + API route test runs per stage4 corpus doc
