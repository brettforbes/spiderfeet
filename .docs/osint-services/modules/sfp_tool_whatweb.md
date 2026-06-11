# Tool - WhatWeb

**Module ID:** `sfp_tool_whatweb`

## Summary

Identify what software is in use on the specified website.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_whatweb
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_whatweb

## CLI / tool

- **Tool:** WhatWeb
- **Website:** https://github.com/urbanadventurer/whatweb
- **Repository:** https://github.com/urbanadventurer/whatweb

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `RAW_RIR_DATA`
- `WEBSERVER_BANNER`
- `WEBSERVER_TECHNOLOGY`

## Flags and categories

- **Flags:** tool
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate

## Module options

- `aggression` — Set WhatWeb aggression level (1-4)
- `ruby_path` — Path to Ruby interpreter to use for WhatWeb. If just 'ruby' then it must be in your $PATH.
- `whatweb_path` — Path to the whatweb executable file. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=7

## Catalogue notes

Identify what software is in use on the specified website.

**Module ID:** `sfp_tool_whatweb`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** INTERNET_NAME
**Produces:** RAW_RIR_DATA, WEBSERVER_BANNER, WEBSERVER_TECHNOLOGY
**Flags:** tool

**Tool requirement:**
Install WhatWeb (`whatweb` on PATH).

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `INTERNET_NAME`
- Input: `example.com`
- Produced count: 0
