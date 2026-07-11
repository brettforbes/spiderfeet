# Creating a Skill and Documentation for httpx — HTTP Probing and Web Surface Discovery

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for **ProjectDiscovery httpx** (not the unrelated Python `httpx` HTTP client or Kali `httpx-toolkit`). When we probe hosts and URLs for live HTTP services, we will export results as **JSON Lines** (`-j` / `-json`), parse them into a structured bundle (`records[]`), and convert those results to nested nuggets (`HTTP_CODE`, `WEBSERVER_TECHNOLOGY`, `WEBSERVER_BANNER`, `WEBSERVER_HTTPHEADERS`, `INTERNET_NAME`, `IP_ADDRESS`, `LINKED_URL_INTERNAL`, and optional `TARGET_WEB_CONTENT` when body capture is in scope).

This skill will teach you how to use httpx to **find live web servers**, fingerprint technologies, and characterize HTTP responses. More importantly it should teach you how to adapt your technique and sequence of operations to maximise useful web-surface data from any target set — permissive labs, CDN-fronted sites, redirect-heavy apps, and hosts that only answer on non-default ports or schemes.

You will use this skill to exercise httpx in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

The total source material, from code to docs to blog posts enables you to get the widest view on the source material you are going to capture into the skill and documentation.

- https://github.com/projectdiscovery/httpx
- https://github.com/projectdiscovery/httpx/tree/dev/cmd/httpx
- https://github.com/projectdiscovery/httpx/tree/dev/examples
- https://github.com/projectdiscovery/httpx/tree/dev/common
- https://github.com/projectdiscovery/httpx/tree/dev/runner
- https://docs.projectdiscovery.io/opensource/httpx/overview
- https://docs.projectdiscovery.io/opensource/httpx/install
- https://docs.projectdiscovery.io/opensource/httpx/running
- https://docs.projectdiscovery.io/opensource/httpx/usage

Some httpx articles and tutorials

- https://projectdiscovery.io/blog/introducing-httpx-dashboard-2
- https://www.hackingarticles.in/a-detailed-guide-on-httpx/
- https://www.geeksforgeeks.org/linux-unix/httpx-fast-and-multi-purpose-http-toolkit-in-kali-linux/
- https://securitycipher.com/httpx-tutorial/
- https://medium.com/search?q=projectdiscovery%20httpx
- https://infosecwriteups.com/search?q=httpx
- https://systemweakness.com/search?q=httpx
- https://hacklido.com/search?query=httpx
- https://www.youtube.com/results?search_query=projectdiscovery+httpx
- https://www.youtube.com/results?search_query=httpx+projectdiscovery+tutorial

**Do not** treat https://www.kali.org/tools/httpx-toolkit/ as primary source material — that is a different product. Always anchor on **ProjectDiscovery httpx**.

## Instructions

Based strictly on the provided source materials (and SpiderFeet ontology docs below), generate the following things:

1. **Skill Trigger & Description (Max 50 words):** A highly specific description of what this skill does and exactly when the AI should trigger it. Include trigger words: HTTP probe, live web server, status code, title, tech-detect, Wappalyzer-style fingerprint, CDN/WAF, redirect chain, pipe from subfinder/dnsx/naabu, JSONL export, `WEBSERVER_TECHNOLOGY` nuggets.

2. **SKILL.md Content** (`.cursor/skills/httpx/SKILL.md`): Deconstruct the workflows from the docs into clear, step-by-step instructions for the AI. Organize using these headers:

   - **Purpose:** When to use this skill (HTTP probing after host discovery, not passive subdomain enum).
   - **Step-by-Step Instructions:** Logical execution order (scope → input prep → probe flags → JSONL capture → parse → nugget map → chain downstream).
   - **If/Then Decision Rules:** Edge cases (stdin host vs URL, HTTP/HTTPS fallback, `-no-fallback`, CDN `-exclude-cdn`, matchers/filters, empty results, redirects, non-web ports).
   - **Guardrails & Pitfalls:** Authorization, rate limits, body/response storage size, confusing with Python httpx, headless/screenshot cost, etc.
   - **References:** Point to `references/SKILLS.md`.
   - **Comprehensive Examples:** At least one example per major flag group (INPUT, PROBES, OUTPUT `-json`, MATCHERS/FILTERS, RATE-LIMIT, ports/paths, pipelines).
   - **Strategies and Tactics:** Sequences that adapt when yield is thin, noisy, CDN-fronted, or rate-limited.

