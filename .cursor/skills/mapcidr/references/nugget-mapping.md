# mapcidr Nugget Mapping

## Nugget Hierarchy

- input block -> `NETBLOCK_OWNER`
- expanded host -> `IP_ADDRESS`

## Node/Edge Rules

- create one netblock node per unique network
- create one IP node per unique host
- add `CONTAINS_IP` edge netblock -> ip

## nodes/edges Example

```json
{
  "nodes": [
    {"id": "netblock:198.51.100.0/30", "type": "NETBLOCK_OWNER", "data": {"value": "198.51.100.0/30"}},
    {"id": "ip:198.51.100.1", "type": "IP_ADDRESS", "data": {"value": "198.51.100.1"}}
  ],
  "edges": [
    {"source": "netblock:198.51.100.0/30", "target": "ip:198.51.100.1", "type": "CONTAINS_IP"}
  ]
}
```
