param(
    [int]$IntervalSeconds = 180,
    [string]$CodexExe = ""
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$LogPath = Join-Path $PSScriptRoot "codex_mailbox_cron.log"
$PidPath = Join-Path $PSScriptRoot "codex_mailbox_cron.pid"
$StopPath = Join-Path $PSScriptRoot "codex_mailbox_cron.stop"
$LockPath = Join-Path $PSScriptRoot "codex_mailbox_cron.lock"
$PromptPath = Join-Path $PSScriptRoot "codex_mailbox_cron.prompt.txt"
$RunsDir = Join-Path $PSScriptRoot "codex_mailbox_cron_runs"

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
    $base = Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"
    $candidate = Get-ChildItem -Path $base -Recurse -Filter codex.exe -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($candidate) {
        return $candidate.FullName
    }
    throw "codex.exe not found"
}

function Get-ExecutableCodexMessages {
    $openDir = Join-Path $Root "Area_comun\mailbox\open"
    if (-not (Test-Path -LiteralPath $openDir)) {
        return @()
    }
    @(Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md" | Where-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
        $to = Get-Field -Content $content -Name "to"
        $requires = Get-Field -Content $content -Name "requires_response"
        $requested = Get-Field -Content $content -Name "requested_action"
        ($to -eq "Codex") -and
        ($requires -match "^(true|yes)$") -and
        -not [string]::IsNullOrWhiteSpace($requested)
    })
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

Si el mensaje sigue abierto, tiene to: Codex, requires_response:true y requested_action ejecutable, procesarlo en esta sesion con claim file-scoped + submit_intent; no dejarlo solo como ACTION_REQUIRED. Si ya fue resuelto o no aplica, emitir cierre concreto.
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
    } catch {
        Write-Log "EXEC_FAIL message=$($Message.Name) error=$($_.Exception.Message)"
    } finally {
        if (Test-Path -LiteralPath $LockPath) {
            Remove-Item -LiteralPath $LockPath -Force
        }
    }
}

Set-Content -LiteralPath $PidPath -Value $PID -Encoding ASCII
if (Test-Path -LiteralPath $StopPath) {
    Remove-Item -LiteralPath $StopPath -Force
}
Write-Log "Codex mailbox cron started. interval_seconds=$IntervalSeconds"

while ($true) {
    if (Test-Path -LiteralPath $StopPath) {
        Write-Log "Stop marker detected; exiting."
        exit 0
    }

    try {
        $messages = @(Get-ExecutableCodexMessages)
        if ($messages.Count -eq 0) {
            Write-Log "Heartbeat executable_messages=0"
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
