#Requires -Version 5.1
<#
.SYNOPSIS
    Generates a comprehensive local system inventory as JSON.

.NOTES
    Run as Administrator for fullest detail (BitLocker, TPM, Defender, some CIM, firewall, etc.).
    Some sections are intentionally capped to avoid multi-GB output (firewall rules, event logs).
#>
[CmdletBinding()]
param(
    [string]$OutputPath = "",
    [int]$MaxFirewallRules = 500,
    [int]$MaxEventLogEntries = 100,
    [switch]$IncludeFirewallRules,
    [switch]$IncludeEventLogs,
    [switch]$IncludeInstalledSoftware,
    [switch]$IncludeCertificates,
    [switch]$IncludeAll  # enables heavy sections
)

if ($IncludeAll) {
    $IncludeFirewallRules = $true
    $IncludeEventLogs = $true
    $IncludeInstalledSoftware = $true
    $IncludeCertificates = $true
}

function Write-ReportProgress { param([string]$Message) Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" }

function Invoke-ReportSection {
    param(
        [string]$Name,
        [scriptblock]$ScriptBlock
    )
    try {
        $value = & $ScriptBlock
        if ($null -eq $value) { return @{ _status = 'empty' } }
        return $value
    }
    catch {
        return @{
            _status = 'error'
            _error  = $_.Exception.Message
        }
    }
}

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator
)

$procMap = @{}
Get-Process -ErrorAction SilentlyContinue | ForEach-Object { $procMap[$_.Id] = $_.ProcessName }

