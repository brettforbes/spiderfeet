**Epic:** #723 · **Phase:** 2b · **Depends:** #796 · **Blocks:** #799

## Problem

Each CLI tool is a separate Python module duplicating subprocess, timeout, and parse logic.

## Desired outcome

Single **`sfp_tool_runner`** (or core `spiderfeet/tool_runner.py`) that:

1. Loads manifest by `module_id` / service id
2. On consumed nugget event: build argv from template, run subprocess, capture stdout/stderr
3. Apply manifest output mappings → emit `SpiderFeetEvent`s
4. Set `errorState` on missing binary, timeout, non-zero exit (configurable)
5. Register as dynamic module or static plugin delegating to manifests

## Acceptance criteria

- [ ] Runner executes 3 reference manifests from #796 end-to-end via `scan_ui`
- [ ] Timeouts and missing-binary paths produce `error_failed` / logged evidence
- [ ] No `shell=True`; argv list only
- [ ] Unit tests with mocked subprocess

## Verification

- `pytest` for runner + integration probe via `run_quarantine_battery.py --local`
- Compare output event types to legacy `sfp_tool_dnstwist` / `sfp_tool_wafw00f` where migrated

## Spec

R3-05-08

## Notes

Keep legacy `sfp_tool_*` modules until parity proven; migration is #799 follow-up.
