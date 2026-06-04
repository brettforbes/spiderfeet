# Quarantined Spiderfeet Modules

Modules listed here **do not** declare an external `dataSource` in their metadata, but they are **not** generic non-OSINT infrastructure. Each implements specialised scan behaviour (DNS, crawling, content extraction, local tools, etc.) that still needs to be checked: whether it works, and exactly how it works in this codebase.

Do **not** treat these as validated non-OSINT modules. They were moved here from an earlier classification that incorrectly grouped all `dataSource`-less modules together. Only [`sfp__stor_db` and `sfp__stor_stdout`](non_osint_modules.md) are confirmed generic modules.

**Total: 54 modules** pending review.

---

## Module Categories (provisional)

| Category | Count | Role |
|----------|------:|------|
| DNS & Domain Intelligence | 10 | Resolve, brute-force, and register domain data |
| Web Crawling & Scanning | 6 | Fetch targets, crawl sites, active probes |
| Content Analysis & Extraction | 21 | Parse text and headers for entities |
| Social & Identity | 2 | Find accounts and social profiles |
| Reputation | 1 | Match findings against user-supplied feeds |
| Public Registries | 1 | Query open registries (PGP keyservers) |
| External Tool Wrappers | 13 | Invoke installed CLI security tools |

---

## All Quarantined Modules

| Module | Name | Category | Use Cases | Flags |
|--------|------|----------|-----------|-------|
| `sfp_dnsbrute` | DNS Brute-forcer | DNS & Domain Intelligence | Footprint, Investigate | — |
| `sfp_dnscommonsrv` | DNS Common SRV | DNS & Domain Intelligence | Footprint, Investigate | `slow` |
| `sfp_dnsneighbor` | DNS Look-aside | DNS & Domain Intelligence | Footprint, Investigate | — |
| `sfp_dnsraw` | DNS Raw Records | DNS & Domain Intelligence | Footprint, Investigate, Passive | — |
| `sfp_dnsresolve` | DNS Resolver | DNS & Domain Intelligence | Footprint, Investigate, Passive | — |
| `sfp_dnszonexfer` | DNS Zone Transfer | DNS & Domain Intelligence | Footprint, Investigate | — |
| `sfp_similar` | Similar Domain Finder | DNS & Domain Intelligence | Footprint, Investigate | — |
| `sfp_subdomain_takeover` | Subdomain Takeover Checker | DNS & Domain Intelligence | Footprint, Investigate | — |
| `sfp_tldsearch` | TLD Searcher | DNS & Domain Intelligence | Footprint | `slow` |
| `sfp_whois` | Whois | DNS & Domain Intelligence | Footprint, Investigate, Passive | — |
| `sfp_crossref` | Cross-Referencer | Web Crawling & Scanning | Footprint | — |
| `sfp_intfiles` | Interesting File Finder | Web Crawling & Scanning | Footprint, Passive | — |
| `sfp_junkfiles` | Junk File Finder | Web Crawling & Scanning | Footprint | `slow`, `errorprone`, `invasive` |
| `sfp_portscan_tcp` | Port Scanner - TCP | Web Crawling & Scanning | Footprint, Investigate | `slow`, `invasive` |
| `sfp_spider` | Web Spider | Web Crawling & Scanning | Footprint, Investigate | `slow` |
| `sfp_sslcert` | SSL Certificate Analyzer | Web Crawling & Scanning | Footprint, Investigate | — |
| `sfp_base64` | Base64 Decoder | Content Analysis & Extraction | Investigate, Passive | — |
| `sfp_binstring` | Binary String Extractor | Content Analysis & Extraction | Footprint | `errorprone` |
| `sfp_bitcoin` | Bitcoin Finder | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_company` | Company Name Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_cookie` | Cookie Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_countryname` | Country Name Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_creditcard` | Credit Card Number Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | `errorprone` |
| `sfp_email` | E-Mail Address Extractor | Content Analysis & Extraction | Passive, Investigate, Footprint | — |
| `sfp_errors` | Error String Extractor | Content Analysis & Extraction | Footprint, Passive | — |
| `sfp_ethereum` | Ethereum Address Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_filemeta` | File Metadata Extractor | Content Analysis & Extraction | Footprint | — |
| `sfp_hashes` | Hash Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_hosting` | Hosting Provider Identifier | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_iban` | IBAN Number Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | `errorprone` |
| `sfp_names` | Human Name Extractor | Content Analysis & Extraction | Footprint, Passive | `errorprone` |
| `sfp_pageinfo` | Page Information | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_phone` | Phone Number Extractor | Content Analysis & Extraction | Passive, Footprint, Investigate | — |
| `sfp_strangeheaders` | Strange Header Identifier | Content Analysis & Extraction | Footprint, Passive | — |
| `sfp_webanalytics` | Web Analytics Extractor | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_webframework` | Web Framework Identifier | Content Analysis & Extraction | Footprint, Passive | — |
| `sfp_webserver` | Web Server Identifier | Content Analysis & Extraction | Footprint, Investigate, Passive | — |
| `sfp_accounts` | Account Finder | Social & Identity | Footprint, Passive | — |
| `sfp_social` | Social Network Identifier | Social & Identity | Footprint, Passive | — |
| `sfp_customfeed` | Custom Threat Feed | Reputation | Investigate, Passive | — |
| `sfp_pgp` | PGP Key Servers | Public Registries | Footprint, Investigate, Passive | — |
| `sfp_tool_cmseek` | Tool - CMSeeK | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_dnstwist` | Tool - DNSTwist | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_nbtscan` | Tool - nbtscan | External Tool Wrappers | Footprint, Investigate | `tool`, `slow` |
| `sfp_tool_nmap` | Tool - Nmap | External Tool Wrappers | Footprint, Investigate | `tool`, `slow`, `invasive` |
| `sfp_tool_nuclei` | Tool - Nuclei | External Tool Wrappers | Footprint, Investigate | `tool`, `slow`, `invasive` |
| `sfp_tool_onesixtyone` | Tool - onesixtyone | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_retirejs` | Tool - Retire.js | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_snallygaster` | Tool - snallygaster | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_testsslsh` | Tool - testssl.sh | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_trufflehog` | Tool - TruffleHog | External Tool Wrappers | Footprint, Investigate | `tool`, `slow` |
| `sfp_tool_wafw00f` | Tool - WAFW00F | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_wappalyzer` | Tool - Wappalyzer | External Tool Wrappers | Footprint, Investigate | `tool` |
| `sfp_tool_whatweb` | Tool - WhatWeb | External Tool Wrappers | Footprint, Investigate | `tool` |

