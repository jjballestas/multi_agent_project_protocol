param(
    [int]$IntervalSeconds = 300,
    [int]$MaxNoArquitectoRounds = 15,
    [string]$AgentExe = "",
    [string]$ReasoningEffort = "medium",
    [int]$ExecTimeoutSeconds = 3600
)

# analista_mailbox_cron.ps1 -- runtime lanzable del Analista (voz adversarial / checker independiente).
# Mirror de personal/Codex/codex_mailbox_cron.ps1 adaptado al rol REVISOR (no implementer).
# Creado por el Arquitecto bajo DECISION-0057 (facultad de activar agentes), autorizado por el operador.

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$RuntimeDir = Join-Path $Root ".protocol-tmp\analista_mailbox_cron"
$LogPath = Join-Path $RuntimeDir "analista_mailbox_cron.log"
$PidPath = Join-Path $RuntimeDir "analista_mailbox_cron.pid"
$StopPath = Join-Path $RuntimeDir "analista_mailbox_cron.stop"
$LockPath = Join-Path $RuntimeDir "analista_mailbox_cron.lock"
$LeasePath = Join-Path $RuntimeDir "analista_mailbox_cron.exec-lease.json"
$SeenPath = Join-Path $RuntimeDir "analista_mailbox_cron.seen.json"
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
        owner = "Analista"
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
        Write-Log "SELF_HEAL_STALE_LOCK owner=Analista pid=$($lease.pid) message=$($lease.task_or_msg_id) state=$deadlineState"
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

function Get-AgentExecutable {
    if ($AgentExe -and (Test-Path -LiteralPath $AgentExe)) {
        return (Resolve-Path -LiteralPath $AgentExe).Path
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
    throw "agent executable (codex.exe) not found"
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

function Get-ProcessableAnalistaMessages {
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
        ($to -eq "Analista") -and
        ($status -in @("", "open")) -and
        (
            ($requires -match "^(true|yes)$") -or
            -not [string]::IsNullOrWhiteSpace($requested) -or
            ($type -in @("REVIEW", "REQUEST", "ACTION", "QUESTION", "DECISION"))
        ) -and
        ((-not $seen.ContainsKey($_.Name)) -or ($seen[$_.Name] -ne $signature))
    })
}

function Get-ArquitectoResponsesToAnalista {
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
            ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^to:\s*Analista\s*$")
        })
    }
    return @($matches)
}

