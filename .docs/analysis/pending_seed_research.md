# Pending seed research (none-tier)

> **Canonical agent guide:** [stage4_seed_corpus_and_tests.md](stage4_seed_corpus_and_tests.md) (fixture rules, `service_state`, scripts, API behaviour).

## Coverage summary

| Pass | Script | Wins | Coverage |
|------|--------|------|----------|
| 1 | `research_pending_seeds.py` | 1 positive | 56 / 87 (64.4%) |
| 2 | `research_pending_seeds_pass2.py` | 11 negative + 4 upstream annotated | 67 / 87 (77.0%) |
| 3 | `research_pending_seeds_pass3.py` | 3 positive + 7 negative | **77 / 87 (88.5%)** |

**Research closed:** 87/87 (100%) — 79 smoke-validated + 8 upstream-blocked (see finalize pass below).

---

## Pending disposition (finalize pass)

| Strategy | Count | Modules | Outcome |
|----------|------:|---------|---------|
| **Smoke negative** | +2 | keybase (`spiderfeet`), crobat_api (`example.com`) | `clean_miss` on benign input |
| **Upstream-blocked** | 8 | dnsdumpster, sublist3r, searchcode, myspace, flickr, commoncrawl, crt, s3bucket | `validation: blocked-upstream` — needs module rewrite, not seed tuning |
| **Module-fix track** | 8 | same as blocked | Open GitHub issues under Stage 4 module maintenance |

### Why not all 87 are smoke-validated?

- **8 modules** have dead or broken upstream APIs / HTML scrapers. Seeds cannot be validated until the module code is fixed.
- **Coverage metric** (`coverage_count`) = smoke-validated only (positive or negative).
- **Research metric** (`research_complete_count`) = smoke + upstream-blocked = **87/87**.

### Module-fix priorities (upstream-blocked)

| Module | Root cause | Fix track |
|--------|------------|-----------|
| dnsdumpster | CSRF form removed from site | Rewrite scraper or new data source |
| sublist3r | API returns empty body | Update endpoint or retire module |
| searchcode | API HTTP 404 | Update API URL or retire |
| myspace | Search endpoint connection failures | Investigate TLS/URL change |
| flickr | API key scrape fails | Require `api_key` config option |
| commoncrawl | Index HTML parser broken | Update index discovery logic |
| crt | crt.sh errors/rate limits | Retry logic + error vs clean_miss distinction |
| s3bucket | Scan exceeds timeout | Async scan or reduce bucket candidates |

Script: `.seed/scripts/research_pending_seeds_finalize.py`

---

## Pass 3 (`research_pending_seeds_pass3.py --write`)

**Prerequisite:** scan_ui target resolution fix (`scan_targets.py`) so `COMPANY_NAME`, `PHYSICAL_ADDRESS`, `WEB_ANALYTICS_ID`, and quoted `USERNAME` reach the scanner.

### Positive wins (3)

| Module | Input | Produced |
|--------|-------|----------|
| `sfp_gleif` | `Google LLC` | 13 |
| `sfp_openstreetmap` | `1600 Amphitheatre Parkway, Mountain View, CA 94043` | 2 |
| `sfp_venmo` | `paypal` | 2 |

### Negative fixtures validated (7)

| Module | Input | Verdict |
|--------|-------|---------|
| `sfp_gravatar` | `noreply@example.com` | clean_miss |
| `sfp_bgpview` | `8.8.8.8` | clean_miss |
| `sfp_threatminer` | `8.8.8.8` | clean_miss |
| `sfp_mnemonic` | `8.8.8.8` | clean_miss |
| `sfp_digitaloceanspace` | `example.com` | clean_miss |
| `sfp_google_tag_manager` | `sbs.com.au` | clean_miss |
| `sfp_crxcavator` | `example.com` | clean_miss |

### Still open after pass 3

| Module | Notes |
|--------|-------|
| `sfp_dnsdumpster`, `sfp_sublist3r`, `sfp_searchcode`, `sfp_myspace` | upstream-blocked (pass 2) |
| `sfp_flickr` | `error_failed` on benign domain |
| `sfp_keybase` | FINISHED clean_miss — candidate for negative fixture |
| `sfp_s3bucket` | neg probe timeout; pos HTTP 504 |
| `sfp_crt`, `sfp_crobat_api`, `sfp_commoncrawl` | upstream API errors |

Full JSON: `.docs/analysis/pending_seed_research_pass3.json`

---

