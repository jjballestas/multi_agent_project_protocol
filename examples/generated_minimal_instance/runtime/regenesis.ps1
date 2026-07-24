param(
    [string]$Root = ".",
    [Parameter(Mandatory = $true)]
    [string]$ActorId,
    [Parameter(Mandatory = $true)]
    [string]$Timestamp,
    [string]$Commit = "",
    [string]$IdempotencyKey = "",
    [string]$Output = "-"
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "regenesis.py"
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
if ($IdempotencyKey) {
    $pythonArgs += @("--idempotency-key", $IdempotencyKey)
}

python @pythonArgs
exit $LASTEXITCODE