$report = [ordered]@{
    Meta = [ordered]@{
        GeneratedAtUtc   = (Get-Date).ToUniversalTime().ToString('o')
        GeneratedAtLocal = (Get-Date).ToString('o')
        ComputerName     = $env:COMPUTERNAME
        UserName         = "$env:USERDOMAIN\$env:USERNAME"
        IsElevatedAdmin  = $isAdmin
        PowerShell       = $PSVersionTable
        ExecutionPolicy  = (Get-ExecutionPolicy -List | ForEach-Object { @{ Scope = $_.Scope; Policy = $_.ExecutionPolicy } })
    }

  # --- Operating system (CIM) ---
    OperatingSystem = Invoke-ReportSection 'OperatingSystem' {
        Get-CimInstance Win32_OperatingSystem | Select-Object *
    }

    ComputerSystem = Invoke-ReportSection 'ComputerSystem' {
        Get-CimInstance Win32_ComputerSystem | Select-Object *
    }

    Bios = Invoke-ReportSection 'Bios' {
        Get-CimInstance Win32_BIOS | Select-Object *
    }

    BaseBoard = Invoke-ReportSection 'BaseBoard' {
        Get-CimInstance Win32_BaseBoard | Select-Object *
    }

    SystemEnclosure = Invoke-ReportSection 'SystemEnclosure' {
        Get-CimInstance Win32_SystemEnclosure | Select-Object *
    }

    TimeZone = Invoke-ReportSection 'TimeZone' {
        Get-TimeZone | Select-Object *
    }

    Culture = Invoke-ReportSection 'Culture' {
        [ordered]@{
            UI_Culture   = (Get-UICulture).Name
            Culture      = (Get-Culture).Name
            WinSystemLocale = (Get-WinSystemLocale).Name
            WinUserLanguageList = (Get-WinUserLanguageList).LanguageTag
        }
    }

  # --- Hardware ---
    Processors = Invoke-ReportSection 'Processors' {
        Get-CimInstance Win32_Processor | Select-Object *
    }

    PhysicalMemory = Invoke-ReportSection 'PhysicalMemory' {
        Get-CimInstance Win32_PhysicalMemory | Select-Object *
    }

    VideoControllers = Invoke-ReportSection 'VideoControllers' {
        Get-CimInstance Win32_VideoController | Select-Object *
    }

    SoundDevices = Invoke-ReportSection 'SoundDevices' {
        Get-CimInstance Win32_SoundDevice | Select-Object *
    }

    Batteries = Invoke-ReportSection 'Batteries' {
        Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue | Select-Object *
    }

    PointingDevices = Invoke-ReportSection 'PointingDevices' {
        Get-CimInstance Win32_PointingDevice -ErrorAction SilentlyContinue | Select-Object *
    }

    Keyboards = Invoke-ReportSection 'Keyboards' {
        Get-CimInstance Win32_Keyboard -ErrorAction SilentlyContinue | Select-Object *
    }

    Monitors = Invoke-ReportSection 'Monitors' {
        Get-CimInstance WmiMonitorID -Namespace root\wmi -ErrorAction SilentlyContinue |
            ForEach-Object {
                $name = ($_.ManufacturerName | ForEach-Object { [char]$_ }) -join ''
                $serial = ($_.SerialNumberID | ForEach-Object { [char]$_ }) -join ''
                [pscustomobject]@{
                    ManufacturerName = $name.Trim([char]0)
                    ProductCodeID    = -join ($_.ProductCodeID | ForEach-Object { [char]$_ })
                    SerialNumberID   = $serial.Trim([char]0)
                    UserFriendlyName = -join ($_.UserFriendlyName | ForEach-Object { [char]$_ })
                    YearOfManufacture = $_.YearOfManufacture
                    WeekOfManufacture = $_.WeekOfManufacture
                }
            }
    }

    PnpDevices = Invoke-ReportSection 'PnpDevices' {
        Get-PnpDevice -ErrorAction SilentlyContinue |
            Select-Object -First 300 Status, Class, FriendlyName, InstanceId, Manufacturer, Present
    }

  # --- Storage ---
    LogicalDisks = Invoke-ReportSection 'LogicalDisks' {
        Get-CimInstance Win32_LogicalDisk | Select-Object *
    }

    DiskDrives = Invoke-ReportSection 'DiskDrives' {
        Get-CimInstance Win32_DiskDrive | Select-Object *
    }

    Volumes = Invoke-ReportSection 'Volumes' {
        Get-Volume -ErrorAction SilentlyContinue | Select-Object *
    }

    Disks = Invoke-ReportSection 'Disks' {
        Get-Disk -ErrorAction SilentlyContinue | Select-Object *
    }

    PhysicalDisks = Invoke-ReportSection 'PhysicalDisks' {
        Get-PhysicalDisk -ErrorAction SilentlyContinue | Select-Object *
    }

    Partitions = Invoke-ReportSection 'Partitions' {
        Get-Partition -ErrorAction SilentlyContinue | Select-Object *
    }

    PageFile = Invoke-ReportSection 'PageFile' {
        Get-CimInstance Win32_PageFileUsage -ErrorAction SilentlyContinue | Select-Object *
    }

    BitLocker = Invoke-ReportSection 'BitLocker' {
        Get-BitLockerVolume -ErrorAction SilentlyContinue | Select-Object *
    }

  # --- Network ---
    NetworkAdapters = Invoke-ReportSection 'NetworkAdapters' {
        Get-NetAdapter -ErrorAction SilentlyContinue | Select-Object *
    }

    IPAddresses = Invoke-ReportSection 'IPAddresses' {
        # FIX: use -AddressFamily, not -InterfaceFamily
        Get-NetIPAddress -ErrorAction SilentlyContinue |
            Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -ne '::1' } |
            Select-Object *
    }

    IPConfiguration = Invoke-ReportSection 'IPConfiguration' {
        Get-NetIPConfiguration -ErrorAction SilentlyContinue | Select-Object *
    }

    DNSClientServerAddress = Invoke-ReportSection 'DNSClientServerAddress' {
        Get-DnsClientServerAddress -ErrorAction SilentlyContinue | Select-Object *
    }

    DNSClientCache = Invoke-ReportSection 'DNSClientCache' {
        Get-DnsClientCache -ErrorAction SilentlyContinue |
            Select-Object -First 200 Entry, RecordName, RecordType, Data, Status, Section, TimeToLive
    }

    NetRoutes = Invoke-ReportSection 'NetRoutes' {
        Get-NetRoute -ErrorAction SilentlyContinue | Select-Object *
    }

    NetNeighbors = Invoke-ReportSection 'NetNeighbors' {
        Get-NetNeighbor -ErrorAction SilentlyContinue | Select-Object *
    }

    NetTCPConnections = Invoke-ReportSection 'NetTCPConnections' {
        $all = Get-NetTCPConnection -ErrorAction SilentlyContinue
        $listen = $all | Where-Object State -eq 'Listen'
        $other = $all | Where-Object State -ne 'Listen' | Select-Object -First 300
        @($listen + $other) |
            Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess,
                @{ n = 'ProcessName'; e = { $procMap[$_.OwningProcess] } }
    }

    NetUDPEndpoints = Invoke-ReportSection 'NetUDPEndpoints' {
        Get-NetUDPEndpoint -ErrorAction SilentlyContinue |
            Select-Object -First 300 LocalAddress, LocalPort, OwningProcess,
                @{ n = 'ProcessName'; e = { $procMap[$_.OwningProcess] } }
    }

    ListeningPorts = Invoke-ReportSection 'ListeningPorts' {
        Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
            Select-Object LocalAddress, LocalPort, OwningProcess,
                @{ n = 'ProcessName'; e = { $procMap[$_.OwningProcess] } }
    }

    FirewallProfiles = Invoke-ReportSection 'FirewallProfiles' {
        Get-NetFirewallProfile -ErrorAction SilentlyContinue | Select-Object *
    }

    NetworkProfiles = Invoke-ReportSection 'NetworkProfiles' {
        Get-NetConnectionProfile -ErrorAction SilentlyContinue | Select-Object *
    }

    ProxySettings = Invoke-ReportSection 'ProxySettings' {
        Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
            Select-Object ProxyEnable, ProxyServer, ProxyOverride, AutoConfigURL
    }

    WinHttpProxy = Invoke-ReportSection 'WinHttpProxy' {
        netsh winhttp show proxy 2>$null
    }

  # --- Security ---
    SecureBoot = Invoke-ReportSection 'SecureBoot' {
        if (Get-Command Confirm-SecureBootUEFI -ErrorAction SilentlyContinue) {
            Confirm-SecureBootUEFI
        }
    }

    Tpm = Invoke-ReportSection 'Tpm' {
        Get-Tpm -ErrorAction SilentlyContinue | Select-Object *
    }

    WindowsDefender = Invoke-ReportSection 'WindowsDefender' {
        Get-MpComputerStatus -ErrorAction SilentlyContinue | Select-Object *
    }

    DefenderPreferences = Invoke-ReportSection 'DefenderPreferences' {
        Get-MpPreference -ErrorAction SilentlyContinue | Select-Object *
    }

    LocalUsers = Invoke-ReportSection 'LocalUsers' {
        Get-LocalUser -ErrorAction SilentlyContinue |
            Select-Object Name, Enabled, Description, LastLogon, PasswordExpires, UserMayChangePassword, PasswordRequired, SID
    }

    LocalGroups = Invoke-ReportSection 'LocalGroups' {
        Get-LocalGroup -ErrorAction SilentlyContinue | Select-Object Name, SID, Description
    }

    LoggedOnUsers = Invoke-ReportSection 'LoggedOnUsers' {
        Get-CimInstance Win32_LoggedOnUser -ErrorAction SilentlyContinue |
            Select-Object Antecedent, Dependent
    }

    UserProfiles = Invoke-ReportSection 'UserProfiles' {
        Get-CimInstance Win32_UserProfile -ErrorAction SilentlyContinue |
            Select-Object LocalPath, SID, Loaded, Special, LastUseTime, Status
    }

  # --- Software & updates ---
    HotFixes = Invoke-ReportSection 'HotFixes' {
        Get-HotFix -ErrorAction SilentlyContinue | Select-Object *
    }

    PackageManagement = Invoke-ReportSection 'PackageManagement' {
        Get-Package -ErrorAction SilentlyContinue | Select-Object Name, Version, ProviderName, Source
    }

    StartupCommands = Invoke-ReportSection 'StartupCommands' {
        Get-CimInstance Win32_StartupCommand -ErrorAction SilentlyContinue | Select-Object *
    }

    AutoRun = Invoke-ReportSection 'AutoRun' {
        $paths = @(
            'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
            'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce',
            'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
            'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce'
        )
        foreach ($p in $paths) {
            $items = Get-ItemProperty $p -ErrorAction SilentlyContinue
            if (-not $items) { continue }
            $values = [ordered]@{}
            foreach ($prop in $items.PSObject.Properties) {
                if ($prop.Name -match '^(PSPath|PSParentPath|PSChildName|PSDrive|PSProvider)$') { continue }
                $values[$prop.Name] = [string]$prop.Value
            }
            if ($values.Count -gt 0) {
                [pscustomobject]@{ RegistryPath = $p; Values = $values }
            }
        }
    }

  # --- Runtime state ---
    Processes = Invoke-ReportSection 'Processes' {
        # Avoid .Path / .Company / .Description — each triggers extra lookups per process.
        Get-Process -ErrorAction SilentlyContinue |
            Select-Object Name, Id, CPU, WorkingSet64, PM, Handles, StartTime,
                @{ n = 'WorkingSetMB'; e = { [math]::Round($_.WorkingSet64 / 1MB, 2) } }
    }

    Services = Invoke-ReportSection 'Services' {
        Get-Service -ErrorAction SilentlyContinue |
            Select-Object Name, DisplayName, Status, StartType, ServiceType
    }

    ScheduledTasks = Invoke-ReportSection 'ScheduledTasks' {
        Get-ScheduledTask -ErrorAction SilentlyContinue |
            Select-Object TaskName, TaskPath, State
    }

    EnvironmentVariables = Invoke-ReportSection 'EnvironmentVariables' {
        Get-ChildItem Env: | Sort-Object Name | Select-Object Name, Value
    }

    Performance = Invoke-ReportSection 'Performance' {
        $os = Get-CimInstance Win32_OperatingSystem
        [ordered]@{
            TotalVisibleMemoryGB  = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
            FreePhysicalMemoryGB  = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
            TotalVirtualMemoryGB  = [math]::Round($os.TotalVirtualMemorySize / 1MB, 2)
            FreeVirtualMemoryGB   = [math]::Round($os.FreeVirtualMemory / 1MB, 2)
            Uptime                = (Get-Date) - $os.LastBootUpTime
            LastBootUpTime        = $os.LastBootUpTime
        }
    }

  # --- Shares & printers ---
    SmbShares = Invoke-ReportSection 'SmbShares' {
        Get-SmbShare -ErrorAction SilentlyContinue | Select-Object *
    }

    Printers = Invoke-ReportSection 'Printers' {
        Get-Printer -ErrorAction SilentlyContinue | Select-Object *
    }

  # --- Licensing ---
    WindowsLicense = Invoke-ReportSection 'WindowsLicense' {
        Get-CimInstance SoftwareLicensingProduct -ErrorAction SilentlyContinue |
            Where-Object { $_.PartialProductKey } |
            Select-Object Name, Description, LicenseStatus, LicenseStatusReason, PartialProductKey
    }

  # --- External command captures ---
    SystemInfo = Invoke-ReportSection 'SystemInfo' {
        systeminfo
    }

    IpConfigAll = Invoke-ReportSection 'IpConfigAll' {
        ipconfig /all
    }

    BcdEdit = Invoke-ReportSection 'BcdEdit' {
        bcdedit /enum all 2>$null
    }
}

