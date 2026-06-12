# Example: CLI JSON-lines (`sfp_tool_nuclei`)

**Pattern:** `cli_subprocess_parse`  
**Source:** `modules/sfp_tool_nuclei.py`

## Input

`INTERNET_NAME`, `IP_ADDRESS`, `NETBLOCK_OWNER`

## Acquisition

Nuclei run with JSON output; stdout read as text, split by newlines.

## Conversion

```python
for line in content.split("\n"):
    if not line.startswith("{"):
        continue
    data = json.loads(line)
    host = data["matched-at"].split(":")[0]
    # Optional IP_ADDRESS / INTERNET_NAME if host != eventData
    matches = re.findall(r"CVE-\d{4}-\d{4,7}", line)
    if matches:
        etype, cvetext = self.sf.cveInfo(cve)
        SpiderFeetEvent(etype, cvetext, ...)
    elif "matcher-name" in data:
        SpiderFeetEvent("VULNERABILITY_GENERAL", ...)
        # severity branches → WEBSERVER_TECHNOLOGY etc.
```

## Why this is the CLI template

- **Machine-readable output** (JSON per finding) — prefer this for all new CLI integrations
- Combines JSON parse + regex CVE extraction + host re-typing
- Maps to multiple CVE tier types via shared `sf.cveInfo()`

## Generalisation

`JsonLinesParser` in CLI framework: one JSON object per line → list of mapping rules. Nuclei template id / matcher-name → nugget type table in YAML.
