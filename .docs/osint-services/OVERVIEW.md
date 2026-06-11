# OSINT services overview

Operator reference for all modules in `osint_services.json`. Per-module detail: [`modules/`](modules/).

**Total services:** 231

## Collections

| Collection | Description |
|------------|-------------|
| [Positive API services](#positive-api-services) | External OSINT APIs expecting produced nuggets |
| [Negative API services](#negative-api-services) | External APIs with clean-miss / reputation style fixtures |
| [Local](#local) | In-process logic (DNS, extractors, WHOIS) — no declared third-party OSINT API |
| [CLI tools](#cli-tools) | External CLI wrappers (`sfp_tool_*`) |
| [Other](#other) | Error state or unclassified |

## Positive API services

| Module | Name | Tier | State | Test |
|--------|------|------|-------|------|
| `sfp_abstractapi` | AbstractAPI | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_ahmia` | Ahmia | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_apple_itunes` | Apple iTunes | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_archiveorg` | Archive.org | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_arin` | ARIN | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_azureblobstorage` | Azure Blob Finder | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_bgpview` | BGPView | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_bingsearch` | Bing | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_bingsharedip` | Bing (Shared IPs) | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_blockchain` | Blockchain | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_builtwith` | BuiltWith | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_c99` | C99 | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_callername` | CallerName | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_censys` | Censys | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_certspotter` | CertSpotter | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_clearbit` | Clearbit | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_crobat_api` | Crobat API | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_crxcavator` | CRXcavator | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_digitaloceanspace` | Digital Ocean Space Finder | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_dnsdb` | DNSDB | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_dnsgrep` | DNSGrep | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_duckduckgo` | DuckDuckGo | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_emailcrawlr` | EmailCrawlr | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_emailformat` | EmailFormat | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_emailrep` | EmailRep | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_etherscan` | Etherscan | free_auth (free_no_auth) | `in-test` | `not-validated` |
| `sfp_focsec` | Focsec | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_fsecure_riddler` | F-Secure Riddler.io | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_fullcontact` | FullContact | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_fullhunt` | FullHunt | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_github` | Github | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_gleif` | GLEIF | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_google_tag_manager` | Google Tag Manager | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_googlemaps` | Google Maps | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_googleobjectstorage` | Google Object Storage Finder | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_googlesearch` | Google | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_gravatar` | Gravatar | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_grep_app` | grep.app | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_hackertarget` | HackerTarget | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_hostio` | Host.io | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_hunter` | Hunter.io | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_intelx` | IntelligenceX | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_ipapico` | ipapi.co | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_ipapicom` | ipapi.com | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_ipinfo` | IPInfo.io | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_ipstack` | ipstack | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_jsonwhoiscom` | JsonWHOIS.com | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_keybase` | Keybase | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_koodous` | Koodous | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_mnemonic` | Mnemonic PassiveDNS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_networksdb` | NetworksDB | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_numverify` | numverify | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_onioncity` | Onion.link | free_auth (free_no_auth) | `in-test` | `not-validated` |
| `sfp_onionsearchengine` | Onionsearchengine.com | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_opencorporates` | OpenCorporates | free_auth (free_no_auth) | `in-test` | `not-validated` |
| `sfp_opennic` | OpenNIC DNS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_openstreetmap` | OpenStreetMap | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_projectdiscovery` | ProjectDiscovery Chaos | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_reversewhois` | ReverseWhois | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_ripe` | RIPE | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_robtex` | Robtex | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_securitytrails` | SecurityTrails | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_seon` | Seon | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_shodan` | SHODAN | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_skymem` | Skymem | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_slideshare` | SlideShare | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_snov` | Snov | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_sociallinks` | Social Links | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_socialprofiles` | Social Media Profile Finder | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_spyonweb` | SpyOnWeb | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_stackoverflow` | StackOverflow | free_auth (free_no_auth) | `in-test` | `not-validated` |
| `sfp_template` | Template Module | free_auth (free_no_auth) | `in-test` | `not-validated` |
| `sfp_textmagic` | TextMagic | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_threatminer` | ThreatMiner | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_torch` | TORCH | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_twilio` | Twilio | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_twitter` | Twitter | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_urlscan` | URLScan.io | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_venmo` | Venmo | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_viewdns` | ViewDNS.info | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_whatcms` | WhatCMS | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_whoisology` | Whoisology | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_whoxy` | Whoxy | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_zetalytics` | Zetalytics | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_zonefiles` | ZoneFile.io | free_auth (free_auth) | `in-test` | `not-validated` |

**Count:** 85

## Negative API services

| Module | Name | Tier | State | Test |
|--------|------|------|-------|------|
| `sfp_abusech` | abuse.ch | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_abuseipdb` | AbuseIPDB | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_abusix` | Abusix Mail Intelligence | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_adblock` | AdBlock Check | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_adguard_dns` | AdGuard DNS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_alienvault` | AlienVault OTX | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_alienvaultiprep` | AlienVault IP Reputation | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_bitcoinabuse` | BitcoinAbuse | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_bitcoinwhoswho` | Bitcoin Who's Who | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_blocklistde` | blocklist.de | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_botscout` | BotScout | free_auth (free_no_auth) | `in-test` | `not-validated` |
| `sfp_botvrij` | botvrij.eu | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_cinsscore` | CINS Army List | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_circllu` | CIRCL.LU | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_citadel` | Leak-Lookup | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_cleanbrowsing` | CleanBrowsing.org | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_cleantalk` | CleanTalk Spam List | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_cloudflaredns` | CloudFlare DNS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_coinblocker` | CoinBlocker Lists | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_comodo` | Comodo Secure DNS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_cybercrimetracker` | CyberCrime-Tracker.net | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_debounce` | Debounce | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_dehashed` | Dehashed | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_dns_for_family` | DNS for Family | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_dronebl` | DroneBL | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_emergingthreats` | Emerging Threats | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_fortinet` | FortiGuard Antispam | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_fraudguard` | Fraudguard | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_googlesafebrowsing` | Google SafeBrowsing | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_grayhatwarfare` | Grayhat Warfare | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_greensnow` | Greensnow | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_greynoise` | GreyNoise | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_greynoise_community` | GreyNoise Community | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_h1nobbdde` | HackerOne (Unofficial) | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_haveibeenpwned` | HaveIBeenPwned | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_honeypot` | Project Honey Pot | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_hybrid_analysis` | Hybrid Analysis | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_iknowwhatyoudownload` | Iknowwhatyoudownload.com | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_ipqualityscore` | IPQualityScore | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_ipregistry` | ipregistry | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_isc` | Internet Storm Center | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_leakix` | LeakIX | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_maltiverse` | Maltiverse | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_malwarepatrol` | MalwarePatrol | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_metadefender` | MetaDefender | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_multiproxy` | multiproxy.org Open Proxies | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_nameapi` | NameAPI | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_neutrinoapi` | NeutrinoAPI | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_onyphe` | Onyphe | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_openbugbounty` | Open Bug Bounty | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_opendns` | OpenDNS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_openphish` | OpenPhish | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_pastebin` | PasteBin | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_phishstats` | PhishStats | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_phishtank` | PhishTank | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_psbdmp` | Psbdmp | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_pulsedive` | Pulsedive | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_punkspider` | PunkSpider | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_quad9` | Quad9 | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_riskiq` | RiskIQ | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_sorbs` | SORBS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_spamcop` | SpamCop | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_spamhaus` | Spamhaus Zen | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_spur` | spur.us | paid_auth (paid) | `in-test` | `not-validated` |
| `sfp_stevenblack_hosts` | Steven Black Hosts | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_surbl` | SURBL | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_talosintel` | Talos Intelligence | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_threatcrowd` | ThreatCrowd | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_threatfox` | ThreatFox | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_threatjammer` | Threat Jammer | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_torexits` | TOR Exit Nodes | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_trashpanda` | Trashpanda | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_trumail` | Trumail | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_uceprotect` | UCEPROTECT | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_virustotal` | VirusTotal | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_voipbl` | VoIP Blacklist (VoIPBL) | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_vxvault` | VXVault.net | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_wigle` | WiGLE | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_wikileaks` | Wikileaks | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_wikipediaedits` | Wikipedia Edits | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_xforce` | XForce Exchange | free_auth (free_auth) | `in-test` | `not-validated` |
| `sfp_yandexdns` | Yandex DNS | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_zoneh` | Zone-H Defacement Check | none (free_no_auth) | `in-test` | `validated-negative` |

**Count:** 83

## Local

| Module | Name | Tier | State | Test |
|--------|------|------|-------|------|
| `sfp_accounts` | Account Finder | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_base64` | Base64 Decoder | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_binstring` | Binary String Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_bitcoin` | Bitcoin Finder | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_company` | Company Name Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_cookie` | Cookie Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_countryname` | Country Name Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_creditcard` | Credit Card Number Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_crossref` | Cross-Referencer | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_customfeed` | Custom Threat Feed | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_dnsbrute` | DNS Brute-forcer | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_dnscommonsrv` | DNS Common SRV | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_dnsneighbor` | DNS Look-aside | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_dnsraw` | DNS Raw Records | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_dnsresolve` | DNS Resolver | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_dnszonexfer` | DNS Zone Transfer | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_email` | E-Mail Address Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_errors` | Error String Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_ethereum` | Ethereum Address Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_filemeta` | File Metadata Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_hashes` | Hash Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_hosting` | Hosting Provider Identifier | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_iban` | IBAN Number Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_intfiles` | Interesting File Finder | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_junkfiles` | Junk File Finder | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_names` | Human Name Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_pageinfo` | Page Information | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_pgp` | PGP Key Servers | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_phone` | Phone Number Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_portscan_tcp` | Port Scanner - TCP | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_similar` | Similar Domain Finder | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_social` | Social Network Identifier | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_spider` | Web Spider | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_sslcert` | SSL Certificate Analyzer | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_strangeheaders` | Strange Header Identifier | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_subdomain_takeover` | Subdomain Takeover Checker | none (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_tldsearch` | TLD Searcher | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_webanalytics` | Web Analytics Extractor | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_webframework` | Web Framework Identifier | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_webserver` | Web Server Identifier | none (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_whois` | Whois | none (free_no_auth) | `in-test` | `validated-positive` |

**Count:** 41

## CLI tools

| Module | Name | Tier | State | Test |
|--------|------|------|-------|------|
| `sfp_tool_cmseek` | Tool - CMSeeK | free_auth (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_tool_dnstwist` | Tool - DNSTwist | free_auth (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_tool_nbtscan` | Tool - nbtscan | free_auth (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_tool_nmap` | Tool - Nmap | free_auth (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_tool_nuclei` | Tool - Nuclei | free_auth (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_tool_onesixtyone` | Tool - onesixtyone | free_auth (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_tool_retirejs` | Tool - Retire.js | free_auth (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_tool_snallygaster` | Tool - snallygaster | free_auth (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_tool_testsslsh` | Tool - testssl.sh | free_auth (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_tool_trufflehog` | Tool - TruffleHog | free_auth (free_no_auth) | `in-test` | `validated-negative` |
| `sfp_tool_wafw00f` | Tool - WAFW00F | free_auth (free_no_auth) | `in-test` | `validated-positive` |
| `sfp_tool_whatweb` | Tool - WhatWeb | free_auth (free_no_auth) | `in-test` | `validated-positive` |

**Count:** 12

## Other

| Module | Name | Tier | State | Test |
|--------|------|------|-------|------|
| `sfp_binaryedge` | BinaryEdge | free_auth (free_auth) | `error` | `not-validated` |
| `sfp_commoncrawl` | CommonCrawl | none (free_no_auth) | `error` | `upstream-blocked` |
| `sfp_crt` | Certificate Transparency | none (free_no_auth) | `error` | `not-validated` |
| `sfp_dnsdumpster` | DNSDumpster | none (free_no_auth) | `error` | `not-validated` |
| `sfp_flickr` | Flickr | none (free_no_auth) | `error` | `upstream-blocked` |
| `sfp_myspace` | MySpace | none (free_no_auth) | `error` | `upstream-blocked` |
| `sfp_s3bucket` | Amazon S3 Bucket Finder | none (free_no_auth) | `error` | `upstream-blocked` |
| `sfp_searchcode` | searchcode | none (free_no_auth) | `error` | `upstream-blocked` |
| `sfp_sublist3r` | Sublist3r PassiveDNS | none (free_no_auth) | `error` | `not-validated` |
| `sfp_tool_wappalyzer` | Tool - Wappalyzer | free_auth (free_no_auth) | `error` | `upstream-blocked` |

**Count:** 10

## Regenerate

```powershell
poetry run python .seed/scripts/fix_catalogue_service_origins.py
poetry run python .seed/scripts/generate_osint_service_docs.py
```
