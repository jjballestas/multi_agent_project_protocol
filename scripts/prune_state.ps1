param(
    [string]$Root = ".",
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
python $scriptPath --root $Root $mode
exit $LASTEXITCODE
