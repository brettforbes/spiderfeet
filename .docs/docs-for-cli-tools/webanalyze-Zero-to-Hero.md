# webanalyze Zero to Hero

Practical guide for using **webanalyze** to fingerprint web stacks and feed SpiderFeet recon workflows. Flags validated against the local binary on **2026-08-10**.

## 1) What webanalyze does

`webanalyze` is a Go port of Wappalyzer-style technology detection. It fetches a target page (and optionally followed links), matches headers/HTML/scripts/cookies/meta/URL patterns against a `technologies.json` definition set, and reports product names, categories, and versions.

Definitions are refreshed with `-update` from the **enthec/webappanalyzer** sources used by current webanalyze builds.

## 2) Install and verify

This host:

| Item | Path |
|------|------|
| Binary | `C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe` |
| Release zip | `C:\projects\spiderfeet\.tools\webanalyze\webanalyze_Windows_x86_64.zip` |

```powershell
& "C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe" -h
```

There is **no** `-version` flag. The tool prints a version line on stderr in the scan header when not `-silent`.

Upstream install alternatives: [releases](https://github.com/rverton/webanalyze/releases) or `go install github.com/rverton/webanalyze/cmd/webanalyze@latest`.

## 3) Update technology definitions (required)

Scans fail if `technologies.json` cannot be found. Download into the current directory:

```powershell
Set-Location C:\projects\spiderfeet\.tools\webanalyze
.\webanalyze.exe -update
```

Lookup order for the apps file: current directory → executable directory → home.

## 4) First structured scan

```bash
webanalyze -host https://example.com -output json -silent
```

Example stdout line (pretty-printed):

```json
{
  "hostname": "https://example.com",
  "matches": [
    {
      "app_name": "Cloudflare",
      "version": "",
      "app": { "category_names": ["CDN"] }
    }
  ]
}
```

Use **`-output json`**, not a non-existent `-json` flag.

## 5) Major option classes and examples

### A. Single target

```bash
webanalyze -host https://shop.example.com -output json -silent
```

Bare `shop.example.com` becomes `http://shop.example.com` — prefer explicit HTTPS.

### B. Path-aware scanning

```bash
webanalyze -host https://shop.example.com/login -search=false -output json -silent
webanalyze -host https://shop.example.com/admin -search=false -output json -silent
```

### C. Batch scanning

```bash
webanalyze -hosts hosts.txt -output json -silent -worker 8
```

### D. Crawl and redirects

```bash
webanalyze -host https://shop.example.com -crawl 2 -redirect -output json -silent
```

`-redirect` defaults to **false**; `-search` defaults to **true** (same base domain). Disable search with `-search=false`.

### E. Human stdout / CSV (exploration or triage)

```bash
webanalyze -host https://shop.example.com -crawl 1
webanalyze -host https://shop.example.com -output csv -silent
```

Formal SpiderFeet examination uses JSON only when JSON is available.

## 6) Practical workflows

### Workflow 1: Breadth classification

1. Feed live web hosts from httpx (or similar).
2. `webanalyze -hosts live.txt -output json -silent`.
3. Group by `app_name` / `category_names`.
4. Prioritize CMS and versioned stacks.

### Workflow 2: Depth on critical hosts

1. Re-scan with `-redirect` and `-crawl 1+`.
2. Add `/login` and `/admin` paths.
3. Merge detections; keep versions.
4. Route to CMSeeK, wafw00f, or Nuclei by category.

### Workflow 3: Drift monitoring

1. Snapshot JSON periodically.
2. Diff technology sets per host.
3. Investigate new high-risk components.

## 7) Convert output to SpiderFeet nuggets

From each JSON host object:

| Field | Nugget |
|-------|--------|
| Host of `hostname` | `INTERNET_NAME` |
| `matches[].app_name` (+ `version` if set) | `WEBSERVER_TECHNOLOGY` |

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "shop.example.com" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "Nginx" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "WordPress 6.4.2" }
  ],
  "edges": [
    { "source": "shop.example.com", "target": "Nginx", "relationship": "had" },
    { "source": "shop.example.com", "target": "WordPress 6.4.2", "relationship": "had" }
  ]
}
```

Details: `.cursor/skills/webanalyze/references/nugget-mapping.md`.

## 8) Tactics to improve reliability

- Prefer explicit schemes; remember default is HTTP.
- Opt in to `-redirect` for bounce-heavy sites.
- Scan more than `/` for frameworks behind routed pages.
- Keep `-silent` for clean NDJSON pipelines; inspect stderr for errors.
- Refresh definitions with `-update` when warned that apps are older than a week.
- Preserve raw JSON lines for audit and parser upgrades.

## 9) Common pitfalls

- Using invented flags (`-json`, `-version`).
- Skipping `-update` on a fresh extract (no `technologies.json`).
- Treating one homepage detection as complete for a large app.
- Leaving `-redirect` off when the interesting app is behind a 3xx.
- Using stdout/CSV as graph source when `-output json` exists.
- Forgetting that failed hosts only appear on stderr.

## 10) Further reading

- `.cursor/skills/webanalyze/SKILL.md`
- `.cursor/skills/webanalyze/references/SKILLS.md`
- `.docs/docs-for-cli-tools/webanalyze-CLI-Options.md`
- [webanalyze README](https://github.com/rverton/webanalyze/blob/master/README.md)
