# Mnemonic PassiveDNS

**Module ID:** `sfp_mnemonic`

## Summary

Obtain Passive DNS information from PassiveDNS.mnemonic.no.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.mnemonic.no
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.mnemonic.no/resources/whitepapers/, https://www.mnemonic.no/research-and-development/, https://docs.mnemonic.no/display/public/API/PassiveDNS+Integration+Guide

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `INTERNET_NAME`
- `DOMAIN_NAME`
- **Produced:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `INTERNAL_IP_ADDRESS`
- `CO_HOSTED_SITE`
- `INTERNET_NAME`
- `DOMAIN_NAME`

## Flags and categories

- **Flags:** —
- **Categories:** Passive DNS
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `cohostsamedomain` — Treat co-hosted sites on the same target domain as co-hosting?
- `max_pages` — Maximum number of pages of results to fetch.
- `maxage` — The maximum age of the data returned, in days, in order to be considered valid.
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `per_page` — Maximum number of results per page.
- `timeout` — Query timeout, in seconds.
- `verify` — Verify identified domains still resolve to the associated specified IP address.

## Test seeds

- `INTERNET_NAME`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)
- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)

## Catalogue notes

mnemonic helps businesses manage their security risks, protect their data and defend against cyber threats.
Our expert team of security consultants, product specialists, threat researchers, incident responders and ethical hackers, combined with our Argus security platform ensures we stay ahead of advanced cyberattacks and protect our customers from evolving threats.
