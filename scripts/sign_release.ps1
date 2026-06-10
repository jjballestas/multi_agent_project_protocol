param(
    [string]$Manifest = "",
    [string]$Digest = "",
    [Parameter(Mandatory = $true)][string]$Backend,
    [string]$Key = "",
    [string]$KeyId = "",
    [string]$Identity = "",
    [string]$Issuer = "",
    [string]$SignCommand = "",
    [string]$SignatureField = "",
    [string]$Output = "-"
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

if (($Manifest -and $Digest) -or (-not $Manifest -and -not $Digest)) {
    throw "Provide exactly one of -Manifest or -Digest."
}

$python = Resolve-Python
$scriptPath = Join-Path $PSScriptRoot "sign_release.py"
$arguments = @($python.Args + @($scriptPath, "--backend", $Backend, "--output", $Output))
if ($Manifest) {
    $arguments += @("--manifest", $Manifest)
}
if ($Digest) {
    $arguments += @("--digest", $Digest)
}
if ($Key) {
    $arguments += @("--key", $Key)
}
if ($KeyId) {
    $arguments += @("--key-id", $KeyId)
}
if ($Identity) {
    $arguments += @("--identity", $Identity)
}
if ($Issuer) {
    $arguments += @("--issuer", $Issuer)
}
if ($SignCommand) {
    $arguments += @("--sign-command", $SignCommand)
}
if ($SignatureField) {
    $arguments += @("--signature-field", $SignatureField)
}

& $python.Exe @arguments
exit $LASTEXITCODE
