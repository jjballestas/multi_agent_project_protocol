param(
    [int]$IntervalSeconds = 180
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$LogPath = Join-Path $PSScriptRoot "work_in_progress_monitor.log"
$PidPath = Join-Path $PSScriptRoot "work_in_progress_monitor.pid"
$StopPath = Join-Path $PSScriptRoot "work_in_progress_monitor.stop"
$DonePath = Join-Path $PSScriptRoot "work_in_progress_monitor.done"
$PendingPath = Join-Path $PSScriptRoot "work_in_progress_monitor.pending.md"
$NoResponsePath = Join-Path $PSScriptRoot "work_in_progress_monitor.no_response.json"
$NoResponseStandDownTasks = @("TASK-0117")

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

function Set-MailboxStatus {
    param([string]$Path, [string]$Status)
    $content = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if ($content -match "(?m)^status:\s*\S+\s*$") {
        $content = [regex]::Replace($content, "(?m)^status:\s*\S+\s*$", "status: $Status", 1)
    } else {
        $content = $content -replace "---\s*\r?\n", "---`nstatus: $Status`n"
    }
    Write-Utf8NoBom -Path $Path -Content $content
}

function Submit-Claim {
    param([string]$Op, [string[]]$Scope)
    $claimId = "CLAIM-20260619-Codex-work-monitor"
    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $intentPath = Join-Path $PSScriptRoot "work_monitor_${Op}_intent.json"
    if ($Op -eq "acquire") {
        $payload = @{
            claim = @{
                op = "acquire"
                claim = @{
                    claim_id = $claimId
                    task_id = "COORD-20260619-WORK-MONITOR"
                    owner = "Codex"
                    scope = $Scope
                    started_at = $timestamp
                    updated_at = $timestamp
                    expires_at = (Get-Date).ToUniversalTime().AddMinutes(30).ToString("yyyy-MM-ddTHH:mm:ssZ")
                    status = "active"
                    notes = "Work monitor mailbox hygiene for Codex messages."
                }
                idempotency_key = "codex-work-monitor-acquire-$timestamp"
            }
        }
    } else {
        $payload = @{
            claim = @{
                op = "release"
                claim_id = $claimId
                idempotency_key = "codex-work-monitor-release-$timestamp"
            }
        }
    }
    Write-Utf8NoBom -Path $intentPath -Content ($payload | ConvertTo-Json -Depth 10)
    Push-Location $Root
    try {
        & python runtime\submit_intent.py --root . --actor-id Codex --timestamp $timestamp --intent $intentPath | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "submit_intent failed for monitor claim $Op"
        }
    } finally {
        Pop-Location
    }
}

function Get-ArquitectoStopOrders {
    $openDir = Join-Path $Root "Area_comun\mailbox\open"
    if (-not (Test-Path -LiteralPath $openDir)) {
        return @()
    }
    @(Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md" | Where-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
        $question = Get-Field -Content $content -Name "question"
        $requested = Get-Field -Content $content -Name "requested_action"
        $controlText = "$question`n$requested"
        ($content -match "(?im)^from:\s*Arquitecto\s*$") -and
        ($content -match "(?im)^to:\s*Codex\s*$") -and
        ($controlText -match "(?i)stand-?down|standdown|detener\s+(el\s+)?monitor|deten\s+(el\s+)?monitor|para(r)?\s+(el\s+)?monitor|monitoreo\s+(cerrado|terminado)|quiesc") -and
        ($controlText -notmatch "(?i)no\s+(detengo|detener|pares|parar)")
    })
}

function Get-CodexMessages {
    $openDir = Join-Path $Root "Area_comun\mailbox\open"
    if (-not (Test-Path -LiteralPath $openDir)) {
        return @()
    }
    @(Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md" | Where-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
        $content -match "(?im)^to:\s*Codex\s*$"
    })
}

function Get-ArquitectoMessagesToCodex {
    $openDir = Join-Path $Root "Area_comun\mailbox\open"
    if (-not (Test-Path -LiteralPath $openDir)) {
        return @()
    }
    @(Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md" | Where-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
        ($content -match "(?im)^from:\s*Arquitecto\s*$") -and
        ($content -match "(?im)^to:\s*Codex\s*$")
    })
}

