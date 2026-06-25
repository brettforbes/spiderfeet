# Nugget Inventory

Central inventory mapping TypeQL entity names to `nugget_id`, descriptions, and scan variable names.

**Sources:** `.seed/spiderfeet_map.tql` · `.docs/analysis/nuggets.json`

**Scan Variable Name** — field or path in CLI scan output when mapping to this nugget. Fill in incrementally; only obvious mappings are pre-filled.

---

## Current entities (`nugget_type`: ENTITY or SUBENTITY)

| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |
|--------------------|-----------|-------------------|-------------------|
| account-external-owned | ACCOUNT_EXTERNAL_OWNED | Account on External Site |  |
| affiliate-company-name | AFFILIATE_COMPANY_NAME | Affiliate - Company Name |  |
| affiliate-domain-name | AFFILIATE_DOMAIN_NAME | Affiliate - Domain Name |  |
| affiliate-domain-unregistered | AFFILIATE_DOMAIN_UNREGISTERED | Affiliate - Domain Name Unregistered |  |
| affiliate-emailaddr | AFFILIATE_EMAILADDR | Affiliate - Email Address |  |
| affiliate-internet-name | AFFILIATE_INTERNET_NAME | Affiliate - Internet Name |  |
| affiliate-internet-name-hijackable | AFFILIATE_INTERNET_NAME_HIJACKABLE | Affiliate - Internet Name Hijackable |  |
| affiliate-internet-name-unresolved | AFFILIATE_INTERNET_NAME_UNRESOLVED | Affiliate - Internet Name - Unresolved |  |
| affiliate-ipaddr | AFFILIATE_IPADDR | Affiliate - IP Address |  |
| affiliate-ipv6-address | AFFILIATE_IPV6_ADDRESS | Affiliate - IPv6 Address |  |
| appstore-entry | APPSTORE_ENTRY | App Store Entry |  |
| bgp-as-member | BGP_AS_MEMBER | BGP AS Membership |  |
| bgp-as-owner | BGP_AS_OWNER | BGP AS Ownership |  |
| bitcoin-address | BITCOIN_ADDRESS | Bitcoin Address |  |
| cloud-storage-bucket | CLOUD_STORAGE_BUCKET | Cloud Storage Bucket |  |
| company-name | COMPANY_NAME | Company Name |  |
| country-name | COUNTRY_NAME | Country Name |  |
| co-hosted-site | CO_HOSTED_SITE | Co-Hosted Site |  |
| co-hosted-site-domain | CO_HOSTED_SITE_DOMAIN | Co-Hosted Site - Domain Name |  |
| credit-card-number | CREDIT_CARD_NUMBER | Credit Card Number |  |
| date-human-dob | DATE_HUMAN_DOB | Date of Birth |  |
| domain-name | DOMAIN_NAME | Domain Name | domain |
| domain-name-parent | DOMAIN_NAME_PARENT | Domain Name (Parent) |  |
| domain-registrar | DOMAIN_REGISTRAR | Domain Registrar |  |
| emailaddr | EMAILADDR | Email Address | email |
| emailaddr-generic | EMAILADDR_GENERIC | Email Address - Generic |  |
| ethereum-address | ETHEREUM_ADDRESS | Ethereum Address |  |
| human-name | HUMAN_NAME | Human Name |  |
| iban-number | IBAN_NUMBER | IBAN Number |  |
| internal-ip-address | INTERNAL_IP_ADDRESS | IP Address - Internal Network |  |
| internet-name | INTERNET_NAME | Internet Name | hostname |
| internet-name-unresolved | INTERNET_NAME_UNRESOLVED | Internet Name - Unresolved |  |
| ipv6-address | IPV6_ADDRESS | IPv6 Address | ipv6 |
| ip-address | IP_ADDRESS | IP Address | ip |
| leaksite-url | LEAKSITE_URL | Leak Site URL |  |
| lei | LEI | Legal Entity Identifier |  |
| linked-url-external | LINKED_URL_EXTERNAL | Linked URL - External |  |
| linked-url-internal | LINKED_URL_INTERNAL | Linked URL - Internal |  |
| netblockv6-member | NETBLOCKV6_MEMBER | Netblock IPv6 Membership |  |
| netblockv6-owner | NETBLOCKV6_OWNER | Netblock IPv6 Ownership |  |
| netblock-member | NETBLOCK_MEMBER | Netblock Membership |  |
| netblock-owner | NETBLOCK_OWNER | Netblock Ownership |  |
| phone-number | PHONE_NUMBER | Phone Number |  |
| physical-address | PHYSICAL_ADDRESS | Physical Address |  |
| physical-coordinates | PHYSICAL_COORDINATES | Physical Coordinates |  |
| provider-dns | PROVIDER_DNS | Name Server (DNS NS Records) |  |
| provider-hosting | PROVIDER_HOSTING | Hosting Provider |  |
| provider-javascript | PROVIDER_JAVASCRIPT | Externally Hosted Javascript |  |
| provider-mail | PROVIDER_MAIL | Email Gateway (DNS MX Records) |  |
| provider-telco | PROVIDER_TELCO | Telecommunications Provider |  |
| public-code-repo | PUBLIC_CODE_REPO | Public Code Repository |  |
| similardomain | SIMILARDOMAIN | Similar Domain |  |
| similar-account-external | SIMILAR_ACCOUNT_EXTERNAL | Similar Account on External Site |  |
| social-media | SOCIAL_MEDIA | Social Media Presence |  |
| software-used | SOFTWARE_USED | Software Used | product |
| ssl-certificate-issued | SSL_CERTIFICATE_ISSUED | SSL Certificate - Issued to |  |
| ssl-certificate-issuer | SSL_CERTIFICATE_ISSUER | SSL Certificate - Issued by |  |
| tcp-port-open | TCP_PORT_OPEN | Open TCP Port | port |
| udp-port-open | UDP_PORT_OPEN | Open UDP Port | udp_port |
| username | USERNAME | Username |  |
| web-analytics-id | WEB_ANALYTICS_ID | Web Analytics |  |
| wifi-access-point | WIFI_ACCESS_POINT | WiFi Access Point Nearby |  |