# --- Optional heavy sections (slow; enable with -IncludeAll or individual switches) ---
if ($IncludeAll) {
    Write-ReportProgress 'Collecting ComputerInfo (slow)...'
    $report.ComputerInfo = Invoke-ReportSection 'ComputerInfo' {
        Get-ComputerInfo | Select-Object *
    }
    Write-ReportProgress 'Collecting Windows optional features (DISM, very slow)...'
    $report.WindowsFeatures = Invoke-ReportSection 'WindowsFeatures' {
        Get-WindowsOptionalFeature -Online -ErrorAction SilentlyContinue |
            Select-Object FeatureName, State
    }
    Write-ReportProgress 'Collecting AppX packages...'
    $report.AppxPackages = Invoke-ReportSection 'AppxPackages' {
        Get-AppxPackage -ErrorAction SilentlyContinue |
            Select-Object Name, PackageFullName, Version, Publisher, InstallLocation, IsFramework, IsResourcePackage
    }
    Write-ReportProgress 'Collecting local group members...'
    $report.LocalGroupMembers = Invoke-ReportSection 'LocalGroupMembers' {
        Get-LocalGroup -ErrorAction SilentlyContinue |
            ForEach-Object {
                $members = Get-LocalGroupMember -Group $_.Name -ErrorAction SilentlyContinue |
                    Select-Object Name, ObjectClass, PrincipalSource
                [pscustomobject]@{ Group = $_.Name; SID = $_.SID; Members = $members }
            }
    }
}

