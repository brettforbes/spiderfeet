# Open Bug Bounty

**Module ID:** `sfp_openbugbounty`

## Summary

Check external vulnerability scanning/reporting service openbugbounty.org to see if the target is listed.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.openbugbounty.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.openbugbounty.org/cert/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `VULNERABILITY_DISCLOSURE`

## Flags and categories

- **Flags:** —
- **Categories:** Leaks, Dumps and Breaches
- **Use cases:** Footprint, Investigate, Passive

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

Open Bug Bounty is an open, disintermediated, cost-free, and community-driven bug bounty platform for coordinated, responsible and ISO 29147 compatible vulnerability disclosure.
The role of Open Bug Bounty is limited to independent verification of the submitted vulnerabilities and proper notification of website owners by all available means. Once notified, the website owner and the researcher are in direct contact to remediate the vulnerability and coordinate its disclosure. At this and at any later stages, we never act as an intermediary between website owners and security researchers.
