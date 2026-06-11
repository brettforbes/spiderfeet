# AdBlock Check

**Module ID:** `sfp_adblock`

## Summary

Check if linked pages would be blocked by AdBlock Plus.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://adblockplus.org/
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://help.eyeo.com/en/adblockplus/, https://adblockplus.org/en/download, https://adblockplus.org/en/filters#options, https://chrome.google.com/webstore/detail/adblock-plus-free-ad-bloc/cfhdojbkjhnklbpkdaibdccddilifddb

## Routes

- **Route seed nugget:** `LINKED_URL_EXTERNAL`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- `LINKED_URL_EXTERNAL`
- `PROVIDER_JAVASCRIPT`
- **Produced:**
- `URL_ADBLOCKED_INTERNAL`
- `URL_ADBLOCKED_EXTERNAL`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `blocklist` — AdBlockPlus block list.
- `cacheperiod` — Hours to cache list data before re-fetching.

## Catalogue notes

Adblock Plus is a free extension that allows you to customize your web experience.You can block annoying ads, disable tracking and lots more.It’s available for all major desktop browsers and for your mobile devices.
Block ads that interrupt your browsing experience.Say goodbye to video ads, pop-ups, flashing banners and more.Blocking these annoyances means pages load faster.
With Adblock Plus avoiding tracking and malware is easy.Blocking intrusive ads reduces the risk of "malvertising" infections.Blocking tracking stops companies following your online activity.
