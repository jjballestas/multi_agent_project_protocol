param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)

$ErrorActionPreference = "Stop"

$cases = @(
    @{ Name = "valid_compact"; Exit = 0 },
    @{ Name = "missing_question"; Exit = 1 },
    @{ Name = "legacy_exempt"; Exit = 0 },
    @{ Name = "missing_context_refs_warning"; Exit = 0 }
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

    if ($pythonExit -ne $case.Exit) {
        Write-Host "FAIL $($case.Name): Python exit $pythonExit, expected $($case.Exit)"
        $failed = $true
    }
    if ($powershellExit -ne $case.Exit) {
        Write-Host "FAIL $($case.Name): PowerShell exit $powershellExit, expected $($case.Exit)"
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

Write-Host "OK: compact communication validation cases passed."
