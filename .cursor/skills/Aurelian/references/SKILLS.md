# Aurelian References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Command tree, SpiderFeet preferred flags, Captured help pointer |
| [output-and-parsing.md](output-and-parsing.md) | `-f` / `--output-dir`, module artifact handling |
| [nugget-mapping.md](nugget-mapping.md) | Cloud findings → SpiderFeet `nodes[]` / `edges[]` |
| [tactics.md](tactics.md) | Sequencing, rich/sparse/error, OPSEC and scope tactics |
| [sources.md](sources.md) | Official repo, blog, releases, docs |

**Read order for new agents**

1. `cli-options.md` — 1.0.4 command tree and SpiderFeet defaults (`-f` structured files).
2. `output-and-parsing.md` — how to treat module outputs and Windows ERROR quirk.
3. `nugget-mapping.md` — map exposures/secrets/IAM/DNS to catalogue nugget ids.
4. `tactics.md` — adapt for secrets-first, IAM offline, takeover, Azure APIM ROE.
5. `sources.md` — upstream docs when help text is insufficient (verify flags against Captured help).

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Aurelian-Zero-to-Hero.md` | Install → whoami → secrets/exposure/IAM/takeover → nuggets |
| `.docs/docs-for-cli-tools/Aurelian-CLI-Options.md` | Full CLI reference + Captured help (**2026-08-10**) |

**Related skills:** [`../../Titus/SKILL.md`](../../Titus/SKILL.md) (secret engine used by `find-secrets`), [`../../trajan/SKILL.md`](../../trajan/SKILL.md) (CI/CD — different surface), [`../../nosey_parker/SKILL.md`](../../nosey_parker/SKILL.md) (legacy secret datastore).

**Ontology:** `.docs/analysis/nuggets.json` — prefer `CLOUD_STORAGE_BUCKET` / `CLOUD_STORAGE_BUCKET_OPEN`, `INTERNET_NAME`, `AFFILIATE_INTERNET_NAME_HIJACKABLE`, `VULNERABILITY_GENERAL`, `RAW_RIR_DATA`, `PASSWORD_COMPROMISED` (confirmed only); do not invent `CLOUD_ACCOUNT` types without `nuggets_extension.json` approval.
