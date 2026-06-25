# Nmap Scenario Graph Description: skip_ping_permissive

## Summary
- Nodes: 21
- Edges: 21

## Node Types
- `CATEGORY`: 2
- `DESCRIPTOR`: 12
- `ENTITY`: 6
- `SUBENTITY`: 1

## Nugget Archetypes
- `APPLICATIONS`: 1
- `HOST`: 1
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `INTERNET_NAME`: 1
- `IP_ADDRESS`: 1
- `NETWORKS`: 1
- `PORT`: 1
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
- `SERVICE`: 1
- `TRANSPORT`: 1

## Relations
- `contains`: 7
- `had`: 13
- `listens-to`: 1

## Edge Examples
- `APPLICATIONS` `contains` `SERVICE`
- `HOST` `contains` `APPLICATIONS`
- `HOST` `contains` `NETWORKS`
- `IP_ADDRESS` `contains` `TRANSPORT`
- `NETWORKS` `contains` `IP_ADDRESS`
- `SCAN_RECORD` `contains` `HOST`
- `TRANSPORT` `contains` `PORT`
- `HOST` `had` `HOST_STATUS`
- `HOST` `had` `HOST_STATUS_REASON`
- `HOST` `had` `INTERNET_NAME`
- `PORT` `had` `PORT_PROTOCOL`
- `PORT` `had` `PORT_STATE`
