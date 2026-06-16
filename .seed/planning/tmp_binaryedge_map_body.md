**Parent epic:** #710

## Problem statement

Map and catalogue still describe BinaryEdge.io (`access_tier: free_auth`, binaryedge branding, `binaryedge_api_key`). These must reflect Coalition Control and interim `error` → future `in-test` state.

## Scope

- `osint_services.json`: name/summary, `data_source`, references, `module_opts`, `access_tier`, logos
- `service_state` lifecycle: remain `error` until module rewrite verified; sync via `sync_service_state.py`
- TypeDB map nodes: `requires_api_key` / service metadata after catalogue update
- Signup metadata: `signup_url`, `signup_bucket`, notes in `signup_links.py` if applicable
- Widget Maps: error filter already shows service; confirm icon/branding after rebrand

## Acceptance criteria

- [ ] Catalogue documents Coalition Control, not binaryedge.io
- [ ] Map graph shows correct service_state and auth requirement flags
- [ ] `sync_service_state.py --write --typedb` run after state promotion
- [ ] Transition doc cross-linked from catalogue references

## Spec binding

- SPEC-002: R2-03-02 (map catalogue)

## References

- `.docs/analysis/binaryedge_coalition_control_transition.md`
