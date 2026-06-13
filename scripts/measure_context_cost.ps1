param(
    [string]$Root = ".",
    [switch]$Json,
    [switch]$Baseline,
    [switch]$Budget
)

$ErrorActionPreference = "Stop"

$DefaultColdstartGlobs = @(
    "AGENTS.md",
    "Area_comun/README.md",
    "Area_comun/protocol/TASK_PROTOCOL.md",
    "Area_comun/state/PROJECT_STATE.json",
    "Area_comun/state/TASK_INDEX.json",
    "Area_comun/state/CLAIMS.json"
)
$DefaultSlimColdstartGlobs = @(
    "AGENTS.md",
    "Area_comun/README.md",
    "Area_comun/protocol/TASK_PROTOCOL.md",
    "Area_comun/state/PROJECT_STATE.slim.json",
    "Area_comun/state/TASK_INDEX.slim.json",
    "Area_comun/state/CLAIMS.slim.json"
)
$SlimViewFiles = @(
    "Area_comun/state/PROJECT_STATE.slim.json",
    "Area_comun/state/TASK_INDEX.slim.json",
    "Area_comun/state/CLAIMS.slim.json"
)
$HotTaskStatuses = @(
    "proposed",
    "ready",
    "claimed",
    "in_progress",
    "in_review",
    "changes_requested",
    "qa_pending",
    "qa_failed",
    "architect_review",
    "blocked"
)

function Read-Text {
    param([string]$Path)
    return Get-Content -Raw -Encoding UTF8 -Path $Path
}

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return $null
    }
    return (Get-Content -Raw -Encoding UTF8 -Path $Path | ConvertFrom-Json)
}

function Get-TokenCount {
    param(
        [int]$CharCount,
        [int]$Divisor
    )
    if ($Divisor -le 0) {
        $Divisor = 4
    }
    return [math]::Floor($CharCount / $Divisor)
}

