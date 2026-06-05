param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path $Root).Path
$fixtureRoot = Join-Path $repoRoot "examples/context_cost_cases/fixture"
$pythonScript = Join-Path $repoRoot "scripts/measure_context_cost.py"
$psScript = Join-Path $repoRoot "scripts/measure_context_cost.ps1"

function Assert-Equal {
    param(
        $Actual,
        $Expected,
        [string]$Label
    )
    if ($Actual -ne $Expected) {
        throw "$Label expected '$Expected' but got '$Actual'"
    }
}

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Label
    )
    if (-not $Condition) {
        throw $Label
    }
}

$pyJson = python $pythonScript --root $fixtureRoot --json | ConvertFrom-Json
$psJson = powershell -NoProfile -ExecutionPolicy Bypass -File $psScript -Root $fixtureRoot -Json | ConvertFrom-Json
$budgetOutput = python $pythonScript --root $fixtureRoot --budget

Assert-Equal $pyJson.chars_per_token 10 "python chars_per_token"
Assert-Equal $pyJson.dead_weight.claims.total 2 "python claims total"
Assert-Equal $pyJson.dead_weight.claims.released 1 "python released claims"
Assert-Equal $pyJson.dead_weight.claims.released_percent 50 "python released percent"
Assert-Equal $pyJson.dead_weight.tasks.total 2 "python tasks total"
Assert-Equal $pyJson.dead_weight.tasks.done 1 "python done tasks"
Assert-Equal $pyJson.dead_weight.tasks.done_percent 50 "python done percent"
Assert-Equal $pyJson.mailbox_overhead.message_count 1 "python mailbox count"
Assert-True $pyJson.budget.exceeded "python budget should be exceeded"
Assert-True (($budgetOutput -join "`n") -match "WARNING: cold-start tokens") "budget warning should be printed"

Assert-Equal $psJson.chars_per_token $pyJson.chars_per_token "parity chars_per_token"
Assert-Equal $psJson.cold_start.total_tokens $pyJson.cold_start.total_tokens "parity cold_start tokens"
Assert-Equal $psJson.dead_weight.claims.released_percent $pyJson.dead_weight.claims.released_percent "parity claims percent"
Assert-Equal $psJson.dead_weight.tasks.done_percent $pyJson.dead_weight.tasks.done_percent "parity tasks percent"
Assert-Equal $psJson.mailbox_overhead.message_count $pyJson.mailbox_overhead.message_count "parity mailbox count"

Write-Host "OK: context cost cases passed."
