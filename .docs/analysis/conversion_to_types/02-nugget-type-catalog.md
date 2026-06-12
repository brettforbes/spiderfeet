# Nugget type catalog

Canonical source: [`.docs/analysis/nuggets.json`](../nuggets.json) — **172** archetype definitions.

In SpiderFeet code these are **event types** (`eventType` on `SpiderFeetEvent`). In the map UI they are **nuggets**.

## How to read this catalog

| Column | Meaning |
|--------|---------|
| **Purpose & definition** | What this type represents in an investigation, why it exists, and how to interpret it in the event chain. Curated in [`nugget_purposes.json`](../nugget_purposes.json). |
| **Archetype** | `Entity` = identifiable thing; `Descriptor` = state/classification on an entity; `Data` = bulk payload; `Sub-entity` = component of a parent (port, URL, software); `Internal` = scan control |
| **Catalogue (consume / produce)** | Count of **OSINT services** in `osint_services.json` listing this type in `consumed_nuggets` (`C`) or `produced_nuggets` (`P`). One service = one module route declaration (231 services). |
| **Typical `data` encoding** | Conventional string shape in `SpiderFeetEvent.data` (not schema-enforced). |

Within each section, **entities and sub-entities are listed first**, then **descriptors**, **data**, and **states** that annotate the same subject (e.g. `EMAILADDR` then `EMAILADDR_COMPROMISED`).

Regenerate: `poetry run python .seed/scripts/generate_nugget_type_catalog.py`

## Summary statistics

| Metric | Value |
|--------|-------|
| Archetype definitions | 172 |
| Types with ≥1 catalogue produce route | 166 |
| Types with ≥1 catalogue consume route | 68 |
| Types unused in catalogue routes | 6 |

Producer module counts (from `producedEvents()`): [nugget_type_producers.md](nugget_type_producers.md).

## Archetype layers

| `nugget_type` | Count | Graph role (intended) |
|---------------|-------|------------------------|
| `INTERNAL` | 1 | Scan anchor, not OSINT |
| `ENTITY` | 57 | First-class node |
| `SUBENTITY` | 5 | Part of parent entity (port, link, software) |
| `DESCRIPTOR` | 79 | State or classification on entity |
| `DATA` | 30 | Evidence blob / opaque payload |

---

## Scan control

Internal types; not OSINT findings.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `ROOT` | Internal SpiderFeet Root event | Scan anchor only — represents the operator-supplied target (domain, IP, etc.). Not an OSINT finding; starts the event chain. | Internal | `icon_root.svg` | `#8B5CF6` | — | — |

## Accounts & usernames

External accounts and identity handles.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `ACCOUNT_EXTERNAL_OWNED` | Account on External Site | User account on a third-party site (GitHub, social, etc.) tied to the target identity. Used for attribution and credential exposure checks. | Entity | `icon_account_external_owned.svg` | `#3B82F6` | C:0 / P:4 | — |
| `ACCOUNT_EXTERNAL_OWNED_COMPROMISED` | Hacked Account on External Site | Descriptor on an owned external account indicating it appears in breach or compromise corpora. Signals credential risk. | Descriptor | `icon_account_external_owned_compromised.svg` | `#F59E0B` | — | — |
| `ACCOUNT_EXTERNAL_USER_SHARED_COMPROMISED` | Hacked User Account on External Site | Descriptor for a compromised account that shares identifiers with the target user but may not be solely owned by them. | Descriptor | `icon_account_external_user_shared_compromised.svg` | `#F59E0B` | — | — |
| `SIMILAR_ACCOUNT_EXTERNAL` | Similar Account on External Site | Account on an external site that resembles the target's handle or identity — possible impersonation or related persona. | Entity | `icon_similar_account_external.svg` | `#3B82F6` | C:0 / P:1 | — |
| `USERNAME` | Username | Discovered login handle or alias used across services. Feeds account enumeration and social modules. | Entity | `icon_username.svg` | `#3B82F6` | C:7 / P:6 | Handle string |
| `SOCIAL_MEDIA` | Social Media Presence | Presence on a social network (profile URL or platform identity). Expands the target's public persona graph. | Entity | `icon_social_media.svg` | `#3B82F6` | C:5 / P:8 | — |

## Domains & registration

Owned and related domain entities.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `DOMAIN_NAME` | Domain Name | Registrable domain in scope for the investigation (usually the target or a discovered owned domain). Primary anchor for DNS, WHOIS, and cert workflows. | Entity | `icon_domain_name.svg` | `#3B82F6` | C:74 / P:20 | FQDN or registrable domain |
| `DOMAIN_NAME_PARENT` | Domain Name (Parent) | Parent/registrable domain extracted from a deeper hostname (e.g. `app.example.com` → `example.com`). Used for breadth-first footprinting. | Entity | `icon_domain_name_parent.svg` | `#3B82F6` | C:4 / P:1 | — |
| `DOMAIN_REGISTRAR` | Domain Registrar | Registrar organisation for a domain. Supports supply-chain and takeover research. | Entity | `icon_domain_registrar.svg` | `#3B82F6` | C:0 / P:3 | — |
| `DOMAIN_WHOIS` | Domain Whois | Raw or normalised WHOIS payload for a domain. Evidence blob for registration dates, contacts, and nameservers. | Data | `icon_domain_whois.svg` | `#14B8A6` | C:6 / P:2 | — |
| `SIMILARDOMAIN` | Similar Domain | Typosquat or look-alike domain (homoglyph, missing character, etc.). Relevant to phishing and brand abuse. | Entity | `icon_similardomain.svg` | `#3B82F6` | C:3 / P:3 | — |
| `SIMILARDOMAIN_WHOIS` | Similar Domain - Whois | WHOIS data for a similar/typosquat domain — compare registration patterns to the real domain. | Data | `icon_similardomain_whois.svg` | `#14B8A6` | C:2 / P:1 | — |
| `DESCRIPTION_CATEGORY` | Description - Category | High-level categorical label for a site or entity (e.g. industry vertical from a directory). | Descriptor | `icon_description_category.svg` | `#F59E0B` | C:0 / P:1 | — |
| `DESCRIPTION_ABSTRACT` | Description - Abstract | Free-text abstract or bio describing a site, company, or profile. | Descriptor | `icon_description_abstract.svg` | `#F59E0B` | C:0 / P:2 | — |

