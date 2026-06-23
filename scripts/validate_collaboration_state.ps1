param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$ConfigPath = ""
)

$ErrorActionPreference = "Stop"

$script:ImplementableTaskTypes = @("implementation", "refactor", "integration", "migration", "security", "release")
$script:LightweightTaskTypes = @("discovery", "analysis", "review", "documentation", "triage")
$script:ImplementableSddStatuses = @("ready", "claimed", "in_progress", "in_review", "changes_requested", "review_approved", "qa_pending", "qa_failed", "architect_review", "done")
$script:ReviewedTaskStatuses = @("in_review", "review_approved", "qa_pending", "architect_review", "done")
$script:FullSddFields = @("spec_id", "execution_pipeline", "acceptance_criteria", "linked_decisions", "test_plan", "closure_criteria")
$script:LightweightSddFields = @("objective", "expected_output", "question_to_resolve", "closure_criterion")
$script:RowScopedLedgerSelectors = @{
    "Area_comun/state/CLAIMS.json" = "^CLAIM-[A-Za-z0-9._-]+$"
    "Area_comun/state/TASK_INDEX.json" = "^(TASK-\d{4}|REQ-[0-9A-Fa-f]+)$"
    "Area_comun/state/PROJECT_STATE.json" = "^(active_tasks/(TASK-\d{4}|REQ-[0-9A-Fa-f]+)|[A-Za-z_][A-Za-z0-9_]*)$"
}
$script:ValidAdoptionTiers = @("coordination", "runtime")
$script:RuntimeTierRequiredPaths = @(
    "runtime",
    "runtime/turn_schema.json",
    "scripts/validate_collaboration_state.py",
    "scripts/validate_collaboration_state.ps1",
    "scripts/scan_encoding.py",
    "scripts/scan_encoding.ps1",
    "scripts/scan_domain_neutrality.py",
    "scripts/scan_domain_neutrality.ps1",
    "scripts/measure_context_cost.py",
    "scripts/prune_state.py",
    "scripts/prune_state.ps1",
    ".github/workflows/validate.yml"
)

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

function Merge-ByArrayField {
    param(
        [object]$Hot,
        [object]$Archive,
        [string]$Field,
        [string]$IdField,
        [string]$Label
    )
    if (-not $Hot) { return $Hot }
    $entries = [System.Collections.Generic.List[object]]::new()
    $seen = @{}
    foreach ($source in @(
        @{ Name = "hot"; Data = $Hot },
        @{ Name = "archive"; Data = $Archive }
    )) {
        if (-not $source.Data -or -not $source.Data.$Field) { continue }
        foreach ($entry in @($source.Data.$Field)) {
            if ($entry.PSObject.Properties.Name -contains $IdField) {
                $entryId = [string]$entry.$IdField
                if ($entryId) {
                    if ($seen.ContainsKey($entryId)) {
                        Fail "Duplicate $Label across hot/archive: $entryId"
                    }
                    $seen[$entryId] = $true
                }
            }
            $entries.Add($entry) | Out-Null
        }
    }
    $Hot.$Field = @($entries)
    return $Hot
}

