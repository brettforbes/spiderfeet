# Titus References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Command tree, SpiderFeet preferred flags, pointer to Captured help |
| [output-and-parsing.md](output-and-parsing.md) | Datastores, `--format json` / sarif, harvest bundle notes |
| [nugget-mapping.md](nugget-mapping.md) | Redacted findings → SpiderFeet `nodes[]` / `edges[]` |
| [tactics.md](tactics.md) | Sequencing, thin yield, GitHub/Docker/SaaS tactics |
| [sources.md](sources.md) | Official repo, blog, releases, pkg.go.dev |

**Read order for new agents**

1. `cli-options.md` — command tree and SpiderFeet defaults (`--format json`).
2. `output-and-parsing.md` — parse JSON from `scan`/`report`; never raw secrets.
3. `nugget-mapping.md` — emit redacted graph nodes for corpus / Profiles.
4. `tactics.md` — adapt for monorepos, Docker layers, noisy rules, SaaS enum.
5. `sources.md` — upstream docs when help text is insufficient.

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Titus-Zero-to-Hero.md` | Install → scan → JSON report → triage → nuggets |
| `.docs/docs-for-cli-tools/Titus-CLI-Options.md` | Full CLI reference + Captured help (2026-08-10) |

**Related skills:** [`../../nosey_parker/SKILL.md`](../../nosey_parker/SKILL.md) (legacy), [`../../trajan/SKILL.md`](../../trajan/SKILL.md) (CI supply-chain — different tool).

**Ontology:** `.docs/docs-for-cli-tools/_Current_Ontology.md` — secret findings map under SECURITY / leak descriptors; never store raw secret bytes as `nugget_data`.
