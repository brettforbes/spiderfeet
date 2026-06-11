# Tool - DNSTwist

**Module ID:** `sfp_tool_dnstwist`

## Summary

Identify bit-squatting, typo and other similar domains to the target using a local DNSTwist installation.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `cli` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `free_auth (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_tool_dnstwist
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_tool_dnstwist

## CLI / tool

- **Tool:** DNSTwist
- **Website:** https://github.com/elceef/dnstwist
- **Repository:** https://github.com/elceef/dnstwist

## Routes

- **Route seed nugget:** `DOMAIN_NAME`
- **Consumed:**
- `DOMAIN_NAME`
- **Produced:**
- `SIMILARDOMAIN`

## Flags and categories

- **Flags:** tool
- **Categories:** DNS
- **Use cases:** Footprint, Investigate

## Module options

- `dnstwistpath` — Path to the where the dnstwist.py file lives. Optional.
- `pythonpath` — Path to Python interpreter to use for DNSTwist. If just 'python' then it must be in your PATH.
- `skipwildcards` — Skip TLDs and sub-TLDs that have wildcard DNS.

## Test seeds

- `DOMAIN_NAME`: input=`example.com` validation=smoke status=UNKNOWN; verdict=hit; produced=106

## Catalogue notes

Identify bit-squatting, typo and other similar domains to the target using a local DNSTwist installation.

**Module ID:** `sfp_tool_dnstwist`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** DOMAIN_NAME
**Produces:** SIMILARDOMAIN
**Flags:** tool

**Tool requirement:**
Install dnstwist (`dnstwist` on PATH).

**Smoke battery:**
- Classification: `tool_missing_or_blocked`
- Seed nugget: `DOMAIN_NAME`
- Input: `example.com`
- Produced count: 0
