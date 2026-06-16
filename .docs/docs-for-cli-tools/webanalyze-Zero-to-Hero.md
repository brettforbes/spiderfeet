# webanalyze Zero to Hero

Practical guide for using `webanalyze` to fingerprint web stacks and feed actionable recon workflows.

## 1) What webanalyze does

`webanalyze` detects web technologies from headers, HTML, script patterns, and other fingerprints in a Wappalyzer-style ecosystem.

## 2) Install and verify

Build/install from the repository and confirm help output:

```bash
webanalyze -h
```

## 3) First scan

```bash
webanalyze -host https://example.com
```

Start with a known live URL and explicit scheme.

## 4) Major option classes and examples

### A. Single target

```bash
webanalyze -host https://shop.example.com
```

### B. Path-aware scanning

```bash
webanalyze -host https://shop.example.com/login
webanalyze -host https://shop.example.com/admin
```

### C. Batch scanning (version-dependent)

```bash
webanalyze -hosts hosts.txt
```

### D. Structured output (if supported)

```bash
webanalyze -host https://shop.example.com -json
```

## 5) Practical workflows

### Workflow 1: Breadth classification

1. Fingerprint all live web hosts.
2. Group by core stack.
3. Prioritize targets by tech risk profile.

### Workflow 2: Depth by business-critical host

1. Scan multiple paths for one host.
2. Merge tech detections.
3. Route to targeted vulnerability modules.

### Workflow 3: Drift monitoring

1. Snapshot technology sets periodically.
2. Diff snapshots.
3. Investigate newly added technologies immediately.

## 6) Convert output to SpiderFeet nuggets (`nodes[]` and `edges[]`)

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "shop.example.com" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "Nginx" },
    { "type": "WEBSERVER_TECHNOLOGY", "data": "WordPress" }
  ],
  "edges": [
    { "source": "shop.example.com", "target": "Nginx", "relationship": "uses_technology" },
    { "source": "shop.example.com", "target": "WordPress", "relationship": "uses_technology" }
  ]
}
```

## 7) Tactics to improve reliability

- Scan more than `/` for app frameworks hidden behind routed pages.
- Keep both confidence and evidence when detections conflict.
- Preserve raw detection output for audit and parser upgrades.
- Reconcile detections with Wappalyzer schema categories.

## 8) Common pitfalls

- Treating one detection as definitive ground truth.
- Ignoring redirects and scanning only pre-redirect endpoints.
- Losing category/version metadata during normalization.
- Failing to deduplicate technology aliases.

## 9) Further reading

- `.cursor/skills/webanalyze/SKILL.md`
- `.cursor/skills/webanalyze/references/SKILLS.md`
- [webanalyze README](https://github.com/rverton/webanalyze/blob/master/README.md)
