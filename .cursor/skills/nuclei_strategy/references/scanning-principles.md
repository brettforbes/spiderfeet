# Scanning Principles

From `.seed/03EB_Rethinking_Nuclei_Strategy.md` — core strategy for high-signal Nuclei runs.

## Start looking for

- **Misconfiguration** templates
- **Exposure** templates
- **Authentication & access-control** related checks
- **Technology-specific** templates — only when Phase A (fingerprint) shows that stack is present

## Avoid

- Broad **informational** template sets when the goal is CVE or critical/high evidence
- **Low-confidence generic** checks that do not chain to deeper testing

## Chainability gate

Before including a template category, ask:

> **“If this template hits, can I chain it?”**

If the answer is **no**, skip it for that batch.

Examples of chainable hits:

- Tech fingerprint → stack-specific CVE templates
- Exposed swagger → API BOLA / mass-assignment / SQLi workflow
- Panel detected → default-login templates
- WordPress detected → WordPress + supplemental Wordfence CVE templates

## Batch discipline

Think in **batches**, not monolithic “scan everything” runs:

| Dimension | Pick one per run |
|-----------|------------------|
| Target group | e.g. one host, one small site, one staging URL |
| Risk category | exposure, auth, CVE, misconfig, panel, API |
| Goal | stated outcome for the examination scenario |

### Example batch goals

- “This scan is only looking for **exposed admin panels**”
- “This run is only about **auth misconfigurations**”
- “This scan is just **tech fingerprinting for chaining**”

## Examination tuning lesson (corpus context)

| Pattern | Typical outcome | Strategy fit |
|---------|-----------------|--------------|
| Full templates on **permissive lab host** (e.g. scanme) | medium / low / info findings | Good for **severity semantics** scenarios |
| Full templates on **hardened CDN property** | mostly low-value `info` noise | Poor CVE corpus; switch to selective tags or different target class |
| Critical+high only on **hardened corporate sites** | often **empty JSONL** | Valid clean-miss; not a substitute for rich CVE discovery |

Prefer **smaller, less-protected targets** and **sequential chained passes** when the goal is critical, high, or CVE-class JSONL records.

## Related

- [sequential-playbook.md](sequential-playbook.md)
- [selective-scan-techniques.md](selective-scan-techniques.md)
