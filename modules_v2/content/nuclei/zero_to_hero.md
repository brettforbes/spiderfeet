# Nuclei Zero to Hero

A practical path from installation to productive vulnerability scanning with [ProjectDiscovery Nuclei](https://github.com/projectdiscovery/nuclei), including SpiderFeet integration.

> **Authorization:** Run Nuclei only against systems you own or have explicit written permission to test. Nuclei sends active probes that can trigger alerts, rate limits, or outages.

---

## 1. What Nuclei does

Nuclei is a fast, template-driven scanner. Each YAML template defines requests and response matchers for a specific misconfiguration, exposure, technology, or CVE. Results stream as **JSON Lines** (`-jsonl`)—ideal for SpiderFeet's `sfp_tool_nuclei` module.

---

## 2. Install

### Binary (recommended)

```bash
# Go install
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Or PD install script (see official install docs)
```

Verify:

```bash
nuclei -version
```

### Templates

```bash
nuclei -update-templates
# Or clone:
git clone https://github.com/projectdiscovery/nuclei-templates.git ~/.local/nuclei-templates
```

SpiderFeet expects templates at `template_path` module option or `.tools/nuclei-templates`.

---

## 3. First scan (60 seconds)

```bash
echo "https://scanme.nmap.org" | nuclei -silent -jsonl \
  -t ~/.local/nuclei-templates \
  -no-interactsh -etags dos,fuzz,misc
```

Each output line is one finding. Pipe to `jq` for readability:

```bash
... | jq -c '{id: ."template-id", severity: .info.severity, at: ."matched-at"}'
```

---

## 4. Core concepts

| Concept | Meaning |
|---------|---------|
| Template | YAML check definition with `id`, `info`, protocol block |
| Tag | Category filter (`cve`, `tech`, `exposure`, …) |
| Severity | `info` → technology; `low`–`critical` → issues |
| Workflow | Conditional chain of templates |
| JSONL | One JSON object per match on stdout |

---

## 5. Essential CLI patterns

### Single URL

```bash
nuclei -u https://example.com -silent -jsonl -t ./nuclei-templates -no-interactsh
```

### Host list

```bash
nuclei -l hosts.txt -silent -jsonl -t ./nuclei-templates -no-interactsh -etags dos,fuzz,misc
```

### CVE-focused

```bash
nuclei -u https://example.com -tags cve -severity critical,high -jsonl -silent -no-interactsh
```

### Technology only

```bash
nuclei -u https://example.com -tags tech -severity info -jsonl -silent -no-interactsh
```

### One template

```bash
nuclei -u https://example.com -id tech-detect -jsonl -silent
```

Full flag reference: [Nuclei-CLI-Options.md](Nuclei-CLI-Options.md) and `.cursor/skills/nuclei/references/cli-options.md`.

---

## 6. SpiderFeet integration

Module: `sfp_tool_nuclei`

| Setting | Purpose |
|---------|---------|
| `nuclei_path` | Binary path (optional if on PATH) |
| `template_path` | Template directory |
| `netblockscan` | Expand `NETBLOCK_OWNER` to per-IP stdin |
| `netblockscanmax` | Max prefix length to scan (24 = /24) |

**Fixed flags** (do not expect module to pass custom tags without code change):

```
-silent -jsonl -concurrency 100 -retries 1 -no-interactsh -etags dos,fuzz,misc
```

**Events produced:**

- CVE strings → `VULNERABILITY_CVE_*` (tiered)
- Matcher + non-info severity → `VULNERABILITY_GENERAL`
- Matcher + info severity → `WEBSERVER_TECHNOLOGY`

See `.cursor/skills/nuclei/references/nugget-mapping.md`.

---

## 7. Reading JSONL output

Typical fields:

```json
{
  "template-id": "CVE-2021-44228",
  "info": { "name": "Log4j RCE", "severity": "critical" },
  "matched-at": "https://app.example.com/",
  "matcher-name": "log4j"
}
```

SpiderFeet extracts CVEs from the **entire line** via regex, then falls back to matcher-based events.

---

## 8. Intermediate: shaping scans

### Reduce noise

```bash
-etags dos,fuzz,misc
-severity critical,high,medium
-tags cve,exposure
```

### Improve reach on live web apps

```bash
-follow-redirects
-rate-limit 50
-c 50
```

### Workflows for depth

```bash
nuclei -u https://example.com -w workflows/ -t nuclei-templates/ -jsonl -silent
```

---

## 9. Advanced: custom templates

1. Start from a similar template in `nuclei-templates`.
2. Set unique `id`, correct `severity` and `tags`.
3. `nuclei -validate -t my-check.yaml`
4. `nuclei -id my-check -u https://staging -jsonl -debug`

Authoring reference: `.cursor/skills/nuclei/references/templates-and-workflows.md`.

---

## 10. Advanced: mass scanning

For large target sets:

1. Split `hosts.txt` into chunks (500–5000 per batch).
2. Use `-rate-limit` and moderate `-c`.
3. Archive JSONL per batch; dedupe by `template-id` + `matched-at`.
4. Read [mass scanning CLI](https://docs.projectdiscovery.io/opensource/nuclei/mass-scanning-cli).

SpiderFeet netblock mode expands CIDR to IPs on stdin—watch timeout growth on /24 (254 hosts).

---

## 11. CI/CD gate

```bash
nuclei -l staging.txt -severity critical,high -jsonl -silent -no-interactsh \
  -t ./nuclei-templates -o findings.jsonl
# fail pipeline if critical count > 0
```

---

## 12. Tactics cheat sheet

| Goal | Command shape |
|------|----------------|
| Footprint tech | `-tags tech -severity info` |
| CVE sweep | `-tags cve -severity critical,high,medium` |
| Panels/exposure | `-tags panel,exposure` |
| Debug one check | `-id <id> -debug` |
| Update signatures | `nuclei -update-templates` |

Full tactics: `.cursor/skills/nuclei/references/tactics.md`.

---

## 13. Troubleshooting

| Symptom | Fix |
|---------|-----|
| No output | Confirm HTTP service; try `-follow-redirects` |
| Timeouts | Lower `-c`; reduce template set |
| WAF 403 | Rate limit; custom User-Agent; scan from allowed IP |
| Empty after module run | Check `nuclei_path`, `template_path`, stderr |
| Wrong event type | Check `info.severity` and CVE regex on line |

---

## 14. Next steps

- Agent skill: `.cursor/skills/nuclei/SKILL.md`
- Sources index: `.cursor/skills/nuclei/references/sources.md`
- Module source: `modules/sfp_tool_nuclei.py`
