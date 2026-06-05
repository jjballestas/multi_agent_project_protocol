param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)

$ErrorActionPreference = "Stop"

$cases = @(
    @{ Name = "legitimate_open"; Exit = 0; ExpectedWarnings = 0 },
    @{ Name = "resolved_in_open"; Exit = 0; ExpectedWarnings = 1 },
    @{ Name = "fyi_no_response"; Exit = 0; ExpectedWarnings = 1 },
    @{ Name = "legacy_message"; Exit = 0; ExpectedWarnings = 0 }
)

$pythonValidator = Join-Path $RepoRoot "scripts/validate_collaboration_state.py"
$powershellValidator = Join-Path $RepoRoot "scripts/validate_collaboration_state.ps1"
$failed = $false

foreach ($case in $cases) {
    $caseRoot = Join-Path $PSScriptRoot $case.Name
    $pythonOutput = & python $pythonValidator --root $caseRoot 2>&1 | Out-String
    $pythonExit = $LASTEXITCODE
    $powershellOutput = & powershell -NoProfile -ExecutionPolicy Bypass -File $powershellValidator -Root $caseRoot 2>&1 | Out-String
    $powershellExit = $LASTEXITCODE

    $normalizedPython = $pythonOutput.Trim() -replace "`r`n", "`n"
    $normalizedPowerShell = $powershellOutput.Trim() -replace "`r`n", "`n"
    $pythonWarnings = ([regex]::Matches($normalizedPython, "Mailbox message .*open/|Mailbox message does not require response")).Count
    $powershellWarnings = ([regex]::Matches($normalizedPowerShell, "Mailbox message .*open/|Mailbox message does not require response")).Count

    if ($pythonExit -ne $case.Exit) {
        Write-Host "FAIL $($case.Name): Python exit $pythonExit, expected $($case.Exit)"
        $failed = $true
    }
    if ($powershellExit -ne $case.Exit) {
        Write-Host "FAIL $($case.Name): PowerShell exit $powershellExit, expected $($case.Exit)"
        $failed = $true
    }
    if ($pythonWarnings -ne $case.ExpectedWarnings) {
        Write-Host "FAIL $($case.Name): Python warnings $pythonWarnings, expected $($case.ExpectedWarnings)"
        Write-Host $normalizedPython
        $failed = $true
    }
    if ($powershellWarnings -ne $case.ExpectedWarnings) {
        Write-Host "FAIL $($case.Name): PowerShell warnings $powershellWarnings, expected $($case.ExpectedWarnings)"
        Write-Host $normalizedPowerShell
        $failed = $true
    }
    if ($normalizedPython -ne $normalizedPowerShell) {
        Write-Host "FAIL $($case.Name): validator outputs differ"
        Write-Host "PYTHON:"
        Write-Host $normalizedPython
        Write-Host "POWERSHELL:"
        Write-Host $normalizedPowerShell
        $failed = $true
    }
    if (-not $failed) {
        Write-Host "OK $($case.Name)"
    }
}

if ($failed) {
    exit 1
}

Write-Host "OK: mailbox hygiene cases passed."