---

## Module Reference

Detailed notes for each quarantined module, grouped by provisional role. Functionality has not yet been validated.

### DNS & Domain Intelligence

#### `sfp_dnsbrute` — DNS Brute-forcer

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate  
**Flags:** —

**Summary:** Attempts to identify hostnames through brute-forcing common names and iterations.

**Listens for:** —

**Produces:** `INTERNET_NAME`

**How it works:** Generates candidate hostnames from built-in and configured wordlists against the scan target domain, performs DNS lookups, and emits resolved names as `INTERNET_NAME`. Runs against the target directly rather than waiting for upstream events.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_dnscommonsrv` — DNS Common SRV

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate  
**Flags:** `slow`

**Summary:** Attempts to identify hostnames through brute-forcing common DNS SRV records.

**Listens for:** `INTERNET_NAME`, `DOMAIN_NAME`

**Produces:** `INTERNET_NAME`, `AFFILIATE_INTERNET_NAME`

**How it works:** Brute-forces common DNS SRV record names (e.g. `_sip._tcp`, `_xmpp-server._tcp`) under known domains and hostnames to discover service endpoints.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_dnsneighbor` — DNS Look-aside

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate  
**Flags:** —

**Summary:** Attempt to reverse-resolve the IP addresses next to your target to see if they are related.

**Listens for:** `IP_ADDRESS`

**Produces:** `AFFILIATE_IPADDR`, `IP_ADDRESS`

**How it works:** For each target IP, reverse-resolves adjacent addresses in the same /24 (or configured range) to find co-located hosts that may belong to the same organisation.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_dnsraw` — DNS Raw Records

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Retrieves raw DNS records such as MX, TXT and others.

**Listens for:** `INTERNET_NAME`, `DOMAIN_NAME`, `DOMAIN_NAME_PARENT`

**Produces:** `PROVIDER_MAIL`, `PROVIDER_DNS`, `RAW_DNS_RECORDS`, `DNS_TEXT`, `DNS_SPF`, `INTERNET_NAME`, `INTERNET_NAME_UNRESOLVED`, `AFFILIATE_INTERNET_NAME`, … (+1 more)

**How it works:** Issues direct DNS queries for MX, NS, TXT, SPF, and related record types against known hostnames and domains, producing structured `DNS_*` events plus raw record blobs.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_dnsresolve` — DNS Resolver

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Resolves hosts and IP addresses identified, also extracted from raw content.

**Listens for:** `CO_HOSTED_SITE`, `AFFILIATE_INTERNET_NAME`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, `IP_ADDRESS`, `IPV6_ADDRESS`, `INTERNET_NAME`, `AFFILIATE_IPADDR`, … (+17 more)

**Produces:** `IP_ADDRESS`, `INTERNET_NAME`, `AFFILIATE_INTERNET_NAME`, `AFFILIATE_IPADDR`, `AFFILIATE_IPV6_ADDRESS`, `DOMAIN_NAME`, `IPV6_ADDRESS`, `INTERNAL_IP_ADDRESS`, … (+4 more)

