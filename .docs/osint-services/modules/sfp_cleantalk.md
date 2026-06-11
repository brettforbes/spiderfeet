# CleanTalk Spam List

**Module ID:** `sfp_cleantalk`

## Summary

Check if a netblock or IP address is on CleanTalk.org's spam IP list.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `external-api` |
| service_state | `in-test` |
| fixture_category | `negative` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** https://cleantalk.org
- **Model:** `FREE_NOAUTH_UNLIMITED`
- **References:** https://cleantalk.org/help, https://cleantalk.org/help/introduction, https://cleantalk.org/help/api-spam-check, https://cleantalk.org/wordpress-security-malware-firewall, https://cleantalk.org/price-anti-spam, https://cleantalk.org/ssl-certificates/cheap-positivessl-certificate, https://cleantalk.org/email-checker, https://cleantalk.org/blacklists

## Routes

- **Route seed nugget:** `IP_ADDRESS`
- **Consumed:**
- `IP_ADDRESS`
- `AFFILIATE_IPADDR`
- `NETBLOCK_OWNER`
- `NETBLOCK_MEMBER`
- **Produced:**
- `BLACKLISTED_IPADDR`
- `BLACKLISTED_AFFILIATE_IPADDR`
- `BLACKLISTED_SUBNET`
- `BLACKLISTED_NETBLOCK`
- `MALICIOUS_IPADDR`
- `MALICIOUS_AFFILIATE_IPADDR`
- `MALICIOUS_NETBLOCK`
- `MALICIOUS_SUBNET`

## Flags and categories

- **Flags:** —
- **Categories:** Reputation Systems
- **Use cases:** Investigate, Passive

## Module options

- `cacheperiod` — Hours to cache list data before re-fetching.
- `checkaffiliates` — Apply checks to affiliate IP addresses?
- `checknetblocks` — Report if any malicious IPs are found within owned netblocks?
- `checksubnets` — Check if any malicious IPs are found within the same subnet of the target?

## Test seeds

- `IP_ADDRESS`: input=`8.8.8.8` validation=smoke status=FINISHED; verdict=clean_miss

## Catalogue notes

CleanTalk is a Cloud-Based spam filtering service that allows you to protect your website from spam. CleanTalk provides spam protection that invisible to visitors without using captcha or other methods when visitors have to prove that they are real people.
CleanTalk provides cloud anti-spam solutions for CMS and we developed plugins for the most of popular CMS: WordPress anti-spam plugin, Joomla anti-spam plugin, Drupal and etc. With our simple cloud spam checker, you can be sure your website is protected from spam bots, spam comments, and users.