3. **References Directory** (`.cursor/skills/httpx/references/`), indexed through `SKILLS.md`. Minimum files:

   | File | Contents |
   |------|----------|
   | `SKILLS.md` | Index and read order |
   | `cli-options.md` | All flags grouped (INPUT, PROBES, HEADLESS, MATCHERS, EXTRACTOR, FILTERS, RATE-LIMIT, OUTPUT, CONFIGURATIONS, DEBUG, OPTIMIZATIONS) |
   | `json-output-schema.md` | JSONL field reference (`-j`, `-irh`, `-include-chain`, tech-detect fields, etc.) |
   | `nugget-mapping.md` | JSONL → SpiderFeet nuggets + `nodes[]`/`edges[]` contract |
   | `probes-matchers-filters.md` | Probe toggles and when to use matchers vs filters |
   | `workflows-and-phases.md` | Pipelines: subfinder → dnsx → httpx → naabu → nuclei |
   | `tactics.md` | CDN, redirects, port/scheme tuning, thin vs rich targets |
   | `config-and-ports.md` | `config.yaml`, `-p` port syntax, `-path`, TLS/CSP probes |
   | `sources.md` | Official URLs and articles |

4. **Zero to Hero Document** (`.docs/docs-for-cli-tools/Httpx-Zero-to-Hero.md`): Progressive guide from install → first probe → JSONL → nugget mapping → recon pipelines. **Not** Subfinder; focus on HTTP probing and web surface discovery.

5. **CLI Options Documentation** (`.docs/docs-for-cli-tools/Httpx-CLI-Options.md`): Full httpx CLI reference with grouped flags and copy-paste examples.

Follow the same depth and tone as existing library skills: `.cursor/skills/subfinder/SKILL.md`, `.cursor/skills/naabu/SKILL.md`, `.cursor/skills/nuclei/SKILL.md`.

## Ontology and nugget alignment

Map httpx findings into the **unified CLI profiling ontology** — do not invent a parallel vocabulary.

| httpx signal | Preferred nugget_id | Notes |
|--------------|-------------------|-------|
| Final URL / probed host | `INTERNET_NAME` or `LINKED_URL_INTERNAL` | Scheme + host + path policy per scenario |
| Resolved IP in JSON | `IP_ADDRESS` | Edge `resolves_to` when host present |
| `status_code` | `HTTP_CODE` | Store numeric code as `data` |
| `webserver` / Server header | `WEBSERVER_BANNER` | Banner string |
| Response headers (full) | `WEBSERVER_HTTPHEADERS` | When `-irh` or header capture in scope |
| `tech` / `-td` detections | `WEBSERVER_TECHNOLOGY` | One node per technology; Wappalyzer-style names |
| CDN/WAF provider field | metadata or `PROVIDER_HOSTING` | When catalogue supports it |
| Body snippet / stored response | `TARGET_WEB_CONTENT` | Only when examination scenario includes body capture |
| Title | metadata on URL/host node | Or descriptor if extension nugget added later |

Read before mapping:

- `.docs/docs-for-cli-tools/_Current_Ontology.md` — httpx extends **APPLICATIONS** / web layer on qualified `HOST` after L3/L4 discovery (Netdiscover/Nmap/Naabu sub-graphs).
- `.docs/analysis/nuggets.json` + `.docs/analysis/nuggets_extension.json` — canonical `nugget_id`, colours, icons.
- `.seed/05_Onotology_for_Nuggets.md` — category and relation rules (`contains`, `had`, `listens-to`).
- `.cursor/rules/proj-05-spiderfeet-nugget-ontology.mdc` — enforceable graph constraints.

