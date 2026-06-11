# Internet Storm Center

**Module ID:** `sfp_isc`

## Summary

Check if an IP address is malicious according to SANS ISC.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://isc.sans.edu
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://isc.sans.edu/api/, https://isc.sans.edu/howto.html, https://isc.sans.edu/honeypot.html, https://isc.sans.edu/glossary.html, https://isc.sans.edu/fightback.html

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `checkaffiliates` — Apply checks to affiliates?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

The ISC provides a free analysis and warning service to thousands of Internet users and organizations, and is actively working with Internet Service Providers to fight back against the most malicious attackers.
Thousands of sensors that work with most firewalls, intrusion detection systems, home broadband devices, and nearly all operating systems are constantly collecting information about unwanted traffic arriving from the Internet. These devices feed the DShield database where human volunteers as well as machines pour through the data looking for abnormal trends and behavior. The resulting analysis is posted to the ISC's main web page where it can be automatically retrieved by simple scripts or can be viewed in near real time by any Internet user.
