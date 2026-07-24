param(
    [string]$Root = ".",
    [string]$ActorId = "",
    [string]$Timestamp = "",
    [string]$Commit = "",
    [switch]$Check,
    [switch]$Apply
)

$ErrorActionPreference = "Stop"

# Parity note: both -Check and -Apply delegate to the Python implementation,
# so mailbox pruning semantics stay identical across entrypoints.
if (($Check -and $Apply) -or (-not $Check -and -not $Apply)) {
    Write-Error "Use exactly one of -Check or -Apply."
    exit 2
}

$scriptPath = Join-Path $PSScriptRoot "prune_state.py"
$mode = if ($Check) { "--check" } else { "--apply" }
$argsList = @($scriptPath, "--root", $Root, $mode)
if ($ActorId) { $argsList += @("--actor-id", $ActorId) }
if ($Timestamp) { $argsList += @("--timestamp", $Timestamp) }
if ($Commit) { $argsList += @("--commit", $Commit) }
python @argsList
exit $LASTEXITCODE
