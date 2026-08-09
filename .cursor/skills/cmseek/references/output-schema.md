# CMSeeK Output Schema — `Result/<target>/cms.json`

## Location

```
<cmseek_install_dir>/
  cmseek.py
  Result/
    <target>/
      cms.json          ← primary machine-readable result
      (optional deep-scan artifacts per CMS)
```

- `<target>` is the hostname/path key CMSeeK uses when creating the result directory (after redirect normalization in logs).
- SpiderFeet reads: `{cmseekpath}/Result/{eventData}/cms.json` where `eventData` is the incoming `INTERNET_NAME`.
- After redirects, CMSeeK may write under the **final host** directory while SpiderFeet still looks up `{eventData}` — align seeds or scan canonical URLs.

## Primary file: `cms.json`

Written on scan completion via `handle_quit()` → `json.dumps` with sorted keys and indentation.

### Core fields

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Original or normalized target URL logged at scan start |
| `target_url` | string | Final URL after redirect handling (when applicable) |
| `last_scanned` | string | Timestamp string when scan directory was initialized |
| `detection_param` | string | Method that matched: `header`, `generator`, `source`, `robots`, or `dirscheck` |
| `cms_id` | string | Internal CMS identifier (e.g. `wordpress`, `joomla`) |
| `cms_name` | string | Human-readable CMS name (e.g. `WordPress`) — **SpiderFeet primary field** |
| `cms_version` | string | Detected version when version module succeeds; may be absent |
| `cms_url` | string | Vendor or project URL for the CMS |

### Initial template (before scan)

```json
{
    "url": "",
    "last_scanned": "",
    "detection_param": "",
    "cms_id": "",
    "cms_name": "",
    "cms_url": "",
    "target_url": ""
}
```

### Example: successful WordPress detection

```json
{
    "cms_id": "wordpress",
    "cms_name": "WordPress",
    "cms_url": "https://wordpress.org",
    "cms_version": "6.4.2",
    "detection_param": "source",
    "last_scanned": "2026-06-15 10:22:01.123456",
    "target_url": "https://www.example.com",
    "url": "https://example.com"
}
```

### Example: detection failed

Stdout shows `CMS Detection failed`. Either no `cms.json` is written with `cms_name`, or `cms_name` remains empty. SpiderFeet treats missing/empty `cms_name` as no event.

## Deep scan artifacts (optional)

When deep scan runs (not `--light-scan` / `--only-cms`), CMSeeK may write additional files under `Result/<target>/` depending on CMS module — for example:

- Plugin lists
- Theme lists
- User enumeration output
- Bruteforce result logs (`bruteforce_result_*.txt`)

SpiderFeet `sfp_tool_cmseek` **does not** ingest these files today — only `cms.json`.

## Result index

CMSeeK maintains a report index under the install directory (`createindex.init`) tracking prior scans for `--skip-scanned`. Structure is internal; agents should rely on per-target `cms.json` for parsing.

## Parsing notes

- All values in `cms.json` are stored as strings via `update_log()`.
- Parse with `json.loads`; do not use TextFSM on this file.
- Check `cms_name` truthiness before emitting downstream events.
- Combine `cms_name` + `cms_version` with a space for display strings (SpiderFeet pattern).

## Python read pattern (SpiderFeet)

```python
log_path = f"{resultpath}/{eventData}/cms.json"
with open(log_path, encoding="utf-8") as f:
    j = json.load(f)
cms_name = j.get("cms_name")
cms_version = j.get("cms_version")
software = " ".join(filter(None, [cms_name, cms_version]))
```