function Normalize-ScopePath {
    param([string]$Scope)
    return $Scope.Replace("\", "/").Trim()
}

function Split-Scope {
    param([string]$Scope)
    $normalized = Normalize-ScopePath $Scope
    $index = $normalized.IndexOf("#")
    if ($index -lt 0) {
        return [pscustomobject]@{ Path = $normalized; Selector = $null }
    }
    return [pscustomobject]@{
        Path = $normalized.Substring(0, $index)
        Selector = $normalized.Substring($index + 1)
    }
}

function Test-ClaimScopeSelector {
    param([string]$Scope, [string]$ClaimId)
    $parts = Split-Scope $Scope
    if ($null -eq $parts.Selector) { return }
    if (-not $parts.Path -or -not $parts.Selector) {
        Fail "Claim $ClaimId has malformed scoped path: $Scope"
        return
    }
    if (-not $script:RowScopedLedgerSelectors.ContainsKey($parts.Path)) {
        Fail "Claim $ClaimId uses row selector on unsupported path: $Scope"
        return
    }
    if ($parts.Selector -notmatch $script:RowScopedLedgerSelectors[$parts.Path]) {
        Fail "Claim $ClaimId has invalid row selector: $Scope"
    }
}

function Get-MailboxClaimScopeError {
    param([string]$Scope)
    $parts = Split-Scope $Scope
    $mailboxRoot = "Area_comun/mailbox"
    $normalized = $parts.Path.TrimEnd("/")
    if ($normalized -ne $mailboxRoot -and -not $normalized.StartsWith("$mailboxRoot/")) {
        return $null
    }
    $filename = ($normalized -split "/")[-1]
    if ($filename.StartsWith("MSG-") -and $filename.EndsWith(".md")) {
        return $null
    }
    return "mailbox claim must be file-scoped: $Scope"
}

function Test-ScopeEntriesOverlap {
    param([string]$LeftScope, [string]$RightScope)
    $left = Split-Scope $LeftScope
    $right = Split-Scope $RightScope
    if ($left.Path -ne $right.Path) { return $false }
    if ($script:RowScopedLedgerSelectors.ContainsKey($left.Path)) {
        return ($null -eq $left.Selector) -or ($null -eq $right.Selector) -or ($left.Selector -eq $right.Selector)
    }
    return $left.Selector -eq $right.Selector
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

function ConvertFrom-FrontmatterValue {
    param([string]$Value)
    $text = $Value.Trim()
    if (-not $text) { return "" }
    if ($text -eq "true") { return $true }
    if ($text -eq "false") { return $false }
    if ($text.StartsWith("[") -and $text.EndsWith("]")) {
        $inner = $text.Substring(1, $text.Length - 2).Trim()
        if (-not $inner) { return @() }
        return @($inner.Split(",") | ForEach-Object { $_.Trim().Trim("`"'") })
    }
    return $text.Trim("`"'")
}

function ConvertFrom-TaskMarkdown {
    param([string]$Path)
    $metadata = @{
        Frontmatter = @{}
        Sections = @{}
    }
    if (-not (Test-Path -LiteralPath $Path)) {
        return $metadata
    }

    $lines = @(Get-Content -LiteralPath $Path)
    $bodyStart = 0
    if ($lines.Count -gt 0 -and $lines[0].Trim() -eq "---") {
        for ($i = 1; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]
            if ($line.Trim() -eq "---") {
                $bodyStart = $i + 1
                break
            }
            if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$') {
                $metadata.Frontmatter[$Matches[1]] = ConvertFrom-FrontmatterValue $Matches[2]
            }
        }
    }

    $currentSection = $null
    $sectionLines = [System.Collections.Generic.List[string]]::new()
    for ($i = $bodyStart; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line -match '^#{2,6}\s+(.+?)\s*$') {
            if ($currentSection) {
                $metadata.Sections[$currentSection] = @($sectionLines)
            }
            $currentSection = $Matches[1].Trim().ToLower() -replace '\s+', '_'
            $sectionLines = [System.Collections.Generic.List[string]]::new()
            continue
        }
        if ($currentSection) {
            $sectionLines.Add($line) | Out-Null
        }
    }
    if ($currentSection) {
        $metadata.Sections[$currentSection] = @($sectionLines)
    }
    return $metadata
}

function Get-TaskField {
    param(
        [object]$Task,
        [hashtable]$ParsedMarkdown,
        [string]$Field
    )
    if ($ParsedMarkdown.Frontmatter.ContainsKey($Field)) {
        return $ParsedMarkdown.Frontmatter[$Field]
    }
    if ($Task.PSObject.Properties.Name -contains $Field) {
        return $Task.$Field
    }
    if ($ParsedMarkdown.Sections.ContainsKey($Field)) {
        return @($ParsedMarkdown.Sections[$Field] | Where-Object { $_.Trim() })
    }
    return $null
}

function Test-SddValue {
    param([object]$Value)
    if ($null -eq $Value) { return $false }
    if ($Value -is [string]) {
        return ($Value.Trim() -and $Value.Trim().ToLower() -ne "none")
    }
    if ($Value -is [array]) {
        foreach ($item in $Value) {
            if (Test-SddValue $item) { return $true }
        }
        return $false
    }
    return $true
}

function Test-Truthy {
    param([object]$Value)
    if ($Value -is [bool]) { return $Value }
    if ($Value -is [string]) { return $Value.Trim().ToLower() -eq "true" }
    return [bool]$Value
}

function Test-PreSddTask {
    param(
        [object]$Task,
        [hashtable]$ParsedMarkdown,
        [string]$AdoptedAt
    )
    if (Test-Truthy (Get-TaskField -Task $Task -ParsedMarkdown $ParsedMarkdown -Field "sdd_exempt")) {
        return $true
    }
    $taskType = Get-TaskField -Task $Task -ParsedMarkdown $ParsedMarkdown -Field "type"
    if (-not (Test-SddValue $taskType)) {
        return $true
    }
    $createdAt = Get-TaskField -Task $Task -ParsedMarkdown $ParsedMarkdown -Field "created_at"
    if ($createdAt -is [string] -and $createdAt -match '^\d{4}-\d{2}-\d{2}$' -and $createdAt -lt $AdoptedAt) {
        return $true
    }
    return $false
}

function Test-SpecIdExists {
    param(
        [string]$Root,
        [object]$SpecId
    )
    if (-not ($SpecId -is [string]) -or -not $SpecId.Trim()) {
        return $false
    }
    $specText = $SpecId.Trim()
    $candidates = [System.Collections.Generic.List[string]]::new()
    $candidates.Add((Join-Path $Root $specText)) | Out-Null
    if ($specText -notmatch '[\\/]') {
        $candidates.Add((Join-Path $Root "Area_comun/specs/$specText")) | Out-Null
        if (-not $specText.EndsWith(".md")) {
            $candidates.Add((Join-Path $Root "Area_comun/specs/$specText.md")) | Out-Null
        }
    }
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $true
        }
    }
    return $false
}

function Test-MarkdownField {
    param(
        [string]$Content,
        [string]$Field
    )
    return ($Content -match "(?m)^\s*$([regex]::Escape($Field))\s*:\s*\S+")
}

function Test-CompactMailboxMessage {
    param([string]$Content)
    foreach ($field in @("one_line_summary", "question", "context_refs", "changed_refs", "validation_refs", "deadline_or_blocking_level")) {
        if (Test-MarkdownField -Content $Content -Field $field) {
            return $true
        }
    }
    return $false
}

function Get-MarkdownField {
    param(
        [string]$Content,
        [string]$Field
    )
    $pattern = "(?m)^\s*$([regex]::Escape($Field))\s*:\s*(.*?)\s*$"
    $match = [regex]::Match($Content, $pattern)
    if (-not $match.Success) {
        return $null
    }
    return $match.Groups[1].Value.Trim().Trim("`"'")
}

function Test-ReferencesExistingWork {
    param([string]$Content)
    foreach ($pattern in @("\bTASK-\d{4}\b", "\bDECISION-\d{4}\b", "\bSPEC-\d{4}\b", "Area_comun/", "scripts/", "examples/", "README")) {
        if ($Content -match $pattern) {
            return $true
        }
    }
    return $false
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

function Validate-AdoptionTier {
    param(
        [string]$Root,
        [object]$Config
    )
    if (-not $Config) {
        return
    }
    $tier = "coordination"
    if (($Config.PSObject.Properties.Name -contains "adoption_tier") -and $null -ne $Config.adoption_tier) {
        $tier = [string]$Config.adoption_tier
    }
    if ($script:ValidAdoptionTiers -notcontains $tier) {
        Fail "Unsupported adoption_tier: $tier"
        return
    }
    if ($tier -ne "runtime") {
        return
    }
    foreach ($relative in $script:RuntimeTierRequiredPaths) {
        $requiredPath = Join-Path $Root $relative
        if (-not (Test-Path -LiteralPath $requiredPath)) {
            Fail "Runtime adoption tier missing required path: $relative"
        }
    }
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

function Validate-Sdd {
    param(
        [string]$Root,
        [object]$Index,
        [object]$Config
    )
    if (-not $Index -or -not $Config) {
        return
    }
    if (-not ($Config.PSObject.Properties.Name -contains "sdd") -or -not $Config.sdd.enabled) {
        return
    }

    $enforcement = $Config.sdd.enforcement
    if (-not $enforcement) {
        $enforcement = "new_implementable_tasks"
    }
    if ($enforcement -ne "new_implementable_tasks") {
        Fail "Unsupported sdd.enforcement: $enforcement"
        return
    }

    $adoptedAt = $Config.sdd.adopted_at
    if (-not $adoptedAt) {
        $adoptedAt = "2026-06-05"
    }
    if (-not ($adoptedAt -is [string]) -or $adoptedAt -notmatch '^\d{4}-\d{2}-\d{2}$') {
        Fail "Invalid sdd.adopted_at: $adoptedAt"
        return
    }

    foreach ($task in @($Index.tasks)) {
        $taskFile = $task.file
        if (-not $taskFile) {
            $taskFile = $task.task_file
        }
        if (-not $taskFile) {
            continue
        }

        $taskPath = Join-Path $Root $taskFile
        $parsed = ConvertFrom-TaskMarkdown $taskPath
        if (Test-PreSddTask -Task $task -ParsedMarkdown $parsed -AdoptedAt $adoptedAt) {
            continue
        }

        $taskType = [string](Get-TaskField -Task $task -ParsedMarkdown $parsed -Field "type")
        $taskType = $taskType.Trim()
        $taskStatus = [string]$task.status
        $taskStatus = $taskStatus.Trim()

        if ($script:ImplementableTaskTypes -contains $taskType) {
            if ($script:ImplementableSddStatuses -notcontains $taskStatus) {
                continue
            }
            foreach ($field in $script:FullSddFields) {
                if (-not (Test-SddValue (Get-TaskField -Task $task -ParsedMarkdown $parsed -Field $field))) {
                    Fail "Task $($task.id) missing SDD field: $field"
                }
            }
            $specId = Get-TaskField -Task $task -ParsedMarkdown $parsed -Field "spec_id"
            if ((Test-SddValue $specId) -and -not (Test-SpecIdExists -Root $Root -SpecId $specId)) {
                Fail "Task $($task.id) spec_id not found: $specId"
            }
        } elseif ($script:LightweightTaskTypes -contains $taskType) {
            if ($taskStatus -eq "proposed") {
                continue
            }
            foreach ($field in $script:LightweightSddFields) {
                if (-not (Test-SddValue (Get-TaskField -Task $task -ParsedMarkdown $parsed -Field $field))) {
                    Warn "Task $($task.id) missing lightweight SDD field: $field"
                }
            }
        } else {
            Warn "Task $($task.id) has unrecognized type: $taskType"
        }
    }
}

function Test-RuntimeStateHasContent {
    param([string]$Root)
    $runtimeState = Join-Path $Root "runtime/state"
    if (-not (Test-Path -LiteralPath $runtimeState)) {
        return $false
    }
    $firstFile = Get-ChildItem -LiteralPath $runtimeState -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1
    return $null -ne $firstFile
}

function Validate-EventLogSnapshot {
    param([string]$Root)
    if (-not (Test-RuntimeStateHasContent -Root $Root)) {
        return
    }

    $toolsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    $oldToolsRoot = $env:EVENTLOG_TOOLS_ROOT
    $oldInstanceRoot = $env:EVENTLOG_INSTANCE_ROOT
    $env:EVENTLOG_TOOLS_ROOT = $toolsRoot
    $env:EVENTLOG_INSTANCE_ROOT = $Root
    $pythonSnippet = @'
import os
import sys
from pathlib import Path

sys.path.insert(0, os.environ["EVENTLOG_TOOLS_ROOT"])
from runtime.eventlog import assert_snapshot_matches

assert_snapshot_matches(Path(os.environ["EVENTLOG_INSTANCE_ROOT"]))
'@
    try {
        $output = $pythonSnippet | python - 2>&1
        if ($LASTEXITCODE -ne 0) {
            Fail "Runtime event log snapshot mismatch: $($output -join ' ')"
        }
    } catch {
        Fail "Runtime event log snapshot mismatch: $($_.Exception.Message)"
    } finally {
        $env:EVENTLOG_TOOLS_ROOT = $oldToolsRoot
        $env:EVENTLOG_INSTANCE_ROOT = $oldInstanceRoot
    }
}

function Test-EventStateEnabled {
    param([object]$Config)
    if (-not $Config) { return $false }
    if (-not ($Config.PSObject.Properties.Name -contains "event_state")) { return $false }
    $eventState = $Config.event_state
    if (-not $eventState) { return $false }
    if (-not ($eventState.PSObject.Properties.Name -contains "enabled")) { return $false }
    return [bool]$eventState.enabled
}

function Test-ConfigBool {
    param([object]$Object, [string]$Name)
    if (-not $Object) { return $false }
    if (-not ($Object.PSObject.Properties.Name -contains $Name)) { return $false }
    return [bool]$Object.$Name
}

function Get-EventStateConfigError {
    param([object]$Config)
    if (-not $Config) { return $null }
    $tier = "coordination"
    if (($Config.PSObject.Properties.Name -contains "adoption_tier") -and $null -ne $Config.adoption_tier) {
        $tier = [string]$Config.adoption_tier
    }
    if ($tier -ne "runtime") { return $null }
    if (-not ($Config.PSObject.Properties.Name -contains "event_state")) { return $null }
    $eventState = $Config.event_state
    if (-not $eventState) { return $null }

    $enabled = Test-ConfigBool -Object $eventState -Name "enabled"
    $materialize = Test-ConfigBool -Object $eventState -Name "materialize"
    $enforce = Test-ConfigBool -Object $eventState -Name "enforce"
    $authoritative = Test-ConfigBool -Object $eventState -Name "authoritative"
    if ($authoritative -and -not $enforce) {
        return "event_state.authoritative=true requires event_state.enforce=true for adoption_tier=runtime; set event_state.enforce=true or event_state.authoritative=false."
    }
    if ($enforce -and -not $materialize) {
        return "event_state.enforce=true requires event_state.materialize=true for adoption_tier=runtime; set event_state.materialize=true or event_state.enforce=false."
    }
    if ($materialize -and -not $enabled) {
        return "event_state.materialize=true requires event_state.enabled=true for adoption_tier=runtime; set event_state.enabled=true or event_state.materialize=false."
    }
    return $null
}

function Validate-ProtocolStateDrift {
    param(
        [string]$Root,
        [object]$Config
    )
    if (-not (Test-EventStateEnabled -Config $Config)) {
        return
    }
    if (-not (Test-RuntimeStateHasContent -Root $Root)) {
        return
    }

    $toolsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    $oldToolsRoot = $env:EVENTLOG_TOOLS_ROOT
    $oldInstanceRoot = $env:EVENTLOG_INSTANCE_ROOT
    $env:EVENTLOG_TOOLS_ROOT = $toolsRoot
    $env:EVENTLOG_INSTANCE_ROOT = $Root
    $pythonSnippet = @'
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.environ["EVENTLOG_TOOLS_ROOT"])
from runtime.protocol_replay import protocol_state_drift

print(json.dumps(protocol_state_drift(Path(os.environ["EVENTLOG_INSTANCE_ROOT"])), sort_keys=True))
'@
    try {
        $output = $pythonSnippet | python - 2>&1
        if ($LASTEXITCODE -ne 0) {
            Fail "Runtime protocol state drift check failed: $($output -join ' ')"
            return
        }
        $drift = ($output -join "`n") | ConvertFrom-Json
        if ($drift.has_drift) {
            $paths = @($drift.entries | ForEach-Object { $_.path }) -join ", "
            if ($drift.enforced) {
                Fail "Runtime protocol state drift detected under event_state.enforce (hard-fail B.3): $paths. Reconcile by re-materializing from replay(log) or writing a fresh genesis."
            } else {
                Warn "Runtime protocol state drift detected (warning-only B.1): $paths"
            }
        }
    } catch {
        Fail "Runtime protocol state drift check failed: $($_.Exception.Message)"
    } finally {
        $env:EVENTLOG_TOOLS_ROOT = $oldToolsRoot
        $env:EVENTLOG_INSTANCE_ROOT = $oldInstanceRoot
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

$stateDir = Join-Path $resolvedRoot "Area_comun/state"
$statePath = Join-Path $stateDir "PROJECT_STATE.json"
$indexPath = Join-Path $stateDir "TASK_INDEX.json"
$claimsPath = Join-Path $stateDir "CLAIMS.json"
$indexArchivePath = Join-Path $stateDir "TASK_INDEX_ARCHIVE.json"
$claimsArchivePath = Join-Path $stateDir "CLAIMS_ARCHIVE.json"

$state = Read-JsonFile $statePath
$indexHot = Read-JsonFile $indexPath
$claimsHot = Read-JsonFile $claimsPath
$indexArchive = $null
$claimsArchive = $null
if (Test-Path -LiteralPath $indexArchivePath) { $indexArchive = Read-JsonFile $indexArchivePath }
if (Test-Path -LiteralPath $claimsArchivePath) { $claimsArchive = Read-JsonFile $claimsArchivePath }
$index = Merge-ByArrayField -Hot $indexHot -Archive $indexArchive -Field "tasks" -IdField "id" -Label "task"
$claims = Merge-ByArrayField -Hot $claimsHot -Archive $claimsArchive -Field "claims" -IdField "claim_id" -Label "claim"

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

Validate-AdoptionTier -Root $resolvedRoot -Config $config
$eventStateConfigError = Get-EventStateConfigError -Config $config
if ($eventStateConfigError) {
    Fail "Event state config invalid: $eventStateConfigError"
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

        if ($script:ReviewedTaskStatuses -contains $task.status) {
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

Validate-Sdd -Root $resolvedRoot -Index $index -Config $config

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
        foreach ($scope in @($claim.scope)) {
            if ($scope) {
                Test-ClaimScopeSelector -Scope ([string]$scope) -ClaimId ([string]$claim.claim_id)
                if ($claim.status -eq "active") {
                    $mailboxError = Get-MailboxClaimScopeError -Scope ([string]$scope)
                    if ($mailboxError) {
                        Fail "Claim $($claim.claim_id) $mailboxError"
                    }
                }
            }
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
                    $leftParts = Split-Scope ([string]$leftScope)
                    $rightParts = Split-Scope ([string]$rightScope)
                    if ($leftParts.Path -like "Area_comun/mailbox/*" -or $rightParts.Path -like "Area_comun/mailbox/*") { continue }
                    if (Test-ScopeEntriesOverlap -LeftScope ([string]$leftScope) -RightScope ([string]$rightScope)) {
                        Fail "Overlapping active claims: $($left.claim_id) and $($right.claim_id) both scope '$leftScope' / '$rightScope'"
                    }
                }
            }
        }
    }
}

if ($index -and $index.tasks -and $claims -and $claims.claims) {
    $reviewedTasks = @{}
    foreach ($task in @($index.tasks)) {
        if ($script:ReviewedTaskStatuses -contains $task.status) {
            $reviewedTasks[[string]$task.id] = $task
        }
    }
    foreach ($claim in @($claims.claims)) {
        if ($claim.status -ne "active") { continue }
        $taskId = [string]$claim.task_id
        if (-not $reviewedTasks.ContainsKey($taskId)) { continue }
        $task = $reviewedTasks[$taskId]
        if ($claim.owner -eq $task.owner) {
            Fail "Handoff-release violation: task $taskId is $($task.status) but owner $($claim.owner) still has active claim $($claim.claim_id)"
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

Validate-EventLogSnapshot -Root $resolvedRoot
Validate-ProtocolStateDrift -Root $resolvedRoot -Config $config

$mailboxRoot = Join-Path $resolvedRoot "Area_comun/mailbox"
foreach ($mailboxState in @("open", "answered", "archived")) {
    $mailboxStatePath = Join-Path $mailboxRoot $mailboxState
    if (-not (Test-Path -LiteralPath $mailboxStatePath)) {
        continue
    }
    Get-ChildItem -LiteralPath $mailboxStatePath -Filter "MSG-*.md" | ForEach-Object {
        $content = Get-Content -Raw -LiteralPath $_.FullName
        $messageStatus = (Get-MarkdownField -Content $content -Field "status")
        if ($messageStatus) { $messageStatus = $messageStatus.ToLower() } else { $messageStatus = "" }
        $rootPrefix = $resolvedRoot.TrimEnd("\", "/") + [System.IO.Path]::DirectorySeparatorChar
        $relativePath = $_.FullName
        if ($relativePath.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            $relativePath = $relativePath.Substring($rootPrefix.Length)
        }
        $relativePath = $relativePath.Replace("\", "/")
        if ($messageStatus -ne $mailboxState) {
            if (-not $messageStatus) { $messageStatus = "<missing>" }
            Fail "Mailbox status/folder mismatch: $relativePath has status '$messageStatus', expected '$mailboxState'"
        }

        if ($mailboxState -eq "open") {
            $messageType = (Get-MarkdownField -Content $content -Field "type")
            if ($messageType) { $messageType = $messageType.ToUpper() }
            $requiresResponse = Get-MarkdownField -Content $content -Field "requires_response"

            if (($messageType -in @("ACK", "FYI")) -and $requiresResponse -and $requiresResponse.ToLower() -eq "false") {
                Warn "Mailbox message does not require response; consider archiving: $($_.Name)"
            }
            if ($content -match 'requires_response:\s*true') {
                if ($content -notmatch 'response_owner:\s*\S+') {
                    Fail "Mailbox message requires response but has no response_owner: $($_.Name)"
                }
                if ($content -notmatch 'requested_action') {
                    Fail "Mailbox message requires response but has no requested_action: $($_.Name)"
                }
                if ((Test-CompactMailboxMessage -Content $content) -and -not (Test-MarkdownField -Content $content -Field "question")) {
                    Fail "Compact mailbox message requires response but has no question: $($_.Name)"
                }
            }
            if ((Test-CompactMailboxMessage -Content $content) -and (Test-ReferencesExistingWork -Content $content) -and -not (Test-MarkdownField -Content $content -Field "context_refs")) {
                Warn "Compact mailbox message references existing work but has no context_refs: $($_.Name)"
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
