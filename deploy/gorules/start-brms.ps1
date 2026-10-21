# Start Docker Desktop, PostgreSQL, and GoRules BRMS for SPEC-020.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Write-State([string]$Component, [string]$State, [string]$Detail) {
    Write-Host "[$Component] $State - $Detail"
}

$EnvFile = Join-Path $PSScriptRoot ".env"
$Example = Join-Path $PSScriptRoot ".env.example"
if (-not (Test-Path $EnvFile)) {
    Write-State "config" "Blocked" "Missing deploy/gorules/.env. Copy deploy/gorules/.env.example and supply local secrets."
    exit 2
}

$values = @{}
foreach ($line in Get-Content $EnvFile) {
    if ($line -match '^\s*#' -or $line -match '^\s*$' -or $line -notmatch '=') { continue }
    $parts = $line.Split('=', 2)
    $values[$parts[0].Trim()] = $parts[1].Trim()
}
foreach ($name in @("DB_USER", "DB_PASSWORD", "DB_NAME", "COOKIE_SECRET", "HASH_SECRET", "RELEASE_ZIP_PASSWORD")) {
    if ([string]::IsNullOrWhiteSpace($values[$name]) -or $values[$name] -like "replace-with-*") {
        Write-State "config" "Blocked" "$name is missing or still uses the example placeholder."
        exit 2
    }
}
$licenseBlocked = [string]::IsNullOrWhiteSpace($values["LICENSE_KEY"])
if ($licenseBlocked) {
    Write-State "license" "Blocked" "LICENSE_KEY is empty. Obtain one from https://portal.gorules.io. Docker and PostgreSQL checks can continue, but BRMS health cannot pass."
}

function Test-DockerEngine {
    & docker info *> $null
    return $LASTEXITCODE -eq 0
}

if (-not (Test-DockerEngine)) {
    $desktop = "${env:ProgramFiles}\Docker\Docker\Docker Desktop.exe"
    if (-not (Test-Path $desktop)) {
        Write-State "docker" "Failed" "Docker engine is unavailable and Docker Desktop was not found at $desktop."
        exit 3
    }
    Write-State "docker" "Starting" "Launching Docker Desktop."
    Start-Process $desktop | Out-Null
    $deadline = (Get-Date).AddMinutes(3)
    while ((Get-Date) -lt $deadline -and -not (Test-DockerEngine)) {
        Start-Sleep -Seconds 5
    }
}
if (-not (Test-DockerEngine)) {
    Write-State "docker" "Failed" "Docker engine did not become ready within 3 minutes."
    exit 3
}
Write-State "docker" "Ready" "Docker engine is accepting commands."

& docker compose --env-file $EnvFile -f (Join-Path $PSScriptRoot "compose.yaml") up -d
if ($LASTEXITCODE -ne 0) {
    Write-State "compose" "Failed" "docker compose up failed."
    exit 4
}

$postgresReady = $false
foreach ($attempt in 1..20) {
    & docker inspect --format "{{.State.Health.Status}}" spiderfeet-gorules-postgres 2>$null | Out-Null
    $status = (& docker inspect --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}" spiderfeet-gorules-postgres).Trim()
    if ($status -eq "healthy") { $postgresReady = $true; break }
    Start-Sleep -Seconds 3
}
if (-not $postgresReady) {
    Write-State "postgres" "Failed" "PostgreSQL did not report healthy."
    exit 5
}
Write-State "postgres" "Ready" "Persistent PostgreSQL service is healthy."

if ($licenseBlocked) {
    Write-State "brms" "Blocked" "Stack files are started, but live BRMS health is blocked until LICENSE_KEY is configured."
    exit 10
}

$port = if ($values["BRMS_HOST_PORT"]) { $values["BRMS_HOST_PORT"] } else { "8088" }
$healthUrl = "http://localhost:$port/api/health"
$healthy = $false
foreach ($attempt in 1..30) {
    try {
        $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300) { $healthy = $true; break }
    } catch {
        Start-Sleep -Seconds 3
    }
}
if (-not $healthy) {
    Write-State "brms" "Failed" "BRMS did not return success from $healthUrl. Check the license portal and container logs."
    exit 6
}
Write-State "brms" "Ready" "$healthUrl returned success."
exit 0
