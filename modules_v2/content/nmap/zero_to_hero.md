# Nmap Zero to Hero — XML Output, Parsing, and Nuggets

End-to-end guide: run Nmap, capture **XML only**, parse with Python, map to SpiderFeet nuggets.

Skill reference: `.cursor/skills/nmap/SKILL.md`

## 0. Why Nmap and why XML?

[Nmap](https://nmap.org/) discovers hosts, ports, services, OS fingerprints, and runs NSE scripts. Output formats include normal text, grepable, and XML.

**Agents parse XML only (`-oX`).** It is stable, hierarchical, and documented with a DTD. Normal output changes layout between versions; regex breaks.

**Do not use TextFSM** on Nmap output — use `xml.etree.ElementTree`.

## 1. Install

### Linux / macOS

```bash
# Debian/Ubuntu
sudo apt install nmap

# macOS
brew install nmap

nmap --version
```

### Windows

Download installer from https://nmap.org/download.html. Default path: `C:\Program Files (x86)\Nmap\nmap.exe`.

SpiderFeet module `sfp_tool_nmap` checks PATH and common install locations.

### Privileges

| Capability | Requires admin/root |
|------------|---------------------|
| SYN scan (`-sS`) | Yes (raw sockets) |
| OS detection (`-O`) | Yes |
| UDP scan (`-sU`) | Yes |
| Connect scan (`-sT`) | No |

On Windows without admin, use `-sT`.

## 2. Hello World — first XML scan

```bash
nmap -sV -O --osscan-limit -oX hello.xml scanme.nmap.org
```

Inspect:

```bash
# Pretty-print (optional)
xmllint --format hello.xml | head -80
```

You should see `<nmaprun>`, `<host>`, `<ports>`, `<port>`, possibly `<os>`.

## 3. Scan workflow (adaptive)

```
Discovery (-sn)  →  Port scan (-sS/-sT)  →  Service/OS (-sV -O)  →  NSE (--script)
        ↓                    ↓                      ↓                      ↓
  discovery.xml          ports.xml              detail.xml              nse.xml
```

### Step 1 — Discovery

```bash
nmap -sn -oX discovery.xml 192.168.1.0/24
```

If zero hosts: `nmap -Pn -PS80,443 -sn -oX discovery_pn.xml ...`

### Step 2 — Ports

```bash
nmap -sS --open -p- -T4 -oX ports.xml -iL live_hosts.txt
```

Unprivileged: replace `-sS` with `-sT`.

### Step 3 — Service + OS

```bash
nmap -sV -O --osscan-limit -oX detail.xml 192.168.1.10
```

### Step 4 — NSE

```bash
nmap -sV --script "default,safe" -p 22,80,443 -oX nse.xml 192.168.1.10
```

Full phase doc: `.cursor/skills/nmap/references/workflows-and-phases.md`

## 4. XML structure essentials

Root: `<nmaprun>`. Children: `<host>` per target, `<runstats>` summary.

Per host:

| Element | Content |
|---------|---------|
| `status` | up/down |
| `address` | ipv4, ipv6, mac |
| `hostnames/hostname` | DNS names |
| `ports/port` | port state, service, scripts |
| `os/osmatch` | OS guesses |
| `hostscript` | host-level NSE |

Per port:

```xml
<port protocol="tcp" portid="443">
  <state state="open" reason="syn-ack"/>
  <service name="https" product="nginx" version="1.18.0"/>
  <script id="http-title" output="Welcome"/>
</port>
```

Full reference: `.cursor/skills/nmap/references/xml-output-schema.md`

DTD: https://nmap.org/book/nmap-dtd.html

## 5. Python parsing

### 5.1 Load file

```python
import xml.etree.ElementTree as ET

tree = ET.parse("hello.xml")
root = tree.getroot()
assert root.tag == "nmaprun"
```

### 5.2 Iterate live hosts

```python
def iter_live_hosts(root):
    for host in root.findall("host"):
        status = host.find("status")
        if status is not None and status.get("state") == "up":
            yield host
```

### 5.3 Extract IPv4

```python
def get_ipv4(host) -> str | None:
    for addr in host.findall("address"):
        if addr.get("addrtype") == "ipv4":
            return addr.get("addr")
    return None
```

### 5.4 Open TCP ports

```python
def iter_open_ports(host):
    for port in host.findall(".//port"):
        state = port.find("state")
        if state is None or state.get("state") != "open":
            continue
        yield {
            "protocol": port.get("protocol"),
            "portid": port.get("portid"),
            "service": port.find("service"),
            "scripts": port.findall("script"),
        }
```

### 5.5 Best OS match

```python
def best_os(host, min_accuracy=90) -> str | None:
    os_el = host.find("os")
    if os_el is None:
        return None
    best = None
    best_acc = 0
    for m in os_el.findall("osmatch"):
        acc = int(m.get("accuracy", "0"))
        if acc >= min_accuracy and acc > best_acc:
            best_acc = acc
            best = m.get("name")
    return best
```

### 5.6 Service label

```python
def format_service(svc) -> str | None:
    if svc is None:
        return None
    parts = [p for p in (svc.get("product"), svc.get("version"), svc.get("extrainfo")) if p]
    if parts:
        return " ".join(parts)
    return svc.get("name")
```

### 5.7 Large files — iterparse

```python
def iter_hosts_from_large_xml(path):
    for event, elem in ET.iterparse(path, events=("end",)):
        if elem.tag == "host":
            yield elem
            elem.clear()
```

### 5.8 Validate exit status

```python
def scan_exit(root) -> str:
    finished = root.find(".//finished")
    return finished.get("exit") if finished is not None else "unknown"
```

## 6. Map XML to SpiderFeet nuggets

Nugget catalogue: `.docs/analysis/nuggets.json`

| Nugget ID | Source in XML |
|-----------|---------------|
| `IP_ADDRESS` | `address@ipv4` / `ipv6`, host up |
| `INTERNET_NAME` | `hostname@name` |
| `TCP_PORT_OPEN` | `port` tcp, `state=open` → data `ip:port` |
| `UDP_PORT_OPEN` | `port` udp, `state=open` |
| `SOFTWARE_USED` | `service@product` + version |
| `TCP_PORT_OPEN_BANNER` | `service@extrainfo`, NSE `banner` |
| `OPERATING_SYSTEM` | `osmatch@name` (accuracy threshold) |
| `WEBSERVER_BANNER` | NSE `http-title`, `http-server-header` |

### 6.1 Node and edge pattern

```python
def build_graph(xml_path: str, seed_id: str):
    root = ET.parse(xml_path).getroot()
    nodes, edges = [], []

    for host in iter_live_hosts(root):
        ip = get_ipv4(host)
        if not ip:
            continue
        ip_id = f"ip:{ip}"
        nodes.append({"id": ip_id, "type": "IP_ADDRESS", "data": ip})
        edges.append({"source": seed_id, "target": ip_id, "relation": "discovered"})

        for p in iter_open_ports(host):
            if p["protocol"] != "tcp":
                continue
            port = p["portid"]
            pid = f"tcp:{ip}:{port}"
            nodes.append({"id": pid, "type": "TCP_PORT_OPEN", "data": f"{ip}:{port}"})
            edges.append({"source": ip_id, "target": pid, "relation": "listens_on"})

            label = format_service(p["service"])
            if label:
                sid = f"sw:{ip}:{port}:{label}"
                nodes.append({"id": sid, "type": "SOFTWARE_USED", "data": label})
                edges.append({"source": pid, "target": sid, "relation": "runs"})

        os_name = best_os(host)
        if os_name:
            oid = f"os:{ip}:{os_name}"
            nodes.append({"id": oid, "type": "OPERATING_SYSTEM", "data": os_name})
            edges.append({"source": ip_id, "target": oid, "relation": "runs"})

    return nodes, edges
```

Full mapping rules: `.cursor/skills/nmap/references/nugget-mapping.md`

## 7. Run Nmap from Python (subprocess)

```python
import subprocess
from pathlib import Path

def run_nmap_xml(target: str, xml_out: Path, extra_args: list[str] | None = None) -> int:
    cmd = ["nmap", "-oX", str(xml_out)]
    if extra_args:
        cmd.extend(extra_args)
    cmd.append(target)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return proc.returncode

run_nmap_xml("203.0.113.10", Path("out.xml"), ["-sV", "-O", "--osscan-limit"])
```

SpiderFeet legacy module (`modules/sfp_tool_nmap.py`) uses `-O --osscan-limit` without XML — new code should use `-oX` and the graph builder.

## 8. Hostile networks — adapt

| Problem | Fix |
|---------|-----|
| No hosts up | `-Pn` |
| All filtered | `-sT`, `-f`, `-T2` |
| No OS | NSE `smb-os-discovery`, lower accuracy threshold carefully |
| Slow | `-T4`, `--top-ports`, `--host-timeout` |

Detail: `.cursor/skills/nmap/references/evasion-and-tactics.md`

## 9. Testing your parser

1. Run scan against `scanme.nmap.org` (allowed test host).
2. Save `hello.xml` as fixture.
3. Assert:

```python
nodes, edges = build_graph("hello.xml", "seed:test")
types = {n["type"] for n in nodes}
assert "IP_ADDRESS" in types
# ports depend on scanme state — at least assert parser doesn't crash
```

4. Add synthetic XML fragments for `filtered`, `open|filtered`, missing `os`.

## 10. CLI reference

- Skill flags: `.cursor/skills/nmap/references/cli-flags.md`
- Full options: `NMAP-CLI-Options.md` (this directory)
- Official: https://nmap.org/book/man.html

## 11. Checklist

- [ ] Every scan uses `-oX`
- [ ] Parser uses ElementTree, not line regex
- [ ] Only `open` ports → `TCP_PORT_OPEN` / `UDP_PORT_OPEN`
- [ ] OS nuggets gated by accuracy
- [ ] Provenance stored (`args`, xml path)
- [ ] Phases split on large networks
- [ ] Authorization documented

## 12. Next steps

- Wire parser into SpiderFeet module with XML path.
- Add fixtures under `test/fixtures/nmap/`.
- Cross-link Maps UI for port graph visualization.
- Compare results with Tests tab seed probes per `.docs/analysis/stage4_seed_corpus_and_tests.md`.