**How it works:** Central DNS resolution hub: forward- and reverse-resolves hostnames and IPs found across virtually all upstream content (web pages, WHOIS, certificates, banners, leak data). Enriches the graph with `IP_ADDRESS`, `INTERNET_NAME`, `DOMAIN_NAME`, and affiliate variants.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_dnszonexfer` — DNS Zone Transfer

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate  
**Flags:** —

**Summary:** Attempts to perform a full DNS zone transfer.

**Listens for:** `PROVIDER_DNS`

**Produces:** `RAW_DNS_RECORDS`, `INTERNET_NAME`

**How it works:** Attempts AXFR zone transfers against nameservers identified as `PROVIDER_DNS`. Successful transfers dump the full zone as `RAW_DNS_RECORDS` and individual hostnames.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_similar` — Similar Domain Finder

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate  
**Flags:** —

**Summary:** Search various sources to identify similar looking domain names, for instance squatted domains.

**Listens for:** `DOMAIN_NAME`

**Produces:** `SIMILARDOMAIN`

**How it works:** Generates typo, homoglyph, and permutation variants of the target domain locally, resolves them via DNS, and emits registered lookalikes as `SIMILARDOMAIN` for squatting analysis.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_subdomain_takeover` — Subdomain Takeover Checker

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** —

**Summary:** Check if affiliated subdomains are vulnerable to takeover.

**Listens for:** `AFFILIATE_INTERNET_NAME`, `AFFILIATE_INTERNET_NAME_UNRESOLVED`

**Produces:** `AFFILIATE_INTERNET_NAME_HIJACKABLE`

**How it works:** Tests unresolved affiliate hostnames for dangling CNAME records pointing to deprovisioned third-party services (GitHub Pages, S3, Heroku, etc.) that could be claimed by an attacker.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tldsearch` — TLD Searcher

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint  
**Flags:** `slow`

**Summary:** Search all Internet TLDs for domains with the same name as the target (this can be very slow.)

**Listens for:** `INTERNET_NAME`

**Produces:** `SIMILARDOMAIN`

**How it works:** Strips the TLD from a hostname and attempts DNS resolution of the same label under every ICANN TLD. Extremely thorough but very slow; surfaces international domain variants.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_whois` — Whois

**Category:** DNS & Domain Intelligence  
**Spiderfeet categories:** Public Registries  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Perform a WHOIS look-up on domain names and owned netblocks.

**Listens for:** `DOMAIN_NAME`, `DOMAIN_NAME_PARENT`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, `CO_HOSTED_SITE_DOMAIN`, `AFFILIATE_DOMAIN_NAME`, `SIMILARDOMAIN`

**Produces:** `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `DOMAIN_REGISTRAR`, `CO_HOSTED_SITE_DOMAIN_WHOIS`, `AFFILIATE_DOMAIN_WHOIS`, `SIMILARDOMAIN_WHOIS`

**How it works:** Performs WHOIS/RDAP lookups on target domains, parent domains, netblocks, co-hosted domains, affiliate domains, and similar domains—emitting raw WHOIS text for downstream extractors.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

### Web Crawling & Scanning

#### `sfp_crossref` — Cross-Referencer

**Category:** Web Crawling & Scanning  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint  
**Flags:** —

**Summary:** Identify whether other domains are associated ('Affiliates') of the target by looking for links back to the target site(s).

**Listens for:** `LINKED_URL_EXTERNAL`, `SIMILARDOMAIN`, `CO_HOSTED_SITE`, `DARKNET_MENTION_URL`

**Produces:** `AFFILIATE_INTERNET_NAME`, `AFFILIATE_WEB_CONTENT`

**How it works:** Fetches external URLs, similar domains, co-hosted sites, and darknet mentions, then checks whether page content links back to the target domain. Reciprocal links indicate an affiliate relationship and produce `AFFILIATE_INTERNET_NAME` / `AFFILIATE_WEB_CONTENT`.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_intfiles` — Interesting File Finder

**Category:** Web Crawling & Scanning  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Passive  
**Flags:** —

**Summary:** Identifies potential files of interest, e.g. office documents, zip files.

**Listens for:** `LINKED_URL_INTERNAL`

**Produces:** `INTERESTING_FILE`

**How it works:** Flags internal linked URLs whose extensions or paths suggest downloadable documents (PDF, Office, archives) as `INTERESTING_FILE` for metadata or content analysis.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_junkfiles` — Junk File Finder

**Category:** Web Crawling & Scanning  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint  
**Flags:** `slow`, `errorprone`, `invasive`

**Summary:** Looks for old/temporary and other similar files.

**Listens for:** `LINKED_URL_INTERNAL`

**Produces:** `JUNK_FILE`

