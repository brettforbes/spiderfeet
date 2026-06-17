**Epic:** #723 · **Phase:** 3 · **Widget:** #62 · **Depends:** #798, spiderfeet-widget #66

## Problem

User-registered CLI services must appear alongside catalogue services on Maps and Tests.

## Desired outcome

- Maps: nodes for `service_origin: custom` with distinct styling (extend quarantine/external/custom legend)
- Tests: module accordion includes custom CLI services; routes from manifest consumed nugget
- Subscriptions: N/A for CLI (`access_tier: none`) — show "Local CLI" badge

## Acceptance criteria

- [ ] Custom service appears on map after registration + bootstrap
- [ ] Tests tab can run module-all for custom service id
- [ ] Filter or legend distinguishes `custom` origin (reuse/fixture filter pattern from quarantine work)
- [ ] Document bootstrap trigger after save (auto vs manual button)

## Verification

- End-to-end: register via Add Service → see on Maps → run Tests route → pass/fail recorded

## Spec

R3-05-05, R3-05-08

## Links

spiderfeet-widget #66, spiderfeet #798
