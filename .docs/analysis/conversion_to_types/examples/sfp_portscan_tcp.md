# Example: Socket probe → port nuggets (`sfp_portscan_tcp`)

**Pattern:** `dns_network_local` (socket, not DNS)  
**Source:** `modules/sfp_portscan_tcp.py`

## Input

`IP_ADDRESS` or expanded `NETBLOCK_OWNER`

## Acquisition

No HTTP. `self.sf.safeSocket(ip, port, timeout)` per port in configured list (thread pool).

## Conversion

```python
evt = SpiderFeetEvent("TCP_PORT_OPEN", f"{ip}:{port}", self.__name__, srcEvent)
self.notifyListeners(evt)

if banner_bytes:
    bevt = SpiderFeetEvent("TCP_PORT_OPEN_BANNER", banner_utf8, self.__name__, evt)
    self.notifyListeners(bevt)
```

**Encoding:** Port identity is always `ip:port` string. Banner event uses **port event as source** (not IP), so provenance is IP scan → open port → banner.

## Structured payload (recommended)

```json
{ "ip": "8.8.8.8", "port": 443, "protocol": "tcp", "state": "open" }
```

Would enable TypeDB `listening-service` without splitting strings (see doc 07).

## Generalisation

Shared with UDP scanners and many CLI tools: **transport-endpoint** normaliser can be one function used by `sfp_portscan_tcp`, `sfp_tool_nmap` (if extended to port scan), masscan adapters.
