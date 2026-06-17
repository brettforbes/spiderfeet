# CMSeeK → SpiderFeet Nugget Mapping

## Module

- **ID:** `sfp_tool_cmseek`
- **Source:** `modules/sfp_tool_cmseek.py`
- **Watched:** `INTERNET_NAME`
- **Produced:** `WEBSERVER_TECHNOLOGY`

## Input event

| Nugget | Role |
|--------|------|
| `INTERNET_NAME` | Hostname or URL seed (e.g. `example.com`, `https://shop.example.com`) |

The module passes `eventData` directly to `cmseek.py -u` and expects results at `Result/{eventData}/cms.json`.

## Output event

| Nugget | When emitted | Value format |
|--------|--------------|--------------|
| `WEBSERVER_TECHNOLOGY` | `cms_name` present in `cms.json` | `"<cms_name> <cms_version>"` (version omitted if empty) |

### Mapping logic

```python
cms_name = j.get("cms_name")
cms_version = j.get("cms_version")
software = " ".join(filter(None, [cms_name, cms_version]))
# → SpiderFeetEvent("WEBSERVER_TECHNOLOGY", software, ...)
```

### Examples

| `cms.json` | `WEBSERVER_TECHNOLOGY` |
|------------|------------------------|
| `cms_name: "WordPress"`, `cms_version: "6.4.2"` | `WordPress 6.4.2` |
| `cms_name: "Drupal"`, no version | `Drupal` |
| no `cms_name` / detection failed | *(no event)* |

## Fields not emitted (today)

| `cms.json` field | Potential future nugget |
|------------------|-------------------------|
| `cms_id` | Could refine technology string or link to CMS-specific modules |
| `detection_param` | Descriptor on scan method |
| `cms_url` | `URL_WEB` or metadata |
| `target_url` | Redirect chain evidence |

## Graph edges (TypeDB / maps)

Typical pattern when integrating manually:

```
INTERNET_NAME (seed)
    └── WEBSERVER_TECHNOLOGY (descriptor on same host)
```

Provenance: attach `source_module: sfp_tool_cmseek`, `detection_param`, raw `cms.json` snippet in edge metadata when building custom parsers.

## CLI manifest / TextFSM

CMSeeK output is **JSON file-based**, not stdout tables. For manifest-driven CLI runners:

- **stdout:** failure messages only; do not parse for CMS name
- **artifact:** `Result/<target>/cms.json`
- **parser:** `json` load, not TextFSM

## Negative / clean-miss semantics

Stage 4 module tests: no `WEBSERVER_TECHNOLOGY` event when CMS is not detected or `cms_name` is absent. A run that completes but finds no CMS is a valid **clean miss**, not a tool error.
