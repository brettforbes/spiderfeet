## Summary

- Closes none-tier seed research (epic #674): **79/87 smoke-validated** (14 positive, 65 negative), **8 upstream-blocked** with `service_state: error`
- Adds `module_execution` verdicts, `GET /scans/{id}/logs`, negative fixture semantics (R2-04-08)
- `scan_ui` resolves catalogue nugget types via `scan_targets.py` (`COMPANY_NAME`, `PHYSICAL_ADDRESS`, etc.)
- Tests and Subscriptions APIs exclude `service_state: error` modules; Maps unchanged (R2-04-09)
- Registry, probe scripts, agent docs (`stage4_seed_corpus_and_tests.md`), project rules `proj-04`

## Test plan

- [x] `poetry run pytest .tests/api .tests/map -m "not slow"` — 98 passed
- [ ] Smoke `POST /api/v1/scan_ui` negative fixture (`sfp_spamcop` / clean_miss)
- [ ] Confirm `/api/v1/tests/modules` omits `sfp_dnsdumpster`
- [ ] Run `sync_service_state.py --write --typedb` after merge if TypeDB needs refresh

## Spec

R2-04-07, R2-04-08, R2-04-09

## Related

- Widget PR: brettforbes/spiderfeet-widget (issue #55)
