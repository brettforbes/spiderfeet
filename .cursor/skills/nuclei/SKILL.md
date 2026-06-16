---
name: nuclei
description: Run ProjectDiscovery Nuclei vulnerability scans, parse JSONL findings, and map results to SpiderFeet nuggets (CVE tiers, VULNERABILITY_GENERAL, WEBSERVER_TECHNOLOGY). Use when scanning hosts, URLs, netblocks, writing custom templates/workflows, tuning template tags/severity, or integrating sfp_tool_nuclei output.
---

# Nuclei — Vulnerability Scanning

## Purpose

Use when an agent must **discover vulnerabilities and technologies** on `INTERNET_NAME`, `IP_ADDRESS`, or expanded `NETBLOCK_OWNER` targets using [ProjectDiscovery Nuclei](https://github.com/projectdiscovery/nuclei), then convert JSONL stdout into SpiderFeet events.

## Step-by-Step Instructions

1. **Confirm scope and authorization** — Nuclei is invasive (`sfp_tool_nuclei` flags: `tool`, `slow`, `invasive`). Only scan targets the operator owns or has written permission to test.
2. **Resolve binary and templates** — `nuclei` on `PATH` or `nuclei_path` option; templates from `template_path` or `.tools/nuclei-templates` via `resolve_nuclei_templates()`.
3. **Prepare targets** — Single hostname/IP on stdin, or one host per line. Netblocks: expand to individual IPs (Nuclei does not accept CIDR stdin directly); respect `netblockscanmax` (default /24).
4. **Run with SpiderFeet defaults** — Pipe targets on stdin:

   ```bash
   nuclei -silent -jsonl -concurrency 100 -retries 1 -t /path/to/nuclei-templates \
     -no-interactsh -etags dos,fuzz,misc
   ```

5. **Parse JSONL** — One JSON object per line; skip blank lines and non-`{` prefixes.
6. **Map findings** — Extract CVE IDs from the raw line → `VULNERABILITY_CVE_*` via `sf.cveInfo()`. Non-CVE matches with `matcher-name` → `VULNERABILITY_GENERAL` or `WEBSERVER_TECHNOLOGY` when `info.severity == "info"`.
7. **Re-type hosts** — If `matched-at` host differs from seed target, emit `IP_ADDRESS` or `INTERNET_NAME` parent event first.
8. **Adapt follow-up scans** — Use tactics in [`references/tactics.md`](references/tactics.md): narrow by tags/severity after broad tech fingerprinting, or widen templates after empty runs on confirmed web services.

## If/Then Decision Rules

| If | Then |
|----|------|
| Target is `NETBLOCK_OWNER` and prefix &lt; `netblockscanmax` | Skip (too large) |
| Target already scanned or inside scanned netblock | Skip duplicate |
| `info.severity == "info"` and `matcher-name` present | Emit `WEBSERVER_TECHNOLOGY` |
| CVE pattern in JSON line | Emit tiered `VULNERABILITY_CVE_*` (not `VULNERABILITY_GENERAL`) |
| No CVE, `matcher-name` present | Emit `VULNERABILITY_GENERAL` with template/matcher/matched-at |
| Process timeout (base 240s + 240s per netblock IP) | Kill process; log timeout; partial JSONL may be lost |
| Return code ≠ 0 and empty stdout | Treat as error |
| Need out-of-band (Interactsh) confirmation | **Do not** enable in SpiderFeet module (`-no-interactsh` is fixed); run manual scan outside module if authorized |
| Need fuzz/dos/misc templates | Remove or override `-etags` only in **authorized** manual runs—not default module behavior |
| Target list is huge | Lower `-concurrency`, split batches, use `-tags` / `-severity` to reduce noise |
| Only technologies needed | `-tags tech` or rely on `info` severity routing to `WEBSERVER_TECHNOLOGY` |
| Authenticated findings required | Use Nuclei authenticated scan config (see `templates-and-workflows.md`); not wired in `sfp_tool_nuclei` today |

## Guardrails & Pitfalls

- **Authorized testing only** — No scanning of third-party assets without explicit written permission.
- **Do not enable Interactsh** in production SpiderFeet runs (`-no-interactsh` prevents OOB callback infrastructure).
- **Excluded tags** (`dos,fuzz,misc`) reduce collateral damage; re-enabling may trigger WAF blocks or service disruption.
- **High concurrency** (100) can overwhelm small hosts or trigger rate limits; tune down on fragile targets.
- **Template drift** — Findings depend on template version; pin or update templates deliberately.
- **JSONL ≠ complete schema** — Fields vary by template; always guard `KeyError` when parsing.
- **CVE regex** — Matches anywhere in line JSON; false positives rare but possible in references text.
- **stdin netblock expansion** — Large /24 = 254× timeout increment; monitor operator expectations.
- Prefer **machine-readable `-jsonl`** over table/text output for all automation.

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Broad → narrow** — Full template tree minus excluded tags, then `-tags cve`, `-severity critical,high` on hits.
2. **Tech-first** — When mapping attack surface, accept `info` severity as `WEBSERVER_TECHNOLOGY`, then run targeted CVE/exposure templates for those stacks.
3. **Workflow templates** — Chain dependent checks (e.g. detect panel → default creds) via Nuclei workflows for higher signal.
4. **Mass scan hygiene** — Split targets, stable template path, consistent `-retries 1`, log stderr separately.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Grouped CLI flags |
| `jsonl-output-schema.md` | JSONL field reference |
| `templates-and-workflows.md` | Template DSL and workflows |
| `nugget-mapping.md` | SpiderFeet event mapping |
| `tactics.md` | Scan adaptation sequences |
| `sources.md` | Official URLs |

## Examples

### SpiderFeet-equivalent single host

```bash
echo "https://scanme.example.com" | nuclei -silent -jsonl -concurrency 100 -retries 1 \
  -t ~/.local/nuclei-templates -no-interactsh -etags dos,fuzz,misc
```

### Severity-filtered manual pass

```bash
printf '%s\n' api.example.com staging.example.com | nuclei -silent -jsonl \
  -severity critical,high,medium -tags cve -t /path/to/templates -no-interactsh
```

### Tag-based technology sweep

```bash
echo "https://app.example.com" | nuclei -silent -jsonl -tags tech -severity info \
  -t /path/to/templates -no-interactsh
```

### Template ID pin

```bash
echo "https://target.example" | nuclei -silent -jsonl -id CVE-2024-1234 -t /path/to/templates
```

### File list input (manual)

```bash
nuclei -silent -jsonl -l targets.txt -t /path/to/templates -no-interactsh -etags dos,fuzz,misc
```

### Update templates before scan

```bash
nuclei -update-templates
# or: git -C /path/to/nuclei-templates pull
```

### Parse one JSONL line (Python)

```python
import json, re

line = '{"template-id":"tech-detect","info":{"name":"Tech","severity":"info"},...}'
data = json.loads(line)
host = data["matched-at"].split(":")[0]
cves = re.findall(r"CVE-\d{4}-\d{4,7}", line)
```

### Workflow run (manual)

```bash
echo "https://target.example" | nuclei -silent -jsonl -w workflows/ -t /path/to/templates
```
