# Nmap Scenario Graph Description: os_aggressive_permissive

## Summary
- Nodes: 109
- Edges: 118

## Node Types
- `CATEGORY`: 10
- `DESCRIPTOR`: 52
- `ENTITY`: 30
- `SUBENTITY`: 17

## Nugget Archetypes
- `APPLICATIONS`: 1
- `CPE_URL`: 1
- `DSA`: 1
- `ECDSA`: 1
- `EDDSA`: 1
- `ENVIRONMENT`: 1
- `HOP_ORDER`: 8
- `HOP_RTT`: 6
- `HOP_TTL`: 8
- `HOST`: 8
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `HTTP_TITLE`: 1
- `INTERNET_NAME`: 8
- `IP_ADDRESS`: 8
- `NETWORKS`: 8
- `OPERATING_SYSTEM`: 1
- `OS_MATCH_ACCURACY`: 1
- `PORT`: 3
- `PORT_PROTOCOL`: 1
- `PORT_STATE`: 2
- `PORT_STATE_REASON`: 2
- `RSA`: 1
- `SCAN_CLI`: 1
- `SCAN_ELAPSED`: 1
- `SCAN_RECORD`: 1
- `SCAN_START`: 1
- `SCAN_SUMMARY`: 1
- `SCAN_TARGET`: 1
- `SCAN_TOOL`: 1
- `SCAN_VERSION`: 1
- `SERVICE`: 3
- `SERVICE_EXTRAINFO`: 1
- `SOFTWARE_USED`: 1
- `SSH_KEY_BITS`: 3
- `SSH_KEY_KEY`: 4
- `SSH_KEY_TYPE`: 4
- `TRACE`: 1
- `TRACE_HOP`: 8
- `TRACE_PROTOCOL`: 1
- `TRANSPORT`: 1

## Relations
- `contains`: 49
- `had`: 67
- `listens-to`: 2

## Notable Extracted Script Data
- SSH host keys represented: 4
  - `DSA` fingerprint `ac00a01a82ffcc5599dc672b34976b75`
  - `ECDSA` fingerprint `9602bb5e57541c4e452f564c4a24b257`
  - `EDDSA` fingerprint `33fa910fe0e17b1f6d05a2b0f1544156`
  - `RSA` fingerprint `203d2d44622ab05a9db5b30514c2a6b2`
- HTTP titles represented: 1
  - `Go ahead and ScanMe!`

## Edge Examples
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `ENVIRONMENT` `contains` `OPERATING_SYSTEM`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `APPLICATIONS`
- `HOST` `contains` `ENVIRONMENT`
