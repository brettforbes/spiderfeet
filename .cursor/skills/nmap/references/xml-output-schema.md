# Nmap XML Output Schema (`-oX`)

Agents **must** capture Nmap results with `-oX` (or `-oA` which includes XML). Parse with `xml.etree.ElementTree` — not grep, not normal output, not TextFSM.

DTD: https://nmap.org/book/nmap-dtd.html

## Document root

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nmaprun>
<nmaprun scanner="nmap" args="..." start="..." startstr="..." version="..." xmloutputversion="1.05">
  <scaninfo type="syn" protocol="tcp" numservices="1000" services="1-1000"/>
  <verbose level="0"/>
  <debugging level="0"/>
  <host>...</host>
  <runstats>...</runstats>
</nmaprun>
```

### `nmaprun` attributes

| Attribute | Meaning |
|-----------|---------|
| `scanner` | Always `nmap` |
| `args` | Full command line (provenance) |
| `start` / `startstr` | Unix epoch and human timestamp |
| `version` | Nmap version string |
| `xmloutputversion` | Schema version (typically `1.05`) |

## `scaninfo`

Describes the port scan phase for a protocol.

| Attribute | Values | Notes |
|-----------|--------|-------|
| `type` | `syn`, `connect`, `ack`, `window`, `maimon`, `null`, `fin`, `xmas`, `udp`, `sctp` | Scan technique |
| `protocol` | `tcp`, `udp`, `sctp` | L4 protocol |
| `numservices` | integer | Port count scanned |
| `services` | e.g. `1-1000`, `22,80,443` | Port expression |

Multiple `scaninfo` elements may appear (e.g. TCP + UDP).

## `host` — per-target container

| Child / attribute | Purpose |
|-------------------|---------|
| `status` | Host up/down state |
| `address` | IP, MAC, or hostname |
| `hostnames` | Reverse/forward DNS names |
| `ports` | Open/filtered/closed port list |
| `os` | OS fingerprint matches |
| `uptime` | Uptime guess |
| `distance` | Hop count |
| `tcpsequence` | TCP ISN analysis |
| `ipidsequence` | IP ID analysis |
| `tcptssequence` | TCP timestamp analysis |
| `hostscript` | NSE host-level script output |
| `times` | Timing stats |

### `status`

```xml
<status state="up" reason="echo-reply" reason_ttl="64"/>
```

| Attribute | Values |
|-----------|--------|
| `state` | `up`, `down`, `unknown`, `skipped` |
| `reason` | `echo-reply`, `arp-response`, `syn-ack`, `reset`, `admin-prohibited`, `host-unreach`, etc. |
| `reason_ttl` | TTL from probe response |

### `address`

```xml
<address addr="192.168.1.10" addrtype="ipv4"/>
<address addr="AA:BB:CC:DD:EE:FF" addrtype="mac" vendor="Vendor Name"/>
```

| `addrtype` | Use |
|------------|-----|
| `ipv4` / `ipv6` | Primary host key |
| `mac` | Layer-2 when on local segment |

### `hostnames` / `hostname`

```xml
<hostnames>
  <hostname name="www.example.com" type="PTR"/>
  <hostname name="example.com" type="user"/>
</hostnames>
```

| `type` | Meaning |
|--------|---------|
| `user` | From user input or forward DNS |
| `PTR` | Reverse DNS |

## `ports` / `port` — core port data

```xml
<ports>
  <extraports state="filtered" count="997"/>
  <port protocol="tcp" portid="22">
    <state state="open" reason="syn-ack" reason_ttl="64"/>
    <service name="ssh" product="OpenSSH" version="8.9p1" extrainfo="Ubuntu" ostype="Linux" method="probed" conf="10"/>
    <script id="ssh-hostkey" output="..."/>
  </port>
