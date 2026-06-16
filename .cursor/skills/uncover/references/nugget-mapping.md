# uncover Nugget Mapping

## Typical Outputs

- `IP_ADDRESS` or `INTERNET_NAME`
- `TCP_PORT_OPEN`
- `WEBSERVER_TECHNOLOGY` (where product/stack hints exist)
- raw provider evidence as metadata

## Node/Edge Rules

- host node for domain/IP
- port node for discovered services
- host -> port as `HAS_OPEN_PORT`
- preserve provider list for confidence tracking

## nodes/edges Example

```json
{
  "nodes": [
    {"id": "ip:203.0.113.20", "type": "IP_ADDRESS", "data": {"value": "203.0.113.20"}},
    {"id": "port:203.0.113.20:8443", "type": "TCP_PORT_OPEN", "data": {"value": "8443"}}
  ],
  "edges": [
    {"source": "ip:203.0.113.20", "target": "port:203.0.113.20:8443", "type": "HAS_OPEN_PORT"}
  ]
}
```
