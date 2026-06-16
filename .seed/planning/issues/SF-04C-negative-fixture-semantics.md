# Stage 4c — Negative fixture semantics (issue pack)

**Spec:** R2-04-08 (extend), R2-03-01 (TypeDB attribute), R2-04-07 (seed registry)  
**Epic:** Stage 4 Tests tab — meaningful pass/fail for blocklists and breach checks  
**Repos:** `spiderfeet` (#670–#673), `spiderfeet-widget` (#55)

---

## Problem

Blocklist, DNS-filter, and breach modules are **negative fixtures**: a clean target should produce **no module output**. Current tests treat `FINISHED + zero produced` as failure for positive fixtures only; negative modules were partially addressed but:

1. Category is not persisted on the TypeDB `osint-service` relation.
2. Tests/Subscriptions UI does not show positive vs negative at module level.
3. Seed registry uses **clean** inputs for negative smoke tests, but tuning needs **dirty** inputs that actually hit the list.
4. `scan_ui` lacks an explicit `module_execution.verdict` (`clean_miss` vs `hit`).
5. Operators cannot fetch scan logs via FastAPI when tuning seeds.

---

## Issue SF-670 — TypeDB `fixture_category` on `osint-service`

**Requirement:** R2-03-01, R2-04-08

### Outcome

- Add `fixture_category` attribute (`positive` | `negative`) to `osint-service` in `.seed/spiderfeet_map.tql`.
- Populate from `osint_services.json` during map bootstrap (`_service_attr_lines`).
- Expose on map read / force-graph nodes when present.
- Sync script: `.seed/scripts/sync_fixture_category.py` derives category from registry + reputation/breach categories.

### Acceptance

- Bootstrap inserts `fixture_category` for new services.
- `GET /api/v1/map/...` nodes include category when seeded.
- Unit test: bootstrap query contains `fixture_category`.

---

## Issue SF-671 — `scan_ui` `module_execution` verdict

**Requirement:** R2-04-08

### Outcome

Extend `POST /api/v1/scan_ui` response:

```json
"module_execution": {
  "module_id": "sfp_spamcop",
  "status": "FINISHED",
  "events_emitted": 0,
  "verdict": "clean_miss"
}
```

**Verdicts (backend only, no module code changes):**

| Verdict | Meaning |
|---------|---------|
| `clean_miss` | `FINISHED`, module emitted 0 produced types, no module ERROR logs |
| `hit` | Module emitted ≥1 produced type |
| `error_failed` | Scan `ERROR-FAILED` or module ERROR/CRITICAL log lines |
| `incomplete` | Non-terminal scan status |
| `absent_violation` | `expected_absent_types` from registry present in `scan_results_by_type` |

### Acceptance

- Unit tests for verdict inference (mock events/logs).
- Widget negative pass uses `verdict === 'clean_miss'` when present.

---

## Issue SF-672 — `GET /api/v1/scans/{scan_id}/logs`

**Requirement:** R2-04-07 (seed tuning diagnostics)

### Outcome

- CherryPy `/scanlog` parity via FastAPI.
- Query params: `limit`, `from_row_id`, `reverse`.
- JSON objects: `generated_ms`, `component`, `type`, `message`, `row_id`.

### Acceptance

- 404 when scan missing; 200 with log array when present.
- API test with mocked `SpiderFeetDb.scanLogs`.

---

## Issue SF-673 — Dual negative seeds + `expected_absent_types`

**Requirement:** R2-04-07, R2-04-08

### Outcome

Extend `module_test_seeds.json` per consumed nugget:

```json
{
  "input_value": "8.8.8.8",
  "fixture_kind": "negative",
  "validated_negative": true,
  "expected_absent_types": ["BLACKLISTED_IPADDR", "MALICIOUS_IPADDR"],
  "positive_hit": {
    "input_value": "185.220.101.1",
    "validated_produces": true,
    "notes": "Tor exit — confirms module can emit on dirty input"
  }
}
```

- Primary `input_value` = **clean** input for automated negative tests.
- `positive_hit` = dirty input for tuning / exploratory runs.
- `mark_negative_fixtures.py` sets `expected_absent_types` from `produced_nuggets`.
- `tune_test_seeds.py` may target `positive_hit` sub-object.

### Acceptance

- Registry loader returns `expected_absent_types` on plan/detail APIs.
- Validation script asserts absent types on clean negative smoke runs.

---

## Issue SFW-55 — Widget fixture icons + verdict pass (widget)

**Requirement:** R2-04-04, R2-04-08

### Outcome

- Accordion headers on **Tests** and **Subscriptions** show fixture icon (`positive` / `negative`).
- Pass rule: negative fixture succeeds on `FINISHED` + `module_execution.verdict === 'clean_miss'`.
- Result panel shows verdict badge and absent-type violations.

### Acceptance

- Manual: spamcop + 8.8.8.8 shows green `clean_miss`; spamhaus dirty hit shows `hit`.

---

## Traceability update

Amend SPEC-002 **R2-04-08**:

> Strict test pass: **positive** — `FINISHED` + produced objects; **negative** — `FINISHED` + `module_execution.verdict = clean_miss` (and `expected_absent_types` not present). Module-level `fixture_category` stored on TypeDB `osint-service` and shown in Tests/Subscriptions UI.
