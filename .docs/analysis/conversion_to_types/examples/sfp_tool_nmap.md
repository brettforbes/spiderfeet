# Example: CLI stdout line parse (`sfp_tool_nmap`)

**Pattern:** `cli_subprocess_parse`  
**Source:** `modules/sfp_tool_nmap.py`

## Input

`IP_ADDRESS`, `NETBLOCK_OWNER` (with netblock scan option)

## Acquisition

```python
Popen([nmap, "-O", "--osscan-limit", eventData], ...)
content = stdout.decode("utf-8", errors="replace")
```

## Conversion (fragile text parse)

Single IP:

```python
for line in content.split("\n"):
    if "OS details:" in line:
        _, opsys = line.split(": ")
        SpiderFeetEvent("OPERATING_SYSTEM", opsys, ...)
```

Netblock: tracks `currentIp` from `scan report for` lines, pairs with next `OS details:`.

**Produces:** `OPERATING_SYSTEM`, and for netblocks also `IP_ADDRESS` per host line.

**Does not emit:** `TCP_PORT_OPEN` (OS scan only, not `-p` port scan).

## Risks

- Locale/nmap version changes break line parsing
- No structured payload — OS string is opaque
- No fixture tests today (roadmap: `.tests/fixtures/cli_stdout/sfp_tool_nmap/`)

## CLI base class target

`parse_stdout(content, event) -> list[TypedObservation]` with versioned regex table; WSL path resolution already shared across tools.
