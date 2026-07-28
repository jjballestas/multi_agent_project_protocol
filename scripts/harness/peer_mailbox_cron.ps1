param(
    [Parameter(Mandatory = $true)][string]$PeerId,
    [string]$CoordinatorId = "Arquitecto",
    [string[]]$AcceptedTypes = @("GO", "REQUEST", "ACTION", "HANDOFF", "REVIEW", "QUESTION", "DECISION"),
    [string]$PromptFile = "",
    [string]$Root = "",
    [string]$AgentExe = "",
    [string[]]$AgentArgs = @(),
    [ValidateSet("Auto", "Anthropic", "Codex")][string]$AgentProvider = "Auto",
    [string]$ReasoningEffort = "medium",
    [int]$IntervalSeconds = 300,
    [int]$MaxNoCoordinatorRounds = 15,
    [int]$ExecTimeoutSeconds = 3600,
    [int]$PostDeliveryTimeoutSeconds = 300,
    [int]$ProgressFreshSeconds = 15,
    [int]$ProgressExtensionSeconds = 60,
    [int]$ProgressHardCapSeconds = 900,
    [int]$MaxTransientRetries = 3,
    [int]$RetryBackoffSeconds = 30,
    [int]$AbortedResidueMinutes = 5
)

# peer_mailbox_cron.ps1 -- generic launchable runtime for a protocol peer agent
# (implementer or reviewer). Shipped by the methodology as part of the instance
# operational layer; unifies the per-peer mirrors that the hub instance evolved
# (codex_mailbox_cron.ps1 / analista_mailbox_cron.ps1) into one parameterized runner.
#
# Contract:
# - The agent CLI is invoked once per processable mailbox message and MUST read its
#   prompt from STDIN (the runner redirects a rendered prompt file into it).
# - The prompt template ($PromptFile) MUST contain the runtime token @@MESSAGE_PATH@@;
#   optional tokens @@ROOT@@, @@PEER_ID@@ and @@COORDINATOR_ID@@ are also substituted.
#   (Runtime tokens use @@...@@ on purpose: {{...}} is reserved by the instancing renderer.)
# - Runtime state lives under <root>/.protocol-tmp/<peerid>_mailbox_cron/ and is CREATED
#   on first run (lock, pid, exec-lease, seen.json, runs/*.log). It is local runtime
#   state, never committed.
# - Stop protocols: (a) stop marker file <runtime-dir>/<peerid>_mailbox_cron.stop;
#   (b) a mailbox message from $CoordinatorId to $PeerId whose requested_action or
#   one_line_summary is EXACTLY "STOP_JOB" (case-sensitive equality; mere mentions of
#   stop words never trip it); (c) $MaxNoCoordinatorRounds rounds without coordinator
#   activity -> graceful exit.

$ErrorActionPreference = "Stop"

function ConvertTo-NormalizedRoot {
    param([string]$Path)
    # Trailing separators break downstream root-relative math (F1: Resolve-Path preserves
    # a trailing backslash, e.g. from tab completion). Normalize, but keep the 'D:\' form
    # for drive roots ('D:' alone would mean "current dir on D:").
    $normalized = $Path.TrimEnd('\', '/')
    if ($normalized -match '^[A-Za-z]:$') {
        $normalized += '\'
    }
    return $normalized
}

function Resolve-ProtocolRoot {
    param([string]$Explicit)
    if ($Explicit) {
        $resolved = ConvertTo-NormalizedRoot -Path (Resolve-Path -LiteralPath $Explicit).Path
        if (-not (Test-Path -LiteralPath (Join-Path $resolved "protocol.config.json"))) {
            throw "explicit -Root '$resolved' has no protocol.config.json"
        }
        return $resolved
    }
    $candidate = $PSScriptRoot
    for ($i = 0; $i -lt 8; $i++) {
        if (Test-Path -LiteralPath (Join-Path $candidate "protocol.config.json")) {
            return ConvertTo-NormalizedRoot -Path (Resolve-Path -LiteralPath $candidate).Path
        }
        $parent = Split-Path -Parent $candidate
        if (-not $parent -or $parent -eq $candidate) {
            break
        }
        $candidate = $parent
    }
    throw "could not locate protocol.config.json walking up from $PSScriptRoot; pass -Root explicitly"
}

$Root = Resolve-ProtocolRoot -Explicit $Root
$PeerLower = $PeerId.ToLowerInvariant()
$RuntimeDir = Join-Path $Root ".protocol-tmp\${PeerLower}_mailbox_cron"
$LogPath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.log"
$PidPath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.pid"
$StopPath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.stop"
$LockPath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.lock"
$LeasePath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.exec-lease.json"
$SeenPath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.seen.json"
$RetryPath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.retry.json"
$ResiduePath = Join-Path $RuntimeDir "${PeerLower}_mailbox_cron.residue-first-seen.json"
$RunsDir = Join-Path $RuntimeDir "runs"
$StartedAtUtc = [DateTime]::UtcNow
$NoCoordinatorRounds = 0
$AcceptedTypesUpper = @($AcceptedTypes | ForEach-Object { $_.ToUpperInvariant() })

if (-not $PromptFile) {
    $PromptFile = Join-Path $PSScriptRoot "prompts\${PeerLower}.prompt.md"
}
if (-not (Test-Path -LiteralPath $PromptFile)) {
    $promptsDir = Join-Path $PSScriptRoot "prompts"
    $available = ""
    if (Test-Path -LiteralPath $promptsDir) {
        $available = (Get-ChildItem -LiteralPath $promptsDir -File -Filter "*.prompt.md" | ForEach-Object { $_.Name }) -join ", "
    }
    throw "prompt file not found: $PromptFile (pass -PromptFile; shipped templates: $available)"
}
$PromptTemplate = Get-Content -LiteralPath $PromptFile -Raw -Encoding UTF8
# Ordinal case-SENSITIVE check to match String.Replace semantics exactly (F2: -notmatch is
# case-insensitive, so a template with @@message_path@@ would pass validation and then never
# get substituted).
if (-not $PromptTemplate.Contains("@@MESSAGE_PATH@@")) {
    throw "prompt template $PromptFile must contain the runtime token @@MESSAGE_PATH@@ (exact upper-case)"
}
foreach ($agentArg in $AgentArgs) {
    if ($null -eq $agentArg -or [string]::IsNullOrEmpty([string]$agentArg)) {
        # F5a: an empty element (e.g. an unset wrapper variable) would pass startup and then
        # fail Start-Process binding on EVERY exec, silently consuming the queue as seen.
        throw "-AgentArgs contains an empty element; check your launcher variables"
    }
}

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
        owner = $PeerId
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
        # Snapshot the complete descendant set before terminating the root. taskkill /T
        # normally handles this, but fast-exiting intermediates can re-parent grandchildren
        # before taskkill reaches them. The snapshot gives us a compensating sweep.
        $descendants = @()
        $pending = [System.Collections.Generic.Queue[int]]::new()
        $pending.Enqueue([int]$Lease.pid)
        $seenPids = @{}
        $childrenByParent = @{}
        foreach ($candidate in @(Get-CimInstance Win32_Process -ErrorAction Stop)) {
            if ($null -eq $candidate.ParentProcessId -or $null -eq $candidate.ProcessId) { continue }
            $candidateParent = [int]$candidate.ParentProcessId
            if (-not $childrenByParent.ContainsKey($candidateParent)) {
                $childrenByParent[$candidateParent] = @()
            }
            $childrenByParent[$candidateParent] += [int]$candidate.ProcessId
        }
        while ($pending.Count -gt 0) {
            $parentPid = $pending.Dequeue()
            if (-not $childrenByParent.ContainsKey($parentPid)) { continue }
            foreach ($childPid in @($childrenByParent[$parentPid])) {
                if (-not $seenPids.ContainsKey($childPid)) {
                    $seenPids[$childPid] = $true
                    $descendants += $childPid
                    $pending.Enqueue($childPid)
                }
            }
        }
        Write-Log "TREE_KILL pid=$($Lease.pid) reason=$Reason message=$($Lease.task_or_msg_id)"
        $killOrder = @($descendants)
        [array]::Reverse($killOrder)
        foreach ($childPid in $killOrder) {
            Stop-Process -Id $childPid -Force -ErrorAction SilentlyContinue
        }
        Stop-Process -Id ([int]$Lease.pid) -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 100
        if (Get-Process -Id ([int]$Lease.pid) -ErrorAction SilentlyContinue) {
            $taskkill = Start-Process -FilePath "taskkill.exe" -ArgumentList @("/PID", [string]$Lease.pid, "/T", "/F") -WindowStyle Hidden -Wait -PassThru
            if ($taskkill.ExitCode -ne 0) {
                Write-Log "TREE_KILL_FAIL pid=$($Lease.pid) error=taskkill_exit_$($taskkill.ExitCode)"
            }
        }
        $survivors = @($descendants | Where-Object { Get-Process -Id $_ -ErrorAction SilentlyContinue })
        if ($survivors.Count -gt 0) {
            Write-Log "TREE_KILL_INCOMPLETE pid=$($Lease.pid) survivors=$($survivors -join ',')"
            return $false
        }
        Write-Log "TREE_KILL_COMPLETE pid=$($Lease.pid) descendants=$($descendants.Count)"
        return (-not (Get-Process -Id ([int]$Lease.pid) -ErrorAction SilentlyContinue))
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
        Remove-Item -LiteralPath $LockPath -Force -ErrorAction SilentlyContinue
        Write-Log "SELF_HEAL_ORPHAN_LOCK owner=$PeerId reason=missing_lease"
        return
    }
    try {
        $lease = Get-Content -LiteralPath $LeasePath -Raw -Encoding UTF8 | ConvertFrom-Json
        $leaseMatches = Test-LeaseProcessMatches -Lease $lease
        $deadline = [DateTime]::Parse([string]$lease.deadline).ToUniversalTime()
        if ($leaseMatches) {
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
        Write-Log "SELF_HEAL_STALE_LOCK owner=$PeerId pid=$($lease.pid) message=$($lease.task_or_msg_id) state=$deadlineState"
    } catch {
        Write-Log "SELF_HEAL_FAIL error=$($_.Exception.Message)"
    }
}