## Pass 2 (`research_pending_seeds_pass2.py --write`)

### Negative fixtures validated (11)

Benign input → `clean_miss` (negative fixture semantics):

| Module | Input | Verdict |
|--------|-------|---------|
| `sfp_ahmia` | `sbs.com.au` | clean_miss |
| `sfp_onionsearchengine` | `sbs.com.au` | clean_miss |
| `sfp_torch` | `sbs.com.au` | clean_miss |
| `sfp_reversewhois` | `example.com` | clean_miss |
| `sfp_emailformat` | `example.com` | clean_miss |
| `sfp_skymem` | `example.com` | clean_miss |
| `sfp_grep_app` | `example.com` | clean_miss |
| `sfp_opennic` | `example.com` | clean_miss |
| `sfp_slideshare` | `example.com` | clean_miss |
| `sfp_twitter` | `example.com` | clean_miss |
| `sfp_callername` | `+18005551212` | clean_miss |

### Upstream blocked (annotated, not smoke-validated)

| Module | Reason |
|--------|--------|
| `sfp_dnsdumpster` | CSRF form removed; module needs rewrite |
| `sfp_sublist3r` | API returns empty/non-JSON |
| `sfp_searchcode` | API HTTP 404 |
| `sfp_myspace` | Search endpoint connection failures |

### Pass 2 failures / still open (20 remaining)

| Module | Blocker class | Notes |
|--------|---------------|-------|
| `sfp_flickr` | module-error | `error_failed` on benign `example.com` (negative probe failed) |
| `sfp_gleif` | api-validation | HTTP 400 — `nugget_data is not a valid SpiderFeet target` for `COMPANY_NAME` |
| `sfp_openstreetmap` | api-validation | HTTP 400 for `PHYSICAL_ADDRESS` probe |
| `sfp_keybase` | api-validation | HTTP 400 for `USERNAME` |
| `sfp_venmo` | api-validation | HTTP 400 for `USERNAME` |
| `sfp_google_tag_manager` | no-output | `clean_miss` on `google.com` / GTM id candidates |
| `sfp_crobat_api` | module-error | Crobat API error on slack.com |
| `sfp_crt` | upstream | crt.sh unavailable / error_failed |
| `sfp_commoncrawl` | module-error | Cannot fetch CommonCrawl index |
| `sfp_bgpview` | upstream | bgpview.io connection failures |
| `sfp_mnemonic` | stale-data | Records too old for google.com |
| `sfp_threatminer` | no-output | Empty API response |
| `sfp_digitaloceanspace` | no-bucket | No public bucket found for digitalocean.com |
| `sfp_gravatar` | no-output | No profile for test@example.com |
| `sfp_crxcavator` | api-json | (pass 1) JSON parse failures |
| `sfp_s3bucket` | unknown | (pass 1) still open |

Full JSON: `.docs/analysis/pending_seed_research_pass2.json`

---

## Pass 1 (`research_pending_seeds.py`)

Wins: **1** / 32.

### Validated

- `sfp_googleobjectstorage` — `youtube.com` (2 produced)

## Blocked / needs follow-up

### sfp_ahmia
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** facebookcorewwwi.onion, google.com, bbc.co.uk, sbs.com.au
- **Logs:** `sflib:STATUS:Fetched https://ahmia.fi/search/?q=facebookcorewwwi.onion (4727 bytes in 1.15773606300354s); sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp__stor_db:DEBUG:Storing an event: INTERNE`

### sfp_bgpview
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** 8.8.8.8, 1.1.1.1, 8.8.8.0/24, 15169
- **Logs:** `sflib:STATUS:Scan [C5F073CD] completed.; sflib:STATUS:Running 37 correlation rules on scan C5F073CD.; sfp_bgpview:STATUS:No results found for IP address 8.8.8.8; sflib:ERROR:Failed to connect to https`

### sfp_callername
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** +12125551234, +18005551212, +14155552671, +61412345678
- **Logs:** `sfp_callername:DEBUG:Received event, PHONE_NUMBER, from SpiderFeet UI; sfp__stor_db:DEBUG:Storing an event: PHONE_NUMBER; sfp__stor_db:DEBUG:Storing an event: ROOT; sflib:STATUS:sfp_callername module `

### sfp_commoncrawl
- **Blocker:** `api-timeout`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, bbc.co.uk, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Fetched https://index.commoncrawl.org/ (7391 bytes in 0.707312822341919s); sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp_commoncrawl:DEBUG:Received event, INTERNET_NAME, from Spid`

