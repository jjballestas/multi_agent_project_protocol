param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)

$ErrorActionPreference = "Stop"

$cases = @(
    @{ Name = "valid_compact"; Exit = 0 },
    @{ Name = "missing_question"; Exit = 1 },
    @{ Name = "legacy_exempt"; Exit = 0 },
    @{ Name = "missing_context_refs_warning"; Exit = 0 },
    @{ Name = "minimal_frontmatter"; Exit = 0 }
)

$pythonValidator = Join-Path $RepoRoot "scripts/validate_collaboration_state.py"
$powershellValidator = Join-Path $RepoRoot "scripts/validate_collaboration_state.ps1"
$failed = $false
$pyStats = @{ ok = 0; skip = 0; fail = 0 }
$psStats = @{ ok = 0; skip = 0; fail = 0 }
$parityStats = @{ checked = 0; skipped = 0 }

function Resolve-Runtime {
    param(
        [string]$Name,
        [array]$Candidates
    )

    foreach ($candidate in $Candidates) {
        $command = Get-Command $candidate.Exe -ErrorAction SilentlyContinue
        if (-not $command) {
            continue
        }

        try {
            $versionOutput = & $command.Source @($candidate.Args + $candidate.VersionArgs) 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                return [pscustomobject]@{
                    Name = $Name
                    Exe = $command.Source
                    Args = $candidate.Args
                    Label = if ($candidate.Args.Count -gt 0) { "$($candidate.Exe) $($candidate.Args -join ' ')" } else { $candidate.Exe }
                    Version = $versionOutput.Trim()
                }
            }
        } catch {
            continue
        }
    }

    return $null
}

function Normalize-Output {
    param([string]$Output)

    return $Output.Trim() -replace "`r`n", "`n"
}

$pythonRuntime = Resolve-Runtime -Name "Python" -Candidates @(
    @{ Exe = "python"; Args = @(); VersionArgs = @("--version") },
    @{ Exe = "py"; Args = @("-3"); VersionArgs = @("--version") },
    @{ Exe = "python3"; Args = @(); VersionArgs = @("--version") }
)
$powershellRuntime = Resolve-Runtime -Name "PowerShell" -Candidates @(
    @{ Exe = "pwsh"; Args = @(); VersionArgs = @("--version") },
    @{ Exe = "powershell"; Args = @(); VersionArgs = @("-NoProfile", "-Command", '$PSVersionTable.PSVersion.ToString()') }
)

if ($pythonRuntime) {
    Write-Host "Runtime Python: $($pythonRuntime.Label) ($($pythonRuntime.Version))"
} else {
    Write-Host "Runtime Python: none"
}

if ($powershellRuntime) {
    Write-Host "Runtime PowerShell: $($powershellRuntime.Label) ($($powershellRuntime.Version))"
} else {
    Write-Host "Runtime PowerShell: none"
}

foreach ($case in $cases) {
    $caseRoot = Join-Path $PSScriptRoot $case.Name
    $caseFailed = $false
    $pythonOutput = $null
    $powershellOutput = $null

    if ($pythonRuntime) {
        $pythonOutput = & $pythonRuntime.Exe @($pythonRuntime.Args + @($pythonValidator, "--root", $caseRoot)) 2>&1 | Out-String
        $pythonExit = $LASTEXITCODE

        if ($pythonExit -ne $case.Exit) {
            Write-Host "FAIL $($case.Name): Python exit $pythonExit, expected $($case.Exit)"
            $pyStats.fail++
            $caseFailed = $true
            $failed = $true
        } else {
            $pyStats.ok++
        }
    } else {
        Write-Host "SKIPPED (WARNING) $($case.Name): Python runtime not resolved; skipping Python half."
        $pyStats.skip++
    }

    if ($powershellRuntime) {
        $powershellOutput = & $powershellRuntime.Exe @($powershellRuntime.Args + @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $powershellValidator, "-Root", $caseRoot)) 2>&1 | Out-String
        $powershellExit = $LASTEXITCODE

        if ($powershellExit -ne $case.Exit) {
            Write-Host "FAIL $($case.Name): PowerShell exit $powershellExit, expected $($case.Exit)"
            $psStats.fail++
            $caseFailed = $true
            $failed = $true
        } else {
            $psStats.ok++
        }
    } else {
        Write-Host "SKIPPED (WARNING) $($case.Name): PowerShell runtime not resolved; skipping PowerShell half."
        $psStats.skip++
    }

    if ($pythonRuntime -and $powershellRuntime) {
        $normalizedPython = Normalize-Output -Output $pythonOutput
        $normalizedPowerShell = Normalize-Output -Output $powershellOutput

        if ($normalizedPython -ne $normalizedPowerShell) {
            Write-Host "FAIL $($case.Name): validator outputs differ"
            Write-Host "PYTHON:"
            Write-Host $normalizedPython
            Write-Host "POWERSHELL:"
            Write-Host $normalizedPowerShell
            $parityStats.checked++
            $caseFailed = $true
            $failed = $true
        } else {
            $parityStats.checked++
        }
    } else {
        $parityStats.skipped++
    }

    if (-not $caseFailed) {
        Write-Host "OK $($case.Name)"
    }
}

if (-not $pythonRuntime -and -not $powershellRuntime) {
    Write-Host "FAIL: no Python or PowerShell runtime resolved; cannot verify compact communication validation cases."
    $failed = $true
}

Write-Host "RESUMEN: py[ok=$($pyStats.ok) skip=$($pyStats.skip) fail=$($pyStats.fail)] ps[ok=$($psStats.ok) skip=$($psStats.skip) fail=$($psStats.fail)] paridad[checked=$($parityStats.checked) skipped=$($parityStats.skipped)]"

if ($failed) {
    exit 1
}

Write-Host "OK: compact communication validation cases passed."
