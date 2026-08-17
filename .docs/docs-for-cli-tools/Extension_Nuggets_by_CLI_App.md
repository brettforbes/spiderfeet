# Extension Nuggets by CLI App

Catalogue of **new / extension** nuggets from `.docs/analysis/nuggets_extension.json`, ordered by CLI app.

Attribution comes from proposed graphs and `*_nugget_graph_structure.md` under `.docs/docs-for-cli-tools/nugget_structure/` for the implemented sub-graphs in [`_Current_Ontology.md`](_Current_Ontology.md).

| Metric | Count |
|--------|------:|
| Extension catalogue | 186 |
| Base catalogue (`nuggets.json`) | 172 |
| Extension-only (not in base) | 184 |
| Attributed to ≥1 implemented CLI app | 160 |
| Shared across ≥2 CLI apps | 24 |

## Shared across CLI apps

| Nugget | Type | Used by |
|--------|------|---------|
| `SCAN_CLI` | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_RECORD` | ENTITY | httpx, Katana, Nerva, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_ELAPSED` | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_EXIT_STATUS` | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nuclei, Pius, Subfinder |
| `SCAN_START` | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TARGET` | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TOOL` | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `IPV4_ADDRESS` | ENTITY | httpx, Nerva, Netdiscover, Nmap, Subfinder |
| `HOST` | ENTITY | httpx, Nerva, Nmap, Nuclei |
| `NETWORKS` | CATEGORY | httpx, Nerva, Netdiscover, Nmap |
| `SERVICE` | ENTITY | httpx, Nerva, Nmap, Nuclei |
| `APPLICATIONS` | CATEGORY | httpx, Nerva, Nmap |
| `HTTP_STATUS_CODE` | DESCRIPTOR | httpx, Katana, Nerva |
| `PORT` | SUBENTITY | httpx, Nerva, Nmap |
| `TRANSPORT` | ENTITY | httpx, Nerva, Nmap |
| `CDN` | ENTITY | httpx, Nerva |
| `CPE_URL` | SUBENTITY | Nerva, Nmap |
| `HTTP_METHOD` | DESCRIPTOR | httpx, Katana |
| `HTTP_TITLE` | DESCRIPTOR | httpx, Nmap |
| `PORT_STATE` | DESCRIPTOR | httpx, Nmap |
| `SCAN_SUMMARY` | DESCRIPTOR | Netdiscover, Nmap |
| `SERVICE_VERSION` | DESCRIPTOR | Nerva, Nmap |
| `SOFTWARE_USED` | SUBENTITY | httpx, Nerva |
| `UPSTREAM_SCENARIO_ID` | DESCRIPTOR | httpx, Katana |

## Nmap

Structure: [`nmap_nugget_graph_structure.md`](nugget_structure/nmap_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `APPLICATIONS` | Applications Category | CATEGORY | httpx, Nerva |
| `CPE_URL` | CPE URL | SUBENTITY | Nerva |
| `DSA` | SSH Key - DSA | SUBENTITY | — |
| `ECDSA` | SSH Key - ECDSA | SUBENTITY | — |
| `EDDSA` | SSH Key - EdDSA | SUBENTITY | — |
| `ENVIRONMENT` | Environment Category | CATEGORY | — |
| `HOP_ORDER` | Trace Hop Order | DESCRIPTOR | — |
| `HOP_RTT` | Trace Hop RTT | DESCRIPTOR | — |
| `HOP_TTL` | Trace Hop TTL | DESCRIPTOR | — |
| `HOST` | Host | ENTITY | httpx, Nerva, Nuclei |
| `HOST_STATUS` | Host Status | DESCRIPTOR | — |
| `HOST_STATUS_REASON` | Host Status Reason | DESCRIPTOR | — |
| `HTTP_TITLE` | HTTP Title | DESCRIPTOR | httpx |
| `IPV4_ADDRESS` | IPv4 Address | ENTITY | httpx, Nerva, Netdiscover, Subfinder |
| `NETWORKS` | Networks Category | CATEGORY | httpx, Nerva, Netdiscover |
| `PORT` | Network Port | SUBENTITY | httpx, Nerva |
| `PORT_PROTOCOL` | Port Protocol | DESCRIPTOR | — |
| `PORT_STATE` | Port State | DESCRIPTOR | httpx |
| `PORT_STATE_REASON` | Port State Reason | DESCRIPTOR | — |
| `RSA` | SSH Key - RSA | SUBENTITY | — |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nuclei, Pius, Subfinder |
| `SCAN_ELAPSED` | Scan Elapsed Time | DESCRIPTOR | httpx, Katana, Nerva, Nuclei, Pius, Subfinder |
| `SCAN_RECORD` | Scan Record | ENTITY | httpx, Katana, Nerva, Netdiscover, Nuclei, Pius, Subfinder |
| `SCAN_START` | Scan Start | DESCRIPTOR | httpx, Katana, Nerva, Nuclei, Pius, Subfinder |
| `SCAN_SUMMARY` | Scan Summary | DESCRIPTOR | Netdiscover |
| `SCAN_TARGET` | Scan Target | DESCRIPTOR | httpx, Katana, Nerva, Nuclei, Pius, Subfinder |
| `SCAN_TOOL` | Scan Tool | DESCRIPTOR | httpx, Katana, Nerva, Nuclei, Pius, Subfinder |
| `SCAN_VERSION` | Scan Version | DESCRIPTOR | — |
| `SERVICE` | Network Service | ENTITY | httpx, Nerva, Nuclei |
| `SERVICE_EXTRAINFO` | Service Extra Information | DESCRIPTOR | — |
| `SERVICE_FINGERPRINT` | Nmap Service Fingerprint | DESCRIPTOR | — |
| `SERVICE_VERSION` | Service Version | DESCRIPTOR | Nerva |
| `SSH_KEY_BITS` | SSH Key Bits | DESCRIPTOR | — |
| `SSH_KEY_KEY` | SSH Public Key | DESCRIPTOR | — |
| `SSH_KEY_TYPE` | SSH Key Type | DESCRIPTOR | — |
| `TRACE` | Trace | ENTITY | — |
| `TRACE_HOP` | Trace Hop | SUBENTITY | — |
| `TRACE_PROTOCOL` | Trace Protocol | DESCRIPTOR | — |
| `TRANSPORT` | Transport Protocol | ENTITY | httpx, Nerva |

## Netdiscover

Structure: [`netdiscover_nugget_graph_structure.md`](nugget_structure/netdiscover_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `IPV4_ADDRESS` | IPv4 Address | ENTITY | httpx, Nerva, Nmap, Subfinder |
| `MAC_VENDOR` | MAC Vendor | DESCRIPTOR | — |
| `NETWORKS` | Networks Category | CATEGORY | httpx, Nerva, Nmap |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_DISCOVERED` | Discovered System Count | DESCRIPTOR | — |
| `SCAN_EMPTY_SCANS` | Empty Scan Count | DESCRIPTOR | — |
| `SCAN_END_TIME` | Scan End Time | DESCRIPTOR | — |
| `SCAN_EXIT_STATUS` | Scan Exit Status | DESCRIPTOR | httpx, Katana, Nerva, Nuclei, Pius, Subfinder |
| `SCAN_RECORD` | Scan Record | ENTITY | httpx, Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_SUMMARY` | Scan Summary | DESCRIPTOR | Nmap |
| `SCAN_TIMESTAMP` | Scan Timestamp | DESCRIPTOR | — |
| `SCAN_TRIES` | Scan Tries | DESCRIPTOR | — |
| `SYSTEM` | System | ENTITY | — |

## Nerva

Structure: [`nerva_nugget_graph_structure.md`](nugget_structure/nerva_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `APPLICATIONS` | Applications Category | CATEGORY | httpx, Nmap |
| `CACHE_STATUS` | Cache Status | DESCRIPTOR | — |
| `CDN` | Content Delivery Network Edge | ENTITY | httpx |
| `CDN_POP_CODE` | CDN Point of Presence Code | DESCRIPTOR | — |
| `CDN_VENDOR` | CDN Vendor | DESCRIPTOR | — |
| `CLASSIFICATION_RULE_FIRED` | Classification Rule Fired | DESCRIPTOR | — |
| `CPE_URL` | CPE URL | SUBENTITY | Nmap |
| `CSP_THIRD_PARTY_DOMAIN` | CSP Third Party Domain | DESCRIPTOR | — |
| `EDGE_DURATION_MS` | Edge Duration Milliseconds | DESCRIPTOR | — |
| `EDGE_NODE_ID` | Edge Node Identifier | DESCRIPTOR | — |
| `HOST` | Host | ENTITY | httpx, Nmap, Nuclei |
| `HOST_CLASSIFICATION` | Host Classification | DESCRIPTOR | — |
| `HSTS_INCLUDE_SUBDOMAINS` | HSTS Include Subdomains | DESCRIPTOR | — |
| `HSTS_MAX_AGE` | HSTS Max Age | DESCRIPTOR | — |
| `HSTS_PRELOAD` | HSTS Preload | DESCRIPTOR | — |
| `HTTP_STATUS_CODE` | HTTP Status Code | DESCRIPTOR | httpx, Katana |
| `IPV4_ADDRESS` | IPv4 Address | ENTITY | httpx, Netdiscover, Nmap, Subfinder |
| `NEL_ACTIVE` | Network Error Logging Active | DESCRIPTOR | — |
| `NETWORKS` | Networks Category | CATEGORY | httpx, Netdiscover, Nmap |
| `ORIGIN_DURATION_MS` | Origin Duration Milliseconds | DESCRIPTOR | — |
| `ORIGIN_FINGERPRINT_SUPPRESSED` | Origin Fingerprint Suppressed | DESCRIPTOR | — |
| `ORIGIN_HOST_COUNT` | Origin Host Count | DESCRIPTOR | — |
| `PORT` | Network Port | SUBENTITY | httpx, Nmap |
| `PROTOCOLS_OFFERED` | Protocols Offered | DESCRIPTOR | — |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | httpx, Katana, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_ELAPSED` | Scan Elapsed Time | DESCRIPTOR | httpx, Katana, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_EXIT_STATUS` | Scan Exit Status | DESCRIPTOR | httpx, Katana, Netdiscover, Nuclei, Pius, Subfinder |
| `SCAN_RECORD` | Scan Record | ENTITY | httpx, Katana, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_START` | Scan Start | DESCRIPTOR | httpx, Katana, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TARGET` | Scan Target | DESCRIPTOR | httpx, Katana, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TOOL` | Scan Tool | DESCRIPTOR | httpx, Katana, Nmap, Nuclei, Pius, Subfinder |
| `SERVICE` | Network Service | ENTITY | httpx, Nmap, Nuclei |
| `SERVICE_VERSION` | Service Version | DESCRIPTOR | Nmap |
| `SOFTWARE_USED` | Software Used | SUBENTITY | httpx |
| `TRANSPORT` | Transport Protocol | ENTITY | httpx, Nmap |

