# Nmap Scenario Graph Description: host_discovery_permissive

## Summary
- Nodes: 14
- Edges: 13

## Node Types
- `CATEGORY`: 1
- `DESCRIPTOR`: 9
- `ENTITY`: 4

## Nugget Archetypes
- `HOST`: 1
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `INTERNET_NAME`: 1
- `IP_ADDRESS`: 1
- `NETWORKS`: 1
- `SCAN_CLI`: 1
- `SCAN_ELAPSED`: 1
- `SCAN_RECORD`: 1
- `SCAN_START`: 1
- `SCAN_SUMMARY`: 1
- `SCAN_TARGET`: 1
- `SCAN_TOOL`: 1
- `SCAN_VERSION`: 1

## Relations
- `contains`: 3
- `had`: 10

## Edge Examples
- `HOST` `contains` `NETWORKS`
- `NETWORKS` `contains` `IP_ADDRESS`
- `SCAN_RECORD` `contains` `HOST`
- `HOST` `had` `HOST_STATUS`
- `HOST` `had` `HOST_STATUS_REASON`
- `HOST` `had` `INTERNET_NAME`
- `SCAN_RECORD` `had` `SCAN_CLI`
- `SCAN_RECORD` `had` `SCAN_ELAPSED`
- `SCAN_RECORD` `had` `SCAN_START`
- `SCAN_RECORD` `had` `SCAN_SUMMARY`
- `SCAN_RECORD` `had` `SCAN_TARGET`
- `SCAN_RECORD` `had` `SCAN_TOOL`
