# Install quarantine CLI tools in WSL Ubuntu-22.04 (Stage 5 — #806 / #807).
# Usage: powershell -File .seed/scripts/install_wsl_cli_tools.ps1

$ErrorActionPreference = "Stop"
$Distro = "Ubuntu-22.04"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

Write-Host "==> WSL distro: $Distro"
Write-Host "==> Repo: $Repo"

# apt deps as root (no interactive sudo on typical WSL)
wsl -d $Distro -u root -e bash -lc @"
set -e
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  make gcc ruby ruby-dev nodejs npm nbtscan onesixtyone \
  git python3 python3-pip python3-venv openssl procps curl
"@

# user-local tool clones + manifest
$RepoWsl = ($Repo -replace '\\', '/') -replace '^C:', '/mnt/c'
wsl -d $Distro -e bash -lc "sed -i 's/\r$//' '$RepoWsl/.seed/scripts/install_wsl_cli_tools.sh' && bash '$RepoWsl/.seed/scripts/install_wsl_cli_tools.sh'"

Write-Host "==> Install complete. Probe:"
wsl -d $Distro -e bash -lc "source ~/.local/spiderfeet-cli/manifest.env && cd '$RepoWsl' && ~/.local/bin/poetry run python .seed/scripts/probe_cli_tools.py 2>/dev/null || python3 .seed/scripts/probe_cli_tools.py"
