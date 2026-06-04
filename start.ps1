# SpiderFeet development entry — launches the web UI (Stage 1 / SF-01-07)
# Requires: Python 3.7+, dependencies via `poetry install`
param(
    [string]$Listen = "127.0.0.1:5001"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Error "Poetry is required. Install from https://python-poetry.org/docs/#installation"
}

Write-Host "Starting SpiderFeet web UI at http://$Listen ..."
poetry run python sf.py -l $Listen
