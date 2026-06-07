param(
    [string]$Root = ".",
    [Parameter(Mandatory = $true)]
    [string]$ActorId,
    [Parameter(Mandatory = $true)]
    [string]$Timestamp,
    [string]$Commit = "",
    [string]$Intent = "",
    [string]$IntentJson = "",
    [string]$Output = "-"
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "submit_intent.py"
$pythonArgs = @(
    $scriptPath,
    "--root", $Root,
    "--actor-id", $ActorId,
    "--timestamp", $Timestamp,
    "--output", $Output
)

if ($Commit) {
    $pythonArgs += @("--commit", $Commit)
}
if ($Intent) {
    $pythonArgs += @("--intent", $Intent)
}
if ($IntentJson) {
    $pythonArgs += @("--intent-json", $IntentJson)
}

python @pythonArgs
exit $LASTEXITCODE