function Test-ArquitectoStopOrder {
    $responses = Get-ArquitectoResponsesToAnalista
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

function Invoke-AnalistaForMessage {
    param([System.IO.FileInfo]$Message)
    Clear-StaleCronLockIfSafe
    if (Test-Path -LiteralPath $LockPath) {
        Write-Log "LOCKED skip $($Message.Name)"
        return
    }

    New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null
    $agentPath = Get-AgentExecutable
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
    $safeName = [IO.Path]::GetFileNameWithoutExtension($Message.Name)
    $stdoutPath = Join-Path $RunsDir "$stamp-$safeName.out.log"
    $stderrPath = Join-Path $RunsDir "$stamp-$safeName.err.log"
    $promptPath = Join-Path $RunsDir "$stamp-$safeName.prompt.txt"
    $messageRelative = $Message.FullName.Substring($Root.Length + 1).Replace("\", "/")

$prompt = @"
Eres el ANALISTA (firma 'Analista'): voz adversarial independiente / checker del repo
multi_agent_project_protocol. NO eres arquitecto, NI Codex, NI disenador. NO implementas, NO promueves,
NO cierras, NO consolidas, NO ratificas. Si te entregan un prompt de otro rol, NO lo asumes (rompe
maker != checker); ante ambiguedad, preguntas. Lee, en orden y sin asumir: AGENTS.md (sec 0 y 7), CLAUDE.md,
personal/Analista/STARTUP_PROMPT.md y personal/Analista/MEMORY.md.

Regla primordial: no narrar proceso. Solo emitir tu veredicto final o un bloqueo concreto.

Arranque obligatorio:
1. cd d:/Agentes/multi_agent_project_protocol ; git fetch origin. git status --short (no toques cambios ajenos).
2. Lee Area_comun/state/*.json con tolerancia a BOM (Codex escribe utf-8-sig BOM+CRLF).
3. Confirma canonico sano: python scripts/validate_collaboration_state.py (exit 0).

Mensaje a procesar en esta ejecucion (instruccion de REVIEW del Arquitecto, dirigida a ti):
$messageRelative

Modo REVISOR ADVERSARIAL obligatorio (tu veredicto GATEA el cierre, DECISION-0056):
1. Ancla SIEMPRE en canonico (el commit de producto y el HEAD del protocolo que cita la instruccion), NO en
   working tree.
2. CLON LIMPIO: clona el repo de producto (D:/Agentes/NOVA-Suite/NOVA) a un tmp, checkout del commit citado,
   y corre npm test AHI (NO in-place; leccion CRLF). Gatea por EXIT.
3. PRUEBA POR COMPORTAMIENTO cada vector/AC que la instruccion pide refutar: no confies en el nombre del test;
   ejercita TODA la familia que el AC promete (no solo el ejemplo). Extrae la funcion/guard y corre tus propios
   payloads. Intenta ROMPER cada garantia y busca un escape NUEVO; si lo hallas, documentalo falsable. Default a
   'no cerrable si dudas'.
4. GATES del protocolo: python scripts/validate_collaboration_state.py con Y sin secretos (exit 0); drift 0;
   python scripts/scan_domain_neutrality.py (exit 0); python scripts/scan_encoding.py (exit 0); #4 byte-identica.
5. EMITE veredicto (ASCII-only; tras escribir corre scan_encoding y arregla; para rr usa el texto 'rr=true',
   nunca el literal requires_response dos-puntos true en el cuerpo):
   - un ARTEFACTO en Area_comun/artifacts/ANALISTA-<tarea>-<tema>-veredicto.md (voz/firma Analista, ancla
     canonica, reproduccion con exit codes, tabla vector-por-vector PASA/SLIPS falsable, residuales declarados,
     RECOMENDACION DE CIERRE OK->CERRABLE o CAMBIO-REQUERIDO). El veredicto debe terminar con el envelope
     textual de 7 campos (no tool call): task_id, status, executive_summary, artifacts, gates, next_recommended,
     risks.
   - un MSG en Area_comun/mailbox/open/ to: Arquitecto type: REVIEW con requires_response (rr=true) que SIEMPRE
     incluya one_line_summary + requested_action + question (el validador EXIGE requested_action en mensajes rr;
     un veredicto sin requested_action deja el canonico ROJO).
6. COMMIT de tu veredicto (para que quede en canonico, no untracked): anti-colision primero (que Arquitecto/Codex
   no tengan claim activo sobre las rutas ni entrega a medias; si la hay, espera y reintenta el proximo disparo).
   Stagea RUTAS EXPLICITAS (tu artefacto + tu MSG), gatea por validate exit 0 + scan_encoding exit 0, commitea
   como Analista y git push origin main. Todo commit que toque rutas gobernadas debe emitir trailers finales:
   Task-Id: <TASK-XXXX> y, si corrige un hallazgo, Fixes-Task: <TASK-XXXX>. Si el commit es solo coordinacion sin
   tarea, usar Ops-Reason: <motivo>. NO commitees archivos de personal/Arquitecto ni personal/Codex.
7. MEMORIA (DECISION-0026): tras el commit, actualiza personal/Analista/MEMORY.md con el contexto del veredicto.
8. Si emites CAMBIO-REQUERIDO/NO-GO, declara el fix-loop esperado: remediacion, gates afectados, re-juicio previo
   al commit de cierre, maximo 2 iteraciones antes de escalar al operador.
9. Si no hay instruccion REVIEW pendiente para ti, no-op con cierre concreto (heartbeat). No implementes, no
   muto estado, no enciendas nada vivo. La parada a 7 rondas sin novedad sigue valida.
"@
    Write-Utf8NoBom -Path $promptPath -Content $prompt
    Write-Utf8NoBom -Path $LockPath -Content "$stamp $($Message.Name)`n"

    try {
        # El prompt se pasa por STDIN (RedirectStandardInput del archivo del prompt), NO como argumento:
        # Start-Process -ArgumentList parte un argumento multi-palabra en tokens sueltos (PS 5.1) y codex
        # interpreta la 2da palabra como subcomando. codex exec lee el prompt de stdin con '-'.
        $execArgs = @(
            "exec",
            "-s", "danger-full-access",
            "-c", "approval_policy=never",
            "-c", "model_reasoning_effort=$ReasoningEffort",
            "--skip-git-repo-check",
            "-"
        )
        $deadlineUtc = [DateTime]::UtcNow.AddSeconds($ExecTimeoutSeconds)
        $process = Start-Process -FilePath $agentPath -ArgumentList $execArgs -WorkingDirectory $Root -WindowStyle Hidden -PassThru -RedirectStandardInput $promptPath -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
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
Write-Log "Analista mailbox cron started. interval_seconds=$IntervalSeconds max_no_arquitecto_rounds=$MaxNoArquitectoRounds effort=$ReasoningEffort"

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

        $architectResponses = @(Get-ArquitectoResponsesToAnalista)
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

        $messages = @(Get-ProcessableAnalistaMessages)
        if ($messages.Count -eq 0) {
            Write-Log "Heartbeat processable_messages=0"
        } else {
            foreach ($message in $messages) {
                Invoke-AnalistaForMessage -Message $message
            }
        }
    } catch {
        Write-Log "LOOP_ERROR $($_.Exception.Message)"
    }

    Start-Sleep -Seconds $IntervalSeconds
}
