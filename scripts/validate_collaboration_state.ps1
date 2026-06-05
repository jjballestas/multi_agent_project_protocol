param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$ConfigPath = ""
)

$ErrorActionPreference = "Stop"

function Fail {
    param([string]$Message)
    $script:Errors.Add($Message) | Out-Null
}

function Warn {
    param([string]$Message)
    $script:Warnings.Add($Message) | Out-Null
}

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        Fail "Missing file: $Path"
        return $null
    }
    try {
        return Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json
    } catch {
        Fail "Invalid JSON: $Path :: $($_.Exception.Message)"
        return $null
    }
}

function Get-TaskStatusFromMarkdown {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }
    $match = Select-String -LiteralPath $Path -Pattern '^\s*status:\s*(\S+)\s*$' | Select-Object -First 1
    if ($match) {
        return $match.Matches[0].Groups[1].Value
    }
    return $null
}

function Get-ValueByPath {
    param(
        [object]$Object,
        [string]$Path
    )
    $current = $Object
    foreach ($part in $Path.Split(".")) {
        if ($null -eq $current) {
            return $null
        }
        $property = $current.PSObject.Properties[$part]
        if ($null -eq $property) {
            return $null
        }
        $current = $property.Value
    }
    return $current
}

$script:Errors = [System.Collections.Generic.List[string]]::new()
$script:Warnings = [System.Collections.Generic.List[string]]::new()

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
if (-not $ConfigPath) {
    $ConfigPath = Join-Path $resolvedRoot "protocol.config.json"
}

$config = $null
if (Test-Path -LiteralPath $ConfigPath) {
    $config = Read-JsonFile $ConfigPath
} else {
    Warn "Missing protocol config: $ConfigPath. No state invariants will be enforced."
}

$statePath = Join-Path $resolvedRoot "Area_comun/state/PROJECT_STATE.json"
$indexPath = Join-Path $resolvedRoot "Area_comun/state/TASK_INDEX.json"
$claimsPath = Join-Path $resolvedRoot "Area_comun/state/CLAIMS.json"

$state = Read-JsonFile $statePath
$index = Read-JsonFile $indexPath
$claims = Read-JsonFile $claimsPath

if ($state -and $config -and $config.state_invariants) {
    foreach ($invariant in @($config.state_invariants)) {
        if (-not $invariant.path) {
            Fail "State invariant without path"
            continue
        }
        $actual = Get-ValueByPath -Object $state -Path $invariant.path
        if ($invariant.PSObject.Properties.Name -contains "equals") {
            if ([string]$actual -ne [string]$invariant.equals) {
                Fail "State invariant failed at '$($invariant.path)': expected '$($invariant.equals)', found '$actual'"
            }
        }
        if ($invariant.PSObject.Properties.Name -contains "required") {
            if ($invariant.required -and $null -eq $actual) {
                Fail "State invariant failed at '$($invariant.path)': value is required"
            }
        }
    }
}

if ($index -and $index.tasks) {
    foreach ($task in @($index.tasks)) {
        $taskFile = $task.file
        if (-not $taskFile) {
            $taskFile = $task.task_file
        }
        if (-not $taskFile) {
            Fail "Task $($task.id) has no file/task_file field"
            continue
        }

        $taskPath = Join-Path $resolvedRoot $taskFile
        if (-not (Test-Path -LiteralPath $taskPath)) {
            Fail "Task $($task.id) references missing task file: $taskFile"
            continue
        }

        $mdStatus = Get-TaskStatusFromMarkdown $taskPath
        if (-not $mdStatus) {
            Warn "Task $($task.id) file has no status metadata: $taskFile"
        } elseif ($mdStatus -ne $task.status) {
            Fail "Task $($task.id) status mismatch: index='$($task.status)' file='$mdStatus'"
        }

        if ($task.status -in @("in_review", "done")) {
            foreach ($deliverable in @($task.deliverables)) {
                if (-not $deliverable) {
                    continue
                }
                $deliverablePath = Join-Path $resolvedRoot $deliverable
                if (-not (Test-Path -LiteralPath $deliverablePath)) {
                    Fail "Task $($task.id) deliverable missing: $deliverable"
                }
            }
        }
    }
}