**How it works:** Probes common backup, temporary, and editor-artifact paths (`index.bak`, `.git`, `~`, etc.) on internal URLs. Invasive and slow; may generate false positives on hardened sites.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_portscan_tcp` — Port Scanner - TCP

**Category:** Web Crawling & Scanning  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `slow`, `invasive`

**Summary:** Scans for commonly open TCP ports on Internet-facing systems.

**Listens for:** `IP_ADDRESS`, `NETBLOCK_OWNER`

**Produces:** `TCP_PORT_OPEN`, `TCP_PORT_OPEN_BANNER`

**How it works:** Connects to a configurable list of common TCP ports on target IPs and netblocks, recording open ports and banner text. Directly contacts the target (`invasive`).

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_spider` — Web Spider

**Category:** Web Crawling & Scanning  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `slow`

**Summary:** Spidering of web-pages to extract content for searching.

**Listens for:** `LINKED_URL_INTERNAL`, `INTERNET_NAME`

**Produces:** `WEBSERVER_HTTPHEADERS`, `HTTP_CODE`, `LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL`, `TARGET_WEB_CONTENT`, `TARGET_WEB_CONTENT_TYPE`

**How it works:** Breadth-first crawler starting from target hostnames and internal links. Fetches pages (respecting optional robots.txt), extracts links, HTTP headers, status codes, and page bodies—feeding the entire content-analysis pipeline.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_sslcert` — SSL Certificate Analyzer

**Category:** Web Crawling & Scanning  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** —

**Summary:** Gather information about SSL certificates used by the target's HTTPS sites.

**Listens for:** `INTERNET_NAME`, `LINKED_URL_INTERNAL`, `IP_ADDRESS`

**Produces:** `TCP_PORT_OPEN`, `INTERNET_NAME`, `INTERNET_NAME_UNRESOLVED`, `CO_HOSTED_SITE`, `CO_HOSTED_SITE_DOMAIN`, `SSL_CERTIFICATE_ISSUED`, `SSL_CERTIFICATE_ISSUER`, `SSL_CERTIFICATE_MISMATCH`, … (+4 more)

**How it works:** Opens TLS connections to target hosts, retrieves certificate chains, checks expiry and hostname mismatch, and identifies co-hosted sites via certificate SAN entries.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

### Content Analysis & Extraction

#### `sfp_base64` — Base64 Decoder

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Investigate, Passive  
**Flags:** —

**Summary:** Identify Base64-encoded strings in URLs, often revealing interesting hidden information.

**Listens for:** `LINKED_URL_INTERNAL`

**Produces:** `BASE64_DATA`

**How it works:** Scans internal linked URLs for Base64-encoded path segments or parameters, decodes them, and emits the decoded content as `BASE64_DATA` for downstream extractors.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_binstring` — Binary String Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint  
**Flags:** `errorprone`

**Summary:** Attempt to identify strings in binary content.

**Listens for:** `LINKED_URL_INTERNAL`

**Produces:** `RAW_FILE_META_DATA`

**How it works:** When binary file types are fetched via internal links, extracts printable ASCII strings and stores them as `RAW_FILE_META_DATA` for further pattern matching.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_bitcoin` — Bitcoin Finder

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Identify bitcoin addresses in scraped webpages.

**Listens for:** `TARGET_WEB_CONTENT`

**Produces:** `BITCOIN_ADDRESS`

**How it works:** Regex-matches Bitcoin address patterns in scraped web page content and emits `BITCOIN_ADDRESS` entities.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_company` — Company Name Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Identify company names in any obtained data.

**Listens for:** `TARGET_WEB_CONTENT`, `SSL_CERTIFICATE_ISSUED`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `AFFILIATE_DOMAIN_WHOIS`, `AFFILIATE_WEB_CONTENT`

**Produces:** `COMPANY_NAME`, `AFFILIATE_COMPANY_NAME`

**How it works:** Uses heuristics and pattern matching across web content, WHOIS records, and SSL certificate fields to identify organisation/company names tied to the target or affiliates.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_cookie` — Cookie Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Extract Cookies from HTTP headers.

**Listens for:** `WEBSERVER_HTTPHEADERS`

**Produces:** `TARGET_WEB_COOKIE`

**How it works:** Parses `Set-Cookie` and related headers from `WEBSERVER_HTTPHEADERS` events and emits individual `TARGET_WEB_COOKIE` records.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_countryname` — Country Name Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Identify country names in any obtained data.

**Listens for:** `IBAN_NUMBER`, `PHONE_NUMBER`, `AFFILIATE_DOMAIN_NAME`, `CO_HOSTED_SITE_DOMAIN`, `DOMAIN_NAME`, `SIMILARDOMAIN`, `AFFILIATE_DOMAIN_WHOIS`, `CO_HOSTED_SITE_DOMAIN_WHOIS`, … (+3 more)

**Produces:** `COUNTRY_NAME`

