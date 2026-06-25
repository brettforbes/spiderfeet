# Nmap Scenario Graph Description: service_version_corporate

## Summary
- Nodes: 24
- Edges: 29

## Node Types
- `CATEGORY`: 2
- `DESCRIPTOR`: 12
- `ENTITY`: 7
- `SUBENTITY`: 3

## Nugget Archetypes
- `APPLICATIONS`: 1
- `HOST`: 1
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `INTERNET_NAME`: 1
- `IP_ADDRESS`: 1
- `NETWORKS`: 1
- `PORT`: 2
- `PORT_PROTOCOL`: 1
- `PORT_STATE`: 1
- `PORT_STATE_REASON`: 1
- `SCAN_CLI`: 1
- `SCAN_ELAPSED`: 1
- `SCAN_RECORD`: 1
- `SCAN_START`: 1
- `SCAN_SUMMARY`: 1
- `SCAN_TARGET`: 1
- `SCAN_TOOL`: 1
- `SCAN_VERSION`: 1
- `SERVICE`: 2
- `SOFTWARE_USED`: 1
- `TRANSPORT`: 1

## Relations
- `contains`: 9
- `had`: 18
- `listens-to`: 2

## Edge Examples
- `APPLICATIONS` `contains` `SERVICE`
- `APPLICATIONS` `contains` `SERVICE`
- `HOST` `contains` `APPLICATIONS`
- `HOST` `contains` `NETWORKS`
- `IP_ADDRESS` `contains` `TRANSPORT`
- `NETWORKS` `contains` `IP_ADDRESS`
- `SCAN_RECORD` `contains` `HOST`
- `TRANSPORT` `contains` `PORT`
- `TRANSPORT` `contains` `PORT`
- `HOST` `had` `HOST_STATUS`
- `HOST` `had` `HOST_STATUS_REASON`
- `HOST` `had` `INTERNET_NAME`
