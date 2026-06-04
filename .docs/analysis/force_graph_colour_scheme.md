# Force Graph Colour Scheme

A reference guide for node types, colours, and icon conventions used in the Spiderfeet nugget force graph.

---

## Node Structure

Each node is rendered as a **50×50 rounded square** (border-radius: 5px) filled with its type colour. A white icon is composited on top to represent the specific nugget.

- **Canvas size:** 50 × 50 px  
- **Corner radius:** 5 px  
- **Background:** White (`#FFFFFF`)  
- **Icon colour:** White (`#FFFFFF`)  
- **Icon style:** Stroke-based line art, stroke-width 2–2.5px  

---

## Type Colour Key

| Type | Hex | Swatch | Count | Description |
|------|-----|--------|-------|-------------|
| `ENTITY` | `#3B82F6` | 🟦 | 75 | Primary nodes — domains, IPs, emails, people, companies |
| `DESCRIPTOR` | `#F59E0B` | 🟨 | 57 | Attributes that qualify another node — blacklists, vulnerabilities, flags |
| `DATA` | `#14B8A6` | 🟩 | 24 | Raw or structured data payloads — DNS records, certificates, web content |
| `SUBENTITY` | `#F97316` | 🟧 | 4 | Child nodes that only exist in context of a parent — open ports, linked URLs |
| `INTERNAL` | `#8B5CF6` | 🟪 | 1 | System-internal nodes — the ROOT event |

---

## Icon Naming Convention

Each icon file follows the pattern:

```
icon_<nugget_id_lowercase>.svg
```

**Examples:**

| nugget_id | Icon filename |
|-----------|---------------|
| `DOMAIN_NAME` | `icon_domain_name.svg` |
| `IP_ADDRESS` | `icon_ip_address.svg` |
| `VULNERABILITY_CVE_CRITICAL` | `icon_vulnerability_cve_critical.svg` |
| `SSL_CERTIFICATE_ISSUED` | `icon_ssl_certificate_issued.svg` |

---

## Icon Design Conventions

Icons use a consistent visual language across families:

| Family | Visual Pattern |
|--------|----------------|
| **Affiliate nodes** | Base icon + side tick marks (`—`) to indicate affiliation |
| **Blacklisted nodes** | Circle with diagonal strike-through |
| **Defaced nodes** | Base icon + ✕ mark in corner |
| **Malicious nodes** | Warning star badge with domain-specific sub-icon |
| **Compromised nodes** | Base icon + ✕ mark overlay |
| **Historic URLs** | Dashed border + clock/arrow motif above |
| **Vulnerability levels** | Triangle warning — larger/bolder = higher severity |
| **SSL certificates** | Shield outline with type-specific interior detail |
| **DNS records** | Rounded rectangle with record type label (`TXT`, `SRV`, `SPF`) |
| **Ports (TCP/UDP)** | Rectangle with horizontal pipe connectors on both sides |
| **Crypto addresses** | Bitcoin `₿` / Ethereum diamond polygon shape |
| **Geo nodes** | Map pin / crosshair |

---

## Full Node List