## Affiliate domains & metadata

Third-party / neighbouring domain assets.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `AFFILIATE_DOMAIN_NAME` | Affiliate - Domain Name | Domain related to the footprint but not owned by the target (neighbour, co-tenant, or linked org). Kept separate from owned `DOMAIN_NAME`. | Entity | `icon_affiliate_domain_name.svg` | `#3B82F6` | C:3 / P:12 | — |
| `AFFILIATE_DOMAIN_UNREGISTERED` | Affiliate - Domain Name Unregistered | Affiliate-style hostname whose domain is unregistered — possible dangling DNS or takeover opportunity. | Entity | `icon_affiliate_domain_unregistered.svg` | `#3B82F6` | C:0 / P:1 | — |
| `AFFILIATE_DOMAIN_WHOIS` | Affiliate - Domain Whois | WHOIS record for an affiliate domain. | Data | `icon_affiliate_domain_whois.svg` | `#14B8A6` | C:4 / P:1 | — |
| `AFFILIATE_COMPANY_NAME` | Affiliate - Company Name | Company name associated with an affiliate domain or site, not the primary target org. | Entity | `icon_affiliate_company_name.svg` | `#3B82F6` | C:0 / P:1 | — |
| `AFFILIATE_DESCRIPTION_CATEGORY` | Affiliate Description - Category | Category label for an affiliate site or organisation. | Descriptor | `icon_affiliate_description_category.svg` | `#F59E0B` | C:0 / P:1 | — |
| `AFFILIATE_DESCRIPTION_ABSTRACT` | Affiliate Description - Abstract | Abstract/description text for an affiliate entity. | Descriptor | `icon_affiliate_description_abstract.svg` | `#F59E0B` | C:0 / P:1 | — |

## Internet names & hostnames

Resolvable names tied to the footprint.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `INTERNET_NAME` | Internet Name | Resolvable hostname (subdomain or FQDN) on the footprint. Drives DNS, HTTP spider, and active scan modules. | Entity | `icon_internet_name.svg` | `#3B82F6` | C:69 / P:41 | Hostname |
| `INTERNET_NAME_UNRESOLVED` | Internet Name - Unresolved | Hostname discovered in content or DNS but which does not resolve at query time — may be stale, internal, or typo. | Entity | `icon_internet_name_unresolved.svg` | `#3B82F6` | C:2 / P:24 | — |
| `AFFILIATE_INTERNET_NAME` | Affiliate - Internet Name | Hostname on an affiliate/co-hosted context, not asserted as target-owned infrastructure. | Entity | `icon_affiliate_internet_name.svg` | `#3B82F6` | C:27 / P:19 | — |
| `AFFILIATE_INTERNET_NAME_UNRESOLVED` | Affiliate - Internet Name - Unresolved | Affiliate hostname that does not resolve when checked. | Entity | `icon_affiliate_internet_name_unresolved.svg` | `#3B82F6` | C:2 / P:5 | — |
| `AFFILIATE_INTERNET_NAME_HIJACKABLE` | Affiliate - Internet Name Hijackable | Affiliate hostname vulnerable to takeover (e.g. dangling CNAME). High-risk finding for adjacent attacks. | Entity | `icon_affiliate_internet_name_hijackable.svg` | `#3B82F6` | C:0 / P:1 | — |

## Co-hosted sites

Shared hosting relationships.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `CO_HOSTED_SITE` | Co-Hosted Site | Site sharing hosting/IP with the target (reverse IP / shared infrastructure). Expands attack surface and third-party risk. | Entity | `icon_co_hosted_site.svg` | `#3B82F6` | C:27 / P:20 | — |
| `CO_HOSTED_SITE_DOMAIN` | Co-Hosted Site - Domain Name | Domain name of a co-hosted site. | Entity | `icon_co_hosted_site_domain.svg` | `#3B82F6` | C:2 / P:4 | — |
| `CO_HOSTED_SITE_DOMAIN_WHOIS` | Co-Hosted Site - Domain Whois | WHOIS for a co-hosted site's domain. | Data | `icon_co_hosted_site_domain_whois.svg` | `#14B8A6` | C:3 / P:1 | — |
| `BLACKLISTED_COHOST` | Blacklisted Co-Hosted Site | Descriptor: co-hosted site is blacklisted. | Descriptor | `icon_blacklisted_cohost.svg` | `#F59E0B` | C:0 / P:17 | — |
| `DEFACED_COHOST` | Defaced Co-Hosted Site | Descriptor: co-hosted site was defaced. | Descriptor | `icon_defaced_cohost.svg` | `#F59E0B` | C:0 / P:1 | — |
| `MALICIOUS_COHOST` | Malicious Co-Hosted Site | Descriptor: co-hosted site flagged malicious. | Descriptor | `icon_malicious_cohost.svg` | `#F59E0B` | C:0 / P:21 | — |

## IP addresses & netblocks

