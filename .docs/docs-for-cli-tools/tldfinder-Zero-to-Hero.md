# tldfinder Zero to Hero — Private TLD Discovery, JSONL, and Nuggets

From install to orchestrated recon with **`tldfinder -oJ`**, nugget mapping, and pipelines to **dnsx → httpx → naabu**.

Skill reference: `.cursor/skills/tldfinder/SKILL.md`  
Evidence binary: `C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe` (**v0.0.2**, **2026-08-10**)

## What tldfinder does

tldfinder is ProjectDiscovery's tool for **discovering private TLDs** and related hostnames for security research. It queries curated OSINT sources and optionally **validates** with DNS (`-active`).

tldfinder does **not**:

- Replace public-zone subdomain enumeration (use **subfinder**)
- Port scan (use **naabu**)
- Probe HTTP (use **httpx**)
- Run vulnerability templates (use **nuclei**)

---

## Level 0 — Install

### Binary

```bash
go install github.com/projectdiscovery/tldfinder/cmd/tldfinder@latest
tldfinder -version
```

Or download from https://github.com/projectdiscovery/tldfinder/releases

This workspace:

```powershell
C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe -version
```

### Provider config (important)

API keys file:

- Linux/macOS: typically under the OS user config directory for `tldfinder`
- Windows: `%APPDATA%\tldfinder\provider-config.yaml`

List sources and which need keys:

```bash
tldfinder -ls
```

Without keys, free sources (`crtsh`, `dnsx`, `waybackarchive`) still work; keyed sources stay thin.

---

## Level 1 — First discovery

Private TLD **label** (not `example.com`):

```bash
tldfinder -d google
```

Pipe-friendly:

```bash
tldfinder -d google -silent
```

Save to file:

```bash
tldfinder -d google -o hosts.txt
```

README examples also accept names under a private TLD (e.g. `example.google`); the private TLD is auto-extracted.

---

## Level 2 — JSONL for automation (preferred)

```bash
tldfinder -d google -oJ -o google.jsonl
```

Example line (v0.0.2):

```json
{"host":"docs.sandbox.google","input":"google","source":"crtsh"}
```

With multi-source collection:

```bash
tldfinder -d google -oJ -cs -o google.jsonl
```

```json
{"host":"storage.google","input":"google","sources":["crtsh"]}
```

For SpiderFeet formal examination: harvest JSONL into a **single-root JSON bundle** (`records[]`); derive text from structured.

---

## Level 3 — Discovery modes

```bash
tldfinder -d google -dm dns -oJ -o dns.jsonl     # default: hosts under private TLD
tldfinder -d google -dm tld -oJ -o tld.jsonl     # TLD-oriented variants
tldfinder -d google -dm domain -oJ -o domain.jsonl
```

Start with **`-dm dns`** for private-namespace host harvesting. Treat `-dm tld` hits that look public (e.g. `google.wf`) with PSL/context checks.

---

## Level 4 — Active validation and IPs

```bash
tldfinder -d google -active -oJ -oI -o live.jsonl
```

```json
{"host":"cache2.c.play.google","ip":"142.250.183.46","input":"google","source":"crtsh"}
```

**Passive names are not guaranteed live** — validate with `-active` or **dnsx** before invasive scans.

```bash
tldfinder -d google -silent | dnsx -silent -a -aaaa
```

---

## Level 5 — Source control

```bash
tldfinder -ls
tldfinder -d google -s crtsh,dnsx,waybackarchive
tldfinder -d google -all
tldfinder -d google -es censys,whoisxmlapi
```

---

## Level 6 — Filters and rate limits

```bash
tldfinder -d google -m corp,sandbox
tldfinder -d google -f test,qa
tldfinder -d google -rl 10
tldfinder -d google -timeout 60 -max-time 30
```

File or comma-separated seeds via `-d` (v0.0.2):

```bash
tldfinder -d google,internal -oJ -o batch.jsonl
tldfinder -d seeds.txt -oJ -o from_file.jsonl
```

---

## Level 7 — Pipelines

```bash
tldfinder -d google -silent | dnsx -silent -a -aaaa | httpx -silent
tldfinder -d google -silent | dnsx -silent -a | naabu -top-ports 1000 -json -silent
```

Automation tip: add `-duc` to skip update-check noise on stderr.

---

## Level 8 — SpiderFeet nuggets (`nodes[]` / `edges[]`)

| Signal | Nugget |
|--------|--------|
| `host` (unvalidated) | `INTERNET_NAME_UNRESOLVED` |
| `host` (resolves) | `INTERNET_NAME` |
| `ip` (`-active -oI`) | `IPV4_ADDRESS` / `IPV6_ADDRESS` via `classify_ip` |
| `input` | Seed / private-TLD context |

Details: `.cursor/skills/tldfinder/references/nugget-mapping.md`

---

## Level 9 — Tactics

- **Seed diversity:** private TLD labels from certs, leaks, org intel — not public apexes.
- **Source tiering:** free sources → keyed sources → `-all`.
- **Mode contrast:** compare `-dm dns` vs `-dm tld` before claiming private namespaces.
- **Split-horizon:** alternate `-r` / `-rL` and keep both views.
- **Structured-first:** always `-oJ` for corpus; derive human text from structured.

Full playbooks: `.cursor/skills/tldfinder/references/tactics-and-workflows.md`

---

## Common pitfalls

- Feeding public domains (`example.com`) as if they were private TLD labels.
- Inventing flags (`-l`, `-min-confidence`, etc.) not present in `tldfinder -h`.
- Treating every unusual suffix as private without recurrence / PSL checks.
- Parsing banners instead of JSONL.
- Skipping dnsx/`-active` before port or HTTP scanning.
- Storing raw `.jsonl` as the CLI Profiling Structured artifact (wrap into a JSON bundle).

---

## Next references

- `.cursor/skills/tldfinder/SKILL.md`
- `.cursor/skills/tldfinder/references/SKILLS.md`
- `.docs/docs-for-cli-tools/tldfinder-CLI-Options.md`
- [tldfinder repository](https://github.com/projectdiscovery/tldfinder)
- [Enumerating private TLDs](https://cloud.google.com/blog/topics/threat-intelligence/enumerating-private-tlds)