function Get-ExecProgressState {
    param(
        $Lease,
        [string]$StdoutPath,
        [string]$StderrPath,
        [string]$EventsPath,
        [long]$PreviousOutputBytes,
        [long]$PreviousLedgerBytes,
        [int]$FreshSeconds
    )
    $outputBytes = 0L
    foreach ($path in @($StdoutPath, $StderrPath)) {
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            $outputBytes += [long](Get-Item -LiteralPath $path).Length
        }
    }
    $ledgerBytes = if (Test-Path -LiteralPath $EventsPath -PathType Leaf) {
        [long](Get-Item -LiteralPath $EventsPath).Length
    } else { 0L }
    $heartbeatFresh = $false
    if ($Lease -and $null -ne $Lease.heartbeat_monotonic) {
        $elapsedTicks = [System.Diagnostics.Stopwatch]::GetTimestamp() - [long]$Lease.heartbeat_monotonic
        $heartbeatAgeSeconds = [double]$elapsedTicks / [double][System.Diagnostics.Stopwatch]::Frequency
        $heartbeatFresh = ($heartbeatAgeSeconds -ge 0 -and $heartbeatAgeSeconds -le $FreshSeconds)
    }
    $reasons = @()
    if ($heartbeatFresh) { $reasons += "heartbeat_fresh" }
    if ($outputBytes -gt $PreviousOutputBytes) { $reasons += "run_log_growing" }
    if ($ledgerBytes -gt $PreviousLedgerBytes) { $reasons += "ledger_growing" }
    return [pscustomobject]@{
        progressing = ($reasons.Count -gt 0)
        reasons = ($reasons -join ",")
        output_bytes = $outputBytes
        ledger_bytes = $ledgerBytes
    }
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
    if ($AgentExe -and (Test-Path -LiteralPath $AgentExe -PathType Leaf)) {
        # -PathType Leaf (F5b): a directory path must not pass startup only to explode on exec.
        return (Resolve-Path -LiteralPath $AgentExe).Path
    }
    if ($AgentExe) {
        $fromPath = Get-Command $AgentExe -ErrorAction SilentlyContinue
        if ($fromPath -and $fromPath.Source -and (Test-Path -LiteralPath $fromPath.Source -PathType Leaf)) {
            return $fromPath.Source
        }
        throw "agent executable not found (or not a file): $AgentExe"
    }
    $commandName = if ($AgentProvider -eq "Anthropic") { "claude" } else { "codex" }
    $cmd = Get-Command $commandName -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -and (Test-Path -LiteralPath $cmd.Source)) {
        if ($AgentProvider -eq "Anthropic") {
            return (Resolve-Path -LiteralPath $cmd.Source).Path
        }
        $content = Get-Content -LiteralPath $cmd.Source -Raw -ErrorAction SilentlyContinue
        $match = [regex]::Match($content, '"([^"]*codex\.exe)"')
        if ($match.Success -and (Test-Path -LiteralPath $match.Groups[1].Value)) {
            return $match.Groups[1].Value
        }
    }
    # where.exe writing to stderr under ErrorActionPreference=Stop raises a terminating
    # NativeCommandError when nothing is found (F8, inherited from the hub originals),
    # which used to dead-code the discovery fallbacks below. Contain it.
    $whereResults = @()
    try {
        $whereResults = @(& where.exe codex 2>$null)
    } catch {
        $whereResults = @()
    }
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
    throw "agent executable not found (provider=$AgentProvider; no usable -AgentExe)"
}

function Get-AgentArguments {
    if ($AgentArgs.Count -gt 0) {
        return $AgentArgs
    }
    if ($AgentProvider -eq "Anthropic") {
        return @("-p", "--permission-mode", "bypassPermissions", "--output-format", "text")
    }
    # Default arguments for the reference agent (codex CLI): read the prompt from STDIN
    # ('-'). Any replacement CLI must honor the same STDIN contract.
    return @(
        "exec",
        "-s", "danger-full-access",
        "-c", "approval_policy=never",
        "-c", "model_reasoning_effort=$ReasoningEffort",
        "--skip-git-repo-check",
        "-"
    )
}

