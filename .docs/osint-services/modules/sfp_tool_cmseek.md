# Tool - CMSeeK

**Module ID:** `sfp_tool_cmseek`

## Summary

Identify what Content Management System (CMS) might be used.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-negative` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_cmseek
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_cmseek

## CLI / tool

- **Tool:** CMSeeK
- **Website:** https://github.com/Tuhinshubhra/CMSeeK
- **Repository:** https://github.com/Tuhinshubhra/CMSeeK

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `WEBSERVER_TECHNOLOGY`

## Flags and categories

- **Flags:** tool
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate

## Module options

- `cmseekpath` — Path to the where the cmseek.py file lives. Must be set.
- `pythonpath` — Path to Python 3 interpreter to use for CMSeeK. If just 'python3' then it must be in your PATH.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke smoke

## Catalogue notes

Identify what Content Management System (CMS) might be used.

**Module ID:** `sfp_tool_cmseek`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME
**Produces:** WEBSERVER_TECHNOLOGY
**Flags:** tool

**Tool requirement:**
Install CMSeeK (`cmseek.py` or `cmsseek` on PATH).

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