**How it works:** Normalises geographic hints from IBANs, phone numbers, WHOIS, geo data, and addresses into canonical `COUNTRY_NAME` entities.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_creditcard` — Credit Card Number Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** `errorprone`

**Summary:** Identify Credit Card Numbers in any data

**Listens for:** `DARKNET_MENTION_CONTENT`, `LEAKSITE_CONTENT`

**Produces:** `CREDIT_CARD_NUMBER`

**How it works:** Searches darknet and leak-site content for credit-card-like number sequences (with Luhn validation where applicable). Marked `errorprone` because numeric false positives are common.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_email` — E-Mail Address Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Passive, Investigate, Footprint  
**Flags:** —

**Summary:** Identify e-mail addresses in any obtained data.

**Listens for:** `TARGET_WEB_CONTENT`, `BASE64_DATA`, `AFFILIATE_DOMAIN_WHOIS`, `CO_HOSTED_SITE_DOMAIN_WHOIS`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `LEAKSITE_CONTENT`, `RAW_DNS_RECORDS`, … (+8 more)

**Produces:** `EMAILADDR`, `EMAILADDR_GENERIC`, `AFFILIATE_EMAILADDR`

**How it works:** Regex-extracts email addresses from web content, WHOIS, DNS TXT, certificates, banners, leak dumps, and other text-bearing events. Classifies generic vs. personal mailboxes.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_errors` — Error String Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Passive  
**Flags:** —

**Summary:** Identify common error messages in content like SQL errors, etc.

**Listens for:** `TARGET_WEB_CONTENT`

**Produces:** `ERROR_MESSAGE`

**How it works:** Pattern-matches common application and database error strings (SQL syntax errors, stack traces, etc.) in fetched web content to flag misconfiguration or information disclosure.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_ethereum` — Ethereum Address Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Identify ethereum addresses in scraped webpages.

**Listens for:** `TARGET_WEB_CONTENT`

**Produces:** `ETHEREUM_ADDRESS`

**How it works:** Regex-matches Ethereum `0x` address patterns in scraped web pages and emits `ETHEREUM_ADDRESS` entities.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_filemeta` — File Metadata Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint  
**Flags:** —

**Summary:** Extracts meta data from documents and images.

**Listens for:** `LINKED_URL_INTERNAL`, `INTERESTING_FILE`

**Produces:** `RAW_FILE_META_DATA`, `SOFTWARE_USED`

**How it works:** Downloads interesting linked files and uses metadata libraries to extract author, software, EXIF, and other embedded properties into `RAW_FILE_META_DATA` and `SOFTWARE_USED`.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_hashes` — Hash Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Identify MD5 and SHA hashes in web content, files and more.

**Listens for:** `TARGET_WEB_CONTENT`, `BASE64_DATA`, `LEAKSITE_CONTENT`, `RAW_DNS_RECORDS`, `RAW_FILE_META_DATA`

**Produces:** `HASH`

**How it works:** Identifies MD5, SHA-1, SHA-256, and other hash formats in text content from web pages, leaks, DNS records, and file metadata.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_hosting` — Hosting Provider Identifier

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Find out if any IP addresses identified fall within known 3rd party hosting ranges, e.g. Amazon, Azure, etc.

**Listens for:** `IP_ADDRESS`

**Produces:** `PROVIDER_HOSTING`

**How it works:** Compares resolved IP addresses against known cloud and hosting provider netblock lists (AWS, Azure, GCP, etc.) to tag `PROVIDER_HOSTING`.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_iban` — IBAN Number Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** `errorprone`

**Summary:** Identify International Bank Account Numbers (IBANs) in any data.

**Listens for:** `TARGET_WEB_CONTENT`, `DARKNET_MENTION_CONTENT`, `LEAKSITE_CONTENT`

**Produces:** `IBAN_NUMBER`

**How it works:** Extracts International Bank Account Numbers from web and leak content with format validation.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_names` — Human Name Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Passive  
**Flags:** `errorprone`

**Summary:** Attempt to identify human names in fetched content.

**Listens for:** `TARGET_WEB_CONTENT`, `EMAILADDR`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `RAW_RIR_DATA`, `RAW_FILE_META_DATA`

**Produces:** `HUMAN_NAME`

**How it works:** Uses name wordlists and NLP-style heuristics to pull probable human names from web content, WHOIS, and document metadata. Marked `errorprone` due to ambiguous capitalised tokens.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_pageinfo` — Page Information

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Obtain information about web pages (do they take passwords, do they contain forms, etc.)

**Listens for:** `TARGET_WEB_CONTENT`

**Produces:** `URL_STATIC`, `URL_JAVASCRIPT`, `URL_FORM`, `URL_PASSWORD`, `URL_UPLOAD`, `URL_JAVA_APPLET`, `URL_FLASH`, `PROVIDER_JAVASCRIPT`