Layer-3 identifiers and allocations.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `IP_ADDRESS` | IP Address | IPv4 address on the footprint. Hub type for port scans, reputation, geolocation, and passive DNS. | Entity | `icon_ip_address.svg` | `#3B82F6` | C:89 / P:26 | IPv4 literal, e.g. `8.8.8.8` |
| `IPV6_ADDRESS` | IPv6 Address | IPv6 address on the footprint. Same routing role as `IP_ADDRESS` for v6-capable modules. | Entity | `icon_ipv6_address.svg` | `#3B82F6` | C:32 / P:8 | IPv6 literal |
| `INTERNAL_IP_ADDRESS` | IP Address - Internal Network | Private RFC1918 or internal-range address found in content (configs, leaks). Indicates internal network exposure. | Entity | `icon_internal_ip_address.svg` | `#3B82F6` | C:0 / P:2 | — |
| `AFFILIATE_IPADDR` | Affiliate - IP Address | IPv4 seen in affiliate/co-hosted context — not labelled as target-owned. | Entity | `icon_affiliate_ipaddr.svg` | `#3B82F6` | C:43 / P:5 | — |
| `AFFILIATE_IPV6_ADDRESS` | Affiliate - IPv6 Address | IPv6 in affiliate context. | Entity | `icon_affiliate_ipv6_address.svg` | `#3B82F6` | C:14 / P:4 | — |
| `NETBLOCK_OWNER` | Netblock Ownership | CIDR netblock owned or allocated to the target organisation. Enables netblock-wide module fan-out (scan each IP). | Entity | `icon_netblock_owner.svg` | `#3B82F6` | C:50 / P:2 | CIDR, e.g. `192.0.2.0/24` |
| `NETBLOCK_MEMBER` | Netblock Membership | CIDR where the target IP is a member but ownership is another party (e.g. ISP allocation). | Entity | `icon_netblock_member.svg` | `#3B82F6` | C:35 / P:4 | — |
| `NETBLOCKV6_OWNER` | Netblock IPv6 Ownership | IPv6 netblock owned by the target. | Entity | `icon_netblockv6_owner.svg` | `#3B82F6` | C:12 / P:1 | — |
| `NETBLOCKV6_MEMBER` | Netblock IPv6 Membership | IPv6 netblock membership without ownership assertion. | Entity | `icon_netblockv6_member.svg` | `#3B82F6` | C:9 / P:3 | — |
| `NETBLOCK_WHOIS` | Netblock Whois | WHOIS/RIR payload for a netblock. | Data | `icon_netblock_whois.svg` | `#14B8A6` | C:5 / P:1 | — |
| `GEOINFO` | Physical Location | Human-readable location (city, region, country) for an IP or entity. Descriptor on address objects. | Descriptor | `icon_geoinfo.svg` | `#F59E0B` | C:1 / P:34 | City, country (comma-separated) |
| `TOR_EXIT_NODE` | TOR Exit Node | Descriptor flagging that an IP is a Tor exit — affects risk interpretation and blocking decisions. | Descriptor | `icon_tor_exit_node.svg` | `#F59E0B` | C:0 / P:4 | — |
| `PROXY_HOST` | Proxy Host | Descriptor indicating the host behaves as an open proxy. | Descriptor | `icon_proxy_host.svg` | `#F59E0B` | C:0 / P:5 | — |
| `VPN_HOST` | VPN Host | Descriptor indicating the host is associated with VPN exit or VPN service infrastructure. | Descriptor | `icon_vpn_host.svg` | `#F59E0B` | C:0 / P:4 | — |

## BGP & providers

ASN and infrastructure provider attribution.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `BGP_AS_OWNER` | BGP AS Ownership | Autonomous System owned or operated by the target org (ASN + context). | Entity | `icon_bgp_as_owner.svg` | `#3B82F6` | C:1 / P:1 | — |
| `BGP_AS_MEMBER` | BGP AS Membership | ASN announcing an IP or netblock the target uses but may not own. | Entity | `icon_bgp_as_member.svg` | `#3B82F6` | C:2 / P:5 | — |
| `MALICIOUS_ASN` | Malicious AS | Descriptor that an ASN appears on threat feeds or reputation sources. | Descriptor | `icon_malicious_asn.svg` | `#F59E0B` | C:0 / P:1 | — |
| `PROVIDER_DNS` | Name Server (DNS NS Records) | Nameserver hostname from NS records — identifies DNS hosting provider. | Entity | `icon_provider_dns.svg` | `#3B82F6` | C:2 / P:6 | — |
| `PROVIDER_MAIL` | Email Gateway (DNS MX Records) | Mail exchanger (MX) host — identifies email delivery infrastructure. | Entity | `icon_provider_mail.svg` | `#3B82F6` | C:0 / P:3 | — |
| `PROVIDER_HOSTING` | Hosting Provider | Hosting provider attribution (datacenter, CDN, cloud) for an IP or site. | Entity | `icon_provider_hosting.svg` | `#3B82F6` | C:0 / P:3 | — |
| `PROVIDER_TELCO` | Telecommunications Provider | Telecommunications/carrier attribution for a number or IP. | Entity | `icon_provider_telco.svg` | `#3B82F6` | C:0 / P:5 | — |
| `PROVIDER_JAVASCRIPT` | Externally Hosted Javascript | Third-party JavaScript host loaded by pages (analytics, widgets, supply chain). | Entity | `icon_provider_javascript.svg` | `#3B82F6` | C:1 / P:1 | — |

## Ports, OS & device fingerprint

