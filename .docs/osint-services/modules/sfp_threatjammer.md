# Threat Jammer

**Module ID:** `sfp_threatjammer`

## Summary

Check if an IP address is malicious according to ThreatJammer.com

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://threatjammer.com
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://threatjammer.com/docs/what-is-threat-jammer, https://threatjammer.com/docs/how-threat-jammer-works, https://threatjammer.com/docs/introduction-threat-jammer-user-api, https://threatjammer.com/docs/introduction-threat-jammer-report-api, https://threatjammer.com/tutorials/how-to-configure-fail2ban-in-ubuntu, https://threatjammer.com/tutorials/how-to-configure-cowrie-honeypot

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

- **Flags:** apikey
- **Categories:** Reputation Systems
- **Use cases:** Passive, Investigate

## Module options

- `api_hostname` — User API hostname
- `api_key` — Threat Jammer API key.
- `checkaffiliates` — Apply checks to affiliates?
- `risk_score_min` — Minimum Threat Jammer risk score

## Catalogue notes

Threat Jammer is a service to access high-quality threat intelligence data from a variety of sources, and integrate it into their applications with the sole purpose of detecting and blocking malicious activity.
