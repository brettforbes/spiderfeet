# Nmap Scenario Graph Description: traceroute_permissive

## Summary
- Nodes: 79
- Edges: 84

## Node Types
- `CATEGORY`: 9
- `DESCRIPTOR`: 33
- `ENTITY`: 28
- `SUBENTITY`: 9

## Nugget Archetypes
- `APPLICATIONS`: 1
- `HOP_ORDER`: 8
- `HOP_RTT`: 4
- `HOP_TTL`: 8
- `HOST`: 8
- `HOST_STATUS`: 1
- `HOST_STATUS_REASON`: 1
- `INTERNET_NAME`: 8
- `IP_ADDRESS`: 8
- `NETWORKS`: 8
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
- `TRACE`: 1
- `TRACE_HOP`: 8
- `TRACE_PROTOCOL`: 1
- `TRANSPORT`: 1

## Relations
- `contains`: 38
- `had`: 45
- `listens-to`: 1

## Edge Examples
- `APPLICATIONS` `contains` `SERVICE`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `APPLICATIONS`
- `HOST` `contains` `NETWORKS`
- `HOST` `contains` `NETWORKS`
- `IP_ADDRESS` `contains` `TRANSPORT`
- `NETWORKS` `contains` `IP_ADDRESS`
