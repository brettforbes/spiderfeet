# WSL Ruby CLI tools runbook (Stage 5)

Windows-native installs for the six quarantine CLI tools are fragile. Use **WSL2 (`Ubuntu-22.04`)** for smoke validation and battery runs.

**One-command install (Windows):**

```powershell
powershell -ExecutionPolicy Bypass -File .seed/scripts/install_wsl_cli_tools.ps1
```

**Run battery (WSL — uses a Linux-only Poetry venv, does not touch Windows `.venv`):**

```powershell
wsl -d Ubuntu-22.04 bash /mnt/c/projects/spiderfeet/.seed/scripts/run_wsl_quarantine_battery.sh
```

**Spec:** SPEC-003 R3-05-07  
**Related issues:** SF-05-14 (WSL Ruby CLI batch)

## Prerequisites

```powershell
wsl --install -d Ubuntu-22.04
# Reboot if prompted; create Linux user
```

In WSL Ubuntu:

```bash
sudo apt update
sudo apt install -y ruby ruby-dev build-essential git curl openssl procps
```

## CMSeeK (`sfp_tool_cmseek`)

```bash
cd ~
git clone https://github.com/Tuhinshubhra/CMSeeK
cd CMSeeK
pip3 install --user -r requirements.txt
# cmseek.py is invoked by SpiderFeet module opts or PATH
sudo ln -sf "$(pwd)/cmseek.py" /usr/local/bin/cmseek
chmod +x /usr/local/bin/cmseek
cmseek --help
```

SpiderFeet module expects `cmseek` on PATH when running under WSL, or set module opt `cmseekpath` if present.

## testssl.sh (`sfp_tool_testsslsh`)

```bash
cd ~
git clone --depth 1 https://github.com/drwetter/testssl.sh.git
sudo ln -sf ~/testssl.sh/testssl.sh /usr/local/bin/testssl.sh
testssl.sh --version
```

Battery: target `example.com` as `INTERNET_NAME`; allow 300s+ timeout.

## WhatWeb (`sfp_tool_whatweb`)

```bash
sudo gem install whatweb
whatweb --version
```

## Bridge SpiderFeet (Windows API) → WSL binaries

Option A — run API inside WSL (full stack):

```bash
cd /mnt/c/projects/spiderfeet
poetry install
poetry run python -m spiderfeet.api
```

Option B — Windows API with WSL PATH for battery only:

```powershell
wsl bash -lc "cd /mnt/c/projects/spiderfeet && poetry run python .seed/scripts/run_quarantine_battery.py --local --only sfp_tool_whatweb --write"
```

Option C — symlink Windows `.tools/bin` from WSL wrappers (advanced): add `cmseek`, `testssl.sh`, `whatweb` shell stubs in `.tools/bin` that delegate to `wsl …`.

## Probe

```powershell
wsl bash -lc "which cmseek testssl.sh whatweb 2>/dev/null; cmseek --help 2>&1 | head -1"
```

Update `.seed/scripts/probe_cli_tools.py` to report WSL availability when Windows `where` fails.

## Validation

```powershell
wsl bash -lc "cd /mnt/c/projects/spiderfeet && poetry run python .seed/scripts/run_quarantine_battery.py --local --timeout 300 --only sfp_tool_cmseek sfp_tool_testsslsh sfp_tool_whatweb --write"
```

On success, promote with `--promote` per `cli_tool_install_runbook.md`.
