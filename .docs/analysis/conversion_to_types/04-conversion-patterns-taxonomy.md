# Conversion patterns taxonomy

Static classification of **231** modules (`pattern_index.md`). Every module uses one dominant pattern; many combine sub-patterns inside `handleEvent`.

## Pattern overview

| Pattern | Modules | Share |
|---------|---------|-------|
| `api_json_map` | 112 | 48% |
| `api_text_or_html` | 56 | 24% |
| `dns_network_local` | 19 | 8% |
| `custom_logic` | 17 | 7% |
| `cli_subprocess_parse` | 13 | 6% |
| `regex_local` | 11 | 5% |
| `content_extract` | 3 | 1% |

---

## 1. `api_json_map` (112 modules)

**Flow:** `fetchUrl` → `json.loads` → field walk → multiple `SpiderFeetEvent`.

**Representative:** `sfp_shodan`, `sfp_censys`, `sfp_securitytrails`, `sfp_binaryedge`

**Typical mapping logic:**

```python
rec = json.loads(res["content"])
evt = SpiderFeetEvent("RAW_RIR_DATA", str(rec), self.__name__, pevent)
self.notifyListeners(evt)
if rec.get("os"):
    self.notifyListeners(SpiderFeetEvent("OPERATING_SYSTEM", f"{rec['os']} ({addr})", ...))
for row in rec.get("data", []):
    self.notifyListeners(SpiderFeetEvent("TCP_PORT_OPEN", f"{addr}:{row['port']}", ...))
```

**Characteristics:**

- Vendor-specific JSON paths duplicated per module
- Often emits `RAW_*` plus derived ENTITY/DESCRIPTOR types
- Netblock expansion: `IPNetwork` → per-IP `IP_ADDRESS` parent events

**Generalisation potential:** **High** — OpenAPI/JSONPath mappings per vendor.

---

## 2. `api_text_or_html` (56 modules)

**Flow:** HTTP → HTML, CSV, or plain text → regex / line split.

**Representative:** `sfp_dnsdumpster` (HTML tables), `sfp_archiveorg`, blocklist feeds, `sfp_whois`

**Characteristics:**

- Fragile when site layout changes
- Sometimes no `json.loads` at all
- May scrape rather than use official API

**Generalisation potential:** **Medium** — CSS selectors / table adapters; still site-specific.

---

## 3. `cli_subprocess_parse` (13 modules)

**Flow:** `Popen([tool, …])` → decode stdout → line/regex/JSON parse.

| Module | Output format | Produced types (examples) |
|--------|---------------|---------------------------|
| `sfp_tool_nmap` | Text (`OS details:` lines) | `OPERATING_SYSTEM`, `IP_ADDRESS` |
| `sfp_tool_nuclei` | JSON-lines | `VULNERABILITY_*`, `IP_ADDRESS`, `WEBSERVER_TECHNOLOGY` |
| `sfp_tool_testsslsh` | Text sections | `SSL_CERTIFICATE_*`, vulnerabilities |
| `sfp_tool_whatweb` | JSON (plugin) | `WEBSERVER_TECHNOLOGY`, `SOFTWARE_USED` |
| `sfp_tool_nbtscan` | Text table | `UDP_PORT_OPEN`, `UDP_PORT_OPEN_INFO` |
| `sfp_tool_dnstwist` | CSV/stdout | `SIMILARDOMAIN`, `INTERNET_NAME` |
| `sfp_tool_trufflehog` | JSON | secrets → `EMAILADDR`, `API_KEY` patterns |

**Characteristics:**

- **Highest priority for future scanning expansion**
- Each tool is a one-off parser; exit codes and locale affect stdout
- Often omits structured port/service objects (flattened to strings)

**Generalisation potential:** **High** — CLI adapter spec + optional grammars (see roadmap).

Deep dives: [examples/sfp_tool_nmap.md](examples/sfp_tool_nmap.md), [examples/sfp_tool_nuclei.md](examples/sfp_tool_nuclei.md)

---

## 4. `dns_network_local` (19 modules)

**Flow:** DNS queries, cert inspection, socket probes — no third-party OSINT API.

**Representative:** `sfp_dnsresolve`, `sfp_sslcert`, `sfp_portscan_tcp`, `sfp_whois`

**Example (`sfp_portscan_tcp`):** socket connect → if open, `TCP_PORT_OPEN` with `ip:port`; banner → `TCP_PORT_OPEN_BANNER`.

**Generalisation potential:** **Medium** — shared network result model; scan primitives library.

---

## 5. `content_extract` (3 modules)

**Flow:** Consume `TARGET_WEB_CONTENT` / URLs → helpers extract entities.

**Representative:** `sfp_email`, `sfp_spider`, `sfp_pageinfo`

**Generalisation potential:** **High** — pipeline of extractors on normalised DOM/text.

---

## 6. `regex_local` (11 modules)

**Flow:** Pure transformation of `event.data` without new HTTP.

**Representative:** `sfp_base64`, `sfp_binstring`, `sfp_cookie`, `sfp_company`

---

## 7. `custom_logic` (17 modules)

Mixed orchestration not caught by heuristics — often multi-phase or unusual inputs.

---

## Cross-cutting behaviours

### Netblock fan-out

Modules watching `NETBLOCK_OWNER` expand CIDRs via `IPNetwork`, emit per-IP events, then attach findings to **IP-scoped** `pevent` — critical for provenance.

### Duplicate suppression

`self.results[eventData] = True` or hash keys — prevents re-query, not semantic dedup of types.

### Error state

`errorState = True` stops further processing after fatal config/API errors.

### Dynamic type selection

```python
etype, text = self.sf.cveInfo(cve)
SpiderFeetEvent(etype, text, ...)
```

Severity → `VULNERABILITY_CVE_LOW|MEDIUM|HIGH|CRITICAL`.

---

## Per-module reference

Every module: [`modules/sfp_<name>.md`](modules/) — declared produces/consumes, static signals, pattern class.
