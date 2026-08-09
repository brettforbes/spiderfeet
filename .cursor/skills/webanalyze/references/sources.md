# webanalyze Sources

## Official docs and repository

- [webanalyze repository](https://github.com/rverton/webanalyze)
- [webanalyze README](https://github.com/rverton/webanalyze/blob/master/README.md)
- [webanalyze releases](https://github.com/rverton/webanalyze/releases)

## Fingerprint definitions

- Live `-update` downloads from **enthec/webappanalyzer** (see package `WappazlyerRoot` in upstream `wappalyze.go`):  
  `https://raw.githubusercontent.com/enthec/webappanalyzer/main/src`
- Bundled/repo `technologies.json` may ship with releases; this Windows extract required a local `-update` (2026-08-10).
- Historical Wappalyzer ecosystem references:
  - [wappalyzer/wappalyzer](https://github.com/wappalyzer/wappalyzer)
  - [Wappalyzer schema](https://github.com/wappalyzer/wappalyzer/blob/master/schema.json)

## Supplementary guide

- [RootSec webanalyze overview](https://www.rootsec.in/tools/technology-detection/fingerprinting/webanalyze)

## Local SpiderFeet artifacts

| Path | Role |
|------|------|
| `C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe` | Binary |
| `C:\projects\spiderfeet\.tools\webanalyze\webanalyze_Windows_x86_64.zip` | Release archive |
| `C:\projects\spiderfeet\.tools\webanalyze\technologies.json` | Definitions after `-update` |
| `C:\projects\spiderfeet\.tmp_webanalyze_help\` | Captured help (2026-08-10) |
| `.docs/docs-for-cli-tools/webanalyze-CLI-Options.md` | Operator CLI reference |
| `.docs/docs-for-cli-tools/webanalyze-Zero-to-Hero.md` | Operator tutorial |

## Authority for flags

**Live `-h` on this binary wins** over README snippets. Notably, Captured help includes `-redirect`, which older README help blocks omit. Prefer `-output json` over any third-party docs that show a non-existent `-json` flag.
