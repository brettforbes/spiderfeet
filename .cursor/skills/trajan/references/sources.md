# Trajan Sources

Prompt-provided and upstream URLs:

- https://github.com/praetorian-inc/trajan
- https://github.com/praetorian-inc/trajan/blob/main/README.md
- https://github.com/praetorian-inc/trajan/releases
- https://github.com/praetorian-inc/trajan/wiki
- https://dev.to/praetorian_guard/we-kept-breaking-cicd-pipelines-across-every-platform-so-we-built-one-tool-to-secure-all-of-them-1c2j
- https://pkg.go.dev/github.com/praetorian-inc/trajan

## Local evidence

| Artifact | Path |
|----------|------|
| Binary | `.tools/trajan/trajan.exe` |
| Help capture | `.tmp_trajan_help/` (2026-08-10) |
| Skill | `.cursor/skills/trajan/SKILL.md` |
| Operator CLI options | `.docs/docs-for-cli-tools/Trajan-CLI-Options.md` |
| Zero to Hero | `.docs/docs-for-cli-tools/Trajan-Zero-to-Hero.md` |

## Version note

SpiderFeet skill and Captured help document **Trajan 1.0.2** CLI surface (`scan` / `enumerate` / `attack` / …). Upstream README may describe newer phased commands; **do not invent flags** — re-capture help when upgrading the binary.
