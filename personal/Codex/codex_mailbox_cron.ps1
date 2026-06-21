param(
    [int]$IntervalSeconds = 300,
    [int]$MaxNoArquitectoRounds = 7,
    [string]$CodexExe = ""
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$RuntimeDir = Join-Path $Root ".protocol-tmp\codex_mailbox_cron"
$LogPath = Join-Path $RuntimeDir "codex_mailbox_cron.log"
$PidPath = Join-Path $RuntimeDir "codex_mailbox_cron.pid"
$StopPath = Join-Path $RuntimeDir "codex_mailbox_cron.stop"
$LockPath = Join-Path $RuntimeDir "codex_mailbox_cron.lock"
$PromptPath = Join-Path $RuntimeDir "codex_mailbox_cron.prompt.txt"
$SeenPath = Join-Path $RuntimeDir "codex_mailbox_cron.seen.json"
$RunsDir = Join-Path $RuntimeDir "runs"
$StartedAtUtc = [DateTime]::UtcNow
$NoArquitectoRounds = 0

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

function Get-CodexExecutable {
    if ($CodexExe -and (Test-Path -LiteralPath $CodexExe)) {
        return (Resolve-Path -LiteralPath $CodexExe).Path
    }
    $cmd = Get-Command codex -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -and (Test-Path -LiteralPath $cmd.Source)) {
        $content = Get-Content -LiteralPath $cmd.Source -Raw -ErrorAction SilentlyContinue
        $match = [regex]::Match($content, '"([^"]*codex\.exe)"')
        if ($match.Success -and (Test-Path -LiteralPath $match.Groups[1].Value)) {
            return $match.Groups[1].Value
        }
    }
    $whereResults = @(& where.exe codex 2>$null)
    foreach ($candidatePath in $whereResults) {
        if ($candidatePath -and (Test-Path -LiteralPath $candidatePath) -and $candidatePath.EndsWith(".exe")) {
            return (Resolve-Path -LiteralPath $candidatePath).Path
        }
    }
    $base = Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"
    $candidate = Get-ChildItem -Path $base -Recurse -Filter codex.exe -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($candidate) {
        return $candidate.FullName
    }
    $extensionBase = Join-Path $env:USERPROFILE ".vscode\extensions"
    $extensionCandidate = Get-ChildItem -Path $extensionBase -Recurse -Filter codex.exe -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($extensionCandidate) {
        return $extensionCandidate.FullName
    }
    throw "codex.exe not found"
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

function Get-ProcessableCodexMessages {
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
        ($to -eq "Codex") -and
        ($status -in @("", "open")) -and
        (
            ($requires -match "^(true|yes)$") -or
            -not [string]::IsNullOrWhiteSpace($requested) -or
            ($type -in @("GO", "REQUEST", "ACTION", "HANDOFF", "REVIEW", "QUESTION"))
        ) -and
        ((-not $seen.ContainsKey($_.Name)) -or ($seen[$_.Name] -ne $signature))
    })
}

function Get-ArquitectoResponsesToCodex {
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
            ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^from:\s*Arquitecto\s*$") -and
            ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^to:\s*Codex\s*$")
        })
    }
    return @($matches)
}

function Test-ArquitectoStopOrder {
    $responses = Get-ArquitectoResponsesToCodex
    foreach ($response in $responses) {
        $content = Get-Content -LiteralPath $response.FullName -Raw -Encoding UTF8
        $requested = Get-Field -Content $content -Name "requested_action"
        $summary = Get-Field -Content $content -Name "one_line_summary"
        $text = "$summary`n$requested`n$content"
        if ($text -match "(?i)\b(detener|deten|parar|para|stop|standdown|stand-down)\b.*\b(cron|monitor|monitoreo|Codex)\b") {
            return $true
        }
    }
    return $false
}

