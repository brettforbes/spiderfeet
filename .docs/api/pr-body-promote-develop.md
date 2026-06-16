## Promotion: develop → master

Release integration for Stage 4 seed corpus and Tests semantics work.

### Included since last master promotion

- PR #707 — None-tier seed research closed (79 smoke + 8 `service_state: error`), `module_execution` verdicts, `scan_targets`, probe scripts
- PRs #661–#669 — Subscriptions/tests plan, module seeds, validation batches, negative fixtures

### Verification

- `poetry run pytest .tests/api .tests/map -m "not slow"` — 98 passed on feature branch before merge
- Post-deploy: run `sync_service_state.py --write --typedb` if map DB predates `service_state` sync

### Spec

R2-04-07, R2-04-08, R2-04-09 (SPEC-002)
