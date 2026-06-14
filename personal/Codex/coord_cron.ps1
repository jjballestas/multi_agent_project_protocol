param(
    [int]$IntervalSeconds = 300,
    [string]$Root = "D:\Agentes\multi_agent_project_protocol"
)

$ErrorActionPreference = "Stop"
$log = Join-Path $Root "personal\Codex\coord_cron.log"
$stop = Join-Path $Root "personal\Codex\coord_cron.stop"

function Write-CoordLog {
    param([string]$Message)
    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    Add-Content -LiteralPath $log -Value "$timestamp $Message" -Encoding ASCII
}

Write-CoordLog "START interval_seconds=$IntervalSeconds root=$Root"

while (-not (Test-Path -LiteralPath $stop)) {
    try {
        $open = Get-ChildItem -LiteralPath (Join-Path $Root "Area_comun\mailbox\open") -File |
            Select-Object -ExpandProperty Name
        $status = git -C $Root status --short
        $openText = if ($open) { ($open -join ",") } else { "<none>" }
        $statusCount = if ($status) { @($status).Count } else { 0 }
        Write-CoordLog "heartbeat mailbox_open=$openText dirty_entries=$statusCount"
    }
    catch {
        Write-CoordLog "ERROR $($_.Exception.Message)"
    }
    Start-Sleep -Seconds $IntervalSeconds
}

Write-CoordLog "STOP stop_file=$stop"