if ($IncludeInstalledSoftware) {
    $report.InstalledSoftware_x86 = Invoke-ReportSection 'InstalledSoftware_x86' {
        Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
            'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
            Where-Object { $_.DisplayName } |
            Select-Object DisplayName, DisplayVersion, Publisher, InstallDate, InstallLocation, UninstallString
    }
    $report.InstalledSoftware_CurrentUser = Invoke-ReportSection 'InstalledSoftware_CurrentUser' {
        Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
            Where-Object { $_.DisplayName } |
            Select-Object DisplayName, DisplayVersion, Publisher, InstallDate
    }
}

if ($IncludeFirewallRules) {
    $report.FirewallRules = Invoke-ReportSection 'FirewallRules' {
        Get-NetFirewallRule -ErrorAction SilentlyContinue |
            Select-Object -First $MaxFirewallRules |
            ForEach-Object {
                $portFilter = $_ | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
                $addrFilter = $_ | Get-NetFirewallAddressFilter -ErrorAction SilentlyContinue
                [pscustomobject]@{
                    DisplayName = $_.DisplayName
                    Name        = $_.Name
                    Enabled     = $_.Enabled
                    Direction   = $_.Direction
                    Action      = $_.Action
                    Profile     = $_.Profile
                    LocalPort   = $portFilter.LocalPort
                    RemotePort  = $portFilter.RemotePort
                    Protocol    = $portFilter.Protocol
                    RemoteAddress = $addrFilter.RemoteAddress
                    LocalAddress  = $addrFilter.LocalAddress
                }
            }
    }
    $report.FirewallRulesNote = "Capped at $MaxFirewallRules rules. Use -MaxFirewallRules to adjust."
}

