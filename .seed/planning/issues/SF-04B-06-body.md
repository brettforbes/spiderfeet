## Problem statement

`test_nugget_data.csv` and related Stage 4b corpus work must prove **realistic, result-producing** inputs — not placeholder strings. Current AU/UK/US rows fail to produce module output at scale (515/526 batch failures when keys present).

## Desired outcome

- Rework corpus generation pipeline (issues #62, #63, #64 scope):
  1. For each OSINT module (or consumption group batch), run `scan_ui` with candidate seeds
  2. **Keep tuning** seed values until `produced.length > 0` OR module documented as `negative-fixture` (expects empty by design)
  3. Store region tags (AU, UK, US) per row
  4. Reject/fail CI check for seeds that never produce output across retry set

## Epic

Parent: #61 [Epic] Stage 4b — Test nugget corpus

## Spec binding

- SPEC-002: **R2-04-02**, **R2-04-07** (SPEC_GAP promotion required)

## Acceptance criteria

- [ ] Updated `test_nugget_data.csv` schema includes `module_id`, `consumed_nugget_id`, `region`, `input_value`, `validated_produces` (bool), `notes`
- [ ] Validation script/report: pass rate per tier (`none` / `free_auth` / `paid_auth`)
- [ ] #63 acceptance criteria revised: "realistic" means **produces scan_ui objects**, not merely valid target syntax
- [ ] Paid/keyed modules: validated only when key configured in Subscriptions API

## Verification

- Run validation script on `none`-tier sample (target ≥60% produce objects)
- Document exceptions in map metadata (`untested`, reason)

## Dependencies

- #SF-04C-10 tier classification
- #SF-04C-11 Subscriptions API (for keyed module validation)
