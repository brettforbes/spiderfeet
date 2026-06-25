# Nmap Scenario Graph Description: host_discovery_local_subnet

## Summary
- Nodes: 17
- Edges: 18

## Node Types
- `CATEGORY`: 2
- `DESCRIPTOR`: 9
- `ENTITY`: 6

## Nugget Archetypes
- `HOST`: 2
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `INTERNET_NAME`: 1
- `IP_ADDRESS`: 2
- `NETWORKS`: 2
- `SCAN_CLI`: 1
- `SCAN_ELAPSED`: 1
- `SCAN_RECORD`: 1
- `SCAN_START`: 1
- `SCAN_SUMMARY`: 1
- `SCAN_TARGET`: 1
- `SCAN_TOOL`: 1
- `SCAN_VERSION`: 1

## Relations
- `contains`: 6
- `had`: 12

## Edge Examples
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `NETWORKS` `contains` `IP_ADDRESS`
- `NETWORKS` `contains` `IP_ADDRESS`
- `SCAN_RECORD` `contains` `HOST`
- `SCAN_RECORD` `contains` `HOST`
- `HOST` `had` `HOST_STATUS`
- `HOST` `had` `HOST_STATUS_REASON`
- `HOST` `had` `INTERNET_NAME`
- `HOST` `had` `HOST_STATUS`
- `HOST` `had` `HOST_STATUS_REASON`
- `SCAN_RECORD` `had` `SCAN_CLI`
