## Summary

- Mark `sfp_binaryedge` as upstream `error` (BinaryEdge shut down; Coalition Control migration tracked in #710).
- Fix `requires_api_key` false positive for `sfp_archiveorg` (`passwordpages` opt no longer treated as credential).
- Add AbstractAPI Email Reputation API key + `EMAILADDR` route in `sfp_abstractapi`.
- Transition/analysis docs and dynamic operator-module count in tests.

## Test plan

- [x] `pytest .tests/map/test_subscription_tiers.py .tests/map/test_service_states.py .tests/map/test_routes_catalog.py`
- [x] `pytest .tests/api/test_tests.py .tests/api/test_subscriptions.py`
- [ ] Restart API; confirm Map shows Archive.org in open bucket and BinaryEdge in error filter
- [ ] Run `sync_service_state.py --write --typedb` on operator machine if TypeDB drift

## Issues

- Closes #718
- Relates #710, #716, AbstractAPI subscriptions

## Spec

- R2-04-03, R2-04-06, R2-04-09
