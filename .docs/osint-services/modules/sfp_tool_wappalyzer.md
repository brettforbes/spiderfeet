# Tool - Wappalyzer

**Module ID:** `sfp_tool_wappalyzer`

## Summary

Wappalyzer indentifies technologies on websites.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `error` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `upstream-blocked` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_wappalyzer
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_wappalyzer

## CLI / tool

- **Tool:** Wappalyzer
- **Website:** https://www.wappalyzer.com/
- **Repository:** https://github.com/AliasIO/Wappalyzer

## Routes

- **Route seed nugget:** `INTERNET_NAME`
- **Consumed:**
- `INTERNET_NAME`
- **Produced:**
- `OPERATING_SYSTEM`
- `SOFTWARE_USED`
- `WEBSERVER_TECHNOLOGY`

## Flags and categories

- **Flags:** tool
- **Categories:** Content Analysis
- **Use cases:** Footprint, Investigate

## Module options

- `node_path` — Path to your NodeJS binary. Must be set.
- `wappalyzer_path` — Path to your wappalyzer cli.js file. Must be set.

## Test seeds

- `INTERNET_NAME`: input=`example.com` validation=error service_state=error; AliasIO/Wappalyzer OSS CLI and GitHub repo no longer available — module not operator-testable

## Catalogue notes

Wappalyzer indentifies technologies on websites.

**Module ID:** `sfp_tool_wappalyzer`
**Service state:** error — legacy open-source CLI retired; AliasIO/Wappalyzer GitHub repo and npm cli.js no longer available for this wrapper.
**Consumes:** INTERNET_NAME
**Produces:** OPERATING_SYSTEM, SOFTWARE_USED, WEBSERVER_TECHNOLOGY
**Flags:** tool

**Operator note:** Module remains in codebase for compatibility but is not testable or promotable until replaced (e.g. retire module or integrate a supported detection path).