if ($IncludeEventLogs) {
    $report.EventLogs = Invoke-ReportSection 'EventLogs' {
        'System', 'Application', 'Security' | ForEach-Object {
            $logName = $_
            $entries = Get-WinEvent -LogName $logName -MaxEvents $MaxEventLogEntries -ErrorAction SilentlyContinue |
                Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message
            [pscustomobject]@{ LogName = $logName; Entries = $entries }
        }
    }
    $report.EventLogsNote = "Capped at $MaxEventLogEntries entries per log."
}

if ($IncludeCertificates) {
    $report.Certificates_LocalMachine_My = Invoke-ReportSection 'Certificates' {
        Get-ChildItem Cert:\LocalMachine\My -ErrorAction SilentlyContinue |
            Select-Object Subject, Issuer, NotBefore, NotAfter, Thumbprint, HasPrivateKey
    }
    $report.Certificates_CurrentUser_My = Invoke-ReportSection 'CertificatesCU' {
        Get-ChildItem Cert:\CurrentUser\My -ErrorAction SilentlyContinue |
            Select-Object Subject, Issuer, NotBefore, NotAfter, Thumbprint, HasPrivateKey
    }
}

if (-not $OutputPath) {
    $desktop = [Environment]::GetFolderPath('Desktop')
    if (-not $desktop) {
        $desktop = Join-Path $env:USERPROFILE 'Documents'
    }
    $OutputPath = Join-Path $desktop "SystemInventory-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
}

$outputDir = Split-Path -Parent $OutputPath
if ($outputDir -and -not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

Write-ReportProgress "Writing JSON sections to $OutputPath ..."
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
try {
    $sw = [System.IO.StreamWriter]::new($OutputPath, $false, $utf8NoBom)
}
catch {
    throw "Cannot create output file '$OutputPath': $($_.Exception.Message)"
}
$sw.WriteLine('{')
$first = $true
foreach ($key in $report.Keys) {
    Write-ReportProgress "  JSON: $key"
    try {
        $sectionJson = ($report[$key] | ConvertTo-Json -Depth 15 -Compress:$false -WarningAction SilentlyContinue)
    }
    catch {
        $sectionJson = (@{ _status = 'serialization_error'; _error = $_.Exception.Message } | ConvertTo-Json -Compress)
    }
    if (-not $first) { $sw.WriteLine(',') }
    $escapedKey = $key -replace '\\', '\\\\' -replace '"', '\"'
    $sw.Write("  `"$escapedKey`": ")
    $sw.Write($sectionJson)
    $first = $false
}
try {
    $sw.WriteLine()
    $sw.WriteLine('}')
}
finally {
    if ($sw) { $sw.Close(); $sw.Dispose() }
}

Write-Host "Report written to: $OutputPath ($([math]::Round((Get-Item -LiteralPath $OutputPath).Length / 1MB, 2)) MB)"

# Return path instead of dumping megabytes to the console
$OutputPath
