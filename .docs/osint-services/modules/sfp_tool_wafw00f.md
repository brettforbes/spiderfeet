# Tool - WAFW00F

**Module ID:** `sfp_tool_wafw00f`

## Summary

Identify what web application firewall (WAF) is in use on the specified website.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_wafw00f
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_wafw00f

## CLI / tool

- **Tool:** WAFW00F
- **Website:** https://github.com/EnableSecurity/wafw00f
- **Repository:** https://github.com/EnableSecurity/wafw00f

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `WEBSERVER_TECHNOLOGY`

## Flags and categories

- **Flags:** tool
- **Categories:** Crawling and Scanning
- **Use cases:** Footprint, Investigate

## Module options

- `python_path` — Path to Python 3 interpreter to use for wafw00f. If just 'python3' then it must be in your $PATH.
- `wafw00f_path` — Path to the wafw00f executable file. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=3

## Catalogue notes

Identify what web application firewall (WAF) is in use on the specified website.

**Module ID:** `sfp_tool_wafw00f`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME
**Produces:** RAW_RIR_DATA, WEBSERVER_TECHNOLOGY
**Flags:** tool

**Tool requirement:**
Install wafw00f (`wafw00f` on PATH).

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
