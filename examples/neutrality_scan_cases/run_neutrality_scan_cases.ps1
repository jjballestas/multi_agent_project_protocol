param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
)

$ErrorActionPreference = "Stop"

$cases = @(
    @{ Name = "clean"; Exit = 0 },
    @{ Name = "domain_term_in_core"; Exit = 1 }
)

$pythonScanner = Join-Path $RepoRoot "scripts/scan_domain_neutrality.py"
$powershellScanner = Join-Path $RepoRoot "scripts/scan_domain_neutrality.ps1"
$failed = $false

function Resolve-Runtime {
    param([array]$Candidates)

    foreach ($candidate in $Candidates) {
        $command = Get-Command $candidate.Exe -ErrorAction SilentlyContinue
        if (-not $command) {
            continue
        }

        try {
            & $command.Source @($candidate.Args + $candidate.VersionArgs) 1>$null 2>$null
            if ($LASTEXITCODE -eq 0) {
                return [pscustomobject]@{
                    Exe = $command.Source
                    Args = $candidate.Args
                    Label = if ($candidate.Args.Count -gt 0) { "$($candidate.Exe) $($candidate.Args -join ' ')" } else { $candidate.Exe }
                }
            }
        } catch {
            continue
        }
    }

    return $null
}

$pythonRuntime = Resolve-Runtime -Candidates @(
    @{ Exe = "python"; Args = @(); VersionArgs = @("--version") },
    @{ Exe = "py"; Args = @("-3"); VersionArgs = @("--version") },
    @{ Exe = "python3"; Args = @(); VersionArgs = @("--version") }
)
$powershellRuntime = Resolve-Runtime -Candidates @(
    @{ Exe = "pwsh"; Args = @(); VersionArgs = @("--version") },
    @{ Exe = "powershell"; Args = @(); VersionArgs = @("-NoProfile", "-Command", '$PSVersionTable.PSVersion.ToString()') }
)

if (-not $pythonRuntime -or -not $powershellRuntime) {
    Write-Host "FAIL: neutrality scan parity requires Python and PowerShell runtimes."
    exit 1
}

foreach ($case in $cases) {
    $caseRoot = Join-Path $PSScriptRoot $case.Name
    $pythonOutput = & $pythonRuntime.Exe @($pythonRuntime.Args + @($pythonScanner, "--root", $caseRoot)) 2>&1 | Out-String
    $pythonExit = $LASTEXITCODE
    $powershellOutput = & $powershellRuntime.Exe @($powershellRuntime.Args + @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $powershellScanner, "-Root", $caseRoot)) 2>&1 | Out-String
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
        Write-Host "FAIL $($case.Name): scanner outputs differ"
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

Write-Host "OK: neutrality scan cases passed."