## Pius

Structure: [`pius_nugget_graph_structure.md`](nugget_structure/pius_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `AFFILIATES` | Affiliated Companies Category | CATEGORY | — |
| `BRAND_NAME` | Brand Name | DESCRIPTOR | — |
| `CANDIDATE_ENTITY` | Unresolved Research Lead | ENTITY | — |
| `CONFIDENCE_SCORE` | Source Confidence Score | DESCRIPTOR | — |
| `DISCOVERY_METHOD` | Discovery Method | DESCRIPTOR | — |
| `DOMAINS` | Domains Category | CATEGORY | — |
| `IS_PLACEHOLDER` | Placeholder Identity Flag | DESCRIPTOR | — |
| `IS_WILDCARD_DNS` | Wildcard DNS Detected | DESCRIPTOR | — |
| `JURISDICTION` | Legal Jurisdiction | DESCRIPTOR | — |
| `LEADS` | Research Leads Category | CATEGORY | — |
| `LEI` | Legal Entity Identifier | DESCRIPTOR | — |
| `NEEDS_REVIEW` | Needs Human Review | DESCRIPTOR | — |
| `NETWORK_TYPE` | Network Type | DESCRIPTOR | — |
| `PAGE` | Web Page URL | ENTITY | — |
| `PAGES` | Pages Category | CATEGORY | — |
| `PAGE_PATH` | Page Path | DESCRIPTOR | — |
| `PAGE_URL` | Page URL | DESCRIPTOR | — |
| `PRESEED_TYPE` | Preseed Record Type | DESCRIPTOR | — |
| `RELATIONSHIP_TYPE` | Relationship Type | DESCRIPTOR | — |
| `REVIEW_STATUS` | Review Status | DESCRIPTOR | — |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nmap, Nuclei, Subfinder |
| `SCAN_ELAPSED` | Scan Elapsed Time | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Subfinder |
| `SCAN_EXIT_STATUS` | Scan Exit Status | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nuclei, Subfinder |
| `SCAN_RECORD` | Scan Record | ENTITY | httpx, Katana, Nerva, Netdiscover, Nmap, Nuclei, Subfinder |
| `SCAN_START` | Scan Start | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Subfinder |
| `SCAN_TARGET` | Scan Target | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Subfinder |
| `SCAN_TARGET_ORG` | Scan Target Organization | DESCRIPTOR | — |
| `SCAN_TOOL` | Scan Tool | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Subfinder |
| `SUBDOMAIN_ENUMERATION_SUPPRESSED` | Subdomain Enumeration Suppressed | DESCRIPTOR | — |
| `WIKIDATA_ID` | Wikidata Identifier | DESCRIPTOR | — |
| `WILDCARD_IP_COUNT` | Wildcard DNS IP Count | DESCRIPTOR | — |

## Subfinder

Structure: [`subfinder_nugget_graph_structure.md`](nugget_structure/subfinder_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `CDN_REVIEW_NEEDED` | CDN Review Needed | DESCRIPTOR | — |
| `DISCOVERY_MODE` | Discovery Mode | DESCRIPTOR | — |
| `DISCOVERY_SOURCE` | Discovery Source | DESCRIPTOR | — |
| `IPV4_ADDRESS` | IPv4 Address | ENTITY | httpx, Nerva, Netdiscover, Nmap |
| `LIVENESS_STATUS` | Liveness Status | DESCRIPTOR | — |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nmap, Nuclei, Pius |
| `SCAN_ELAPSED` | Scan Elapsed Time | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius |
| `SCAN_EXIT_STATUS` | Scan Exit Status | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nuclei, Pius |
| `SCAN_MODE` | Scan Enumeration Mode | DESCRIPTOR | — |
| `SCAN_RECORD` | Scan Record | ENTITY | httpx, Katana, Nerva, Netdiscover, Nmap, Nuclei, Pius |
| `SCAN_START` | Scan Start | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius |
| `SCAN_TARGET` | Scan Target | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius |
| `SCAN_TOOL` | Scan Tool | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Nuclei, Pius |

## httpx

Structure: [`httpx_nugget_graph_structure.md`](nugget_structure/httpx_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `APPLICATIONS` | Applications Category | CATEGORY | Nerva, Nmap |
| `CDN` | Content Delivery Network Edge | ENTITY | Nerva |
| `CDN_NAME` | CDN Name | DESCRIPTOR | — |
| `CDN_TYPE` | CDN Type | DESCRIPTOR | — |
| `CNAME_TARGET` | CNAME Target | DESCRIPTOR | — |
| `CONTENT_LENGTH` | Content Length | DESCRIPTOR | — |
| `CONTENT_TYPE` | Content Type | DESCRIPTOR | — |
| `HOST` | Host | ENTITY | Nerva, Nmap, Nuclei |
| `HTTP_LIVENESS_STATUS` | HTTP Liveness Status | DESCRIPTOR | — |
| `HTTP_METHOD` | HTTP Method | DESCRIPTOR | Katana |
| `HTTP_PATH` | HTTP Path | DESCRIPTOR | — |
| `HTTP_STATUS_CODE` | HTTP Status Code | DESCRIPTOR | Katana, Nerva |
| `HTTP_TITLE` | HTTP Title | DESCRIPTOR | Nmap |
| `IPV4_ADDRESS` | IPv4 Address | ENTITY | Nerva, Netdiscover, Nmap, Subfinder |
| `IS_ERROR_PAGE` | Is Error Page | DESCRIPTOR | — |
| `LINE_COUNT` | Line Count | DESCRIPTOR | — |
| `NETWORKS` | Networks Category | CATEGORY | Nerva, Netdiscover, Nmap |
| `PAGE_HASH` | Page Hash | DESCRIPTOR | — |
| `PAGE_TYPE` | Page Type | DESCRIPTOR | — |
| `PORT` | Network Port | SUBENTITY | Nerva, Nmap |
| `PORT_STATE` | Port State | DESCRIPTOR | Nmap |
| `PROBE_CONNECTED` | Probe Connected Address | DESCRIPTOR | — |
| `PROBE_FAILED` | Probe Failed | DESCRIPTOR | — |
| `PROBE_TIMESTAMP` | Probe Timestamp | DESCRIPTOR | — |
| `RESPONSE_TIME_MS` | Response Time Milliseconds | DESCRIPTOR | — |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | Katana, Nerva, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_ELAPSED` | Scan Elapsed Time | DESCRIPTOR | Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_EXIT_STATUS` | Scan Exit Status | DESCRIPTOR | Katana, Nerva, Netdiscover, Nuclei, Pius, Subfinder |
| `SCAN_HOST_INPUT_COUNT` | Scan Host Input Count | DESCRIPTOR | — |
| `SCAN_PROBE_PROFILE` | Scan Probe Profile | DESCRIPTOR | — |
| `SCAN_RECORD` | Scan Record | ENTITY | Katana, Nerva, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_START` | Scan Start | DESCRIPTOR | Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TARGET` | Scan Target | DESCRIPTOR | Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TOOL` | Scan Tool | DESCRIPTOR | Katana, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SERVICE` | Network Service | ENTITY | Nerva, Nmap, Nuclei |
| `SOFTWARE_USED` | Software Used | SUBENTITY | Nerva |
| `SOFTWARE_VERSION` | Software Version | DESCRIPTOR | — |
| `TRANSPORT` | Transport Protocol | ENTITY | Nerva, Nmap |
| `TRANSPORT_PROTOCOL` | Transport Protocol | DESCRIPTOR | — |
| `UPSTREAM_SCENARIO_ID` | Upstream Scenario Identifier | DESCRIPTOR | Katana |
| `WORD_COUNT` | Word Count | DESCRIPTOR | — |

## Katana

Structure: [`katana_nugget_graph_structure.md`](nugget_structure/katana_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `HTTP_METHOD` | HTTP Method | DESCRIPTOR | httpx |
| `HTTP_STATUS_CODE` | HTTP Status Code | DESCRIPTOR | httpx, Nerva |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | httpx, Nerva, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_CRAWL_PROFILE` | Scan Crawl Profile | DESCRIPTOR | — |
| `SCAN_ELAPSED` | Scan Elapsed Time | DESCRIPTOR | httpx, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_EXIT_STATUS` | Scan Exit Status | DESCRIPTOR | httpx, Nerva, Netdiscover, Nuclei, Pius, Subfinder |
| `SCAN_RECORD` | Scan Record | ENTITY | httpx, Nerva, Netdiscover, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_START` | Scan Start | DESCRIPTOR | httpx, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TARGET` | Scan Target | DESCRIPTOR | httpx, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_TOOL` | Scan Tool | DESCRIPTOR | httpx, Nerva, Nmap, Nuclei, Pius, Subfinder |
| `SCAN_URL_INPUT_COUNT` | Scan URL Input Count | DESCRIPTOR | — |
| `UPSTREAM_SCENARIO_ID` | Upstream Scenario Identifier | DESCRIPTOR | httpx |

## Nuclei

Structure: [`nuclei_nugget_graph_structure.md`](nugget_structure/nuclei_nugget_graph_structure.md)

| Nugget | Description | Type | Also in other CLI apps |
|--------|-------------|------|------------------------|
| `FINDINGS` | Findings Container | CATEGORY | — |
| `HOST` | Host | ENTITY | httpx, Nerva, Nmap |
| `NUCLEI_EXTRACTED_RESULTS` | Nuclei Extracted Results | DESCRIPTOR | — |
| `NUCLEI_FINDING` | Nuclei Finding | ENTITY | — |
| `NUCLEI_FINDING_HOST` | Nuclei Finding Host | DESCRIPTOR | — |
| `NUCLEI_FINDING_IP` | Nuclei Finding IP | DESCRIPTOR | — |
| `NUCLEI_FINDING_PORT` | Nuclei Finding Port | DESCRIPTOR | — |
| `NUCLEI_FINDING_PROTOCOL` | Nuclei Finding Protocol | DESCRIPTOR | — |
| `NUCLEI_FINDING_TIMESTAMP` | Nuclei Finding Timestamp | DESCRIPTOR | — |
| `NUCLEI_FINDING_URL` | Nuclei Finding URL | DESCRIPTOR | — |
| `NUCLEI_MATCHED_AT` | Nuclei Matched At | DESCRIPTOR | — |
| `NUCLEI_MATCHER_NAME` | Nuclei Matcher Name | DESCRIPTOR | — |
| `NUCLEI_MATCHER_STATUS` | Nuclei Matcher Status | DESCRIPTOR | — |
| `NUCLEI_SEVERITY_CRITICAL` | Nuclei Critical Severity Bucket | CATEGORY | — |
| `NUCLEI_SEVERITY_HIGH` | Nuclei High Severity Bucket | CATEGORY | — |
| `NUCLEI_SEVERITY_INFO` | Nuclei Info Severity Bucket | CATEGORY | — |
| `NUCLEI_SEVERITY_LOW` | Nuclei Low Severity Bucket | CATEGORY | — |
| `NUCLEI_SEVERITY_MEDIUM` | Nuclei Medium Severity Bucket | CATEGORY | — |
| `NUCLEI_TEMPLATE` | Nuclei Template | ENTITY | — |
| `NUCLEI_TEMPLATE_AUTHOR` | Nuclei Template Author | DESCRIPTOR | — |
| `NUCLEI_TEMPLATE_ID` | Nuclei Template ID | DESCRIPTOR | — |
| `NUCLEI_TEMPLATE_NAME` | Nuclei Template Name | DESCRIPTOR | — |
| `NUCLEI_TEMPLATE_PATH` | Nuclei Template Path | DESCRIPTOR | — |
| `NUCLEI_TEMPLATE_PROTOCOL` | Nuclei Template Protocol | DESCRIPTOR | — |
| `NUCLEI_TEMPLATE_TAGS` | Nuclei Template Tags | DESCRIPTOR | — |
| `NUCLEI_VULNERABILITY` | Nuclei Vulnerability Observation | ENTITY | — |
| `NUCLEI_VULN_CPE` | Nuclei Vulnerability CPE | DESCRIPTOR | — |
| `NUCLEI_VULN_CVSS_METRICS` | Nuclei Vulnerability CVSS Metrics | DESCRIPTOR | — |
| `NUCLEI_VULN_CVSS_SCORE` | Nuclei Vulnerability CVSS Score | DESCRIPTOR | — |
| `NUCLEI_VULN_CWE` | Nuclei Vulnerability CWE | DESCRIPTOR | — |
| `NUCLEI_VULN_DESCRIPTION` | Nuclei Vulnerability Description | DESCRIPTOR | — |
| `NUCLEI_VULN_EPSS_PERCENTILE` | Nuclei Vulnerability EPSS Percentile | DESCRIPTOR | — |
| `NUCLEI_VULN_EPSS_SCORE` | Nuclei Vulnerability EPSS Score | DESCRIPTOR | — |
| `NUCLEI_VULN_IMPACT` | Nuclei Vulnerability Impact | DESCRIPTOR | — |
| `NUCLEI_VULN_PRODUCT` | Nuclei Vulnerability Product | DESCRIPTOR | — |
| `NUCLEI_VULN_REMEDIATION` | Nuclei Vulnerability Remediation | DESCRIPTOR | — |
| `NUCLEI_VULN_SEVERITY` | Nuclei Vulnerability Severity | DESCRIPTOR | — |
| `NUCLEI_VULN_TAGS` | Nuclei Vulnerability Tags | DESCRIPTOR | — |
| `NUCLEI_VULN_VENDOR` | Nuclei Vulnerability Vendor | DESCRIPTOR | — |
| `SCAN_CLI` | Scan CLI | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Nmap, Pius, Subfinder |
| `SCAN_ELAPSED` | Scan Elapsed Time | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Pius, Subfinder |
| `SCAN_EXIT_STATUS` | Scan Exit Status | DESCRIPTOR | httpx, Katana, Nerva, Netdiscover, Pius, Subfinder |
| `SCAN_FINDING_COUNT` | Scan Finding Count | DESCRIPTOR | — |
| `SCAN_RECORD` | Scan Record | ENTITY | httpx, Katana, Nerva, Netdiscover, Nmap, Pius, Subfinder |
| `SCAN_START` | Scan Start | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Pius, Subfinder |
| `SCAN_TARGET` | Scan Target | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Pius, Subfinder |
| `SCAN_TOOL` | Scan Tool | DESCRIPTOR | httpx, Katana, Nerva, Nmap, Pius, Subfinder |
| `SECURITY` | Security Knowledge Container | CATEGORY | — |
| `SERVICE` | Network Service | ENTITY | httpx, Nerva, Nmap |
| `TEMPLATES_USED` | Templates Used Container | CATEGORY | — |

## Extension nuggets not yet attributed to an implemented CLI app

In `nuggets_extension.json` but not found in the eight implemented structure docs / proposed graphs:

| Nugget | Description | Type |
|--------|-------------|------|
| `ANYCAST_SUSPECTED` | Anycast Suspected | DESCRIPTOR |
| `CDN_ASN` | CDN ASN | DESCRIPTOR |
| `CDN_ASN_ORG` | CDN ASN Organization | DESCRIPTOR |
| `CDN_DETECTION_SIGNAL` | CDN Detection Signal | DESCRIPTOR |
| `CDN_PRODUCT_HINT` | CDN Product Hint | DESCRIPTOR |
| `CDN_VENDOR_CONFIDENCE` | CDN Vendor Confidence | DESCRIPTOR |
| `CLASSIFICATION_CONFIDENCE` | Host Classification Confidence | DESCRIPTOR |
| `CSP_PRESENT` | Content Security Policy Present | DESCRIPTOR |
| `HSTS_ENABLED` | HSTS Enabled | DESCRIPTOR |
| `IP_VERSION` | IP Version | DESCRIPTOR |
| `NEL_REPORT_ENDPOINT` | Network Error Logging Report Endpoint | DESCRIPTOR |
| `ORIGIN_FINGERPRINT_RAW` | Raw Origin Fingerprint | DESCRIPTOR |
| `ORIGIN_IP` | Origin IP | DESCRIPTOR |
| `ORIGIN_TECHNOLOGY` | Origin Technology | DESCRIPTOR |
| `OS_MATCH_ACCURACY` | OS Match Accuracy | DESCRIPTOR |
| `RAW_VALUE` | Raw Unnormalized Value | DESCRIPTOR |
| `RECORD_ID` | Scan Record Identifier | DESCRIPTOR |
| `REDIRECT_LOCATION` | Redirect Location | DESCRIPTOR |
| `RESPONSE_HEADERS_RAW` | Raw Response Headers | DESCRIPTOR |
| `SAME_SYSTEM_CONFIDENCE` | Same System Confidence | DESCRIPTOR |
| `SAME_SYSTEM_EVIDENCE` | Same System Evidence | DESCRIPTOR |
| `SAME_SYSTEM_GROUP_ID` | Same System Group Identifier | DESCRIPTOR |
| `SCAN_ARGS` | Scan Arguments | DESCRIPTOR |
| `SERVER_HEADER` | Server Header | DESCRIPTOR |
| `WAF_BOT_MANAGEMENT_DETECTED` | WAF Bot Management Detected | DESCRIPTOR |
| `WAF_VENDOR_HINT` | WAF Vendor Hint | DESCRIPTOR |

