[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$Root = ".",
    [Parameter(Mandatory = $true)]
    [ValidateSet("auto-claim", "handoff-release")]
    [string]$Operation,
    [Parameter(Mandatory = $true)]
    [string]$ActorId,
    [Parameter(Mandatory = $true)]
    [string]$Timestamp,
    [string]$Commit = "",
    [Parameter(Mandatory = $true)]
    [string]$TaskId,
    [Parameter(Mandatory = $true)]
    [string]$ClaimId,
    [string]$FromStatus = "",
    [string]$ToStatus = "",
    [string[]]$Scope = @(),
    [string]$Owner = "",
    [string]$ExpiresAt = "",
    [string]$StartedAt = "",
    [string]$UpdatedAt = "",
    [string]$Notes = "",
    [string[]]$TaskUpsertJson = @(),
    [switch]$Submit,
    [string]$Output = "-"
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "ledger_ops.py"
$pythonArgs = @(
    $scriptPath,
    "--root", $Root,
    "--operation", $Operation,
    "--actor-id", $ActorId,
    "--timestamp", $Timestamp,
    "--task-id", $TaskId,
    "--claim-id", $ClaimId,
    "--output", $Output
)

if ($Commit) {
    $pythonArgs += @("--commit", $Commit)
}
if ($FromStatus) {
    $pythonArgs += @("--from-status", $FromStatus)
}
if ($ToStatus) {
    $pythonArgs += @("--to-status", $ToStatus)
}
foreach ($Item in $Scope) {
    foreach ($ScopeEntry in ($Item -split ",")) {
        if ($ScopeEntry) {
            $pythonArgs += @("--scope", $ScopeEntry)
        }
    }
}
if ($Owner) {
    $pythonArgs += @("--owner", $Owner)
}
if ($ExpiresAt) {
    $pythonArgs += @("--expires-at", $ExpiresAt)
}
if ($StartedAt) {
    $pythonArgs += @("--started-at", $StartedAt)
}
if ($UpdatedAt) {
    $pythonArgs += @("--updated-at", $UpdatedAt)
}
if ($Notes) {
    $pythonArgs += @("--notes", $Notes)
}
foreach ($Item in $TaskUpsertJson) {
    if ($Item) {
        $pythonArgs += @("--task-upsert-json", $Item)
    }
}
if ($Submit.IsPresent) {
    $pythonArgs += "--submit"
}

python @pythonArgs
exit $LASTEXITCODE