---

## Current descriptors (`nugget_type`: DESCRIPTOR or DATA)

| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |
|--------------------|-----------|-------------------|-------------------|
| account-external-owned-compromised | ACCOUNT_EXTERNAL_OWNED_COMPROMISED | Hacked Account on External Site |  |
| account-external-user-shared-compromised | ACCOUNT_EXTERNAL_USER_SHARED_COMPROMISED | Hacked User Account on External Site |  |
| affiliate-description-abstract | AFFILIATE_DESCRIPTION_ABSTRACT | Affiliate Description - Abstract |  |
| affiliate-description-category | AFFILIATE_DESCRIPTION_CATEGORY | Affiliate Description - Category |  |
| affiliate-domain-whois | AFFILIATE_DOMAIN_WHOIS | Affiliate - Domain Whois |  |
| affiliate-web-content | AFFILIATE_WEB_CONTENT | Affiliate - Web Content |  |
| base64-data | BASE64_DATA | Base64-encoded Data |  |
| bitcoin-balance | BITCOIN_BALANCE | Bitcoin Balance |  |
| blacklisted-affiliate-internet-name | BLACKLISTED_AFFILIATE_INTERNET_NAME | Blacklisted Affiliate Internet Name |  |
| blacklisted-affiliate-ipaddr | BLACKLISTED_AFFILIATE_IPADDR | Blacklisted Affiliate IP Address |  |
| blacklisted-cohost | BLACKLISTED_COHOST | Blacklisted Co-Hosted Site |  |
| blacklisted-internet-name | BLACKLISTED_INTERNET_NAME | Blacklisted Internet Name |  |
| blacklisted-ipaddr | BLACKLISTED_IPADDR | Blacklisted IP Address |  |
| blacklisted-netblock | BLACKLISTED_NETBLOCK | Blacklisted IP on Owned Netblock |  |
| blacklisted-subnet | BLACKLISTED_SUBNET | Blacklisted IP on Same Subnet |  |
| cloud-storage-bucket-open | CLOUD_STORAGE_BUCKET_OPEN | Cloud Storage Bucket Open |  |
| co-hosted-site-domain-whois | CO_HOSTED_SITE_DOMAIN_WHOIS | Co-Hosted Site - Domain Whois |  |
| darknet-mention-content | DARKNET_MENTION_CONTENT | Darknet Mention Web Content |  |
| darknet-mention-url | DARKNET_MENTION_URL | Darknet Mention URL |  |
| defaced-affiliate-internet-name | DEFACED_AFFILIATE_INTERNET_NAME | Defaced Affiliate |  |
| defaced-affiliate-ipaddr | DEFACED_AFFILIATE_IPADDR | Defaced Affiliate IP Address |  |
| defaced-cohost | DEFACED_COHOST | Defaced Co-Hosted Site |  |
| defaced-internet-name | DEFACED_INTERNET_NAME | Defaced |  |
| defaced-ipaddr | DEFACED_IPADDR | Defaced IP Address |  |
| description-abstract | DESCRIPTION_ABSTRACT | Description - Abstract |  |
| description-category | DESCRIPTION_CATEGORY | Description - Category |  |
| device-type | DEVICE_TYPE | Device Type |  |
| dns-spf | DNS_SPF | DNS SPF Record |  |
| dns-srv | DNS_SRV | DNS SRV Record |  |
| dns-text | DNS_TEXT | DNS TXT Record |  |
| domain-whois | DOMAIN_WHOIS | Domain Whois |  |
| emailaddr-compromised | EMAILADDR_COMPROMISED | Hacked Email Address |  |
| emailaddr-deliverable | EMAILADDR_DELIVERABLE | Deliverable Email Address |  |
| emailaddr-disposable | EMAILADDR_DISPOSABLE | Disposable Email Address |  |
| emailaddr-undeliverable | EMAILADDR_UNDELIVERABLE | Undeliverable Email Address |  |
| error-message | ERROR_MESSAGE | Error Message | error |
| ethereum-balance | ETHEREUM_BALANCE | Ethereum Balance |  |
| geoinfo | GEOINFO | Physical Location |  |
| hash | HASH | Hash |  |
| hash-compromised | HASH_COMPROMISED | Compromised Password Hash |  |
| http-code | HTTP_CODE | HTTP Status Code | http_code |
| interesting-file | INTERESTING_FILE | Interesting File |  |
| interesting-file-historic | INTERESTING_FILE_HISTORIC | Historic Interesting File |  |
| job-title | JOB_TITLE | Job Title |  |
| junk-file | JUNK_FILE | Junk File |  |
| leaksite-content | LEAKSITE_CONTENT | Leak Site Content |  |
| malicious-affiliate-internet-name | MALICIOUS_AFFILIATE_INTERNET_NAME | Malicious Affiliate |  |
| malicious-affiliate-ipaddr | MALICIOUS_AFFILIATE_IPADDR | Malicious Affiliate IP Address |  |
| malicious-asn | MALICIOUS_ASN | Malicious AS |  |
| malicious-bitcoin-address | MALICIOUS_BITCOIN_ADDRESS | Malicious Bitcoin Address |  |
| malicious-cohost | MALICIOUS_COHOST | Malicious Co-Hosted Site |  |
| malicious-emailaddr | MALICIOUS_EMAILADDR | Malicious E-mail Address |  |
| malicious-internet-name | MALICIOUS_INTERNET_NAME | Malicious Internet Name |  |
| malicious-ipaddr | MALICIOUS_IPADDR | Malicious IP Address |  |
| malicious-netblock | MALICIOUS_NETBLOCK | Malicious IP on Owned Netblock |  |
| malicious-phone-number | MALICIOUS_PHONE_NUMBER | Malicious Phone Number |  |
| malicious-subnet | MALICIOUS_SUBNET | Malicious IP on Same Subnet |  |
| netblock-whois | NETBLOCK_WHOIS | Netblock Whois |  |
| operating-system | OPERATING_SYSTEM | Operating System | os |
| password-compromised | PASSWORD_COMPROMISED | Compromised Password |  |
| pgp-key | PGP_KEY | PGP Public Key |  |
| phone-number-compromised | PHONE_NUMBER_COMPROMISED | Phone Number Compromised |  |
| phone-number-type | PHONE_NUMBER_TYPE | Phone Number Type |  |
| proxy-host | PROXY_HOST | Proxy Host |  |
| raw-dns-records | RAW_DNS_RECORDS | Raw DNS Records |  |
| raw-file-meta-data | RAW_FILE_META_DATA | Raw File Meta Data |  |
| raw-rir-data | RAW_RIR_DATA | Raw Data from RIRs/APIs |  |
| search-engine-web-content | SEARCH_ENGINE_WEB_CONTENT | Search Engine Web Content |  |
| similardomain-whois | SIMILARDOMAIN_WHOIS | Similar Domain - Whois |  |
| ssl-certificate-expired | SSL_CERTIFICATE_EXPIRED | SSL Certificate Expired |  |
| ssl-certificate-expiring | SSL_CERTIFICATE_EXPIRING | SSL Certificate Expiring |  |
| ssl-certificate-mismatch | SSL_CERTIFICATE_MISMATCH | SSL Certificate Host Mismatch |  |
| ssl-certificate-raw | SSL_CERTIFICATE_RAW | SSL Certificate - Raw Data |  |
| target-web-content | TARGET_WEB_CONTENT | Web Content |  |
| target-web-content-type | TARGET_WEB_CONTENT_TYPE | Web Content Type |  |
| target-web-cookie | TARGET_WEB_COOKIE | Cookies |  |
| tcp-port-open-banner | TCP_PORT_OPEN_BANNER | Open TCP Port Banner |  |
| tor-exit-node | TOR_EXIT_NODE | TOR Exit Node |  |
| udp-port-open-info | UDP_PORT_OPEN_INFO | Open UDP Port Information |  |
| url-adblocked-external | URL_ADBLOCKED_EXTERNAL | URL (AdBlocked External) |  |
| url-adblocked-internal | URL_ADBLOCKED_INTERNAL | URL (AdBlocked Internal) |  |
| url-flash | URL_FLASH | URL (Uses Flash) |  |
| url-flash-historic | URL_FLASH_HISTORIC | Historic URL (Uses Flash) |  |
| url-form | URL_FORM | URL (Form) |  |
| url-form-historic | URL_FORM_HISTORIC | Historic URL (Form) |  |
| url-javascript | URL_JAVASCRIPT | URL (Uses Javascript) |  |
| url-javascript-historic | URL_JAVASCRIPT_HISTORIC | Historic URL (Uses Javascript) |  |
| url-java-applet | URL_JAVA_APPLET | URL (Uses Java Applet) |  |
| url-java-applet-historic | URL_JAVA_APPLET_HISTORIC | Historic URL (Uses Java Applet) |  |
| url-password | URL_PASSWORD | URL (Accepts Passwords) |  |
| url-password-historic | URL_PASSWORD_HISTORIC | Historic URL (Accepts Passwords) |  |
| url-static | URL_STATIC | URL (Purely Static) |  |
| url-static-historic | URL_STATIC_HISTORIC | Historic URL (Purely Static) |  |
| url-upload | URL_UPLOAD | URL (Accepts Uploads) |  |
| url-upload-historic | URL_UPLOAD_HISTORIC | Historic URL (Accepts Uploads) |  |
| url-web-framework | URL_WEB_FRAMEWORK | URL (Uses a Web Framework) |  |
| url-web-framework-historic | URL_WEB_FRAMEWORK_HISTORIC | Historic URL (Uses a Web Framework) |  |
| vpn-host | VPN_HOST | VPN Host |  |
| vulnerability-cve-critical | VULNERABILITY_CVE_CRITICAL | Vulnerability - CVE Critical |  |
| vulnerability-cve-high | VULNERABILITY_CVE_HIGH | Vulnerability - CVE High |  |
| vulnerability-cve-low | VULNERABILITY_CVE_LOW | Vulnerability - CVE Low |  |
| vulnerability-cve-medium | VULNERABILITY_CVE_MEDIUM | Vulnerability - CVE Medium |  |
| vulnerability-disclosure | VULNERABILITY_DISCLOSURE | Vulnerability - Third Party Disclosure |  |
| vulnerability-general | VULNERABILITY_GENERAL | Vulnerability - General |  |
| webserver-banner | WEBSERVER_BANNER | Web Server |  |
| webserver-httpheaders | WEBSERVER_HTTPHEADERS | HTTP Headers |  |
| webserver-strangeheader | WEBSERVER_STRANGEHEADER | Non-Standard HTTP Header |  |
| webserver-technology | WEBSERVER_TECHNOLOGY | Web Technology | technology |
| wikipedia-page-edit | WIKIPEDIA_PAGE_EDIT | Wikipedia Page Edit |  |

