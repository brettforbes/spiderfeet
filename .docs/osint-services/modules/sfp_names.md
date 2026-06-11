# Human Name Extractor

**Module ID:** `sfp_names`

## Summary

Attempt to identify human names in fetched content.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_names
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_names

## Routes

- **Route seed nugget:** `TARGET_WEB_CONTENT`
- **Consumed:**
- `TARGET_WEB_CONTENT`
- `EMAILADDR`
- `DOMAIN_WHOIS`
- `NETBLOCK_WHOIS`
- `RAW_RIR_DATA`
- `RAW_FILE_META_DATA`
- **Produced:**
- `HUMAN_NAME`

## Flags and categories

- **Flags:** errorprone
- **Categories:** Content Analysis
- **Use cases:** Footprint, Passive

## Module options

- `algolimit` — A value between 0-100 to tune the sensitivity of the name finder. Less than 40 will give you a lot of junk, over 50 and you'll probably miss things but will have less false positives.
- `emailtoname` — Convert e-mail addresses in the form of firstname.surname@target to names?
- `filterjscss` — Filter out names that originated from CSS/JS content. Enabling this avoids detection of popular Javascript and web framework author names.

## Test seeds

- `TARGET_WEB_CONTENT`: input=`Qwzxxy Plugh announced results today` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Attempt to identify human names in fetched content.

**Module ID:** `sfp_names`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** TARGET_WEB_CONTENT, EMAILADDR, DOMAIN_WHOIS, NETBLOCK_WHOIS, RAW_RIR_DATA, RAW_FILE_META_DATA
**Produces:** HUMAN_NAME
**Flags:** errorprone

**Smoke battery:**
- Classification: `clean_miss`
- Seed nugget: `TARGET_WEB_CONTENT`
- Input: `Contact "Jane Citizen" for details`
- Produced count: 0
