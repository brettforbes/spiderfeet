# Shared parsing primitives

Modules convert data using **local code** plus shared libraries. These primitives are the main lever for generalisation.

## `sflib.py` (`self.sf` on plugins)

| Method | Used for | Conversion impact |
|--------|----------|-------------------|
| `fetchUrl(url, …)` | HTTP GET/POST | Gateway to API JSON/HTML; returns `{code, content}` |
| `validIP` / `validIP6` / `validIpNetwork` | Validation | Gate before emit; choose `IP_ADDRESS` vs reject |
| `validHost` / `isDomain` / `hostDomain` | Hostname logic | Split FQDN vs subdomain; affiliate detection |
| `resolveHost` / `resolveIP` | DNS | `INTERNET_NAME` ↔ `IP_ADDRESS` in local modules |
| `urlFQDN` | URL parsing | Normalise crawl targets |
| `parseCert` | TLS certificates | `SSL_CERTIFICATE_*` family from PEM/DER text |
| `cveInfo(cveId)` | CVE lookup | Maps id → `(VULNERABILITY_CVE_*, description text)` |
| `safeSocket` | TCP connect | Banner reads for `sfp_portscan_tcp` |
| `optValueToData` | Config paths | Load port lists, wordlists from file/URL |

**Pattern:** API modules call `fetchUrl` → `json.loads` → iterate keys → `SpiderFeetEvent` per field.

## `spiderfeet/helpers.py` (`SpiderFeetHelpers`)

| Method | Emits via modules |
|--------|-------------------|
| `extractLinksFromHtml` | `LINKED_URL_*`, spider input |
| `extractEmailsFromText` | `sfp_email` → `EMAILADDR` |
| `extractPhoneNumbers` | `PHONE_NUMBER` |
| `extractHashesFromText` | `HASH` |
| `extractIbansFromText` | `IBAN_NUMBER` |
| `sanitiseInput` | Input validation (CLI modules) |

Content modules (`sfp_spider`, `sfp_pageinfo`, `sfp_email`) chain **fetch → BeautifulSoup/helpers → many event types**.

## Third-party libraries (in-module)

| Library | Typical use |
|---------|-------------|
| `json` | API responses, Nuclei JSON-lines |
| `re` | CVE extraction, Nmap line parse, grep-style |
| `netaddr.IPNetwork` | Expand `NETBLOCK_OWNER` to IPs |
| `BeautifulSoup` | HTML parsing |
| `subprocess.Popen` | CLI tools (`sfp_tool_*`) |
| `phonenumbers` | Normalise phone entities |

## CLI resolution (Stage 4 additions)

`.seed/scripts/` and module helpers resolve binaries (`which`, configured paths, WSL). Conversion still happens in Python after `communicate()`.

## What is *not* shared today

- No central **port parser** (`ip:port` duplicated across Shodan, portscan, Nuclei, …)
- No **JSON schema registry** per API vendor
- No **CLI output adapter** interface (each tool hand-parses stdout)
- No **structured event payload** (typed dict → validated → serialised)
- No unit-test harness for parsers isolated from `handleEvent`

## Primitive usage by pattern

| Pattern | Primary primitives |
|---------|-------------------|
| `api_json_map` | `fetchUrl`, `json.loads`, `cveInfo` |
| `api_text_or_html` | `fetchUrl`, regex, occasional BeautifulSoup |
| `cli_subprocess_parse` | `Popen`, line/regex/JSON-lines |
| `dns_network_local` | `resolveHost`, `resolveIP`, `safeSocket` |
| `content_extract` | helpers + BeautifulSoup |
| `regex_local` | `re` on `event.data` |

See [04-conversion-patterns-taxonomy.md](04-conversion-patterns-taxonomy.md) for module examples.
