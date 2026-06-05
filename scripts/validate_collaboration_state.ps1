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

function Test-SemVer {
    param([object]$Version)
    return ($Version -is [string] -and $Version -match '^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$')
}

function ConvertTo-SemVer {
    param([string]$Version)
    if (-not (Test-SemVer $Version)) {
        return $null
    }
    return [version]$Version
}

function Test-VersionComparator {
    param(
        [version]$ProtocolVersion,
        [string]$Operator,
        [version]$RequiredVersion
    )
    $comparison = $ProtocolVersion.CompareTo($RequiredVersion)
    switch ($Operator) {
        "==" { return $comparison -eq 0 }
        ">=" { return $comparison -ge 0 }
        ">"  { return $comparison -gt 0 }
        "<=" { return $comparison -le 0 }
        "<"  { return $comparison -lt 0 }
        default { return $false }
    }
}

function Test-ProtocolVersionSatisfies {
    param(
        [object]$ProtocolVersion,
        [object]$Requirement
    )
    $parsedProtocol = $null
    if ($ProtocolVersion -is [string]) {
        $parsedProtocol = ConvertTo-SemVer $ProtocolVersion
    }
    if ($null -eq $parsedProtocol -or -not ($Requirement -is [string]) -or -not $Requirement.Trim()) {
        return @{ Satisfies = $false; Parseable = $false }
    }

    $requirementText = $Requirement.Trim()
    if (Test-SemVer $requirementText) {
        $parsedRequired = ConvertTo-SemVer $requirementText
        return @{
            Satisfies = ($parsedProtocol.CompareTo($parsedRequired) -eq 0)
            Parseable = $true
        }
    }

    foreach ($token in $requirementText.Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)) {
        if ($token -notmatch '^(>=|<=|>|<|==)(\d+\.\d+\.\d+)$') {
            return @{ Satisfies = $false; Parseable = $false }
        }
        $operator = $Matches[1]
        $requiredVersion = ConvertTo-SemVer $Matches[2]
        if ($null -eq $requiredVersion -or -not (Test-VersionComparator -ProtocolVersion $parsedProtocol -Operator $operator -RequiredVersion $requiredVersion)) {
            return @{ Satisfies = $false; Parseable = $true }
        }
    }

    return @{ Satisfies = $true; Parseable = $true }
}

function Validate-AdoptedProfiles {
    param(
        [string]$Root,
        [object]$State,
        [object]$Config
    )
    if (-not $State -or -not ($State.PSObject.Properties.Name -contains "adopted_profiles")) {
        return
    }

    $adoptedProfilesValue = $State.adopted_profiles
    if ($null -eq $adoptedProfilesValue) {
        return
    }
    $adoptedProfiles = @($adoptedProfilesValue)
    if ($adoptedProfiles.Count -eq 0) {
        return
    }
    if ($adoptedProfilesValue -isnot [array]) {
        # ConvertFrom-Json can collapse one-item arrays in older PowerShell hosts; allow objects here.
        if ($adoptedProfilesValue -isnot [pscustomobject]) {
            Fail "adopted_profiles must be an array"
            return
        }
    }

    $profileIds = @{}
    $adoptedById = @{}
    for ($i = 0; $i -lt $adoptedProfiles.Count; $i++) {
        $profile = $adoptedProfiles[$i]
        $label = "adopted_profiles[$i]"
        if ($profile -isnot [pscustomobject]) {
            Fail "$label must be an object"
            continue
        }

        $profileId = $profile.profile_id
        $profileVersion = $profile.profile_version
        $adoptedAt = $profile.adopted_at

        if (-not ($profileId -is [string]) -or -not $profileId) {
            Fail "$label missing profile_id"
        } elseif ($profileId -notmatch '^[a-z0-9][a-z0-9_-]*$') {
            Fail "$label profile_id has invalid format: $profileId"
        } elseif ($profileIds.ContainsKey($profileId)) {
            Fail "Duplicate adopted profile: $profileId"
        } else {
            $profileIds[$profileId] = $true
            $adoptedById[$profileId] = $profile
        }

        if (-not (Test-SemVer $profileVersion)) {
            Fail "$label profile_version must be SemVer MAJOR.MINOR.PATCH"
        }
        if (-not ($adoptedAt -is [string]) -or $adoptedAt -notmatch '^\d{4}-\d{2}-\d{2}$') {
            Fail "$label adopted_at must be YYYY-MM-DD"
        }

        $decisionRef = $profile.decision_ref
        if ($decisionRef -is [string] -and $decisionRef) {
            $decisionPath = Join-Path $Root $decisionRef
            if (-not (Test-Path -LiteralPath $decisionPath)) {
                Warn "$label decision_ref not found: $decisionRef"
            }
        }
    }

    foreach ($profileId in $adoptedById.Keys) {
        $profile = $adoptedById[$profileId]
        $manifestPath = Join-Path $Root "profiles/$profileId/profile.manifest.json"
        if (-not (Test-Path -LiteralPath $manifestPath)) {
            Warn "Adopted profile '$profileId' is not locally verifiable: missing profiles/$profileId/profile.manifest.json"
            continue
        }

        $manifest = Read-JsonFile $manifestPath
        if (-not $manifest) {
            continue
        }

        if ($manifest.profile_id -ne $profileId) {
            Fail "Adopted profile '$profileId' manifest profile_id mismatch: '$($manifest.profile_id)'"
        }
        if ($manifest.profile_version -ne $profile.profile_version) {
            Fail "Adopted profile '$profileId' version mismatch: state='$($profile.profile_version)' manifest='$($manifest.profile_version)'"
        }

        $protocolVersion = $null
        if ($Config) {
            $protocolVersion = $Config.protocol_version
        }
        $compatibility = Test-ProtocolVersionSatisfies -ProtocolVersion $protocolVersion -Requirement $manifest.requires_protocol_version
        if (-not $compatibility.Parseable) {
            Warn "Adopted profile '$profileId' has unsupported requires_protocol_version: $($manifest.requires_protocol_version)"
        } elseif (-not $compatibility.Satisfies) {
            Fail "Adopted profile '$profileId' requires protocol version '$($manifest.requires_protocol_version)', found '$protocolVersion'"
        }

        foreach ($dependency in @($manifest.depends_on_profiles)) {
            if ($dependency -and -not $adoptedById.ContainsKey($dependency)) {
                Fail "Adopted profile '$profileId' depends on missing profile '$dependency'"
            }
        }
    }
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

Validate-AdoptedProfiles -Root $resolvedRoot -State $state -Config $config

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
