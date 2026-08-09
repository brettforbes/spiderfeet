# Recon-ng Zero to Hero

From first launch on this SpiderFeet host through a full modular domain OSINT pipeline: workspace → marketplace modules → subdomain/host expansion → contacts/ports → export → SpiderFeet mapping. Framework version **5.1.2**. Prefer **`recon-cli`** once a sequence is proven.

| Field | Value |
|-------|-------|
| Python | `C:\projects\spiderfeet\.venv\Scripts\python.exe` |
| Framework | `C:\projects\spiderfeet\.tools\recon-ng\` |
| Launchers | `recon-ng`, `recon-cli`, `recon-web` |
| Skill | `.cursor/skills/recon_ng/SKILL.md` |
| CLI options | `recon-ng-CLI-Options.md` (Captured help **2026-08-10**) |

---

## 1) Install and bootstrap

1. Framework tree is at `.tools/recon-ng/` (see `REQUIREMENTS` for Python deps in the project venv).
2. Set `PYTHONPATH` to the framework root and verify:

```powershell
$env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
$py = "C:\projects\spiderfeet\.venv\Scripts\python.exe"
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-ng --version
# expect: 5.1.2
```

3. Launch interactive console **without** `--stealth` so marketplace can work:

```powershell
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-ng
```

4. Confirm console families: `help`, `workspaces`, `marketplace`, `modules`, `keys`, `db`.

**Important:** `--stealth` disables marketplace. Captured `recon-cli --stealth -M` shows `[!] No modules found.` Install modules first; stealth later if needed.

---

## 2) Create engagement workspace

```text
workspaces create acme-ext-2026q3
workspaces select acme-ext-2026q3
workspaces list
```

Or launch with `-w acme-ext-2026q3`. Why: isolates target data and preserves chain-of-custody for exports.

---

## 3) Configure keys and global posture

```text
keys list
keys add <provider> <value>
```

Tune globals (captured defaults include `NAMESERVER`, `PROXY`, `THREADS`, `TIMEOUT`, `USER-AGENT`, `VERBOSITY`) conservatively when stealth/quota matter. Via CLI: `recon-cli -g VERBOSITY=1 -g THREADS=5`.

Validate key-backed modules on tiny seeds before full scope.

---

## 4) Refresh marketplace and prepare modules

Still with marketplace **enabled**:

```text
marketplace refresh
marketplace search domains-hosts
marketplace info recon/domains-hosts/<module>
marketplace install recon/domains-hosts/<module>
```

Install families as needed:

- `recon/domains-hosts/*`
- `recon/domains-contacts/*`
- `recon/hosts-ports/*`
- `reporting/*`

Load one module at a time; `show info` + `show options`.

---

## 5) Seed domain and run domains → hosts

```text
modules load recon/domains-hosts/<module>
options set SOURCE example.com
run
db query SELECT COUNT(*) FROM hosts
```

If no growth: alternate module in the same path, verify SOURCE, check D/K requirements.

Headless equivalent:

```powershell
$cli = "C:\projects\spiderfeet\.tools\recon-ng\recon-cli"
& $py $cli -w acme-ext-2026q3 -m recon/domains-hosts/<module> -o SOURCE=example.com -x
```

---

## 6) Expand domains → contacts (parallel lane)

```text
modules load recon/domains-contacts/<module>
options set SOURCE example.com
run
db query SELECT * FROM contacts LIMIT 20
```

Value: people/email breadth without waiting on host→port enrichment.

---

## 7) Chain hosts → ports (SQL SOURCE)

```text
modules load recon/hosts-ports/<module>
options set SOURCE query SELECT host FROM hosts WHERE host IS NOT NULL
run
db query SELECT COUNT(*) FROM ports
```

API spend: filter to newly discovered hosts; avoid replaying the entire historical host list unless the provider/module changed.

---

## 8) Optional vulnerability enrichment

If installed modules map host/service context to vulnerability rows:

1. Confirm prerequisite tables exist
2. Bound SOURCE to priority hosts/ports
3. Capture rows for `VULNERABILITY_GENERAL` (and CVE types when present)

---

## 9) Export and reporting

```text
modules load reporting/<module>
show options
run
```

Optional review UI:

```powershell
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-web --host 127.0.0.1 --port 5000
# UI + Recon-API under /api/
```

Name artifacts `<workspace>-<family>-<timestamp>.*`.

---

## 10) SpiderFeet ingestion mapping

| Table / field | Nugget direction |
|---------------|------------------|
| domains | `INTERNET_NAME` / `DOMAIN_NAME` |
| hosts | `INTERNET_NAME`; IPs via `classify_ip` |
| contacts | `HUMAN_NAME`, `EMAILADDR`, `PHONE_NUMBER` |
| ports | `TCP_PORT_OPEN` / `UDP_PORT_OPEN` |
| vulnerabilities | `VULNERABILITY_GENERAL` |

Edges: `contains` (domain→host, host→port); `had` for descriptors. Details: `.cursor/skills/recon_ng/references/nugget-mapping.md`.

Tabs: text (spool/report) · data (SQL/reporting structured) · graph (nodes/edges from structured rows).

---

## 11) Automation upgrade path

After a successful interactive run:

1. `script record` during the validated session
2. `script execute` to replay
3. Convert to resource file → `recon-ng -r`
4. Productionize with **`recon-cli`** for SpiderFeet pipelines

```powershell
& $py C:\projects\spiderfeet\.tools\recon-ng\recon-ng -w acme-ext-2026q3 -r .\pipelines\acme-domain.rc
```

---

## 12) Troubleshooting checkpoints

| Symptom | Check |
|---------|--------|
| No modules found | Marketplace disabled (`--stealth` / `--no-marketplace`); install modules with marketplace on |
| Empty outputs | SOURCE + prerequisite table rows |
| Module failure | D/K markers, `VERBOSITY=2`, marketplace issues |
| Low yield | Pivot module family/provider |
| Quota risk | Shrink SOURCE; prioritize high-yield rows |

---

## Worked command-family examples

- **workspaces** — create/select/list for isolation
- **marketplace** — refresh/search/install/info (marketplace enabled)
- **modules** — load by path matching current table state
- **options** — explicit SOURCE + module tuning
- **keys** — providers before K modules
- **db / show** — row gates and metadata
- **reporting** — export for SpiderFeet tabs
- **recon-cli** — `-w -m -o -x` headless runs (preferred automation)
