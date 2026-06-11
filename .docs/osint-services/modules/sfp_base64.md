# Base64 Decoder

**Module ID:** `sfp_base64`

## Summary

Identify Base64-encoded strings in URLs, often revealing interesting hidden information.

## Classification

| Field | Value |
|-------|-------|
| service_origin | `local` |
| service_state | `in-test` |
| fixture_category | `positive` |
| subscription_tier | `none (free_no_auth)` |
| test_status (route seed) | `validated-positive` |

## Data source

- **Website:** spiderfeet://local/sfp_base64
- **Model:** `LOCAL_NOAUTH`
- **References:** spiderfeet://local/sfp_base64

## Routes

- **Route seed nugget:** `LINKED_URL_INTERNAL`
- **Consumed:**
- `LINKED_URL_INTERNAL`
- **Produced:**
- `BASE64_DATA`

## Flags and categories

- **Flags:** —
- **Categories:** Content Analysis
- **Use cases:** Investigate, Passive

## Module options

- `minlength` — The minimum length a string that looks like a base64-encoded string needs to be.

## Test seeds

- `LINKED_URL_INTERNAL`: input=`https://example.com/x?d=U3BpZGVyRm9vdA%3d%3d` validation=smoke status=UNKNOWN; verdict=hit; produced=1

## Catalogue notes

Identify Base64-encoded strings in URLs, often revealing interesting hidden information.

**Module ID:** `sfp_base64`
**Origin:** quarantine (local SpiderFeet processing)
**Consumes:** LINKED_URL_INTERNAL
**Produces:** BASE64_DATA

**Smoke battery:**
- Classification: `validated_hit`
- Seed nugget: `LINKED_URL_INTERNAL`
- Input: `https://example.com/x?d=U3BpZGVyRm9vdA%3d%3d`
- Produced count: 1
