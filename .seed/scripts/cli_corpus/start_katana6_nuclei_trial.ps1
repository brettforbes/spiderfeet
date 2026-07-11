# Launch chunked nuclei critical/high scan over katana exam 6 URLs.
# Default single-worker run binds to WiFi 2 (USB) when connected — keeps main WiFi clean.
# Use -Dual for overnight max-throughput: parallel workers on WiFi 2 + WiFi.
param(
    [switch]$Resume,
    [switch]$Dual,
    [int]$ChunkSize = 5,
    [int]$ChunkTimeout = 2400
)

$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Set-Location $Repo

# Only kill stray nuclei when starting a fresh job (not resume).
if (-not $Resume) {
    Get-Process nuclei -ErrorAction SilentlyContinue | Stop-Process -Force
}

$pyArgs = @(
    ".seed\scripts\cli_corpus\run_nuclei_katana_trial.py",
    "--chunk-size", $ChunkSize,
    "--chunk-timeout", $ChunkTimeout
)
if ($Resume) { $pyArgs += "--resume" }
if ($Dual) {
    $pyArgs += "--launch-dual"
} else {
    $pyArgs += "--launch-chunked"
}

python @pyArgs
Write-Host ""
Write-Host "Progress:"
Write-Host "  .docs\docs-for-cli-tools\exploration_scratch\nuclei\trials\katana_exam6_upside_com\job_overview.json"
Write-Host "Findings (grows as hits appear):"
Write-Host "  .docs\docs-for-cli-tools\exploration_scratch\nuclei\trials\katana_exam6_upside_com\critical_high_findings.json"
Write-Host "Log:"
Write-Host "  .docs\docs-for-cli-tools\exploration_scratch\nuclei\trials\katana_exam6_upside_com\run.log"
if ($Dual) {
    Write-Host ""
    Write-Host "Dual mode: worker0 -> WiFi 2, worker1 -> WiFi (alternating chunks)"
}
