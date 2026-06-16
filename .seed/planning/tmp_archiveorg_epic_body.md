## Problem statement

`sfp_archiveorg` (Archive.org / Wayback Machine) is misbehaving in SpiderFeet operator UI and needs hardening — **not** an upstream shutdown (unlike BinaryEdge #710).

The user flagged [Archive.org About Search](https://archive.org/help/aboutsearch.htm); that documents **metadata search** APIs (`advancedsearch.php`, scraping API). Our module uses the separate **Wayback Availability API** ([wayback_api.php](https://archive.org/help/wayback_api.php)), which is still operational.

## Issues identified

1. **Map false positive (fix in progress):** opt name `passwordpages` triggered `requires_api_key` via substring `password` → service shown as “needs subscription” despite `free_no_auth`.
2. **Module gaps:** no URL encoding; ignores `available: false`; weak snapshot date logic (`farback` only).
3. **Stage 4:** no test seeds; #470 blocked on seeds + validation.

Analysis: `.docs/analysis/archiveorg_wayback_vs_search.md`

## Child work

- [ ] Module hardening (Wayback API correctness)
- [ ] Map/subscription classification fix + catalogue doc references
- [ ] Tests + seeds; complete #470

## Spec binding

- SPEC-002: R2-03-02 (map), R2-04-03 (module tests), R2-04-06 (subscriptions)

## Non-goals (unless explicitly scoped)

- New metadata-search module using scraping API (different product surface)

## Related

- #470 — module test issue
