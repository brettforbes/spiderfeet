# Nuclei CLI Options (Reference)

Grouped flags for [ProjectDiscovery Nuclei](https://docs.projectdiscovery.io/opensource/nuclei/running). Run `nuclei -h` for the installed version—flags evolve between releases.

## SpiderFeet module defaults (`sfp_tool_nuclei`)

Fixed argument vector in `modules/sfp_tool_nuclei.py`:

| Flag | Value | Rationale |
|------|-------|-----------|
| `-silent` | — | Suppress banner/progress; stdout is JSONL only |
| `-jsonl` | — | One JSON object per finding line |
| `-concurrency` | `100` | Parallel template executions |
| `-retries` | `1` | Single retry on transient failures |
| `-t` | template directory | Full template tree |
| `-no-interactsh` | — | Disable OOB Interactsh callbacks |
| `-etags` | `dos,fuzz,misc` | Exclude disruptive/noisy template tags |

Targets are passed on **stdin** (one host/URL per line). No `-u` flag in module.

---

## Target input

| Flag | Description |
|------|-------------|
| `-u`, `-target` | Single target URL/host |
| `-l`, `-list` | File with one target per line |
| `-eh`, `-exclude-hosts` | Hosts to exclude from list |
| stdin | Targets when no `-u`/`-l` (SpiderFeet pattern) |

**Input formats:** URLs, hosts, IPs, ASNs (version-dependent), combinations per [input formats](https://docs.projectdiscovery.io/opensource/nuclei/input-formats).

---

## Template selection

| Flag | Description |
|------|-------------|
| `-t`, `-templates` | Template directory or file path |
| `-w`, `-workflows` | Workflow directory or file |
| `-tl` | List available templates |
| `-id` | Run specific template ID(s), comma-separated |
| `-tags` | Include templates with tag(s) |
| `-etags` | Exclude templates with tag(s) |
| `-itags` | Include tags (intersection semantics per version) |
| `-severity` | Filter: `info`, `low`, `medium`, `high`, `critical`, `unknown` |
| `-author` | Filter by template author |
| `-type` | Protocol type: `http`, `dns`, `ssl`, `file`, `network`, etc. |
| `-template-url` | Remote template URL |
| `-code` | Enable code protocol templates |
| `-sign` | Require signed templates only |
| `-validate` | Validate templates without running |
| `-ud`, `-update-templates` | Update official template repo |
| `-duc`, `-disable-update-check` | Skip update check |

---

## Output

| Flag | Description |
|------|-------------|
| `-jsonl` | JSON Lines (one object per match) — **SpiderFeet uses this** |
| `-j`, `-json` | JSON export (format varies by version) |
| `-o`, `-output` | Write results to file |
| `-s`, `-silent` | Minimal console output |
| `-v`, `-verbose` | Verbose logging |
| `-debug` | Debug mode |
| `-stats` | Show scan statistics |
| `-si`, `-stats-interval` | Stats print interval |
| `-me`, `-markdown-export` | Markdown report path |
| `-se`, `-sarif-export` | SARIF export path |
| `-je`, `-json-export` | JSON export path |
| `-nc`, `-no-color` | Disable ANSI colors |
| `-nm`, `-no-meta` | Omit metadata in output |
| `-ts`, `-timestamp` | Include timestamp in output |
| `-rdb`, `-report-db` | Report database path |
| `-ms`, `-matcher-status` | Print matcher status |

---

## Rate limiting and performance

| Flag | Description |
|------|-------------|
| `-c`, `-concurrency` | Max parallel templates (SpiderFeet: `100`) |
| `-bs`, `-bulk-size` | Hosts processed in parallel per template |
| `-rl`, `-rate-limit` | Max requests per second |
| `-rlm`, `-rate-limit-minute` | Requests per minute |
| `-timeout` | Request timeout (seconds) |
| `-retries` | Retry count (SpiderFeet: `1`) |
| `-mhe`, `-max-host-error` | Max errors per host before skip |
| `-project` | Use project folder for caching |
| `-spm`, `-stop-at-first-match` | Stop template after first match on host |

---

## Network and HTTP

| Flag | Description |
|------|-------------|
| `-H`, `-header` | Custom header `Header: value` |
| `-V`, `-var` | Custom variable `key=value` |
| `-r`, `-resolvers` | DNS resolver file |
| `-system-resolvers` | Use system DNS |
| `-passive` | Passive-only templates |
| `-follow-redirects` | Follow HTTP redirects |
| `-fr`, `-follow-host-redirects` | Follow redirects on same host |
| `-max-redirects` | Redirect limit |
| `-disable-redirects` | Do not follow redirects |
| `-fhr`, `-force-http2` | Force HTTP/2 |
| `-ip-version` | `4`, `6`, or `4,6` |
| `-interactsh-server` | Custom Interactsh server |
| `-no-interactsh` | Disable Interactsh — **SpiderFeet default** |
| `-iserver`, `-interactsh-url` | Interactsh URL override |
| `-fuzz` | Enable fuzzing templates |
| `-dast` | Enable DAST mode |
| `-profile` | Scan profile (e.g. `quick`, `full`) |

---

## Authentication and secrets

| Flag | Description |
|------|-------------|
| `-secret-file` | Secrets for authenticated scans |
| `-auth` | Authenticated scan config |

See [authenticated scans](https://docs.projectdiscovery.io/opensource/nuclei/authenticated-scans).

---

## Filtering and scope

| Flag | Description |
|------|-------------|
| `-exclude-tags` | Alias for exclude tag behavior (prefer `-etags`) |
| `-include-tags` | Include-only tags |
| `-exclude-id` | Exclude template IDs |
| `-exclude-severity` | Exclude severity levels |
| `-exclude-type` | Exclude protocol types |
| `-include-rr` | Include request/response in output |
| `-omit-raw` | Omit raw request/response |
| `-omit-template` | Omit embedded template in output |

---

## CI/CD and reporting

| Flag | Description |
|------|-------------|
| `-cloud` | Run on ProjectDiscovery Cloud |
| `-dashboard` | Upload to PD dashboard |
| `-report-config` | Reporting configuration file |
| `-tp`, `-template-path` | Additional template paths |

See [CI/CD integration](https://docs.projectdiscovery.io/opensource/nuclei/ci-cd).

---

## Configuration file

Nuclei supports `config.yaml` in user config directory for persistent defaults. CLI flags override config.

Example `~/.config/nuclei/config.yaml` snippets:

```yaml
templates-directory: /opt/nuclei-templates
severity: critical,high,medium
tags: cve
rate-limit: 150
no-interactsh: true
```

---

## Common flag combinations

```bash
# SpiderFeet-equivalent
nuclei -silent -jsonl -concurrency 100 -retries 1 -t ./templates \
  -no-interactsh -etags dos,fuzz,misc

# CVE-only, high signal
nuclei -silent -jsonl -tags cve -severity critical,high -t ./templates -no-interactsh

# Technology fingerprint
nuclei -silent -jsonl -tags tech -severity info -t ./templates -no-interactsh

# Single template debug (manual)
nuclei -id panel-detect -u https://target -jsonl -debug -no-interactsh

# Mass scan file with rate limit
nuclei -l targets.txt -jsonl -silent -rate-limit 50 -c 25 -t ./templates -no-interactsh
```

---

## Version notes

- Prefer `-jsonl` over legacy `-json` for streaming parsers.
- Template tag names are lowercase in community templates (`cve`, `tech`, `exposure`, `misconfig`, `panel`, etc.).
- Some flags renamed across v2/v3; verify with `nuclei -h` on the deployment host.