function Get-AgentInvocation {
    param([string]$AgentPath, [string[]]$Arguments)
    $extension = [IO.Path]::GetExtension($AgentPath).ToLowerInvariant()
    if ($extension -eq ".ps1") {
        return @{ FilePath = (Get-Command powershell.exe -ErrorAction Stop).Source; Arguments = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $AgentPath) + $Arguments }
    }
    if ($extension -in @(".cmd", ".bat")) {
        return @{ FilePath = (Get-Command cmd.exe -ErrorAction Stop).Source; Arguments = @("/d", "/s", "/c", $AgentPath) + $Arguments }
    }
    return @{ FilePath = $AgentPath; Arguments = $Arguments }
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

function Read-RetryState {
    if (-not (Test-Path -LiteralPath $RetryPath)) { return @{} }
    try {
        $json = Get-Content -LiteralPath $RetryPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $state = @{}
        foreach ($prop in $json.PSObject.Properties) { $state[$prop.Name] = $prop.Value }
        return $state
    } catch { return @{} }
}

function Write-RetryState {
    param([hashtable]$State)
    $object = [ordered]@{}
    foreach ($key in ($State.Keys | Sort-Object)) { $object[$key] = $State[$key] }
    Write-Utf8NoBom -Path $RetryPath -Content (($object | ConvertTo-Json -Depth 8) + "`n")
}

function Get-FilePrefixSha256 {
    param([string]$Path, [long]$Length)
    if ($Length -lt 0) { return $null }
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $stream = $null
    try {
        $stream = [System.IO.File]::Open($Path, 'Open', 'Read', 'ReadWrite')
        if ($stream.Length -lt $Length) { return $null }
        $buffer = New-Object byte[] 65536
        $remaining = $Length
        while ($remaining -gt 0) {
            $wanted = [int][Math]::Min([long]$buffer.Length, $remaining)
            $read = $stream.Read($buffer, 0, $wanted)
            if ($read -le 0) { return $null }
            [void]$sha.TransformBlock($buffer, 0, $read, $null, 0)
            $remaining -= $read
        }
        [void]$sha.TransformFinalBlock((New-Object byte[] 0), 0, 0)
        return ([BitConverter]::ToString($sha.Hash).Replace('-', '').ToLowerInvariant())
    } finally {
        if ($stream) { $stream.Dispose() }
        $sha.Dispose()
    }
}

function Get-OwnEvidence {
    param([long]$LedgerBytesBefore, [string]$LedgerPrefixSha256Before)
    $eventsPath = Join-Path $Root "runtime\state\events.jsonl"
    if (-not (Test-Path -LiteralPath $eventsPath)) { return $false }
    $currentLength = (Get-Item -LiteralPath $eventsPath).Length
    if ($currentLength -le $LedgerBytesBefore) { return $false }
    $prefixNow = Get-FilePrefixSha256 -Path $eventsPath -Length $LedgerBytesBefore
    if (-not $prefixNow -or $prefixNow -cne $LedgerPrefixSha256Before) {
        Write-Log "EVIDENCE_UNAVAILABLE reason=ledger_not_pure_append"
        return $false
    }
    $stream = [System.IO.File]::Open($eventsPath, 'Open', 'Read', 'ReadWrite')
    try {
        [void]$stream.Seek($LedgerBytesBefore, 'Begin')
        $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8, $true, 4096, $true)
        try { $tail = $reader.ReadToEnd() } finally { $reader.Dispose() }
    } finally {
        $stream.Dispose()
    }
    foreach ($line in @($tail -split "\r?\n")) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $event = $line | ConvertFrom-Json } catch { continue }
        if ([string]$event.actor -cne $PeerId) { continue }
        if ($event.applied -ne $true) { continue }
        if ([string]$event.actor_auth.method -cne "ed25519") { continue }
        $expectedKeyPrefix = $PeerId.ToLowerInvariant() + ":"
        if (-not ([string]$event.actor_auth.keyid).StartsWith($expectedKeyPrefix, [StringComparison]::Ordinal)) { continue }
        if ([string]::IsNullOrWhiteSpace([string]$event.actor_auth.sig)) { continue }
        $intentType = [string]$event.payload.intent_type
        $hasUsefulIntent = $intentType -in @("task_status", "task_upsert", "decision")
        if (-not $hasUsefulIntent) { continue }
        return $true
    }
    return $false
}

function Get-OwnDeliveryEvidence {
    param([long]$LedgerBytesBefore, [string]$LedgerPrefixSha256Before)
    $eventsPath = Join-Path $Root "runtime\state\events.jsonl"
    if (-not (Test-Path -LiteralPath $eventsPath)) { return $false }
    $currentLength = (Get-Item -LiteralPath $eventsPath).Length
    if ($currentLength -le $LedgerBytesBefore) { return $false }
    $prefixNow = Get-FilePrefixSha256 -Path $eventsPath -Length $LedgerBytesBefore
    if (-not $prefixNow -or $prefixNow -cne $LedgerPrefixSha256Before) { return $false }
    $stream = [System.IO.File]::Open($eventsPath, 'Open', 'Read', 'ReadWrite')
    try {
        [void]$stream.Seek($LedgerBytesBefore, 'Begin')
        $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8, $true, 4096, $true)
        try { $tail = $reader.ReadToEnd() } finally { $reader.Dispose() }
    } finally { $stream.Dispose() }
    $taskIndexResult = Read-JsonWithDeadline -Path (Join-Path $Root "Area_comun\state\TASK_INDEX.json")
    if (-not $taskIndexResult.ok) { return $false }
    foreach ($line in @($tail -split "\r?\n")) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $event = $line | ConvertFrom-Json } catch { continue }
        if ([string]$event.actor -cne $PeerId -or $event.applied -ne $true) { continue }
        if ([string]$event.actor_auth.method -cne "ed25519") { continue }
        $expectedKeyPrefix = $PeerId.ToLowerInvariant() + ":"
        if (-not ([string]$event.actor_auth.keyid).StartsWith($expectedKeyPrefix, [StringComparison]::Ordinal)) { continue }
        if ([string]::IsNullOrWhiteSpace([string]$event.actor_auth.sig)) { continue }
        if ([string]$event.payload.intent_type -cne "task_status") { continue }
        if ([string]$event.payload.transitions.task_status.to -cne "in_review") { continue }
        $taskId = [string]$event.payload.task_id
        $owned = @($taskIndexResult.value.tasks | Where-Object { [string]$_.id -ceq $taskId -and [string]$_.owner -ceq $PeerId })
        if ($owned.Count -gt 0) { return $true }
    }
    return $false
}

function Get-LedgerHead {
    $helper = Join-Path $Root "scripts\ledger_head.py"
    $previousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try { $raw = & python $helper --root $Root 2>$null; $exitCode = $LASTEXITCODE }
    finally { $ErrorActionPreference = $previousErrorAction }
    if ($exitCode -ne 0) { return [pscustomobject]@{ readable = $false; seq = $null; hash = ""; torn_tail = $false } }
    try {
        $head = $raw | ConvertFrom-Json
        $head | Add-Member -NotePropertyName readable -NotePropertyValue $true
        return $head
    } catch {
        return [pscustomobject]@{ readable = $false; seq = 0; hash = ""; torn_tail = $false }
    }
}