$mailboxRoot = Join-Path $resolvedRoot "Area_comun/mailbox"
foreach ($mailboxState in @("open", "answered", "archived")) {
    $mailboxStatePath = Join-Path $mailboxRoot $mailboxState
    if (-not (Test-Path -LiteralPath $mailboxStatePath)) {
        Fail "Missing mailbox folder: Area_comun/mailbox/$mailboxState"
    }
}

$reportsPath = Join-Path $resolvedRoot "Area_comun/reports"
if (-not (Test-Path -LiteralPath $reportsPath)) {
    Fail "Missing reports folder: Area_comun/reports"
} else {
    $reportTemplate = Join-Path $reportsPath "HUMAN_REPORT_TEMPLATE.md"
    if (-not (Test-Path -LiteralPath $reportTemplate)) {
        Fail "Missing human report template: Area_comun/reports/HUMAN_REPORT_TEMPLATE.md"
    }
}

if ($claims -and $claims.claims) {
    foreach ($claim in @($claims.claims)) {
        if (-not $claim.claim_id) { Fail "Claim without claim_id" }
        if (-not $claim.task_id) { Fail "Claim without task_id: $($claim.claim_id)" }
        if (-not $claim.owner) { Fail "Claim without owner: $($claim.claim_id)" }
        if ($claim.status -notin @("active", "released", "blocked")) {
            Fail "Claim $($claim.claim_id) has invalid status '$($claim.status)'"
        }
    }

    $activeClaims = @($claims.claims | Where-Object { $_.status -eq "active" })
    for ($i = 0; $i -lt $activeClaims.Count; $i++) {
        for ($j = $i + 1; $j -lt $activeClaims.Count; $j++) {
            $left = $activeClaims[$i]
            $right = $activeClaims[$j]
            if ($left.owner -eq $right.owner) { continue }
            foreach ($leftScope in @($left.scope)) {
                foreach ($rightScope in @($right.scope)) {
                    if (-not $leftScope -or -not $rightScope) { continue }
                    if ($leftScope -eq "Area_comun/state/CLAIMS.json" -or $rightScope -eq "Area_comun/state/CLAIMS.json") { continue }
                    if ($leftScope -like "Area_comun/mailbox/*" -or $rightScope -like "Area_comun/mailbox/*") { continue }
                    if ($leftScope -eq $rightScope) {
                        Fail "Overlapping active claims: $($left.claim_id) and $($right.claim_id) both scope '$leftScope'"
                    }
                }
            }
        }
    }
}

$handoffDir = Join-Path $resolvedRoot "Area_comun/handoffs"
if (Test-Path -LiteralPath $handoffDir) {
    Get-ChildItem -LiteralPath $handoffDir -Filter "HANDOFF-*.md" | ForEach-Object {
        $content = Get-Content -Raw -LiteralPath $_.FullName
        if ($content -match 'requires_response:\s*(yes|true)') {
            if ($content -notmatch 'response_owner:\s*\S+') {
                Fail "Handoff requires response but has no response_owner: $($_.Name)"
            }
            if ($content -notmatch 'requested_action') {
                Fail "Handoff requires response but has no requested_action: $($_.Name)"
            }
        }
    }
}

$openMailboxDir = Join-Path $resolvedRoot "Area_comun/mailbox/open"
if (Test-Path -LiteralPath $openMailboxDir) {
    Get-ChildItem -LiteralPath $openMailboxDir -Filter "MSG-*.md" | ForEach-Object {
        $content = Get-Content -Raw -LiteralPath $_.FullName
        if ($content -match 'requires_response:\s*true') {
            if ($content -notmatch 'response_owner:\s*\S+') {
                Fail "Mailbox message requires response but has no response_owner: $($_.Name)"
            }
            if ($content -notmatch 'requested_action') {
                Fail "Mailbox message requires response but has no requested_action: $($_.Name)"
            }
        }
    }
}

if ($Warnings.Count -gt 0) {
    Write-Host "WARNINGS:"
    $Warnings | ForEach-Object { Write-Host "- $_" }
}

if ($Errors.Count -gt 0) {
    Write-Host "ERRORS:"
    $Errors | ForEach-Object { Write-Host "- $_" }
    exit 1
}

Write-Host "OK: collaboration state is valid."

