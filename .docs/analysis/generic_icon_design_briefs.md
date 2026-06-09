# Generic / placeholder OSINT service icon briefs

Generated for **70** services whose Maps icon is the shared `icon_software_used.svg` placeholder or a copied quarantine stub.

Hand each section to a design agent to produce a unique SVG per service.
## Technical specification (all icons)

| Property | Value |
|----------|-------|
| Format | SVG 1.1, standalone file |
| Canvas | `viewBox="0 0 50 50"` (square) |
| Display size | 40×40 px in map icon mode (scale cleanly) |
| Background | Rounded rect `rx="5"`; use service brand colour or category hue |
| Foreground | White or near-white (`#FFFFFF`) strokes/fills for contrast |
| Style | Flat vector, 2–2.5 px stroke at 50×50 scale; no raster embeds |
| File name | As listed per service (`icons/...`) |
| Export path | `spiderfeet-widget/src/assets/icons/<filename>` |
| Accessibility | Recognisable at 24×24; avoid text smaller than 4 px cap height |

---

## sfp_abusix — Abusix Mail Intelligence

- **Output file:** `icons/icon_service_abusix.svg`
- **Category:** Reputation Systems
- **Service origin:** external
- **Access tier:** free_auth

### Narrative / brand story

Abusix Mail Intelligence is an external OSINT integration (https://abusix.org/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check if a netblock or IP address is in the Abusix Mail Intelligence blacklist.

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS, IPV6_ADDRESS, AFFILIATE_IPADDR, AFFILIATE_IPV6_ADDRESS, NETBLOCK_MEMBER, NETBLOCKV6_MEMBER…
- Produced: BLACKLISTED_IPADDR, BLACKLISTED_AFFILIATE_IPADDR, BLACKLISTED_SUBNET, BLACKLISTED_NETBLOCK, BLACKLISTED_INTERNET_NAME, BLACKLISTED_AFFILIATE_INTERNET_NAME…

---

## sfp_accounts — Account Finder

- **Output file:** `icons/icon_service_accounts.svg`
- **Category:** Social Media
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Account Finder runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Look for possible associated accounts on over 500 social and other websites such as Instagram, Reddit, etc.

### Visual direction

- **Metaphor:** connected nodes / profile silhouette
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: EMAILADDR, DOMAIN_NAME, HUMAN_NAME, USERNAME
- Produced: USERNAME, ACCOUNT_EXTERNAL_OWNED, SIMILAR_ACCOUNT_EXTERNAL

---

## sfp_base64 — Base64 Decoder

- **Output file:** `icons/icon_service_base64.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Base64 Decoder runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify Base64-encoded strings in URLs, often revealing interesting hidden information.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_INTERNAL
- Produced: BASE64_DATA

---

## sfp_binstring — Binary String Extractor

- **Output file:** `icons/icon_service_binstring.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Binary String Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Attempt to identify strings in binary content.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_INTERNAL
- Produced: RAW_FILE_META_DATA

---

## sfp_bitcoin — Bitcoin Finder

- **Output file:** `icons/icon_service_bitcoin.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Bitcoin Finder runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify bitcoin addresses in scraped webpages.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT
- Produced: BITCOIN_ADDRESS

---

## sfp_botvrij — botvrij.eu

- **Output file:** `icons/icon_service_botvrij.svg`
- **Category:** Reputation Systems
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

botvrij.eu is an external OSINT integration (https://botvrij.eu/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check if a domain is malicious according to botvrij.eu.

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, AFFILIATE_INTERNET_NAME, CO_HOSTED_SITE
- Produced: BLACKLISTED_INTERNET_NAME, BLACKLISTED_AFFILIATE_INTERNET_NAME, BLACKLISTED_COHOST, MALICIOUS_INTERNET_NAME, MALICIOUS_AFFILIATE_INTERNET_NAME, MALICIOUS_COHOST

---

## sfp_company — Company Name Extractor

- **Output file:** `icons/icon_service_company.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Company Name Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify company names in any obtained data.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT, SSL_CERTIFICATE_ISSUED, DOMAIN_WHOIS, NETBLOCK_WHOIS, AFFILIATE_DOMAIN_WHOIS, AFFILIATE_WEB_CONTENT
- Produced: COMPANY_NAME, AFFILIATE_COMPANY_NAME

---

## sfp_cookie — Cookie Extractor

- **Output file:** `icons/icon_service_cookie.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Cookie Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Extract Cookies from HTTP headers.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: WEBSERVER_HTTPHEADERS
- Produced: TARGET_WEB_COOKIE

---

## sfp_countryname — Country Name Extractor

- **Output file:** `icons/icon_service_countryname.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Country Name Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify country names in any obtained data.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IBAN_NUMBER, PHONE_NUMBER, AFFILIATE_DOMAIN_NAME, CO_HOSTED_SITE_DOMAIN, DOMAIN_NAME, SIMILARDOMAIN…
- Produced: COUNTRY_NAME

---

## sfp_creditcard — Credit Card Number Extractor

- **Output file:** `icons/icon_service_creditcard.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Credit Card Number Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify Credit Card Numbers in any data

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DARKNET_MENTION_CONTENT, LEAKSITE_CONTENT
- Produced: CREDIT_CARD_NUMBER

---

## sfp_crobat_api — Crobat API

- **Output file:** `icons/icon_service_crobat_api.svg`
- **Category:** Passive DNS
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

Crobat API is an external OSINT integration (https://sonar.omnisint.io/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Search Crobat API for subdomains.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #0EA5E9 sky blue
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME
- Produced: RAW_RIR_DATA, INTERNET_NAME, INTERNET_NAME_UNRESOLVED

---

## sfp_crossref — Cross-Referencer

- **Output file:** `icons/icon_service_crossref.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Cross-Referencer runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify whether other domains are associated ('Affiliates') of the target by looking for links back to the target site(s).

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_EXTERNAL, SIMILARDOMAIN, CO_HOSTED_SITE, DARKNET_MENTION_URL
- Produced: AFFILIATE_INTERNET_NAME, AFFILIATE_WEB_CONTENT

---

## sfp_customfeed — Custom Threat Feed

- **Output file:** `icons/icon_service_customfeed.svg`
- **Category:** Reputation Systems
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Custom Threat Feed runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Check if a host/domain, netblock, ASN or IP is malicious according to your custom feed.

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, IP_ADDRESS, AFFILIATE_INTERNET_NAME, AFFILIATE_IPADDR, CO_HOSTED_SITE
- Produced: MALICIOUS_IPADDR, MALICIOUS_INTERNET_NAME, MALICIOUS_AFFILIATE_IPADDR, MALICIOUS_AFFILIATE_INTERNET_NAME, MALICIOUS_COHOST

---

## sfp_dnsbrute — DNS Brute-forcer

- **Output file:** `icons/icon_service_dnsbrute.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

DNS Brute-forcer runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Attempts to identify hostnames through brute-forcing common names and iterations.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME, INTERNET_NAME
- Produced: INTERNET_NAME

---

## sfp_dnscommonsrv — DNS Common SRV

- **Output file:** `icons/icon_service_dnscommonsrv.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

DNS Common SRV runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Attempts to identify hostnames through brute-forcing common DNS SRV records.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, DOMAIN_NAME
- Produced: INTERNET_NAME, AFFILIATE_INTERNET_NAME

---

## sfp_dnsdumpster — DNSDumpster

- **Output file:** `icons/icon_service_dnsdumpster.svg`
- **Category:** Passive DNS
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

DNSDumpster is an external OSINT integration (https://dnsdumpster.com/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Passive subdomain enumeration using HackerTarget's DNSDumpster

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #0EA5E9 sky blue
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME, INTERNET_NAME
- Produced: INTERNET_NAME, INTERNET_NAME_UNRESOLVED

---

## sfp_dnsneighbor — DNS Look-aside

- **Output file:** `icons/icon_service_dnsneighbor.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

DNS Look-aside runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Attempt to reverse-resolve the IP addresses next to your target to see if they are related.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS
- Produced: AFFILIATE_IPADDR, IP_ADDRESS

---

## sfp_dnsraw — DNS Raw Records

- **Output file:** `icons/icon_service_dnsraw.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

DNS Raw Records runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Retrieves raw DNS records such as MX, TXT and others.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, DOMAIN_NAME, DOMAIN_NAME_PARENT
- Produced: PROVIDER_MAIL, PROVIDER_DNS, RAW_DNS_RECORDS, DNS_TEXT, DNS_SPF, INTERNET_NAME…

---

## sfp_dnsresolve — DNS Resolver

- **Output file:** `icons/icon_service_dnsresolve.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

DNS Resolver runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Resolves hosts and IP addresses identified, also extracted from raw content.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: CO_HOSTED_SITE, AFFILIATE_INTERNET_NAME, NETBLOCK_OWNER, NETBLOCKV6_OWNER, IP_ADDRESS, IPV6_ADDRESS…
- Produced: IP_ADDRESS, INTERNET_NAME, AFFILIATE_INTERNET_NAME, AFFILIATE_IPADDR, AFFILIATE_IPV6_ADDRESS, DOMAIN_NAME…

---

## sfp_dnszonexfer — DNS Zone Transfer

- **Output file:** `icons/icon_service_dnszonexfer.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

DNS Zone Transfer runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Attempts to perform a full DNS zone transfer.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: PROVIDER_DNS
- Produced: RAW_DNS_RECORDS, INTERNET_NAME

---

## sfp_email — E-Mail Address Extractor

- **Output file:** `icons/icon_service_email.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

E-Mail Address Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify e-mail addresses in any obtained data.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT, BASE64_DATA, AFFILIATE_DOMAIN_WHOIS, CO_HOSTED_SITE_DOMAIN_WHOIS, DOMAIN_WHOIS, NETBLOCK_WHOIS…
- Produced: EMAILADDR, EMAILADDR_GENERIC, AFFILIATE_EMAILADDR

---

## sfp_errors — Error String Extractor

- **Output file:** `icons/icon_service_errors.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Error String Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify common error messages in content like SQL errors, etc.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT
- Produced: ERROR_MESSAGE

---

## sfp_ethereum — Ethereum Address Extractor

- **Output file:** `icons/icon_service_ethereum.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Ethereum Address Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify ethereum addresses in scraped webpages.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT
- Produced: ETHEREUM_ADDRESS

---

## sfp_filemeta — File Metadata Extractor

- **Output file:** `icons/icon_service_filemeta.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

File Metadata Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Extracts meta data from documents and images.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_INTERNAL, INTERESTING_FILE
- Produced: RAW_FILE_META_DATA, SOFTWARE_USED

---

## sfp_hashes — Hash Extractor

- **Output file:** `icons/icon_service_hashes.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Hash Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify MD5 and SHA hashes in web content, files and more.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT, BASE64_DATA, LEAKSITE_CONTENT, RAW_DNS_RECORDS, RAW_FILE_META_DATA
- Produced: HASH

---

## sfp_hosting — Hosting Provider Identifier

- **Output file:** `icons/icon_service_hosting.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Hosting Provider Identifier runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Find out if any IP addresses identified fall within known 3rd party hosting ranges, e.g. Amazon, Azure, etc.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS
- Produced: PROVIDER_HOSTING

---

## sfp_iban — IBAN Number Extractor

- **Output file:** `icons/icon_service_iban.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

IBAN Number Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify International Bank Account Numbers (IBANs) in any data.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT, DARKNET_MENTION_CONTENT, LEAKSITE_CONTENT
- Produced: IBAN_NUMBER

---

## sfp_intfiles — Interesting File Finder

- **Output file:** `icons/icon_service_intfiles.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Interesting File Finder runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identifies potential files of interest, e.g. office documents, zip files.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_INTERNAL
- Produced: INTERESTING_FILE

---

## sfp_junkfiles — Junk File Finder

- **Output file:** `icons/icon_service_junkfiles.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Junk File Finder runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Looks for old/temporary and other similar files.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_INTERNAL
- Produced: JUNK_FILE

---

## sfp_names — Human Name Extractor

- **Output file:** `icons/icon_service_names.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Human Name Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Attempt to identify human names in fetched content.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT, EMAILADDR, DOMAIN_WHOIS, NETBLOCK_WHOIS, RAW_RIR_DATA, RAW_FILE_META_DATA
- Produced: HUMAN_NAME

---

## sfp_opennic — OpenNIC DNS

- **Output file:** `icons/icon_service_opennic.svg`
- **Category:** DNS
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

OpenNIC DNS is an external OSINT integration (https://www.opennic.org/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Resolves host names in the OpenNIC alternative DNS system.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #0EA5E9 sky blue
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, INTERNET_NAME_UNRESOLVED, AFFILIATE_INTERNET_NAME, AFFILIATE_INTERNET_NAME_UNRESOLVED
- Produced: IP_ADDRESS, IPV6_ADDRESS, AFFILIATE_IPADDR, AFFILIATE_IPV6_ADDRESS

---

## sfp_openphish — OpenPhish

- **Output file:** `icons/icon_service_openphish.svg`
- **Category:** Reputation Systems
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

OpenPhish is an external OSINT integration (https://openphish.com/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check if a host/domain is malicious according to OpenPhish.com.

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, AFFILIATE_INTERNET_NAME, CO_HOSTED_SITE
- Produced: BLACKLISTED_INTERNET_NAME, BLACKLISTED_AFFILIATE_INTERNET_NAME, BLACKLISTED_COHOST, MALICIOUS_INTERNET_NAME, MALICIOUS_AFFILIATE_INTERNET_NAME, MALICIOUS_COHOST

---

## sfp_pageinfo — Page Information

- **Output file:** `icons/icon_service_pageinfo.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Page Information runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Obtain information about web pages (do they take passwords, do they contain forms, etc.)

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT
- Produced: URL_STATIC, URL_JAVASCRIPT, URL_FORM, URL_PASSWORD, URL_UPLOAD, URL_JAVA_APPLET…

---

## sfp_pgp — PGP Key Servers

- **Output file:** `icons/icon_service_pgp.svg`
- **Category:** Public Registries
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

PGP Key Servers runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Look up domains and e-mail addresses in PGP public key servers.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, EMAILADDR, DOMAIN_NAME
- Produced: EMAILADDR, EMAILADDR_GENERIC, AFFILIATE_EMAILADDR, PGP_KEY

---

## sfp_phone — Phone Number Extractor

- **Output file:** `icons/icon_service_phone.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Phone Number Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify phone numbers in scraped webpages.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT, DOMAIN_WHOIS, NETBLOCK_WHOIS, PHONE_NUMBER
- Produced: PHONE_NUMBER, PROVIDER_TELCO

---

## sfp_portscan_tcp — Port Scanner - TCP

- **Output file:** `icons/icon_service_portscan_tcp.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Port Scanner - TCP runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Scans for commonly open TCP ports on Internet-facing systems.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS, NETBLOCK_OWNER
- Produced: TCP_PORT_OPEN, TCP_PORT_OPEN_BANNER

---

## sfp_projectdiscovery — ProjectDiscovery Chaos

- **Output file:** `icons/icon_service_projectdiscovery.svg`
- **Category:** Passive DNS
- **Service origin:** external
- **Access tier:** paid

### Narrative / brand story

ProjectDiscovery Chaos is an external OSINT integration (https://chaos.projectdiscovery.io). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Search for hosts/subdomains using chaos.projectdiscovery.io

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #0EA5E9 sky blue
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME
- Produced: RAW_RIR_DATA, INTERNET_NAME, INTERNET_NAME_UNRESOLVED

---

## sfp_psbdmp — Psbdmp

- **Output file:** `icons/icon_service_psbdmp.svg`
- **Category:** Leaks, Dumps and Breaches
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

Psbdmp is an external OSINT integration (https://psbdmp.cc/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check psbdmp.cc (PasteBin Dump) for potentially hacked e-mails and domains.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: EMAILADDR, DOMAIN_NAME, INTERNET_NAME
- Produced: LEAKSITE_URL, LEAKSITE_CONTENT

---

## sfp_punkspider — PunkSpider

- **Output file:** `icons/icon_service_punkspider.svg`
- **Category:** Leaks, Dumps and Breaches
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

PunkSpider is an external OSINT integration (https://punkspider.io/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check the QOMPLX punkspider.io service to see if the target is listed as vulnerable.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME
- Produced: VULNERABILITY_GENERAL

---

## sfp_searchcode — searchcode

- **Output file:** `icons/icon_service_searchcode.svg`
- **Category:** Search Engines
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

searchcode is an external OSINT integration (https://searchcode.com/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Search searchcode for code repositories mentioning the target domain.

### Visual direction

- **Metaphor:** magnifying glass over data grid
- **Primary colour:** #3B82F6 blue
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME
- Produced: EMAILADDR, EMAILADDR_GENERIC, LINKED_URL_INTERNAL, PUBLIC_CODE_REPO, RAW_RIR_DATA

---

## sfp_similar — Similar Domain Finder

- **Output file:** `icons/icon_service_similar.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Similar Domain Finder runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Search various sources to identify similar looking domain names, for instance squatted domains.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME
- Produced: SIMILARDOMAIN

---

## sfp_social — Social Network Identifier

- **Output file:** `icons/icon_service_social.svg`
- **Category:** Social Media
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Social Network Identifier runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify presence on social media networks such as LinkedIn, Twitter and others.

### Visual direction

- **Metaphor:** connected nodes / profile silhouette
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_EXTERNAL
- Produced: SOCIAL_MEDIA, USERNAME

---

## sfp_spider — Web Spider

- **Output file:** `icons/icon_service_spider.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Web Spider runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Spidering of web-pages to extract content for searching.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_INTERNAL, INTERNET_NAME
- Produced: WEBSERVER_HTTPHEADERS, HTTP_CODE, LINKED_URL_INTERNAL, LINKED_URL_EXTERNAL, TARGET_WEB_CONTENT, TARGET_WEB_CONTENT_TYPE

---

## sfp_sslcert — SSL Certificate Analyzer

- **Output file:** `icons/icon_service_sslcert.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

SSL Certificate Analyzer runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Gather information about SSL certificates used by the target's HTTPS sites.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, LINKED_URL_INTERNAL, IP_ADDRESS
- Produced: TCP_PORT_OPEN, INTERNET_NAME, INTERNET_NAME_UNRESOLVED, CO_HOSTED_SITE, CO_HOSTED_SITE_DOMAIN, SSL_CERTIFICATE_ISSUED…

---

## sfp_stevenblack_hosts — Steven Black Hosts

- **Output file:** `icons/icon_service_stevenblack_hosts.svg`
- **Category:** Reputation Systems
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

Steven Black Hosts is an external OSINT integration (https://github.com/StevenBlack/hosts). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check if a domain is malicious (malware or adware) according to Steven Black Hosts list.

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, AFFILIATE_INTERNET_NAME, CO_HOSTED_SITE
- Produced: BLACKLISTED_INTERNET_NAME, BLACKLISTED_AFFILIATE_INTERNET_NAME, BLACKLISTED_COHOST, MALICIOUS_INTERNET_NAME, MALICIOUS_AFFILIATE_INTERNET_NAME, MALICIOUS_COHOST

---

## sfp_strangeheaders — Strange Header Identifier

- **Output file:** `icons/icon_service_strangeheaders.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Strange Header Identifier runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Obtain non-standard HTTP headers returned by web servers.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: WEBSERVER_HTTPHEADERS
- Produced: WEBSERVER_STRANGEHEADER

---

## sfp_subdomain_takeover — Subdomain Takeover Checker

- **Output file:** `icons/icon_service_subdomain_takeover.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Subdomain Takeover Checker runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Check if affiliated subdomains are vulnerable to takeover.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: AFFILIATE_INTERNET_NAME, AFFILIATE_INTERNET_NAME_UNRESOLVED
- Produced: AFFILIATE_INTERNET_NAME_HIJACKABLE

---

## sfp_sublist3r — Sublist3r PassiveDNS

- **Output file:** `icons/icon_service_sublist3r.svg`
- **Category:** Passive DNS
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

Sublist3r PassiveDNS is an external OSINT integration (https://api.sublist3r.com). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Passive subdomain enumeration using Sublist3r's API

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #0EA5E9 sky blue
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME, INTERNET_NAME
- Produced: INTERNET_NAME, INTERNET_NAME_UNRESOLVED

---

## sfp_surbl — SURBL

- **Output file:** `icons/icon_service_surbl.svg`
- **Category:** Reputation Systems
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

SURBL is an external OSINT integration (http://www.surbl.org/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check if a netblock, IP address or domain is in the SURBL blacklist.

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS, AFFILIATE_IPADDR, NETBLOCK_OWNER, NETBLOCK_MEMBER, INTERNET_NAME, AFFILIATE_INTERNET_NAME…
- Produced: BLACKLISTED_IPADDR, BLACKLISTED_AFFILIATE_IPADDR, BLACKLISTED_SUBNET, BLACKLISTED_NETBLOCK, BLACKLISTED_INTERNET_NAME, BLACKLISTED_AFFILIATE_INTERNET_NAME…

---

## sfp_tldsearch — TLD Searcher

- **Output file:** `icons/icon_service_tldsearch.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

TLD Searcher runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Search all Internet TLDs for domains with the same name as the target (this can be very slow.)

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME
- Produced: SIMILARDOMAIN

---

## sfp_tool_cmseek — Tool - CMSeeK

- **Output file:** `icons/icon_service_tool_cmseek.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - CMSeeK wraps the `cmseek` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Identify what Content Management System (CMS) might be used.

### Visual direction

- **Metaphor:** terminal window with wrench or shield overlay
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME
- Produced: WEBSERVER_TECHNOLOGY

---

## sfp_tool_dnstwist — Tool - DNSTwist

- **Output file:** `icons/icon_service_tool_dnstwist.svg`
- **Category:** DNS
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - DNSTwist wraps the `dnstwist` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Identify bit-squatting, typo and other similar domains to the target using a local DNSTwist installation.

### Visual direction

- **Metaphor:** globe + magnifier on hostname letters, or stylised DNS record stack
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME
- Produced: SIMILARDOMAIN

---

## sfp_tool_nbtscan — Tool - nbtscan

- **Output file:** `icons/icon_service_tool_nbtscan.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - nbtscan wraps the `nbtscan` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Scans for open NETBIOS nameservers on your target's network.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS, NETBLOCK_OWNER
- Produced: UDP_PORT_OPEN, UDP_PORT_OPEN_INFO, IP_ADDRESS

---

## sfp_tool_nmap — Tool - Nmap

- **Output file:** `icons/icon_service_tool_nmap.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - Nmap wraps the `nmap` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Identify what Operating System might be used.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS, NETBLOCK_OWNER
- Produced: OPERATING_SYSTEM, IP_ADDRESS

---

## sfp_tool_nuclei — Tool - Nuclei

- **Output file:** `icons/icon_service_tool_nuclei.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - Nuclei wraps the `nuclei` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Fast and customisable vulnerability scanner.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, IP_ADDRESS, NETBLOCK_OWNER
- Produced: VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW, IP_ADDRESS, VULNERABILITY_GENERAL…

---

## sfp_tool_onesixtyone — Tool - onesixtyone

- **Output file:** `icons/icon_service_tool_onesixtyone.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - onesixtyone wraps the `onesixtyone` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Fast scanner to find publicly exposed SNMP services.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS, NETBLOCK_OWNER
- Produced: UDP_PORT_OPEN_INFO, UDP_PORT_OPEN, IP_ADDRESS

---

## sfp_tool_retirejs — Tool - Retire.js

- **Output file:** `icons/icon_service_tool_retirejs.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - Retire.js wraps the `retirejs` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Scanner detecting the use of JavaScript libraries with known vulnerabilities

### Visual direction

- **Metaphor:** terminal window with wrench or shield overlay
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: LINKED_URL_INTERNAL, LINKED_URL_EXTERNAL
- Produced: VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW, VULNERABILITY_GENERAL

---

## sfp_tool_snallygaster — Tool - snallygaster

- **Output file:** `icons/icon_service_tool_snallygaster.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - snallygaster wraps the `snallygaster` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Finds file leaks and other security problems on HTTP servers.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME
- Produced: VULNERABILITY_GENERAL, VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW

---

## sfp_tool_testsslsh — Tool - testssl.sh

- **Output file:** `icons/icon_service_tool_testsslsh.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - testssl.sh wraps the `testsslsh` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Identify various TLS/SSL weaknesses, including Heartbleed, CRIME and ROBOT.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, IP_ADDRESS, NETBLOCK_OWNER
- Produced: VULNERABILITY_CVE_CRITICAL, VULNERABILITY_CVE_HIGH, VULNERABILITY_CVE_MEDIUM, VULNERABILITY_CVE_LOW, VULNERABILITY_GENERAL, IP_ADDRESS

---

## sfp_tool_trufflehog — Tool - TruffleHog

- **Output file:** `icons/icon_service_tool_trufflehog.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - TruffleHog wraps the `trufflehog` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Searches through git repositories for high entropy strings and secrets, digging deep into commit history.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: SOCIAL_MEDIA, PUBLIC_CODE_REPO
- Produced: PASSWORD_COMPROMISED

---

## sfp_tool_wafw00f — Tool - WAFW00F

- **Output file:** `icons/icon_service_tool_wafw00f.svg`
- **Category:** Crawling and Scanning
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - WAFW00F wraps the `wafw00f` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Identify what web application firewall (WAF) is in use on the specified website.

### Visual direction

- **Metaphor:** spider web or radar sweep
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME
- Produced: RAW_RIR_DATA, WEBSERVER_TECHNOLOGY

---

## sfp_tool_wappalyzer — Tool - Wappalyzer

- **Output file:** `icons/icon_service_tool_wappalyzer.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - Wappalyzer wraps the `wappalyzer` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Wappalyzer indentifies technologies on websites.

### Visual direction

- **Metaphor:** terminal window with wrench or shield overlay
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME
- Produced: OPERATING_SYSTEM, SOFTWARE_USED, WEBSERVER_TECHNOLOGY

---

## sfp_tool_whatweb — Tool - WhatWeb

- **Output file:** `icons/icon_service_tool_whatweb.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Tool - WhatWeb wraps the `whatweb` CLI installed on the operator host. The icon should evoke a terminal/command badge plus the tool's security function. Identify what software is in use on the specified website.

### Visual direction

- **Metaphor:** terminal window with wrench or shield overlay
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME
- Produced: RAW_RIR_DATA, WEBSERVER_BANNER, WEBSERVER_TECHNOLOGY

---

## sfp_torch — TORCH

- **Output file:** `icons/icon_service_torch.svg`
- **Category:** Search Engines
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

TORCH is an external OSINT integration (https://torchsearch.wordpress.com/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Search Tor 'TORCH' search engine for mentions of the target domain.

### Visual direction

- **Metaphor:** magnifying glass over data grid
- **Primary colour:** #3B82F6 blue
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME, HUMAN_NAME, EMAILADDR
- Produced: DARKNET_MENTION_URL, DARKNET_MENTION_CONTENT

---

## sfp_voipbl — VoIP Blacklist (VoIPBL)

- **Output file:** `icons/icon_service_voipbl.svg`
- **Category:** Reputation Systems
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

VoIP Blacklist (VoIPBL) is an external OSINT integration (https://voipbl.org/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check if an IP address or netblock is malicious according to VoIP Blacklist (VoIPBL).

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: IP_ADDRESS, AFFILIATE_IPADDR, NETBLOCK_MEMBER, NETBLOCK_OWNER
- Produced: BLACKLISTED_IPADDR, BLACKLISTED_AFFILIATE_IPADDR, BLACKLISTED_SUBNET, BLACKLISTED_NETBLOCK, MALICIOUS_IPADDR, MALICIOUS_AFFILIATE_IPADDR…

---

## sfp_vxvault — VXVault.net

- **Output file:** `icons/icon_service_vxvault.svg`
- **Category:** Reputation Systems
- **Service origin:** external
- **Access tier:** free_no_auth

### Narrative / brand story

VXVault.net is an external OSINT integration (http://vxvault.net/). Prefer the provider's visual identity where licensing permits; otherwise an abstract metaphor. Check if a domain or IP address is malicious according to VXVault.net.

### Visual direction

- **Metaphor:** shield with feed/list motif
- **Primary colour:** #57534E stone (positive fixture) or provider brand primary
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: INTERNET_NAME, IP_ADDRESS, IPV6_ADDRESS, AFFILIATE_IPADDR, AFFILIATE_IPV6_ADDRESS, AFFILIATE_INTERNET_NAME…
- Produced: MALICIOUS_IPADDR, MALICIOUS_INTERNET_NAME, MALICIOUS_AFFILIATE_IPADDR, MALICIOUS_AFFILIATE_INTERNET_NAME, MALICIOUS_COHOST

---

## sfp_webanalytics — Web Analytics Extractor

- **Output file:** `icons/icon_service_webanalytics.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Web Analytics Extractor runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify web analytics IDs in scraped webpages and DNS TXT records.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT, DNS_TEXT
- Produced: WEB_ANALYTICS_ID

---

## sfp_webframework — Web Framework Identifier

- **Output file:** `icons/icon_service_webframework.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Web Framework Identifier runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Identify the usage of popular web frameworks like jQuery, YUI and others.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: TARGET_WEB_CONTENT
- Produced: URL_WEB_FRAMEWORK

---

## sfp_webserver — Web Server Identifier

- **Output file:** `icons/icon_service_webserver.svg`
- **Category:** Content Analysis
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Web Server Identifier runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Obtain web server banners to identify versions of web servers being used.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: WEBSERVER_HTTPHEADERS
- Produced: WEBSERVER_BANNER, WEBSERVER_TECHNOLOGY, LINKED_URL_INTERNAL, LINKED_URL_EXTERNAL

---

## sfp_whois — Whois

- **Output file:** `icons/icon_service_whois.svg`
- **Category:** Public Registries
- **Service origin:** quarantine
- **Access tier:** free_no_auth

### Narrative / brand story

Whois runs entirely inside SpiderFeet (no external API). Icon should communicate local processing / parsing, not a cloud vendor logo. Perform a WHOIS look-up on domain names and owned netblocks.

### Visual direction

- **Metaphor:** abstract OSINT glyph distinct from the generic orange terminal placeholder
- **Primary colour:** #7C3AED (violet) accent — aligns with quarantine map ring; pair with white glyph
- **Must not:** reuse the orange `#F97316` terminal rectangle from `icon_software_used.svg`
- **Must:** read clearly at 40 px inside a white circular ring on the force graph

### Consumes / produces (context)

- Consumed: DOMAIN_NAME, DOMAIN_NAME_PARENT, NETBLOCK_OWNER, NETBLOCKV6_OWNER, CO_HOSTED_SITE_DOMAIN, AFFILIATE_DOMAIN_NAME…
- Produced: DOMAIN_WHOIS, NETBLOCK_WHOIS, DOMAIN_REGISTRAR, CO_HOSTED_SITE_DOMAIN_WHOIS, AFFILIATE_DOMAIN_WHOIS, SIMILARDOMAIN_WHOIS

---