Active scan and fingerprint outputs.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `TCP_PORT_OPEN` | Open TCP Port | Sub-entity: TCP port observed open on an IP (`ip:port`). Feeds banner grab and vuln scanners. | Sub-entity | `icon_tcp_port_open.svg` | `#F97316` | C:0 / P:10 | `ip:port` string |
| `TCP_PORT_OPEN_BANNER` | Open TCP Port Banner | Service banner or initial bytes from an open TCP port. Evidence for service identification. | Data | `icon_tcp_port_open_banner.svg` | `#14B8A6` | C:2 / P:5 | Banner text; source event often port |
| `UDP_PORT_OPEN` | Open UDP Port | Sub-entity: UDP port open on an IP. | Sub-entity | `icon_udp_port_open.svg` | `#F97316` | C:0 / P:4 | `ip:port` |
| `UDP_PORT_OPEN_INFO` | Open UDP Port Information | Extra metadata from UDP probe (e.g. NetBIOS name, SNMP string). | Data | `icon_udp_port_open_info.svg` | `#14B8A6` | C:0 / P:3 | — |
| `OPERATING_SYSTEM` | Operating System | OS fingerprint guess (nmap, Shodan, etc.) attached to a host/IP. | Descriptor | `icon_operating_system.svg` | `#F59E0B` | C:0 / P:7 | OS guess text, often with IP in parentheses |
| `DEVICE_TYPE` | Device Type | Device class (router, webcam, etc.) from passive/active fingerprinting. | Descriptor | `icon_device_type.svg` | `#F59E0B` | C:0 / P:2 | — |
| `WEBSERVER_BANNER` | Web Server | HTTP server header or raw server identification string. | Data | `icon_webserver_banner.svg` | `#14B8A6` | C:2 / P:4 | — |
| `WEBSERVER_HTTPHEADERS` | HTTP Headers | Full or partial HTTP response headers as evidence. | Data | `icon_webserver_httpheaders.svg` | `#14B8A6` | C:5 / P:3 | — |
| `WEBSERVER_STRANGEHEADER` | Non-Standard HTTP Header | Unusual or non-standard HTTP header worth reviewing. | Data | `icon_webserver_strangeheader.svg` | `#14B8A6` | C:0 / P:1 | — |
| `WEBSERVER_TECHNOLOGY` | Web Technology | Detected web stack component (server, framework, CMS) as a descriptor. | Descriptor | `icon_webserver_technology.svg` | `#F59E0B` | C:0 / P:11 | — |
| `SOFTWARE_USED` | Software Used | Sub-entity: named product/service running on a host (from Shodan, WhatWeb, nuclei, etc.). | Sub-entity | `icon_software_used.svg` | `#F97316` | C:0 / P:5 | — |

## DNS records

Structured DNS payloads.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `DNS_SPF` | DNS SPF Record | SPF TXT record content — email sender policy for a domain. | Data | `icon_dns_spf.svg` | `#14B8A6` | C:0 / P:1 | — |
| `DNS_SRV` | DNS SRV Record | SRV record — locates services (LDAP, SIP, etc.) for a domain. | Data | `icon_dns_srv.svg` | `#14B8A6` | — | — |
| `DNS_TEXT` | DNS TXT Record | Generic DNS TXT record (verification tokens, policies, etc.). | Data | `icon_dns_text.svg` | `#14B8A6` | C:1 / P:2 | — |
| `RAW_DNS_RECORDS` | Raw DNS Records | Complete DNS answer set preserved for audit and re-parsing. | Data | `icon_raw_dns_records.svg` | `#14B8A6` | C:3 / P:3 | — |

## Web content & analytics

Pages, cookies, and tracking identifiers.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `TARGET_WEB_CONTENT` | Web Content | HTML or text body fetched from a target URL. Feeds extractors (email, phone, links, metadata). | Data | `icon_target_web_content.svg` | `#14B8A6` | C:13 / P:1 | — |
| `TARGET_WEB_CONTENT_TYPE` | Web Content Type | MIME or content-type descriptor for fetched web content. | Descriptor | `icon_target_web_content_type.svg` | `#F59E0B` | C:0 / P:1 | — |
| `TARGET_WEB_COOKIE` | Cookies | HTTP cookie name/value from a target response — session and tracking analysis. | Data | `icon_target_web_cookie.svg` | `#14B8A6` | C:0 / P:1 | — |
| `AFFILIATE_WEB_CONTENT` | Affiliate - Web Content | Page body from an affiliate/co-hosted URL context. | Data | `icon_affiliate_web_content.svg` | `#14B8A6` | C:1 / P:1 | — |
| `SEARCH_ENGINE_WEB_CONTENT` | Search Engine Web Content | Snippet or page content from search-engine results — not direct target fetch. | Data | `icon_search_engine_web_content.svg` | `#14B8A6` | — | — |
| `HTTP_CODE` | HTTP Status Code | HTTP status code observed for a URL (200, 403, etc.). | Data | `icon_http_code.svg` | `#14B8A6` | C:0 / P:1 | — |
| `WEB_ANALYTICS_ID` | Web Analytics | Tracking ID (Google Analytics, AdSense, etc.) — links sites and tenants. | Entity | `icon_web_analytics_id.svg` | `#3B82F6` | C:4 / P:4 | `Network: id` |

## Linked URLs

Internal vs external link graph.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `LINKED_URL_INTERNAL` | Linked URL - Internal | Sub-entity: URL on the same site/domain as the crawl root (spider output). | Sub-entity | `icon_linked_url_internal.svg` | `#F97316` | C:9 / P:13 | — |
| `LINKED_URL_EXTERNAL` | Linked URL - External | Sub-entity: outbound URL leaving the target site — third-party dependencies. | Sub-entity | `icon_linked_url_external.svg` | `#F97316` | C:9 / P:2 | — |
| `URL_ADBLOCKED_INTERNAL` | URL (AdBlocked Internal) | Internal URL that would be blocked by ad blockers (trackers, ads). | Descriptor | `icon_url_adblocked_internal.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_ADBLOCKED_EXTERNAL` | URL (AdBlocked External) | External URL classified as ad/tracker by block lists. | Descriptor | `icon_url_adblocked_external.svg` | `#F59E0B` | C:0 / P:1 | — |