**How it works:** Analyses HTML structure of target pages to detect forms, password fields, file uploads, JavaScript usage, Flash, Java applets, and static vs. dynamic content—emitting URL descriptor events used heavily by reporting and risk scoring.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_phone` — Phone Number Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Passive, Footprint, Investigate  
**Flags:** —

**Summary:** Identify phone numbers in scraped webpages.

**Listens for:** `TARGET_WEB_CONTENT`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `PHONE_NUMBER`

**Produces:** `PHONE_NUMBER`, `PROVIDER_TELCO`

**How it works:** Extracts phone numbers from web content and WHOIS using international format heuristics; may infer telecom provider metadata.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_strangeheaders` — Strange Header Identifier

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Passive  
**Flags:** —

**Summary:** Obtain non-standard HTTP headers returned by web servers.

**Listens for:** `WEBSERVER_HTTPHEADERS`

**Produces:** `WEBSERVER_STRANGEHEADER`

**How it works:** Compares HTTP response headers against a catalogue of standard headers; non-standard or unusual names/values are emitted as `WEBSERVER_STRANGEHEADER`.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_webanalytics` — Web Analytics Extractor

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Identify web analytics IDs in scraped webpages and DNS TXT records.

**Listens for:** `TARGET_WEB_CONTENT`, `DNS_TEXT`

**Produces:** `WEB_ANALYTICS_ID`

**How it works:** Regex-extracts Google Analytics, Matomo, and similar tracking IDs from page HTML and DNS TXT records.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_webframework` — Web Framework Identifier

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Passive  
**Flags:** —

**Summary:** Identify the usage of popular web frameworks like jQuery, YUI and others.

**Listens for:** `TARGET_WEB_CONTENT`

**Produces:** `URL_WEB_FRAMEWORK`

**How it works:** Detects references to known JavaScript/CSS web frameworks (jQuery, YUI, Bootstrap, etc.) in page source.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_webserver` — Web Server Identifier

**Category:** Content Analysis & Extraction  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Obtain web server banners to identify versions of web servers being used.

**Listens for:** `WEBSERVER_HTTPHEADERS`

**Produces:** `WEBSERVER_BANNER`, `WEBSERVER_TECHNOLOGY`, `LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL`

**How it works:** Parses the `Server` header and related fields from HTTP responses to identify web server software and version banners.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

### Social & Identity

#### `sfp_accounts` — Account Finder

**Category:** Social & Identity  
**Spiderfeet categories:** Social Media  
**Use cases:** Footprint, Passive  
**Flags:** —

**Summary:** Look for possible associated accounts on over 500 social and other websites such as Instagram, Reddit, etc.

**Listens for:** `EMAILADDR`, `DOMAIN_NAME`, `HUMAN_NAME`, `USERNAME`

**Produces:** `USERNAME`, `ACCOUNT_EXTERNAL_OWNED`, `SIMILAR_ACCOUNT_EXTERNAL`

**How it works:** Downloads the WhatsMyName site list (WebBreacher) and, for each username derived from emails, domains, or human names, probes hundreds of social and web platforms for matching profile URLs. Threaded HTTP checks with optional permutation and name filtering reduce false positives.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_social` — Social Network Identifier

**Category:** Social & Identity  
**Spiderfeet categories:** Social Media  
**Use cases:** Footprint, Passive  
**Flags:** —

**Summary:** Identify presence on social media networks such as LinkedIn, Twitter and others.

**Listens for:** `LINKED_URL_EXTERNAL`

**Produces:** `SOCIAL_MEDIA`, `USERNAME`

**How it works:** Parses external linked URLs for known social-network URL patterns (LinkedIn, Twitter/X, Facebook, etc.) and emits `SOCIAL_MEDIA` plus extracted usernames.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

### Reputation

#### `sfp_customfeed` — Custom Threat Feed

**Category:** Reputation  
**Spiderfeet categories:** Reputation Systems  
**Use cases:** Investigate, Passive  
**Flags:** —

**Summary:** Check if a host/domain, netblock, ASN or IP is malicious according to your custom feed.

**Listens for:** `INTERNET_NAME`, `IP_ADDRESS`, `AFFILIATE_INTERNET_NAME`, `AFFILIATE_IPADDR`, `CO_HOSTED_SITE`

**Produces:** `MALICIOUS_IPADDR`, `MALICIOUS_INTERNET_NAME`, `MALICIOUS_AFFILIATE_IPADDR`, `MALICIOUS_AFFILIATE_INTERNET_NAME`, `MALICIOUS_COHOST`

**How it works:** Downloads a user-supplied plain-text feed (one indicator per line: IP, netblock, ASN, or hostname) and matches discovered target entities against it, emitting malicious descriptor events when hits are found.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

### Public Registries

#### `sfp_pgp` — PGP Key Servers

