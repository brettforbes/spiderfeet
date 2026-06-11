# VXVault.net

**Module ID:** `sfp_vxvault`

## Summary

Check if a domain or IP address is malicious according to VXVault.net.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** http://vxvault.net/
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** http://vxvault.net/URL_List.php, https://github.com/InfectedPacket/VxVault

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- `IP_ADDRESS`
- `IPV6_ADDRESS`
- `AFFILIATE_IPADDR`
- `AFFILIATE_IPV6_ADDRESS`
- `AFFILIATE_INTERNET_NAME`
- `CO_HOSTED_SITE`
- **Produced:**
- `MALICIOUS_IPADDR`
- `MALICIOUS_INTERNET_NAME`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_AFFILIATE_INTERNET_NAME`
- `MALICIOUS_COHOST`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliates?
- `checkcohosts` — Apply checks to sites found to be co-hosted on the target's IP?

## Test seeds

- `INTERNET_NAME`: input=`sbs.com.au` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

VxVault is a malware management program to automatically download and classify malware samples. VxVault downloads malware samples from links from online sources such as webpages or RSS feeds, downloads them and attempts to identify the malware using VirusTotal. It then sort the malware onto a local file system and into a SQLite database.
