Investigation note: Archive.org Wayback API is **not** shut down. [About Search](https://archive.org/help/aboutsearch.htm) documents metadata search APIs; `sfp_archiveorg` uses the separate [Wayback Availability API](https://archive.org/help/wayback_api.php).

**Bug found:** `passwordpages` module opt falsely classified as a secret → Map showed `requires_api_key: true` for this `free_no_auth` service.

Tracked under epic #716 (#717 module hardening, #718 map/subscriptions fix, #719 tests/seeds).

Analysis: `.docs/analysis/archiveorg_wayback_vs_search.md`