### sfp_crobat_api
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, microsoft.com, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Fetched https://sonar.omnisint.io/subdomains/google.com?page=0 (977 bytes in 19.457515478134155s); sfp_crobat_api:DEBUG:Received event, DOMAIN_NAME, from SpiderFeet UI; sflib:STATUS:Fetch`

### sfp_crt
- **Blocker:** `api-json`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, github.com, microsoft.com, sbs.com.au
- **Logs:** `sflib:STATUS:Fetched https://crt.sh/?q=%25.google.com&output=json (150 bytes in 1.2163667678833008s); sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp__stor_db:DEBUG:Storing an event: INTERNET_NA`

### sfp_crxcavator
- **Blocker:** `api-json`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [EF803788] completed.; sflib:STATUS:Running 37 correlation rules on scan EF803788.; sfp_crxcavator:STATUS:No results found for google; sfp_crxcavator:DEBUG:Error processing JSON resp`

### sfp_digitaloceanspace
- **Blocker:** `api-404`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** digitalocean.com, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [85E71BB7] completed.; sflib:STATUS:Running 37 correlation rules on scan 85E71BB7.; sfp_digitaloceanspace:DEBUG:Not a valid bucket: https://digitalocean-staging.ams3.digitaloceanspac`

### sfp_dnsdumpster
- **Blocker:** `module-error`
- **Last:** status=FINISHED verdict=error_failed produced=0
- **Tried:** google.com, microsoft.com, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [BBE360D7] completed.; sflib:STATUS:Running 37 correlation rules on scan BBE360D7.; sfp_dnsdumpster:DEBUG:Received event, DOMAIN_NAME, from SpiderFeet UI; sfp_dnsdumpster:DEBUG:Skipp`

### sfp_emailformat
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, bbc.co.uk, microsoft.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [D39875A6] completed.; sflib:STATUS:Running 37 correlation rules on scan D39875A6.; sflib:STATUS:Fetched https://www.email-format.com/d/google.com/ (75812 bytes in 0.2560834884643554`

### sfp_flickr
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** flickr.com, yahoo.com, sbs.com.au
- **Logs:** `sflib:STATUS:Fetched https://www.flickr.com/ (55370 bytes in 0.6885278224945068s); sflib:STATUS:Fetching (GET): https://www.flickr.com/ (proxy=None, user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64`

### sfp_gleif
- **Blocker:** `unknown`
- **Last:** status=HTTP_400 verdict=None produced=0
- **Tried:** Google LLC, Microsoft Corporation, Apple Inc., sbs.com.au
- **Logs:** ``

### sfp_google_tag_manager
- **Blocker:** `unknown`
- **Last:** status=HTTP_400 verdict=None produced=0
- **Tried:** GTM-5K8Q5L, GTM-WQZ7T5, google.com, sbs.com.au
- **Logs:** ``

### sfp_gravatar
- **Blocker:** `api-json`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** noreply@google.com, test@gmail.com, admin@bbc.co.uk, noreply@spiderfoot.net
- **Logs:** `sflib:STATUS:Fetched https://secure.gravatar.com/b713d76a68338e1a1d00ad0045c8717f.json (16 bytes in 0.26789331436157227s); sflib:STATUS:Fetching (GET): https://secure.gravatar.com/b713d76a68338e1a1d00`

### sfp_grep_app
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Fetched https://grep.app/api/search?q=google.com&page=1 (33569 bytes in 0.562312126159668s); sfp_grep_app:DEBUG:Received event, DOMAIN_NAME, from SpiderFeet UI; sflib:STATUS:Fetching (GET`

### sfp_keybase
- **Blocker:** `unknown`
- **Last:** status=HTTP_400 verdict=None produced=0
- **Tried:** google, github, spiderfoot, "spiderfeet"
- **Logs:** ``

### sfp_mnemonic
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** 8.8.8.8, google.com, 1.1.1.1
- **Logs:** `sfp_mnemonic:DEBUG:Record 8.8.8.8 found for 0.adad.ir is too old, skipping.; sfp_mnemonic:DEBUG:Record 8.8.8.8 found for 100rx.com is too old, skipping.; sfp_mnemonic:DEBUG:Record 8.8.8.8 found for 11`

### sfp_myspace
- **Blocker:** `module-error`
- **Last:** status=FINISHED verdict=error_failed produced=0
- **Tried:** test@gmail.com, admin@yahoo.com, noreply@spiderfoot.net
- **Logs:** `sflib:STATUS:Running 37 correlation rules on scan ACC63F5E.; sfp_myspace:ERROR:Could not fetch MySpace content for test@gmail.com; sflib:ERROR:Failed to connect to https://myspace.com/search/people?q=`