function Get-CodexTasksAwaitingArquitecto {
    $indexPath = Join-Path $Root "Area_comun\state\TASK_INDEX.json"
    if (-not (Test-Path -LiteralPath $indexPath)) {
        return @()
    }
    $index = Get-Content -LiteralPath $indexPath -Raw -Encoding UTF8 | ConvertFrom-Json
    @($index.tasks | Where-Object {
        $_.owner -eq "Codex" -and $_.status -in @("in_review", "architect_review", "qa_pending")
    } | Select-Object -ExpandProperty id | Where-Object { $NoResponseStandDownTasks -notcontains $_ })
}

function Get-OpenWorkSignal {
    $openDir = Join-Path $Root "Area_comun\mailbox\open"
    if (-not (Test-Path -LiteralPath $openDir)) {
        return "open_messages=0 codex_messages=0"
    }
    $messages = @(Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md")
    $codexMessages = @(Get-CodexMessages)
    return "open_messages=$($messages.Count) codex_messages=$($codexMessages.Count)"
}

function Read-NoResponseState {
    if (-not (Test-Path -LiteralPath $NoResponsePath)) {
        return [pscustomobject]@{ counts = [pscustomobject]@{}; notified = @() }
    }
    try {
        return Get-Content -LiteralPath $NoResponsePath -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
        return [pscustomobject]@{ counts = [pscustomobject]@{}; notified = @() }
    }
}

function Write-NoResponseState {
    param([object]$State)
    Write-Utf8NoBom -Path $NoResponsePath -Content (($State | ConvertTo-Json -Depth 10) + "`n")
}

function Send-ArquitectoNoResponseCoordination {
    param([string[]]$TaskIds)
    if ($TaskIds.Count -eq 0) {
        return
    }
    $date = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss")
    $taskLabel = ($TaskIds -join "-")
    $fileName = "MSG-$date-Codex-to-Arquitecto-no-response-$taskLabel.md"
    $relativeOpen = "Area_comun/mailbox/open/$fileName"
    $target = Join-Path $Root ("Area_comun\mailbox\open\$fileName")
    $summary = "Tras 3 rondas del monitor sin respuesta de Arquitecto, Codex solicita estado de revision/bloqueo para " + ($TaskIds -join ", ") + "."
    $body = @(
        "---",
        "message_id: MSG-$date-Codex-to-Arquitecto-no-response-$taskLabel",
        "type: QUESTION",
        "task_id: " + ($TaskIds -join ","),
        "from: Codex",
        "to: Arquitecto",
        "status: open",
        "requires_response: true",
        "response_owner: Arquitecto",
        "one_line_summary: $summary",
        "question: Confirmar estado, bloqueo o ETA de revision tras 3 rondas del monitor sin respuesta.",
        "requested_action: Confirmar estado, bloqueo o ETA de revision tras 3 rondas del monitor sin respuesta.",
        "context_refs:",
        "  - Area_comun/state/TASK_INDEX.json",
        "---",
        "",
        "# Coordinacion por ausencia de respuesta",
        "",
        $summary,
        "",
        "Necesito confirmacion de estado, bloqueo o ETA para continuar la coordinacion sin asumir promocion ni encendido."
    ) -join "`n"
    try {
        Submit-Claim -Op "acquire" -Scope @(
            "Area_comun/state/CLAIMS.json",
            $relativeOpen,
            "runtime/state/events.jsonl",
            "runtime/state/snapshot.json"
        )
        try {
            Write-Utf8NoBom -Path $target -Content ($body + "`n")
            Write-Log "NO_RESPONSE_COORD sent $fileName for $($TaskIds -join ',')"
        } finally {
            Submit-Claim -Op "release" -Scope @()
        }
    } catch {
        Write-Log "NO_RESPONSE_COORD failed for $($TaskIds -join ','): $($_.Exception.Message)"
    }
}

function Invoke-ArquitectoNoResponseWatch {
    $awaiting = @(Get-CodexTasksAwaitingArquitecto)
    if ($awaiting.Count -eq 0) {
        if (Test-Path -LiteralPath $NoResponsePath) {
            Remove-Item -LiteralPath $NoResponsePath -Force
        }
        return
    }
    if ((Get-ArquitectoMessagesToCodex).Count -gt 0) {
        $state = [pscustomobject]@{ counts = [pscustomobject]@{}; notified = @() }
        Write-NoResponseState -State $state
        return
    }
    $state = Read-NoResponseState
    $notified = @($state.notified)
    $counts = @{}
    if ($state.counts) {
        foreach ($prop in $state.counts.PSObject.Properties) {
            $counts[$prop.Name] = [int]$prop.Value
        }
    }
    $toNotify = @()
    foreach ($taskId in $awaiting) {
        $current = 0
        if ($counts.ContainsKey($taskId)) {
            $current = [int]$counts[$taskId]
        }
        $counts[$taskId] = $current + 1
        if ($counts[$taskId] -ge 3 -and $notified -notcontains $taskId) {
            $toNotify += $taskId
            $notified += $taskId
        }
    }
    $state = [pscustomobject]@{
        counts = [pscustomobject]$counts
        notified = @($notified)
    }
    Write-NoResponseState -State $state
    if ($toNotify.Count -gt 0) {
        Send-ArquitectoNoResponseCoordination -TaskIds $toNotify
    }
}

function Invoke-CodexMessageProcessing {
    $messages = Get-CodexMessages
    if ($messages.Count -eq 0) {
        if (Test-Path -LiteralPath $PendingPath) {
            Remove-Item -LiteralPath $PendingPath -Force
        }
        return
    }

    $pendingLines = @("# Pending Codex mailbox", "")
    foreach ($message in $messages) {
        $content = Get-Content -LiteralPath $message.FullName -Raw -Encoding UTF8
        $requires = Get-Field -Content $content -Name "requires_response"
        $type = (Get-Field -Content $content -Name "type").ToUpperInvariant()
        $summary = Get-Field -Content $content -Name "one_line_summary"
        $requested = Get-Field -Content $content -Name "requested_action"
        $relativeOpen = "Area_comun/mailbox/open/" + $message.Name
        $relativeArchive = "Area_comun/mailbox/archived/" + $message.Name

        if ($requires -match "^(false|no)$" -and $type -in @("FYI", "ACK", "INFO")) {
            try {
                Submit-Claim -Op "acquire" -Scope @(
                    "Area_comun/state/CLAIMS.json",
                    $relativeOpen,
                    $relativeArchive,
                    "runtime/state/events.jsonl",
                    "runtime/state/snapshot.json"
                )
                try {
                    Set-MailboxStatus -Path $message.FullName -Status "archived"
                    $destination = Join-Path $Root ("Area_comun\mailbox\archived\" + $message.Name)
                    Move-Item -LiteralPath $message.FullName -Destination $destination -Force
                    Write-Log "Archived non-response Codex message $($message.Name)"
                } finally {
                    Submit-Claim -Op "release" -Scope @()
                }
            } catch {
                Write-Log "Could not archive $($message.Name): $($_.Exception.Message)"
                $pendingLines += "- $($message.Name): hygiene blocked; $summary"
            }
            continue
        }

        Write-Log "ACTION_REQUIRED $($message.Name): $summary"
        $pendingLines += "- $($message.Name)"
        if ($summary) {
            $pendingLines += "  summary: $summary"
        }
        if ($requested) {
            $pendingLines += "  requested_action: $requested"
        }
    }

    if ($pendingLines.Count -gt 2) {
        Write-Utf8NoBom -Path $PendingPath -Content (($pendingLines -join "`n") + "`n")
    } elseif (Test-Path -LiteralPath $PendingPath) {
        Remove-Item -LiteralPath $PendingPath -Force
    }
}

Set-Content -LiteralPath $PidPath -Value $PID -Encoding ASCII
if (Test-Path -LiteralPath $DonePath) {
    Remove-Item -LiteralPath $DonePath -Force
}

Write-Log "Work-in-progress monitor started. interval_seconds=$IntervalSeconds"

while ($true) {
    if (Test-Path -LiteralPath $StopPath) {
        Write-Log "Local stop marker detected; exiting."
        Set-Content -LiteralPath $DonePath -Value "done" -Encoding ASCII
        exit 0
    }

    $stopOrders = Get-ArquitectoStopOrders
    if ($stopOrders.Count -gt 0) {
        $names = ($stopOrders | Select-Object -ExpandProperty Name) -join ","
        Write-Log "Arquitecto stop order detected: $names"
        Set-Content -LiteralPath $DonePath -Value "done" -Encoding ASCII
        exit 0
    }

    Invoke-CodexMessageProcessing
    Invoke-ArquitectoNoResponseWatch
    Write-Log ("Heartbeat " + (Get-OpenWorkSignal))
    Start-Sleep -Seconds $IntervalSeconds
}