---

## Internal (excluded from entity/descriptor tables)

| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |
|--------------------|-----------|-------------------|-------------------|
| root | ROOT | Internal SpiderFeet Root event |  |

---

## Proposed new entities (to fill in)

| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |
|--------------------|-----------|-------------------|-------------------|
| scan | SCAN | Generic Scan entity placeholder - graph collection head | |
| system | SYSTEM | Generic System entity placeholder - graph entity head | |
| host | HOST |  Host with Operating System - graph entity head | |
| device | DEVICE |  Device either on the network or running the network - graph entity head | |
| mobile | MOBILE |  iPhone, Android, iPad etc. - graph entity head | |
| applications | APPLICATIONS | Generic Category for Applications installed on the system | |
| service | SERVICE | Generic Service running on the system | |
| processes | PROCESSES | Generic Category for Processes running on the system | |
| network | NETWORK | Generic Category for Networks | |
| network-adapter | NETWORK_ADAPTER | Generic Network Adapter | |
| port | PORT | Generic Port | |

---

## Proposed new descriptors (to fill in)

| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |
|--------------------|-----------|-------------------|-------------------|
| tag | TAG | Tag descriptor placeholder | |


---

## Proposed Internal (excluded from entity/descriptor tables)

| TypeQL Entity Name | nugget_id | nugget_description | Scan Variable Name |
|--------------------|-----------|-------------------|-------------------|
| clean-miss | CLEAN_MISS | Internal SpiderFeet Root `clean-miss` event from a negative fixture |  |