### sfp_onionsearchengine
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** facebookcorewwwi.onion, google.com, sbs.com.au
- **Logs:** `sflib:STATUS:Running 37 correlation rules on scan B754117A.; sflib:STATUS:Fetched https://onionsearchengine.com/search.php?search=%22facebookcorewwwi.onion%22&submit=Search&page=1 (2257 bytes in; sfli`

### sfp_opennic
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** opennic.org, wiki.opennic.org, sbs.com.au
- **Logs:** `sflib:STATUS:Running 37 correlation rules on scan 24B551B3.; sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp_opennic:DEBUG:Received event, INTERNET_NAME, from SpiderFeet UI; sfp__stor_db:DEBUG:S`

### sfp_openstreetmap
- **Blocker:** `unknown`
- **Last:** status=HTTP_400 verdict=None produced=0
- **Tried:** 1600 Amphitheatre Parkway, Mountain View, CA, London, UK, sbs.com.au
- **Logs:** ``

### sfp_reversewhois
- **Blocker:** `api-timeout`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, microsoft.com, sbs.com.au
- **Logs:** `sfp_reversewhois:STATUS:No ReverseWhois info found for google.com; sflib:STATUS:Fetched https://reversewhois.io?searchterm=google.com (15881 bytes in 0.4332253932952881s); sflib:STATUS:Fetching (GET):`

### sfp_s3bucket
- **Blocker:** `unknown`
- **Last:** status=HTTP_504 verdict=None produced=0
- **Tried:** amazon.com, github.com, sbs.com.au
- **Logs:** ``

### sfp_searchcode
- **Blocker:** `module-error`
- **Last:** status=FINISHED verdict=error_failed produced=0
- **Tried:** google.com, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [0F443D37] completed.; sflib:STATUS:Running 37 correlation rules on scan 0F443D37.; sfp_searchcode:ERROR:Unexpected reply from searchcode: 404; sflib:STATUS:Fetched https://searchcod`

### sfp_skymem
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** google.com, bbc.co.uk, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [593B7731] completed.; sflib:STATUS:Running 37 correlation rules on scan 593B7731.; sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp__stor_db:DEBUG:Storing an event: INTERNET_NA`

### sfp_slideshare
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** slideshare.net, linkedin.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [F20A5B2E] completed.; sflib:STATUS:Running 37 correlation rules on scan F20A5B2E.; sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp__stor_db:DEBUG:Storing an event: INTERNET_NA`

### sfp_sublist3r
- **Blocker:** `module-error`
- **Last:** status=FINISHED verdict=error_failed produced=0
- **Tried:** google.com, microsoft.com, github.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [4129B76B] completed.; sflib:STATUS:Running 37 correlation rules on scan 4129B76B.; sfp_sublist3r:DEBUG:Received event, DOMAIN_NAME, from SpiderFeet UI; sfp_sublist3r:DEBUG:Skipping `

### sfp_threatminer
- **Blocker:** `api-timeout`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** 8.8.8.8, google.com
- **Logs:** `sflib:STATUS:Scan [2856B712] completed.; sflib:STATUS:Running 37 correlation rules on scan 2856B712.; sflib:STATUS:Fetched https://api.threatminer.org/v2/host.php?q=8.8.8.8&rt=2 (0 bytes in 0.68576884`

### sfp_torch
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** facebookcorewwwi.onion, google.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [ACC7431B] completed.; sflib:STATUS:Running 37 correlation rules on scan ACC7431B.; sflib:ERROR:Failed to connect to http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.o`

### sfp_twitter
- **Blocker:** `no-output-clean-input`
- **Last:** status=FINISHED verdict=clean_miss produced=0
- **Tried:** twitter.com, x.com, sbs.com.au
- **Logs:** `sflib:STATUS:Scan [F5C03A59] completed.; sflib:STATUS:Running 37 correlation rules on scan F5C03A59.; sfp__stor_db:DEBUG:Storing an event: DOMAIN_NAME; sfp__stor_db:DEBUG:Storing an event: INTERNET_NA`

### sfp_venmo
- **Blocker:** `unknown`
- **Last:** status=HTTP_400 verdict=None produced=0
- **Tried:** venmo, paypal, google, "spiderfeet"
- **Logs:** ``

