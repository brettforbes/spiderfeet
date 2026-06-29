<#
.SYNOPSIS
  Verify WSL mirrored networking prerequisites for netdiscover harvest on 192.168.1.0/24.

.EXAMPLE
  & .seed/scripts/verify_wsl_netdiscover_prereqs.ps1
  & .seed/scripts/verify_wsl_netdiscover_prereqs.ps1 -SkipSmoke
#>
param(
    [string]$ExpectedInterface = 'eth1',
    [string]$Subnet = '192.168.1.0/24',
    [switch]$SkipSmoke,
    [switch]$ApplyShutdown
)

$ErrorActionPreference = 'Stop'
$WslConfig = Join-Path $env:USERPROFILE '.wslconfig'

function Fail($code, $msg) {
    Write-Host "FAIL: $msg" -ForegroundColor Red
    exit $code
}

function Ok($msg) {
    Write-Host "OK: $msg" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Netdiscover WSL prerequisites ===" -ForegroundColor Cyan

if (-not (Test-Path $WslConfig)) {
    Fail 1 ".wslconfig missing at $WslConfig - run .seed/scripts/setup_wsl_lan_network.ps1 (admin)"
}
$cfg = Get-Content $WslConfig -Raw
if ($cfg -notmatch '(?m)^\s*networkingMode\s*=\s*mirrored\s*$') {
    Fail 1 ".wslconfig must set networkingMode=mirrored (see $WslConfig)"
}
Ok ".wslconfig has networkingMode=mirrored"

if ($ApplyShutdown) {
    Write-Host "Applying wsl --shutdown..."
    wsl --shutdown 2>$null
    Start-Sleep -Seconds 3
}

$probeCmd = "ip -br addr show; echo '---'; ip -4 -o addr show | grep 192.168.1 || true"
$probe = wsl -u root bash -lc $probeCmd 2>&1 | Out-String
Write-Host $probe

if ($probe -notmatch '192\.168\.1\.') {
    Fail 2 "No 192.168.1.x on WSL. Run: wsl --shutdown, then retry or setup_wsl_lan_network.ps1"
}
Ok "WSL has 192.168.1.x address (mirrored LAN visible)"

$ifacePattern = "$ExpectedInterface\s+UP\s+192\.168\.1\."
if ($probe -match $ifacePattern) {
    Ok "$ExpectedInterface is UP with 192.168.1.x (matches netdiscover.yaml)"
} elseif (($probe -match 'eth2\s+UP\s+192\.168\.1\.') -and ($probe -notmatch 'eth1\s+UP\s+192\.168\.1\.')) {
    Fail 2 "Expected -i $ExpectedInterface but only eth2 has 192.168.1.x - update netdiscover.yaml"
} else {
    Write-Host "WARN: Could not confirm $ExpectedInterface; check ip -br addr" -ForegroundColor Yellow
}

if ($SkipSmoke) {
    Write-Host ""
    Write-Host "Ready (smoke test skipped)." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Running netdiscover smoke test on -i $ExpectedInterface ..." -ForegroundColor Cyan
$smokeCmd = "netdiscover -P -N -i $ExpectedInterface -r $Subnet -c 1 -s 30 2>&1 | tail -5"
$smoke = wsl -u root bash -lc $smokeCmd 2>&1 | Out-String
Write-Host $smoke

if ($smoke -match '(\d+) Hosts found') {
    $count = [int]$Matches[1]
    if ($count -gt 0) {
        Ok "Smoke test: $count hosts on $Subnet"
        Write-Host ""
        Write-Host "All prerequisites satisfied." -ForegroundColor Green
        exit 0
    }
}

Fail 3 "Smoke test found 0 hosts - check Wi-Fi, interface -i $ExpectedInterface, or VPN"
