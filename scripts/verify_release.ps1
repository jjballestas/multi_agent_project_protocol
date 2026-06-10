param(
    [string]$Root = ".",
    [Parameter(Mandatory = $true)][string]$Manifest,
    [string]$Output = "-",
    [string]$Signature = "",
    [string]$Backend = "",
    [string]$Pubkey = "",
    [string]$Key = "",
    [string]$VerifyCommand = ""
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
$scriptPath = Join-Path $PSScriptRoot "verify_release.py"
$arguments = @($python.Args + @($scriptPath, "--root", $Root, "--manifest", $Manifest, "--output", $Output))
if ($Signature) {
    $arguments += @("--signature", $Signature)
}
if ($Backend) {
    $arguments += @("--backend", $Backend)
}
if ($Pubkey) {
    $arguments += @("--pubkey", $Pubkey)
}
if ($Key) {
    $arguments += @("--key", $Key)
}
if ($VerifyCommand) {
    $arguments += @("--verify-command", $VerifyCommand)
}

& $python.Exe @arguments
exit $LASTEXITCODE
