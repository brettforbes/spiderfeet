# Netdiscover Output and Parsing

## Output modes

| Mode | Flag | Use |
|------|------|-----|
| Interactive TUI | *(default)* | Human operator; scrollable table |
| Parseable | `-P` | Scripts, SpiderFeet modules, TextFSM |
| Parseable + passive tail | `-P -L` | Stream new hosts after active phase |

**Rule:** SpiderFeet parsers must invoke netdiscover with **`-P`** (and **`-N`** when available).

---

## Interactive table format

Header and status lines (not parseable rows):

```
Currently scanning: 192.168.1.0/24   |   Screen View: Unique Hosts
3 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 180
_____________________________________________________________________________
  IP            At MAC Address     Count     Len  MAC Vendor / Hostname
-----------------------------------------------------------------------------
192.168.1.1     00:14:22:01:23:45      1      60  Dell Inc.
192.168.1.100   08:00:27:53:81:2b      1      60  PCS Systemtechnik GmbH
```

Skip all banner, separator, and summary lines in parsers.

---

## `-P` parseable format

Each discovered host is one line, **whitespace-separated** fields:

| Column | Name | Example | Notes |
|--------|------|---------|-------|
| 1 | `IP` | `192.168.1.1` | IPv4 |
| 2 | `MAC` | `00:14:22:01:23:45` | Lower or mixed case |
| 3 | `COUNT` | `1` | ARP packets seen |
| 4 | `LEN` | `60` | Frame length |
| 5+ | `VENDOR` | `Dell Inc.` | May contain spaces; remainder of line |

### Sample `-P` stdout

```
192.168.1.1     00:14:22:01:23:45       1       60      Dell Inc.
192.168.1.100   08:00:27:53:81:2b       1       60      PCS Systemtechnik GmbH
192.168.1.254   aa:bb:cc:dd:ee:ff       1       60      Unknown vendor
```

With hostname enrichment (`-m` file), vendor column may look like:

```
Dell Inc. / server01
```

### Lines to skip

- Empty lines
- `Currently scanning:` status lines (if `-N` absent)
- `-- Ending netdiscover` footer (some versions)
- Any line not starting with an IPv4 octet pattern

---

## Recommended invocation for capture

```bash
sudo netdiscover -P -N -i eth0 -r 192.168.1.0/24 2>/dev/null
```

Redirect stderr unless debugging privilege errors.

---

## TextFSM template

Save as `netdiscover_parsable.textfsm`:

```
Value Required IP (\d+\.\d+\.\d+\.\d+)
Value Required MAC ([0-9a-fA-F:]{17})
Value COUNT (\d+)
Value LEN (\d+)
Value VENDOR (.+)

Start
  ^${IP}\s+${MAC}\s+${COUNT}\s+${LEN}\s+${VENDOR} -> Record
  ^\s*$$
  ^Currently scanning: -> Next
  ^-- Ending netdiscover -> Next
  ^.* -> Next

EOF
```

### Hostname split (optional second pass)

If vendor field contains ` / ` hostname suffix:

```python
def split_vendor_hostname(vendor: str) -> tuple[str, str | None]:
    if " / " in vendor:
        v, h = vendor.split(" / ", 1)
        return v.strip(), h.strip()
    return vendor.strip(), None
```

---

## Python parser sketch

```python
import textfsm
from pathlib import Path

_TEMPLATE = Path(__file__).with_name("netdiscover_parsable.textfsm")

def parse_netdiscover_p(raw: str) -> list[dict]:
    with _TEMPLATE.open() as f:
        fsm = textfsm.TextFSM(f)
    return fsm.ParseTextToDicts(raw)
```

Pair with [`nugget-mapping.md`](nugget-mapping.md) for graph emission.

---

## Validation

```bash
python -m textfsm.parser netdiscover_parsable.textfsm fixtures/netdiscover_p_sample.txt
```

Fixture should include:

- Multiple hosts
- Vendor with spaces (`Samsung Electronics Co.,Ltd`)
- `Unknown vendor` row
- Optional `Vendor / hostname` row

---

## Partial / streaming input

`-P -L` may append rows over time. For streaming:

```python
fsm = textfsm.TextFSM(template_file)
for chunk in stream:
    rows = fsm.ParseText(chunk, eof=False)
    emit_nuggets(rows)
final = fsm.ParseText("", eof=True)
```

---

## What netdiscover does **not** output

- Open TCP/UDP ports
- Hostnames via DNS (unless `-m` enrichment)
- IPv6 neighbors (tool is IPv4 ARP focused)
- Routed remote hosts outside the local segment

Port and service data come from **Nmap** → **Nerva** in the downstream pipeline (see [`tactics.md`](tactics.md)).

---

## Cross-reference

- TextFSM skill: [`../../textfsm/SKILL.md`](../../textfsm/SKILL.md)
- Row → nugget mapping: [`nugget-mapping.md`](nugget-mapping.md)