function Get-GitStatusPorcelainUtf8 {
    $start = New-Object System.Diagnostics.ProcessStartInfo
    $start.FileName = "git"
    $start.WorkingDirectory = $Root
    $start.Arguments = "status --porcelain=v1 -z --untracked-files=all"
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.StandardOutputEncoding = New-Object System.Text.UTF8Encoding($false, $true)
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) { return [pscustomobject]@{ ok = $false; raw = "" } }
        # Drain both pipes concurrently. Sequential ReadToEnd deadlocks when either
        # redirected pipe fills before the other one is drained.
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit(10000)) {
            try { $process.Kill() } catch {}
            return [pscustomobject]@{ ok = $false; raw = ""; reason = "timeout" }
        }
        if (-not [System.Threading.Tasks.Task]::WaitAll(@($stdoutTask, $stderrTask), 10000)) {
            return [pscustomobject]@{ ok = $false; raw = ""; reason = "drain_timeout" }
        }
        $raw = $stdoutTask.Result
        return [pscustomobject]@{ ok = ($process.ExitCode -eq 0); raw = $raw }
    } catch {
        return [pscustomobject]@{ ok = $false; raw = "" }
    } finally {
        $process.Dispose()
    }
}

function Get-WorktreeDiskProof {
    $statusResult = Get-GitStatusPorcelainUtf8
    if (-not $statusResult.ok) { return $null }
    $raw = [string]$statusResult.raw
    $rows = @()
    foreach ($entry in @($raw -split [char]0 | Where-Object { $_ })) {
        if ($entry.Length -lt 4) { return $null }
        $path = $entry.Substring(3).Replace("\", "/")
        if ($path -match ' -> ') { $path = ($path -split ' -> ', 2)[1] }
        $full = Join-Path $Root $path
        if (Test-Path -LiteralPath $full -PathType Leaf) {
            $item = Get-Item -LiteralPath $full
            $hash = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant()
            $rows += [ordered]@{ path = $path; exists = $true; length = [long]$item.Length; sha256 = $hash }
        } else {
            $rows += [ordered]@{ path = $path; exists = $false; length = 0; sha256 = "" }
        }
    }
    return (($rows | Sort-Object { $_.path } | ConvertTo-Json -Compress -Depth 4))
}

function Get-StagedResidueState {
    $statusResult = Get-GitStatusPorcelainUtf8
    if (-not $statusResult.ok) { return "unknown" }
    $statusRaw = [string]$statusResult.raw
    if ([string]::IsNullOrEmpty($statusRaw)) {
        if (Test-Path -LiteralPath $ResiduePath) { Remove-Item -LiteralPath $ResiduePath -Force -ErrorAction SilentlyContinue }
        return "none"
    }
    $status = @($statusRaw -split [char]0 | Where-Object { $_ })
    $cutoff = [DateTime]::UtcNow.AddMinutes(-$AbortedResidueMinutes)
    $firstSeen = @{}
    if (Test-Path -LiteralPath $ResiduePath) {
        try {
            $stored = Get-Content -LiteralPath $ResiduePath -Raw -Encoding UTF8 | ConvertFrom-Json
            foreach ($property in $stored.PSObject.Properties) { $firstSeen[$property.Name] = [string]$property.Value }
        } catch { return "unknown" }
    }
    $nextSeen = @{}
    for ($index = 0; $index -lt $status.Count; $index++) {
        $row = $status[$index]
        if ($row.Length -lt 4) { return "unknown" }
        $relative = $row.Substring(3)
        $full = Join-Path $Root $relative
        $now = [DateTime]::UtcNow
        $observed = $now
        if ($firstSeen.ContainsKey($relative)) {
            try { $observed = [DateTime]::Parse($firstSeen[$relative]).ToUniversalTime() } catch { return "unknown" }
        } elseif (Test-Path -LiteralPath $full) {
            $observed = (Get-Item -LiteralPath $full).LastWriteTimeUtc
        }
        $nextSeen[$relative] = $observed.ToString("o")
        if ($observed -gt $cutoff) {
            Write-Utf8NoBom -Path $ResiduePath -Content (($nextSeen | ConvertTo-Json -Depth 4) + "`n")
            return "live"
        }
        if ($row.Substring(0, 2) -match '[RC]') { $index++ }
    }
    Write-Utf8NoBom -Path $ResiduePath -Content (($nextSeen | ConvertTo-Json -Depth 4) + "`n")
    return "aborted"
}

function Read-JsonWithDeadline {
    param([string]$Path, [int]$TimeoutMilliseconds = 2000)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return [pscustomobject]@{ ok = $true; value = $null }
    }
    $deadline = [DateTime]::UtcNow.AddMilliseconds($TimeoutMilliseconds)
    do {
        try {
            $raw = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
            return [pscustomobject]@{ ok = $true; value = ($raw | ConvertFrom-Json) }
        } catch {
            Start-Sleep -Milliseconds 25
        }
    } while ([DateTime]::UtcNow -lt $deadline)
    return [pscustomobject]@{ ok = $false; value = $null }
}

function Get-AdditionalWorkSignal {
    # Claims and live peer leases reinforce a defer. Their absence is never used
    # as permission to override the dirty-tree veto.
    $claimsResult = Read-JsonWithDeadline -Path (Join-Path $Root "Area_comun\state\CLAIMS.json")
    if (-not $claimsResult.ok) { return "claims_unreadable" }
    $now = [DateTime]::UtcNow
    foreach ($claim in @($claimsResult.value.claims)) {
        if ([string]$claim.owner -eq $PeerId -or [string]$claim.status -eq "released") { continue }
        try { $expires = [DateTime]::Parse([string]$claim.expires_at).ToUniversalTime() } catch { continue }
        if ($expires -gt $now) { return "active_external_claim" }
    }
    $tmpRoot = Join-Path $Root ".protocol-tmp"
    foreach ($leaseFile in @(Get-ChildItem -LiteralPath $tmpRoot -Recurse -File -Filter "*.exec-lease.json" -ErrorAction SilentlyContinue)) {
        if ($leaseFile.FullName -eq $LeasePath) { continue }
        $leaseResult = Read-JsonWithDeadline -Path $leaseFile.FullName
        if (-not $leaseResult.ok) { return "peer_lease_unreadable" }
        if (Test-LeaseProcessMatches -Lease $leaseResult.value) { return "active_peer_lease" }
    }
    return "none"
}

