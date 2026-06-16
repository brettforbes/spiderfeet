**Parent epic:** #716

## Problem statement

`modules/sfp_archiveorg.py` uses Wayback Availability API but has correctness gaps.

## Scope

- URL-encode `eventData` in `wayback/available` requests
- Respect `archived_snapshots.closest.available is False` (skip, do not emit historic nugget)
- Guard missing `closest` key safely
- Review `farback` semantics vs OSINT intent (snapshots at N days ago vs any historic capture)
- Update module `meta` references to [Wayback API docs](https://archive.org/help/wayback_api.php) (not generic search docs only)

## Acceptance criteria

- [ ] Unit test with mocked JSON for empty/missing/unavailable snapshots
- [ ] Live smoke: `INTERESTING_FILE` for `https://example.com` produces historic event when snapshot exists
- [ ] No unhandled exceptions on malformed API payloads

## Spec binding

- SPEC-002: R2-04-03

## References

- `.docs/analysis/archiveorg_wayback_vs_search.md`
