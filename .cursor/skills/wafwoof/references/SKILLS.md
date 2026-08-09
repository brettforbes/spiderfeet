# WAFWOOF (wafw00f) References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | All `wafw00f` CLI flags + **captured `--help` (v2.4.2)** |
| [json-output-schema.md](json-output-schema.md) | JSON array written to stdout/file |
| [nugget-mapping.md](nugget-mapping.md) | SpiderFeet `WEBSERVER_TECHNOLOGY` and `RAW_RIR_DATA` |
| [tactics.md](tactics.md) | Adaptive WAF fingerprint workflows |
| [sources.md](sources.md) | GitHub, wiki, blogs, SpiderFeet paths |

## Operator docs (repo root)

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/WAFWOOF-Zero-to-Hero.md` | Install → pipelines → nuggets |
| `.docs/docs-for-cli-tools/WAFWOOF-CLI-Options.md` | CLI reference + captured help |

## Usage notes

- Read `json-output-schema.md` before writing parsers. Output is JSON — use `json.loads`, not TextFSM.
- SpiderFeet command: `wafw00f -a -o- -f json <url>`
- Binary path (this host): `C:\projects\spiderfeet\.venv\Scripts\wafw00f.exe`