function Register-PreExecDefer {
    param([System.IO.FileInfo]$Message, [string]$Reason, [string]$Outcome = "deferred")
    $signature = Get-MessageSignature -Message $Message
    $retry = Read-RetryState
    $same = $retry.ContainsKey($Message.Name) -and ([string]$retry[$Message.Name].signature -eq $signature)
    $attempts = if ($same -and $null -ne $retry[$Message.Name].attempts) { [int]$retry[$Message.Name].attempts } else { 0 }
    $defers = if ($same -and $null -ne $retry[$Message.Name].defers) { [int]$retry[$Message.Name].defers + 1 } else { 1 }
    $terminal = ($defers -ge $MaxTransientRetries)
    $effectiveOutcome = if ($terminal) { "defer_terminal" } else { $Outcome }
    $retry[$Message.Name] = [ordered]@{ signature = $signature; attempts = $attempts; defers = $defers; exhausted = $terminal; outcome = $effectiveOutcome; reason = $Reason; updated_at = [DateTime]::UtcNow.ToString("o") }
    Write-RetryState -State $retry
    if ($defers -ge $MaxTransientRetries) {
        Write-Log "RETRY_EXHAUSTED defers=$defers attempts=$attempts signal=watchdog outcome=defer_terminal reason=$Reason message=$($Message.Name)"
    } else {
        Write-Log "RETRY_DEFER defer=$defers max=$MaxTransientRetries reason=$Reason message=$($Message.Name)"
        if ($RetryBackoffSeconds -gt 0) { Start-Sleep -Seconds $RetryBackoffSeconds }
    }
}

function Test-LedgerManagedPath {
    param([string]$Path)
    $normalized = $Path.Replace("\", "/")
    return ($normalized -like "runtime/state/*") -or
        ($normalized -like "Area_comun/state/*") -or
        ($normalized -like "Area_comun/tasks/*") -or
        ($normalized -like "Area_comun/mailbox/*")
}

function Invoke-PreExecPatch {
    param([string]$PatchPath, [bool]$Index, [string[]]$ExcludePaths = @())
    if (-not (Test-Path $PatchPath) -or (Get-Item $PatchPath).Length -eq 0) { return }
    $args = @("-C", $Root, "apply")
    if ($Index) { $args += "--cached" }
    $args += "--binary"
    foreach ($path in $ExcludePaths) {
        $args += "--exclude=$path"
    }
    $args += $PatchPath
    & git @args 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "APPLY_FAIL index=$Index patch=$PatchPath exit=$LASTEXITCODE"
    }
}

function Test-LedgerDerivedState {
    $probe = "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; raise SystemExit(1 if protocol_state_drift(Path(r'$($Root.Replace("'", "''"))'))['has_drift'] else 0)"
    & python -c $probe 2>$null
    return $LASTEXITCODE -eq 0
}

function Restore-TransientExecResidue {
    param([string]$HeadBefore, [string]$IndexPatch, [string[]]$UntrackedBefore, [object]$LedgerHeadBefore)
    trap {
        Write-Log "ROLLBACK_DEFER reason=rollback_probe_failed"
        return
    }
    $headAfter = (& git -C $Root rev-parse HEAD 2>$null | Select-Object -First 1)
    if ($headAfter -ne $HeadBefore) { Write-Log "ROLLBACK_DEFER reason=head_changed"; return }
    if (-not [bool]$LedgerHeadBefore.readable) { Write-Log "ROLLBACK_DEFER reason=ledger_unreadable_before_exec"; return }
    $ledgerHeadAfter = Get-LedgerHead
    if (-not [bool]$ledgerHeadAfter.readable) { Write-Log "ROLLBACK_DEFER reason=ledger_unreadable_after_exec"; return }
    if ([bool]$ledgerHeadAfter.torn_tail) { Write-Log "ROLLBACK_DEFER reason=ledger_torn_tail"; return }
    $ledgerAdvanced = ([long]$ledgerHeadAfter.seq -ne [long]$LedgerHeadBefore.seq) -or ([string]$ledgerHeadAfter.hash -cne [string]$LedgerHeadBefore.hash)
    if ($ledgerAdvanced) {
        # An applied signed event makes ownership ambiguous. Preserve the complete
        # post-exec tree; never infer safe rollback from event kinds or path lists.
        $proofBefore = Get-WorktreeDiskProof
        if ($null -eq $proofBefore) { Write-Log "ROLLBACK_DEFER reason=disk_proof_failed"; return }
        $ledgerHeadVerified = Get-LedgerHead
        $proofAfter = Get-WorktreeDiskProof
        if (-not [bool]$ledgerHeadVerified.readable -or
            [long]$ledgerHeadVerified.seq -ne [long]$ledgerHeadAfter.seq -or
            [string]$ledgerHeadVerified.hash -cne [string]$ledgerHeadAfter.hash -or
            $null -eq $proofAfter -or $proofAfter -cne $proofBefore) {
            Write-Log "ROLLBACK_LEDGER_DRIFT reason=disk_verification_failed seq_before=$($LedgerHeadBefore.seq) seq_after=$($ledgerHeadAfter.seq)"
            return
        }
        if (-not (Test-LedgerDerivedState)) { Write-Log "ROLLBACK_LEDGER_DRIFT reason=derived_state_mismatch seq_before=$($LedgerHeadBefore.seq) seq_after=$($ledgerHeadAfter.seq)"; return }
        Write-Log "ROLLBACK_LEDGER_PRESERVED seq_before=$($LedgerHeadBefore.seq) seq_after=$($ledgerHeadAfter.seq) proof=disk"
        return
    }
    # Restore only the pre-exec index before any filesystem movement. The shared
    # worktree is never reset or re-applied.
    & git -C $Root read-tree $HeadBefore 2>$null
    if ($LASTEXITCODE -ne 0) { Write-Log "ROLLBACK_DEFER reason=index_unstage_failed"; return }
    Invoke-PreExecPatch -PatchPath $IndexPatch -Index $true
    if ($LASTEXITCODE -ne 0) { Write-Log "ROLLBACK_DEFER reason=index_restore_failed"; return }
    $beforeUntracked = @{}; foreach ($path in $UntrackedBefore) { $beforeUntracked[$path] = $true }
    $createdRaw = @(& git -C $Root ls-files --others --exclude-standard -z 2>$null) -join ""
    if ($LASTEXITCODE -ne 0) { Write-Log "ROLLBACK_DEFER reason=untracked_enumeration_failed"; return }
    $quarantineId = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffffffZ')
    $quarantineRoot = Join-Path $Root ".protocol-tmp\rollback-quarantine\$quarantineId"
    foreach ($path in @($createdRaw -split [char]0 | Where-Object { $_ -and -not $beforeUntracked.ContainsKey($_) })) {
        if (Test-LedgerManagedPath -Path $path) { continue }
        $full = Join-Path $Root $path
        if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { continue }
        try {
            $destination = Join-Path $quarantineRoot $path
            $parent = Split-Path -Parent $destination
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
            Move-Item -LiteralPath $full -Destination $destination -ErrorAction Stop
            $quarantineRelative = ".protocol-tmp/rollback-quarantine/$quarantineId/$($path.Replace('\', '/'))"
            Write-Log "ROLLBACK_QUARANTINED path=$path quarantine_path=$quarantineRelative"
        } catch { Write-Log "ROLLBACK_DEFER reason=quarantine_move_failed path=$path" }
    }
}