function Invoke-CodexForMessage {
    param([System.IO.FileInfo]$Message)
    if (Test-Path -LiteralPath $LockPath) {
        Write-Log "LOCKED skip $($Message.Name)"
        return
    }

    New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null
    $codexPath = Get-CodexExecutable
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
    $safeName = [IO.Path]::GetFileNameWithoutExtension($Message.Name)
    $stdoutPath = Join-Path $RunsDir "$stamp-$safeName.out.log"
    $stderrPath = Join-Path $RunsDir "$stamp-$safeName.err.log"
    $messageRelative = $Message.FullName.Substring($Root.Length + 1).Replace("\", "/")

    $prompt = @"
Lee AGENTS.md, personal/Codex/STARTUP_PROMPT.md y personal/Codex/Memory.md antes de actuar.

Regla primordial: no narrar proceso. Solo emitir cierre, bloqueo concreto, fallo/riesgo accionable, decision requerida o resultado de coordinacion.

Arranque obligatorio:
1. Revisar git status --short y no tocar cambios ajenos.
2. Revisar Area_comun/mailbox/open/.
3. Validar drift antes de cualquier ledger action.

Mensaje a procesar en esta ejecucion:
$messageRelative

Si el mensaje sigue abierto, esta dirigido a Codex y contiene una accion ejecutable (requested_action, GO, QUESTION, HANDOFF o requires_response:true), procesarlo en esta sesion con claim file-scoped + submit_intent cuando toque ledger; no dejarlo solo como ACTION_REQUIRED. Si ya fue resuelto o no aplica, emitir cierre concreto.
"@
    Write-Utf8NoBom -Path $PromptPath -Content $prompt
    Write-Utf8NoBom -Path $LockPath -Content "$stamp $($Message.Name)`n"

    try {
        $args = @(
            "exec",
            "-s", "danger-full-access",
            "-c", "approval_policy=never",
            "-c", "model_reasoning_effort=low",
            "--skip-git-repo-check",
            "--"
        )
        $args += $prompt
        $process = Start-Process -FilePath $codexPath -ArgumentList $args -WorkingDirectory $Root -WindowStyle Hidden -PassThru -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
        Write-Log "EXEC_START pid=$($process.Id) message=$($Message.Name)"
        $process.WaitForExit()
        Write-Log "EXEC_EXIT code=$($process.ExitCode) message=$($Message.Name)"
        $seen = Read-Seen
        $seen[$Message.Name] = Get-MessageSignature -Message $Message
        Write-Seen -Seen $seen
    } catch {
        Write-Log "EXEC_FAIL message=$($Message.Name) error=$($_.Exception.Message)"
        $seen = Read-Seen
        $seen[$Message.Name] = Get-MessageSignature -Message $Message
        Write-Seen -Seen $seen
    } finally {
        if (Test-Path -LiteralPath $LockPath) {
            Remove-Item -LiteralPath $LockPath -Force
        }
    }
}

New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null
Set-Content -LiteralPath $PidPath -Value $PID -Encoding ASCII
if (Test-Path -LiteralPath $StopPath) {
    Remove-Item -LiteralPath $StopPath -Force
}
Write-Log "Codex mailbox cron started. interval_seconds=$IntervalSeconds max_no_arquitecto_rounds=$MaxNoArquitectoRounds"

while ($true) {
    if (Test-Path -LiteralPath $StopPath) {
        Write-Log "Stop marker detected; exiting."
        exit 0
    }

    try {
        if (Test-ArquitectoStopOrder) {
            Write-Log "Arquitecto stop order detected; exiting."
            exit 0
        }

        $architectResponses = @(Get-ArquitectoResponsesToCodex)
        if ($architectResponses.Count -gt 0) {
            $NoArquitectoRounds = 0
            Write-Log "Arquitecto responses detected count=$($architectResponses.Count)"
        } else {
            $NoArquitectoRounds += 1
            Write-Log "No Arquitecto response round=$NoArquitectoRounds"
            if ($NoArquitectoRounds -ge $MaxNoArquitectoRounds) {
                Write-Log "No Arquitecto response limit reached; exiting."
                exit 0
            }
        }

        $messages = @(Get-ProcessableCodexMessages)
        if ($messages.Count -eq 0) {
            Write-Log "Heartbeat processable_messages=0"
        } else {
            foreach ($message in $messages) {
                Invoke-CodexForMessage -Message $message
            }
        }
    } catch {
        Write-Log "LOOP_ERROR $($_.Exception.Message)"
    }

    Start-Sleep -Seconds $IntervalSeconds
}
