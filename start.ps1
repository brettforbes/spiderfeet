# SpiderFeet development entry
#   .\start.ps1              — CherryPy web UI (legacy, port 5001)
#   .\start.ps1 -Mode api    — FastAPI for widget / Requestly (port 8001; TypeDB HTTP uses 8000)
param(
    [ValidateSet("web", "api")]
    [string]$Mode = "web",
    [string]$Listen = ""
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Error "Poetry is required. Install from https://python-poetry.org/docs/#installation"
}

if ($Mode -eq "api") {
    if (-not $Listen) { $Listen = "127.0.0.1:8001" }
    $parts = $Listen -split ":", 2
    if ($parts.Count -ne 2) {
        Write-Error "Listen must be IP:port (e.g. 127.0.0.1:8001)"
    }
    $env:SPIDERFEET_API_HOST = $parts[0]
    $env:SPIDERFEET_API_PORT = $parts[1]
    Write-Host "Starting SpiderFeet FastAPI at http://$Listen (docs: http://$Listen/docs) ..."
    poetry run python -m spiderfeet.api
    exit $LASTEXITCODE
}

if (-not $Listen) { $Listen = "127.0.0.1:5001" }
Write-Host "Starting SpiderFeet web UI at http://$Listen ..."
poetry run python sf.py -l $Listen
