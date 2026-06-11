# ThreatMiner

**Module ID:** `sfp_threatminer`

## Summary

Obtain information from ThreatMiner's database for passive DNS and threat intelligence.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://www.threatminer.org/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://www.threatminer.org/api.php, https://www.threatminer.org/features.php

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `IP_ADDRESS`
- `DOMAIN_NAME`
- `NETBLOCK_OWNER`
- `NETBLOCK_MEMBER`
- **Produced:**
- `INTERNET_NAME`
- `CO_HOSTED_SITE`

## Flags and categories

- **Flags:** —
- **Categories:** Search Engines
- **Use cases:** Footprint, Investigate, Passive

## Module options

- `age_limit_days` — Ignore records older than this many days. 0 = Unlimited.
- `maxcohost` — Stop reporting co-hosted sites after this many are found, as it would likely indicate web hosting.
- `maxnetblock` — If looking up owned netblocks, the maximum netblock size to look up all IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `maxsubnet` — If looking up subnets, the maximum subnet size to look up all the IPs within (CIDR value, 24 = /24, 16 = /16, etc.)
- `netblocklookup` — Look up all IPs on netblocks deemed to be owned by your target for possible blacklisted hosts on the same target subdomain/domain?
- `subnetlookup` — Look up all IPs on subnets which your target is a part of?
- `verify` — Verify that any hostnames found on the target domain still resolve?

## Test seeds

- `DOMAIN_NAME`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)
- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss; Pass 3 benign input; expect clean_miss (negative fixture)

## Catalogue notes

ThreatMiner is a threat intelligence portal designed to enable analysts to research under a single interface. It is used in the SANS FOR578 Cyber Threat Intelligence course.
Threat intelligence and intrusion analysts who regularly perform research into malware and network infrastructure often find the need to rely on mutliple websites that individually holds a small piece of the larger puzzle.