## URL surface types (current)

Page behaviour classification from spider/pageinfo.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `URL_FORM` | URL (Form) | URL hosting an HTML form — input surface for testing. | Descriptor | `icon_url_form.svg` | `#F59E0B` | C:1 / P:1 | — |
| `URL_JAVASCRIPT` | URL (Uses Javascript) | URL serving JavaScript resources. | Descriptor | `icon_url_javascript.svg` | `#F59E0B` | C:1 / P:1 | — |
| `URL_STATIC` | URL (Purely Static) | URL serving mostly static content. | Descriptor | `icon_url_static.svg` | `#F59E0B` | C:1 / P:1 | — |
| `URL_FLASH` | URL (Uses Flash) | URL referencing Flash (legacy attack surface). | Descriptor | `icon_url_flash.svg` | `#F59E0B` | C:1 / P:1 | — |
| `URL_JAVA_APPLET` | URL (Uses Java Applet) | URL with Java applet (legacy). | Descriptor | `icon_url_java_applet.svg` | `#F59E0B` | C:1 / P:1 | — |
| `URL_WEB_FRAMEWORK` | URL (Uses a Web Framework) | URL associated with a detected web framework. | Descriptor | `icon_url_web_framework.svg` | `#F59E0B` | C:1 / P:1 | — |
| `URL_PASSWORD` | URL (Accepts Passwords) | URL that accepts password submission. | Descriptor | `icon_url_password.svg` | `#F59E0B` | C:1 / P:1 | — |
| `URL_UPLOAD` | URL (Accepts Uploads) | URL that accepts file uploads. | Descriptor | `icon_url_upload.svg` | `#F59E0B` | C:1 / P:1 | — |

## URL surface types (historic)

Archive-derived URL classifications.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `URL_FORM_HISTORIC` | Historic URL (Form) | Historic (archived) URL that had a form — Wayback/archive derived. | Descriptor | `icon_url_form_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_JAVASCRIPT_HISTORIC` | Historic URL (Uses Javascript) | Historic URL serving JavaScript. | Descriptor | `icon_url_javascript_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_STATIC_HISTORIC` | Historic URL (Purely Static) | Historic static URL from archive crawl. | Descriptor | `icon_url_static_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_FLASH_HISTORIC` | Historic URL (Uses Flash) | Historic Flash URL. | Descriptor | `icon_url_flash_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_JAVA_APPLET_HISTORIC` | Historic URL (Uses Java Applet) | Historic Java applet URL. | Descriptor | `icon_url_java_applet_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_WEB_FRAMEWORK_HISTORIC` | Historic URL (Uses a Web Framework) | Historic framework-associated URL. | Descriptor | `icon_url_web_framework_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_PASSWORD_HISTORIC` | Historic URL (Accepts Passwords) | Historic password-accepting URL. | Descriptor | `icon_url_password_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `URL_UPLOAD_HISTORIC` | Historic URL (Accepts Uploads) | Historic upload URL. | Descriptor | `icon_url_upload_historic.svg` | `#F59E0B` | C:0 / P:1 | — |

## SSL / TLS certificates

Certificate entities and lifecycle descriptors.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `SSL_CERTIFICATE_ISSUED` | SSL Certificate - Issued to | Certificate subject (issued to) — ties cert to hostname/org. | Entity | `icon_ssl_certificate_issued.svg` | `#3B82F6` | C:3 / P:3 | — |
| `SSL_CERTIFICATE_ISSUER` | SSL Certificate - Issued by | Certificate authority that issued the cert. | Entity | `icon_ssl_certificate_issuer.svg` | `#3B82F6` | C:0 / P:2 | — |
| `SSL_CERTIFICATE_RAW` | SSL Certificate - Raw Data | Full PEM/DER or parsed cert blob for audit. | Data | `icon_ssl_certificate_raw.svg` | `#14B8A6` | C:2 / P:3 | — |
| `SSL_CERTIFICATE_MISMATCH` | SSL Certificate Host Mismatch | Descriptor: cert CN/SAN does not match the hostname — misconfiguration or interception risk. | Descriptor | `icon_ssl_certificate_mismatch.svg` | `#F59E0B` | C:0 / P:2 | — |
| `SSL_CERTIFICATE_EXPIRED` | SSL Certificate Expired | Descriptor: certificate past validity date. | Descriptor | `icon_ssl_certificate_expired.svg` | `#F59E0B` | C:0 / P:2 | — |
| `SSL_CERTIFICATE_EXPIRING` | SSL Certificate Expiring | Descriptor: certificate nearing expiry. | Descriptor | `icon_ssl_certificate_expiring.svg` | `#F59E0B` | C:0 / P:2 | — |

## Email addresses

