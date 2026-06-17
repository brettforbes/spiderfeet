# PIUS → SpiderFeet Nugget Mapping

Pius is a **CLI pipeline tool** (not yet a built-in SpiderFeet module in stage 4). This document defines the recommended mapping when ingesting NDJSON into SpiderFeet scans or custom modules.

## Recommended mappings

| PIUS `Type` | SpiderFeet nugget | Value | Notes |
|-------------|-------------------|-------|-------|
| `domain` | `INTERNET_NAME` | `Value` (hostname) | Normalize to lowercase; strip wildcards |
| `cidr` | `NETBLOCK_OWNER` | `Value` (CIDR) | Pair with org from `--org` in event context |

## `INTERNET_NAME` (domains)

### When to emit

- `Type == "domain"`
- `Value` is a valid hostname (not corporate name strings from noisy plugins)
- Optional: skip when `Data.needs_review == true` unless operator accepts review queue

### Value normalization

```python
def to_internet_name(finding: dict) -> str | None:
    if finding.get("Type") != "domain":
        return None
    host = finding.get("Value", "").strip().lower()
    if host.startswith("*."):
        host = host[2:]
    if not host or " " in host:
        return None
    return host
```

### Provenance metadata

Attach to event or edge data:

| Field | Source |
|-------|--------|
| `source_plugin` | `Source` |
| `confidence` | `Data.confidence` |
| `needs_review` | `Data.needs_review` |
| `seed_org` | `--org` CLI argument |

### Examples

| NDJSON line | `INTERNET_NAME` |
|-------------|-----------------|
| `{"Type":"domain","Value":"api.acme.com","Source":"crt-sh"}` | `api.acme.com` |
| `{"Type":"domain","Value":"*.acme.com","Source":"crt-sh"}` | `acme.com` |
| `{"Type":"domain","Value":"Acme Holdings","Source":"gleif","Data":{"needs_review":true}} | Skip or queue for review |

## `NETBLOCK_OWNER` (CIDRs)

### When to emit

- `Type == "cidr"`
- `Value` matches CIDR notation

### Value

Use the CIDR string directly: `203.0.113.0/24`.

SpiderFeet `NETBLOCK_OWNER` represents netblock ownership context. Enrich with:

| Metadata | Source |
|----------|--------|
| Owner org | `--org` argument |
| RIR | infer from `Source` (`arin`, `ripe`, …) |
| Plugin | `Source` field |

```python
def to_netblock_owner(finding: dict, org: str) -> tuple[str, dict] | None:
    if finding.get("Type") != "cidr":
        return None
    cidr = finding.get("Value", "").strip()
    if "/" not in cidr:
        return None
    meta = {"organization": org, "source_plugin": finding.get("Source")}
    return cidr, meta
```

## Graph patterns

```
COMPANY_NAME (seed / manual)
    ├── INTERNET_NAME (from domain findings)
    │       └── WEBSERVER_TECHNOLOGY (from WAFWOOF/CMSeeK downstream)
    └── NETBLOCK_OWNER (from cidr findings)
            └── IP_ADDRESS (from port scan downstream)
```

## Pipeline to other CLI tools

| PIUS output | Next tool | SpiderFeet nugget |
|-------------|-----------|-------------------|
| `domain` | `wafw00f -a -o- -f json` | `WEBSERVER_TECHNOLOGY` |
| `domain` | CMSeeK | `WEBSERVER_TECHNOLOGY` |
| `domain` | Nuclei | `VULNERABILITY_*` / custom |
| `cidr` | Nmap, Nerva | `IP_ADDRESS`, services |

## Confidence gating

| Policy | Rule |
|--------|------|
| Strict in-scope | Emit only `needs_review != true` or `confidence >= 0.65` |
| Inclusive discovery | Emit all; tag low confidence in descriptor metadata |
| SpiderFeet stage 4 | Align with operator fixture policy for clean_miss vs positive |

## Future module

When `sfp_tool_pius` or manifest runner lands:

- **Input:** `COMPANY_NAME` or similar org seed
- **Output:** `INTERNET_NAME`, `NETBLOCK_OWNER`
- **Parser:** NDJSON line reader, not TextFSM
