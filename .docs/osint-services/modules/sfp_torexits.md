# TOR Exit Nodes

**Module ID:** `sfp_torexits`

## Summary

Check if an IP adddress or netblock appears on the Tor Metrics exit node list.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://metrics.torproject.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://metrics.torproject.org/rs.html#search/flag:exit

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `NETBLOCK_OWNER`
- `NETBLOCKV6_OWNER`
- **Produced:**
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `TOR_EXIT_NODE`

## Flags and categories

- **Flags:** —
- **Categories:** Secondary Networks
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliates?
- `checknetblocks` — Report if any malicious IPs are found within owned netblocks?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

The relay search tool displays data about single relays and bridges in the Tor network.