Mailbox entities and validation/compromise states.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `EMAILADDR` | Email Address | Email address on the footprint (owned or discovered in target content). | Entity | `icon_emailaddr.svg` | `#3B82F6` | C:36 / P:20 | RFC5322-like address |
| `EMAILADDR_GENERIC` | Email Address - Generic | Role-based mailbox (info@, admin@) rather than a named individual. | Entity | `icon_emailaddr_generic.svg` | `#3B82F6` | C:0 / P:16 | — |
| `EMAILADDR_COMPROMISED` | Hacked Email Address | Descriptor: address appears in breach corpora. | Descriptor | `icon_emailaddr_compromised.svg` | `#F59E0B` | C:0 / P:8 | — |
| `EMAILADDR_DELIVERABLE` | Deliverable Email Address | Descriptor: validation API reports mailbox exists. | Descriptor | `icon_emailaddr_deliverable.svg` | `#F59E0B` | C:0 / P:2 | — |
| `EMAILADDR_UNDELIVERABLE` | Undeliverable Email Address | Descriptor: validation reports mailbox does not exist. | Descriptor | `icon_emailaddr_undeliverable.svg` | `#F59E0B` | C:0 / P:2 | — |
| `EMAILADDR_DISPOSABLE` | Disposable Email Address | Descriptor: address is from a disposable provider. | Descriptor | `icon_emailaddr_disposable.svg` | `#F59E0B` | C:0 / P:5 | — |
| `AFFILIATE_EMAILADDR` | Affiliate - Email Address | Email found in affiliate/third-party context. | Entity | `icon_affiliate_emailaddr.svg` | `#3B82F6` | C:0 / P:3 | — |
| `MALICIOUS_EMAILADDR` | Malicious E-mail Address | Descriptor: address flagged malicious on reputation feeds. | Descriptor | `icon_malicious_emailaddr.svg` | `#F59E0B` | C:0 / P:5 | — |

## Phone numbers

Telephone entities and metadata.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `PHONE_NUMBER` | Phone Number | E.164 or local-format phone number tied to the target. | Entity | `icon_phone_number.svg` | `#3B82F6` | C:14 / P:9 | — |
| `PHONE_NUMBER_TYPE` | Phone Number Type | Descriptor: line type (mobile, VoIP, fixed) from validation APIs. | Descriptor | `icon_phone_number_type.svg` | `#F59E0B` | C:0 / P:3 | — |
| `PHONE_NUMBER_COMPROMISED` | Phone Number Compromised | Descriptor: number linked to spam/abuse or breach sources. | Descriptor | `icon_phone_number_compromised.svg` | `#F59E0B` | C:0 / P:1 | — |
| `MALICIOUS_PHONE_NUMBER` | Malicious Phone Number | Descriptor: number on telephony threat lists. | Descriptor | `icon_malicious_phone_number.svg` | `#F59E0B` | C:0 / P:3 | — |

## People, organisations & location

Real-world identity and org entities.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `HUMAN_NAME` | Human Name | Person name associated with the target (WHOIS, profiles, leaks). | Entity | `icon_human_name.svg` | `#3B82F6` | C:7 / P:6 | — |
| `JOB_TITLE` | Job Title | Job title descriptor linked to a person or org record. | Descriptor | `icon_job_title.svg` | `#F59E0B` | C:0 / P:1 | — |
| `DATE_HUMAN_DOB` | Date of Birth | Date of birth for a person — high-sensitivity PII for identity verification. | Entity | `icon_date_human_dob.svg` | `#3B82F6` | — | — |
| `COMPANY_NAME` | Company Name | Organisation name on the footprint (owned or attributed). | Entity | `icon_company_name.svg` | `#3B82F6` | C:2 / P:10 | — |
| `COUNTRY_NAME` | Country Name | Country associated with an entity (registration, geo, or content). | Entity | `icon_country_name.svg` | `#3B82F6` | C:0 / P:1 | — |
| `PHYSICAL_ADDRESS` | Physical Address | Postal or street address. | Entity | `icon_physical_address.svg` | `#3B82F6` | C:3 / P:9 | — |
| `PHYSICAL_COORDINATES` | Physical Coordinates | Lat/long or coordinate pair for a location. | Entity | `icon_physical_coordinates.svg` | `#3B82F6` | C:1 / P:8 | — |
| `LEI` | Legal Entity Identifier | Legal Entity Identifier (GLEIF) for a company — formal org identity. | Entity | `icon_lei.svg` | `#3B82F6` | C:1 / P:1 | — |

## Credentials, cards & banking

Sensitive financial identifiers.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `CREDIT_CARD_NUMBER` | Credit Card Number | Payment card number found in content or leaks — critical secret. | Entity | `icon_credit_card_number.svg` | `#3B82F6` | C:0 / P:1 | — |
| `IBAN_NUMBER` | IBAN Number | International bank account number. | Entity | `icon_iban_number.svg` | `#3B82F6` | C:1 / P:1 | — |
| `PASSWORD_COMPROMISED` | Compromised Password | Cleartext or recovered password from breaches — critical secret. | Data | `icon_password_compromised.svg` | `#14B8A6` | C:0 / P:3 | — |
| `HASH` | Hash | Cryptographic hash found in content (file integrity, commits, etc.). | Data | `icon_hash.svg` | `#14B8A6` | C:0 / P:1 | Hex digest |
| `HASH_COMPROMISED` | Compromised Password Hash | Password hash appearing in breach databases. | Data | `icon_hash_compromised.svg` | `#14B8A6` | C:0 / P:1 | — |
| `BASE64_DATA` | Base64-encoded Data | Base64-encoded blob extracted from content — may hide secrets or payloads. | Data | `icon_base64_data.svg` | `#14B8A6` | C:3 / P:1 | — |

## Cryptocurrency

