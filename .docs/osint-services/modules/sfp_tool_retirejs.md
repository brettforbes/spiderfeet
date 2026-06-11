# Tool - Retire.js

**Module ID:** `sfp_tool_retirejs`

## Summary

Scanner detecting the use of JavaScript libraries with known vulnerabilities

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_retirejs
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_retirejs

## CLI / tool

- **Tool:** Retire.js
- **Website:** http://retirejs.github.io/retire.js/
- **Repository:** https://github.com/RetireJS/retire.js

## Routes

- **Route seed nugget:** `LINKED_URL_INTERNAL`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- `LINKED_URL_EXTERNAL`
- **Produced:**
- `VULNERABILITY_CVE_CRITICAL`
- `VULNERABILITY_CVE_HIGH`
- `VULNERABILITY_CVE_MEDIUM`
- `VULNERABILITY_CVE_LOW`
- `VULNERABILITY_GENERAL`

## Flags and categories

- **Flags:** tool
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate

## Module options

- `retirejs_path` — Path to your retire binary. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=blocked-tool blocked-tool
- `LINKED_URL_INTERNAL`: input=`https://code.jquery.com/jquery-1.2.6.min.js` validation=smoke status=UNKNOWN; verdict=hit; produced=6

## Catalogue notes

Scanner detecting the use of JavaScript libraries with known vulnerabilities

**Module ID:** `sfp_tool_retirejs`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_INTERNAL, LINKED_URL_EXTERNAL
**Produces:** VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW, VULNERABILITY_GENERAL
**Flags:** tool

**Tool requirement:**
Install retire.js CLI.

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
