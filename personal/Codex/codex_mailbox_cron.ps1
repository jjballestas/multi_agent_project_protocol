param(
    [int]$IntervalSeconds = 300,
    [int]$MaxNoArquitectoRounds = 15,
    [string]$CodexExe = "",
    [int]$ExecTimeoutSeconds = 3600
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$RuntimeDir = Join-Path $Root ".protocol-tmp\codex_mailbox_cron"
$LogPath = Join-Path $RuntimeDir "codex_mailbox_cron.log"
$PidPath = Join-Path $RuntimeDir "codex_mailbox_cron.pid"
$StopPath = Join-Path $RuntimeDir "codex_mailbox_cron.stop"
$LockPath = Join-Path $RuntimeDir "codex_mailbox_cron.lock"
$LeasePath = Join-Path $RuntimeDir "codex_mailbox_cron.exec-lease.json"
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

function Get-ProcessStartTimeUtc {
    param([System.Diagnostics.Process]$Process)
    try {
        return $Process.StartTime.ToUniversalTime().ToString("o")
    } catch {
        return ""
    }
}

function Get-CmdlineHash {
    param([string]$Text)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
        return ([System.BitConverter]::ToString($sha.ComputeHash($bytes)) -replace "-", "").ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function Write-ExecLease {
    param(
        [System.Diagnostics.Process]$Process,
        [string]$MessageName,
        [string[]]$Arguments,
        [DateTime]$DeadlineUtc
    )
    $cmdline = "$($Process.StartInfo.FileName) $($Arguments -join ' ')"
    $lease = [ordered]@{
        schema_version = 1
        owner = "Codex"
        task_or_msg_id = $MessageName
        pid = $Process.Id
        process_start_time_utc = Get-ProcessStartTimeUtc -Process $Process
        cmdline_hash = Get-CmdlineHash -Text $cmdline
        cmdline = $cmdline
        started_at = (Get-Date).ToUniversalTime().ToString("o")
        deadline = $DeadlineUtc.ToString("o")
        heartbeat_monotonic = [System.Diagnostics.Stopwatch]::GetTimestamp()
        shutdown_policy = "stop_after_current_turn"
    }
    Write-Utf8NoBom -Path $LeasePath -Content (($lease | ConvertTo-Json -Depth 8) + "`n")
}

function Update-ExecLeaseHeartbeat {
    if (-not (Test-Path -LiteralPath $LeasePath)) {
        return
    }
    try {
        $lease = Get-Content -LiteralPath $LeasePath -Raw -Encoding UTF8 | ConvertFrom-Json
        $lease.heartbeat_monotonic = [System.Diagnostics.Stopwatch]::GetTimestamp()
        Write-Utf8NoBom -Path $LeasePath -Content (($lease | ConvertTo-Json -Depth 8) + "`n")
    } catch {
        Write-Log "LEASE_HEARTBEAT_FAIL error=$($_.Exception.Message)"
    }
}

function Test-LeaseProcessMatches {
    param($Lease)
    if (-not $Lease -or -not $Lease.pid -or -not $Lease.process_start_time_utc) {
        return $false
    }
    try {
        $process = Get-Process -Id ([int]$Lease.pid) -ErrorAction Stop
        $started = $process.StartTime.ToUniversalTime().ToString("o")
        return ($started -eq [string]$Lease.process_start_time_utc)
    } catch {
        return $false
    }
}

function Stop-LeaseProcessTree {
    param($Lease, [string]$Reason)
    if (-not (Test-LeaseProcessMatches -Lease $Lease)) {
        return $false
    }
    $cmdline = [string]$Lease.cmdline
    if ($cmdline -match "(?i)(submit_intent|git(\.exe)?\s|npm(\.cmd)?\s+test|vitest|validate_collaboration_state)") {
        Write-Log "TREE_KILL_DENY pid=$($Lease.pid) reason=deny_cmdline message=$($Lease.task_or_msg_id)"
        return $false
    }
    try {
        Write-Log "TREE_KILL pid=$($Lease.pid) reason=$Reason message=$($Lease.task_or_msg_id)"
        $taskkill = Start-Process -FilePath "taskkill.exe" -ArgumentList @("/PID", [string]$Lease.pid, "/T", "/F") -WindowStyle Hidden -Wait -PassThru
        return ($taskkill.ExitCode -eq 0)
    } catch {
        Write-Log "TREE_KILL_FAIL pid=$($Lease.pid) error=$($_.Exception.Message)"
        return $false
    }
}

function Clear-StaleCronLockIfSafe {
    if (-not (Test-Path -LiteralPath $LockPath)) {
        return
    }
    if (-not (Test-Path -LiteralPath $LeasePath)) {
        return
    }
    try {
        $lease = Get-Content -LiteralPath $LeasePath -Raw -Encoding UTF8 | ConvertFrom-Json
        $matches = Test-LeaseProcessMatches -Lease $lease
        $deadline = [DateTime]::Parse([string]$lease.deadline).ToUniversalTime()
        if ($matches) {
            if ([DateTime]::UtcNow -le $deadline) {
                return
            }
            if (-not (Stop-LeaseProcessTree -Lease $lease -Reason "orphan_expired")) {
                return
            }
        }
        Remove-Item -LiteralPath $LockPath -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath $LeasePath -Force -ErrorAction SilentlyContinue
        $deadlineState = if ([DateTime]::UtcNow -le $deadline) { "pre_deadline" } else { "expired" }
        Write-Log "SELF_HEAL_STALE_LOCK owner=Codex pid=$($lease.pid) message=$($lease.task_or_msg_id) state=$deadlineState"
    } catch {
        Write-Log "SELF_HEAL_FAIL error=$($_.Exception.Message)"
    }
}

function Stop-ExpiredLeaseProcess {
    param($Lease)
    [void](Stop-LeaseProcessTree -Lease $Lease -Reason "deadline")
}

function Test-ExistingCronInstance {
    if (-not (Test-Path -LiteralPath $PidPath)) {
        return $false
    }
    try {
        $pidText = (Get-Content -LiteralPath $PidPath -Raw -Encoding ASCII).Trim()
        if (-not $pidText) {
            return $false
        }
        $existing = Get-Process -Id ([int]$pidText) -ErrorAction Stop
        if ($existing.Id -eq $PID) {
            return $false
        }
        $pidInfoPath = "$PidPath.json"
        if (Test-Path -LiteralPath $pidInfoPath) {
            $info = Get-Content -LiteralPath $pidInfoPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $started = $existing.StartTime.ToUniversalTime().ToString("o")
            return ($started -eq [string]$info.process_start_time_utc)
        }
        return $true
    } catch {
        return $false
    }
}

function Write-CronPid {
    Set-Content -LiteralPath $PidPath -Value $PID -Encoding ASCII
    $info = [ordered]@{
        pid = $PID
        process_start_time_utc = (Get-Process -Id $PID).StartTime.ToUniversalTime().ToString("o")
    }
    Write-Utf8NoBom -Path "$PidPath.json" -Content (($info | ConvertTo-Json -Depth 4) + "`n")
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
        ($type -in @("GO", "REQUEST", "ACTION", "HANDOFF", "REVIEW", "QUESTION", "DECISION"))
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
        # DIRECTIVA operador: SOLO el token exacto STOP_JOB detiene al agente (sin ambiguedades).
        # Case-sensitive y solo en summary/requested_action (no en el body, para no tripear con menciones).
        if (($requested.Trim() -ceq "STOP_JOB") -or ($summary.Trim() -ceq "STOP_JOB")) {
            return $true
        }
    }
    return $false
}

function Invoke-CodexForMessage {
    param([System.IO.FileInfo]$Message)
    Clear-StaleCronLockIfSafe
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
    $promptPath = Join-Path $RunsDir "$stamp-$safeName.prompt.txt"
    $messageRelative = $Message.FullName.Substring($Root.Length + 1).Replace("\", "/")

$prompt = @"
Lee AGENTS.md, personal/Codex/STARTUP_PROMPT.md y personal/Codex/Memory.md antes de actuar.

Regla primordial: no narrar proceso. Solo emitir cierre, bloqueo concreto, fallo/riesgo accionable, decision requerida o resultado de coordinacion.

Arranque obligatorio:
1. Revisar git status --short en d:/Agentes/multi_agent_project_protocol y D:/Agentes/NOVA-Suite/NOVA; no tocar cambios ajenos.
2. Revisar Area_comun/mailbox/open/.
3. Revisar Area_comun/state/TASK_INDEX.json y Area_comun/state/CLAIMS.json.
4. Validar drift antes de cualquier ledger action.

Mensaje a procesar en esta ejecucion:
$messageRelative

Modo ejecutor obligatorio:
1. Si el mensaje sigue abierto, esta dirigido a Codex y contiene una accion ejecutable (requested_action, GO, QUESTION, HANDOFF, DECISION ejecutable o requires_response:true), resolverlo en esta sesion.
2. Si hay GO a Codex asociado a una tarea owner=Codex status=ready y Codex no tiene otra tarea in_progress activa, tomar UNA tarea: claim file-scoped via runtime/submit_intent.py, task_status ready->in_progress via submit_intent e implementar el codigo requerido en D:/Agentes/NOVA-Suite/NOVA (producto en la raiz: src/, apps/; si la tarea es de gobernanza de NOVA, submit_intent y Area_comun viven bajo D:/Agentes/NOVA-Suite/NOVA/Aegis/).
3. Si Codex ya tiene claim in_progress, continuar esa implementacion hasta entregar; no quedarse en lectura, resumen ni ACTION_REQUIRED.
4. Ejecutar gates aplicables del producto (node --check, npm test, smoke cuando exista) y del protocolo (validate, drift, #4 byte-identica cuando aplique).
5. Entregar como implementer: commit explicito, handoff autocontenido en Area_comun/handoffs/, mensaje Codex->Arquitecto en Area_comun/mailbox/open/, task_status in_progress->in_review y release de claim via submit_intent. No auto-cerrar a done: maker!=checker. Todo commit que toque rutas gobernadas debe emitir trailers finales: Task-Id: <TASK-XXXX> y, si corrige un hallazgo, Fixes-Task: <TASK-XXXX>. Si el commit es solo coordinacion sin tarea, O un ANNOUNCE en el HUB sobre una tarea de OTRA instancia (p.ej. Aegis, cuyo Task-Id NO existe en el TASK_INDEX del hub), emitir Task-Id: none Y Ops-Reason: <motivo> JUNTOS en el bloque final de trailers (AMBOS, nunca solo uno; sin blank line entre ellos ni con Co-Authored-By; Ops-Reason <=120 chars). Un announce del hub sobre una tarea de Aegis con Task-Id: TASK-XXXX de Aegis, o con solo Ops-Reason, rompe el gate de trailers del hub.
6. Responder o mover a answered el GO/mensaje consumido solo despues de que el ledger respalde la entrega.
7. Tras un NO-GO/change_required del checker, ejecutar fix-loop antes del commit de cierre: remediar, re-ejecutar gates afectados, re-juzgar contra criterios de aceptacion y hallazgo, maximo 2 iteraciones; si persiste la misma clase de hallazgo, escalar al operador con una pregunta concreta.
8. La salida final del turno y todo handoff de entrega deben terminar con el envelope textual de 7 campos (no tool call): task_id, status, executive_summary, artifacts, gates, next_recommended, risks. Usar ASCII y citar commits/rutas/comandos exactos.
9. Si no hay tarea ejecutable para Codex, no-op con cierre concreto. La parada a 7 rondas sin novedad sigue valida. No activar uso vivo ni cron nuevo sin GO explicito.
"@
    Write-Utf8NoBom -Path $promptPath -Content $prompt
    Write-Utf8NoBom -Path $LockPath -Content "$stamp $($Message.Name)`n"

    try {
        # El prompt se pasa por STDIN (RedirectStandardInput), NO como argumento: Start-Process -ArgumentList
        # parte un argumento multi-palabra en tokens sueltos (PS 5.1) y codex interpreta la 2da palabra como
        # subcomando. codex exec lee el prompt de stdin con '-'.
        $execArgs = @(
            "exec",
            "-s", "danger-full-access",
            "-c", "approval_policy=never",
            "-c", "model_reasoning_effort=low",
            "--skip-git-repo-check",
            "-"
        )
        $deadlineUtc = [DateTime]::UtcNow.AddSeconds($ExecTimeoutSeconds)
        $process = Start-Process -FilePath $codexPath -ArgumentList $execArgs -WorkingDirectory $Root -WindowStyle Hidden -PassThru -RedirectStandardInput $promptPath -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
        Write-ExecLease -Process $process -MessageName $Message.Name -Arguments $execArgs -DeadlineUtc $deadlineUtc
        Write-Log "EXEC_START pid=$($process.Id) message=$($Message.Name)"
        while (-not $process.WaitForExit(1000)) {
            Update-ExecLeaseHeartbeat
            if (Test-Path -LiteralPath $StopPath) {
                Write-Log "Stop marker detected; waiting for current exec pid=$($process.Id)"
            }
            if ([DateTime]::UtcNow -gt $deadlineUtc) {
                $lease = Get-Content -LiteralPath $LeasePath -Raw -Encoding UTF8 | ConvertFrom-Json
                Stop-ExpiredLeaseProcess -Lease $lease
                $process.WaitForExit()
                break
            }
        }
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
        if (Test-Path -LiteralPath $LeasePath) {
            Remove-Item -LiteralPath $LeasePath -Force
        }
    }
}

New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null
Clear-StaleCronLockIfSafe
if (Test-ExistingCronInstance) {
    Write-Log "INSTANCE_ALREADY_RUNNING pid_file=$PidPath; exiting."
    exit 0
}
Write-CronPid
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
