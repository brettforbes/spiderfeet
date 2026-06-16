**Parent epic:** #716  
**Blocks:** #470

## Problem statement

Stage 4 module testing for `sfp_archiveorg` has no seeds and 81 route candidates untested.

## Scope

- Add `module_test_seeds.json` for `INTERESTING_FILE` route (minimum) and other enabled opt routes
- Negative seeds where Wayback returns empty snapshots
- Run API route tests; record scan-records
- Complete acceptance criteria on #470

## Acceptance criteria

- [ ] At least `INTERESTING_FILE → INTERESTING_FILE_HISTORIC` validated with realistic URL
- [ ] Disabled opt routes (form/flash/js pages default off) documented as N/A or enabled for test pass
- [ ] Evidence posted on #470

## Spec binding

- SPEC-002: R2-04-03

## Verification

- `pytest` + Tests tab smoke per stage4 corpus doc