On-chain addresses and balances.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `BITCOIN_ADDRESS` | Bitcoin Address | Bitcoin address on the footprint. | Entity | `icon_bitcoin_address.svg` | `#3B82F6` | C:4 / P:2 | — |
| `BITCOIN_BALANCE` | Bitcoin Balance | Descriptor: on-chain balance or value observation for a BTC address. | Descriptor | `icon_bitcoin_balance.svg` | `#F59E0B` | C:0 / P:1 | — |
| `MALICIOUS_BITCOIN_ADDRESS` | Malicious Bitcoin Address | Descriptor: BTC address on scam/ransomware lists. | Descriptor | `icon_malicious_bitcoin_address.svg` | `#F59E0B` | C:0 / P:2 | — |
| `ETHEREUM_ADDRESS` | Ethereum Address | Ethereum address on the footprint. | Entity | `icon_ethereum_address.svg` | `#3B82F6` | C:1 / P:1 | — |
| `ETHEREUM_BALANCE` | Ethereum Balance | Descriptor: ETH balance or token holding observation. | Descriptor | `icon_ethereum_balance.svg` | `#F59E0B` | C:0 / P:1 | — |

## Files & interesting content

Discovered files and leak-adjacent blobs.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `INTERESTING_FILE` | Interesting File | Descriptor: file path/URL flagged as sensitive (configs, backups, keys). | Descriptor | `icon_interesting_file.svg` | `#F59E0B` | C:2 / P:1 | — |
| `INTERESTING_FILE_HISTORIC` | Historic Interesting File | Historic interesting file from archive sources. | Descriptor | `icon_interesting_file_historic.svg` | `#F59E0B` | C:0 / P:1 | — |
| `JUNK_FILE` | Junk File | Descriptor: low-value or noise file (skip further processing). | Descriptor | `icon_junk_file.svg` | `#F59E0B` | C:0 / P:1 | — |
| `LEAKSITE_URL` | Leak Site URL | URL pointing to a paste/leak site entry. | Entity | `icon_leaksite_url.svg` | `#3B82F6` | C:0 / P:6 | — |
| `LEAKSITE_CONTENT` | Leak Site Content | Content body from a leak/paste site. | Data | `icon_leaksite_content.svg` | `#14B8A6` | C:5 / P:7 | — |
| `DARKNET_MENTION_URL` | Darknet Mention URL | URL referencing darknet/onion mention of the target. | Descriptor | `icon_darknet_mention_url.svg` | `#F59E0B` | C:1 / P:5 | — |
| `DARKNET_MENTION_CONTENT` | Darknet Mention Web Content | Content from darknet mention sources. | Data | `icon_darknet_mention_content.svg` | `#14B8A6` | C:2 / P:4 | — |
| `PGP_KEY` | PGP Public Key | PGP public key material — ties to encrypted comms identity. | Data | `icon_pgp_key.svg` | `#14B8A6` | C:0 / P:2 | — |

## Cloud & app stores

Exposed buckets and mobile store entries.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `CLOUD_STORAGE_BUCKET` | Cloud Storage Bucket | Object storage bucket name (S3, Azure, GCS, etc.). | Entity | `icon_cloud_storage_bucket.svg` | `#3B82F6` | C:0 / P:5 | — |
| `CLOUD_STORAGE_BUCKET_OPEN` | Cloud Storage Bucket Open | Descriptor: bucket allows public listing or read — data exposure risk. | Descriptor | `icon_cloud_storage_bucket_open.svg` | `#F59E0B` | C:0 / P:4 | — |
| `APPSTORE_ENTRY` | App Store Entry | Mobile app store listing linked to the target org or brand. | Entity | `icon_appstore_entry.svg` | `#3B82F6` | C:0 / P:3 | — |
| `PUBLIC_CODE_REPO` | Public Code Repository | Source code repository (GitHub, GitLab, etc.). | Entity | `icon_public_code_repo.svg` | `#3B82F6` | C:1 / P:2 | — |

## Reputation — internet names

Blacklist / deface / malicious overlays on names.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `BLACKLISTED_INTERNET_NAME` | Blacklisted Internet Name | Descriptor: hostname on DNS or web reputation blocklists. | Descriptor | `icon_blacklisted_internet_name.svg` | `#F59E0B` | C:0 / P:18 | — |
| `BLACKLISTED_AFFILIATE_INTERNET_NAME` | Blacklisted Affiliate Internet Name | Descriptor: affiliate hostname blacklisted. | Descriptor | `icon_blacklisted_affiliate_internet_name.svg` | `#F59E0B` | C:0 / P:17 | — |
| `DEFACED_INTERNET_NAME` | Defaced | Descriptor: hostname reported defaced. | Descriptor | `icon_defaced_internet_name.svg` | `#F59E0B` | C:0 / P:1 | — |
| `DEFACED_AFFILIATE_INTERNET_NAME` | Defaced Affiliate | Descriptor: affiliate hostname defaced. | Descriptor | `icon_defaced_affiliate_internet_name.svg` | `#F59E0B` | C:0 / P:1 | — |
| `MALICIOUS_INTERNET_NAME` | Malicious Internet Name | Descriptor: hostname on malware/phishing feeds. | Descriptor | `icon_malicious_internet_name.svg` | `#F59E0B` | C:0 / P:24 | — |
| `MALICIOUS_AFFILIATE_INTERNET_NAME` | Malicious Affiliate | Descriptor: affiliate hostname flagged malicious. | Descriptor | `icon_malicious_affiliate_internet_name.svg` | `#F59E0B` | C:0 / P:21 | — |

## Reputation — IP & netblocks