| Icon | nugget_id | Description | Type | Colour | Icon file |
|------|-----------|-------------|------|--------|-----------|
| <img src="nugget_icons/icon_root.svg" width="40" height="40" alt="" /> | `ROOT` | Internal Spiderfeet Root event | INTERNAL | `#8B5CF6` | `icon_root.svg` |
| <img src="nugget_icons/icon_account_external_owned.svg" width="40" height="40" alt="" /> | `ACCOUNT_EXTERNAL_OWNED` | Account on External Site | ENTITY | `#3B82F6` | `icon_account_external_owned.svg` |
| <img src="nugget_icons/icon_account_external_owned_compromised.svg" width="40" height="40" alt="" /> | `ACCOUNT_EXTERNAL_OWNED_COMPROMISED` | Hacked Account on External Site | DESCRIPTOR | `#F59E0B` | `icon_account_external_owned_compromised.svg` |
| <img src="nugget_icons/icon_account_external_user_shared_compromised.svg" width="40" height="40" alt="" /> | `ACCOUNT_EXTERNAL_USER_SHARED_COMPROMISED` | Hacked User Account on External Site | DESCRIPTOR | `#F59E0B` | `icon_account_external_user_shared_compromised.svg` |
| <img src="nugget_icons/icon_affiliate_emailaddr.svg" width="40" height="40" alt="" /> | `AFFILIATE_EMAILADDR` | Affiliate - Email Address | ENTITY | `#3B82F6` | `icon_affiliate_emailaddr.svg` |
| <img src="nugget_icons/icon_affiliate_internet_name.svg" width="40" height="40" alt="" /> | `AFFILIATE_INTERNET_NAME` | Affiliate - Internet Name | ENTITY | `#3B82F6` | `icon_affiliate_internet_name.svg` |
| <img src="nugget_icons/icon_affiliate_internet_name_hijackable.svg" width="40" height="40" alt="" /> | `AFFILIATE_INTERNET_NAME_HIJACKABLE` | Affiliate - Internet Name Hijackable | ENTITY | `#3B82F6` | `icon_affiliate_internet_name_hijackable.svg` |
| <img src="nugget_icons/icon_affiliate_internet_name_unresolved.svg" width="40" height="40" alt="" /> | `AFFILIATE_INTERNET_NAME_UNRESOLVED` | Affiliate - Internet Name - Unresolved | ENTITY | `#3B82F6` | `icon_affiliate_internet_name_unresolved.svg` |
| <img src="nugget_icons/icon_affiliate_ipaddr.svg" width="40" height="40" alt="" /> | `AFFILIATE_IPADDR` | Affiliate - IP Address | ENTITY | `#3B82F6` | `icon_affiliate_ipaddr.svg` |
| <img src="nugget_icons/icon_affiliate_ipv6_address.svg" width="40" height="40" alt="" /> | `AFFILIATE_IPV6_ADDRESS` | Affiliate - IPv6 Address | ENTITY | `#3B82F6` | `icon_affiliate_ipv6_address.svg` |
| <img src="nugget_icons/icon_affiliate_web_content.svg" width="40" height="40" alt="" /> | `AFFILIATE_WEB_CONTENT` | Affiliate - Web Content | DATA | `#14B8A6` | `icon_affiliate_web_content.svg` |
| <img src="nugget_icons/icon_affiliate_domain_name.svg" width="40" height="40" alt="" /> | `AFFILIATE_DOMAIN_NAME` | Affiliate - Domain Name | ENTITY | `#3B82F6` | `icon_affiliate_domain_name.svg` |
| <img src="nugget_icons/icon_affiliate_domain_unregistered.svg" width="40" height="40" alt="" /> | `AFFILIATE_DOMAIN_UNREGISTERED` | Affiliate - Domain Name Unregistered | ENTITY | `#3B82F6` | `icon_affiliate_domain_unregistered.svg` |
| <img src="nugget_icons/icon_affiliate_company_name.svg" width="40" height="40" alt="" /> | `AFFILIATE_COMPANY_NAME` | Affiliate - Company Name | ENTITY | `#3B82F6` | `icon_affiliate_company_name.svg` |
| <img src="nugget_icons/icon_affiliate_domain_whois.svg" width="40" height="40" alt="" /> | `AFFILIATE_DOMAIN_WHOIS` | Affiliate - Domain Whois | DATA | `#14B8A6` | `icon_affiliate_domain_whois.svg` |
| <img src="nugget_icons/icon_affiliate_description_category.svg" width="40" height="40" alt="" /> | `AFFILIATE_DESCRIPTION_CATEGORY` | Affiliate Description - Category | DESCRIPTOR | `#F59E0B` | `icon_affiliate_description_category.svg` |
| <img src="nugget_icons/icon_affiliate_description_abstract.svg" width="40" height="40" alt="" /> | `AFFILIATE_DESCRIPTION_ABSTRACT` | Affiliate Description - Abstract | DESCRIPTOR | `#F59E0B` | `icon_affiliate_description_abstract.svg` |
| <img src="nugget_icons/icon_appstore_entry.svg" width="40" height="40" alt="" /> | `APPSTORE_ENTRY` | App Store Entry | ENTITY | `#3B82F6` | `icon_appstore_entry.svg` |
| <img src="nugget_icons/icon_cloud_storage_bucket.svg" width="40" height="40" alt="" /> | `CLOUD_STORAGE_BUCKET` | Cloud Storage Bucket | ENTITY | `#3B82F6` | `icon_cloud_storage_bucket.svg` |
| <img src="nugget_icons/icon_cloud_storage_bucket_open.svg" width="40" height="40" alt="" /> | `CLOUD_STORAGE_BUCKET_OPEN` | Cloud Storage Bucket Open | DESCRIPTOR | `#F59E0B` | `icon_cloud_storage_bucket_open.svg` |
| <img src="nugget_icons/icon_company_name.svg" width="40" height="40" alt="" /> | `COMPANY_NAME` | Company Name | ENTITY | `#3B82F6` | `icon_company_name.svg` |
| <img src="nugget_icons/icon_credit_card_number.svg" width="40" height="40" alt="" /> | `CREDIT_CARD_NUMBER` | Credit Card Number | ENTITY | `#3B82F6` | `icon_credit_card_number.svg` |
| <img src="nugget_icons/icon_base64_data.svg" width="40" height="40" alt="" /> | `BASE64_DATA` | Base64-encoded Data | DATA | `#14B8A6` | `icon_base64_data.svg` |
| <img src="nugget_icons/icon_bitcoin_address.svg" width="40" height="40" alt="" /> | `BITCOIN_ADDRESS` | Bitcoin Address | ENTITY | `#3B82F6` | `icon_bitcoin_address.svg` |
| <img src="nugget_icons/icon_bitcoin_balance.svg" width="40" height="40" alt="" /> | `BITCOIN_BALANCE` | Bitcoin Balance | DESCRIPTOR | `#F59E0B` | `icon_bitcoin_balance.svg` |
| <img src="nugget_icons/icon_bgp_as_owner.svg" width="40" height="40" alt="" /> | `BGP_AS_OWNER` | BGP AS Ownership | ENTITY | `#3B82F6` | `icon_bgp_as_owner.svg` |
| <img src="nugget_icons/icon_bgp_as_member.svg" width="40" height="40" alt="" /> | `BGP_AS_MEMBER` | BGP AS Membership | ENTITY | `#3B82F6` | `icon_bgp_as_member.svg` |
| <img src="nugget_icons/icon_blacklisted_cohost.svg" width="40" height="40" alt="" /> | `BLACKLISTED_COHOST` | Blacklisted Co-Hosted Site | DESCRIPTOR | `#F59E0B` | `icon_blacklisted_cohost.svg` |
| <img src="nugget_icons/icon_blacklisted_internet_name.svg" width="40" height="40" alt="" /> | `BLACKLISTED_INTERNET_NAME` | Blacklisted Internet Name | DESCRIPTOR | `#F59E0B` | `icon_blacklisted_internet_name.svg` |
| <img src="nugget_icons/icon_blacklisted_affiliate_internet_name.svg" width="40" height="40" alt="" /> | `BLACKLISTED_AFFILIATE_INTERNET_NAME` | Blacklisted Affiliate Internet Name | DESCRIPTOR | `#F59E0B` | `icon_blacklisted_affiliate_internet_name.svg` |
| <img src="nugget_icons/icon_blacklisted_ipaddr.svg" width="40" height="40" alt="" /> | `BLACKLISTED_IPADDR` | Blacklisted IP Address | DESCRIPTOR | `#F59E0B` | `icon_blacklisted_ipaddr.svg` |
| <img src="nugget_icons/icon_blacklisted_affiliate_ipaddr.svg" width="40" height="40" alt="" /> | `BLACKLISTED_AFFILIATE_IPADDR` | Blacklisted Affiliate IP Address | DESCRIPTOR | `#F59E0B` | `icon_blacklisted_affiliate_ipaddr.svg` |
| <img src="nugget_icons/icon_blacklisted_subnet.svg" width="40" height="40" alt="" /> | `BLACKLISTED_SUBNET` | Blacklisted IP on Same Subnet | DESCRIPTOR | `#F59E0B` | `icon_blacklisted_subnet.svg` |
| <img src="nugget_icons/icon_blacklisted_netblock.svg" width="40" height="40" alt="" /> | `BLACKLISTED_NETBLOCK` | Blacklisted IP on Owned Netblock | DESCRIPTOR | `#F59E0B` | `icon_blacklisted_netblock.svg` |
| <img src="nugget_icons/icon_country_name.svg" width="40" height="40" alt="" /> | `COUNTRY_NAME` | Country Name | ENTITY | `#3B82F6` | `icon_country_name.svg` |
| <img src="nugget_icons/icon_co_hosted_site.svg" width="40" height="40" alt="" /> | `CO_HOSTED_SITE` | Co-Hosted Site | ENTITY | `#3B82F6` | `icon_co_hosted_site.svg` |
| <img src="nugget_icons/icon_co_hosted_site_domain.svg" width="40" height="40" alt="" /> | `CO_HOSTED_SITE_DOMAIN` | Co-Hosted Site - Domain Name | ENTITY | `#3B82F6` | `icon_co_hosted_site_domain.svg` |
| <img src="nugget_icons/icon_co_hosted_site_domain_whois.svg" width="40" height="40" alt="" /> | `CO_HOSTED_SITE_DOMAIN_WHOIS` | Co-Hosted Site - Domain Whois | DATA | `#14B8A6` | `icon_co_hosted_site_domain_whois.svg` |
| <img src="nugget_icons/icon_darknet_mention_url.svg" width="40" height="40" alt="" /> | `DARKNET_MENTION_URL` | Darknet Mention URL | DESCRIPTOR | `#F59E0B` | `icon_darknet_mention_url.svg` |
| <img src="nugget_icons/icon_darknet_mention_content.svg" width="40" height="40" alt="" /> | `DARKNET_MENTION_CONTENT` | Darknet Mention Web Content | DATA | `#14B8A6` | `icon_darknet_mention_content.svg` |
| <img src="nugget_icons/icon_date_human_dob.svg" width="40" height="40" alt="" /> | `DATE_HUMAN_DOB` | Date of Birth | ENTITY | `#3B82F6` | `icon_date_human_dob.svg` |
| <img src="nugget_icons/icon_defaced_internet_name.svg" width="40" height="40" alt="" /> | `DEFACED_INTERNET_NAME` | Defaced | DESCRIPTOR | `#F59E0B` | `icon_defaced_internet_name.svg` |
| <img src="nugget_icons/icon_defaced_ipaddr.svg" width="40" height="40" alt="" /> | `DEFACED_IPADDR` | Defaced IP Address | DESCRIPTOR | `#F59E0B` | `icon_defaced_ipaddr.svg` |
| <img src="nugget_icons/icon_defaced_affiliate_internet_name.svg" width="40" height="40" alt="" /> | `DEFACED_AFFILIATE_INTERNET_NAME` | Defaced Affiliate | DESCRIPTOR | `#F59E0B` | `icon_defaced_affiliate_internet_name.svg` |
| <img src="nugget_icons/icon_defaced_cohost.svg" width="40" height="40" alt="" /> | `DEFACED_COHOST` | Defaced Co-Hosted Site | DESCRIPTOR | `#F59E0B` | `icon_defaced_cohost.svg` |
| <img src="nugget_icons/icon_defaced_affiliate_ipaddr.svg" width="40" height="40" alt="" /> | `DEFACED_AFFILIATE_IPADDR` | Defaced Affiliate IP Address | DESCRIPTOR | `#F59E0B` | `icon_defaced_affiliate_ipaddr.svg` |
| <img src="nugget_icons/icon_description_category.svg" width="40" height="40" alt="" /> | `DESCRIPTION_CATEGORY` | Description - Category | DESCRIPTOR | `#F59E0B` | `icon_description_category.svg` |
| <img src="nugget_icons/icon_description_abstract.svg" width="40" height="40" alt="" /> | `DESCRIPTION_ABSTRACT` | Description - Abstract | DESCRIPTOR | `#F59E0B` | `icon_description_abstract.svg` |
| <img src="nugget_icons/icon_device_type.svg" width="40" height="40" alt="" /> | `DEVICE_TYPE` | Device Type | DESCRIPTOR | `#F59E0B` | `icon_device_type.svg` |
| <img src="nugget_icons/icon_dns_text.svg" width="40" height="40" alt="" /> | `DNS_TEXT` | DNS TXT Record | DATA | `#14B8A6` | `icon_dns_text.svg` |
| <img src="nugget_icons/icon_dns_srv.svg" width="40" height="40" alt="" /> | `DNS_SRV` | DNS SRV Record | DATA | `#14B8A6` | `icon_dns_srv.svg` |
| <img src="nugget_icons/icon_dns_spf.svg" width="40" height="40" alt="" /> | `DNS_SPF` | DNS SPF Record | DATA | `#14B8A6` | `icon_dns_spf.svg` |
| <img src="nugget_icons/icon_domain_name.svg" width="40" height="40" alt="" /> | `DOMAIN_NAME` | Domain Name | ENTITY | `#3B82F6` | `icon_domain_name.svg` |
| <img src="nugget_icons/icon_domain_name_parent.svg" width="40" height="40" alt="" /> | `DOMAIN_NAME_PARENT` | Domain Name (Parent) | ENTITY | `#3B82F6` | `icon_domain_name_parent.svg` |
| <img src="nugget_icons/icon_domain_registrar.svg" width="40" height="40" alt="" /> | `DOMAIN_REGISTRAR` | Domain Registrar | ENTITY | `#3B82F6` | `icon_domain_registrar.svg` |
| <img src="nugget_icons/icon_domain_whois.svg" width="40" height="40" alt="" /> | `DOMAIN_WHOIS` | Domain Whois | DATA | `#14B8A6` | `icon_domain_whois.svg` |
| <img src="nugget_icons/icon_emailaddr.svg" width="40" height="40" alt="" /> | `EMAILADDR` | Email Address | ENTITY | `#3B82F6` | `icon_emailaddr.svg` |
| <img src="nugget_icons/icon_emailaddr_compromised.svg" width="40" height="40" alt="" /> | `EMAILADDR_COMPROMISED` | Hacked Email Address | DESCRIPTOR | `#F59E0B` | `icon_emailaddr_compromised.svg` |
| <img src="nugget_icons/icon_emailaddr_deliverable.svg" width="40" height="40" alt="" /> | `EMAILADDR_DELIVERABLE` | Deliverable Email Address | DESCRIPTOR | `#F59E0B` | `icon_emailaddr_deliverable.svg` |
| <img src="nugget_icons/icon_emailaddr_disposable.svg" width="40" height="40" alt="" /> | `EMAILADDR_DISPOSABLE` | Disposable Email Address | DESCRIPTOR | `#F59E0B` | `icon_emailaddr_disposable.svg` |
| <img src="nugget_icons/icon_emailaddr_generic.svg" width="40" height="40" alt="" /> | `EMAILADDR_GENERIC` | Email Address - Generic | ENTITY | `#3B82F6` | `icon_emailaddr_generic.svg` |
| <img src="nugget_icons/icon_emailaddr_undeliverable.svg" width="40" height="40" alt="" /> | `EMAILADDR_UNDELIVERABLE` | Undeliverable Email Address | DESCRIPTOR | `#F59E0B` | `icon_emailaddr_undeliverable.svg` |
| <img src="nugget_icons/icon_error_message.svg" width="40" height="40" alt="" /> | `ERROR_MESSAGE` | Error Message | DATA | `#14B8A6` | `icon_error_message.svg` |
| <img src="nugget_icons/icon_ethereum_address.svg" width="40" height="40" alt="" /> | `ETHEREUM_ADDRESS` | Ethereum Address | ENTITY | `#3B82F6` | `icon_ethereum_address.svg` |
| <img src="nugget_icons/icon_ethereum_balance.svg" width="40" height="40" alt="" /> | `ETHEREUM_BALANCE` | Ethereum Balance | DESCRIPTOR | `#F59E0B` | `icon_ethereum_balance.svg` |
| <img src="nugget_icons/icon_geoinfo.svg" width="40" height="40" alt="" /> | `GEOINFO` | Physical Location | DESCRIPTOR | `#F59E0B` | `icon_geoinfo.svg` |
| <img src="nugget_icons/icon_hash.svg" width="40" height="40" alt="" /> | `HASH` | Hash | DATA | `#14B8A6` | `icon_hash.svg` |
| <img src="nugget_icons/icon_hash_compromised.svg" width="40" height="40" alt="" /> | `HASH_COMPROMISED` | Compromised Password Hash | DATA | `#14B8A6` | `icon_hash_compromised.svg` |
| <img src="nugget_icons/icon_http_code.svg" width="40" height="40" alt="" /> | `HTTP_CODE` | HTTP Status Code | DATA | `#14B8A6` | `icon_http_code.svg` |
| <img src="nugget_icons/icon_human_name.svg" width="40" height="40" alt="" /> | `HUMAN_NAME` | Human Name | ENTITY | `#3B82F6` | `icon_human_name.svg` |
| <img src="nugget_icons/icon_iban_number.svg" width="40" height="40" alt="" /> | `IBAN_NUMBER` | IBAN Number | ENTITY | `#3B82F6` | `icon_iban_number.svg` |
| <img src="nugget_icons/icon_interesting_file.svg" width="40" height="40" alt="" /> | `INTERESTING_FILE` | Interesting File | DESCRIPTOR | `#F59E0B` | `icon_interesting_file.svg` |
| <img src="nugget_icons/icon_interesting_file_historic.svg" width="40" height="40" alt="" /> | `INTERESTING_FILE_HISTORIC` | Historic Interesting File | DESCRIPTOR | `#F59E0B` | `icon_interesting_file_historic.svg` |
| <img src="nugget_icons/icon_junk_file.svg" width="40" height="40" alt="" /> | `JUNK_FILE` | Junk File | DESCRIPTOR | `#F59E0B` | `icon_junk_file.svg` |
| <img src="nugget_icons/icon_internal_ip_address.svg" width="40" height="40" alt="" /> | `INTERNAL_IP_ADDRESS` | IP Address - Internal Network | ENTITY | `#3B82F6` | `icon_internal_ip_address.svg` |
| <img src="nugget_icons/icon_internet_name.svg" width="40" height="40" alt="" /> | `INTERNET_NAME` | Internet Name | ENTITY | `#3B82F6` | `icon_internet_name.svg` |
| <img src="nugget_icons/icon_internet_name_unresolved.svg" width="40" height="40" alt="" /> | `INTERNET_NAME_UNRESOLVED` | Internet Name - Unresolved | ENTITY | `#3B82F6` | `icon_internet_name_unresolved.svg` |
| <img src="nugget_icons/icon_ip_address.svg" width="40" height="40" alt="" /> | `IP_ADDRESS` | IP Address | ENTITY | `#3B82F6` | `icon_ip_address.svg` |
| <img src="nugget_icons/icon_ipv6_address.svg" width="40" height="40" alt="" /> | `IPV6_ADDRESS` | IPv6 Address | ENTITY | `#3B82F6` | `icon_ipv6_address.svg` |
| <img src="nugget_icons/icon_lei.svg" width="40" height="40" alt="" /> | `LEI` | Legal Entity Identifier | ENTITY | `#3B82F6` | `icon_lei.svg` |
| <img src="nugget_icons/icon_job_title.svg" width="40" height="40" alt="" /> | `JOB_TITLE` | Job Title | DESCRIPTOR | `#F59E0B` | `icon_job_title.svg` |
| <img src="nugget_icons/icon_linked_url_internal.svg" width="40" height="40" alt="" /> | `LINKED_URL_INTERNAL` | Linked URL - Internal | SUBENTITY | `#F97316` | `icon_linked_url_internal.svg` |
| <img src="nugget_icons/icon_linked_url_external.svg" width="40" height="40" alt="" /> | `LINKED_URL_EXTERNAL` | Linked URL - External | SUBENTITY | `#F97316` | `icon_linked_url_external.svg` |
| <img src="nugget_icons/icon_malicious_asn.svg" width="40" height="40" alt="" /> | `MALICIOUS_ASN` | Malicious AS | DESCRIPTOR | `#F59E0B` | `icon_malicious_asn.svg` |
| <img src="nugget_icons/icon_malicious_bitcoin_address.svg" width="40" height="40" alt="" /> | `MALICIOUS_BITCOIN_ADDRESS` | Malicious Bitcoin Address | DESCRIPTOR | `#F59E0B` | `icon_malicious_bitcoin_address.svg` |
| <img src="nugget_icons/icon_malicious_ipaddr.svg" width="40" height="40" alt="" /> | `MALICIOUS_IPADDR` | Malicious IP Address | DESCRIPTOR | `#F59E0B` | `icon_malicious_ipaddr.svg` |
| <img src="nugget_icons/icon_malicious_cohost.svg" width="40" height="40" alt="" /> | `MALICIOUS_COHOST` | Malicious Co-Hosted Site | DESCRIPTOR | `#F59E0B` | `icon_malicious_cohost.svg` |
| <img src="nugget_icons/icon_malicious_emailaddr.svg" width="40" height="40" alt="" /> | `MALICIOUS_EMAILADDR` | Malicious E-mail Address | DESCRIPTOR | `#F59E0B` | `icon_malicious_emailaddr.svg` |
| <img src="nugget_icons/icon_malicious_internet_name.svg" width="40" height="40" alt="" /> | `MALICIOUS_INTERNET_NAME` | Malicious Internet Name | DESCRIPTOR | `#F59E0B` | `icon_malicious_internet_name.svg` |
| <img src="nugget_icons/icon_malicious_affiliate_internet_name.svg" width="40" height="40" alt="" /> | `MALICIOUS_AFFILIATE_INTERNET_NAME` | Malicious Affiliate | DESCRIPTOR | `#F59E0B` | `icon_malicious_affiliate_internet_name.svg` |
| <img src="nugget_icons/icon_malicious_affiliate_ipaddr.svg" width="40" height="40" alt="" /> | `MALICIOUS_AFFILIATE_IPADDR` | Malicious Affiliate IP Address | DESCRIPTOR | `#F59E0B` | `icon_malicious_affiliate_ipaddr.svg` |
| <img src="nugget_icons/icon_malicious_netblock.svg" width="40" height="40" alt="" /> | `MALICIOUS_NETBLOCK` | Malicious IP on Owned Netblock | DESCRIPTOR | `#F59E0B` | `icon_malicious_netblock.svg` |
| <img src="nugget_icons/icon_malicious_phone_number.svg" width="40" height="40" alt="" /> | `MALICIOUS_PHONE_NUMBER` | Malicious Phone Number | DESCRIPTOR | `#F59E0B` | `icon_malicious_phone_number.svg` |
| <img src="nugget_icons/icon_malicious_subnet.svg" width="40" height="40" alt="" /> | `MALICIOUS_SUBNET` | Malicious IP on Same Subnet | DESCRIPTOR | `#F59E0B` | `icon_malicious_subnet.svg` |
| <img src="nugget_icons/icon_netblock_owner.svg" width="40" height="40" alt="" /> | `NETBLOCK_OWNER` | Netblock Ownership | ENTITY | `#3B82F6` | `icon_netblock_owner.svg` |
| <img src="nugget_icons/icon_netblockv6_owner.svg" width="40" height="40" alt="" /> | `NETBLOCKV6_OWNER` | Netblock IPv6 Ownership | ENTITY | `#3B82F6` | `icon_netblockv6_owner.svg` |
| <img src="nugget_icons/icon_netblock_member.svg" width="40" height="40" alt="" /> | `NETBLOCK_MEMBER` | Netblock Membership | ENTITY | `#3B82F6` | `icon_netblock_member.svg` |
| <img src="nugget_icons/icon_netblockv6_member.svg" width="40" height="40" alt="" /> | `NETBLOCKV6_MEMBER` | Netblock IPv6 Membership | ENTITY | `#3B82F6` | `icon_netblockv6_member.svg` |
| <img src="nugget_icons/icon_netblock_whois.svg" width="40" height="40" alt="" /> | `NETBLOCK_WHOIS` | Netblock Whois | DATA | `#14B8A6` | `icon_netblock_whois.svg` |
| <img src="nugget_icons/icon_operating_system.svg" width="40" height="40" alt="" /> | `OPERATING_SYSTEM` | Operating System | DESCRIPTOR | `#F59E0B` | `icon_operating_system.svg` |
| <img src="nugget_icons/icon_leaksite_url.svg" width="40" height="40" alt="" /> | `LEAKSITE_URL` | Leak Site URL | ENTITY | `#3B82F6` | `icon_leaksite_url.svg` |
| <img src="nugget_icons/icon_leaksite_content.svg" width="40" height="40" alt="" /> | `LEAKSITE_CONTENT` | Leak Site Content | DATA | `#14B8A6` | `icon_leaksite_content.svg` |
| <img src="nugget_icons/icon_password_compromised.svg" width="40" height="40" alt="" /> | `PASSWORD_COMPROMISED` | Compromised Password | DATA | `#14B8A6` | `icon_password_compromised.svg` |
| <img src="nugget_icons/icon_phone_number.svg" width="40" height="40" alt="" /> | `PHONE_NUMBER` | Phone Number | ENTITY | `#3B82F6` | `icon_phone_number.svg` |
| <img src="nugget_icons/icon_phone_number_compromised.svg" width="40" height="40" alt="" /> | `PHONE_NUMBER_COMPROMISED` | Phone Number Compromised | DESCRIPTOR | `#F59E0B` | `icon_phone_number_compromised.svg` |
| <img src="nugget_icons/icon_phone_number_type.svg" width="40" height="40" alt="" /> | `PHONE_NUMBER_TYPE` | Phone Number Type | DESCRIPTOR | `#F59E0B` | `icon_phone_number_type.svg` |
| <img src="nugget_icons/icon_physical_address.svg" width="40" height="40" alt="" /> | `PHYSICAL_ADDRESS` | Physical Address | ENTITY | `#3B82F6` | `icon_physical_address.svg` |
| <img src="nugget_icons/icon_physical_coordinates.svg" width="40" height="40" alt="" /> | `PHYSICAL_COORDINATES` | Physical Coordinates | ENTITY | `#3B82F6` | `icon_physical_coordinates.svg` |
| <img src="nugget_icons/icon_pgp_key.svg" width="40" height="40" alt="" /> | `PGP_KEY` | PGP Public Key | DATA | `#14B8A6` | `icon_pgp_key.svg` |
| <img src="nugget_icons/icon_proxy_host.svg" width="40" height="40" alt="" /> | `PROXY_HOST` | Proxy Host | DESCRIPTOR | `#F59E0B` | `icon_proxy_host.svg` |
| <img src="nugget_icons/icon_provider_dns.svg" width="40" height="40" alt="" /> | `PROVIDER_DNS` | Name Server (DNS NS Records) | ENTITY | `#3B82F6` | `icon_provider_dns.svg` |
| <img src="nugget_icons/icon_provider_javascript.svg" width="40" height="40" alt="" /> | `PROVIDER_JAVASCRIPT` | Externally Hosted Javascript | ENTITY | `#3B82F6` | `icon_provider_javascript.svg` |
| <img src="nugget_icons/icon_provider_mail.svg" width="40" height="40" alt="" /> | `PROVIDER_MAIL` | Email Gateway (DNS MX Records) | ENTITY | `#3B82F6` | `icon_provider_mail.svg` |
| <img src="nugget_icons/icon_provider_hosting.svg" width="40" height="40" alt="" /> | `PROVIDER_HOSTING` | Hosting Provider | ENTITY | `#3B82F6` | `icon_provider_hosting.svg` |
| <img src="nugget_icons/icon_provider_telco.svg" width="40" height="40" alt="" /> | `PROVIDER_TELCO` | Telecommunications Provider | ENTITY | `#3B82F6` | `icon_provider_telco.svg` |
| <img src="nugget_icons/icon_public_code_repo.svg" width="40" height="40" alt="" /> | `PUBLIC_CODE_REPO` | Public Code Repository | ENTITY | `#3B82F6` | `icon_public_code_repo.svg` |
| <img src="nugget_icons/icon_raw_rir_data.svg" width="40" height="40" alt="" /> | `RAW_RIR_DATA` | Raw Data from RIRs/APIs | DATA | `#14B8A6` | `icon_raw_rir_data.svg` |
| <img src="nugget_icons/icon_raw_dns_records.svg" width="40" height="40" alt="" /> | `RAW_DNS_RECORDS` | Raw DNS Records | DATA | `#14B8A6` | `icon_raw_dns_records.svg` |
| <img src="nugget_icons/icon_raw_file_meta_data.svg" width="40" height="40" alt="" /> | `RAW_FILE_META_DATA` | Raw File Meta Data | DATA | `#14B8A6` | `icon_raw_file_meta_data.svg` |
| <img src="nugget_icons/icon_search_engine_web_content.svg" width="40" height="40" alt="" /> | `SEARCH_ENGINE_WEB_CONTENT` | Search Engine Web Content | DATA | `#14B8A6` | `icon_search_engine_web_content.svg` |
| <img src="nugget_icons/icon_social_media.svg" width="40" height="40" alt="" /> | `SOCIAL_MEDIA` | Social Media Presence | ENTITY | `#3B82F6` | `icon_social_media.svg` |
| <img src="nugget_icons/icon_similar_account_external.svg" width="40" height="40" alt="" /> | `SIMILAR_ACCOUNT_EXTERNAL` | Similar Account on External Site | ENTITY | `#3B82F6` | `icon_similar_account_external.svg` |
| <img src="nugget_icons/icon_similardomain.svg" width="40" height="40" alt="" /> | `SIMILARDOMAIN` | Similar Domain | ENTITY | `#3B82F6` | `icon_similardomain.svg` |
| <img src="nugget_icons/icon_similardomain_whois.svg" width="40" height="40" alt="" /> | `SIMILARDOMAIN_WHOIS` | Similar Domain - Whois | DATA | `#14B8A6` | `icon_similardomain_whois.svg` |
| <img src="nugget_icons/icon_software_used.svg" width="40" height="40" alt="" /> | `SOFTWARE_USED` | Software Used | SUBENTITY | `#F97316` | `icon_software_used.svg` |
| <img src="nugget_icons/icon_ssl_certificate_raw.svg" width="40" height="40" alt="" /> | `SSL_CERTIFICATE_RAW` | SSL Certificate - Raw Data | DATA | `#14B8A6` | `icon_ssl_certificate_raw.svg` |
| <img src="nugget_icons/icon_ssl_certificate_issued.svg" width="40" height="40" alt="" /> | `SSL_CERTIFICATE_ISSUED` | SSL Certificate - Issued to | ENTITY | `#3B82F6` | `icon_ssl_certificate_issued.svg` |
| <img src="nugget_icons/icon_ssl_certificate_issuer.svg" width="40" height="40" alt="" /> | `SSL_CERTIFICATE_ISSUER` | SSL Certificate - Issued by | ENTITY | `#3B82F6` | `icon_ssl_certificate_issuer.svg` |
| <img src="nugget_icons/icon_ssl_certificate_mismatch.svg" width="40" height="40" alt="" /> | `SSL_CERTIFICATE_MISMATCH` | SSL Certificate Host Mismatch | DESCRIPTOR | `#F59E0B` | `icon_ssl_certificate_mismatch.svg` |
| <img src="nugget_icons/icon_ssl_certificate_expired.svg" width="40" height="40" alt="" /> | `SSL_CERTIFICATE_EXPIRED` | SSL Certificate Expired | DESCRIPTOR | `#F59E0B` | `icon_ssl_certificate_expired.svg` |
| <img src="nugget_icons/icon_ssl_certificate_expiring.svg" width="40" height="40" alt="" /> | `SSL_CERTIFICATE_EXPIRING` | SSL Certificate Expiring | DESCRIPTOR | `#F59E0B` | `icon_ssl_certificate_expiring.svg` |
| <img src="nugget_icons/icon_target_web_content.svg" width="40" height="40" alt="" /> | `TARGET_WEB_CONTENT` | Web Content | DATA | `#14B8A6` | `icon_target_web_content.svg` |
| <img src="nugget_icons/icon_target_web_content_type.svg" width="40" height="40" alt="" /> | `TARGET_WEB_CONTENT_TYPE` | Web Content Type | DESCRIPTOR | `#F59E0B` | `icon_target_web_content_type.svg` |
| <img src="nugget_icons/icon_target_web_cookie.svg" width="40" height="40" alt="" /> | `TARGET_WEB_COOKIE` | Cookies | DATA | `#14B8A6` | `icon_target_web_cookie.svg` |
| <img src="nugget_icons/icon_tcp_port_open.svg" width="40" height="40" alt="" /> | `TCP_PORT_OPEN` | Open TCP Port | SUBENTITY | `#F97316` | `icon_tcp_port_open.svg` |
| <img src="nugget_icons/icon_tcp_port_open_banner.svg" width="40" height="40" alt="" /> | `TCP_PORT_OPEN_BANNER` | Open TCP Port Banner | DATA | `#14B8A6` | `icon_tcp_port_open_banner.svg` |
| <img src="nugget_icons/icon_tor_exit_node.svg" width="40" height="40" alt="" /> | `TOR_EXIT_NODE` | TOR Exit Node | DESCRIPTOR | `#F59E0B` | `icon_tor_exit_node.svg` |
| <img src="nugget_icons/icon_udp_port_open.svg" width="40" height="40" alt="" /> | `UDP_PORT_OPEN` | Open UDP Port | SUBENTITY | `#F97316` | `icon_udp_port_open.svg` |
| <img src="nugget_icons/icon_udp_port_open_info.svg" width="40" height="40" alt="" /> | `UDP_PORT_OPEN_INFO` | Open UDP Port Information | DATA | `#14B8A6` | `icon_udp_port_open_info.svg` |
| <img src="nugget_icons/icon_url_adblocked_external.svg" width="40" height="40" alt="" /> | `URL_ADBLOCKED_EXTERNAL` | URL (AdBlocked External) | DESCRIPTOR | `#F59E0B` | `icon_url_adblocked_external.svg` |
| <img src="nugget_icons/icon_url_adblocked_internal.svg" width="40" height="40" alt="" /> | `URL_ADBLOCKED_INTERNAL` | URL (AdBlocked Internal) | DESCRIPTOR | `#F59E0B` | `icon_url_adblocked_internal.svg` |
| <img src="nugget_icons/icon_url_form.svg" width="40" height="40" alt="" /> | `URL_FORM` | URL (Form) | DESCRIPTOR | `#F59E0B` | `icon_url_form.svg` |
| <img src="nugget_icons/icon_url_flash.svg" width="40" height="40" alt="" /> | `URL_FLASH` | URL (Uses Flash) | DESCRIPTOR | `#F59E0B` | `icon_url_flash.svg` |
| <img src="nugget_icons/icon_url_javascript.svg" width="40" height="40" alt="" /> | `URL_JAVASCRIPT` | URL (Uses Javascript) | DESCRIPTOR | `#F59E0B` | `icon_url_javascript.svg` |
| <img src="nugget_icons/icon_url_web_framework.svg" width="40" height="40" alt="" /> | `URL_WEB_FRAMEWORK` | URL (Uses a Web Framework) | DESCRIPTOR | `#F59E0B` | `icon_url_web_framework.svg` |
| <img src="nugget_icons/icon_url_java_applet.svg" width="40" height="40" alt="" /> | `URL_JAVA_APPLET` | URL (Uses Java Applet) | DESCRIPTOR | `#F59E0B` | `icon_url_java_applet.svg` |
| <img src="nugget_icons/icon_url_static.svg" width="40" height="40" alt="" /> | `URL_STATIC` | URL (Purely Static) | DESCRIPTOR | `#F59E0B` | `icon_url_static.svg` |
| <img src="nugget_icons/icon_url_password.svg" width="40" height="40" alt="" /> | `URL_PASSWORD` | URL (Accepts Passwords) | DESCRIPTOR | `#F59E0B` | `icon_url_password.svg` |
| <img src="nugget_icons/icon_url_upload.svg" width="40" height="40" alt="" /> | `URL_UPLOAD` | URL (Accepts Uploads) | DESCRIPTOR | `#F59E0B` | `icon_url_upload.svg` |
| <img src="nugget_icons/icon_url_form_historic.svg" width="40" height="40" alt="" /> | `URL_FORM_HISTORIC` | Historic URL (Form) | DESCRIPTOR | `#F59E0B` | `icon_url_form_historic.svg` |
| <img src="nugget_icons/icon_url_flash_historic.svg" width="40" height="40" alt="" /> | `URL_FLASH_HISTORIC` | Historic URL (Uses Flash) | DESCRIPTOR | `#F59E0B` | `icon_url_flash_historic.svg` |
| <img src="nugget_icons/icon_url_javascript_historic.svg" width="40" height="40" alt="" /> | `URL_JAVASCRIPT_HISTORIC` | Historic URL (Uses Javascript) | DESCRIPTOR | `#F59E0B` | `icon_url_javascript_historic.svg` |
| <img src="nugget_icons/icon_url_web_framework_historic.svg" width="40" height="40" alt="" /> | `URL_WEB_FRAMEWORK_HISTORIC` | Historic URL (Uses a Web Framework) | DESCRIPTOR | `#F59E0B` | `icon_url_web_framework_historic.svg` |
| <img src="nugget_icons/icon_url_java_applet_historic.svg" width="40" height="40" alt="" /> | `URL_JAVA_APPLET_HISTORIC` | Historic URL (Uses Java Applet) | DESCRIPTOR | `#F59E0B` | `icon_url_java_applet_historic.svg` |
| <img src="nugget_icons/icon_url_static_historic.svg" width="40" height="40" alt="" /> | `URL_STATIC_HISTORIC` | Historic URL (Purely Static) | DESCRIPTOR | `#F59E0B` | `icon_url_static_historic.svg` |
| <img src="nugget_icons/icon_url_password_historic.svg" width="40" height="40" alt="" /> | `URL_PASSWORD_HISTORIC` | Historic URL (Accepts Passwords) | DESCRIPTOR | `#F59E0B` | `icon_url_password_historic.svg` |
| <img src="nugget_icons/icon_url_upload_historic.svg" width="40" height="40" alt="" /> | `URL_UPLOAD_HISTORIC` | Historic URL (Accepts Uploads) | DESCRIPTOR | `#F59E0B` | `icon_url_upload_historic.svg` |
| <img src="nugget_icons/icon_username.svg" width="40" height="40" alt="" /> | `USERNAME` | Username | ENTITY | `#3B82F6` | `icon_username.svg` |
| <img src="nugget_icons/icon_vpn_host.svg" width="40" height="40" alt="" /> | `VPN_HOST` | VPN Host | DESCRIPTOR | `#F59E0B` | `icon_vpn_host.svg` |
| <img src="nugget_icons/icon_vulnerability_disclosure.svg" width="40" height="40" alt="" /> | `VULNERABILITY_DISCLOSURE` | Vulnerability - Third Party Disclosure | DESCRIPTOR | `#F59E0B` | `icon_vulnerability_disclosure.svg` |
| <img src="nugget_icons/icon_vulnerability_cve_critical.svg" width="40" height="40" alt="" /> | `VULNERABILITY_CVE_CRITICAL` | Vulnerability - CVE Critical | DESCRIPTOR | `#F59E0B` | `icon_vulnerability_cve_critical.svg` |
| <img src="nugget_icons/icon_vulnerability_cve_high.svg" width="40" height="40" alt="" /> | `VULNERABILITY_CVE_HIGH` | Vulnerability - CVE High | DESCRIPTOR | `#F59E0B` | `icon_vulnerability_cve_high.svg` |
| <img src="nugget_icons/icon_vulnerability_cve_medium.svg" width="40" height="40" alt="" /> | `VULNERABILITY_CVE_MEDIUM` | Vulnerability - CVE Medium | DESCRIPTOR | `#F59E0B` | `icon_vulnerability_cve_medium.svg` |
| <img src="nugget_icons/icon_vulnerability_cve_low.svg" width="40" height="40" alt="" /> | `VULNERABILITY_CVE_LOW` | Vulnerability - CVE Low | DESCRIPTOR | `#F59E0B` | `icon_vulnerability_cve_low.svg` |
| <img src="nugget_icons/icon_vulnerability_general.svg" width="40" height="40" alt="" /> | `VULNERABILITY_GENERAL` | Vulnerability - General | DESCRIPTOR | `#F59E0B` | `icon_vulnerability_general.svg` |
| <img src="nugget_icons/icon_web_analytics_id.svg" width="40" height="40" alt="" /> | `WEB_ANALYTICS_ID` | Web Analytics | ENTITY | `#3B82F6` | `icon_web_analytics_id.svg` |
| <img src="nugget_icons/icon_webserver_banner.svg" width="40" height="40" alt="" /> | `WEBSERVER_BANNER` | Web Server | DATA | `#14B8A6` | `icon_webserver_banner.svg` |
| <img src="nugget_icons/icon_webserver_httpheaders.svg" width="40" height="40" alt="" /> | `WEBSERVER_HTTPHEADERS` | HTTP Headers | DATA | `#14B8A6` | `icon_webserver_httpheaders.svg` |
| <img src="nugget_icons/icon_webserver_strangeheader.svg" width="40" height="40" alt="" /> | `WEBSERVER_STRANGEHEADER` | Non-Standard HTTP Header | DATA | `#14B8A6` | `icon_webserver_strangeheader.svg` |
| <img src="nugget_icons/icon_webserver_technology.svg" width="40" height="40" alt="" /> | `WEBSERVER_TECHNOLOGY` | Web Technology | DESCRIPTOR | `#F59E0B` | `icon_webserver_technology.svg` |
| <img src="nugget_icons/icon_wifi_access_point.svg" width="40" height="40" alt="" /> | `WIFI_ACCESS_POINT` | WiFi Access Point Nearby | ENTITY | `#3B82F6` | `icon_wifi_access_point.svg` |
| <img src="nugget_icons/icon_wikipedia_page_edit.svg" width="40" height="40" alt="" /> | `WIKIPEDIA_PAGE_EDIT` | Wikipedia Page Edit | DESCRIPTOR | `#F59E0B` | `icon_wikipedia_page_edit.svg` |


---

*Generated from Spiderfeet core_nugget_list. Total: 167 nuggets across 5 types.*
