param(
    [int]$IntervalSeconds = 300,
    [int]$MaxNoOperatorRounds = 7,
    [string]$AgentExe = "",
    [string]$ReasoningEffort = "medium",
    [switch]$DryRunOnce,
    [switch]$RunClassifierSelfTest
)

# arquitecto_cron.ps1 -- runtime headless del Arquitecto para orquestar GOAL-REQ-ZEUS-001.
# El operador lanza este harness. El script no escribe ledger por si mismo: solo invoca el runtime
# del Arquitecto con el prompt cableado por stdin.

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$RuntimeDir = Join-Path $Root ".protocol-tmp\arquitecto_cron"
$LogPath = Join-Path $RuntimeDir "arquitecto_cron.log"
$PidPath = Join-Path $RuntimeDir "arquitecto_cron.pid"
$StopPath = Join-Path $RuntimeDir "arquitecto_cron.stop"
$LockPath = Join-Path $RuntimeDir "arquitecto_cron.lock"
$SeenPath = Join-Path $RuntimeDir "arquitecto_cron.seen.json"
$PromptSourcePath = Join-Path $PSScriptRoot "arquitecto_cron.prompt.txt"
$PromptRuntimePath = Join-Path $RuntimeDir "arquitecto_cron.prompt.txt"
$RunsDir = Join-Path $RuntimeDir "runs"
$StartedAtUtc = [DateTime]::UtcNow
$NoOperatorRounds = 0

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, ($Content -replace "`r`n", "`n"), $encoding)
}

function Write-Log {
    param([string]$Message)
    $line = "$(Get-Date -Format s) $Message`n"
    if (Test-Path -LiteralPath $LogPath) {
        $current = Get-Content -LiteralPath $LogPath -Raw -Encoding UTF8
        Write-Utf8NoBom -Path $LogPath -Content ($current + $line)
    } else {
        Write-Utf8NoBom -Path $LogPath -Content $line
    }
}

function Get-Field {
    param([string]$Content, [string]$Name)
    $match = [regex]::Match($Content, "(?im)^" + [regex]::Escape($Name) + ":\s*(.+?)\s*$")
    if ($match.Success) {
        return $match.Groups[1].Value.Trim().Trim('"')
    }
    return ""
}

function Get-AgentExecutable {
    if ($AgentExe -and (Test-Path -LiteralPath $AgentExe)) {
        return (Resolve-Path -LiteralPath $AgentExe).Path
    }
    foreach ($name in @("claude", "codex")) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd -and $cmd.Source -and (Test-Path -LiteralPath $cmd.Source)) {
            return (Resolve-Path -LiteralPath $cmd.Source).Path
        }
    }
    foreach ($name in @("claude.exe", "codex.exe")) {
        $whereResults = @(& where.exe $name 2>$null)
        foreach ($candidatePath in $whereResults) {
            if ($candidatePath -and (Test-Path -LiteralPath $candidatePath)) {
                return (Resolve-Path -LiteralPath $candidatePath).Path
            }
        }
    }
    $bases = @(
        (Join-Path $env:LOCALAPPDATA "AnthropicClaude\bin"),
        (Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"),
        (Join-Path $env:USERPROFILE ".vscode\extensions")
    )
    foreach ($base in $bases) {
        foreach ($filter in @("claude.exe", "codex.exe")) {
            $candidate = Get-ChildItem -Path $base -Recurse -Filter $filter -ErrorAction SilentlyContinue |
                Sort-Object LastWriteTime -Descending |
                Select-Object -First 1
            if ($candidate) {
                return $candidate.FullName
            }
        }
    }
    throw "agent executable not found; pass -AgentExe"
}

function Read-Seen {
    if (-not (Test-Path -LiteralPath $SeenPath)) {
        return @{}
    }
    try {
        $json = Get-Content -LiteralPath $SeenPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $seen = @{}
        foreach ($prop in $json.PSObject.Properties) {
            $seen[$prop.Name] = [string]$prop.Value
        }
        return $seen
    } catch {
        return @{}
    }
}

