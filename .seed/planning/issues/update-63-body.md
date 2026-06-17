## Problem statement

Original Stage 4b CSV work assumed valid target strings equal "realistic" data. Batch testing proved most seeds produce **no module output**.

## Desired outcome (revised)

Author `test_nugget_data.csv` with **AU, UK, US** rows per `(module_id, consumed_nugget_id)` where values are tuned until `POST /scan_ui` returns `produced.length > 0` (or row marked `negative-fixture` with justification).

## Epic

Parent: #61

## Spec binding

- SPEC-002: **R2-04-02**, **R2-04-07**

## Acceptance criteria (revised)

- [ ] CSV includes `module_id`, `consumed_nugget_id`, `region`, `input_value`
- [ ] Each row validated against live module run (document date/key used)
- [ ] No row ships with only generic `sbs.com.au` unless module proven to produce from it
- [ ] Paired with SF-04B-06 validation harness

## Verification

- Validation report attached to issue on completion
- Sample: ≥10 modules × 3 regions with `validated_produces=true`

## Supersedes

Previous one-liner acceptance ("Realistic values; AU, UK, US rows per consumed nugget") — **realistic = produces scan results**.
