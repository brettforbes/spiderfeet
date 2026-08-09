# CMSeeK References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | **Live captured `-h` output** (v1.1.3) + structured flag tables and argparse notes |
| [output-schema.md](output-schema.md) | `Result/<target>/cms.json` structure and related artifacts |
| [nugget-mapping.md](nugget-mapping.md) | SpiderFeet `WEBSERVER_TECHNOLOGY` emission rules |
| [tactics.md](tactics.md) | Adaptive workflows when detection is blocked or incomplete |
| [sources.md](sources.md) | GitHub repo, blogs, install paths, SpiderFeet module links |

## Read order

1. **`cli-options.md`** — before constructing non-default command lines or harvest manifests  
2. **`output-schema.md`** — before parsers; JSON native (not TextFSM)  
3. **`nugget-mapping.md`** — before graph or module integration work  
4. **`tactics.md`** — when baseline `--follow-redirect --batch -u` fails  
5. **`sources.md`** — upstream and project cross-links  

## Operator docs (repo root)

| Document | Path |
|----------|------|
| Zero to Hero | `.docs/docs-for-cli-tools/CMSeeK-Zero-to-Hero.md` |
| CLI Options | `.docs/docs-for-cli-tools/CMSeeK-CLI-Options.md` |

## SpiderFeet defaults

```bash
python3 cmseek.py --follow-redirect --batch -u <INTERNET_NAME>
```

Structured artifact: `{cmseekpath}/Result/{eventData}/cms.json` → `WEBSERVER_TECHNOLOGY`.
