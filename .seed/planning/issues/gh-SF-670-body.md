## Problem
Positive vs negative fixture semantics are not persisted on the TypeDB `osint-service` relation.

## Outcome
- Add `fixture_category` (`positive` | `negative`) to `.seed/spiderfeet_map.tql`
- Bootstrap writes attribute from `osint_services.json` / `fixture_category_for_service()`
- Sync script: `.seed/scripts/sync_fixture_category.py`

## Spec
R2-03-01, R2-04-08

## Acceptance
- Bootstrap query includes `fixture_category`
- Map force-graph nodes expose category when seeded
- `sync_fixture_category.py --write` updates catalog JSON

## Related
`.seed/planning/issues/SF-04C-negative-fixture-semantics.md`
