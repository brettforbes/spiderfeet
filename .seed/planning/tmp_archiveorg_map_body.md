**Parent epic:** #716

## Problem statement

Archive.org appeared under Map “needs subscription” due to `passwordpages` opt false positive in `is_secret_module_opt()`.

## Scope

- Verify fix in `spiderfeet/map/subscriptions.py` (`password` credential heuristic)
- Regression test: `sfp_archiveorg` → `requires_api_key: false`, tier `none`
- Update `osint_services.json` references to Wayback API + search API distinction
- Confirm map graph node flags after API restart

## Acceptance criteria

- [ ] Map filter “passes-tests / open” includes Archive.org
- [ ] `GET /api/v1/map/graph` shows `requires_api_key: false` for `sfp_archiveorg`
- [ ] Tests tab plan does not skip Archive.org for `missing-api-key`

## Spec binding

- SPEC-002: R2-03-02, R2-04-06
