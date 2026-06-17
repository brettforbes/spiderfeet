## Promotion: develop → master

Stage 4 infrastructure and subscription fixes since last promotion (#708).

### Included

- PR #709 — Subscriptions signup metadata + free_auth guide export
- PR #720 — BinaryEdge `service_state: error`, Archive.org `requires_api_key` fix, AbstractAPI email reputation

### Verification

- `pytest .tests/map/test_subscription_tiers.py .tests/map/test_routes_catalog.py .tests/api/test_tests.py` — passed before merge
- Post-deploy: `python .seed/scripts/sync_service_state.py --write --typedb`

### Spec

R2-04-03, R2-04-06, R2-04-09 (SPEC-002)
