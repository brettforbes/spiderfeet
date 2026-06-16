## Summary

- Adds **POST /api/v1/scan_ui** for widget workflows: consumed nugget + module_id, returns scan_record (TypeDB map shape), consumed[], produced[].
- Expands **.seed/spiderfeet_map.tql** scan-record with scan_status, scan_event_count, scan_results_by_type.
- **API reference** (`.docs/api/api_reference.md`), **Requestly** Postman collection + walkthrough, pytest (12 fast + 1 slow integration).

## Test plan

- [x] `poetry run pytest .tests/api -q -m "not slow"`
- [ ] `poetry run pytest .tests/api -q -m slow` (optional)
- [ ] Operator Requestly walkthrough (`.docs/api/requestly/WALKTHROUGH.md`) — sign-off on epic #26

## Spec

R2-02-01 / Epic #26
