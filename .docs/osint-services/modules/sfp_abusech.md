# abuse.ch

**Module ID:** `sfp_abusech`

## Summary

Check if a host/domain, IP address or netblock is malicious according to Abuse.ch.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `free_auth (free_auth)` |
| test_status (route seed) | `not-validated` |

## Data source

- **Website:** https://www.abuse.ch
- **Model:** `FREE_AUTH_UNLIMITED`
- **References:** https://feodotracker.abuse.ch/, https://sslbl.abuse.ch/, https://urlhaus.abuse.ch/

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `NETBLOCK_MEMBER`
- `AFFILIATE_INTERNET_NAME`
- `AFFILIATE_IPADDR`
- `CO_HOSTED_SITE`
- `NETBLOCK_OWNER`
- **Produced:**
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_AFFILIATE_INTERNET_NAME`
- `MALICIOUS_SUBNET`
- `MALICIOUS_COHOST`
- `MALICIOUS_NETBLOCK`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Passive, Investigate

## Module options

- `abusefeodoip` — Enable abuse.ch Feodo IP check?
- `abusesslblip` — Enable abuse.ch SSL Backlist IP check?
- `abuseurlhaus` — Enable abuse.ch URLhaus check?
- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliates?
- `checkcohosts` — Apply checks to sites found to be co-hosted on the target's IP?
- `checknetblocks` — Report if any malicious IPs are found within owned netblocks?
- `checksubnets` — Check if any malicious IPs are found within the same subnet of the target?

## Catalogue notes

abuse.ch is operated by a random swiss guy fighting malware for non-profit, running a couple of projects helping internet service providers and network operators protecting their infrastructure from malware.
IT-Security researchers, vendors and law enforcement agencies rely on data from abuse.ch,trying to make the internet a safer place.
