#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Enable WSL LAN access for ARP tools (netdiscover) on 192.168.1.0/24.

.DESCRIPTION
  Attempts mirrored networking first (recommended). If that fails on this host,
  creates a Hyper-V external switch on the chosen Wi-Fi adapter and enables
  bridged mode (deprecated but often works for single-NIC L2 access).

  Run from an elevated PowerShell:
    Set-ExecutionPolicy -Scope Process Bypass -Force
    & "$PSScriptRoot\setup_wsl_lan_network.ps1"

  Reboot if mirrored mode still fails after HNS reset (known Windows bug).
#>
param(
    [string]$WifiAdapterName = 'WiFi 2',
    [string]$VmSwitchName = 'WSL-WiFi2',
    [ValidateSet('mirrored', 'bridged', 'auto')]
    [string]$Mode = 'auto'
)

$ErrorActionPreference = 'Stop'
$WslConfig = Join-Path $env:USERPROFILE '.wslconfig'

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }

function Test-WslNetwork {
    $out = wsl -u root bash -lc "ip -br addr; echo '---'; ip route | head -3" 2>&1
    $text = ($out | Out-String)
    Write-Host $text
    if ($text -match '192\.168\.1\.') { return $true }
    if ($text -match '172\.(1[6-9]|2[0-9]|3[0-1])\.' ) { Write-Host 'WSL still on NAT range (172.x)' -ForegroundColor Yellow }
    return $false
}

Write-Step 'Stopping WSL'
wsl --shutdown 2>$null
Start-Sleep -Seconds 2

Write-Step 'Restarting Host Network Service (HNS)'
try {
    Restart-Service hns -Force -ErrorAction Stop
    Write-Host 'HNS restarted.'
} catch {
    Write-Warning "Could not restart HNS: $_"
}

function Set-MirroredConfig {
    @"
[wsl2]
networkingMode=mirrored
firewall=false
autoProxy=false
dnsTunneling=false
"@ | Set-Content -Path $WslConfig -Encoding UTF8
    Write-Host "Wrote mirrored .wslconfig -> $WslConfig"
}

function Set-BridgedConfig {
    param([string]$SwitchName)
    @"
[wsl2]
networkingMode=bridged
vmSwitch=$SwitchName
"@ | Set-Content -Path $WslConfig -Encoding UTF8
    Write-Host "Wrote bridged .wslconfig (vmSwitch=$SwitchName) -> $WslConfig"
}

function Ensure-ExternalSwitch {
    param([string]$SwitchName, [string]$AdapterName)
    if (-not (Get-Command Get-VMSwitch -ErrorAction SilentlyContinue)) {
        throw @'
Hyper-V PowerShell module not available.
Enable: Settings -> Optional features -> Hyper-V Platform + Windows Hypervisor Platform,
       or run: Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
Then reboot and re-run this script.
'@
    }
    $existing = Get-VMSwitch -Name $SwitchName -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Virtual switch '$SwitchName' already exists ($($existing.SwitchType))."
        if ($existing.SwitchType -eq 'External') {
            $ext = Get-VMSwitchExtensionPortFeature -SwitchName $SwitchName -ErrorAction SilentlyContinue
        }
        return
    }
    $adapter = Get-NetAdapter -Name $AdapterName -ErrorAction Stop
    Write-Host "Creating external switch '$SwitchName' on adapter '$AdapterName' ($($adapter.InterfaceDescription))..."
    New-VMSwitch -Name $SwitchName -NetAdapterName $AdapterName -AllowManagementOS $true
}

function Try-StartWsl {
    $probe = wsl -u root bash -lc 'echo ok' 2>&1 | Out-String
    if ($probe -match 'ConfigureNetworking/0x8007054f' -or $probe -match 'falling back to networkingMode None') {
        Write-Warning 'WSL reported ConfigureNetworking/0x8007054f'
        return $false
    }
    if ($probe -notmatch '\bok\b') {
        Write-Warning "WSL probe output: $probe"
    }
    return ($LASTEXITCODE -eq 0)
}

# --- Mirrored attempt ---
if ($Mode -in @('mirrored', 'auto')) {
    Write-Step 'Configuring mirrored networking (recommended)'
    Set-MirroredConfig
    wsl --shutdown 2>$null
    Start-Sleep -Seconds 3
    if (Try-StartWsl) {
        Write-Step 'Checking WSL addresses after mirrored start'
        if (Test-WslNetwork) {
            Write-Host "`nSUCCESS: WSL mirrored mode has LAN visibility." -ForegroundColor Green
            exit 0
        }
        Write-Warning 'Mirrored started but no 192.168.1.x on WSL interfaces yet.'
        Write-Host 'Tip: disable unused Wi-Fi/Ethernet adapters if multiple NICs are up (known mirrored-mode issue).'
        if ($Mode -eq 'mirrored') { exit 2 }
    } else {
        Write-Warning 'Mirrored mode failed on this host.'
        if ($Mode -eq 'mirrored') {
            Write-Host @'

Mirrored mode troubleshooting:
  1. Reboot Windows (often clears HNS state)
  2. Disable VPN/proxy (Clash, v2ray, GlobalProtect) and retry
  3. Disable the second Wi-Fi adapter temporarily (you have WiFi + WiFi 2 both up)
  4. Restart-Service hns; Restart-Service SharedAccess
  5. See: https://github.com/microsoft/WSL/issues/12351

'@
            exit 1
        }
    }
}

# --- Bridged fallback ---
if ($Mode -in @('bridged', 'auto')) {
    Write-Step "Configuring bridged networking on '$WifiAdapterName'"
    Ensure-ExternalSwitch -SwitchName $VmSwitchName -AdapterName $WifiAdapterName
    Set-BridgedConfig -SwitchName $VmSwitchName
    wsl --shutdown 2>$null
    Start-Sleep -Seconds 3
    if (-not (Try-StartWsl)) {
        Write-Error 'Bridged mode failed to start WSL. Check Event Viewer and vmSwitch name.'
        exit 1
    }
    Write-Step 'Checking WSL addresses after bridged start'
    if (Test-WslNetwork) {
        Write-Host "`nSUCCESS: WSL bridged mode on $VmSwitchName." -ForegroundColor Green
        exit 0
    }
    Write-Warning 'Bridged WSL started but no 192.168.1.x detected. DHCP may need a moment — run: wsl ip -br addr'
    exit 2
}
