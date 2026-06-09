# Archive.org — Wayback module vs Search API

**Module:** `sfp_archiveorg`  
**Status:** `in-test` (upstream Wayback API operational; not an upstream-shutdown case like BinaryEdge).

## What the module uses today

`modules/sfp_archiveorg.py` calls the **Wayback Availability JSON API**:

```
GET https://archive.org/wayback/available?url={url}&timestamp={YYYYMMDD}
```

Documented at [Wayback Machine APIs](https://archive.org/help/wayback_api.php). Live probes return HTTP 200 with expected JSON (`archived_snapshots.closest` or empty `{}`).

This is **not** the Internet Archive **metadata search** API described in [About Search](https://archive.org/help/aboutsearch.htm).

## What About Search covers (different product surface)

| API | Purpose | Notes |
|-----|---------|-------|
| `advancedsearch.php` | Metadata search | Paged results capped at **10,000** sorted pages |
| `/services/search/v1/scrape` | Deep metadata search | Cursor-based; replaces deep paging past 10k limit |

Both are for searching **items in the archive catalogue** (books, collections, etc.), not for resolving historic **web page snapshots** for OSINT URL inputs.

SpiderFeet does **not** call these endpoints today. A future module or route expansion would be new scope, not a drop-in fix for `sfp_archiveorg`.

## Issues found (2026-06)

### 1. Map / subscription false positive (fixed)

Catalogue opt `passwordpages` (boolean: query password URL types) matched substring `password` in `is_secret_module_opt()`, causing `requires_api_key: true` for a `free_no_auth` service. Map “needs subscription” filter incorrectly hid Archive.org from the open-services bucket.

### 2. Module hardening gaps (open)

- No `urllib.parse.quote` on `eventData` in Wayback URL
- Does not check `archived_snapshots.closest.available is False`
- Possible `KeyError` if `closest` missing while `archived_snapshots` non-empty
- `farback` only checks snapshots near 30/60/90 **days ago**, not “any historic capture” — may miss obvious Wayback hits

### 3. Stage 4 testing

- No entries in `module_test_seeds.json` yet
- Module test issue: GitHub #470

## Optional enhancements (backlog)

- **CDX Server API** for richer historic URL queries ([Wayback CDX](https://archive.org/help/wayback_api.php))
- Separate metadata-search module using scraping API if catalogue search becomes a product requirement

## References

- [Wayback Machine APIs](https://archive.org/help/wayback_api.php)
- [Archive.org About Search](https://archive.org/help/aboutsearch.htm)
- [Scraping search API](https://archive.org/services/search/v1/scrape)