function Write-Seen {
    param([hashtable]$Seen)
    $object = [ordered]@{}
    foreach ($key in ($Seen.Keys | Sort-Object)) {
        $object[$key] = $Seen[$key]
    }
    Write-Utf8NoBom -Path $SeenPath -Content (($object | ConvertTo-Json -Depth 5) + "`n")
}

function Get-MessageSignature {
    param([System.IO.FileInfo]$Message)
    return "$($Message.Name)|$($Message.Length)|$($Message.LastWriteTimeUtc.Ticks)"
}

function Get-ProcessableArquitectoMessages {
    $openDir = Join-Path $Root "Area_comun\mailbox\open"
    if (-not (Test-Path -LiteralPath $openDir)) {
        return @()
    }
    $seen = Read-Seen
    @(Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md" | Where-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
        $to = Get-Field -Content $content -Name "to"
        $status = Get-Field -Content $content -Name "status"
        $requires = Get-Field -Content $content -Name "requires_response"
        $type = (Get-Field -Content $content -Name "type").ToUpperInvariant()
        $requested = Get-Field -Content $content -Name "requested_action"
        $signature = Get-MessageSignature -Message $_
        ($to -eq "Arquitecto") -and
        ($status -in @("", "open")) -and
        (
            ($requires -match "^(true|yes)$") -or
            -not [string]::IsNullOrWhiteSpace($requested) -or
            ($type -in @("GO", "REQUEST", "ACTION", "HANDOFF", "REVIEW", "QUESTION", "DECISION"))
        ) -and
        ((-not $seen.ContainsKey($_.Name)) -or ($seen[$_.Name] -ne $signature))
    })
}

function Get-OperatorMessagesToArquitecto {
    $mailboxRoot = Join-Path $Root "Area_comun\mailbox"
    $folders = @("open", "answered", "archived")
    $matches = @()
    foreach ($folder in $folders) {
        $dir = Join-Path $mailboxRoot $folder
        if (-not (Test-Path -LiteralPath $dir)) {
            continue
        }
        $matches += @(Get-ChildItem -LiteralPath $dir -File -Filter "MSG-*.md" | Where-Object {
            $_.LastWriteTimeUtc -ge $StartedAtUtc -and
            ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^from:\s*(Operador|operador humano)\s*$") -and
            ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^to:\s*Arquitecto\s*$")
        })
    }
    return @($matches)
}

function Test-OperatorStopOrder {
    $messages = Get-OperatorMessagesToArquitecto
    foreach ($message in $messages) {
        $content = Get-Content -LiteralPath $message.FullName -Raw -Encoding UTF8
        $requested = Get-Field -Content $content -Name "requested_action"
        $summary = Get-Field -Content $content -Name "one_line_summary"
        $text = "$summary`n$requested`n$content"
        if ($text -match "(?i)\b(detener|deten|parar|para|stop|standdown|stand-down)\b.*\b(cron|monitor|monitoreo|Arquitecto)\b") {
            return $true
        }
    }
    return $false
}

function Test-WsTask {
    param($Task)
    $id = [string]$Task.id
    $title = [string]$Task.title
    $project = [string]$Task.project

    return (
        ($id -match "^TASK-02") -or
        ($id -match "^REQ-ZEUS") -or
        ($title -match "(?i)(Zeus|WS|REQ-ZEUS|Aegis|cron)") -or
        ($project -in @("Zeus-protocol", "Zeus-Aegis", "multi_agent_project_protocol"))
    )
}

function New-WsSnapshot {
    param([object[]]$Tasks, [int]$OpenMessages)
    $relevantTasks = @($Tasks | Where-Object { Test-WsTask -Task $_ } | Sort-Object id)
    $inReview = @($relevantTasks | Where-Object { $_.status -eq "in_review" })
    $ready = @($relevantTasks | Where-Object { $_.status -eq "ready" })
    $codexActive = @($relevantTasks | Where-Object { $_.owner -eq "Codex" -and $_.status -eq "in_progress" })

    [ordered]@{
        utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        in_review = @($inReview | Select-Object -First 5 id, owner, title, status)
        ready = @($ready | Select-Object -First 5 id, owner, title, status)
        codex_in_progress = @($codexActive | Select-Object id, title, status)
        open_mailbox_messages = $OpenMessages
        decision = if ($inReview.Count -gt 0) {
            "review_or_ratify"
        } elseif ($ready.Count -gt 0 -and $codexActive.Count -eq 0) {
            "promote_one_ready_task"
        } else {
            "no_action"
        }
    }
}

