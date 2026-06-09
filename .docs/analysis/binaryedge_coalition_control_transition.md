# BinaryEdge → Coalition Control transition

**Status (interim):** `sfp_binaryedge` marked `service_state: error` (upstream shutdown).  
**Supersedes:** legacy `api.binaryedge.io` + `binaryedge_api_key` (X-Key header).

## Shutdown

- BinaryEdge standalone shut down **31 Mar 2025 23:59 GMT** ([Transition FAQ](https://help.coalitioninc.com/hc/en-us/articles/34383910057371-BinaryEdge-Transition-FAQ)).
- Replacement product: **Coalition Control** — free business signup at [coalitioninc.com/control](https://www.coalitioninc.com/control).

## Coalition Control API (free account)

| Topic | Detail |
|-------|--------|
| Base URL | `https://api.control.coalitioninc.com` |
| OpenAPI docs | [api.control.coalitioninc.com/docs/api](https://api.control.coalitioninc.com/docs/api) |
| Auth | **Not a static API key.** `POST /auth/login` with `username` + `password` → **Bearer token** for subsequent requests. |
| MFA | Must be **disabled** on the API user account ([QuickStart](https://help.coalitioninc.com/hc/en-us/articles/43715669577627-Coalition-Control-API-Basics-and-QuickStart)). |
| Entity scope | ASM data is keyed by `entity_id` from `GET /asm/me`. |
| ASM endpoints (examples) | `findings`, `dataleaks`, `ip_addresses`, `assets/impacted` under `/asm/entity/{entity_id}/…` |
| Free tier | Coalition Control **platform** is free for cyber-health / ASM basics for **your registered organization**. Extended scanning / full API entitlement may require paid subscription — confirm against live account + OpenAPI before route design. |

## Architectural gap (SpiderFeet)

Legacy **BinaryEdge** was a **public internet query** API: pass an arbitrary IP, domain, or email and receive scan/leak/CVE/torrent/passive-DNS results.

**Coalition Control ASM** is **organization attack-surface monitoring**: API responses describe assets and findings for the **authenticated customer entity**, not arbitrary third-party OSINT targets.

Re-engineering must decide per consumed nugget:

1. **Map** Coalition findings to existing produced nuggets where semantics align.
2. **Drop or quarantine** routes that have no Coalition equivalent (e.g. co-hosted passive DNS on arbitrary IPs, torrent historical on arbitrary IPs).
3. **Change module role** from “external lookup” to “sync org ASM into scan context” if product intent shifts — bind in SPEC-002 / `SPEC_GAP`.

## Legacy module routes (`modules/sfp_binaryedge.py`)

| Query type | Legacy endpoint | Produced nuggets (summary) |
|------------|-----------------|----------------------------|
| `email` | `dataleaks/email/{email}` | `EMAILADDR_COMPROMISED` |
| `passive` | `domains/ip/{ip}` | `INTERNET_NAME`, `DOMAIN_NAME`, `CO_HOSTED_SITE` |
| `subs` | `domains/subdomain/{domain}` | `INTERNET_NAME` |
| `torrent` | `torrent/historical/{ip}` | `MALICIOUS_IPADDR` |
| `vuln` | `cve/ip/{ip}` | CVE severity nuggets |
| `ip` | `ip/{ip}` | `TCP_PORT_OPEN`, banners, UDP |

## Coalition ASM mapping (draft — spike issue validates)

| Legacy route | Coalition candidate | Confidence |
|--------------|---------------------|------------|
| Email leaks | `/asm/entity/{id}/dataleaks` | Medium — org-scoped leaks, not arbitrary email lookup |
| CVE / vulns | `/asm/entity/{id}/findings` | Medium — finding types need taxonomy mapping |
| Ports / banners | findings + `ip_addresses` | Low — confirm field shapes vs legacy `events` JSON |
| Subdomains | entity asset inventory | Low — not subdomain enumeration of arbitrary domains |
| Passive DNS / co-host | — | **No direct equivalent** |
| Torrent | — | **No direct equivalent** |

## SpiderFeet interim handling

- `UPSTREAM_ERROR_MODULE_IDS` includes `sfp_binaryedge`.
- Sync: `.seed/scripts/sync_service_state.py --write [--typedb]`
- Hidden from **Tests** and **Subscriptions**; still on **Maps** with error filter.
- GitHub: epic + sub-issues for module, catalogue/map, subscriptions auth, tests (see issues linked from #474).

## References

- [BinaryEdge Transition FAQ](https://help.coalitioninc.com/hc/en-us/articles/34383910057371-BinaryEdge-Transition-FAQ)
- [Coalition Control API QuickStart](https://help.coalitioninc.com/hc/en-us/articles/43715669577627-Coalition-Control-API-Basics-and-QuickStart)
- Module issue: GitHub `brettforbes/spiderFeet` #474
