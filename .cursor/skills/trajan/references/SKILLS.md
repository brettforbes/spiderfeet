# Trajan References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Command tree, SpiderFeet preferred flags, pointer to Captured help |
| [platforms.md](platforms.md) | Per-platform commands, auth env vars, capability notes (1.0.2) |
| [output-and-parsing.md](output-and-parsing.md) | `-o json` / sarif / html, harvest bundle notes |
| [nugget-mapping.md](nugget-mapping.md) | Redacted findings → SpiderFeet `nodes[]` / `edges[]` |
| [tactics.md](tactics.md) | Sequencing, thin yield, offensive gates |
| [sources.md](sources.md) | Official repo, blog, releases, wiki, pkg.go.dev |

**Read order for new agents**

1. `cli-options.md` — command tree and SpiderFeet defaults (`-o json`).
2. `platforms.md` — pick the right adapter and auth.
3. `output-and-parsing.md` — parse JSON; never raw secrets from retrieve/attack.
4. `nugget-mapping.md` — emit redacted graph nodes for corpus / Profiles.
5. `tactics.md` — adapt for org sweeps, offline path, ROE-gated attack.
6. `sources.md` — upstream docs when help text is insufficient.

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Trajan-Zero-to-Hero.md` | Install → enum → scan JSON → nuggets → offensive gates |
| `.docs/docs-for-cli-tools/Trajan-CLI-Options.md` | Full CLI reference + Captured help (2026-08-10) |

**Related skills:** [`../../Titus/SKILL.md`](../../Titus/SKILL.md) (secret content), [`../../nosey_parker/SKILL.md`](../../nosey_parker/SKILL.md) (legacy secrets).

**Ontology:** `.docs/docs-for-cli-tools/_Current_Ontology.md` — pipeline findings map under VULNERABILITIES / RAW descriptors; never store raw secret bytes as `nugget_data`.
