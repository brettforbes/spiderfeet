# Nmap Scenario Graph Description: service_version_permissive

## Summary
- Nodes: 38
- Edges: 50

## Node Types
- `CATEGORY`: 2
- `DESCRIPTOR`: 16
- `ENTITY`: 10
- `SUBENTITY`: 10

## Nugget Archetypes
- `APPLICATIONS`: 1
- `CPE_URL`: 3
- `HOST`: 1
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `INTERNET_NAME`: 1
- `IP_ADDRESS`: 1
- `NETWORKS`: 1
- `PORT`: 5
- `PORT_PROTOCOL`: 1
- `PORT_STATE`: 2
- `PORT_STATE_REASON`: 2
- `SCAN_CLI`: 1
- `SCAN_ELAPSED`: 1
- `SCAN_RECORD`: 1
- `SCAN_START`: 1
- `SCAN_SUMMARY`: 1
- `SCAN_TARGET`: 1
- `SCAN_TOOL`: 1
- `SCAN_VERSION`: 1
- `SERVICE`: 5
- `SERVICE_EXTRAINFO`: 2
- `SOFTWARE_USED`: 2
- `TRANSPORT`: 1

## Relations
- `contains`: 18
- `had`: 29
- `listens-to`: 3

## Edge Examples
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `HOST` `contains` `APPLICATIONS`
- `HOST` `contains` `NETWORKS`
- `IP_ADDRESS` `contains` `TRANSPORT`
- `NETWORKS` `contains` `IP_ADDRESS`
- `SCAN_RECORD` `contains` `HOST`
- `SERVICE` `contains` `CPE_URL`
- `SERVICE` `contains` `CPE_URL`
