## Problem
Operators tuning `module_test_seeds.json` need scan diagnostic logs; only CherryPy `/scanlog` existed.

## Outcome
- `GET /api/v1/scans/{scan_id}/logs` with `limit`, `from_row_id`, `reverse`

## Spec
R2-04-07

## Acceptance
- 404 when scan missing; API test coverage