</ports>
```

### `port` attributes

| Attribute | Example |
|-----------|---------|
| `protocol` | `tcp`, `udp`, `sctp` |
| `portid` | `22`, `443` |

### `state` (under `port`)

| `state` value | Meaning |
|---------------|---------|
| `open` | Service accepting connections |
| `closed` | Reachable, nothing listening |
| `filtered` | Probe blocked (firewall/ACL) |
| `open\|filtered` | No response (UDP/common) |
| `closed\|filtered` | Ambiguous (idle scan) |

| `reason` | Examples: `syn-ack`, `reset`, `no-response`, `admin-prohibited` |

### `service` (version detection `-sV`)

| Attribute | Maps to |
|-----------|---------|
| `name` | Well-known service (ssh, http) |
| `product` | Product name |
| `version` | Version string |
| `extrainfo` | Extra banner text |
| `ostype` | OS hint from service |
| `hostname` | SSL cert CN, etc. |
| `method` | `probed`, `table`, `user` |
| `conf` | Confidence 0–10 |
| `tunnel` | `ssl`, `ssl/http` |
| `cpes` | CPE strings (child elements) |

### `script` (NSE under port)

```xml
<script id="http-title" output="Site Title">
  <elem key="title">Welcome</elem>
  <table key="something">...</table>
</script>
```

Structured children: `elem`, `table`, `table key="..."`.

## `os` — OS detection (`-O`)

```xml
<os>
  <portused state="open" proto="tcp" portid="22"/>
  <osmatch name="Linux 5.4" accuracy="95" line="12345">
    <osclass type="general purpose" vendor="Linux" osfamily="Linux" osgen="5.X" accuracy="95"/>
  </osmatch>
  <osfingerprint fingerprint="SF-Port22-TCP:..."/>
</os>
```

| Element | Notes |
|---------|-------|
| `osmatch` | Best guesses; use highest `accuracy` |
| `osclass` | Vendor/family/generation taxonomy |
| `osfingerprint` | Raw fingerprint string |

## `hostscript` — host-level NSE

```xml
<hostscript>
  <script id="smb-os-discovery" output="OS: Windows 10">
    <elem key="os">Windows 10</elem>
  </script>
</hostscript>
```

## `runstats` — scan summary

```xml
<runstats>
  <finished time="..." timestr="..." elapsed="12.34" summary="Nmap done..." exit="success"/>
  <hosts up="5" down="95" total="100"/>
</runstats>
```

## Python parsing patterns

### Load and iterate hosts

```python
import xml.etree.ElementTree as ET

def parse_nmap_xml(path: str):
    root = ET.parse(path).getroot()
    for host in root.findall("host"):
        yield host
```

### Host up filter

```python
status = host.find("status")
if status is None or status.get("state") != "up":
    continue
```

### Primary IPv4

```python
def host_ipv4(host) -> str | None:
    for addr in host.findall("address"):
        if addr.get("addrtype") == "ipv4":
            return addr.get("addr")
    return None
```

### Open ports

```python
for port in host.findall(".//port"):
    st = port.find("state")
    if st is None or st.get("state") != "open":
        continue
    proto = port.get("protocol")
    portid = port.get("portid")
    svc = port.find("service")
    name = svc.get("name") if svc is not None else None
```

### Best OS match

```python
def best_os_match(host) -> str | None:
    os_el = host.find("os")
    if os_el is None:
        return None
    matches = os_el.findall("osmatch")
    if not matches:
        return None
    best = max(matches, key=lambda m: int(m.get("accuracy", "0")))
    return best.get("name")
```

### Script output (structured)

```python
for script in port.findall("script"):
    sid = script.get("id")
    output = script.get("output", "")
    for elem in script.findall("elem"):
        key = elem.get("key")
        text = elem.text
```

## Pitfalls

- **Missing `host`**: target down or discovery skipped — not an error.
- **`open|filtered`**: treat as uncertain; do not emit `TCP_PORT_OPEN` without policy.
- **Multiple addresses**: prefer `ipv4`/`ipv6` over `mac` for graph keys.
- **Large files**: use `iterparse` for huge scans; `findall` is fine for single-host XML.
- **DTD**: optional for parsing; ElementTree ignores DOCTYPE.
- **Merging runs**: `nmaprun` per invocation; merge graphs in application layer, not by concatenating XML without a wrapper.

See [nugget-mapping.md](nugget-mapping.md) for SpiderFeet type assignment.
