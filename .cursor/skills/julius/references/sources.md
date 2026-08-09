# Julius — Canonical Sources

## Official repository and wiki

| Resource | URL |
|----------|-----|
| GitHub repository | https://github.com/praetorian-inc/julius |
| Wiki home | https://github.com/praetorian-inc/julius/wiki |
| Architecture | https://github.com/praetorian-inc/julius/wiki/Architecture |
| CLI Reference | https://github.com/praetorian-inc/julius/wiki/CLI-Reference |
| Supported Services | https://github.com/praetorian-inc/julius/wiki/Supported-Services |
| Probe YAML Reference | https://github.com/praetorian-inc/julius/wiki/Probe-YAML-Reference |
| Match Rules | https://github.com/praetorian-inc/julius/wiki/Match-Rules |
| Security Policy | https://github.com/praetorian-inc/julius/blob/main/SECURITY.md |

## Blog posts and articles

| Title | URL |
|-------|-----|
| Introducing Julius (Praetorian) | https://www.praetorian.com/blog/introducing-julius-open-source-llm-service-fingerprinting/ |
| Shadow AI / Dev.to | https://dev.to/praetorian_guard/shadow-ai-is-everywhere-meet-julius-the-open-source-llm-fingerprinting-tool-410g |
| v0.2.0 — Cloud AI, RAG | https://www.praetorian.com/blog/julius-v020-cloud-ai-rag-detection/ |
| There's Always a Secret Hiding Somewhere | https://medium.com/@praetorianguard/theres-always-a-secret-hiding-somewhere-we-built-a-tool-to-find-it-d5398b155a4f |

## Local binary / help

| Item | Path |
|------|------|
| Windows binary | `C:\projects\spiderfeet\.tools\julius\julius.exe` |
| Bundled README / CHANGELOG | `.tools/julius/` |
| Captured help (2026-08-10) | `.tmp_julius_help/` |

## Install

Releases: https://github.com/praetorian-inc/julius/releases

```bash
go install github.com/praetorian-inc/julius/cmd/julius@latest
```

## SpiderFeet integration notes

- Always capture **`julius probe -o json`** or **`-o jsonl`** for structured examination.
- `-o` is format only — redirect with the shell (`> file.jsonl`).
- No `version` / `--version` on the captured binary.
- Chain upstream port discovery: **Naabu** / **Nmap** → HTTPS URLs → Julius.
- Optional downstream: **`--augustus`** for Augustus safety scans.
- Wiki CLI pages may lag the binary (extra globals: `--banner`, `--ca-cert`, `--insecure`, `--max-response-size`, `--no-color`; probe: `--base-paths`, `-H`). Prefer Captured help.
