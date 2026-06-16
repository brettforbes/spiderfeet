## Problem statement

`nuggets_consumed_list.json` must stay aligned with map catalog and module-validated seed work (#659).

## Desired outcome (extends original)

- Regenerate list from `osint_services.json` consumed nuggets union
- Cross-check against `test_nugget_data.csv` / module seed registry — every consumed type has at least one candidate seed path
- Feed TypeDB load (#64) only after #659 registry validated

## Epic

Parent: #61

## Spec binding

- SPEC-002: R2-04-02, R2-04-07

## Acceptance criteria (revised)

- [ ] File matches catalog consumed types (currently 44 entries)
- [ ] Diff report vs previous version in PR
- [ ] No orphan consumed types without seed plan in #659/#660

## Dependencies

- Coordinate with #659 before final load (#64)