Threat overlays on addresses and ranges.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `BLACKLISTED_IPADDR` | Blacklisted IP Address | Descriptor: IPv4 on IP reputation blocklists. | Descriptor | `icon_blacklisted_ipaddr.svg` | `#F59E0B` | C:0 / P:29 | — |
| `BLACKLISTED_AFFILIATE_IPADDR` | Blacklisted Affiliate IP Address | Descriptor: affiliate IP blacklisted. | Descriptor | `icon_blacklisted_affiliate_ipaddr.svg` | `#F59E0B` | C:0 / P:26 | — |
| `BLACKLISTED_SUBNET` | Blacklisted IP on Same Subnet | Descriptor: another IP on same subnet is blacklisted — neighbourhood risk. | Descriptor | `icon_blacklisted_subnet.svg` | `#F59E0B` | C:0 / P:19 | — |
| `BLACKLISTED_NETBLOCK` | Blacklisted IP on Owned Netblock | Descriptor: blacklisted IP within target-owned netblock. | Descriptor | `icon_blacklisted_netblock.svg` | `#F59E0B` | C:0 / P:19 | — |
| `DEFACED_IPADDR` | Defaced IP Address | Descriptor: IP associated with a defacement incident. | Descriptor | `icon_defaced_ipaddr.svg` | `#F59E0B` | C:0 / P:1 | — |
| `DEFACED_AFFILIATE_IPADDR` | Defaced Affiliate IP Address | Descriptor: affiliate IP tied to defacement. | Descriptor | `icon_defaced_affiliate_ipaddr.svg` | `#F59E0B` | C:0 / P:1 | — |
| `MALICIOUS_IPADDR` | Malicious IP Address | Descriptor: IP on malware/C2/phishing intelligence feeds. | Descriptor | `icon_malicious_ipaddr.svg` | `#F59E0B` | C:0 / P:49 | — |
| `MALICIOUS_AFFILIATE_IPADDR` | Malicious Affiliate IP Address | Descriptor: affiliate IP flagged malicious. | Descriptor | `icon_malicious_affiliate_ipaddr.svg` | `#F59E0B` | C:0 / P:38 | — |
| `MALICIOUS_SUBNET` | Malicious IP on Same Subnet | Descriptor: malicious host on same subnet as target IP. | Descriptor | `icon_malicious_subnet.svg` | `#F59E0B` | C:0 / P:24 | — |
| `MALICIOUS_NETBLOCK` | Malicious IP on Owned Netblock | Descriptor: malicious host within owned netblock. | Descriptor | `icon_malicious_netblock.svg` | `#F59E0B` | C:0 / P:26 | — |

## Vulnerabilities

CVE tiers and general findings.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `VULNERABILITY_GENERAL` | Vulnerability - General | Non-CVE security finding (misconfig, exposed panel, nuclei matcher, etc.). | Descriptor | `icon_vulnerability_general.svg` | `#F59E0B` | C:0 / P:9 | — |
| `VULNERABILITY_DISCLOSURE` | Vulnerability - Third Party Disclosure | Public disclosure reference (advisory, responsible disclosure ticket). | Descriptor | `icon_vulnerability_disclosure.svg` | `#F59E0B` | C:0 / P:2 | — |
| `VULNERABILITY_CVE_CRITICAL` | Vulnerability - CVE Critical | CVE rated critical severity — patch priority. | Descriptor | `icon_vulnerability_cve_critical.svg` | `#F59E0B` | C:0 / P:7 | CVE description from `sf.cveInfo()` |
| `VULNERABILITY_CVE_HIGH` | Vulnerability - CVE High | CVE rated high severity. | Descriptor | `icon_vulnerability_cve_high.svg` | `#F59E0B` | C:0 / P:7 | — |
| `VULNERABILITY_CVE_MEDIUM` | Vulnerability - CVE Medium | CVE rated medium severity. | Descriptor | `icon_vulnerability_cve_medium.svg` | `#F59E0B` | C:0 / P:7 | — |
| `VULNERABILITY_CVE_LOW` | Vulnerability - CVE Low | CVE rated low severity. | Descriptor | `icon_vulnerability_cve_low.svg` | `#F59E0B` | C:0 / P:7 | — |

## WiFi & misc network

Wireless and error surfaces.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `WIFI_ACCESS_POINT` | WiFi Access Point Nearby | WiFi BSSIDs/SSIDs near a geo location (Wigle, etc.). | Entity | `icon_wifi_access_point.svg` | `#3B82F6` | C:0 / P:1 | — |
| `ERROR_MESSAGE` | Error Message | Error string from a module or HTTP failure — diagnostic, not intelligence. | Data | `icon_error_message.svg` | `#14B8A6` | C:0 / P:1 | — |
| `WIKIPEDIA_PAGE_EDIT` | Wikipedia Page Edit | Wikipedia edit event tied to target-related pages — reputation/history OSINT. | Descriptor | `icon_wikipedia_page_edit.svg` | `#F59E0B` | C:0 / P:1 | — |

## Raw API & registry payloads

Opaque evidence retained for audit and re-parse.

| Nugget ID | Description | Purpose & definition | Archetype | Icon | Colour | Catalogue (consume / produce) | Typical `data` encoding |
|-----------|-------------|----------------------|-----------|------|--------|------------------------------|-------------------------|
| `RAW_RIR_DATA` | Raw Data from RIRs/APIs | Unprocessed API/RIR JSON — preserves vendor response for replay and deep parsing. | Data | `icon_raw_rir_data.svg` | `#14B8A6` | C:3 / P:80 | `str(api_dict)` or JSON-like blob |
| `RAW_FILE_META_DATA` | Raw File Meta Data | File metadata blob (EXIF, Office props) from `sfp_filemeta`. | Data | `icon_raw_file_meta_data.svg` | `#14B8A6` | C:4 / P:2 | — |

---

## Extending the catalog

Adding a type requires: row in `nuggets.json`, TypeDB entity in `spiderfeet_map.tql`, module `producedEvents()` + emission code, catalogue route + test seed. See [06-recommendations-and-roadmap.md](06-recommendations-and-roadmap.md).
