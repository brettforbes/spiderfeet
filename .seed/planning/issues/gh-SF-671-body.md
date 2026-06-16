## Problem
Negative fixtures pass on `FINISHED` with no module output, but `scan_ui` only returns produced arrays — no explicit verdict.

## Outcome
Extend `POST /api/v1/scan_ui` with `module_execution` (`clean_miss`, `hit`, `error_failed`, `incomplete`, `absent_violation`).

## Spec
R2-04-08

## Acceptance
- Unit tests in `.tests/api/test_module_execution.py`
- Widget negative pass uses `verdict === 'clean_miss'`
