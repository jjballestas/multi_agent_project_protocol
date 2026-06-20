param(
    [int]$IntervalSeconds = 180
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$LogPath = Join-Path $PSScriptRoot "carril_a_coord_monitor.log"
$PidPath = Join-Path $PSScriptRoot "carril_a_coord_monitor.pid"
$StopPath = Join-Path $PSScriptRoot "carril_a_coord_monitor.stop"
$DonePath = Join-Path $PSScriptRoot "carril_a_coord_monitor.done"

$OriginalOpen = Join-Path $Root "Area_comun\mailbox\open\MSG-20260619-Codex-to-Arquitecto-carril-A-review.md"
$OriginalAnswered = Join-Path $Root "Area_comun\mailbox\answered\MSG-20260619-Codex-to-Arquitecto-carril-A-review.md"
$OriginalArchived = Join-Path $Root "Area_comun\mailbox\archived\MSG-20260619-Codex-to-Arquitecto-carril-A-review.md"

function Write-Log {
    param([string]$Message)
    $stamp = (Get-Date).ToString("s")
    Add-Content -LiteralPath $LogPath -Value "$stamp $Message" -Encoding UTF8
}

function Get-ArquitectoResponses {
    $mailboxRoot = Join-Path $Root "Area_comun\mailbox"
    $folders = @("open", "answered", "archived")
    $files = @()
    foreach ($folder in $folders) {
        $dir = Join-Path $mailboxRoot $folder
        if (Test-Path -LiteralPath $dir) {
            $files += @(Get-ChildItem -LiteralPath $dir -File -Filter "MSG-*.md")
        }
    }
    @($files | Where-Object {
        $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
        ($content -match "(?im)^from:\s*Arquitecto\s*$") -and
        ($content -match "(?im)^to:\s*(Codex|operador humano|Operador|Arquitecto)\s*$") -and
        (
            $_.Name -match "(?i)carril.?a" -or
            $content -match "(?i)carril\s*a|DECISION-0039|DECISION-0040|DECISION-0041|SPEC-0081|GATE-DATASET|atestacion"
        )
    })
}

function Test-Agreement {
    param([System.IO.FileInfo[]]$Responses)
    foreach ($response in $Responses) {
        $content = Get-Content -LiteralPath $response.FullName -Raw -Encoding UTF8
        if ($content -match "(?im)^requires_response:\s*(true|yes)\s*$") {
            continue
        }
        if ($content -match "(?i)acuerdo\s+cerrado|objeciones\s+cerradas|ajustes\s+aplicados|codex\s+concurre|carril\s*a\s+cerrado|coordinacion\s+cerrada") {
            return $true
        }
    }
    return $false
}

function Set-MailboxStatus {
    param(
        [string]$Path,
        [string]$Status
    )
    $content = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if ($content -match "(?m)^status:\s*\S+\s*$") {
        $content = [regex]::Replace($content, "(?m)^status:\s*\S+\s*$", "status: $Status", 1)
    } else {
        $content = $content -replace "---\s*\r?\n", "---`nstatus: $Status`n"
    }
    Set-Content -LiteralPath $Path -Value $content -Encoding UTF8
}

function Submit-Claim {
    param(
        [string]$Op,
        [string[]]$Scope
    )
    $claimId = "CLAIM-20260619-Codex-carril-A-monitor"
    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $intentPath = Join-Path $PSScriptRoot "carril_a_monitor_${Op}_intent.json"
    if ($Op -eq "acquire") {
        $payload = @{
            claim = @{
                op = "acquire"
                claim = @{
                    claim_id = $claimId
                    task_id = "COORD-20260619-CARRIL-A-MONITOR"
                    owner = "Codex"
                    scope = $Scope
                    started_at = $timestamp
                    updated_at = $timestamp
                    expires_at = (Get-Date).ToUniversalTime().AddHours(2).ToString("yyyy-MM-ddTHH:mm:ssZ")
                    status = "active"
                    notes = "Carril A monitor hygiene after Arquitecto/Codex agreement."
                }
                idempotency_key = "codex-carril-a-monitor-acquire-$timestamp"
            }
        }
    } else {
        $payload = @{
            claim = @{
                op = "release"
                claim_id = $claimId
                idempotency_key = "codex-carril-a-monitor-release-$timestamp"
            }
        }
    }
    $payload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $intentPath -Encoding UTF8
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

function Invoke-Hygiene {
    param([System.IO.FileInfo[]]$Responses)
    $scope = @(
        "Area_comun/state/CLAIMS.json",
        "runtime/state/events.jsonl",
        "runtime/state/snapshot.json"
    )
    if (Test-Path -LiteralPath $OriginalOpen) {
        $scope += "Area_comun/mailbox/open/MSG-20260619-Codex-to-Arquitecto-carril-A-review.md"
        $scope += "Area_comun/mailbox/answered/MSG-20260619-Codex-to-Arquitecto-carril-A-review.md"
    }
    foreach ($response in $Responses) {
        $relative = $response.FullName.Substring($Root.Length + 1).Replace("\", "/")
        $scope += $relative
        $scope += ("Area_comun/mailbox/archived/" + $response.Name)
    }

    Submit-Claim -Op "acquire" -Scope $scope
    try {
        if (Test-Path -LiteralPath $OriginalOpen) {
            Set-MailboxStatus -Path $OriginalOpen -Status "answered"
            Move-Item -LiteralPath $OriginalOpen -Destination $OriginalAnswered -Force
            Write-Log "Moved Codex review message to answered."
        }
        foreach ($response in $Responses) {
            if (-not (Test-Path -LiteralPath $response.FullName)) {
                continue
            }
            $content = Get-Content -LiteralPath $response.FullName -Raw -Encoding UTF8
            $doesNotRequireResponse = $content -match "(?im)^requires_response:\s*(false|no)\s*$"
            if ($doesNotRequireResponse) {
                Set-MailboxStatus -Path $response.FullName -Status "archived"
                $destination = Join-Path $Root ("Area_comun\mailbox\archived\" + $response.Name)
                Move-Item -LiteralPath $response.FullName -Destination $destination -Force
                Write-Log "Archived non-blocking Arquitecto response $($response.Name)."
            }
        }
    } finally {
        Submit-Claim -Op "release" -Scope @()
    }
}

function Invoke-RestorePendingRequests {
    param([System.IO.FileInfo[]]$Responses)
    $pending = @($Responses | Where-Object {
        $_.FullName -match "\\mailbox\\archived\\" -and
        ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^to:\s*Codex\s*$") -and
        ((Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?im)^requires_response:\s*(true|yes)\s*$")
    })
    if (-not $pending) {
        return
    }

    foreach ($response in $pending) {
        $scope = @(
            "Area_comun/state/CLAIMS.json",
            "runtime/state/events.jsonl",
            "runtime/state/snapshot.json",
            ("Area_comun/mailbox/archived/" + $response.Name),
            ("Area_comun/mailbox/open/" + $response.Name)
        )
        try {
            Submit-Claim -Op "acquire" -Scope $scope
            try {
                Set-MailboxStatus -Path $response.FullName -Status "open"
                $destination = Join-Path $Root ("Area_comun\mailbox\open\" + $response.Name)
                Move-Item -LiteralPath $response.FullName -Destination $destination -Force
                Write-Log "Restored pending Arquitecto request $($response.Name) to open."
            } finally {
                Submit-Claim -Op "release" -Scope @()
            }
        } catch {
            Write-Log "Pending request restore blocked for $($response.Name): $($_.Exception.Message)"
        }
    }
}

Set-Content -LiteralPath $PidPath -Value $PID -Encoding ASCII
Write-Log "Carril A coordination monitor started. interval_seconds=$IntervalSeconds"

while ($true) {
    if (Test-Path -LiteralPath $StopPath) {
        Write-Log "Stop marker detected; exiting."
        exit 0
    }

    $responses = Get-ArquitectoResponses
    Invoke-RestorePendingRequests -Responses $responses
    $responses = Get-ArquitectoResponses

    if (Test-Agreement -Responses $responses) {
        Write-Log "Strict agreement detected; attempting hygiene and stopping only if successful."
        try {
            Invoke-Hygiene -Responses $responses
            Set-Content -LiteralPath $DonePath -Value "done" -Encoding ASCII
            exit 0
        } catch {
            Write-Log "Hygiene blocked: $($_.Exception.Message)"
        }
    }

    Write-Log "No agreement detected; sleeping."
    Start-Sleep -Seconds $IntervalSeconds
}
