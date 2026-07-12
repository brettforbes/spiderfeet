# Nerva scan narrative — `tcp_http_rich_json`

## Introduction

This report summarizes a Nerva fingerprint capture after Rulesets A/C/B qualification. **1** system node(s) were emitted (0 HOST, 1 CDN).

## Systems

- `CDN` `scanme.nmap.org` — classification `fronted_unknown`

## CDN / edge fronting

This hostname is fronted by a CDN/edge vendor. Origin host count is indeterminate — do not treat edge IP cardinality as origin host count.

Detected vendor(s): **Netlify**.

Origin host count is **indeterminate** — edge IP cardinality must not be treated as origin host count.

## Origin fingerprint suppression

SOFTWARE_USED nodes tagged ORIGIN_FINGERPRINT_SUPPRESSED are retained for audit only and must not be reported as confirmed origin stack.

Suppressed fingerprint markers present: **1**.

## Services

- `http`

## Appendix

### Nodes

- `APPLICATIONS`: applications:scanme.nmap.org
- `CDN`: scanme.nmap.org
- `CDN_VENDOR`: Netlify
- `CLASSIFICATION_RULE_FIRED`: C1: Server/header signature (Netlify)
- `CPE_URL`: cpe:2.3:a:apache:http_server:*:*:*:*:*:*:*:*
- `CPE_URL`: cpe:2.3:a:apache:http_server:2.4.7:*:*:*:*:*:*:*
- `CPE_URL`: cpe:2.3:o:canonical:ubuntu_linux:*:*:*:*:*:*:*:*
- `HOST_CLASSIFICATION`: fronted_unknown
- `HTTP_STATUS_CODE`: 200
- `IPV6_ADDRESS`: 2600:3c01::f03c:91ff:fe18:bb2f
- `IP_ADDRESS`: 45.33.32.156
- `NETWORKS`: networks:scanme.nmap.org
- `ORIGIN_FINGERPRINT_SUPPRESSED`: True
- `ORIGIN_HOST_COUNT`: indeterminate
- `PORT`: 80
- `SCAN_CLI`: nerva -t scanme.nmap.org:80 --json -w 5000
- `SCAN_ELAPSED`: 16.094
- `SCAN_EXIT_STATUS`: 0
- `SCAN_RECORD`: nerva:scanme.nmap.org:80:2026-06-30T07:38:43.148728+00:00
- `SCAN_START`: 2026-06-30T07:38:43.148728+00:00
- `SCAN_TARGET`: scanme.nmap.org:80
- `SCAN_TOOL`: nerva
- `SERVICE`: http
- `SERVICE_VERSION`: Apache/2.4.7 (Ubuntu)
- `SOFTWARE_USED`: Apache HTTP Server:2.4.7
- `SOFTWARE_USED`: Ubuntu
- `SOFTWARE_USED`: apache_httpd:2.4.7
- `TLS_ENABLED`: False
- `TRANSPORT`: tcp

### Edges

- `SCAN_RECORD` `had` `SCAN_CLI`
- `SCAN_RECORD` `had` `SCAN_TARGET`
- `SCAN_RECORD` `had` `SCAN_START`
- `SCAN_RECORD` `had` `SCAN_ELAPSED`
- `SCAN_RECORD` `had` `SCAN_EXIT_STATUS`
- `SCAN_RECORD` `had` `SCAN_TOOL`
- `SCAN_RECORD` `contains` `CDN`
- `CDN` `had` `HOST_CLASSIFICATION`
- `CDN` `had` `CLASSIFICATION_RULE_FIRED`
- `CDN` `had` `CDN_VENDOR`
- `CDN` `had` `ORIGIN_HOST_COUNT`
- `CDN` `contains` `NETWORKS`
- `CDN` `contains` `APPLICATIONS`
- `NETWORKS` `contains` `IPV6_ADDRESS`
- `APPLICATIONS` `contains` `SERVICE`
- `IPV6_ADDRESS` `contains` `TRANSPORT`
- `TRANSPORT` `contains` `PORT`
- `SERVICE` `listens-to` `PORT`
- `SERVICE` `had` `SERVICE_VERSION`
- `SERVICE` `had` `HTTP_STATUS_CODE`
- `SERVICE` `had` `TLS_ENABLED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SOFTWARE_USED` `had` `ORIGIN_FINGERPRINT_SUPPRESSED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SOFTWARE_USED` `had` `ORIGIN_FINGERPRINT_SUPPRESSED`
- `SERVICE` `contains` `SOFTWARE_USED`
- `SOFTWARE_USED` `had` `ORIGIN_FINGERPRINT_SUPPRESSED`
- `SERVICE` `contains` `CPE_URL`
- `SERVICE` `contains` `CPE_URL`
- `SERVICE` `contains` `CPE_URL`
- `NETWORKS` `contains` `IP_ADDRESS`
- `IP_ADDRESS` `contains` `TRANSPORT`
