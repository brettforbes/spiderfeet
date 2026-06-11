# AbuseIPDB

**Module ID:** `sfp_abuseipdb`

## Summary

Check if an IP address is malicious according to AbuseIPDB.com blacklist.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.abuseipdb.com
- **Model:** `FREE_AUTH_LIMITED`
- **References:** https://docs.abuseipdb.com/#introduction, https://www.abuseipdb.com/fail2ban.html, https://www.abuseipdb.com/csf, https://www.abuseipdb.com/suricata, https://www.abuseipdb.com/splunk, https://www.abuseipdb.com/categories

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

- `api_key` — AbuseIPDB.com API key.
- `checkaffiliates` — Apply checks to affiliates?
- `confidenceminimum` — The minimium AbuseIPDB confidence level to require.
- `limit` — Maximum number of results to retrieve.

## Catalogue notes

AbuseIPDB is a project dedicated to helping combat the spread of hackers,spammers, and abusive activity on the internet.
Our mission is to help make Web safer by providing a central blacklist forwebmasters, system administrators, and other interested parties toreport and find IP addresses that have been associated with malicious activity online.
