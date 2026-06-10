# CLI tool install runbook (Stage 5 — #733)

SpiderFeet wraps 13 external CLI tools as `sfp_tool_*` modules. Smoke validation requires each binary on `PATH` (or explicit module opts for legacy layouts).

## Quick probe

```powershell
cd c:\projects\spiderfeet
.\.venv\Scripts\python.exe .seed\scripts\probe_cli_tools.py
```

Prepends `.venv\Scripts` (Windows) or `.venv/bin` (Unix) and `.tools/bin` before checking.

## Local dev binaries (no admin)

Download nuclei + trufflehog into gitignored `.tools/`:

```powershell
powershell -ExecutionPolicy Bypass -File .seed\scripts\install_dev_cli_tools.ps1
```

Modules and battery scripts resolve binaries via `spiderfeet.tools.cli_paths` (PATH → `.tools/bin` → Windows nmap defaults).

| Module | Binary | Local install |
|--------|--------|---------------|
| `sfp_tool_nuclei` | `nuclei` | Script above; templates in `.tools/nuclei-templates/` |
| `sfp_tool_trufflehog` | `trufflehog` | Script above |

Nuclei v3 uses `-jsonl` (not `-json`); battery needs `--timeout 600` for nuclei/trufflehog.

## Pip-installable (dev venv)

These can be installed into the project venv for local battery runs:

```powershell
.\.venv\Scripts\pip.exe install dnstwist wafw00f snallygaster
```

| Module | Binary | Install |
|--------|--------|---------|
| `sfp_tool_dnstwist` | `dnstwist` | `pip install dnstwist` |
| `sfp_tool_wafw00f` | `wafw00f` | `pip install wafw00f` |
| `sfp_tool_snallygaster` | `snallygaster` | `pip install snallygaster` |

`dnstwist`, `wafw00f`, and `snallygaster` modules auto-resolve via `shutil.which()` when the binary is on PATH.

## System / manual install

| Module | Binary | Reference |
|--------|--------|-----------|
| `sfp_tool_cmseek` | `cmseek` | https://github.com/Tuhinshubhra/CMSeeK |
| `sfp_tool_nbtscan` | `nbtscan` | http://www.unixwiz.net/tools/nbtscan.html |
| `sfp_tool_nmap` | `nmap` | https://nmap.org/ (Windows: `winget install Insecure.Nmap`) |
| `sfp_tool_nuclei` | `nuclei` | https://nuclei.projectdiscovery.io/ |
| `sfp_tool_onesixtyone` | `onesixtyone` | https://github.com/trailofbits/onesixtyone |
| `sfp_tool_retirejs` | `retire` | `npm install -g retire` |
| `sfp_tool_testsslsh` | `testssl.sh` | https://testssl.sh |
| `sfp_tool_trufflehog` | `trufflehog` | https://github.com/trufflesecurity/trufflehog |
| `sfp_tool_wappalyzer` | `wappalyzer` | Legacy AliasIO CLI (`cli.js`); npm `wappalyzer@6` deprecated |
| `sfp_tool_whatweb` | `whatweb` | https://github.com/urbanadventurer/WhatWeb |

## Validate and promote

```powershell
$env:PATH = "c:\projects\spiderfeet\.venv\Scripts;" + $env:PATH
.\.venv\Scripts\python.exe .seed\scripts\run_quarantine_battery.py `
  --local --timeout 180 `
  --only sfp_tool_dnstwist sfp_tool_wafw00f sfp_tool_snallygaster `
  --write --promote
```

Promoted modules move from `quarantine_services.json` to `external` + `in-test` in `osint_services.json`.

## Spec binding

SPEC-003 R3-05-08 (custom CLI registration); program epic #723.
