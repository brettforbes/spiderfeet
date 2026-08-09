# Vespasian References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Command tree, SpiderFeet preferred flags, Captured help pointer |
| [output-and-parsing.md](output-and-parsing.md) | `capture.json`, OpenAPI / GraphQL SDL / WSDL parsing |
| [nugget-mapping.md](nugget-mapping.md) | Specs → SpiderFeet `nodes[]` / `edges[]` |
| [tactics.md](tactics.md) | Sequencing, thin yield, proxy/import tactics |
| [sources.md](sources.md) | Official repo, blog, releases, docs |

**Read order for new agents**

1. `cli-options.md` — v1.0.0 command tree and SpiderFeet defaults (`-o` specs + `capture.json`).
2. `output-and-parsing.md` — parse generated OpenAPI/GraphQL/WSDL and capture JSON.
3. `nugget-mapping.md` — map hosts/URLs/descriptors to catalogue nugget ids.
4. `tactics.md` — adapt for SPA, auth, proxy imports, private labs.
5. `sources.md` — upstream docs when help text is insufficient (verify flags against Captured help).

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Vespasian-Zero-to-Hero.md` | Install → scan/crawl/import → generate → nuggets |
| `.docs/docs-for-cli-tools/Vespasian-CLI-Options.md` | Full CLI reference + Captured help (**2026-08-10**) |

**Related skills:** [`../../httpx/SKILL.md`](../../httpx/SKILL.md) (live URL confirm), [`../../katana/SKILL.md`](../../katana/SKILL.md) (crawl URLs — different tool), [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md) (template vulns after surface map).

**Ontology:** `.docs/analysis/nuggets.json` — prefer `INTERNET_NAME`, `LINKED_URL_INTERNAL`, `URL_FORM`, `WEBSERVER_TECHNOLOGY`, `RAW_RIR_DATA`; do not invent `API_ENDPOINT` types without `nuggets_extension.json` approval.
