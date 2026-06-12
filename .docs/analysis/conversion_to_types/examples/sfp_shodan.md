# Example: API JSON → multiple nugget types (`sfp_shodan`)

**Pattern:** `api_json_map`  
**Source:** `modules/sfp_shodan.py`

## Input

Consumed: `IP_ADDRESS`, `NETBLOCK_OWNER`, `DOMAIN_NAME`, `WEB_ANALYTICS_ID`

## Acquisition

```python
res = self.sf.fetchUrl(f"https://api.shodan.io/shodan/host/{qry}?key=...", ...)
rec = json.loads(res["content"])
```

## Conversion steps

1. **Raw preservation** — entire dict as string:
   - `RAW_RIR_DATA` ← `str(rec)`

2. **Host-level fields** (if present):
   - `OPERATING_SYSTEM` ← `f"{rec['os']} ({addr})"`
   - `DEVICE_TYPE` ← `f"{rec['devtype']} ({addr})"`
   - `GEOINFO` ← `city, country_name` joined

3. **Per-service array** `rec['data'][]`:
   - `TCP_PORT_OPEN` ← `addr + ":" + port`
   - `TCP_PORT_OPEN_BANNER` ← banner string
   - `SOFTWARE_USED` ← product
   - `BGP_AS_MEMBER` ← ASN stripped of `AS` prefix
   - CVE keys in `vulns` → `sf.cveInfo(vuln)` → `VULNERABILITY_CVE_*`

## Netblock handling

For `NETBLOCK_OWNER`, expands CIDR to IPs, emits `IP_ADDRESS` per host, then runs host query with `pevent` = that IP event (provenance chain).

## Generalisation opportunity

Highly structured JSON — ideal **declarative map** candidate (Phase B in roadmap). Same loop pattern appears in Censys, BinaryEdge, Onyphe with different field names.

## Declared vs emitted

`producedEvents()` lists all types above. `SOFTWARE_USED` and `BGP_AS_MEMBER` are emitted in code but easy to miss in catalogue routes — verify `osint_services.json` route completeness.