function Test-WsClassifier {
    $cases = @(
        [pscustomobject]@{
            name = "task02_in_review_without_project"
            tasks = @(
                [pscustomobject]@{ id = "TASK-0299"; owner = "Codex"; title = "Classifier review candidate"; status = "in_review" },
                [pscustomobject]@{ id = "TASK-0300"; owner = "Codex"; title = "Next ready candidate"; status = "ready" }
            )
            expectedDecision = "review_or_ratify"
            expectedInReview = 1
        },
        [pscustomobject]@{
            name = "req_zeus_ws_in_review_without_project"
            tasks = @(
                [pscustomobject]@{ id = "REQ-ZEUS-WS-TEST"; owner = "Arquitecto"; title = "WS review candidate"; status = "in_review" }
            )
            expectedDecision = "review_or_ratify"
            expectedInReview = 1
        },
        [pscustomobject]@{
            name = "ready_not_promoted_when_relevant_in_review_exists"
            tasks = @(
                [pscustomobject]@{ id = "TASK-0298"; owner = "Codex"; title = "Ready candidate"; status = "ready" },
                [pscustomobject]@{ id = "TASK-0297"; owner = "Codex"; title = "Review candidate"; status = "in_review" }
            )
            expectedDecision = "review_or_ratify"
            expectedInReview = 1
        }
    )
    $results = @()
    foreach ($case in $cases) {
        $snapshot = New-WsSnapshot -Tasks $case.tasks -OpenMessages 0
        $passed = (($snapshot.decision -eq $case.expectedDecision) -and ($snapshot.in_review.Count -eq $case.expectedInReview))
        $results += [ordered]@{
            name = $case.name
            passed = $passed
            decision = $snapshot.decision
            in_review_count = $snapshot.in_review.Count
        }
    }
    $failed = @($results | Where-Object { -not $_.passed })
    [ordered]@{
        classifier_self_test = if ($failed.Count -eq 0) { "PASS" } else { "FAIL" }
        tests = $results
    } | ConvertTo-Json -Depth 8
    if ($failed.Count -gt 0) {
        exit 1
    }
}

function Get-WsSnapshot {
    $taskIndexPath = Join-Path $Root "Area_comun\state\TASK_INDEX.json"
    $mailboxPath = Join-Path $Root "Area_comun\mailbox\open"
    $tasks = @()
    if (Test-Path -LiteralPath $taskIndexPath) {
        $doc = Get-Content -LiteralPath $taskIndexPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $tasks = @($doc.tasks)
    }
    $openMessages = 0
    if (Test-Path -LiteralPath $mailboxPath) {
        $openMessages = @(Get-ChildItem -LiteralPath $mailboxPath -File -Filter "MSG-*.md").Count
    }
    New-WsSnapshot -Tasks $tasks -OpenMessages $openMessages
}

function Get-CyclePrompt {
    if (Test-Path -LiteralPath $PromptSourcePath) {
        return Get-Content -LiteralPath $PromptSourcePath -Raw -Encoding UTF8
    }
    return @"
Eres el ARQUITECTO. Placeholder operativo para arquitecto_cron.prompt.txt.
Lee AGENTS.md, personal/Arquitecto/STARTUP_PROMPT.md, state y mailbox. Respeta DECISION-0038,
DECISION-0057 y GOAL-REQ-ZEUS-001. No escribas ledger salvo accion gobernada con gates verdes.
"@
}