**Downstream chain position:** httpx sits **after** host/subdomain resolution (`subfinder`, `dnsx`) and often **after or alongside** port discovery (`naabu`, `nmap`); it feeds **nuclei**, **webanalyze**, and **Julius** on confirmed HTTP URLs.

## CLI profiling alignment

When exercising httpx for the SpiderFeet corpus, follow `.cursor/skills/cli_app_profiling/SKILL.md` and `.cursor/rules/proj-06-spiderfeet-cli-app-exercising.mdc`:

- Draft a **semantic outcome matrix** before formal examination. Minimum rows to plan:

  | Outcome class | Example scenario |
  |---------------|------------------|
  | Rich web row | 200 + title + tech-detect on permissive lab |
  | Redirect chain | 301/302 with `-include-chain` |
  | Auth / forbidden | 401/403 (filter or document as negative) |
  | CDN/WAF front | `-cdn` metadata; `-exclude-cdn` behaviour |
  | Non-web / connection refused | clean miss from IP:port with no HTTP |
  | Timeout / host error | `-max-host-error`, slow target |
  | HTTP vs HTTPS fallback | default probe vs `-no-fallback` |
  | Duplicate/near-duplicate pages | `-filter-duplicates` |
  | Stdin pipeline | `subfinder \| httpx -json -silent` |
  | Invalid/malformed input | bad URL or empty stdin |

- **Explore with `-j` / `-json` JSONL** during discovery; at **harvest**, convert to a single JSON bundle with `schema`, metadata, and `records[]` (not raw `.jsonl` as the examination structured artifact — same rule as Nerva/Pius/Nuclei).
- Validate **input forms** in exploration before locking manifests: host `example.com`, URL `https://example.com`, `host:port`, list file `-l`, stdin — document which forms the corpus uses.
- Implement harvest support when landing formal scenarios: `httpx_structured.py`, manifest `structured_ext: json`, graph builder reading `records[]`.
- Chain documentation must show: **subfinder → dnsx → httpx → naabu → nuclei** (and where httpx repeats after naabu on open web ports).

## Best Practices for Library Skills

When reviewing the AI's output, ensure your final skill file follows these platform-standard rules:

- **Meaning and Goals:** The skill should tell the AI *why* each probe matters (live surface confirmation, tech stack for nuclei tags, redirect discovery) and how operations combine into recon goals.
- **Focus on Workflows over Features:** Tell the AI how to probe a host list for live HTTP services and map results — not merely list every flag.
- **Comprehensive Documentation:** Every major flag group belongs in `references/`; `cli-options.md` should be exhaustive enough that the agent rarely needs the web.
- **Keep Descriptions Distinct:** The trigger must not overlap with `subfinder` (passive DNS), `naabu` (port scan), or `nuclei` (vuln templates). httpx = **HTTP probe and web fingerprint**.
- **Include Comprehensive Examples:** SKILL.md includes examples for INPUT modes, common PROBES (`-status-code -title -tech-detect -server -cdn -ip`), JSONL output, matchers/filters, rate limits, ports/paths, and stdin pipelines.
- **Strategies and Tactics:** Document adaptation when: only 80/443 respond; tech-detect empty behind CDN; need `-probe-all-ips`; widen with `-path`; tighten with `-match-code` / `-filter-code`; lower `-threads` / `-rate-limit` on fragile targets.

## Deliverable checklist

Before marking the skill complete, verify:

- [ ] `SKILL.md` frontmatter `name: httpx` and ≤50-word `description`
- [ ] No Subfinder/Naabu wording left in httpx docs (except pipeline chain mentions)
- [ ] `references/SKILLS.md` indexes all reference files
- [ ] `nugget-mapping.md` cites catalogue ids from `nuggets.json`
- [ ] Zero-to-Hero and CLI-Options filenames use **`Httpx-`** prefix
- [ ] JSONL flag documented as **`-j` / `-json`** (not subfinder's `-oJ`)
- [ ] Cross-links to `subfinder`, `dnsx`, `naabu`, `nuclei` skills for pipeline context
