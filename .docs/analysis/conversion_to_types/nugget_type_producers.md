# Nugget type producers (index)

Auto-generated from `analyse_module_conversions.py`. One row per nugget type; modules that declare it in `producedEvents()`.

| Nugget ID | Archetype | Producer count | Modules |
|-----------|-----------|----------------|---------|
| `ACCOUNT_EXTERNAL_OWNED` | ENTITY | 4 | `sfp_accounts`, `sfp_c99`, `sfp_gravatar`, `sfp_sociallinks` |
| `AFFILIATE_COMPANY_NAME` | ENTITY | 1 | `sfp_company` |
| `AFFILIATE_DESCRIPTION_ABSTRACT` | DESCRIPTOR | 1 | `sfp_duckduckgo` |
| `AFFILIATE_DESCRIPTION_CATEGORY` | DESCRIPTOR | 1 | `sfp_duckduckgo` |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | 12 | `sfp_dnsresolve`, `sfp_fsecure_riddler`, `sfp_google_tag_manager`, `sfp_hackertarget`, `sfp_reversewhois`, … (+7) |
| `AFFILIATE_DOMAIN_UNREGISTERED` | ENTITY | 1 | `sfp_jsonwhoiscom` |
| `AFFILIATE_DOMAIN_WHOIS` | DATA | 1 | `sfp_whois` |
| `AFFILIATE_EMAILADDR` | ENTITY | 3 | `sfp_email`, `sfp_pgp`, `sfp_stackoverflow` |
| `AFFILIATE_INTERNET_NAME` | ENTITY | 19 | `sfp_apple_itunes`, `sfp_clearbit`, `sfp_crossref`, `sfp_crxcavator`, `sfp_dnscommonsrv`, … (+14) |
| `AFFILIATE_INTERNET_NAME_HIJACKABLE` | ENTITY | 1 | `sfp_subdomain_takeover` |
| `AFFILIATE_INTERNET_NAME_UNRESOLVED` | ENTITY | 5 | `sfp_crxcavator`, `sfp_dnsraw`, `sfp_fsecure_riddler`, `sfp_fullhunt`, `sfp_hackertarget` |
| `AFFILIATE_IPADDR` | ENTITY | 5 | `sfp_alienvault`, `sfp_dnsneighbor`, `sfp_dnsresolve`, `sfp_opennic`, `sfp_stackoverflow` |
| `AFFILIATE_IPV6_ADDRESS` | ENTITY | 4 | `sfp_alienvault`, `sfp_dnsresolve`, `sfp_opennic`, `sfp_stackoverflow` |
| `AFFILIATE_WEB_CONTENT` | DATA | 1 | `sfp_crossref` |
| `APPSTORE_ENTRY` | ENTITY | 3 | `sfp_apple_itunes`, `sfp_crxcavator`, `sfp_koodous` |
| `BASE64_DATA` | DATA | 1 | `sfp_base64` |
| `BGP_AS_MEMBER` | ENTITY | 5 | `sfp_bgpview`, `sfp_censys`, `sfp_greynoise`, `sfp_ripe`, `sfp_urlscan` |
| `BGP_AS_OWNER` | ENTITY | 1 | `sfp_ripe` |
| `BITCOIN_ADDRESS` | ENTITY | 2 | `sfp_bitcoin`, `sfp_keybase` |
| `BITCOIN_BALANCE` | DESCRIPTOR | 1 | `sfp_blockchain` |
| `BLACKLISTED_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | 17 | `sfp_abusix`, `sfp_adguard_dns`, `sfp_botvrij`, `sfp_cleanbrowsing`, `sfp_cloudflaredns`, … (+12) |
| `BLACKLISTED_AFFILIATE_IPADDR` | DESCRIPTOR | 26 | `sfp_abuseipdb`, `sfp_abusix`, `sfp_alienvaultiprep`, `sfp_blocklistde`, `sfp_cinsscore`, … (+21) |
| `BLACKLISTED_COHOST` | DESCRIPTOR | 17 | `sfp_abusix`, `sfp_adguard_dns`, `sfp_botvrij`, `sfp_cleanbrowsing`, `sfp_cloudflaredns`, … (+12) |
| `BLACKLISTED_INTERNET_NAME` | DESCRIPTOR | 18 | `sfp_abusix`, `sfp_adguard_dns`, `sfp_botvrij`, `sfp_cleanbrowsing`, `sfp_cloudflaredns`, … (+13) |
| `BLACKLISTED_IPADDR` | DESCRIPTOR | 29 | `sfp_abuseipdb`, `sfp_abusix`, `sfp_alienvaultiprep`, `sfp_blocklistde`, `sfp_botscout`, … (+24) |
| `BLACKLISTED_NETBLOCK` | DESCRIPTOR | 19 | `sfp_abusix`, `sfp_alienvaultiprep`, `sfp_blocklistde`, `sfp_cinsscore`, `sfp_cleantalk`, … (+14) |
| `BLACKLISTED_SUBNET` | DESCRIPTOR | 19 | `sfp_abusix`, `sfp_alienvaultiprep`, `sfp_blocklistde`, `sfp_cinsscore`, `sfp_cleantalk`, … (+14) |
| `CLOUD_STORAGE_BUCKET` | ENTITY | 5 | `sfp_azureblobstorage`, `sfp_digitaloceanspace`, `sfp_googleobjectstorage`, `sfp_grayhatwarfare`, `sfp_s3bucket` |
| `CLOUD_STORAGE_BUCKET_OPEN` | DESCRIPTOR | 4 | `sfp_digitaloceanspace`, `sfp_googleobjectstorage`, `sfp_grayhatwarfare`, `sfp_s3bucket` |
| `COMPANY_NAME` | ENTITY | 10 | `sfp_abstractapi`, `sfp_company`, `sfp_gleif`, `sfp_greynoise`, `sfp_greynoise_community`, … (+5) |
| `COUNTRY_NAME` | ENTITY | 1 | `sfp_countryname` |
| `CO_HOSTED_SITE` | ENTITY | 20 | `sfp_alienvault`, `sfp_binaryedge`, `sfp_bingsharedip`, `sfp_builtwith`, `sfp_c99`, … (+15) |
| `CO_HOSTED_SITE_DOMAIN` | ENTITY | 4 | `sfp_certspotter`, `sfp_crt`, `sfp_dnsresolve`, `sfp_sslcert` |
| `CO_HOSTED_SITE_DOMAIN_WHOIS` | DATA | 1 | `sfp_whois` |
| `CREDIT_CARD_NUMBER` | ENTITY | 1 | `sfp_creditcard` |
| `DARKNET_MENTION_CONTENT` | DATA | 4 | `sfp_ahmia`, `sfp_onioncity`, `sfp_onionsearchengine`, `sfp_torch` |
| `DARKNET_MENTION_URL` | DESCRIPTOR | 5 | `sfp_ahmia`, `sfp_intelx`, `sfp_onioncity`, `sfp_onionsearchengine`, `sfp_torch` |
| `DEFACED_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | 1 | `sfp_zoneh` |
| `DEFACED_AFFILIATE_IPADDR` | DESCRIPTOR | 1 | `sfp_zoneh` |
| `DEFACED_COHOST` | DESCRIPTOR | 1 | `sfp_zoneh` |
| `DEFACED_INTERNET_NAME` | DESCRIPTOR | 1 | `sfp_zoneh` |
| `DEFACED_IPADDR` | DESCRIPTOR | 1 | `sfp_zoneh` |
| `DESCRIPTION_ABSTRACT` | DESCRIPTOR | 2 | `sfp_duckduckgo`, `sfp_hostio` |
| `DESCRIPTION_CATEGORY` | DESCRIPTOR | 1 | `sfp_duckduckgo` |
| `DEVICE_TYPE` | DESCRIPTOR | 2 | `sfp_shodan`, `sfp_template` |
| `DNS_SPF` | DATA | 1 | `sfp_dnsraw` |
| `DNS_TEXT` | DATA | 2 | `sfp_dnsdb`, `sfp_dnsraw` |
| `DOMAIN_NAME` | ENTITY | 20 | `sfp_binaryedge`, `sfp_builtwith`, `sfp_certspotter`, `sfp_crt`, `sfp_dnsresolve`, … (+15) |
| `DOMAIN_NAME_PARENT` | ENTITY | 1 | `sfp_dnsresolve` |
| `DOMAIN_REGISTRAR` | ENTITY | 3 | `sfp_jsonwhoiscom`, `sfp_reversewhois`, `sfp_whois` |
| `DOMAIN_WHOIS` | DATA | 2 | `sfp_jsonwhoiscom`, `sfp_whois` |
| `EMAILADDR` | ENTITY | 20 | `sfp_builtwith`, `sfp_clearbit`, `sfp_dehashed`, `sfp_email`, `sfp_emailcrawlr`, … (+15) |
| `EMAILADDR_COMPROMISED` | DESCRIPTOR | 8 | `sfp_abstractapi`, `sfp_binaryedge`, `sfp_citadel`, `sfp_dehashed`, `sfp_emailrep`, … (+3) |
| `EMAILADDR_DELIVERABLE` | DESCRIPTOR | 2 | `sfp_abstractapi`, `sfp_seon` |
| `EMAILADDR_DISPOSABLE` | DESCRIPTOR | 5 | `sfp_abstractapi`, `sfp_debounce`, `sfp_ipqualityscore`, `sfp_nameapi`, `sfp_trumail` |
| `EMAILADDR_GENERIC` | ENTITY | 16 | `sfp_builtwith`, `sfp_clearbit`, `sfp_email`, `sfp_emailcrawlr`, `sfp_emailformat`, … (+11) |
| `EMAILADDR_UNDELIVERABLE` | DESCRIPTOR | 2 | `sfp_abstractapi`, `sfp_seon` |
| `ERROR_MESSAGE` | DATA | 1 | `sfp_errors` |
| `ETHEREUM_ADDRESS` | ENTITY | 1 | `sfp_ethereum` |
| `ETHEREUM_BALANCE` | DESCRIPTOR | 1 | `sfp_etherscan` |
| `GEOINFO` | DESCRIPTOR | 34 | `sfp_abstractapi`, `sfp_c99`, `sfp_callername`, `sfp_censys`, `sfp_emailcrawlr`, … (+29) |
| `HASH` | DATA | 1 | `sfp_hashes` |
| `HASH_COMPROMISED` | DATA | 1 | `sfp_dehashed` |
| `HTTP_CODE` | DATA | 1 | `sfp_spider` |
| `HUMAN_NAME` | ENTITY | 6 | `sfp_arin`, `sfp_names`, `sfp_seon`, `sfp_sociallinks`, `sfp_stackoverflow`, … (+1) |
| `IBAN_NUMBER` | ENTITY | 1 | `sfp_iban` |
| `INTERESTING_FILE` | DESCRIPTOR | 1 | `sfp_intfiles` |
| `INTERESTING_FILE_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `INTERNAL_IP_ADDRESS` | ENTITY | 2 | `sfp_dnsresolve`, `sfp_mnemonic` |
| `INTERNET_NAME` | ENTITY | 41 | `sfp_alienvault`, `sfp_apple_itunes`, `sfp_binaryedge`, `sfp_builtwith`, `sfp_c99`, … (+36) |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | 24 | `sfp_alienvault`, `sfp_c99`, `sfp_certspotter`, `sfp_crobat_api`, `sfp_crt`, … (+19) |
| `IPV6_ADDRESS` | ENTITY | 8 | `sfp_alienvault`, `sfp_dnsdb`, `sfp_dnsresolve`, `sfp_mnemonic`, `sfp_networksdb`, … (+3) |
| `IP_ADDRESS` | ENTITY | 26 | `sfp_alienvault`, `sfp_bingsharedip`, `sfp_builtwith`, `sfp_c99`, `sfp_circllu`, … (+21) |
| `JOB_TITLE` | DESCRIPTOR | 1 | `sfp_sociallinks` |
| `JUNK_FILE` | DESCRIPTOR | 1 | `sfp_junkfiles` |
| `LEAKSITE_CONTENT` | DATA | 7 | `sfp_haveibeenpwned`, `sfp_leakix`, `sfp_onyphe`, `sfp_pastebin`, `sfp_psbdmp`, … (+2) |
| `LEAKSITE_URL` | ENTITY | 6 | `sfp_haveibeenpwned`, `sfp_intelx`, `sfp_pastebin`, `sfp_psbdmp`, `sfp_trashpanda`, … (+1) |
| `LEI` | ENTITY | 1 | `sfp_gleif` |
| `LINKED_URL_EXTERNAL` | SUBENTITY | 2 | `sfp_spider`, `sfp_webserver` |
| `LINKED_URL_INTERNAL` | SUBENTITY | 13 | `sfp_alienvault`, `sfp_apple_itunes`, `sfp_bingsearch`, `sfp_commoncrawl`, `sfp_crxcavator`, … (+8) |
| `MALICIOUS_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | 21 | `sfp_abusech`, `sfp_abusix`, `sfp_botvrij`, `sfp_cleanbrowsing`, `sfp_cloudflaredns`, … (+16) |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | 38 | `sfp_abusech`, `sfp_abuseipdb`, `sfp_abusix`, `sfp_alienvault`, `sfp_alienvaultiprep`, … (+33) |
| `MALICIOUS_ASN` | DESCRIPTOR | 1 | `sfp_greynoise` |
| `MALICIOUS_BITCOIN_ADDRESS` | DESCRIPTOR | 2 | `sfp_bitcoinabuse`, `sfp_bitcoinwhoswho` |
| `MALICIOUS_COHOST` | DESCRIPTOR | 21 | `sfp_abusech`, `sfp_abusix`, `sfp_botvrij`, `sfp_cleanbrowsing`, `sfp_cloudflaredns`, … (+16) |
| `MALICIOUS_EMAILADDR` | DESCRIPTOR | 5 | `sfp_botscout`, `sfp_emailrep`, `sfp_ipqualityscore`, `sfp_seon`, `sfp_threatcrowd` |
| `MALICIOUS_INTERNET_NAME` | DESCRIPTOR | 24 | `sfp_abusech`, `sfp_abusix`, `sfp_botvrij`, `sfp_cleanbrowsing`, `sfp_cloudflaredns`, … (+19) |
| `MALICIOUS_IPADDR` | DESCRIPTOR | 49 | `sfp_abusech`, `sfp_abuseipdb`, `sfp_abusix`, `sfp_alienvault`, `sfp_alienvaultiprep`, … (+44) |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | 26 | `sfp_abusech`, `sfp_abusix`, `sfp_alienvault`, `sfp_alienvaultiprep`, `sfp_blocklistde`, … (+21) |
| `MALICIOUS_PHONE_NUMBER` | DESCRIPTOR | 3 | `sfp_callername`, `sfp_ipqualityscore`, `sfp_seon` |
| `MALICIOUS_SUBNET` | DESCRIPTOR | 24 | `sfp_abusech`, `sfp_abusix`, `sfp_alienvaultiprep`, `sfp_blocklistde`, `sfp_cinsscore`, … (+19) |
| `NETBLOCKV6_MEMBER` | ENTITY | 3 | `sfp_bgpview`, `sfp_censys`, `sfp_ripe` |
| `NETBLOCKV6_OWNER` | ENTITY | 1 | `sfp_ripe` |
| `NETBLOCK_MEMBER` | ENTITY | 4 | `sfp_bgpview`, `sfp_censys`, `sfp_networksdb`, `sfp_ripe` |
| `NETBLOCK_OWNER` | ENTITY | 2 | `sfp_ripe`, `sfp_riskiq` |
| `NETBLOCK_WHOIS` | DATA | 1 | `sfp_whois` |
| `OPERATING_SYSTEM` | DESCRIPTOR | 7 | `sfp_censys`, `sfp_greynoise`, `sfp_leakix`, `sfp_shodan`, `sfp_template`, … (+2) |
| `PASSWORD_COMPROMISED` | DATA | 3 | `sfp_dehashed`, `sfp_tool_trufflehog`, `sfp_trashpanda` |
| `PGP_KEY` | DATA | 2 | `sfp_keybase`, `sfp_pgp` |
| `PHONE_NUMBER` | ENTITY | 9 | `sfp_builtwith`, `sfp_clearbit`, `sfp_emailcrawlr`, `sfp_fullcontact`, `sfp_gravatar`, … (+4) |
| `PHONE_NUMBER_COMPROMISED` | DESCRIPTOR | 1 | `sfp_haveibeenpwned` |
| `PHONE_NUMBER_TYPE` | DESCRIPTOR | 3 | `sfp_ipqualityscore`, `sfp_seon`, `sfp_textmagic` |
| `PHYSICAL_ADDRESS` | ENTITY | 9 | `sfp_bgpview`, `sfp_c99`, `sfp_clearbit`, `sfp_crxcavator`, `sfp_fullcontact`, … (+4) |
| `PHYSICAL_COORDINATES` | ENTITY | 8 | `sfp_abstractapi`, `sfp_c99`, `sfp_fsecure_riddler`, `sfp_googlemaps`, `sfp_hostio`, … (+3) |
| `PROVIDER_DNS` | ENTITY | 6 | `sfp_c99`, `sfp_dnsdb`, `sfp_dnsraw`, `sfp_fullhunt`, `sfp_jsonwhoiscom`, … (+1) |
| `PROVIDER_HOSTING` | ENTITY | 3 | `sfp_c99`, `sfp_hosting`, `sfp_securitytrails` |
| `PROVIDER_JAVASCRIPT` | ENTITY | 1 | `sfp_pageinfo` |
| `PROVIDER_MAIL` | ENTITY | 3 | `sfp_dnsdb`, `sfp_dnsraw`, `sfp_fullhunt` |
| `PROVIDER_TELCO` | ENTITY | 5 | `sfp_abstractapi`, `sfp_c99`, `sfp_numverify`, `sfp_phone`, `sfp_seon` |
| `PROXY_HOST` | DESCRIPTOR | 5 | `sfp_dronebl`, `sfp_focsec`, `sfp_neutrinoapi`, `sfp_seon`, `sfp_sorbs` |
| `PUBLIC_CODE_REPO` | ENTITY | 2 | `sfp_github`, `sfp_searchcode` |
| `RAW_DNS_RECORDS` | DATA | 3 | `sfp_dnsraw`, `sfp_dnszonexfer`, `sfp_hackertarget` |
| `RAW_FILE_META_DATA` | DATA | 2 | `sfp_binstring`, `sfp_filemeta` |
| `RAW_RIR_DATA` | DATA | 80 | `sfp_abstractapi`, `sfp_apple_itunes`, `sfp_arin`, `sfp_bgpview`, `sfp_bingsearch`, … (+75) |
| `SIMILARDOMAIN` | ENTITY | 3 | `sfp_similar`, `sfp_tldsearch`, `sfp_tool_dnstwist` |
| `SIMILARDOMAIN_WHOIS` | DATA | 1 | `sfp_whois` |
| `SIMILAR_ACCOUNT_EXTERNAL` | ENTITY | 1 | `sfp_accounts` |
| `SOCIAL_MEDIA` | ENTITY | 8 | `sfp_abstractapi`, `sfp_gravatar`, `sfp_keybase`, `sfp_myspace`, `sfp_seon`, … (+3) |
| `SOFTWARE_USED` | SUBENTITY | 5 | `sfp_censys`, `sfp_filemeta`, `sfp_leakix`, `sfp_tool_wappalyzer`, `sfp_zonefiles` |
| `SSL_CERTIFICATE_EXPIRED` | DESCRIPTOR | 2 | `sfp_certspotter`, `sfp_sslcert` |
| `SSL_CERTIFICATE_EXPIRING` | DESCRIPTOR | 2 | `sfp_certspotter`, `sfp_sslcert` |
| `SSL_CERTIFICATE_ISSUED` | ENTITY | 3 | `sfp_certspotter`, `sfp_circllu`, `sfp_sslcert` |
| `SSL_CERTIFICATE_ISSUER` | ENTITY | 2 | `sfp_certspotter`, `sfp_sslcert` |
| `SSL_CERTIFICATE_MISMATCH` | DESCRIPTOR | 2 | `sfp_certspotter`, `sfp_sslcert` |
| `SSL_CERTIFICATE_RAW` | DATA | 3 | `sfp_certspotter`, `sfp_crt`, `sfp_sslcert` |
| `TARGET_WEB_CONTENT` | DATA | 1 | `sfp_spider` |
| `TARGET_WEB_CONTENT_TYPE` | DESCRIPTOR | 1 | `sfp_spider` |
| `TARGET_WEB_COOKIE` | DATA | 1 | `sfp_cookie` |
| `TCP_PORT_OPEN` | SUBENTITY | 10 | `sfp_binaryedge`, `sfp_censys`, `sfp_fullhunt`, `sfp_leakix`, `sfp_portscan_tcp`, … (+5) |
| `TCP_PORT_OPEN_BANNER` | DATA | 5 | `sfp_binaryedge`, `sfp_censys`, `sfp_portscan_tcp`, `sfp_shodan`, `sfp_template` |
| `TOR_EXIT_NODE` | DESCRIPTOR | 4 | `sfp_focsec`, `sfp_neutrinoapi`, `sfp_seon`, `sfp_torexits` |
| `UDP_PORT_OPEN` | SUBENTITY | 4 | `sfp_binaryedge`, `sfp_censys`, `sfp_tool_nbtscan`, `sfp_tool_onesixtyone` |
| `UDP_PORT_OPEN_INFO` | DATA | 3 | `sfp_binaryedge`, `sfp_tool_nbtscan`, `sfp_tool_onesixtyone` |
| `URL_ADBLOCKED_EXTERNAL` | DESCRIPTOR | 1 | `sfp_adblock` |
| `URL_ADBLOCKED_INTERNAL` | DESCRIPTOR | 1 | `sfp_adblock` |
| `URL_FLASH` | DESCRIPTOR | 1 | `sfp_pageinfo` |
| `URL_FLASH_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `URL_FORM` | DESCRIPTOR | 1 | `sfp_pageinfo` |
| `URL_FORM_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `URL_JAVASCRIPT` | DESCRIPTOR | 1 | `sfp_pageinfo` |
| `URL_JAVASCRIPT_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `URL_JAVA_APPLET` | DESCRIPTOR | 1 | `sfp_pageinfo` |
| `URL_JAVA_APPLET_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `URL_PASSWORD` | DESCRIPTOR | 1 | `sfp_pageinfo` |
| `URL_PASSWORD_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `URL_STATIC` | DESCRIPTOR | 1 | `sfp_pageinfo` |
| `URL_STATIC_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `URL_UPLOAD` | DESCRIPTOR | 1 | `sfp_pageinfo` |
| `URL_UPLOAD_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `URL_WEB_FRAMEWORK` | DESCRIPTOR | 1 | `sfp_webframework` |
| `URL_WEB_FRAMEWORK_HISTORIC` | DESCRIPTOR | 1 | `sfp_archiveorg` |
| `USERNAME` | ENTITY | 6 | `sfp_accounts`, `sfp_c99`, `sfp_gravatar`, `sfp_keybase`, `sfp_social`, … (+1) |
| `VPN_HOST` | DESCRIPTOR | 4 | `sfp_dronebl`, `sfp_focsec`, `sfp_neutrinoapi`, `sfp_seon` |
| `VULNERABILITY_CVE_CRITICAL` | DESCRIPTOR | 7 | `sfp_binaryedge`, `sfp_onyphe`, `sfp_shodan`, `sfp_tool_nuclei`, `sfp_tool_retirejs`, … (+2) |
| `VULNERABILITY_CVE_HIGH` | DESCRIPTOR | 7 | `sfp_binaryedge`, `sfp_onyphe`, `sfp_shodan`, `sfp_tool_nuclei`, `sfp_tool_retirejs`, … (+2) |
| `VULNERABILITY_CVE_LOW` | DESCRIPTOR | 7 | `sfp_binaryedge`, `sfp_onyphe`, `sfp_shodan`, `sfp_tool_nuclei`, `sfp_tool_retirejs`, … (+2) |
| `VULNERABILITY_CVE_MEDIUM` | DESCRIPTOR | 7 | `sfp_binaryedge`, `sfp_onyphe`, `sfp_shodan`, `sfp_tool_nuclei`, `sfp_tool_retirejs`, … (+2) |
| `VULNERABILITY_DISCLOSURE` | DESCRIPTOR | 2 | `sfp_h1nobbdde`, `sfp_openbugbounty` |
| `VULNERABILITY_GENERAL` | DESCRIPTOR | 9 | `sfp_binaryedge`, `sfp_onyphe`, `sfp_punkspider`, `sfp_shodan`, `sfp_template`, … (+4) |
| `WEBSERVER_BANNER` | DATA | 4 | `sfp_leakix`, `sfp_tool_whatweb`, `sfp_urlscan`, `sfp_webserver` |
| `WEBSERVER_HTTPHEADERS` | DATA | 3 | `sfp_censys`, `sfp_hackertarget`, `sfp_spider` |
| `WEBSERVER_STRANGEHEADER` | DATA | 1 | `sfp_strangeheaders` |
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | 11 | `sfp_builtwith`, `sfp_c99`, `sfp_hostio`, `sfp_seon`, `sfp_tool_cmseek`, … (+6) |
| `WEB_ANALYTICS_ID` | ENTITY | 4 | `sfp_builtwith`, `sfp_hostio`, `sfp_spyonweb`, `sfp_webanalytics` |
| `WIFI_ACCESS_POINT` | ENTITY | 1 | `sfp_wigle` |
| `WIKIPEDIA_PAGE_EDIT` | DESCRIPTOR | 1 | `sfp_wikipediaedits` |