**Category:** Public Registries  
**Spiderfeet categories:** Public Registries  
**Use cases:** Footprint, Investigate, Passive  
**Flags:** —

**Summary:** Look up domains and e-mail addresses in PGP public key servers.

**Listens for:** `INTERNET_NAME`, `EMAILADDR`, `DOMAIN_NAME`

**Produces:** `EMAILADDR`, `EMAILADDR_GENERIC`, `AFFILIATE_EMAILADDR`, `PGP_KEY`

**How it works:** Queries public PGP keyserver pools (SKS/HKP) for keys matching target domains and email addresses, returning key material and any additional email identities found.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

### External Tool Wrappers

#### `sfp_tool_cmseek` — Tool - CMSeeK

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Identify what Content Management System (CMS) might be used.

**Listens for:** `INTERNET_NAME`

**Produces:** `WEBSERVER_TECHNOLOGY`

**Tool:** [CMSeeK](https://github.com/Tuhinshubhra/CMSeeK)

**How it works:** Wraps the external **CMSeeK** CLI tool. When triggered by `INTERNET_NAME` events, executes the tool against the target, parses stdout/stderr, and maps findings to `WEBSERVER_TECHNOLOGY` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_dnstwist` — Tool - DNSTwist

**Category:** External Tool Wrappers  
**Spiderfeet categories:** DNS  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Identify bit-squatting, typo and other similar domains to the target using a local DNSTwist installation.

**Listens for:** `DOMAIN_NAME`

**Produces:** `SIMILARDOMAIN`

**Tool:** [DNSTwist](https://github.com/elceef/dnstwist)

**How it works:** Wraps the external **DNSTwist** CLI tool. When triggered by `DOMAIN_NAME` events, executes the tool against the target, parses stdout/stderr, and maps findings to `SIMILARDOMAIN` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_nbtscan` — Tool - nbtscan

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`, `slow`

**Summary:** Scans for open NETBIOS nameservers on your target's network.

**Listens for:** `IP_ADDRESS`, `NETBLOCK_OWNER`

**Produces:** `UDP_PORT_OPEN`, `UDP_PORT_OPEN_INFO`, `IP_ADDRESS`

**Tool:** [nbtscan](http://www.unixwiz.net/tools/nbtscan.html)

**How it works:** Wraps the external **nbtscan** CLI tool. When triggered by `IP_ADDRESS`, `NETBLOCK_OWNER` events, executes the tool against the target, parses stdout/stderr, and maps findings to `UDP_PORT_OPEN`, `UDP_PORT_OPEN_INFO`, `IP_ADDRESS` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_nmap` — Tool - Nmap

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`, `slow`, `invasive`

**Summary:** Identify what Operating System might be used.

**Listens for:** `IP_ADDRESS`, `NETBLOCK_OWNER`

**Produces:** `OPERATING_SYSTEM`, `IP_ADDRESS`

**Tool:** [Nmap](https://nmap.org/)

**How it works:** Wraps the external **Nmap** CLI tool. When triggered by `IP_ADDRESS`, `NETBLOCK_OWNER` events, executes the tool against the target, parses stdout/stderr, and maps findings to `OPERATING_SYSTEM`, `IP_ADDRESS` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_nuclei` — Tool - Nuclei

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`, `slow`, `invasive`

**Summary:** Fast and customisable vulnerability scanner.

**Listens for:** `INTERNET_NAME`, `IP_ADDRESS`, `NETBLOCK_OWNER`

**Produces:** `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`, `IP_ADDRESS`, `VULNERABILITY_GENERAL`, `WEBSERVER_TECHNOLOGY`

**Tool:** [Nuclei](https://nuclei.projectdiscovery.io/)

**How it works:** Wraps the external **Nuclei** CLI tool. When triggered by `INTERNET_NAME`, `IP_ADDRESS`, `NETBLOCK_OWNER` events, executes the tool against the target, parses stdout/stderr, and maps findings to `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`, … (+3 more) events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_onesixtyone` — Tool - onesixtyone

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Fast scanner to find publicly exposed SNMP services.

**Listens for:** `IP_ADDRESS`, `NETBLOCK_OWNER`

**Produces:** `UDP_PORT_OPEN_INFO`, `UDP_PORT_OPEN`, `IP_ADDRESS`

**Tool:** [onesixtyone](https://github.com/trailofbits/onesixtyone)

**How it works:** Wraps the external **onesixtyone** CLI tool. When triggered by `IP_ADDRESS`, `NETBLOCK_OWNER` events, executes the tool against the target, parses stdout/stderr, and maps findings to `UDP_PORT_OPEN_INFO`, `UDP_PORT_OPEN`, `IP_ADDRESS` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_retirejs` — Tool - Retire.js

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Scanner detecting the use of JavaScript libraries with known vulnerabilities

**Listens for:** `LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL`

**Produces:** `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`, `VULNERABILITY_GENERAL`

**Tool:** [Retire.js](http://retirejs.github.io/retire.js/)

**How it works:** Wraps the external **Retire.js** CLI tool. When triggered by `LINKED_URL_INTERNAL`, `LINKED_URL_EXTERNAL` events, executes the tool against the target, parses stdout/stderr, and maps findings to `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`, … (+1 more) events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_snallygaster` — Tool - snallygaster

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Finds file leaks and other security problems on HTTP servers.

**Listens for:** `INTERNET_NAME`

**Produces:** `VULNERABILITY_GENERAL`, `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`

**Tool:** [snallygaster](https://github.com/hannob/snallygaster)

**How it works:** Wraps the external **snallygaster** CLI tool. When triggered by `INTERNET_NAME` events, executes the tool against the target, parses stdout/stderr, and maps findings to `VULNERABILITY_GENERAL`, `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, … (+1 more) events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_testsslsh` — Tool - testssl.sh

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Identify various TLS/SSL weaknesses, including Heartbleed, CRIME and ROBOT.

**Listens for:** `INTERNET_NAME`, `IP_ADDRESS`, `NETBLOCK_OWNER`

**Produces:** `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`, `VULNERABILITY_GENERAL`, `IP_ADDRESS`

**Tool:** [testssl.sh](https://testssl.sh)

**How it works:** Wraps the external **testssl.sh** CLI tool. When triggered by `INTERNET_NAME`, `IP_ADDRESS`, `NETBLOCK_OWNER` events, executes the tool against the target, parses stdout/stderr, and maps findings to `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`, … (+2 more) events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_trufflehog` — Tool - TruffleHog

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`, `slow`

**Summary:** Searches through git repositories for high entropy strings and secrets, digging deep into commit history.

**Listens for:** `SOCIAL_MEDIA`, `PUBLIC_CODE_REPO`

**Produces:** `PASSWORD_COMPROMISED`

**Tool:** [TruffleHog](https://github.com/trufflesecurity/truffleHog)

**How it works:** Wraps the external **TruffleHog** CLI tool. When triggered by `SOCIAL_MEDIA`, `PUBLIC_CODE_REPO` events, executes the tool against the target, parses stdout/stderr, and maps findings to `PASSWORD_COMPROMISED` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_wafw00f` — Tool - WAFW00F

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Crawling and Scanning  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Identify what web application firewall (WAF) is in use on the specified website.

**Listens for:** `INTERNET_NAME`

**Produces:** `RAW_RIR_DATA`, `WEBSERVER_TECHNOLOGY`

**Tool:** [WAFW00F](https://github.com/EnableSecurity/wafw00f)

**How it works:** Wraps the external **WAFW00F** CLI tool. When triggered by `INTERNET_NAME` events, executes the tool against the target, parses stdout/stderr, and maps findings to `RAW_RIR_DATA`, `WEBSERVER_TECHNOLOGY` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_wappalyzer` — Tool - Wappalyzer

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Wappalyzer indentifies technologies on websites.

**Listens for:** `INTERNET_NAME`

**Produces:** `OPERATING_SYSTEM`, `SOFTWARE_USED`, `WEBSERVER_TECHNOLOGY`

**Tool:** [Wappalyzer](https://www.wappalyzer.com/)

**How it works:** Wraps the external **Wappalyzer** CLI tool. When triggered by `INTERNET_NAME` events, executes the tool against the target, parses stdout/stderr, and maps findings to `OPERATING_SYSTEM`, `SOFTWARE_USED`, `WEBSERVER_TECHNOLOGY` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

#### `sfp_tool_whatweb` — Tool - WhatWeb

**Category:** External Tool Wrappers  
**Spiderfeet categories:** Content Analysis  
**Use cases:** Footprint, Investigate  
**Flags:** `tool`

**Summary:** Identify what software is in use on the specified website.

**Listens for:** `INTERNET_NAME`

**Produces:** `RAW_RIR_DATA`, `WEBSERVER_BANNER`, `WEBSERVER_TECHNOLOGY`

**Tool:** [WhatWeb](https://github.com/urbanadventurer/whatweb)

**How it works:** Wraps the external **WhatWeb** CLI tool. When triggered by `INTERNET_NAME` events, executes the tool against the target, parses stdout/stderr, and maps findings to `RAW_RIR_DATA`, `WEBSERVER_BANNER`, `WEBSERVER_TECHNOLOGY` events. Requires the tool binary to be installed and available on the host running Spiderfeet.

**Status:** Quarantined — module behaviour and reliability still to be verified.

**When to use:** Do not enable by default. Review and test before adding to a scan profile.

---

*Generated from Spiderfeet module metadata. Quarantined = no `dataSource` in module `meta`, specialised behaviour pending verification. Total: 54 modules.*
