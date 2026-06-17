## Outcome (revised 2026-06-05)

API platform for module tests: `scan_ui`, strict pass semantics, subscription tier metadata, Subscriptions key API.

## Child stories

### Original
- #67–#73 Route test execution stories
- #68 API run module test (**revised** — strict pass + key gate)

### New
- #657 SF-04C-10 Subscription tier classification + fix `api_hostname` key-detection bug
- #658 SF-04C-11 Subscriptions API (CRUD keys → module opts)

## Widget consumers
- spiderfeet-widget #48–#51, #50 visibility gate

## Spec binding
- SPEC-002: R2-04-03, R2-04-05 (SPEC_GAP), R2-04-06 (SPEC_GAP), R2-04-08 (SPEC_GAP)

## Board state
**Ready** for #657 (no deps); #658 depends on tier model; widget #49 depends on #658.
