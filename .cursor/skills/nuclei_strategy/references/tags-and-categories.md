# Tags and Categories

Standard tags used in the official ProjectDiscovery Nuclei Templates repository, classified for selective scanning.

Source: `.seed/03EB_Rethinking_Nuclei_Strategy.md`

## Vulnerability types (bug bounty / pentesting)

| Tag | Meaning |
|-----|---------|
| `rce` | Remote code execution |
| `sqli` | SQL injection (source doc typo: `qli`) |
| `xss` | Cross-site scripting |
| `lfi` / `rfi` | Local / remote file inclusion |
| `ssrf` | Server-side request forgery |
| `ssti` | Server-side template injection |
| `deserialization` | Insecure deserialization |
| `idor` | Insecure direct object references |
| `misconfiguration` | Security misconfigurations |
| `exposure` | Exposed sensitive files, tokens, or credentials |

## Technologies and software stacks

| Tag | Meaning |
|-----|---------|
| `cve` / `cve2024` / `cve2025` | CVE-specific templates |
| `wp` / `wordpress` | WordPress core, plugins, themes |
| `jira` / `atlassian` | Atlassian Jira ecosystem |
| `aws` / `s3` / `cloud` | Cloud platforms and storage misconfigurations |
| `apache` / `nginx` / `tomcat` | Specific web servers |
| `generic` / `default-login` | Generic checks and factory-default credentials |
| `panel` / `admin` | Control panels and administrative interfaces |

## Protocol and infrastructure

| Tag | Meaning |
|-----|---------|
| `http` | Web application targets |
| `dns` | DNS routing and records |
| `tcp` / `udp` | Network-level port / raw socket checks |
| `ssl` / `tls` | Certificate and weak TLS configuration |
| `fuzz` | Fuzzing templates — **disabled by default**; requires `-itags fuzz` |
| `osint` | Open-source intelligence / profile gathering |

## Phase mapping (strategy use)

| Examination phase | Suggested tags |
|-------------------|----------------|
| A — Fingerprint | `tech`, stack tags from hits (`apache`, `wordpress`, …) |
| B — Secrets / leaks | `exposure`, `misconfiguration` |
| C — Access | `panel`, `admin`, `default-login` |
| D — CVE depth | `cve`, `cve2024`, `cve2025`, stack-specific CVE tags |
| E — API | `http` + workflow-driven API templates (see api-pentest doc) |

## Related

- [selective-scan-techniques.md](selective-scan-techniques.md)
- [../../nuclei/references/templates-and-workflows.md](../../nuclei/references/templates-and-workflows.md)
