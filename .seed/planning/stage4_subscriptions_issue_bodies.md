# Stage 4 — Subscriptions & test-data rework (issue bodies)

Reference analysis: Tests tab batch run 515 fail / 11 pass — missing API keys, generic seeds, strict produced-object pass rule, api_hostname key-detection bug.

## New requirement IDs (SPEC_GAP → promote to SPEC-002 before implementation)

| ID | Summary |
|----|---------|
| R2-04-05 | Subscriptions page: store/edit per-module API keys; masked display |
| R2-04-06 | Subscription tier model: none / free-auth / paid-auth; gate Tests visibility & Run All |
| R2-04-07 | Module-validated test corpus: seeds tuned until scan_ui returns produced objects |
| R2-04-08 | Tests pass/fail: FINISHED + produced.length > 0; session summary counts |

---

Issue bodies below are used for `gh issue create` / `gh issue edit`.
