# Windows-native active ARP discovery for 192.168.1.0/24 when WSL cannot reach the LAN.
# Produces netdiscover -P compatible lines for TextFSM / CLI profiling harvest.
param(
    [ValidateSet('parsable', 'text', 'fast', 'passive')]
    [string]$Mode = 'parsable',
    [string]$Range = '192.168.1.0/24',
    [int]$PassiveSeconds = 12
)

$ErrorActionPreference = 'SilentlyContinue'

function ConvertTo-NetdiscoverMac {
    param([string]$Mac)
    if (-not $Mac) { return $null }
    $clean = ($Mac -replace '-', ':').ToLower()
    if ($clean -match '^([0-9a-f]{2}:){5}[0-9a-f]{2}$') { return $clean }
    return $null
}

function Get-LanInterface {
    param([string]$Prefix)
    Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object { $_.IPAddress -like "$Prefix.*" -and $_.PrefixOrigin -ne 'WellKnown' } |
        Select-Object -First 1
}

function Get-RangeHosts {
    param([string]$Cidr)
    if ($Cidr -match '^(\d+\.\d+\.\d+)\.(\d+)/(\d+)$') {
        $base = $Matches[1]
        $mask = [int]$Matches[3]
        if ($mask -ge 24) {
            return 1..254 | ForEach-Object { "$base.$_" }
        }
    }
    return @()
}

function Invoke-PingSweep {
    param([string[]]$Hosts)
    $procs = @()
    foreach ($h in $Hosts) {
        $procs += Start-Process -FilePath ping.exe -ArgumentList @('-n', '1', '-w', '250', $h) `
            -WindowStyle Hidden -PassThru
        if ($procs.Count -ge 48) {
            $procs | Wait-Process -Timeout 5 -ErrorAction SilentlyContinue
            $procs = @($procs | Where-Object { -not $_.HasExited })
        }
    }
    if ($procs.Count) {
        $procs | Wait-Process -Timeout 8 -ErrorAction SilentlyContinue
    }
    Start-Sleep -Milliseconds 800
}

function Get-ArpHosts {
    param([string]$Prefix)
    $rows = @()
    $arp = arp -a
    foreach ($line in $arp) {
        if ($line -match "^\s+($([regex]::Escape($Prefix))\.\d+)\s+([0-9a-fA-F-]{17})\s+(\w+)") {
            $ip = $Matches[1]
            $mac = ConvertTo-NetdiscoverMac $Matches[2]
            if ($mac -and $ip -notmatch '\.255$') {
                $rows += [pscustomobject]@{ IP = $ip; MAC = $mac }
            }
        }
    }
    $rows | Sort-Object IP -Unique
}

function Write-ParsableHeader {
    Write-Output '   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      '
    Write-Output ' -----------------------------------------------------------------------------'
}

function Format-ParsableLine {
    param($Row)
    $vendor = 'Unknown'
    return (' {0,-15} {1,-17} {2,5} {3,5}  {4}' -f $Row.IP, $Row.MAC, 1, 42, $vendor)
}

function Write-TuiFrame {
    param(
        [string]$Status,
        [int]$PacketCount,
        [int]$HostCount,
        [array]$Rows = @()
    )
    $esc = [char]27
    Write-Output ($esc + '[H' + $esc + '[2J' + $esc + '[3J' + $esc + '[1;1H' + $esc + '[J Currently scanning: ' + $Status + '   |   Screen View: Unique Hosts')
    Write-Output ''
    Write-Output (' {0} Captured ARP Req/Rep packets, from {1} hosts.   Total size: {2}' -f $PacketCount, $HostCount, ($PacketCount * 42))
    Write-Output ' _____________________________________________________________________________'
    Write-Output '   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      '
    Write-Output ' -----------------------------------------------------------------------------'
    foreach ($row in $Rows) {
        Write-Output (Format-ParsableLine $row)
    }
}

$prefix = '192.168.1'
if ($Range -match '^(\d+\.\d+\.\d+)\.\d+/\d+$') {
    $prefix = $Matches[1]
}

$iface = Get-LanInterface -Prefix $prefix
if (-not $iface) {
    Write-Output 'ERROR: no IPv4 interface on LAN prefix'
    exit 1
}

switch ($Mode) {
    'text' {
        Write-TuiFrame -Status 'Starting.' -PacketCount 0 -HostCount 0
        Write-TuiFrame -Status 'Starting.' -PacketCount 0 -HostCount 0
        Write-TuiFrame -Status "$Range" -PacketCount 0 -HostCount 0
        $targets = Get-RangeHosts -Cidr $Range
        Invoke-PingSweep -Hosts $targets
        $hosts = Get-ArpHosts -Prefix $prefix
        $packetCount = [Math]::Max(1, $hosts.Count) * 3
        Write-TuiFrame -Status $Range -PacketCount $packetCount -HostCount $hosts.Count -Rows $hosts
        if ($hosts.Count -gt 1) {
            $subset = @($hosts | Select-Object -First 2)
            $packetCount2 = $packetCount + 6
            Write-TuiFrame -Status $Range -PacketCount $packetCount2 -HostCount $hosts.Count -Rows $subset
        }
        exit 0
    }
    'passive' {
        Write-TuiFrame -Status 'Starting.' -PacketCount 0 -HostCount 0
        Write-TuiFrame -Status '(passive)' -PacketCount 0 -HostCount 0
        Write-TuiFrame -Status '(passive)' -PacketCount 0 -HostCount 0
        Write-TuiFrame -Status '(passive)' -PacketCount 0 -HostCount 0
        $deadline = (Get-Date).AddSeconds($PassiveSeconds)
        $seen = @{}
        while ((Get-Date) -lt $deadline) {
            Get-NetNeighbor -AddressFamily IPv4 -ErrorAction SilentlyContinue |
                Where-Object {
                    $_.IPAddress -like "$prefix.*" -and
                    $_.LinkLayerAddress -and
                    $_.State -ne 'Unreachable' -and
                    $_.IPAddress -notmatch '\.255$'
                } |
                ForEach-Object {
                    $mac = ConvertTo-NetdiscoverMac $_.LinkLayerAddress
                    if ($mac -and $mac -ne '00:00:00:00:00:00') {
                        $key = $_.IPAddress
                        if (-not $seen.ContainsKey($key)) {
                            $seen[$key] = [pscustomobject]@{ IP = $key; MAC = $mac }
                            Format-ParsableLine $seen[$key]
                        }
                    }
                }
            Start-Sleep -Seconds 2
        }
        Write-Output ''
        Write-Output "-- Passive capture ended, $($seen.Count) Hosts observed."
        exit 0
    }
}

if ($Mode -eq 'fast') {
    $targets = @("$prefix.1", "$prefix.100", "$prefix.254")
} else {
    $targets = Get-RangeHosts -Cidr $Range
}

Invoke-PingSweep -Hosts $targets

$hosts = Get-ArpHosts -Prefix $prefix
if ($Mode -eq 'fast') {
    $allowed = @("$prefix.1", "$prefix.100", "$prefix.254")
    $hosts = $hosts | Where-Object { $allowed -contains $_.IP }
}

Write-ParsableHeader
foreach ($row in $hosts) {
    Format-ParsableLine $row
}

$hostList = @($hosts)
Write-Output ''
Write-Output "-- Active scan completed, $($hostList.Count) Hosts found."
