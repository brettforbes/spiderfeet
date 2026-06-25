# Nmap Scenario Graph Description: nse_default_permissive

## Summary
- Nodes: 42
- Edges: 48

## Node Types
- `CATEGORY`: 2
- `DESCRIPTOR`: 25
- `ENTITY`: 8
- `SUBENTITY`: 7

## Nugget Archetypes
- `APPLICATIONS`: 1
- `DSA`: 1
- `ECDSA`: 1
- `EDDSA`: 1
- `HOST`: 1
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `INTERNET_NAME`: 1
- `IP_ADDRESS`: 1
- `NETWORKS`: 1
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
- `SSH_KEY_BITS`: 3
- `SSH_KEY_KEY`: 4
- `SSH_KEY_TYPE`: 4
- `TRANSPORT`: 1

## Relations
- `contains`: 15
- `had`: 31
- `listens-to`: 2

## Notable Extracted Script Data
- SSH host keys represented: 4
  - `DSA` fingerprint `ac00a01a82ffcc5599dc672b34976b75`
  - `ECDSA` fingerprint `9602bb5e57541c4e452f564c4a24b257`
  - `EDDSA` fingerprint `33fa910fe0e17b1f6d05a2b0f1544156`
  - `RSA` fingerprint `203d2d44622ab05a9db5b30514c2a6b2`

## Edge Examples
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `HOST` `contains` `APPLICATIONS`
- `HOST` `contains` `NETWORKS`
- `IP_ADDRESS` `contains` `TRANSPORT`
- `NETWORKS` `contains` `IP_ADDRESS`
- `SCAN_RECORD` `contains` `HOST`
- `SERVICE` `contains` `DSA`
- `SERVICE` `contains` `ECDSA`
- `SERVICE` `contains` `EDDSA`
- `SERVICE` `contains` `RSA`
