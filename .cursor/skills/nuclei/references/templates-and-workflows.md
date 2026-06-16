# Nuclei Templates and Workflows

## Templates overview

Nuclei templates are YAML files describing **how to probe a target** and **what response patterns constitute a match**. The community template repository (`nuclei-templates`) contains thousands of checks organized by protocol, tag, and severity.

Official references:

- [Introduction](https://docs.projectdiscovery.io/templates/introduction)
- [Template structure](https://docs.projectdiscovery.io/templates/structure)
- [FAQ](https://docs.projectdiscovery.io/templates/faq)

## Template file structure

```yaml
id: example-detect

info:
  name: Example Detection
  author: pdteam
  severity: info
  description: Detects example service
  tags: tech,example
  reference:
    - https://example.com/docs

http:
  - method: GET
    path:
      - "{{BaseURL}}/"
    matchers:
      - type: word
        words:
          - "ExampleServer"
        part: body
```

### Key sections

| Section | Purpose |
|---------|---------|
| `id` | Unique template ID (used in JSONL `template-id`) |
| `info` | Metadata: name, severity, tags, references |
| `http` / `dns` / `ssl` / `tcp` / `file` / `headless` / `code` | Protocol blocks |
| `matchers` | Conditions that mark a finding |
| `extractors` | Pull values from responses into `extracted-results` |
| `variables` | Template-local variables |
| `payloads` | Fuzzing payload definitions |
| `workflow` | Sub-template orchestration (in workflow files) |

## Protocols

| Protocol | Doc | Use case |
|----------|-----|----------|
| HTTP | [basic HTTP](https://docs.projectdiscovery.io/templates/protocols/http/basic-http) | Web apps, APIs, panels |
| Raw HTTP | [raw HTTP](https://docs.projectdiscovery.io/templates/protocols/http/raw-http) | Custom requests |
| DNS | [DNS](https://docs.projectdiscovery.io/templates/protocols/dns) | DNS takeovers, records |
| Network | [network](https://docs.projectdiscovery.io/templates/protocols/network) | TCP/UDP banners |
| SSL | (under network/ssl) | Certificate issues |
| Headless | [headless](https://docs.projectdiscovery.io/templates/protocols/headless) | Browser-based checks |
| File | [file](https://docs.projectdiscovery.io/templates/protocols/file) | Local file audit |
| Flow | [flow](https://docs.projectdiscovery.io/templates/protocols/flow) | Multi-step logic |
| Multi-protocol | [multi-protocol](https://docs.projectdiscovery.io/templates/protocols/multi-protocol) | Combined probes |

SpiderFeet default scan uses the **full template tree** minus tags `dos`, `fuzz`, `misc`.

## Matchers and extractors

- [Matchers](https://docs.projectdiscovery.io/templates/reference/matchers) — `word`, `regex`, `status`, `dsl`, `binary`, etc.
- [Extractors](https://docs.projectdiscovery.io/templates/reference/extractors) — capture versions, tokens, paths
- Matcher name appears in JSONL as `matcher-name` (drives SpiderFeet non-CVE events)

## Tags (selection strategy)

Common community tags:

| Tag | Typical findings |
|-----|------------------|
| `cve` | Known CVE checks |
| `tech` | Technology stack fingerprint |
| `exposure` | Sensitive paths, leaks |
| `misconfig` | Configuration mistakes |
| `panel` | Admin/login panels |
| `default-login` | Default credentials |
| `takeover` | Subdomain/service takeover |
| `dos` | Denial-of-service (**excluded** in SpiderFeet) |
| `fuzz` | Fuzzing (**excluded**) |
| `misc` | Miscellaneous noisy (**excluded**) |

Use `-tags` / `-etags` / `-severity` to shape signal vs noise.

## Workflows

Workflows chain templates: run child templates only when parent matches.

- [Overview](https://docs.projectdiscovery.io/templates/workflows/overview)
- [Examples](https://docs.projectdiscovery.io/templates/workflows/examples)

```yaml
id: wordpress-workflow

info:
  name: WordPress Security Checks
  author: pdteam
  severity: info

workflows:
  - template: technologies/wordpress-detect.yaml
    subtemplates:
      - tags: wordpress
      - tags: cve,wordpress
```

Run with:

```bash
nuclei -w workflows/ -t nuclei-templates/ -u https://target -jsonl -silent
```

## Custom templates

1. Copy an existing template from `nuclei-templates` as a skeleton.
2. Set unique `id`, accurate `info.severity` and `tags`.
3. Validate: `nuclei -validate -t my-template.yaml`
4. Test: `nuclei -id my-template-id -u https://staging-target -jsonl -debug`
5. Add to a private template directory referenced by `-t`.

**Severity guidance for SpiderFeet mapping:**

- `info` + matcher → `WEBSERVER_TECHNOLOGY`
- `low`–`critical` + matcher → `VULNERABILITY_GENERAL`
- CVE string anywhere in JSON line → tiered `VULNERABILITY_CVE_*`

## Authenticated scans

Templates can use secrets from `-secret-file` or `-auth` config. Required for findings behind login. Not integrated in `sfp_tool_nuclei` today—manual or future module option.

## Template maintenance

```bash
# Official update
nuclei -update-templates

# Git pull community repo
git -C /path/to/nuclei-templates pull --ff-only

# List templates matching filter
nuclei -tl -tags cve -severity critical
```

Pin template commits in production for reproducible scans.

## Fuzzing and DAST

Fuzzing templates (`-fuzz`, `-dast`, tag `fuzz`) can generate high request volume and trigger WAFs. SpiderFeet excludes `fuzz` tag via `-etags`. Use only on authorized staging with rate limits.

## Related

- [tactics.md](tactics.md) — when to narrow/widen template sets
- [cli-options.md](cli-options.md) — `-t`, `-w`, `-tags`, `-id`
