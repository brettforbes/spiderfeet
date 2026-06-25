# Nmap Scenario Graph Description: windows_enrich_local

## Summary
- Nodes: 8
- Edges: 7

## Node Types
- `DESCRIPTOR`: 7
- `ENTITY`: 1

## Nugget Archetypes
- `SCAN_CLI`: 1
- `SCAN_ELAPSED`: 1
- `SCAN_RECORD`: 1
- `SCAN_START`: 1
- `SCAN_SUMMARY`: 1
- `SCAN_TARGET`: 1
- `SCAN_TOOL`: 1
- `SCAN_VERSION`: 1

## Relations
- `had`: 7

## Edge Examples
- `SCAN_RECORD` `had` `SCAN_CLI`
- `SCAN_RECORD` `had` `SCAN_ELAPSED`
- `SCAN_RECORD` `had` `SCAN_START`
- `SCAN_RECORD` `had` `SCAN_SUMMARY`
- `SCAN_RECORD` `had` `SCAN_TARGET`
- `SCAN_RECORD` `had` `SCAN_TOOL`
- `SCAN_RECORD` `had` `SCAN_VERSION`