function Get-ExecOutcomeClass {
    param([int]$ExitCode, [string]$AgentResponse, [string]$InvokerDiagnostics = "", [bool]$OwnEvidence)
    # Only stdout is the agent response. Invoker diagnostics/epilogues and echoed prompts
    # live on stderr for the supported CLIs and must never influence message consumption.
    $lastLine = @($AgentResponse -split "\r?\n" | Where-Object { $_ -notmatch '^\s*$' } | Select-Object -Last 1)
    if ($lastLine.Count -eq 1 -and $lastLine[0] -cmatch '^OUTCOME: (confirmed|transient|definitive)$') { return $Matches[1] }
    if ($ExitCode -ne 0) { return "transient" }
    if ($OwnEvidence) { return "confirmed" }
    # Free text can request a retry, but can never consume a message definitively.
    if ($AgentResponse -match '(?im)(pre-gate|precondition|claim ajeno|active claim|ventana (roja|ocupada)|tree.*(dirty|peer)|cambios ajenos|staged residue|resource deadlock)') {
        return "transient"
    }
    return "unconfirmed"
}

function Get-MessageSignature {
    param([System.IO.FileInfo]$Message)
    return "$($Message.Name)|$($Message.Length)|$($Message.LastWriteTimeUtc.Ticks)"
}

function Get-ProcessablePeerMessages {
    $openDir = Join-Path $Root "Area_comun\mailbox\open"
    if (-not (Test-Path -LiteralPath $openDir)) {
        return @()
    }
    $seen = Read-Seen
    $retry = Read-RetryState
    @(Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md" | Where-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
        $to = Get-Field -Content $content -Name "to"
        $status = Get-Field -Content $content -Name "status"
        $requires = Get-Field -Content $content -Name "requires_response"
        $type = (Get-Field -Content $content -Name "type").ToUpperInvariant()
        $requested = Get-Field -Content $content -Name "requested_action"
        $signature = Get-MessageSignature -Message $_
        ($to -eq $PeerId) -and
        ($status -in @("", "open")) -and
        (
            ($requires -match "^(true|yes)$") -or
            -not [string]::IsNullOrWhiteSpace($requested) -or
            ($type -in $AcceptedTypesUpper)
        ) -and
        ((-not $seen.ContainsKey($_.Name)) -or ($seen[$_.Name] -ne $signature)) -and
        ((-not $retry.ContainsKey($_.Name)) -or ([string]$retry[$_.Name].signature -ne $signature) -or (-not [bool]$retry[$_.Name].exhausted))
    })
}

function Get-CoordinatorResponsesToPeer {
    $mailboxRoot = Join-Path $Root "Area_comun\mailbox"
    $folders = @("open", "answered", "archived")
    $found = @()
    foreach ($folder in $folders) {
        $dir = Join-Path $mailboxRoot $folder
        if (-not (Test-Path -LiteralPath $dir)) {
            continue
        }
        $found += @(Get-ChildItem -LiteralPath $dir -File -Filter "MSG-*.md" | Where-Object {
            $_.LastWriteTimeUtc -ge $StartedAtUtc -and
            ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^from:\s*$([regex]::Escape($CoordinatorId))\s*$") -and
            ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^to:\s*$([regex]::Escape($PeerId))\s*$")
        })
    }
    return @($found)
}

function Test-CoordinatorStopOrder {
    $responses = Get-CoordinatorResponsesToPeer
    foreach ($response in $responses) {
        $content = Get-Content -LiteralPath $response.FullName -Raw -Encoding UTF8
        $requested = Get-Field -Content $content -Name "requested_action"
        $summary = Get-Field -Content $content -Name "one_line_summary"
        # Hardened stop detector: ONLY the exact token STOP_JOB stops the agent (no
        # ambiguity). Case-sensitive equality, and only in summary/requested_action --
        # never the body -- so mere mentions of stop words cannot trip the cron.
        if (($requested.Trim() -ceq "STOP_JOB") -or ($summary.Trim() -ceq "STOP_JOB")) {
            return $true
        }
    }
    return $false
}

