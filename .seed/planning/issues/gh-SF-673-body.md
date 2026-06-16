## Problem
Negative modules need clean inputs for `clean_miss` tests and dirty `positive_hit` inputs to confirm emit behavior.

## Outcome
- `expected_absent_types` on negative registry entries
- `positive_hit` sub-object for dirty tuning
- Scripts: `backfill_expected_absent_types.py`, `split_negative_positive_hit.py`

## Spec
R2-04-07, R2-04-08

## Acceptance
- Plan/detail APIs expose `expected_absent_types`
- spamhaus: clean `8.8.8.8` primary, Tor exit under `positive_hit`
