# CleanBrowsing.org

**Module ID:** `sfp_cleanbrowsing`

## Summary

Check if a host would be blocked by CleanBrowsing.org DNS content filters.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://cleanbrowsing.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://cleanbrowsing.org/guides/, https://cleanbrowsing.org/filters/, https://cleanbrowsing.org/how-it-works, https://cleanbrowsing.org/web-filtering-for-shools-and-cipa-compliance, https://cleanbrowsing.org/getting-started

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `AFFILIATE_INTERNET_NAME`
- `CO_HOSTED_SITE`
- **Produced:**
- `BLACKLISTED_INTERNET_NAME`
- `BLACKLISTED_AFFILIATE_INTERNET_NAME`
- `BLACKLISTED_COHOST`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_INTERNET_NAME`
- `MALICIOUS_COHOST`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

You get to decide what type of content is allowed in your home or network via our DNS-based content filtering service. Parents can protect their kids from adult content, schools can be CIPA compliant and businesses can block malicious domains and gain visibility into their network.
CleanBrowsing is a DNS-based content filtering service that offers a safe way to browse the web without surprises. It intercepts domain requests and filter sites that should be blocked, based on your requirements. Our free family filter, for example, blocks adult content, while still allowing Google, Youtube, Bing, DuckDuckGo and the rest of the web to load safely.