function Invoke-ArquitectoCycle {
    if (Test-Path -LiteralPath $LockPath) {
        Write-Log "LOCKED skip cycle"
        return
    }

    New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null
    $agentPath = Get-AgentExecutable
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
    $stdoutPath = Join-Path $RunsDir "$stamp-arquitecto.out.log"
    $stderrPath = Join-Path $RunsDir "$stamp-arquitecto.err.log"
    $processable = @(Get-ProcessableArquitectoMessages | Select-Object -ExpandProperty Name)
    $snapshot = Get-WsSnapshot
    $cyclePrompt = @"
$(Get-CyclePrompt)

MENSAJES ABIERTOS PROCESABLES PARA ARQUITECTO:
$($processable -join "`n")

SNAPSHOT DRY-READ DEL HARNESS:
$($snapshot | ConvertTo-Json -Depth 8)
"@
    Write-Utf8NoBom -Path $PromptRuntimePath -Content $cyclePrompt
    Write-Utf8NoBom -Path $LockPath -Content "$stamp arquitecto-cycle`n"

    try {
        $leaf = Split-Path -Leaf $agentPath
        if ($leaf -match "^codex(\.exe)?$") {
            $execArgs = @(
                "exec",
                "-s", "danger-full-access",
                "-c", "approval_policy=never",
                "-c", "model_reasoning_effort=$ReasoningEffort",
                "--skip-git-repo-check",
                "-"
            )
        } else {
            $execArgs = @()
        }
        $process = Start-Process -FilePath $agentPath -ArgumentList $execArgs -WorkingDirectory $Root -WindowStyle Hidden -PassThru -RedirectStandardInput $PromptRuntimePath -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
        Write-Log "EXEC_START pid=$($process.Id)"
        $process.WaitForExit()
        Write-Log "EXEC_EXIT code=$($process.ExitCode)"
        $seen = Read-Seen
        foreach ($message in Get-ProcessableArquitectoMessages) {
            $seen[$message.Name] = Get-MessageSignature -Message $message
        }
        Write-Seen -Seen $seen
    } catch {
        Write-Log "EXEC_FAIL error=$($_.Exception.Message)"
    } finally {
        if (Test-Path -LiteralPath $LockPath) {
            Remove-Item -LiteralPath $LockPath -Force
        }
    }
}

New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null

if ($RunClassifierSelfTest) {
    Test-WsClassifier
    exit 0
}

if ($DryRunOnce) {
    $snapshot = Get-WsSnapshot
    $processable = @(Get-ProcessableArquitectoMessages | Select-Object -ExpandProperty Name)
    [ordered]@{
        mode = "dry_run_once"
        ledger_write = $false
        prompt_source = $PromptSourcePath
        processable_messages = $processable
        ws_snapshot = $snapshot
    } | ConvertTo-Json -Depth 10
    exit 0
}

Set-Content -LiteralPath $PidPath -Value $PID -Encoding ASCII
if (Test-Path -LiteralPath $StopPath) {
    Remove-Item -LiteralPath $StopPath -Force
}
Write-Log "Arquitecto cron started. interval_seconds=$IntervalSeconds max_no_operator_rounds=$MaxNoOperatorRounds effort=$ReasoningEffort"

while ($true) {
    if (Test-Path -LiteralPath $StopPath) {
        Write-Log "Stop marker detected; exiting."
        exit 0
    }

    try {
        if (Test-OperatorStopOrder) {
            Write-Log "Operator stop order detected; exiting."
            exit 0
        }

        $operatorMessages = @(Get-OperatorMessagesToArquitecto)
        if ($operatorMessages.Count -gt 0) {
            $NoOperatorRounds = 0
            Write-Log "Operator messages detected count=$($operatorMessages.Count)"
        } else {
            $NoOperatorRounds += 1
            Write-Log "No operator message round=$NoOperatorRounds"
            if ($NoOperatorRounds -ge $MaxNoOperatorRounds) {
                Write-Log "No operator message limit reached; exiting."
                exit 0
            }
        }

        Invoke-ArquitectoCycle
    } catch {
        Write-Log "LOOP_ERROR $($_.Exception.Message)"
    }

    Start-Sleep -Seconds $IntervalSeconds
}
