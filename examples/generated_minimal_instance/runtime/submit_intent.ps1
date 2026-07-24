param(
    [string]$Root = ".",
    [string]$ActorId = "",
    [string]$Timestamp = "",
    [string]$Commit = "",
    [string]$Intent = "",
    [string]$IntentJson = "",
    [string]$Intents = "",
    [string]$IntentsJson = "",
    [string]$Output = "-"
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "submit_intent.py"
$pythonArgs = @(
    $scriptPath,
    "--root", $Root,
    "--output", $Output
)

if ($ActorId) {
    $pythonArgs += @("--actor-id", $ActorId)
}
if ($Timestamp) {
    $pythonArgs += @("--timestamp", $Timestamp)
}
if ($Commit) {
    $pythonArgs += @("--commit", $Commit)
}
if ($Intent) {
    $pythonArgs += @("--intent", $Intent)
}
if ($IntentJson) {
    $pythonArgs += @("--intent-json", $IntentJson)
}
if ($Intents) {
    $pythonArgs += @("--intents", $Intents)
}
if ($IntentsJson) {
    $pythonArgs += @("--intents-json", $IntentsJson)
}

python @pythonArgs
exit $LASTEXITCODE