function Get-RelativePath {
    param(
        [string]$RootPath,
        [string]$FullPath
    )
    $rootUri = [System.Uri]((Resolve-Path $RootPath).Path.TrimEnd("\", "/") + [System.IO.Path]::DirectorySeparatorChar)
    $fileUri = [System.Uri](Resolve-Path $FullPath).Path
    return $rootUri.MakeRelativeUri($fileUri).ToString()
}

function Get-UniqueFiles {
    param(
        [string]$RootPath,
        [array]$Patterns
    )
    $files = @{}
    foreach ($pattern in $Patterns) {
        Get-ChildItem -Path (Join-Path $RootPath $pattern) -File -ErrorAction SilentlyContinue | ForEach-Object {
            $relative = Get-RelativePath -RootPath $RootPath -FullPath $_.FullName
            $files[$relative] = $_.FullName
        }
    }
    return $files.GetEnumerator() | Sort-Object Name | ForEach-Object { $_.Value }
}

function New-FileEntry {
    param(
        [string]$RootPath,
        [string]$Path,
        [int]$Divisor
    )
    $text = Read-Text -Path $Path
    $chars = $text.Length
    return [pscustomobject][ordered]@{
        path = Get-RelativePath -RootPath $RootPath -FullPath $Path
        chars = $chars
        tokens = (Get-TokenCount -CharCount $chars -Divisor $Divisor)
    }
}

function New-VirtualFileEntry {
    param(
        [string]$Path,
        [string]$Text,
        [int]$Divisor
    )
    $chars = $Text.Length
    return [pscustomobject][ordered]@{
        path = $Path
        chars = $chars
        tokens = (Get-TokenCount -CharCount $chars -Divisor $Divisor)
        virtual = $true
    }
}

function ConvertTo-MeasureJson {
    param($Value)
    return (($Value | ConvertTo-Json -Depth 30) + "`n")
}

function Get-RecentLimit {
    param(
        $Config,
        [string]$Field
    )
    if ($Config -and $Config.maintenance) {
        $specific = "recent_$Field"
        if ($Config.maintenance.PSObject.Properties.Name -contains $specific) {
            return [int]$Config.maintenance.$specific
        }
        if ($Config.maintenance.recent_next_actions) {
            return [int]$Config.maintenance.recent_next_actions
        }
    }
    return 8
}

function Get-TailStrings {
    param(
        $Values,
        [int]$Limit
    )
    if ($null -eq $Values -or $Limit -le 0) {
        return @()
    }
    $items = @($Values | ForEach-Object { [string]$_ })
    if ($items.Count -le $Limit) {
        return $items
    }
    return $items[($items.Count - $Limit)..($items.Count - 1)]
}

function Get-GeneratedSlimEntries {
    param(
        [string]$RootPath,
        $Config,
        [int]$Divisor
    )
    $taskDoc = Read-JsonFile -Path (Join-Path $RootPath "Area_comun/state/TASK_INDEX.json")
    $projectDoc = Read-JsonFile -Path (Join-Path $RootPath "Area_comun/state/PROJECT_STATE.json")
    $claimsDoc = Read-JsonFile -Path (Join-Path $RootPath "Area_comun/state/CLAIMS.json")
    $tasks = @()
    if ($taskDoc -and $taskDoc.tasks) {
        $tasks = @($taskDoc.tasks | Where-Object { $HotTaskStatuses -contains ([string]$_.status) } | Sort-Object id | ForEach-Object {
            $item = [ordered]@{}
            foreach ($key in @("id", "status", "owner", "phase", "priority", "title")) {
                if ($null -ne $_.$key) { $item[$key] = $_.$key }
            }
            if ($_.blocked_by_questions -and @($_.blocked_by_questions).Count -gt 0) {
                $item["blocked_by_questions"] = @($_.blocked_by_questions)
            }
            [pscustomobject]$item
        })
    }
    $activeTasks = @()
    if ($projectDoc -and $projectDoc.active_tasks) {
        $activeTasks = @($projectDoc.active_tasks | Where-Object { $HotTaskStatuses -contains ([string]$_.status) } | Sort-Object id | ForEach-Object {
            $item = [ordered]@{}
            foreach ($key in @("id", "status", "owner", "title")) {
                if ($null -ne $_.$key) { $item[$key] = $_.$key }
            }
            [pscustomobject]$item
        })
    }
    $claims = @()
    if ($claimsDoc -and $claimsDoc.claims) {
        $claims = @($claimsDoc.claims | Where-Object { ([string]$_.status) -eq "active" } | Sort-Object claim_id | ForEach-Object {
            [pscustomobject][ordered]@{
                claim_id = $_.claim_id
                task_id = $_.task_id
                owner = $_.owner
                scope = @($_.scope)
            }
        })
    }
    $projectSlim = [pscustomobject][ordered]@{
        view = "project_state.slim"
        status = $projectDoc.status
        active_tasks = $activeTasks
        next_actions = Get-TailStrings -Values $projectDoc.next_actions -Limit (Get-RecentLimit -Config $Config -Field "next_actions")
        risks = Get-TailStrings -Values $projectDoc.risks -Limit (Get-RecentLimit -Config $Config -Field "risks")
        open_questions = Get-TailStrings -Values $projectDoc.open_questions -Limit (Get-RecentLimit -Config $Config -Field "open_questions")
    }
    $taskSlim = [pscustomobject][ordered]@{
        schema_version = "1.0"
        view = "task_index.slim"
        tasks = $tasks
    }
    $claimSlim = [pscustomobject][ordered]@{
        schema_version = "1.0"
        view = "claims.slim"
        claims = $claims
    }
    return @(
        New-VirtualFileEntry -Path "Area_comun/state/CLAIMS.slim.json" -Text (ConvertTo-MeasureJson -Value $claimSlim) -Divisor $Divisor
        New-VirtualFileEntry -Path "Area_comun/state/PROJECT_STATE.slim.json" -Text (ConvertTo-MeasureJson -Value $projectSlim) -Divisor $Divisor
        New-VirtualFileEntry -Path "Area_comun/state/TASK_INDEX.slim.json" -Text (ConvertTo-MeasureJson -Value $taskSlim) -Divisor $Divisor
    )
}

function Measure-ColdStartPatterns {
    param(
        [string]$RootPath,
        [array]$Patterns,
        $Config,
        [int]$Divisor
    )
    $patterns = @($Patterns)
    if ($patterns -notcontains "Area_comun/mailbox/open/*.md") {
        $patterns += "Area_comun/mailbox/open/*.md"
    }
    $files = @(Get-UniqueFiles -RootPath $RootPath -Patterns $patterns | ForEach-Object {
        New-FileEntry -RootPath $RootPath -Path $_ -Divisor $Divisor
    })
    $present = @($files | ForEach-Object { $_.path })
    $missingSlim = @($SlimViewFiles | Where-Object { ($patterns -contains $_) -and ($present -notcontains $_) })
    if ($missingSlim.Count -gt 0) {
        $generated = @(Get-GeneratedSlimEntries -RootPath $RootPath -Config $Config -Divisor $Divisor | Where-Object {
            $missingSlim -contains $_.path
        })
        $files = @($files + $generated | Sort-Object path)
    }
    $totalChars = ($files | Measure-Object -Property chars -Sum).Sum
    $totalTokens = ($files | Measure-Object -Property tokens -Sum).Sum
    if ($null -eq $totalChars) { $totalChars = 0 }
    if ($null -eq $totalTokens) { $totalTokens = 0 }
    return [ordered]@{
        files = $files
        total_chars = [int]$totalChars
        total_tokens = [int]$totalTokens
    }
}

function Get-Percent {
    param(
        [double]$Part,
        [double]$Total
    )
    if ($Total -eq 0) {
        return 0.0
    }
    return [math]::Round(($Part / $Total) * 100, 2)
}

function Measure-ColdStart {
    param(
        [string]$RootPath,
        $Config,
        [int]$Divisor
    )
    $patterns = $DefaultColdstartGlobs
    if ($Config -and $Config.token_cost -and $Config.token_cost.coldstart_globs) {
        $patterns = @($Config.token_cost.coldstart_globs)
    }
    return Measure-ColdStartPatterns -RootPath $RootPath -Patterns $patterns -Config $Config -Divisor $Divisor
}

function Measure-ColdStartModes {
    param(
        [string]$RootPath,
        $Config,
        [int]$Divisor
    )
    $full = Measure-ColdStartPatterns -RootPath $RootPath -Patterns $DefaultColdstartGlobs -Config $Config -Divisor $Divisor
    $slim = Measure-ColdStartPatterns -RootPath $RootPath -Patterns $DefaultSlimColdstartGlobs -Config $Config -Divisor $Divisor
    return [ordered]@{
        full = $full
        slim = $slim
        delta_tokens = [int]($full.total_tokens - $slim.total_tokens)
        delta_chars = [int]($full.total_chars - $slim.total_chars)
        target_tokens = 10000
        slim_within_target = [bool]($slim.total_tokens -lt 10000)
    }
}

function Measure-DeadWeight {
    param([string]$RootPath)
    $claimsDoc = Read-JsonFile -Path (Join-Path $RootPath "Area_comun/state/CLAIMS.json")
    $tasksDoc = Read-JsonFile -Path (Join-Path $RootPath "Area_comun/state/TASK_INDEX.json")
    $claims = @()
    $tasks = @()
    if ($claimsDoc -and $claimsDoc.claims) { $claims = @($claimsDoc.claims) }
    if ($tasksDoc -and $tasksDoc.tasks) { $tasks = @($tasksDoc.tasks) }
    $released = @($claims | Where-Object { ([string]$_.status).ToLowerInvariant() -eq "released" })
    $done = @($tasks | Where-Object { ([string]$_.status).ToLowerInvariant() -eq "done" })
    return [ordered]@{
        claims = [ordered]@{
            total = $claims.Count
            released = $released.Count
            released_percent = (Get-Percent -Part $released.Count -Total $claims.Count)
        }
        tasks = [ordered]@{
            total = $tasks.Count
            done = $done.Count
            done_percent = (Get-Percent -Part $done.Count -Total $tasks.Count)
        }
    }
}

function Split-Frontmatter {
    param([string]$Text)
    $match = [regex]::Match($Text, "(?s)^---\r?\n(?<frontmatter>.*?)\r?\n---\r?\n?(?<body>.*)$")
    if (-not $match.Success) {
        return $null
    }
    return [ordered]@{
        frontmatter = $match.Groups["frontmatter"].Value
        body = $match.Groups["body"].Value
    }
}

function Measure-MailboxOverhead {
    param(
        [string]$RootPath,
        [int]$Divisor
    )
    $frontmatterChars = 0
    $bodyChars = 0
    $entries = New-Object System.Collections.Generic.List[object]
    Get-ChildItem -Path (Join-Path $RootPath "Area_comun/mailbox") -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue |
        Sort-Object FullName |
        ForEach-Object {
            $split = Split-Frontmatter -Text (Read-Text -Path $_.FullName)
            if ($null -eq $split) {
                return
            }
            $fmChars = $split.frontmatter.Length
            $bChars = $split.body.Length
            $frontmatterChars += $fmChars
            $bodyChars += $bChars
            $entries.Add([pscustomobject][ordered]@{
                path = Get-RelativePath -RootPath $RootPath -FullPath $_.FullName
                frontmatter_chars = $fmChars
                body_chars = $bChars
            })
        }
    $totalChars = $frontmatterChars + $bodyChars
    $ratio = 0.0
    if ($bodyChars -gt 0) {
        $ratio = [math]::Round($frontmatterChars / $bodyChars, 4)
    }
    return [ordered]@{
        files = @($entries.ToArray())
        message_count = $entries.Count
        frontmatter_chars = $frontmatterChars
        body_chars = $bodyChars
        frontmatter_tokens = (Get-TokenCount -CharCount $frontmatterChars -Divisor $Divisor)
        body_tokens = (Get-TokenCount -CharCount $bodyChars -Divisor $Divisor)
        frontmatter_to_body_ratio = $ratio
        frontmatter_percent = (Get-Percent -Part $frontmatterChars -Total $totalChars)
    }
}

function Get-RuntimeContextPolicy {
    param($Config)
    $raw = $null
    if ($Config -and $Config.runtime -and $Config.runtime.context_policy) {
        $raw = $Config.runtime.context_policy
    }
    function Get-PolicyInt {
        param($Object, [string]$Name, [int]$Default)
        if ($Object -and ($Object.PSObject.Properties.Name -contains $Name) -and $null -ne $Object.$Name) {
            return [int]$Object.$Name
        }
        return $Default
    }
    return [ordered]@{
        compaction_enabled = [bool]($raw -and $raw.compaction_enabled)
        recent_turn_summaries = Get-PolicyInt -Object $raw -Name "recent_turn_summaries" -Default 3
        task_close_summary_max_tokens = Get-PolicyInt -Object $raw -Name "task_close_summary_max_tokens" -Default 2000
        subagents_enabled = [bool]($raw -and $raw.subagents_enabled)
        subagent_summary_max_tokens = Get-PolicyInt -Object $raw -Name "subagent_summary_max_tokens" -Default 2000
        assembled_context_warn_tokens = if ($raw) { $raw.assembled_context_warn_tokens } else { $null }
        consolidation_tool_call_count = Get-PolicyInt -Object $raw -Name "consolidation_tool_call_count" -Default 10
        consolidation_overhead_budget_pct = Get-PolicyInt -Object $raw -Name "consolidation_overhead_budget_pct" -Default 5
    }
}

function Get-TaskSpecPaths {
    param(
        [string]$RootPath,
        $Task
    )
    $value = [string]$Task.spec_id
    if ([string]::IsNullOrWhiteSpace($value) -or $value.ToLowerInvariant() -eq "none") {
        return @()
    }
    $normalized = $value.Replace("\", "/")
    if ($normalized.EndsWith(".md") -or $normalized.Contains("/")) {
        return @($normalized)
    }
    $specDir = Join-Path $RootPath "Area_comun/specs"
    return @(Get-ChildItem -Path $specDir -File -Filter "$normalized*.md" -ErrorAction SilentlyContinue |
        Sort-Object Name |
        ForEach-Object { Get-RelativePath -RootPath $RootPath -FullPath $_.FullName })
}

function Measure-TaskContextFiles {
    param(
        [string]$RootPath,
        [array]$Paths,
        [int]$Divisor
    )
    $seen = @{}
    $files = @()
    foreach ($relative in @($Paths | Sort-Object)) {
        $text = ([string]$relative).Replace("\", "/")
        if ([string]::IsNullOrWhiteSpace($text) -or $seen.ContainsKey($text)) {
            continue
        }
        $seen[$text] = $true
        $path = Join-Path $RootPath $text
        if (Test-Path $path -PathType Leaf) {
            $files += New-FileEntry -RootPath $RootPath -Path $path -Divisor $Divisor
        }
    }
    $totalChars = ($files | Measure-Object -Property chars -Sum).Sum
    $totalTokens = ($files | Measure-Object -Property tokens -Sum).Sum
    if ($null -eq $totalChars) { $totalChars = 0 }
    if ($null -eq $totalTokens) { $totalTokens = 0 }
    return [ordered]@{
        files = $files
        total_chars = [int]$totalChars
        total_tokens = [int]$totalTokens
    }
}

function Measure-TurnContext {
    param(
        [string]$RootPath,
        $Config,
        [int]$Divisor
    )
    $taskDoc = Read-JsonFile -Path (Join-Path $RootPath "Area_comun/state/TASK_INDEX.json")
    $tasks = @()
    if ($taskDoc -and $taskDoc.tasks) {
        $tasks = @($taskDoc.tasks | Where-Object { @("ready", "claimed", "in_progress", "in_review", "blocked") -contains ([string]$_.status).ToLowerInvariant() })
    }
    $compactSources = $DefaultSlimColdstartGlobs
    if ($Config -and $Config.token_cost -and $Config.token_cost.coldstart_globs) {
        $compactSources = @($Config.token_cost.coldstart_globs)
    }
    $entries = @()
    foreach ($task in $tasks) {
        $specs = @(Get-TaskSpecPaths -RootPath $RootPath -Task $task)
        $compact = Measure-TaskContextFiles -RootPath $RootPath -Paths @($compactSources + $specs) -Divisor $Divisor
        $legacy = Measure-TaskContextFiles -RootPath $RootPath -Paths @($DefaultColdstartGlobs + $specs) -Divisor $Divisor
        $entries += [pscustomobject][ordered]@{
            task_id = $task.id
            status = $task.status
            with_compaction = $compact
            without_compaction = $legacy
            delta_tokens = [int]($legacy.total_tokens - $compact.total_tokens)
            delta_chars = [int]($legacy.total_chars - $compact.total_chars)
        }
    }
    $withTokens = ($entries | ForEach-Object { $_.with_compaction.total_tokens } | Measure-Object -Sum).Sum
    $withoutTokens = ($entries | ForEach-Object { $_.without_compaction.total_tokens } | Measure-Object -Sum).Sum
    $deltaTokens = ($entries | ForEach-Object { $_.delta_tokens } | Measure-Object -Sum).Sum
    if ($null -eq $withTokens) { $withTokens = 0 }
    if ($null -eq $withoutTokens) { $withoutTokens = 0 }
    if ($null -eq $deltaTokens) { $deltaTokens = 0 }
    return [ordered]@{
        context_policy = Get-RuntimeContextPolicy -Config $Config
        tasks = $entries
        total_with_compaction_tokens = [int]$withTokens
        total_without_compaction_tokens = [int]$withoutTokens
        total_delta_tokens = [int]$deltaTokens
    }
}

function Measure-ContextCost {
    param([string]$RootPath)
    $config = Read-JsonFile -Path (Join-Path $RootPath "protocol.config.json")
    $divisor = 4
    $budgetValue = $null
    if ($config -and $config.token_cost) {
        if ($config.token_cost.chars_per_token) {
            $divisor = [int]$config.token_cost.chars_per_token
        }
        if ($null -ne $config.token_cost.budget) {
            $budgetValue = [int]$config.token_cost.budget
        }
    }
    $coldStart = Measure-ColdStart -RootPath $RootPath -Config $config -Divisor $divisor
    return [ordered]@{
        root = $RootPath
        chars_per_token = $divisor
        cold_start = $coldStart
        cold_start_modes = Measure-ColdStartModes -RootPath $RootPath -Config $config -Divisor $divisor
        dead_weight = Measure-DeadWeight -RootPath $RootPath
        mailbox_overhead = Measure-MailboxOverhead -RootPath $RootPath -Divisor $divisor
        turn_context = Measure-TurnContext -RootPath $RootPath -Config $config -Divisor $divisor
        budget = [ordered]@{
            cold_start_tokens = $budgetValue
            exceeded = [bool]($null -ne $budgetValue -and $coldStart.total_tokens -gt $budgetValue)
        }
    }
}

function Write-HumanReport {
    param(
        $Result,
        [bool]$ShowBudget
    )
    Write-Host "Context cost report"
    Write-Host "Root: $($Result.root)"
    Write-Host "Chars per token: $($Result.chars_per_token)"
    Write-Host ""
    Write-Host "Cold-start"
    Write-Host "  total_chars: $($Result.cold_start.total_chars)"
    Write-Host "  total_tokens: $($Result.cold_start.total_tokens)"
    foreach ($item in $Result.cold_start.files) {
        Write-Host "  - $($item.path): $($item.tokens) tok ($($item.chars) chars)"
    }
    Write-Host ""
    Write-Host "Cold-start modes"
    Write-Host "  full_tokens: $($Result.cold_start_modes.full.total_tokens)"
    Write-Host "  slim_tokens: $($Result.cold_start_modes.slim.total_tokens)"
    Write-Host "  delta_tokens: $($Result.cold_start_modes.delta_tokens)"
    Write-Host "  slim_within_target: $($Result.cold_start_modes.slim_within_target)"
    Write-Host ""
    Write-Host "Dead weight"
    Write-Host "  claims released: $($Result.dead_weight.claims.released)/$($Result.dead_weight.claims.total) ($($Result.dead_weight.claims.released_percent)%)"
    Write-Host "  tasks done: $($Result.dead_weight.tasks.done)/$($Result.dead_weight.tasks.total) ($($Result.dead_weight.tasks.done_percent)%)"
    Write-Host ""
    Write-Host "Mailbox frontmatter"
    Write-Host "  messages: $($Result.mailbox_overhead.message_count)"
    Write-Host "  frontmatter/body ratio: $($Result.mailbox_overhead.frontmatter_to_body_ratio)"
    Write-Host "  frontmatter_percent: $($Result.mailbox_overhead.frontmatter_percent)%"
    if ($ShowBudget -and $null -ne $Result.budget.cold_start_tokens) {
        if ($Result.budget.exceeded) {
            Write-Host "WARNING: cold-start tokens $($Result.cold_start.total_tokens) exceed budget $($Result.budget.cold_start_tokens)"
        } else {
            Write-Host "OK: cold-start tokens $($Result.cold_start.total_tokens) within budget $($Result.budget.cold_start_tokens)"
        }
    }
}

$resolvedRoot = (Resolve-Path $Root).Path
$result = Measure-ContextCost -RootPath $resolvedRoot
if ($Baseline) {
    $Json = $true
    $result["baseline"] = [ordered]@{
        schema_version = "context_baseline.v1"
        measured_with = "measure_context_cost"
    }
}
if ($Json) {
    $result | ConvertTo-Json -Depth 20
} else {
    Write-HumanReport -Result $result -ShowBudget ([bool]$Budget)
}
