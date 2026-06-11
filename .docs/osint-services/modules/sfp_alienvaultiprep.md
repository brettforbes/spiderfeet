# AlienVault IP Reputation

**Module ID:** `sfp_alienvaultiprep`

## Summary

Check if an IP or netblock is malicious according to the AlienVault IP Reputation database.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://cybersecurity.att.com/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://cybersecurity.att.com/documentation/, https://cybersecurity.att.com/resource-center, https://success.alienvault.com/s/article/Can-I-use-the-OTX-IP-Reputation-List-as-a-blocklist

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `NETBLOCK_MEMBER`
- `NETBLOCK_OWNER`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `BLACKLISTED_SUBNET`
- `BLACKLISTED_NETBLOCK`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_SUBNET`
- `MALICIOUS_NETBLOCK`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliates?
- `checknetblocks` — Report if any malicious IPs are found within owned netblocks?
- `checksubnets` — Check if any malicious IPs are found within the same subnet of the target?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

Looking at security through new eyes.
AT&T Business and AlienVault have joined forces to create AT&T Cybersecurity, with a vision to bring together the people, process, and technology that help businesses of any size stay ahead of threats.
