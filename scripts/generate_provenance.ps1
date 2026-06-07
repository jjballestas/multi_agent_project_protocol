param(
    [Parameter(Mandatory = $true)][string]$Manifest,
    [string]$Output = "-",
    [switch]$Verify,
    [string]$Provenance = "",
    [string]$BuilderId = "",
    [string]$Commit = "",
    [Alias("Process")][string]$InvocationProcess = "",
    [string]$Timestamp = "",
    [string]$SubjectName = ""
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
$scriptPath = Join-Path $PSScriptRoot "generate_provenance.py"
$arguments = @($python.Args + @($scriptPath, "--manifest", $Manifest, "--output", $Output))
if ($Verify) {
    $arguments += "--verify"
    if ($Provenance) {
        $arguments += @("--provenance", $Provenance)
    }
} else {
    if ($BuilderId) {
        $arguments += @("--builder-id", $BuilderId)
    }
    if ($Commit) {
        $arguments += @("--commit", $Commit)
    }
    if ($InvocationProcess) {
        $arguments += @("--process", $InvocationProcess)
    }
    if ($Timestamp) {
        $arguments += @("--timestamp", $Timestamp)
    }
    if ($SubjectName) {
        $arguments += @("--subject-name", $SubjectName)
    }
}

& $python.Exe @arguments
exit $LASTEXITCODE
