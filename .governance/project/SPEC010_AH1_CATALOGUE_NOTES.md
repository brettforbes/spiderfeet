# SPEC-010 AH1 — Catalogue split notes

**Issue:** [#1067](https://github.com/brettforbes/spiderfeet/issues/1067) · **R10-02**

## Changes

| nugget_id | Action |
|-----------|--------|
| `IPV4_ADDRESS` | **Added** to `.docs/analysis/nuggets_extension.json` (ENTITY, colour `#3B82F6`, icon `icon_ip_address.svg`) |
| `IPV6_ADDRESS` | **Already present** in `.docs/analysis/nuggets.json` — reused (no extension duplicate) |
| `IP_ADDRESS` | Retained in `nuggets.json` as keep-legacy v1 event type; emitting code retires it in AH2 |

## Derived `*_IPADDR` decisions (from AH0 inventory)

| Variant | Decision |
|---------|----------|
| `AFFILIATE_IPADDR` | keep-legacy v1 event; affiliate role IPv4 stays this id until a later split |
| `AFFILIATE_IPV6_ADDRESS` | keep |
| `BLACKLISTED_IPADDR` / `BLACKLISTED_AFFILIATE_IPADDR` | keep-legacy v1 |
| `MALICIOUS_IPADDR` / `MALICIOUS_AFFILIATE_IPADDR` | keep-legacy v1 |
| `INTERNAL_IP_ADDRESS` | keep for internal IPv4; optional follow-up `INTERNAL_IPV4_ADDRESS` |

## Verification

```bash
poetry run python -c "import json;ids={n['nugget_id'] for n in json.load(open('.docs/analysis/nuggets_extension.json'))};assert 'IPV4_ADDRESS' in ids; print('IPV4_ADDRESS ok')"
poetry run python -c "import json;ids={n['nugget_id'] for n in json.load(open('.docs/analysis/nuggets.json'))};assert 'IPV6_ADDRESS' in ids; print('IPV6_ADDRESS ok')"
```