function Invoke-PeerForMessage {
    param([System.IO.FileInfo]$Message)
    Clear-StaleCronLockIfSafe
    if (Test-Path -LiteralPath $LockPath) {
        Write-Log "LOCKED skip $($Message.Name)"
        return
    }
    # Pre-gate before taking the exec lock. A failed/slow probe retains the launch
    # and cannot strand a lock owned by no process.
    $residueState = Get-StagedResidueState
    if ($residueState -eq "unknown") {
        Register-PreExecDefer -Message $Message -Reason "residue_probe_failed"
        return
    }
    if ($residueState -eq "live") {
        Register-PreExecDefer -Message $Message -Reason "worktree_residue_live"
        return
    }
    if ($residueState -eq "aborted") {
        Write-Log "RETRY_TRANSIENT reason=staged_residue_aborted age_minutes=$AbortedResidueMinutes message=$($Message.Name)"
    }
    $additionalSignal = Get-AdditionalWorkSignal
    if ($additionalSignal -ne "none") {
        Register-PreExecDefer -Message $Message -Reason $additionalSignal
        return
    }
    New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null
    $agentPath = $ResolvedAgentPath
    $execArgs = Get-AgentArguments
    $invocation = Get-AgentInvocation -AgentPath $agentPath -Arguments $execArgs
    $execArgs = @($invocation.Arguments)
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
    $safeName = [IO.Path]::GetFileNameWithoutExtension($Message.Name)
    $stdoutPath = Join-Path $RunsDir "$stamp-$safeName.out.log"
    $stderrPath = Join-Path $RunsDir "$stamp-$safeName.err.log"
    $promptPath = Join-Path $RunsDir "$stamp-$safeName.prompt.txt"
    # Root-relative path computed by trimming separators, not by +1 arithmetic (F1: a root
    # normalized to 'D:\' or any residual trailing separator must not eat the first char).
    $messageRelative = $Message.FullName.Substring($Root.Length).TrimStart('\', '/').Replace("\", "/")

    $prompt = $PromptTemplate.Replace("@@MESSAGE_PATH@@", $messageRelative)
    $prompt = $prompt.Replace("@@ROOT@@", $Root.Replace("\", "/"))
    $prompt = $prompt.Replace("@@PEER_ID@@", $PeerId)
    $prompt = $prompt.Replace("@@COORDINATOR_ID@@", $CoordinatorId)
    $prompt += "`n`nEnd the final response with exactly one structured outcome line: OUTCOME: confirmed, OUTCOME: transient, or OUTCOME: definitive. This exact token is authoritative; prose is not.`n"

    Write-Utf8NoBom -Path $promptPath -Content $prompt
    $indexPatch = Join-Path $RunsDir "$stamp-$safeName.before-index.patch"
    $ledgerHeadBefore = $null
    $headBefore = ""
    $untrackedBefore = @()
    try {
        Write-Utf8NoBom -Path $LockPath -Content "$stamp $($Message.Name)`n"
        $headBefore = (& git -C $Root rev-parse HEAD 2>$null | Select-Object -First 1)
        $ledgerHeadBefore = Get-LedgerHead
        if (-not [bool]$ledgerHeadBefore.readable) { Register-PreExecDefer -Message $Message -Reason "ledger_unreadable_before_exec"; return }
        $eventsPath = Join-Path $Root "runtime\state\events.jsonl"
        $ledgerBytesBefore = if (Test-Path -LiteralPath $eventsPath) { [long](Get-Item -LiteralPath $eventsPath).Length } else { 0 }
        $ledgerPrefixSha256Before = if (Test-Path -LiteralPath $eventsPath) { Get-FilePrefixSha256 -Path $eventsPath -Length $ledgerBytesBefore } else { "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" }
        if (-not $ledgerPrefixSha256Before) { Register-PreExecDefer -Message $Message -Reason "ledger_prefix_snapshot_failed"; return }
        & git -C $Root diff --cached --binary --output=$indexPatch
        if ($LASTEXITCODE -ne 0) { Register-PreExecDefer -Message $Message -Reason "index_snapshot_failed"; return }
        $untrackedBeforeRaw = @(& git -C $Root ls-files --others --exclude-standard -z 2>$null) -join ""
        if ($LASTEXITCODE -ne 0) { Register-PreExecDefer -Message $Message -Reason "untracked_snapshot_failed"; return }
        $untrackedBefore = @($untrackedBeforeRaw -split [char]0 | Where-Object { $_ })
        # The prompt goes through STDIN (RedirectStandardInput of the rendered prompt
        # file), NOT as an argument: Start-Process -ArgumentList splits a multi-word
        # argument into loose tokens (PS 5.1) and CLIs may misread the second word as a
        # subcommand. The reference agent (codex exec) reads the prompt from stdin via '-'.
        $deadlineUtc = [DateTime]::UtcNow.AddSeconds($ExecTimeoutSeconds)
        $process = Start-Process -FilePath $invocation.FilePath -ArgumentList $execArgs -WorkingDirectory $Root -WindowStyle Hidden -PassThru -RedirectStandardInput $promptPath -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
        $null = $process.Handle  # cache the handle or ExitCode reads null when the exec finishes before the first WaitForExit
        Write-ExecLease -Process $process -MessageName $Message.Name -Arguments $execArgs -DeadlineUtc $deadlineUtc
        Write-Log "EXEC_START pid=$($process.Id) message=$($Message.Name)"
        $postDeliveryDeadlineUtc = $null
        $postDeliveryHardDeadlineUtc = $null
        $execHardDeadlineUtc = $deadlineUtc.AddSeconds($ProgressHardCapSeconds)
        $eventsPath = Join-Path $Root "runtime\state\events.jsonl"
        $progressOutputBytes = 0L
        foreach ($progressPath in @($stdoutPath, $stderrPath)) {
            if (Test-Path -LiteralPath $progressPath -PathType Leaf) { $progressOutputBytes += [long](Get-Item -LiteralPath $progressPath).Length }
        }
        $progressLedgerBytes = if (Test-Path -LiteralPath $eventsPath -PathType Leaf) { [long](Get-Item -LiteralPath $eventsPath).Length } else { 0L }
        while (-not $process.WaitForExit(1000)) {
            Update-ExecLeaseHeartbeat
            if (Test-Path -LiteralPath $StopPath) {
                Write-Log "Stop marker detected; waiting for current exec pid=$($process.Id)"
            }
            if ([DateTime]::UtcNow -gt $deadlineUtc) {
                $lease = Get-Content -LiteralPath $LeasePath -Raw -Encoding UTF8 | ConvertFrom-Json
                $progress = Get-ExecProgressState -Lease $lease -StdoutPath $stdoutPath -StderrPath $stderrPath -EventsPath $eventsPath -PreviousOutputBytes $progressOutputBytes -PreviousLedgerBytes $progressLedgerBytes -FreshSeconds $ProgressFreshSeconds
                if ($progress.progressing -and [DateTime]::UtcNow -lt $execHardDeadlineUtc) {
                    $progressOutputBytes = $progress.output_bytes
                    $progressLedgerBytes = $progress.ledger_bytes
                    $deadlineUtc = [DateTime]::UtcNow.AddSeconds($ProgressExtensionSeconds)
                    if ($deadlineUtc -gt $execHardDeadlineUtc) { $deadlineUtc = $execHardDeadlineUtc }
                    Write-Log "EXEC_PROGRESSING pid=$($process.Id) reason=$($progress.reasons) next_deadline=$($deadlineUtc.ToString('o')) hard_deadline=$($execHardDeadlineUtc.ToString('o')) message=$($Message.Name)"
                } else {
                    $hungReason = if ([DateTime]::UtcNow -ge $execHardDeadlineUtc) { "hard_cap" } else { "no_progress" }
                    Write-Log "EXEC_HUNG pid=$($process.Id) reason=$hungReason action=terminate message=$($Message.Name)"
                    [void](Stop-LeaseProcessTree -Lease $lease -Reason "deadline")
                    if (-not $process.WaitForExit(2000)) { Write-Log "TREE_KILL_WAIT_TIMEOUT pid=$($process.Id) reason=deadline" }
                    break
                }
            }
            if ($PostDeliveryTimeoutSeconds -gt 0) {
                $deliveryEvidence = Get-OwnDeliveryEvidence -LedgerBytesBefore $ledgerBytesBefore -LedgerPrefixSha256Before $ledgerPrefixSha256Before
                if ($deliveryEvidence -and $null -eq $postDeliveryDeadlineUtc) {
                    $postDeliveryDeadlineUtc = [DateTime]::UtcNow.AddSeconds($PostDeliveryTimeoutSeconds)
                    $postDeliveryHardDeadlineUtc = $postDeliveryDeadlineUtc.AddSeconds($ProgressHardCapSeconds)
                    $progressOutputBytes = 0L
                    foreach ($progressPath in @($stdoutPath, $stderrPath)) {
                        if (Test-Path -LiteralPath $progressPath -PathType Leaf) { $progressOutputBytes += [long](Get-Item -LiteralPath $progressPath).Length }
                    }
                    $progressLedgerBytes = if (Test-Path -LiteralPath $eventsPath -PathType Leaf) { [long](Get-Item -LiteralPath $eventsPath).Length } else { 0L }
                    Write-Log "POST_DELIVERY_WINDOW_START pid=$($process.Id) timeout_seconds=$PostDeliveryTimeoutSeconds message=$($Message.Name)"
                } elseif ($null -ne $postDeliveryDeadlineUtc -and [DateTime]::UtcNow -gt $postDeliveryDeadlineUtc) {
                    $lease = Get-Content -LiteralPath $LeasePath -Raw -Encoding UTF8 | ConvertFrom-Json
                    $progress = Get-ExecProgressState -Lease $lease -StdoutPath $stdoutPath -StderrPath $stderrPath -EventsPath $eventsPath -PreviousOutputBytes $progressOutputBytes -PreviousLedgerBytes $progressLedgerBytes -FreshSeconds $ProgressFreshSeconds
                    if ($progress.progressing -and [DateTime]::UtcNow -lt $postDeliveryHardDeadlineUtc) {
                        $progressOutputBytes = $progress.output_bytes
                        $progressLedgerBytes = $progress.ledger_bytes
                        $postDeliveryDeadlineUtc = [DateTime]::UtcNow.AddSeconds($ProgressExtensionSeconds)
                        if ($postDeliveryDeadlineUtc -gt $postDeliveryHardDeadlineUtc) { $postDeliveryDeadlineUtc = $postDeliveryHardDeadlineUtc }
                        Write-Log "EXEC_PROGRESSING pid=$($process.Id) phase=post_delivery reason=$($progress.reasons) next_deadline=$($postDeliveryDeadlineUtc.ToString('o')) hard_deadline=$($postDeliveryHardDeadlineUtc.ToString('o')) message=$($Message.Name)"
                    } else {
                        $hungReason = if ([DateTime]::UtcNow -ge $postDeliveryHardDeadlineUtc) { "hard_cap" } else { "no_progress" }
                        Write-Log "POST_DELIVERY_TIMEOUT pid=$($process.Id) timeout_seconds=$PostDeliveryTimeoutSeconds action=terminate message=$($Message.Name)"
                        Write-Log "EXEC_HUNG pid=$($process.Id) phase=post_delivery reason=$hungReason action=terminate message=$($Message.Name)"
                        [void](Stop-LeaseProcessTree -Lease $lease -Reason "post_delivery")
                        if (-not $process.WaitForExit(2000)) { Write-Log "TREE_KILL_WAIT_TIMEOUT pid=$($process.Id) reason=post_delivery" }
                        break
                    }
                }
            }
        }
        $agentResponse = ""
        if (Test-Path -LiteralPath $stdoutPath) { $agentResponse = Get-Content -LiteralPath $stdoutPath -Raw -Encoding UTF8 }
        $invokerDiagnostics = ""
        if (Test-Path -LiteralPath $stderrPath) { $invokerDiagnostics = Get-Content -LiteralPath $stderrPath -Raw -Encoding UTF8 }
        $outcome = Get-ExecOutcomeClass -ExitCode $process.ExitCode -AgentResponse $agentResponse -InvokerDiagnostics $invokerDiagnostics -OwnEvidence (Get-OwnEvidence -LedgerBytesBefore $ledgerBytesBefore -LedgerPrefixSha256Before $ledgerPrefixSha256Before)
        Write-Log "EXEC_EXIT code=$($process.ExitCode) outcome=$outcome message=$($Message.Name)"
        $signature = Get-MessageSignature -Message $Message
        if ($outcome -in @("confirmed", "definitive")) {
            $seen = Read-Seen
            $seen[$Message.Name] = $signature
            Write-Seen -Seen $seen
            $retry = Read-RetryState
            if ($retry.ContainsKey($Message.Name)) { $retry.Remove($Message.Name); Write-RetryState -State $retry }
        } else {
            Restore-TransientExecResidue -HeadBefore $headBefore -IndexPatch $indexPatch -UntrackedBefore $untrackedBefore -LedgerHeadBefore $ledgerHeadBefore
            $retry = Read-RetryState
            $previous = if ($retry.ContainsKey($Message.Name) -and ([string]$retry[$Message.Name].signature -eq $signature)) { [int]$retry[$Message.Name].attempts } else { 0 }
            $attempt = $previous + 1
            $exhausted = $attempt -ge $MaxTransientRetries
            $retry[$Message.Name] = [ordered]@{ signature = $signature; attempts = $attempt; exhausted = $exhausted; outcome = $outcome; updated_at = [DateTime]::UtcNow.ToString("o") }
            Write-RetryState -State $retry
            if ($exhausted) {
                Write-Log "RETRY_EXHAUSTED attempts=$attempt signal=watchdog outcome=$outcome message=$($Message.Name)"
            } else {
                Write-Log "RETRY_SCHEDULED attempt=$attempt max=$MaxTransientRetries backoff_seconds=$RetryBackoffSeconds outcome=$outcome message=$($Message.Name)"
                if ($RetryBackoffSeconds -gt 0) { Start-Sleep -Seconds $RetryBackoffSeconds }
            }
        }
    } catch {
        Write-Log "EXEC_FAIL message=$($Message.Name) error=$($_.Exception.Message)"
        if ($ledgerHeadBefore -and $headBefore) { Restore-TransientExecResidue -HeadBefore $headBefore -IndexPatch $indexPatch -UntrackedBefore $untrackedBefore -LedgerHeadBefore $ledgerHeadBefore }
        $signature = Get-MessageSignature -Message $Message
        $retry = Read-RetryState
        $previous = if ($retry.ContainsKey($Message.Name) -and ([string]$retry[$Message.Name].signature -eq $signature)) { [int]$retry[$Message.Name].attempts } else { 0 }
        $attempt = $previous + 1
        $exhausted = $attempt -ge $MaxTransientRetries
        $retry[$Message.Name] = [ordered]@{ signature = $signature; attempts = $attempt; exhausted = $exhausted; outcome = "transient"; updated_at = [DateTime]::UtcNow.ToString("o") }
        Write-RetryState -State $retry
        if ($exhausted) { Write-Log "RETRY_EXHAUSTED attempts=$attempt signal=watchdog outcome=transient message=$($Message.Name)" }
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
# Resolve the agent executable ONCE at startup (fail-fast with a clear error instead of a
# perpetual LOOP_ERROR every interval when the CLI is missing -- F8, inherited failure mode).
$ResolvedAgentPath = Get-AgentExecutable
Clear-StaleCronLockIfSafe
if (Test-ExistingCronInstance) {
    Write-Log "INSTANCE_ALREADY_RUNNING pid_file=$PidPath; exiting."
    exit 0
}
Write-CronPid
if (Test-Path -LiteralPath $StopPath) {
    Remove-Item -LiteralPath $StopPath -Force
}
Write-Log "$PeerId mailbox cron started. root=$Root agent=$ResolvedAgentPath interval_seconds=$IntervalSeconds max_no_coordinator_rounds=$MaxNoCoordinatorRounds effort=$ReasoningEffort prompt=$PromptFile"

while ($true) {
    if (Test-Path -LiteralPath $StopPath) {
        Write-Log "Stop marker detected; exiting."
        exit 0
    }

    try {
        if (Test-CoordinatorStopOrder) {
            Write-Log "$CoordinatorId stop order detected; exiting."
            exit 0
        }

        $coordinatorResponses = @(Get-CoordinatorResponsesToPeer)
        if ($coordinatorResponses.Count -gt 0) {
            $NoCoordinatorRounds = 0
            Write-Log "$CoordinatorId responses detected count=$($coordinatorResponses.Count)"
        } else {
            $NoCoordinatorRounds += 1
            Write-Log "No $CoordinatorId response round=$NoCoordinatorRounds"
            if ($NoCoordinatorRounds -ge $MaxNoCoordinatorRounds) {
                Write-Log "No $CoordinatorId response limit reached; exiting."
                exit 0
            }
        }

        $messages = @(Get-ProcessablePeerMessages)
        if ($messages.Count -eq 0) {
            Write-Log "Heartbeat processable_messages=0"
        } else {
            foreach ($message in $messages) {
                Invoke-PeerForMessage -Message $message
            }
        }
    } catch {
        Write-Log "LOOP_ERROR $($_.Exception.Message)"
    }

    Start-Sleep -Seconds $IntervalSeconds
}
