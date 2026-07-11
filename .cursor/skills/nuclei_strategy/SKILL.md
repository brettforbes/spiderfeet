---
name: nuclei_strategy
description: Plan sequential, tag-targeted Nuclei scan batches for CLI examination—tech fingerprint first, then chained CVE/exposure/auth/misconfig passes on smaller permissive targets. Trigger when retuning nuclei corpus scenarios, avoiding full-template noise on hardened sites, or hunting critical/high/CVE JSONL records.
---

# Nuclei Strategy — Sequential Targeted Scanning

## Purpose

Use when designing or re-running **Nuclei CLI examination scenarios** that need **high-signal JSONL** (especially critical, high, medium, and CVE-class findings) instead of low-value informational noise from full-template sweeps on hardened targets.

Read the execution skill first: [`.cursor/skills/nuclei/SKILL.md`](../nuclei/SKILL.md) for binary defaults, JSONL parsing, and SpiderFeet mapping.

## Step-by-Step Instructions

1. **Define one batch goal** — Pick exactly one target group, one risk category, and one outcome per run (e.g. “exposed admin panels only”, “auth misconfigurations only”, “tech fingerprint for chaining”). Do not combine unrelated goals in a single examination scenario.
2. **Prefer smaller, less-hardened targets** — Favor permissive lab or smaller sites over major CDN-backed properties when the goal is critical/high/CVE evidence. Full-template runs on hardened sites often yield only low-value `info` noise or empty critical/high passes.
3. **Phase A — Technology fingerprint (chaining input)** — Run a narrow tech-discovery pass before vulnerability depth:
   - `nuclei -u <target> -tags tech -severity info -silent -jsonl -no-interactsh` (or equivalent tag sweep).
   - Parse JSONL; note stack tags (`wordpress`, `apache`, `nginx`, `jira`, `aws`, etc.) and exposed surfaces (panels, swagger paths, metrics).
4. **Phase B — Selective vulnerability passes** — Based on Phase A hits, run **separate** batched scans (one category per command):
   - CVE-focused: `-tags cve` (include year tags like `cve2024`, `cve2025` when relevant).
   - Exposure: `-tags exposure` or `-t ~/nuclei-templates/exposures/` (`.env`, `.git`, configs, API keys, backups).
   - Panels / admin: `-tags panel,exposure` or `-tags panel,admin`.
   - Misconfiguration: `-tags misconfiguration`.
   - Auth / access: templates for default logins (`-t ~/nuclei-templates/default-logins/`) or auth-related tags.
   - Stack-specific: e.g. `-tags wordpress`, `-tags apache`, `-tags joomla` only after stack confirmed in Phase A.
5. **Phase C — Severity escalation** — After signal appears, tighten or widen deliberately:
   - Hunt critical/high: `-severity critical -severity high` (repeat per platform flag rules).
   - If only medium/low/info so far on a permissive target, that may still be valid examination evidence for severity semantics—do not treat as failure.
   - If empty on hardened target after selective passes, do not rerun full 12k+ template tree; change target class or chaining inputs instead.
6. **Phase D — Workflow chaining (when parent detection exists)** — When API or multi-step attack surface is suspected, use Nuclei workflows so subtemplates run only after parent match (e.g. swagger-detect → BOLA / mass-assignment / SQLi). See [`references/api-pentest-techniques.md`](references/api-pentest-techniques.md).
7. **Capture evidence per batch** — Each scenario gets its own command, JSONL export, and structured JSON bundle (`records[]` list of dicts). Name scenarios by **goal + target + tag/severity slice**, not “all templates” unless explicitly profiling severity semantics on a known-good permissive host.
8. **Evaluate chainability before adding templates** — For every template category, ask: “If this hits, can I chain it?” If no, skip it for that batch.
9. **Record follow-up matrix** — Document which Phase A signals triggered which Phase B/C commands and whether JSONL contained CVE IDs, critical/high severities, or clean miss.

## If/Then Decision Rules

| If | Then |
|----|------|
| Goal is CVE / critical / high evidence | Do **not** start with full template tree on CDN-backed corporate sites; use selective tags + smaller targets first |
| Full-template run produces only `info` tech noise | Accept as low-value for CVE goals; rerun with `-tags cve`, `exposure`, `misconfiguration`, `panel`, or stack-specific tags |
| Phase A identifies WordPress | Run `-tags wordpress`; consider additional Wordfence CVE templates per strategy doc |
| Phase A identifies Apache / Joomla / Atlassian | Run matching stack tags (`apache`, `joomla`, `jira`) before broad CVE tree |
| Need exposed secrets or configs | Run `exposures/` template path or `-tags exposure` batch |
| Need default credentials | Run `default-logins/` template path batch |
| API surface suspected | Run swagger/OpenAPI detection, then workflow subtemplates (BOLA, mass assignment, SQLi) |
| Selective passes all empty on hardened target | Change target (smaller/less protected) or enrich Phase A; do not equate empty with scanner failure |
| Permissive target returns medium/low findings | Valid examination for severity semantics; capture as structured scenario |
| Windows command line | Use repeated `-severity` flags (`-severity critical -severity high`), not comma-joined single flag |
| Need fuzz templates | Requires `-itags fuzz`; excluded by SpiderFeet default `-etags dos,fuzz,misc`—manual authorized runs only |
| Chaining question answer is “no” | Omit that template category from the batch |

## Guardrails & Pitfalls

- **Do not run everything by default** — Full-template examinations on hardened sites produce noise (e.g. CDN/TLS/info-only) or empty critical/high exports; they are poor CVE corpus scenarios.
- **Avoid broad informational sets** and **low-confidence generic checks** when the goal is actionable vulnerability evidence.
- **One batch, one goal** — Mixing admin-panel, auth, CVE, and tech fingerprinting in one run obscures which inputs produced signal.
- **Authorized targets only** — Same authorization rules as the base Nuclei skill.
- **Keep SpiderFeet-safe defaults** unless operator explicitly overrides: `-no-interactsh`, `-etags dos,fuzz,misc`, `-jsonl`, `-silent`.
- **Do not treat template count as coverage** — Nuclei emits JSONL only for matches; running all templates ≠ one line per template.
- **Corporate CDN targets** — Expect clean critical/high misses; use them for negative fixtures, not rich CVE discovery.
- **JSONL → structured JSON** — Convert NDJSON to `records[]` bundles for examination artifacts (see CLI corpus harvest pattern).
- **Template drift** — Pin or update template trees deliberately; CVE year tags (`cve2024`, `cve2025`) matter for selective passes.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `scanning-principles.md` | Signal-over-volume, chainability, batch goals |
| `tags-and-categories.md` | Official template tags by category |
| `selective-scan-techniques.md` | Tag/severity/path-specific commands |
| `high-value-targets.md` | Chaining targets and exposure classes |
| `api-pentest-techniques.md` | Swagger, BOLA, mass assignment, workflows |
| `sequential-playbook.md` | Multi-phase scan sequences for examination tuning |
| `sources.md` | Upstream strategy doc and related skills |
