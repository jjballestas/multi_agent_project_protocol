param(
    [string]$Root = ".",
    [Parameter(Mandatory = $true)][string]$Commit,
    [Parameter(Mandatory = $true)][string]$Timestamp,
    [string]$Output = "-",
    [string[]]$IncludeGlob = @(),
    [string[]]$ExcludeGlob = @(),
    [switch]$NoDefaultGlobs
)

$ErrorActionPreference = "Stop"

function Resolve-Python {
    $candidates = @(
        @{ Exe = "python"; Args = @(); VersionArgs = @("--version") },
        @{ Exe = "py"; Args = @("-3"); VersionArgs = @("--version") },
        @{ Exe = "python3"; Args = @(); VersionArgs = @("--version") }
    )
    foreach ($candidate in $candidates) {
        $command = Get-Command $candidate.Exe -ErrorAction SilentlyContinue
        if (-not $command) {
            continue
        }
        & $command.Source @($candidate.Args + $candidate.VersionArgs) 1>$null 2>$null
        if ($LASTEXITCODE -eq 0) {
            return [pscustomobject]@{ Exe = $command.Source; Args = $candidate.Args }
        }
    }
    throw "Python runtime not found."
}

$python = Resolve-Python
$scriptPath = Join-Path $PSScriptRoot "generate_sbom.py"
$arguments = @($python.Args + @($scriptPath, "--root", $Root, "--commit", $Commit, "--timestamp", $Timestamp, "--output", $Output))
foreach ($glob in $IncludeGlob) {
    $arguments += @("--include-glob", $glob)
}
foreach ($glob in $ExcludeGlob) {
    $arguments += @("--exclude-glob", $glob)
}
if ($NoDefaultGlobs) {
    $arguments += "--no-default-globs"
}

& $python.Exe @arguments
exit $LASTEXITCODE
