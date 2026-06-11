# Tool - TruffleHog

**Module ID:** `sfp_tool_trufflehog`

## Summary

Searches through git repositories for high entropy strings and secrets, digging deep into commit history.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_trufflehog
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_trufflehog

## CLI / tool

- **Tool:** TruffleHog
- **Website:** https://github.com/trufflesecurity/truffleHog
- **Repository:** https://github.com/trufflesecurity/truffleHog

## Routes

- **Route seed nugget:** `SOCIAL_MEDIA`
- **Consumed:**
- `SOCIAL_MEDIA`
- `PUBLIC_CODE_REPO`
- **Produced:**
- `PASSWORD_COMPROMISED`

## Flags and categories

- **Flags:** tool, slow
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `allrepos` — Search all code repositories found. By default TruffleHog only searches those linked from the target website.
- `entropy` — Enable entropy checks? If disabled, TruffleHog will solely rely on high-signal regular expressions to identify secrets.
- `trufflehog_path` — Path to your trufflehog binary. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`github.com` validation=blocked-tool blocked-tool
- `SOCIAL_MEDIA`: input=`GitHub: https://github.com/octocat/Hello-World` validation=smoke smoke

## Catalogue notes

Searches through git repositories for high entropy strings and secrets, digging deep into commit history.

**Module ID:** `sfp_tool_trufflehog`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** SOCIAL_MEDIA, PUBLIC_CODE_REPO
**Produces:** PASSWORD_COMPROMISED
**Flags:** tool, slow

**Tool requirement:**
Install TruffleHog v3+ (`trufflehog` on PATH).

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `github.com`
- Produced count: 0
