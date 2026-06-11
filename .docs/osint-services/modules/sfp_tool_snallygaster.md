# Tool - snallygaster

**Module ID:** `sfp_tool_snallygaster`

## Summary

Finds file leaks and other security problems on HTTP servers.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_snallygaster
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_snallygaster

## CLI / tool

- **Tool:** snallygaster
- **Website:** https://github.com/hannob/snallygaster
- **Repository:** https://github.com/hannob/snallygaster

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `VULNERABILITY_GENERAL`
- `VULNERABILITY_CVE_CRITICAL`
- `VULNERABILITY_CVE_HIGH`
- `VULNERABILITY_CVE_MEDIUM`
- `VULNERABILITY_CVE_LOW`

## Flags and categories

- **Flags:** tool
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `snallygaster_path` — Path to your snallygaster binary. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke smoke

## Catalogue notes

Finds file leaks and other security problems on HTTP servers.

**Module ID:** `sfp_tool_snallygaster`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME
**Produces:** VULNERABILITY_GENERAL, VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW
**Flags:** tool

**Tool requirement:**
Install snallygaster (`snallygaster` on PATH).

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
