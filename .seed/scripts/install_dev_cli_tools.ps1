# Install dev CLI binaries into .tools/ (no admin required)
# Usage: powershell -ExecutionPolicy Bypass -File .seed/scripts/install_dev_cli_tools.ps1

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$ToolsBin = Join-Path $RepoRoot ".tools\bin"
$Templates = Join-Path $RepoRoot ".tools\nuclei-templates"

New-Item -ItemType Directory -Force -Path $ToolsBin, $Templates | Out-Null

function Install-Nuclei {
    if (Test-Path (Join-Path $ToolsBin "nuclei.exe")) { return }
    $zip = Join-Path $RepoRoot ".tools\nuclei.zip"
    $tag = "v3.8.0"
    Invoke-WebRequest -Uri "https://github.com/projectdiscovery/nuclei/releases/download/$tag/nuclei_3.8.0_windows_amd64.zip" -OutFile $zip
    Expand-Archive -Path $zip -DestinationPath $ToolsBin -Force
    Remove-Item $zip
    & (Join-Path $ToolsBin "nuclei.exe") -update-templates -ud $Templates | Out-Null
}

function Install-Trufflehog {
    if (Test-Path (Join-Path $ToolsBin "trufflehog.exe")) { return }
    $tag = "v3.95.5"
    $tar = Join-Path $RepoRoot ".tools\trufflehog.tar.gz"
    Invoke-WebRequest -Uri "https://github.com/trufflesecurity/trufflehog/releases/download/$tag/trufflehog_3.95.5_windows_amd64.tar.gz" -OutFile $tar
    tar -xzf $tar -C $ToolsBin
    Remove-Item $tar
}

Install-Nuclei
Install-Trufflehog
Write-Host "Installed tools in $ToolsBin"
Get-ChildItem $ToolsBin -Filter *.exe | Select-Object Name
