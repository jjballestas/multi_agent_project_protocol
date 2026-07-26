[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory = $true)][string]$Python,
    [Parameter(Mandatory = $true)][string[]]$ScanRoot,
    [Parameter(Mandatory = $true)][string]$ScratchRoot,
    [string[]]$KnownRepo = @(),
    [string[]]$AllowHome = @(),
    [ValidateRange(1, 64)][int]$MaxDepth = 2,
    [ValidateRange(5, 1440)][int]$IntervalMinutes = 30,
    [string]$TaskName = "ProtocolScratchDisciplineMonitor"
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$monitor = Join-Path $PSScriptRoot "run_scratch_discipline_monitor.py"
$arguments = @($monitor, "--")
foreach ($root in $ScanRoot) { $arguments += @("--scan-root", $root) }
$arguments += @("--scratch-root", $ScratchRoot, "--max-depth", [string]$MaxDepth)
foreach ($repo in $KnownRepo) { $arguments += @("--known-repo", $repo) }
foreach ($canonicalPath in $AllowHome) { $arguments += @("--allow-home", $canonicalPath) }

$quoted = $arguments | ForEach-Object {
    $escaped = $_ -replace '(\\*)"', '$1$1\"'
    $escaped = $escaped -replace '(\\+)$', '$1$1'
    '"' + $escaped + '"'
}
$argumentLine = $quoted -join " "
if ($WhatIfPreference) { Write-Host "Scheduled task arguments: $argumentLine" }
Write-Verbose "Scheduled task arguments: $argumentLine"
$action = New-ScheduledTaskAction -Execute $Python -Argument $argumentLine -WorkingDirectory $repoRoot
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew

if ($PSCmdlet.ShouldProcess($TaskName, "register periodic host-local scratch-discipline monitor")) {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
        -Settings $settings -Description "Host-local DECISION-0018 scratch-discipline enforcement" `
        -Force | Out-Null
}
